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


def top_retrieved_detail(item: dict[str, Any]) -> dict[str, Any]:
    if not item.get("retrieved"):
        return {"chunk_id": "", "tags": [], "section": "", "score": ""}
    top = item["retrieved"][0]
    return {
        "chunk_id": top.get("chunk_id", ""),
        "tags": top.get("tags", []),
        "section": top.get("section", ""),
        "score": top.get("score", ""),
    }


def compare_per_query(runs: dict[str, dict[str, Any]], retrievers: list[str]) -> list[dict[str, Any]]:
    query_ids = [item["query_id"] for item in runs[retrievers[0]]["per_query"]]
    indexed = {retriever: {item["query_id"]: item for item in runs[retriever]["per_query"]} for retriever in retrievers}
    comparisons = []
    for query_id in query_ids:
        row: dict[str, Any] = {"query_id": query_id, "retrievers": {}}
        best_mrr = max(float(indexed[retriever][query_id].get("mrr", 0.0)) for retriever in retrievers)
        winners = []
        for retriever in retrievers:
            item = indexed[retriever][query_id]
            detail = top_retrieved_detail(item)
            mrr = float(item.get("mrr", 0.0))
            if mrr == best_mrr:
                winners.append(retriever)
            row["retrievers"][retriever] = {
                "hit@5": item.get("hit@5", 0),
                "must_hit@5": item.get("must_hit@5", 0),
                "mrr": item.get("mrr", 0.0),
                "top_rank": item.get("top_rank"),
                "top_retrieved": detail["chunk_id"],
                "top_retrieved_tags": detail["tags"],
                "top_retrieved_section": detail["section"],
                "top_retrieved_score": detail["score"],
            }
        row["best_by_mrr"] = winners
        comparisons.append(row)
    return comparisons


def regression_entry(query_id: str, baseline_name: str, baseline: dict[str, Any], hybrid: dict[str, Any]) -> dict[str, Any]:
    baseline_mrr = float(baseline.get("mrr", 0.0))
    hybrid_mrr = float(hybrid.get("mrr", 0.0))
    return {
        "query_id": query_id,
        "baseline": baseline_name,
        f"{baseline_name}_mrr": baseline_mrr,
        "hybrid_mrr": hybrid_mrr,
        "mrr_delta": round(hybrid_mrr - baseline_mrr, 6),
        f"{baseline_name}_must_hit@5": baseline.get("must_hit@5", 0),
        "hybrid_must_hit@5": hybrid.get("must_hit@5", 0),
        f"{baseline_name}_top_retrieved": baseline.get("top_retrieved", ""),
        "hybrid_top_retrieved": hybrid.get("top_retrieved", ""),
    }


def build_diagnostics(runs: dict[str, dict[str, Any]], retrievers: list[str], per_query: list[dict[str, Any]]) -> dict[str, Any]:
    failed_by_retriever = {retriever: runs[retriever]["summary"].get("failed_queries", []) for retriever in retrievers}
    diagnostics: dict[str, Any] = {
        "failed_by_retriever": failed_by_retriever,
        "hybrid_regressions_vs_keyword": [],
        "hybrid_regressions_vs_vector": [],
        "must_hit_disagreements": [],
    }
    if "hybrid" not in retrievers:
        return diagnostics

    for row in per_query:
        query_id = row["query_id"]
        retriever_rows = row["retrievers"]
        hybrid = retriever_rows["hybrid"]
        for baseline_name in ("keyword", "vector"):
            if baseline_name not in retriever_rows:
                continue
            baseline = retriever_rows[baseline_name]
            mrr_regressed = float(hybrid.get("mrr", 0.0)) < float(baseline.get("mrr", 0.0))
            must_regressed = int(hybrid.get("must_hit@5", 0)) < int(baseline.get("must_hit@5", 0))
            if mrr_regressed or must_regressed:
                diagnostics[f"hybrid_regressions_vs_{baseline_name}"].append(regression_entry(query_id, baseline_name, baseline, hybrid))
        for retriever, item in retriever_rows.items():
            if int(item.get("hit@5", 0)) == 1 and int(item.get("must_hit@5", 0)) == 0:
                diagnostics["must_hit_disagreements"].append(
                    {
                        "query_id": query_id,
                        "retriever": retriever,
                        "hit@5": item.get("hit@5", 0),
                        "must_hit@5": item.get("must_hit@5", 0),
                        "mrr": item.get("mrr", 0.0),
                        "top_retrieved": item.get("top_retrieved", ""),
                        "top_retrieved_tags": item.get("top_retrieved_tags", []),
                        "top_retrieved_section": item.get("top_retrieved_section", ""),
                    }
                )
    return diagnostics


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


def markdown_retriever_cell(item: dict[str, Any]) -> str:
    tags = ",".join(str(tag) for tag in item.get("top_retrieved_tags", []))
    return (
        f"`{escape_table(item.get('top_retrieved', ''))}` / "
        f"rank {item.get('top_rank') or ''} / "
        f"MRR {format_float(item.get('mrr', 0.0))} / "
        f"must@5 {item.get('must_hit@5', 0)} / "
        f"tags `{escape_table(tags)}`"
    )


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

    lines.extend(
        [
            "",
            "## Per-query comparison",
            "",
            "| Query ID | Best by MRR | Keyword top/rank/MRR/must/tags | Vector top/rank/MRR/must/tags | Hybrid top/rank/MRR/must/tags |",
            "|---|---|---|---|---|",
        ]
    )
    for row in results["per_query_comparison"]:
        cells = []
        for retriever in ["keyword", "vector", "hybrid"]:
            cells.append(markdown_retriever_cell(row["retrievers"].get(retriever, {})))
        lines.append(
            "| "
            + " | ".join([f"`{escape_table(row['query_id'])}`", ", ".join(row["best_by_mrr"]), *cells])
            + " |"
        )

    diagnostics = results.get("diagnostics", {})
    lines.extend(["", "## Hybrid regressions", ""])
    regressions = diagnostics.get("hybrid_regressions_vs_keyword", []) + diagnostics.get("hybrid_regressions_vs_vector", [])
    if not regressions:
        lines.append("No hybrid regressions detected.")
    else:
        lines.extend(["| Query ID | Baseline | Baseline MRR | Hybrid MRR | MRR delta | Baseline must@5 | Hybrid must@5 |", "|---|---|---:|---:|---:|---:|---:|"])
        for item in regressions:
            baseline = item["baseline"]
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{escape_table(item['query_id'])}`",
                        baseline,
                        format_float(item.get(f"{baseline}_mrr", 0.0)),
                        format_float(item.get("hybrid_mrr", 0.0)),
                        format_float(item.get("mrr_delta", 0.0)),
                        str(item.get(f"{baseline}_must_hit@5", 0)),
                        str(item.get("hybrid_must_hit@5", 0)),
                    ]
                )
                + " |"
            )

    lines.extend(["", "## Must-hit disagreements", ""])
    disagreements = diagnostics.get("must_hit_disagreements", [])
    if not disagreements:
        lines.append("No must-hit disagreements detected.")
    else:
        lines.extend(["| Query ID | Retriever | MRR | Top retrieved | Tags | Section |", "|---|---|---:|---|---|---|"])
        for item in disagreements:
            tags = ",".join(str(tag) for tag in item.get("top_retrieved_tags", []))
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{escape_table(item['query_id'])}`",
                        item["retriever"],
                        format_float(item.get("mrr", 0.0)),
                        f"`{escape_table(item.get('top_retrieved', ''))}`",
                        f"`{escape_table(tags)}`",
                        escape_table(item.get("top_retrieved_section", "")),
                    ]
                )
                + " |"
            )

    lines.extend(["", "## Hybrid failed queries", ""])
    hybrid_failed = diagnostics.get("failed_by_retriever", {}).get("hybrid", [])
    if not hybrid_failed:
        lines.append("No hybrid failed queries.")
    else:
        hybrid_rows = {row["query_id"]: row["retrievers"].get("hybrid", {}) for row in results["per_query_comparison"]}
        lines.extend(["| Query ID | Hybrid top retrieved | Tags | Section | MRR | must@5 |", "|---|---|---|---|---:|---:|"])
        for query_id in hybrid_failed:
            item = hybrid_rows.get(query_id, {})
            tags = ",".join(str(tag) for tag in item.get("top_retrieved_tags", []))
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{escape_table(query_id)}`",
                        f"`{escape_table(item.get('top_retrieved', ''))}`",
                        f"`{escape_table(tags)}`",
                        escape_table(item.get("top_retrieved_section", "")),
                        format_float(item.get("mrr", 0.0)),
                        str(item.get("must_hit@5", 0)),
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
    runs = {retriever: evaluator.evaluate_cases(cases, chunks, retriever_name=retriever) for retriever in selected_retrievers}
    comparison_summary = {retriever: summarize_run(runs[retriever]) for retriever in selected_retrievers}
    per_query_comparison = compare_per_query(runs, selected_retrievers)
    diagnostics = build_diagnostics(runs, selected_retrievers, per_query_comparison)
    warnings = threshold_warnings(comparison_summary, min_hit_at_5, min_mrr)
    results = {
        "chunks_path": display_path(resolved_chunks),
        "eval_set_path": display_path(resolved_eval_set),
        "report_path": display_path(resolved_report),
        "retrievers": selected_retrievers,
        "runs": runs,
        "comparison_summary": comparison_summary,
        "per_query_comparison": per_query_comparison,
        "diagnostics": diagnostics,
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
