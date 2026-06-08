#!/usr/bin/env python3
"""Search RAG chunks with deterministic lexical vector scoring.

This module provides an offline sparse-vector baseline. It does not use a
remote embedding API, model download, or vector database; it exists so retrieval
evaluation can compare keyword scoring with a cosine-similarity baseline.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Any

from scripts.search_rag_chunks import DEFAULT_LIMIT, SearchFilters, matches_filters, tokenize


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
