#!/usr/bin/env python3
"""Download open-access PDFs listed in paper metadata.

Compliance boundary:
- only download PDF URLs already present in metadata;
- if no open PDF URL is available, mark the record as manual_required;
- do not attempt paywall bypasses, scraping tricks, or institution-only flows.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = BASE_DIR / "papers" / "selected_papers.jsonl"
DEFAULT_OUTPUT = BASE_DIR / "papers" / "download_results.jsonl"
DEFAULT_LOG = BASE_DIR / "papers" / "pdf_download_log.md"
DEFAULT_PDF_DIR = BASE_DIR / "papers" / "raw_pdf"
SLUG_WORD_LIMIT = 8


@dataclass(frozen=True)
class DownloadConfig:
    input_path: Path = DEFAULT_INPUT
    output_path: Path = DEFAULT_OUTPUT
    log_path: Path = DEFAULT_LOG
    pdf_dir: Path = DEFAULT_PDF_DIR
    timeout: int = 60
    overwrite: bool = False


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records



def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")



def choose_pdf_url(record: dict[str, Any]) -> str | None:
    pdf_url = record.get("pdf_url")
    if pdf_url:
        return pdf_url

    best_oa_location = record.get("best_oa_location") or {}
    best_pdf_url = best_oa_location.get("pdf_url")
    if best_pdf_url:
        return best_pdf_url

    return None



def slugify(value: str | None) -> str:
    if not value:
        return ""
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = value.strip("_")
    value = re.sub(r"_+", "_", value)
    return value



def make_pdf_filename(record: dict[str, Any]) -> str:
    year = record.get("year")
    title_slug = slugify(record.get("title"))
    doi_slug = slugify(record.get("doi"))

    if title_slug:
        title_slug = "_".join(title_slug.split("_")[:SLUG_WORD_LIMIT])
        stem = f"{year}_{title_slug}" if year else title_slug
    elif doi_slug:
        stem = doi_slug
    else:
        stem = slugify(record.get("paper_id")) or "paper"

    return f"{stem}.pdf"



def unique_record_suffix(record: dict[str, Any]) -> str:
    for key in ("doi", "openalex_id", "paper_id"):
        slug = slugify(record.get(key))
        if slug:
            return slug[:24]
    return ""



def target_pdf_path(record: dict[str, Any], output_dir: Path) -> Path:
    base_path = output_dir / make_pdf_filename(record)
    if not base_path.exists():
        return base_path

    suffix = unique_record_suffix(record)
    if not suffix:
        return base_path

    return base_path.with_name(f"{base_path.stem}_{suffix}{base_path.suffix}")



def is_pdf_response(content_type: str | None, data: bytes) -> bool:
    normalized_type = (content_type or "").lower()
    return "pdf" in normalized_type or data.startswith(b"%PDF")



def result_for(record: dict[str, Any], *, status: str, pdf_path: Path | None = None, note: str | None = None) -> dict[str, Any]:
    result = dict(record)
    result["selected_pdf_url"] = choose_pdf_url(record)
    result["download_status"] = status
    result["downloaded_pdf"] = f"papers/raw_pdf/{pdf_path.name}" if pdf_path else None
    if note is not None:
        result["download_note"] = note
    return result



def download_pdf(record: dict[str, Any], config: DownloadConfig) -> dict[str, Any]:
    pdf_url = choose_pdf_url(record)
    if not pdf_url:
        return result_for(record, status="manual_required", note="No open PDF URL in metadata")

    config.pdf_dir.mkdir(parents=True, exist_ok=True)
    base_pdf_path = config.pdf_dir / make_pdf_filename(record)
    if base_pdf_path.exists():
        pdf_path = target_pdf_path(record, config.pdf_dir)
        if pdf_path.exists() and not config.overwrite:
            return result_for(record, status="skipped_existing", pdf_path=pdf_path, note="PDF already exists")
    else:
        pdf_path = base_pdf_path

    request = urllib.request.Request(
        pdf_url,
        headers={"User-Agent": "AI-Agent-Reading/0.1 (open-access-pdf-downloader)"},
    )

    try:
        with urllib.request.urlopen(request, timeout=config.timeout) as response:
            data = response.read()
            content_type = response.headers.get("Content-Type")
    except (HTTPError, URLError, TimeoutError, ValueError, OSError) as exc:
        return result_for(record, status="failed", note=str(exc))

    if not is_pdf_response(content_type, data):
        return result_for(record, status="failed", note=f"Non-PDF response: {content_type or 'unknown content type'}")

    try:
        pdf_path.write_bytes(data)
    except OSError as exc:
        return result_for(record, status="failed", note=str(exc))

    return result_for(record, status="downloaded", pdf_path=pdf_path)



def write_markdown_log(log_path: Path, results: list[dict[str, Any]]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    downloaded = sum(1 for item in results if item.get("download_status") == "downloaded")
    skipped_existing = sum(1 for item in results if item.get("download_status") == "skipped_existing")
    manual_required = sum(1 for item in results if item.get("download_status") == "manual_required")
    failed = sum(1 for item in results if item.get("download_status") == "failed")

    lines = [
        "# PDF 下载记录",
        "",
        "> 该文件由 `scripts/download_pdfs.py` 生成。仅下载元数据中已提供的开放 PDF URL。",
        "",
        "## 总览",
        "",
        f"- 下载成功：{downloaded}",
        f"- 已存在跳过：{skipped_existing}",
        f"- 需要人工处理：{manual_required}",
        f"- 下载失败：{failed}",
        "",
        "## 明细",
        "",
        "| Title | Year | Status | PDF | URL | Note |",
        "|---|---:|---|---|---|---|",
    ]

    for item in results:
        title = (item.get("title") or "").replace("|", "\\|")
        year = item.get("year") or ""
        status = item.get("download_status") or ""
        pdf = item.get("downloaded_pdf") or ""
        url = item.get("selected_pdf_url") or ""
        note = (item.get("download_note") or "").replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {title} | {year} | {status} | {pdf} | {url} | {note} |")

    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")



def run(config: DownloadConfig) -> list[dict[str, Any]]:
    records = load_jsonl(config.input_path)
    results = [download_pdf(record, config) for record in records]
    write_jsonl(config.output_path, results)
    write_markdown_log(config.log_path, results)
    return results



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download open-access PDFs from existing metadata URLs.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Input JSONL metadata path.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output JSONL result path.")
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG, help="Markdown log path.")
    parser.add_argument("--pdf-dir", type=Path, default=DEFAULT_PDF_DIR, help="Directory for downloaded PDFs.")
    parser.add_argument("--timeout", type=int, default=60, help="HTTP timeout in seconds.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing PDFs.")
    return parser.parse_args()



def main() -> None:
    args = parse_args()
    config = DownloadConfig(
        input_path=args.input,
        output_path=args.output,
        log_path=args.log,
        pdf_dir=args.pdf_dir,
        timeout=args.timeout,
        overwrite=args.overwrite,
    )
    results = run(config)
    print(f"Processed {len(results)} records")
    print(f"Wrote results to {config.output_path}")
    print(f"Wrote log to {config.log_path}")


if __name__ == "__main__":
    main()
