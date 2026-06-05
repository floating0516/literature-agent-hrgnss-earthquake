#!/usr/bin/env python3
"""Evaluate parsed PDF Markdown quality before RAG ingestion."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = BASE_DIR / "papers" / "parsed_md"
DEFAULT_OUTPUT = BASE_DIR / "papers" / "parse_quality.jsonl"
DEFAULT_REPORT = BASE_DIR / "papers" / "parse_quality_report.md"
DEFAULT_MIN_SCORE = 60

HEADING_RE = re.compile(r"^#{1,6}\s+", re.MULTILINE)
SOURCE_RE = re.compile(r">\s*Source PDF:\s*`([^`]+)`")
PARSER_RE = re.compile(r">\s*Parser:\s*`([^`]+)`")
REFERENCE_RE = re.compile(r"^#{1,6}\s+(references|bibliography|参考文献)\b", re.IGNORECASE | re.MULTILINE)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(BASE_DIR))
    except ValueError:
        return str(path)


def extract_title(markdown: str, path: Path) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def extract_body(markdown: str) -> str:
    if "---" in markdown:
        return markdown.split("---", 1)[1].strip()
    return markdown.strip()


def reference_section_ratio(body: str) -> float:
    match = REFERENCE_RE.search(body)
    if not match or not body.strip():
        return 0.0
    return len(body[match.start() :].strip()) / max(len(body.strip()), 1)


def short_line_ratio(lines: list[str]) -> float:
    non_empty = [line.strip() for line in lines if line.strip()]
    if not non_empty:
        return 1.0
    short_lines = [line for line in non_empty if len(line) < 35]
    return len(short_lines) / len(non_empty)


def garbled_char_ratio(text: str) -> float:
    if not text:
        return 1.0
    garbled = sum(1 for ch in text if ch in {"�", "□", "■", "�"})
    unusual = len(re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", text))
    return (garbled + unusual) / len(text)


def status_for(score: int, min_score: int) -> str:
    if score < min_score:
        return "fail"
    if score < 80:
        return "warn"
    return "pass"


def evaluate_markdown(path: Path, min_score: int = DEFAULT_MIN_SCORE) -> dict[str, Any]:
    markdown = path.read_text(encoding="utf-8", errors="replace")
    body = extract_body(markdown)
    lines = body.splitlines()
    source_match = SOURCE_RE.search(markdown)
    parser_match = PARSER_RE.search(markdown)

    metrics = {
        "char_count": len(body),
        "line_count": len(lines),
        "heading_count": len(HEADING_RE.findall(body)),
        "short_line_ratio": round(short_line_ratio(lines), 4),
        "garbled_char_ratio": round(garbled_char_ratio(body), 4),
        "reference_section_ratio": round(reference_section_ratio(body), 4),
    }
    checks = {
        "has_body": metrics["char_count"] > 0,
        "min_length_pass": metrics["char_count"] >= 400,
        "has_structure": metrics["heading_count"] >= 2,
        "low_garbled_ratio": metrics["garbled_char_ratio"] <= 0.01,
        "low_reference_ratio": metrics["reference_section_ratio"] <= 0.35,
        "low_short_line_ratio": metrics["short_line_ratio"] <= 0.65,
        "has_parser_metadata": parser_match is not None,
        "has_source_pdf_metadata": source_match is not None,
    }

    score = 100
    reasons: list[str] = []
    penalties = [
        ("has_body", 40, "document body is empty"),
        ("min_length_pass", 35, "document body is too short"),
        ("has_structure", 10, "too few Markdown headings"),
        ("low_garbled_ratio", 25, "garbled character ratio is high"),
        ("low_reference_ratio", 25, "reference section dominates document"),
        ("low_short_line_ratio", 10, "too many very short lines"),
        ("has_parser_metadata", 5, "missing parser metadata"),
        ("has_source_pdf_metadata", 5, "missing source PDF metadata"),
    ]
    for check, penalty, reason in penalties:
        if not checks[check]:
            score -= penalty
            reasons.append(reason)
    score = max(0, score)

    return {
        "source_file": display_path(path),
        "source_pdf": source_match.group(1) if source_match else "",
        "title": extract_title(markdown, path),
        "parser": parser_match.group(1) if parser_match else "",
        "score": score,
        "status": status_for(score, min_score),
        "checks": checks,
        "metrics": metrics,
        "reasons": reasons,
    }


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_report(path: Path, records: list[dict[str, Any]], output_path: Path) -> None:
    counts = {status: sum(1 for record in records if record["status"] == status) for status in ["pass", "warn", "fail"]}
    lines = [
        "# PDF 解析质量报告",
        "",
        "> 该文件由 `scripts/evaluate_parse_quality.py` 生成，用于在 PDF→RAG 之间检查解析质量。",
        "",
        "## 总览",
        "",
        f"- JSONL 输出：`{display_path(output_path)}`",
        f"- 文件数：{len(records)}",
        f"- pass：{counts['pass']}",
        f"- warn：{counts['warn']}",
        f"- fail：{counts['fail']}",
        "",
        "## 明细",
        "",
        "| Parsed Markdown | Status | Score | Parser | Reasons |",
        "|---|---|---:|---|---|",
    ]
    for record in records:
        reasons = "; ".join(record["reasons"]).replace("|", "\\|")
        lines.append(
            f"| `{record['source_file']}` | {record['status']} | {record['score']} | "
            f"{record['parser']} | {reasons} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    input_dir: Path = DEFAULT_INPUT_DIR,
    output_path: Path = DEFAULT_OUTPUT,
    report_path: Path = DEFAULT_REPORT,
    min_score: int = DEFAULT_MIN_SCORE,
) -> list[dict[str, Any]]:
    md_paths = sorted(input_dir.glob("*.md"))
    records = [evaluate_markdown(path, min_score=min_score) for path in md_paths]
    write_jsonl(output_path, records)
    write_report(report_path, records, output_path)
    print(f"Evaluated {len(records)} parsed Markdown files")
    print(f"Wrote quality JSONL to {output_path}")
    print(f"Wrote quality report to {report_path}")
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate parsed PDF Markdown quality before RAG ingestion.")
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--min-score", type=int, default=DEFAULT_MIN_SCORE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(input_dir=args.input_dir, output_path=args.output, report_path=args.report, min_score=args.min_score)


if __name__ == "__main__":
    main()
