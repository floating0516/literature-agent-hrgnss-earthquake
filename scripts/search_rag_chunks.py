#!/usr/bin/env python3
"""Search minimal RAG chunks with lightweight keyword scoring.

This is intentionally a simple JSONL-first search helper. It does not require
embeddings or a vector database; it helps inspect whether curated chunks are
usable before adding heavier retrieval infrastructure.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CHUNKS = BASE_DIR / "rag" / "chunks.jsonl"
DEFAULT_LIMIT = 5
EXCERPT_CHARS = 320


@dataclass(frozen=True)
class SearchFilters:
    source_type: str | None = None
    tag: str | None = None
    paper_id: str | None = None


def tokenize(text: str) -> list[str]:
    return re.findall(r"[\w一-鿿-]+", text.lower())


def load_chunks(path: Path) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                chunks.append(json.loads(line))
    return chunks


def score_chunk(chunk: dict[str, Any], query_terms: list[str]) -> int:
    searchable_fields = [
        str(chunk.get("title", "")),
        str(chunk.get("section", "")),
        str(chunk.get("source_file", "")),
        " ".join(str(tag) for tag in chunk.get("tags", [])),
        str(chunk.get("text", "")),
    ]
    searchable_text = "\n".join(searchable_fields).lower()

    score = 0
    for term in query_terms:
        if not term:
            continue
        score += searchable_text.count(term)
        if term in str(chunk.get("section", "")).lower():
            score += 2
        if term in str(chunk.get("title", "")).lower():
            score += 2
        if term in [str(tag).lower() for tag in chunk.get("tags", [])]:
            score += 3
    return score


def matches_filters(chunk: dict[str, Any], filters: SearchFilters | None) -> bool:
    if filters is None:
        return True
    if filters.source_type and chunk.get("source_type") != filters.source_type:
        return False
    if filters.paper_id and chunk.get("paper_id") != filters.paper_id:
        return False
    if filters.tag and filters.tag not in chunk.get("tags", []):
        return False
    return True


def search_chunks(
    chunks: list[dict[str, Any]],
    query: str,
    limit: int = DEFAULT_LIMIT,
    filters: SearchFilters | None = None,
) -> list[dict[str, Any]]:
    query_terms = tokenize(query)
    results = []
    for chunk in chunks:
        if not matches_filters(chunk, filters):
            continue
        score = score_chunk(chunk, query_terms)
        if score > 0:
            results.append({"score": score, "chunk": chunk})

    return sorted(
        results,
        key=lambda result: (
            -int(result["score"]),
            int(result["chunk"].get("chunk_index", 0) or 0),
            str(result["chunk"].get("chunk_id", "")),
        ),
    )[:limit]


def excerpt(text: str, query: str, max_chars: int = EXCERPT_CHARS) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    if len(normalized) <= max_chars:
        return normalized

    terms = tokenize(query)
    lower_text = normalized.lower()
    match_positions = [lower_text.find(term) for term in terms if lower_text.find(term) >= 0]
    center = min(match_positions) if match_positions else 0
    start = max(center - max_chars // 3, 0)
    end = min(start + max_chars, len(normalized))
    snippet = normalized[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(normalized):
        snippet += "..."
    return snippet


def format_result(result: dict[str, Any], query: str, rank: int) -> str:
    chunk = result["chunk"]
    tags = ", ".join(str(tag) for tag in chunk.get("tags", []))
    lines = [
        f"## {rank}. {chunk.get('chunk_id', '')}",
        f"- score: {result['score']}",
        f"- source_file: {chunk.get('source_file', '')}",
        f"- source_type: {chunk.get('source_type', '')}",
        f"- paper_id: {chunk.get('paper_id', '')}",
        f"- section: {chunk.get('section', '')}",
        f"- tags: {tags}",
        "",
        excerpt(str(chunk.get("text", "")), query),
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search rag/chunks.jsonl with keyword scoring.")
    parser.add_argument("query", help="Keyword query to search for.")
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS, help=f"Chunk JSONL path. Default: {DEFAULT_CHUNKS}")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"Maximum results. Default: {DEFAULT_LIMIT}")
    parser.add_argument("--source-type", choices=["reading_note", "synthesis", "markdown"], help="Only search chunks with this source_type.")
    parser.add_argument("--tag", help="Only search chunks containing this tag.")
    parser.add_argument("--paper-id", help="Only search chunks from this paper_id.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON results instead of Markdown.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    chunks_path = args.chunks if args.chunks.is_absolute() else BASE_DIR / args.chunks
    chunks = load_chunks(chunks_path)
    filters = SearchFilters(source_type=args.source_type, tag=args.tag, paper_id=args.paper_id)
    results = search_chunks(chunks, args.query, args.limit, filters=filters)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    if not results:
        print(f"No matching chunks for: {args.query}")
        return

    for rank, result in enumerate(results, start=1):
        if rank > 1:
            print()
        print(format_result(result, args.query, rank))


if __name__ == "__main__":
    main()
