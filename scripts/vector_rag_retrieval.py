#!/usr/bin/env python3
"""Search RAG chunks with deterministic lexical vector scoring.

This module provides an offline sparse-vector baseline. It does not use a
remote embedding API, model download, or vector database; it exists so retrieval
evaluation can compare keyword scoring with a cosine-similarity baseline.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from scripts.search_rag_chunks import (
        BASE_DIR,
        DEFAULT_CHUNKS,
        DEFAULT_LIMIT,
        SearchFilters,
        format_result,
        load_chunks,
        matches_filters,
        search_chunks,
        tokenize,
    )
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.search_rag_chunks import (
        BASE_DIR,
        DEFAULT_CHUNKS,
        DEFAULT_LIMIT,
        SearchFilters,
        format_result,
        load_chunks,
        matches_filters,
        search_chunks,
        tokenize,
    )


def chunk_to_search_text(chunk: dict[str, Any]) -> str:
    searchable_fields = [
        str(chunk.get("title", "")),
        str(chunk.get("section", "")),
        str(chunk.get("source_file", "")),
        " ".join(str(tag) for tag in chunk.get("tags", [])),
        str(chunk.get("text", "")),
    ]
    return "\n".join(searchable_fields)


def vectorize_text(text: str) -> dict[str, float]:
    counts = Counter(tokenize(text))
    norm = math.sqrt(sum(count * count for count in counts.values()))
    if norm == 0:
        return {}
    return {term: count / norm for term, count in counts.items()}


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    if len(left) > len(right):
        left, right = right, left
    return sum(weight * right.get(term, 0.0) for term, weight in left.items())


def chunk_identity(chunk: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(chunk.get("chunk_id", "")),
        str(chunk.get("source_file", "")),
        str(chunk.get("section", "")),
        str(chunk.get("chunk_index", "")),
    )


def normalized_scores(results: list[dict[str, Any]]) -> dict[tuple[str, str, str, str], float]:
    if not results:
        return {}
    max_score = max(float(result["score"]) for result in results)
    if max_score <= 0:
        return {}
    return {chunk_identity(result["chunk"]): float(result["score"]) / max_score for result in results}


def vector_search_chunks(
    chunks: list[dict[str, Any]],
    query: str,
    limit: int = DEFAULT_LIMIT,
    filters: SearchFilters | None = None,
) -> list[dict[str, Any]]:
    query_vector = vectorize_text(query)
    if not query_vector:
        return []

    results = []
    for chunk in chunks:
        if not matches_filters(chunk, filters):
            continue
        score = cosine_similarity(query_vector, vectorize_text(chunk_to_search_text(chunk)))
        if score > 0:
            results.append({"score": round(score, 6), "chunk": chunk})

    return sorted(
        results,
        key=lambda result: (
            -float(result["score"]),
            int(result["chunk"].get("chunk_index", 0) or 0),
            str(result["chunk"].get("chunk_id", "")),
        ),
    )[:limit]


def hybrid_search_chunks(
    chunks: list[dict[str, Any]],
    query: str,
    limit: int = DEFAULT_LIMIT,
    filters: SearchFilters | None = None,
    keyword_weight: float = 0.6,
    vector_weight: float = 0.4,
) -> list[dict[str, Any]]:
    candidate_limit = max(limit * 3, limit)
    keyword_results = search_chunks(chunks, query, limit=candidate_limit, filters=filters)
    vector_results = vector_search_chunks(chunks, query, limit=candidate_limit, filters=filters)

    keyword_by_id = normalized_scores(keyword_results)
    vector_by_id = normalized_scores(vector_results)

    chunks_by_id: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for result in keyword_results + vector_results:
        chunks_by_id[chunk_identity(result["chunk"])] = result["chunk"]

    fused_results = []
    for identity, chunk in chunks_by_id.items():
        score = (keyword_weight * keyword_by_id.get(identity, 0.0)) + (vector_weight * vector_by_id.get(identity, 0.0))
        if score > 0:
            fused_results.append({"score": round(score, 6), "chunk": chunk})

    return sorted(
        fused_results,
        key=lambda result: (
            -float(result["score"]),
            int(result["chunk"].get("chunk_index", 0) or 0),
            str(result["chunk"].get("chunk_id", "")),
        ),
    )[:limit]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search rag/chunks.jsonl with vector or hybrid scoring.")
    parser.add_argument("query", help="Query to search for.")
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS, help=f"Chunk JSONL path. Default: {DEFAULT_CHUNKS}")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"Maximum results. Default: {DEFAULT_LIMIT}")
    parser.add_argument("--retriever", choices=["vector", "hybrid"], default="vector", help="Retrieval strategy. Default: vector")
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
    search = hybrid_search_chunks if args.retriever == "hybrid" else vector_search_chunks
    results = search(chunks, args.query, args.limit, filters=filters)

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
