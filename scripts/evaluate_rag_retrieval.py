#!/usr/bin/env python3
"""Evaluate RAG retrieval quality with a curated JSONL eval set."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.search_rag_chunks import SearchFilters, load_chunks, search_chunks
from scripts.vector_rag_retrieval import hybrid_search_chunks, vector_search_chunks

BASE_DIR = PROJECT_ROOT
DEFAULT_CHUNKS = BASE_DIR / "rag" / "chunks.jsonl"
DEFAULT_EVAL_SET = BASE_DIR / "rag" / "retrieval_eval_set.jsonl"
DEFAULT_REPORT = BASE_DIR / "rag" / "retrieval_eval_report.md"
DEFAULT_METRICS_AT = [1, 3, 5]
DEFAULT_MIN_HIT_AT_5 = 0.8
DEFAULT_MIN_MRR = 0.5

Target = str | dict[str, str]
Retriever = Callable[[list[dict[str, Any]], "EvalCase", int], list[dict[str, Any]]]
ALLOWED_FILTER_KEYS = {"source_type", "tag", "paper_id"}


@dataclass(frozen=True)
class EvalCase:
    query_id: str
    query: str
    intent: str
    must_retrieve: list[Target]
    relevant: list[Target]
    acceptable: list[Target]
    filters: SearchFilters | None
    metrics_at: list[int]
    notes: str = ""


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else BASE_DIR / path


def display_path(path: Path) -> str:
    try:
        return path.relative_to(BASE_DIR).as_posix()
    except ValueError:
        return str(path)


def parse_filters(payload: object) -> SearchFilters | None:
    if payload in (None, {}):
        return None
    if not isinstance(payload, dict):
        raise ValueError("filters must be an object")
    unknown = set(payload) - ALLOWED_FILTER_KEYS
    if unknown:
        raise ValueError(f"unknown filter keys: {', '.join(sorted(unknown))}")
    return SearchFilters(
        source_type=payload.get("source_type"),
        tag=payload.get("tag"),
        paper_id=payload.get("paper_id"),
    )


def ensure_targets(value: object, field: str) -> list[Target]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")
    targets: list[Target] = []
    for target in value:
        if isinstance(target, str):
            targets.append(target)
        elif isinstance(target, dict):
            targets.append({str(key): str(val) for key, val in target.items() if val is not None})
        else:
            raise ValueError(f"{field} targets must be strings or objects")
    return targets


def eval_case_from_record(record: dict[str, Any]) -> EvalCase:
    return EvalCase(
        query_id=str(record.get("query_id", "")),
        query=str(record.get("query", "")),
        intent=str(record.get("intent", "")),
        must_retrieve=ensure_targets(record.get("must_retrieve", []), "must_retrieve"),
        relevant=ensure_targets(record.get("relevant", []), "relevant"),
        acceptable=ensure_targets(record.get("acceptable", []), "acceptable"),
        filters=parse_filters(record.get("filters")),
        metrics_at=[int(value) for value in record.get("metrics_at", DEFAULT_METRICS_AT)],
        notes=str(record.get("notes", "")),
    )


def validate_eval_cases(cases: list[EvalCase]) -> None:
    seen: set[str] = set()
    for case in cases:
        if not case.query_id:
            raise ValueError("query_id is required")
        if case.query_id in seen:
            raise ValueError(f"duplicate query_id: {case.query_id}")
        seen.add(case.query_id)
        if not case.query:
            raise ValueError(f"query is required for {case.query_id}")
        if not case.must_retrieve and not case.relevant:
            raise ValueError(f"must_retrieve or relevant is required for {case.query_id}")
        if not case.metrics_at:
            raise ValueError(f"metrics_at is required for {case.query_id}")
        if any(k <= 0 for k in case.metrics_at):
            raise ValueError(f"metrics_at values must be positive for {case.query_id}")


def load_eval_cases(path: Path) -> list[EvalCase]:
    cases: list[EvalCase] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON on line {line_number}: {exc}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"eval record on line {line_number} must be an object")
            cases.append(eval_case_from_record(record))
    validate_eval_cases(cases)
    return cases


def target_matches_chunk(target: Target, chunk: dict[str, Any]) -> bool:
    if isinstance(target, str):
        return chunk.get("chunk_id") == target

    for key in ("chunk_id", "paper_id", "source_type", "section", "source_file"):
        expected = target.get(key)
        if expected is not None and chunk.get(key) != expected:
            return False

    expected_tag = target.get("tag")
    if expected_tag is not None and expected_tag not in chunk.get("tags", []):
        return False
    return True


def target_matched_by_chunks(target: Target, chunks: list[dict[str, Any]]) -> bool:
    return any(target_matches_chunk(target, chunk) for chunk in chunks)


def chunk_matches_any(targets: list[Target], chunk: dict[str, Any]) -> bool:
    return any(target_matches_chunk(target, chunk) for target in targets)


def keyword_retriever(chunks: list[dict[str, Any]], case: EvalCase, limit: int) -> list[dict[str, Any]]:
    return search_chunks(chunks, case.query, limit=limit, filters=case.filters)


def vector_retriever(chunks: list[dict[str, Any]], case: EvalCase, limit: int) -> list[dict[str, Any]]:
    return vector_search_chunks(chunks, case.query, limit=limit, filters=case.filters)


def hybrid_retriever(chunks: list[dict[str, Any]], case: EvalCase, limit: int) -> list[dict[str, Any]]:
    return hybrid_search_chunks(chunks, case.query, limit=limit, filters=case.filters)


RETRIEVERS: dict[str, Retriever] = {"keyword": keyword_retriever, "vector": vector_retriever, "hybrid": hybrid_retriever}


def evaluate_case(
    case: EvalCase,
    chunks: list[dict[str, Any]],
    limit: int | None = None,
    retriever: Retriever = keyword_retriever,
) -> dict[str, Any]:
    metrics_at = sorted(set(case.metrics_at))
    max_k = limit or max(metrics_at)
    retrieval_results = retriever(chunks, case, max_k)
    retrieved_chunks = [result["chunk"] for result in retrieval_results]
    relevant_targets = case.must_retrieve + [target for target in case.relevant if target not in case.must_retrieve]

    first_rank = None
    for rank, retrieved in enumerate(retrieved_chunks, start=1):
        if chunk_matches_any(relevant_targets, retrieved):
            first_rank = rank
            break

    result: dict[str, Any] = {
        "query_id": case.query_id,
        "query": case.query,
        "intent": case.intent,
        "filters": filters_to_dict(case.filters),
        "metrics_at": metrics_at,
        "mrr": round(1 / first_rank, 6) if first_rank else 0.0,
        "top_rank": first_rank,
        "retrieved_chunk_ids": [str(chunk.get("chunk_id", "")) for chunk in retrieved_chunks],
        "retrieved": [retrieved_summary(item, rank) for rank, item in enumerate(retrieval_results, start=1)],
        "must_retrieve": case.must_retrieve,
        "relevant": case.relevant,
        "acceptable": case.acceptable,
    }

    for k in metrics_at:
        top_k = retrieved_chunks[:k]
        result[f"hit@{k}"] = int(any(target_matched_by_chunks(target, top_k) for target in relevant_targets))
        result[f"must_hit@{k}"] = int(any(target_matched_by_chunks(target, top_k) for target in case.must_retrieve))
        if case.relevant:
            matched = sum(1 for target in case.relevant if target_matched_by_chunks(target, top_k))
            result[f"recall@{k}"] = round(matched / len(case.relevant), 6)
        else:
            result[f"recall@{k}"] = 0.0
    return result


def retrieved_summary(result: dict[str, Any], rank: int) -> dict[str, Any]:
    chunk = result["chunk"]
    return {
        "rank": rank,
        "score": result["score"],
        "chunk_id": chunk.get("chunk_id", ""),
        "paper_id": chunk.get("paper_id", ""),
        "source_file": chunk.get("source_file", ""),
        "source_type": chunk.get("source_type", ""),
        "section": chunk.get("section", ""),
        "tags": chunk.get("tags", []),
    }


def filters_to_dict(filters: SearchFilters | None) -> dict[str, str | None]:
    if filters is None:
        return {"source_type": None, "tag": None, "paper_id": None}
    return {"source_type": filters.source_type, "tag": filters.tag, "paper_id": filters.paper_id}


def mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 6)


def aggregate_results(per_query: list[dict[str, Any]], metrics_at: list[int]) -> dict[str, Any]:
    summary: dict[str, Any] = {"num_queries": len(per_query)}
    for k in metrics_at:
        summary[f"mean_hit@{k}"] = mean([float(result.get(f"hit@{k}", 0)) for result in per_query])
        summary[f"mean_must_hit@{k}"] = mean([float(result.get(f"must_hit@{k}", 0)) for result in per_query])
        summary[f"mean_recall@{k}"] = mean([float(result.get(f"recall@{k}", 0.0)) for result in per_query])
    summary["mrr"] = mean([float(result["mrr"]) for result in per_query])
    strict_k = max(metrics_at) if metrics_at else 5
    summary["failed_queries"] = [result["query_id"] for result in per_query if not result.get(f"must_hit@{strict_k}")]
    return summary


def evaluate_cases(cases: list[EvalCase], chunks: list[dict[str, Any]], retriever_name: str = "keyword", limit: int | None = None) -> dict[str, Any]:
    if retriever_name not in RETRIEVERS:
        raise ValueError(f"Unknown retriever: {retriever_name}")
    metrics_at = sorted({k for case in cases for k in case.metrics_at}) or DEFAULT_METRICS_AT
    max_k = limit or max(metrics_at)
    per_query = [evaluate_case(case, chunks, limit=max_k, retriever=RETRIEVERS[retriever_name]) for case in cases]
    return {"retriever": retriever_name, "summary": aggregate_results(per_query, metrics_at), "per_query": per_query}


def escape_table(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def format_float(value: object) -> str:
    if isinstance(value, (int, float)):
        return f"{float(value):.3f}"
    return str(value)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_markdown_report(path: Path, results: dict[str, Any]) -> None:
    summary = results["summary"]
    per_query = results["per_query"]
    lines = [
        "# RAG 检索评测报告",
        "",
        "> 该文件由 `scripts/evaluate_rag_retrieval.py` 生成，用于评估当前 RAG 检索是否能找回人工标注的目标 chunks。",
        "",
        "## Summary",
        "",
        f"- Retriever: {results['retriever']}",
        f"- Chunks: `{results.get('chunks_path', '')}`",
        f"- Eval set: `{results.get('eval_set_path', '')}`",
        f"- Queries: {summary['num_queries']}",
        f"- mean_hit@1: {format_float(summary.get('mean_hit@1', 0.0))}",
        f"- mean_hit@3: {format_float(summary.get('mean_hit@3', 0.0))}",
        f"- mean_hit@5: {format_float(summary.get('mean_hit@5', 0.0))}",
        f"- MRR: {format_float(summary.get('mrr', 0.0))}",
        "",
        "## Per-query results",
        "",
        "| Query ID | hit@1 | hit@3 | hit@5 | must_hit@5 | MRR | Top rank | Top retrieved |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for item in per_query:
        top = item["retrieved"][0]["chunk_id"] if item["retrieved"] else ""
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_table(item['query_id'])}`",
                    str(item.get("hit@1", 0)),
                    str(item.get("hit@3", 0)),
                    str(item.get("hit@5", 0)),
                    str(item.get("must_hit@5", 0)),
                    format_float(item.get("mrr", 0.0)),
                    str(item.get("top_rank") or ""),
                    f"`{escape_table(top)}`",
                ]
            )
            + " |"
        )

    failures = [item for item in per_query if item["query_id"] in summary.get("failed_queries", [])]
    lines.extend(["", "## Failures", ""])
    if not failures:
        lines.append("No failed queries.")
    for item in failures:
        lines.extend(
            [
                f"### {item['query_id']}",
                "",
                f"- Query: `{item['query']}`",
                f"- Intent: {item['intent']}",
                f"- Expected must targets: `{json.dumps(item['must_retrieve'], ensure_ascii=False)}`",
                "- Retrieved:",
            ]
        )
        if not item["retrieved"]:
            lines.append("  - No retrieved chunks.")
        for retrieved in item["retrieved"]:
            lines.append(
                f"  {retrieved['rank']}. `{retrieved['chunk_id']}` — score {retrieved['score']} — "
                f"{retrieved['paper_id']} / {retrieved['section']}"
            )
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def enforce_strict(summary: dict[str, Any], min_hit_at_5: float | None, min_mrr: float | None) -> list[str]:
    failures = []
    if min_hit_at_5 is not None and float(summary.get("mean_hit@5", 0.0)) < min_hit_at_5:
        failures.append(f"mean_hit@5={summary.get('mean_hit@5', 0.0)} below threshold {min_hit_at_5}")
    if min_mrr is not None and float(summary.get("mrr", 0.0)) < min_mrr:
        failures.append(f"mrr={summary.get('mrr', 0.0)} below threshold {min_mrr}")
    return failures


def run(
    chunks_path: Path = DEFAULT_CHUNKS,
    eval_set_path: Path = DEFAULT_EVAL_SET,
    report_path: Path = DEFAULT_REPORT,
    json_output_path: Path | None = None,
    retriever_name: str = "keyword",
    limit: int | None = None,
    strict: bool = False,
    min_hit_at_5: float | None = None,
    min_mrr: float | None = None,
) -> dict[str, Any]:
    resolved_chunks = resolve_path(chunks_path)
    resolved_eval_set = resolve_path(eval_set_path)
    resolved_report = resolve_path(report_path)
    resolved_json = resolve_path(json_output_path) if json_output_path else None

    chunks = load_chunks(resolved_chunks)
    cases = load_eval_cases(resolved_eval_set)
    results = evaluate_cases(cases, chunks, retriever_name=retriever_name, limit=limit)
    results["chunks_path"] = display_path(resolved_chunks)
    results["eval_set_path"] = display_path(resolved_eval_set)
    results["report_path"] = display_path(resolved_report)
    if resolved_json:
        results["json_output_path"] = display_path(resolved_json)

    write_markdown_report(resolved_report, results)
    if resolved_json:
        write_json(resolved_json, results)

    summary = results["summary"]
    print(f"Evaluated {summary['num_queries']} queries with {retriever_name} retriever")
    print(f"mean_hit@5={summary.get('mean_hit@5', 0.0):.3f} mrr={summary.get('mrr', 0.0):.3f}")
    print(f"Wrote report to {resolved_report}")
    if resolved_json:
        print(f"Wrote JSON results to {resolved_json}")

    if strict:
        threshold_failures = enforce_strict(summary, min_hit_at_5, min_mrr)
        if threshold_failures:
            for failure in threshold_failures:
                print(f"Strict check failed: {failure}", file=sys.stderr)
            raise SystemExit(1)
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate RAG retrieval against a curated JSONL eval set.")
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS)
    parser.add_argument("--eval-set", type=Path, default=DEFAULT_EVAL_SET)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--retriever", choices=sorted(RETRIEVERS), default="keyword")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--min-hit-at-5", type=float, default=DEFAULT_MIN_HIT_AT_5)
    parser.add_argument("--min-mrr", type=float, default=DEFAULT_MIN_MRR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        run(
            chunks_path=args.chunks,
            eval_set_path=args.eval_set,
            report_path=args.report,
            json_output_path=args.json_output,
            retriever_name=args.retriever,
            limit=args.limit,
            strict=args.strict,
            min_hit_at_5=args.min_hit_at_5 if args.strict else None,
            min_mrr=args.min_mrr if args.strict else None,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
