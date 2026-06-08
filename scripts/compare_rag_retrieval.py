#!/usr/bin/env python3
"""Compare RAG retrieval baselines on one curated eval set."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import evaluate_rag_retrieval as evaluator
from scripts.search_rag_chunks import load_chunks

BASE_DIR = PROJECT_ROOT
DEFAULT_CHUNKS = BASE_DIR / "rag" / "chunks.jsonl"
DEFAULT_EVAL_SET = BASE_DIR / "rag" / "retrieval_eval_set.jsonl"
DEFAULT_REPORT = BASE_DIR / "rag" / "retrieval_compare_report.md"
DEFAULT_RETRIEVERS = ["keyword", "vector", "hybrid"]
DEFAULT_MIN_HIT_AT_5 = 0.8
DEFAULT_MIN_MRR = 0.5


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else BASE_DIR / path


def display_path(path: Path) -> str:
    try:
        return path.relative_to(BASE_DIR).as_posix()
    except ValueError:
        return str(path)


def summarize_run(run: dict[str, Any]) -> dict[str, Any]:
    summary = run["summary"]
    return {
        "num_queries": summary.get("num_queries", 0),
        "mean_hit@1": summary.get("mean_hit@1", 0.0),
        "mean_hit@3": summary.get("mean_hit@3", 0.0),
        "mean_hit@5": summary.get("mean_hit@5", 0.0),
        "mean_must_hit@5": summary.get("mean_must_hit@5", 0.0),
        "mean_recall@5": summary.get("mean_recall@5", 0.0),
        "mrr": summary.get("mrr", 0.0),
        "failed_queries_count": len(summary.get("failed_queries", [])),
        "failed_queries": summary.get("failed_queries", []),
    }


def compare_per_query(runs: dict[str, dict[str, Any]], retrievers: list[str]) -> list[dict[str, Any]]:
    query_ids = [item["query_id"] for item in runs[retrievers[0]]["per_query"]]
    indexed = {
        retriever: {item["query_id"]: item for item in runs[retriever]["per_query"]}
        for retriever in retrievers
    }
    comparisons = []
    for query_id in query_ids:
        row: dict[str, Any] = {"query_id": query_id, "retrievers": {}}
        best_mrr = max(float(indexed[retriever][query_id].get("mrr", 0.0)) for retriever in retrievers)
        winners = []
        for retriever in retrievers:
            item = indexed[retriever][query_id]
            mrr = float(item.get("mrr", 0.0))
            if mrr == best_mrr:
                winners.append(retriever)
            row["retrievers"][retriever] = {
                "hit@5": item.get("hit@5", 0),
                "must_hit@5": item.get("must_hit@5", 0),
                "mrr": item.get("mrr", 0.0),
                "top_rank": item.get("top_rank"),
                "top_retrieved": item["retrieved_chunk_ids"][0] if item.get("retrieved_chunk_ids") else "",
            }
        row["best_by_mrr"] = winners
        comparisons.append(row)
    return comparisons


def threshold_warnings(summary: dict[str, dict[str, Any]], min_hit_at_5: float | None, min_mrr: float | None) -> list[str]:
    warnings = []
    for retriever, item in summary.items():
        if min_hit_at_5 is not None and float(item.get("mean_hit@5", 0.0)) < min_hit_at_5:
            warnings.append(f"{retriever} mean_hit@5={item.get('mean_hit@5', 0.0)} below threshold {min_hit_at_5}")
        if min_mrr is not None and float(item.get("mrr", 0.0)) < min_mrr:
            warnings.append(f"{retriever} mrr={item.get('mrr', 0.0)} below threshold {min_mrr}")
    return warnings


def format_float(value: object) -> str:
    if isinstance(value, (int, float)):
        return f"{float(value):.3f}"
    return str(value)


def escape_table(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_markdown_report(path: Path, results: dict[str, Any]) -> None:
    lines = [
        "# RAG 检索对比报告",
        "",
        "> 该文件由 `scripts/compare_rag_retrieval.py` 生成，用于比较 keyword / vector / hybrid retriever 在同一评测集上的表现。",
        "",
        "## Summary",
        "",
        f"- Chunks: `{results['chunks_path']}`",
        f"- Eval set: `{results['eval_set_path']}`",
        f"- Retrievers: {', '.join(results['retrievers'])}",
        "",
        "| Retriever | Queries | mean_hit@1 | mean_hit@3 | mean_hit@5 | mean_must_hit@5 | mean_recall@5 | MRR | Failed queries |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for retriever in results["retrievers"]:
        item = results["comparison_summary"][retriever]
        lines.append(
            "| "
            + " | ".join(
                [
                    retriever,
                    str(item["num_queries"]),
                    format_float(item["mean_hit@1"]),
                    format_float(item["mean_hit@3"]),
                    format_float(item["mean_hit@5"]),
                    format_float(item["mean_must_hit@5"]),
                    format_float(item["mean_recall@5"]),
                    format_float(item["mrr"]),
                    str(item["failed_queries_count"]),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Per-query comparison", "", "| Query ID | Best by MRR | Keyword top/rank/MRR | Vector top/rank/MRR | Hybrid top/rank/MRR |", "|---|---|---|---|---|"])
    for row in results["per_query_comparison"]:
        cells = []
        for retriever in ["keyword", "vector", "hybrid"]:
            item = row["retrievers"].get(retriever, {})
            cells.append(f"`{escape_table(item.get('top_retrieved', ''))}` / {item.get('top_rank') or ''} / {format_float(item.get('mrr', 0.0))}")
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_table(row['query_id'])}`",
                    ", ".join(row["best_by_mrr"]),
                    *cells,
                ]
            )
            + " |"
        )

    lines.extend(["", "## Warnings", ""])
    if results["warnings"]:
        for warning in results["warnings"]:
            lines.append(f"- {warning}")
    else:
        lines.append("No warnings.")

    lines.extend(["", "## Failed queries by retriever", ""])
    for retriever in results["retrievers"]:
        failed = results["comparison_summary"][retriever]["failed_queries"]
        lines.append(f"- **{retriever}**: {', '.join(failed) if failed else 'None'}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    chunks_path: Path = DEFAULT_CHUNKS,
    eval_set_path: Path = DEFAULT_EVAL_SET,
    report_path: Path = DEFAULT_REPORT,
    json_output_path: Path | None = None,
    retrievers: list[str] | None = None,
    strict: bool = False,
    min_hit_at_5: float | None = None,
    min_mrr: float | None = None,
) -> dict[str, Any]:
    selected_retrievers = retrievers or DEFAULT_RETRIEVERS
    unknown = [name for name in selected_retrievers if name not in evaluator.RETRIEVERS]
    if unknown:
        raise ValueError(f"Unknown retriever(s): {', '.join(unknown)}")

    resolved_chunks = resolve_path(chunks_path)
    resolved_eval_set = resolve_path(eval_set_path)
    resolved_report = resolve_path(report_path)
    resolved_json = resolve_path(json_output_path) if json_output_path else None

    chunks = load_chunks(resolved_chunks)
    cases = evaluator.load_eval_cases(resolved_eval_set)
    runs = {
        retriever: evaluator.evaluate_cases(cases, chunks, retriever_name=retriever)
        for retriever in selected_retrievers
    }
    comparison_summary = {retriever: summarize_run(runs[retriever]) for retriever in selected_retrievers}
    warnings = threshold_warnings(comparison_summary, min_hit_at_5, min_mrr)
    results = {
        "chunks_path": display_path(resolved_chunks),
        "eval_set_path": display_path(resolved_eval_set),
        "report_path": display_path(resolved_report),
        "retrievers": selected_retrievers,
        "runs": runs,
        "comparison_summary": comparison_summary,
        "per_query_comparison": compare_per_query(runs, selected_retrievers),
        "warnings": warnings,
    }
    if resolved_json:
        results["json_output_path"] = display_path(resolved_json)

    write_markdown_report(resolved_report, results)
    if resolved_json:
        write_json(resolved_json, results)

    print(f"Compared {len(selected_retrievers)} retrievers on {len(cases)} queries: {', '.join(selected_retrievers)}")
    print(f"Wrote report to {resolved_report}")
    if resolved_json:
        print(f"Wrote JSON results to {resolved_json}")
    for warning in warnings:
        print(f"Strict check failed: {warning}", file=sys.stderr)
    if strict and warnings:
        raise SystemExit(1)
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare RAG retrievers against one curated JSONL eval set.")
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS)
    parser.add_argument("--eval-set", type=Path, default=DEFAULT_EVAL_SET)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--retrievers", nargs="+", choices=sorted(evaluator.RETRIEVERS), default=DEFAULT_RETRIEVERS)
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
            retrievers=args.retrievers,
            strict=args.strict,
            min_hit_at_5=args.min_hit_at_5 if args.strict else None,
            min_mrr=args.min_mrr if args.strict else None,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
