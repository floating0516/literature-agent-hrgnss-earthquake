#!/usr/bin/env python3
"""Match locally downloaded PDFs back to paper metadata.

Compliance boundary:
- only scans local PDF files the user already has;
- does not download, scrape, or access publisher websites;
- does not bypass paywalls, CAPTCHA, Cloudflare, or access controls.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.download_pdfs import (
    BASE_DIR,
    DEFAULT_INPUT,
    DEFAULT_OUTPUT,
    DEFAULT_PDF_DIR,
    display_path,
    load_jsonl,
    make_pdf_filename,
    write_jsonl,
)

DEFAULT_MANUAL_DIR = BASE_DIR / "papers" / "manual_pdf_inbox"
DEFAULT_LOG = BASE_DIR / "papers" / "manual_pdf_match_log.md"
DEFAULT_STATUSES = frozenset({"failed", "manual_required"})
TITLE_MATCH_THRESHOLD = 0.82
TITLE_MATCH_MARGIN = 0.15


@dataclass(frozen=True)
class ManualMatchConfig:
    input_path: Path = DEFAULT_INPUT
    results_path: Path = DEFAULT_OUTPUT
    manual_dir: Path = DEFAULT_MANUAL_DIR
    pdf_dir: Path = DEFAULT_PDF_DIR
    log_path: Path = DEFAULT_LOG
    apply: bool = False
    overwrite: bool = False
    recursive: bool = False
    only_status: frozenset[str] = DEFAULT_STATUSES
    require_doi: bool = False


@dataclass(frozen=True)
class PdfProbe:
    path: Path
    text: str
    doi_candidates: frozenset[str]


@dataclass(frozen=True)
class MatchScore:
    record_index: int
    score: float
    method: str
    confidence: str
    note: str


@dataclass(frozen=True)
class MatchAction:
    source_pdf: Path
    record_index: int | None
    status: str
    target_pdf: Path | None = None
    method: str = ""
    confidence: str = ""
    note: str = ""


def normalize_doi(value: str | None) -> str:
    if not value:
        return ""
    normalized = value.strip().lower()
    normalized = re.sub(r"^https?://(dx\.)?doi\.org/", "", normalized)
    normalized = re.sub(r"^doi\s*:\s*", "", normalized)
    normalized = normalized.strip(" \t\n\r<>.,;)]")
    return normalized


def extract_doi_candidates(text: str) -> set[str]:
    candidates: set[str] = set()
    doi_pattern = r"10[._][0-9]{4,9}(?:[._/][A-Za-z0-9][A-Za-z0-9._;()/:+-]*)?"
    for match in re.finditer(doi_pattern, text, flags=re.IGNORECASE):
        candidate = match.group(0).replace("_", "/", 1)
        candidate = candidate.strip(".,;:)]}")
        normalized = normalize_doi(candidate)
        if normalized:
            candidates.add(normalized)
    return candidates


def normalize_title(value: str | None) -> str:
    if not value:
        return ""
    normalized = value.lower()
    normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def title_tokens(value: str | None) -> set[str]:
    return {token for token in normalize_title(value).split() if len(token) > 2}


def score_title_match(text: str, record: dict[str, Any]) -> float:
    record_title = normalize_title(record.get("title"))
    candidate_text = normalize_title(text)
    if not record_title or not candidate_text:
        return 0.0

    record_tokens = title_tokens(record_title)
    candidate_tokens = title_tokens(candidate_text)
    if not record_tokens or not candidate_tokens:
        return 0.0

    overlap = len(record_tokens & candidate_tokens) / len(record_tokens)
    substring_bonus = 0.15 if record_title in candidate_text or candidate_text in record_title else 0.0
    year = record.get("year")
    year_bonus = 0.1 if year and str(year) in candidate_text else 0.0
    return min(1.0, overlap + substring_bonus + year_bonus)


def extract_pdf_text(pdf_path: Path) -> str:
    try:
        result = subprocess.run(
            ["pdftotext", "-f", "1", "-l", "1", "-layout", "-enc", "UTF-8", str(pdf_path), "-"],
            check=True,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return ""
    return result.stdout[:12000]


def build_pdf_probe(pdf_path: Path) -> PdfProbe:
    filename_text = pdf_path.stem.replace("_", " ").replace("-", " ")
    raw_filename_text = pdf_path.stem
    pdf_text = extract_pdf_text(pdf_path)
    combined_text = f"{raw_filename_text}\n{filename_text}\n{pdf_text}"
    return PdfProbe(
        path=pdf_path,
        text=combined_text,
        doi_candidates=frozenset(extract_doi_candidates(combined_text)),
    )


def score_record_match(probe: PdfProbe, record: dict[str, Any], record_index: int, *, require_doi: bool = False) -> MatchScore | None:
    record_doi = normalize_doi(record.get("doi"))
    if record_doi and record_doi in probe.doi_candidates:
        return MatchScore(
            record_index=record_index,
            score=1.0,
            method="doi_exact",
            confidence="high",
            note="DOI matched exactly",
        )

    if require_doi:
        return None

    title_score = score_title_match(probe.text, record)
    if title_score >= TITLE_MATCH_THRESHOLD:
        return MatchScore(
            record_index=record_index,
            score=title_score,
            method="title_year_strong",
            confidence="medium",
            note="Title and year matched strongly",
        )

    return None


def choose_unique_match(probe: PdfProbe, records: list[dict[str, Any]], *, require_doi: bool = False) -> MatchScore | str | None:
    scores = [
        score
        for index, record in enumerate(records)
        if (score := score_record_match(probe, record, index, require_doi=require_doi)) is not None
    ]
    if not scores:
        return None

    scores.sort(key=lambda item: item.score, reverse=True)
    if len(scores) == 1:
        return scores[0]

    best = scores[0]
    second = scores[1]
    if best.method == "doi_exact" and second.method != "doi_exact":
        return best
    if best.score - second.score >= TITLE_MATCH_MARGIN:
        return best
    return "ambiguous"


def records_for_matching(records: list[dict[str, Any]], statuses: frozenset[str]) -> list[dict[str, Any]]:
    return [record for record in records if record.get("download_status") in statuses]


def scan_manual_pdfs(config: ManualMatchConfig) -> list[Path]:
    if not config.manual_dir.exists():
        return []
    pattern = "**/*.pdf" if config.recursive else "*.pdf"
    return sorted(path for path in config.manual_dir.glob(pattern) if path.is_file())


def build_updated_record(record: dict[str, Any], action: MatchAction) -> dict[str, Any]:
    updated = dict(record)
    updated["download_status"] = "matched_manual"
    updated["downloaded_pdf"] = display_path(action.target_pdf)
    updated["download_source"] = "manual_pdf"
    updated["manual_pdf_source"] = display_path(action.source_pdf)
    updated["manual_match_method"] = action.method
    updated["manual_match_confidence"] = action.confidence
    updated["download_note"] = "Matched from manually downloaded PDF"
    return updated


def action_for_probe(probe: PdfProbe, records: list[dict[str, Any]], eligible_indexes: list[int], config: ManualMatchConfig) -> MatchAction:
    eligible_records = [records[index] for index in eligible_indexes]
    decision = choose_unique_match(probe, eligible_records, require_doi=config.require_doi)
    if decision is None:
        return MatchAction(source_pdf=probe.path, record_index=None, status="unmatched", note="No matching metadata record")
    if decision == "ambiguous":
        return MatchAction(source_pdf=probe.path, record_index=None, status="ambiguous", note="Multiple matching metadata records")

    assert isinstance(decision, MatchScore)
    record_index = eligible_indexes[decision.record_index]
    target_pdf = config.pdf_dir / make_pdf_filename(records[record_index])
    if target_pdf.exists() and not config.overwrite:
        return MatchAction(
            source_pdf=probe.path,
            record_index=record_index,
            status="skipped_existing",
            target_pdf=target_pdf,
            method=decision.method,
            confidence=decision.confidence,
            note="Target PDF already exists",
        )

    return MatchAction(
        source_pdf=probe.path,
        record_index=record_index,
        status="matched",
        target_pdf=target_pdf,
        method=decision.method,
        confidence=decision.confidence,
        note=decision.note,
    )


def write_match_log(log_path: Path, actions: list[MatchAction], records: list[dict[str, Any]], config: ManualMatchConfig) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    counts = summarize_actions(actions)
    lines = [
        "# 手动 PDF 匹配记录",
        "",
        "> 该文件由 `scripts/match_manual_pdfs.py` 生成。仅匹配用户已经合法获得的本地 PDF，不联网、不绕过访问控制。",
        "",
        "## 总览",
        "",
        f"- 模式：{'apply' if config.apply else 'dry-run'}",
        f"- 手动 PDF 目录：{display_path(config.manual_dir)}",
        f"- PDF 输出目录：{display_path(config.pdf_dir)}",
        f"- 结果文件：{display_path(config.results_path)}",
        f"- 扫描 PDF：{len(actions)}",
        f"- 自动匹配：{counts['matched']}",
        f"- 歧义：{counts['ambiguous']}",
        f"- 未匹配：{counts['unmatched']}",
        f"- 已存在跳过：{counts['skipped_existing']}",
        "",
        "## 明细",
        "",
        "| Source PDF | Matched Title | Year | Status | Target PDF | Method | Confidence | Note |",
        "|---|---|---:|---|---|---|---|---|",
    ]
    for action in actions:
        record = records[action.record_index] if action.record_index is not None else {}
        title = (record.get("title") or "").replace("|", "\\|")
        year = record.get("year") or ""
        note = action.note.replace("|", "\\|").replace("\n", " ")
        lines.append(
            "| "
            f"{display_path(action.source_pdf)} | {title} | {year} | {action.status} | "
            f"{display_path(action.target_pdf) or ''} | {action.method} | {action.confidence} | {note} |"
        )
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def summarize_actions(actions: list[MatchAction]) -> dict[str, int]:
    return {
        "matched": sum(1 for action in actions if action.status == "matched"),
        "ambiguous": sum(1 for action in actions if action.status == "ambiguous"),
        "unmatched": sum(1 for action in actions if action.status == "unmatched"),
        "skipped_existing": sum(1 for action in actions if action.status == "skipped_existing"),
    }


def load_records_for_run(config: ManualMatchConfig) -> list[dict[str, Any]]:
    if config.results_path.exists():
        return load_jsonl(config.results_path)
    return load_jsonl(config.input_path)


def match_manual_pdfs(config: ManualMatchConfig) -> dict[str, int]:
    records = load_records_for_run(config)
    eligible_indexes = [
        index for index, record in enumerate(records) if record.get("download_status") in config.only_status
    ]
    actions = [
        action_for_probe(build_pdf_probe(pdf_path), records, eligible_indexes, config)
        for pdf_path in scan_manual_pdfs(config)
    ]

    if config.apply:
        updated_records = list(records)
        for action in actions:
            if action.status != "matched" or action.record_index is None or action.target_pdf is None:
                continue
            action.target_pdf.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(action.source_pdf, action.target_pdf)
            updated_records[action.record_index] = build_updated_record(records[action.record_index], action)
        write_jsonl(config.results_path, updated_records)

    write_match_log(config.log_path, actions, records, config)
    return summarize_actions(actions)


def parse_statuses(raw_statuses: str) -> frozenset[str]:
    return frozenset(status.strip() for status in raw_statuses.split(",") if status.strip())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Match locally downloaded PDFs back to paper metadata.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--results", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--manual-dir", type=Path, required=True)
    parser.add_argument("--pdf-dir", type=Path, default=DEFAULT_PDF_DIR)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--dry-run", action="store_true", help="Preview matches without copying PDFs or updating results.")
    parser.add_argument("--apply", action="store_true", help="Copy matched PDFs and update results.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing canonical PDFs.")
    parser.add_argument("--recursive", action="store_true", help="Scan manual-dir recursively.")
    parser.add_argument("--only-status", default="failed,manual_required")
    parser.add_argument("--require-doi", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = ManualMatchConfig(
        input_path=args.input,
        results_path=args.results,
        manual_dir=args.manual_dir,
        pdf_dir=args.pdf_dir,
        log_path=args.log,
        apply=bool(args.apply and not args.dry_run),
        overwrite=args.overwrite,
        recursive=args.recursive,
        only_status=parse_statuses(args.only_status),
        require_doi=args.require_doi,
    )
    summary = match_manual_pdfs(config)
    print(f"Scanned manual PDFs: {sum(summary.values())}")
    print(f"Matched: {summary['matched']}")
    print(f"Ambiguous: {summary['ambiguous']}")
    print(f"Unmatched: {summary['unmatched']}")
    print(f"Skipped existing: {summary['skipped_existing']}")
    print(f"Wrote log to {config.log_path}")
    if config.apply:
        print(f"Updated results at {config.results_path}")
    else:
        print("Dry run only; results were not updated")


if __name__ == "__main__":
    main()
