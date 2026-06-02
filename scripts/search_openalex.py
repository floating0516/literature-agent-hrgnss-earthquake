#!/usr/bin/env python3
"""Lightweight OpenAlex search for literature-agent candidates.

This script intentionally starts simple:
- query OpenAlex only;
- collect metadata, OA status, and possible PDF URLs;
- do not download PDFs;
- save machine-readable JSONL plus a Markdown summary.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_QUERIES = [
    '"high-rate GNSS" earthquake early warning',
    '"geodetic earthquake early warning"',
    '"G-FAST" GNSS earthquake',
]

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = BASE_DIR / "papers" / "candidates.jsonl"
DEFAULT_SUMMARY = BASE_DIR / "papers" / "search_summary.md"


def fetch_openalex(query: str, per_page: int, mailto: str | None) -> tuple[list[dict[str, Any]], dict[str, Any], float]:
    params = {
        "search": query,
        "per-page": str(per_page),
        "sort": "cited_by_count:desc",
    }
    if mailto:
        params["mailto"] = mailto

    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": f"AI-Agent-Reading/0.1 ({mailto or 'no-email-provided'})"},
    )

    start = time.perf_counter()
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.load(response)
    elapsed = time.perf_counter() - start

    return payload.get("results", []), payload.get("meta", {}), elapsed


def abstract_from_inverted_index(index: dict[str, list[int]] | None) -> str | None:
    if not index:
        return None

    positions: list[tuple[int, str]] = []
    for word, word_positions in index.items():
        positions.extend((position, word) for position in word_positions)

    return " ".join(word for _, word in sorted(positions)) or None


def author_names(work: dict[str, Any]) -> list[str]:
    authors = []
    for authorship in work.get("authorships", []):
        author = authorship.get("author") or {}
        name = author.get("display_name")
        if name:
            authors.append(name)
    return authors


def host_venue(work: dict[str, Any]) -> str | None:
    primary_location = work.get("primary_location") or {}
    source = primary_location.get("source") or {}
    return source.get("display_name")


def best_pdf_url(work: dict[str, Any]) -> str | None:
    best = work.get("best_oa_location") or {}
    if best.get("pdf_url"):
        return best.get("pdf_url")

    primary = work.get("primary_location") or {}
    if primary.get("pdf_url"):
        return primary.get("pdf_url")

    for location in work.get("locations", []) or []:
        if location.get("pdf_url"):
            return location.get("pdf_url")

    return None


def normalize_work(work: dict[str, Any], query: str) -> dict[str, Any]:
    open_access = work.get("open_access") or {}
    pdf_url = best_pdf_url(work)
    is_oa = open_access.get("is_oa")

    if pdf_url:
        fulltext_status = "open_pdf_found"
    elif is_oa:
        fulltext_status = "open_landing_page_or_oa_no_pdf"
    elif is_oa is False:
        fulltext_status = "closed_or_manual_required"
    else:
        fulltext_status = "unknown"

    doi = work.get("doi")
    if doi and doi.startswith("https://doi.org/"):
        doi_value = doi.removeprefix("https://doi.org/")
    else:
        doi_value = doi

    return {
        "paper_id": work.get("id"),
        "openalex_id": work.get("id"),
        "title": work.get("title"),
        "authors": author_names(work),
        "year": work.get("publication_year"),
        "venue": host_venue(work),
        "doi": doi_value,
        "doi_url": work.get("doi"),
        "url": work.get("id"),
        "abstract": abstract_from_inverted_index(work.get("abstract_inverted_index")),
        "cited_by_count": work.get("cited_by_count"),
        "type": work.get("type"),
        "search_query": query,
        "source": "openalex",
        "open_access": {
            "is_oa": is_oa,
            "oa_status": open_access.get("oa_status"),
            "oa_url": open_access.get("oa_url"),
        },
        "best_oa_location": work.get("best_oa_location"),
        "pdf_url": pdf_url,
        "fulltext_status": fulltext_status,
    }


def dedupe(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []

    for record in sorted(records, key=lambda item: item.get("cited_by_count") or 0, reverse=True):
        key = record.get("doi") or record.get("openalex_id") or record.get("title")
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(record)

    return unique


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_summary(path: Path, records: list[dict[str, Any]], query_stats: list[dict[str, Any]], elapsed_total: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    open_pdf = sum(1 for record in records if record["fulltext_status"] == "open_pdf_found")
    oa_no_pdf = sum(1 for record in records if record["fulltext_status"] == "open_landing_page_or_oa_no_pdf")
    closed = sum(1 for record in records if record["fulltext_status"] == "closed_or_manual_required")
    unknown = sum(1 for record in records if record["fulltext_status"] == "unknown")

    lines = [
        "# OpenAlex 候选论文搜索摘要",
        "",
        "> 该文件由 `scripts/search_openalex.py` 生成。当前脚本只搜索 OpenAlex，不下载 PDF。",
        "",
        "## 总览",
        "",
        f"- 总耗时：{elapsed_total:.2f} 秒",
        f"- 去重后候选论文数量：{len(records)}",
        f"- 找到开放 PDF：{open_pdf}",
        f"- OA 但暂无 PDF URL：{oa_no_pdf}",
        f"- 闭源或需人工下载：{closed}",
        f"- 状态未知：{unknown}",
        "",
        "## Query 统计",
        "",
        "| Query | OpenAlex 命中数 | 本次返回数 | 耗时 |",
        "|---|---:|---:|---:|",
    ]

    for stat in query_stats:
        lines.append(
            f"| `{stat['query']}` | {stat['count']} | {stat['returned']} | {stat['elapsed']:.2f}s |"
        )

    lines.extend([
        "",
        "## 候选论文 Top 列表",
        "",
        "| # | Year | Cited | OA | Fulltext | Title | DOI | PDF URL |",
        "|---:|---:|---:|---|---|---|---|---|",
    ])

    for index, record in enumerate(records, 1):
        title = (record.get("title") or "").replace("|", "\\|")
        doi = record.get("doi") or ""
        pdf = record.get("pdf_url") or ""
        oa = record.get("open_access", {}).get("oa_status") or "unknown"
        lines.append(
            f"| {index} | {record.get('year') or ''} | {record.get('cited_by_count') or 0} | "
            f"{oa} | {record.get('fulltext_status')} | {title} | {doi} | {pdf} |"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search OpenAlex for candidate literature metadata.")
    parser.add_argument("--query", action="append", help="Search query. Can be repeated. Defaults to GNSS test queries.")
    parser.add_argument("--per-page", type=int, default=20, help="Number of results per query.")
    parser.add_argument("--mailto", default=None, help="Email for OpenAlex polite pool/User-Agent.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="JSONL output path.")
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY, help="Markdown summary output path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    queries = args.query or DEFAULT_QUERIES

    start_total = time.perf_counter()
    records: list[dict[str, Any]] = []
    query_stats: list[dict[str, Any]] = []

    for query in queries:
        works, meta, elapsed = fetch_openalex(query, args.per_page, args.mailto)
        query_stats.append({
            "query": query,
            "count": meta.get("count"),
            "returned": len(works),
            "elapsed": elapsed,
        })
        records.extend(normalize_work(work, query) for work in works)

    unique_records = dedupe(records)
    elapsed_total = time.perf_counter() - start_total

    write_jsonl(args.output, unique_records)
    write_summary(args.summary, unique_records, query_stats, elapsed_total)

    print(f"Saved {len(unique_records)} records to {args.output}")
    print(f"Saved summary to {args.summary}")
    print(f"Elapsed: {elapsed_total:.2f}s")


if __name__ == "__main__":
    main()
