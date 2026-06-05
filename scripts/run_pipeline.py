#!/usr/bin/env python3
"""Run the literature-reading pipeline from a single entry point.

The pipeline composes the existing scripts without changing their compliance
boundary: PDF downloading only uses open PDF URLs already present in metadata,
and manual PDF matching is opt-in for local files the user already has.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import build_minimal_rag_chunks, download_pdfs, match_manual_pdfs, parse_pdfs, screen_candidates, search_openalex

BASE_DIR = PROJECT_ROOT
STAGES = ["search", "screen", "download", "match_manual", "parse", "rag"]
SKIP_FLAGS = {
    "search": "skip_search",
    "screen": "skip_screen",
    "download": "skip_download",
    "match_manual": "skip_match_manual",
    "parse": "skip_parse",
    "rag": "skip_rag",
}


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else BASE_DIR / path


def selected_stages(args: argparse.Namespace) -> list[str]:
    start = STAGES.index(args.from_stage)
    end = STAGES.index(args.to_stage)
    if start > end:
        raise SystemExit("--from-stage must not come after --to-stage")

    stages = STAGES[start : end + 1]
    if not args.match_manual:
        stages = [stage for stage in stages if stage != "match_manual"]
    return [stage for stage in stages if not getattr(args, SKIP_FLAGS[stage])]


def run_search(args: argparse.Namespace) -> None:
    print("==> search")
    search_openalex.run(
        queries=args.query or search_openalex.DEFAULT_QUERIES,
        per_page=args.per_page,
        mailto=args.mailto,
        output_path=resolve_path(args.candidates),
        summary_path=resolve_path(args.search_summary),
    )


def run_screen(args: argparse.Namespace) -> None:
    print("==> screen")
    screen_candidates.run(
        input_path=resolve_path(args.candidates),
        output_path=resolve_path(args.screened),
        selected_path=resolve_path(args.selected),
        report_path=resolve_path(args.screening_report),
        comparison_path=resolve_path(args.screening_comparison),
    )


def run_download(args: argparse.Namespace) -> None:
    print("==> download")
    policy = download_pdfs.load_download_policy(resolve_path(args.download_config))
    config = download_pdfs.DownloadConfig(
        input_path=resolve_path(args.selected),
        output_path=resolve_path(args.download_results),
        log_path=resolve_path(args.download_log),
        pdf_dir=resolve_path(args.pdf_dir),
        timeout=args.download_timeout if args.download_timeout is not None else float(policy["timeout_seconds"]),
        sleep_seconds=args.download_sleep if args.download_sleep is not None else float(policy["sleep_seconds"]),
        user_agent=args.download_user_agent if args.download_user_agent is not None else str(policy["user_agent"]),
        overwrite=args.overwrite_downloads,
        enabled=bool(policy["enabled"]),
        dry_run=args.dry_run,
    )
    results = download_pdfs.run(config)
    print(f"Processed {len(results)} download records")


def run_manual_match(args: argparse.Namespace) -> None:
    print("==> match_manual")
    config = match_manual_pdfs.ManualMatchConfig(
        input_path=resolve_path(args.selected),
        results_path=resolve_path(args.download_results),
        manual_dir=resolve_path(args.manual_dir),
        pdf_dir=resolve_path(args.pdf_dir),
        log_path=resolve_path(args.manual_match_log),
        apply=not args.dry_run,
        overwrite=args.overwrite_manual_matches,
        recursive=args.recursive_manual_dir,
        only_status=match_manual_pdfs.parse_statuses(args.manual_only_status),
        require_doi=args.manual_require_doi,
    )
    summary = match_manual_pdfs.match_manual_pdfs(config)
    print(f"Scanned manual PDFs: {sum(summary.values())}")


def run_parse(args: argparse.Namespace) -> None:
    print("==> parse")
    results = parse_pdfs.run(
        input_dir=resolve_path(args.pdf_dir),
        pdf_path=resolve_path(args.pdf) if args.pdf else None,
        output_dir=resolve_path(args.parsed_dir),
        log_path=resolve_path(args.parse_log),
        backend=args.parse_backend,
    )
    print(f"Parsed {len(results)} PDFs")


def run_rag(args: argparse.Namespace) -> None:
    print("==> rag")
    input_paths = [resolve_path(path) for path in args.rag_inputs]
    chunks = build_minimal_rag_chunks.run(
        input_paths=input_paths,
        output_path=resolve_path(args.rag_output),
        report_path=resolve_path(args.rag_report),
    )
    print(f"Built {len(chunks)} RAG chunks")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the literature-reading pipeline from search through RAG chunks.")
    parser.add_argument("--from-stage", choices=STAGES, default="search")
    parser.add_argument("--to-stage", choices=STAGES, default="rag")
    parser.add_argument("--skip-search", action="store_true")
    parser.add_argument("--skip-screen", action="store_true")
    parser.add_argument("--skip-download", action="store_true")
    parser.add_argument("--skip-match-manual", action="store_true")
    parser.add_argument("--skip-parse", action="store_true")
    parser.add_argument("--skip-rag", action="store_true")

    parser.add_argument("--dry-run", action="store_true", help="Dry run stages that support it, such as download and manual matching.")
    parser.add_argument("--match-manual", action="store_true", help="Opt in to matching user-local manual PDFs.")

    parser.add_argument("--query", action="append", help="OpenAlex query. Can be repeated.")
    parser.add_argument("--per-page", type=int, default=20)
    parser.add_argument("--mailto", default=None)

    parser.add_argument("--candidates", type=Path, default=search_openalex.DEFAULT_OUTPUT)
    parser.add_argument("--search-summary", type=Path, default=search_openalex.DEFAULT_SUMMARY)
    parser.add_argument("--screened", type=Path, default=screen_candidates.DEFAULT_OUTPUT)
    parser.add_argument("--selected", type=Path, default=screen_candidates.DEFAULT_SELECTED)
    parser.add_argument("--screening-report", type=Path, default=screen_candidates.DEFAULT_REPORT)
    parser.add_argument("--screening-comparison", type=Path, default=screen_candidates.DEFAULT_COMPARISON)

    parser.add_argument("--download-config", type=Path, default=download_pdfs.DEFAULT_CONFIG)
    parser.add_argument("--download-results", type=Path, default=download_pdfs.DEFAULT_OUTPUT)
    parser.add_argument("--download-log", type=Path, default=download_pdfs.DEFAULT_LOG)
    parser.add_argument("--pdf-dir", type=Path, default=download_pdfs.DEFAULT_PDF_DIR)
    parser.add_argument("--download-sleep", type=float, default=None)
    parser.add_argument("--download-timeout", type=float, default=None)
    parser.add_argument("--download-user-agent", default=None)
    parser.add_argument("--overwrite-downloads", action="store_true")

    parser.add_argument("--manual-dir", type=Path, default=match_manual_pdfs.DEFAULT_MANUAL_DIR)
    parser.add_argument("--manual-match-log", type=Path, default=match_manual_pdfs.DEFAULT_LOG)
    parser.add_argument("--overwrite-manual-matches", action="store_true")
    parser.add_argument("--recursive-manual-dir", action="store_true")
    parser.add_argument("--manual-only-status", default="failed,manual_required")
    parser.add_argument("--manual-require-doi", action="store_true")

    parser.add_argument("--pdf", type=Path, help="Parse one PDF instead of the full PDF directory.")
    parser.add_argument("--parsed-dir", type=Path, default=parse_pdfs.DEFAULT_OUTPUT_DIR)
    parser.add_argument("--parse-log", type=Path, default=parse_pdfs.DEFAULT_LOG)
    parser.add_argument("--parse-backend", choices=["pymupdf4llm", "pdftotext"], default="pymupdf4llm")

    parser.add_argument("--rag-output", type=Path, default=build_minimal_rag_chunks.DEFAULT_OUTPUT)
    parser.add_argument("--rag-report", type=Path, default=build_minimal_rag_chunks.DEFAULT_REPORT)
    parser.add_argument("rag_inputs", nargs="*", type=Path, default=build_minimal_rag_chunks.DEFAULT_INPUTS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    runners = {
        "search": run_search,
        "screen": run_screen,
        "download": run_download,
        "match_manual": run_manual_match,
        "parse": run_parse,
        "rag": run_rag,
    }
    stages = selected_stages(args)
    print(f"Pipeline stages: {', '.join(stages) if stages else '(none)'}")
    for stage in stages:
        runners[stage](args)
    print("Pipeline finished")


if __name__ == "__main__":
    main()
