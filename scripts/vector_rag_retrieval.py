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

from scripts.search_rag_chunks import DEFAULT_LIMIT, SearchFilters, matches_filters, search_chunks, tokenize


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
