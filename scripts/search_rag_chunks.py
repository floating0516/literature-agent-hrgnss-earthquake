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
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CHUNKS = BASE_DIR / "rag" / "chunks.jsonl"
DEFAULT_LIMIT = 5
EXCERPT_CHARS = 320


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
    return score


def search_chunks(chunks: list[dict[str, Any]], query: str, limit: int = DEFAULT_LIMIT) -> list[dict[str, Any]]:
    query_terms = tokenize(query)
    results = []
    for chunk in chunks:
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
    lines = [
        f"## {rank}. {chunk.get('chunk_id', '')}",
        f"- score: {result['score']}",
        f"- source_file: {chunk.get('source_file', '')}",
        f"- source_type: {chunk.get('source_type', '')}",
        f"- section: {chunk.get('section', '')}",
        "",
        excerpt(str(chunk.get("text", "")), query),
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search rag/chunks.jsonl with keyword scoring.")
    parser.add_argument("query", help="Keyword query to search for.")
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS, help=f"Chunk JSONL path. Default: {DEFAULT_CHUNKS}")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"Maximum results. Default: {DEFAULT_LIMIT}")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    chunks_path = args.chunks if args.chunks.is_absolute() else BASE_DIR / args.chunks
    chunks = load_chunks(chunks_path)
    results = search_chunks(chunks, args.query, args.limit)

    if not results:
        print(f"No matching chunks for: {args.query}")
        return

    for rank, result in enumerate(results, start=1):
        if rank > 1:
            print()
        print(format_result(result, args.query, rank))


if __name__ == "__main__":
    main()
