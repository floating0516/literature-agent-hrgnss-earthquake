import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import evaluate_rag_retrieval as evaluator
from scripts.search_rag_chunks import SearchFilters


def write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text("\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n", encoding="utf-8")


def chunk(
    chunk_id: str,
    text: str,
    *,
    paper_id: str = "paper-a",
    source_type: str = "reading_note",
    section: str = "6. Method",
    tags: list[str] | None = None,
    chunk_index: int = 1,
) -> dict[str, object]:
    return {
        "chunk_id": chunk_id,
        "paper_id": paper_id,
        "title": paper_id.replace("-", " ").title(),
        "source_file": f"papers/notes/{paper_id}.md",
        "source_type": source_type,
        "section": section,
        "tags": tags or ["method"],
        "chunk_index": chunk_index,
        "text": text,
    }


def eval_record(**overrides: object) -> dict[str, object]:
    record: dict[str, object] = {
        "query_id": "method_bayesian_uncertainty",
        "query": "bayesian uncertainty method",
        "intent": "Find the Bayesian uncertainty method chunk.",
        "must_retrieve": [{"paper_id": "paper-a", "tag": "method"}],
        "relevant": [{"paper_id": "paper-a", "tag": "method"}],
        "acceptable": [{"paper_id": "paper-a"}],
        "filters": {"source_type": "reading_note", "tag": "method", "paper_id": None},
        "metrics_at": [1, 3, 5],
        "notes": "Fixture case.",
    }
    record.update(overrides)
    return record


class RagRetrievalEvalSchemaTests(unittest.TestCase):
    def test_load_eval_cases_parses_jsonl_and_filters(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "eval.jsonl"
            write_jsonl(path, [eval_record()])

            cases = evaluator.load_eval_cases(path)

        self.assertEqual(len(cases), 1)
        self.assertEqual(cases[0].query_id, "method_bayesian_uncertainty")
        self.assertEqual(cases[0].query, "bayesian uncertainty method")
        self.assertEqual(cases[0].filters, SearchFilters(source_type="reading_note", tag="method", paper_id=None))
        self.assertEqual(cases[0].metrics_at, [1, 3, 5])
        self.assertEqual(cases[0].must_retrieve, [{"paper_id": "paper-a", "tag": "method"}])

    def test_validate_eval_cases_rejects_missing_query_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "eval.jsonl"
            record = eval_record()
            del record["query_id"]
            write_jsonl(path, [record])

            with self.assertRaises(ValueError):
                evaluator.load_eval_cases(path)

    def test_validate_eval_cases_rejects_duplicate_query_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "eval.jsonl"
            write_jsonl(path, [eval_record(), eval_record()])

            with self.assertRaises(ValueError):
                evaluator.load_eval_cases(path)

    def test_validate_eval_cases_rejects_cases_without_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "eval.jsonl"
            write_jsonl(path, [eval_record(must_retrieve=[], relevant=[])])

            with self.assertRaises(ValueError):
                evaluator.load_eval_cases(path)

    def test_validate_eval_cases_rejects_unknown_filter_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "eval.jsonl"
            write_jsonl(path, [eval_record(filters={"unknown": "value"})])

            with self.assertRaises(ValueError):
                evaluator.load_eval_cases(path)


class RagRetrievalEvalMatchingTests(unittest.TestCase):
    def test_string_target_matches_exact_chunk_id(self):
        self.assertTrue(evaluator.target_matches_chunk("chunk-a", chunk("chunk-a", "text")))
        self.assertFalse(evaluator.target_matches_chunk("chunk-b", chunk("chunk-a", "text")))

    def test_dict_target_matches_metadata_and_tag(self):
        sample = chunk("chunk-a", "Bayesian method text", paper_id="paper-a", section="6. Method", tags=["method", "metric"])

        self.assertTrue(
            evaluator.target_matches_chunk(
                {"paper_id": "paper-a", "source_type": "reading_note", "section": "6. Method", "tag": "metric"},
                sample,
            )
        )
        self.assertFalse(evaluator.target_matches_chunk({"paper_id": "paper-b"}, sample))
        self.assertFalse(evaluator.target_matches_chunk({"tag": "dataset"}, sample))


class RagRetrievalEvalMetricTests(unittest.TestCase):
    def test_keyword_retriever_uses_existing_search_filters(self):
        chunks = [
            chunk("chunk-a", "Bayesian deep learning uncertainty method.", tags=["method"], chunk_index=1),
            chunk("chunk-b", "High-rate GNSS permanent displacement dataset.", tags=["dataset"], chunk_index=2),
        ]
        case = evaluator.EvalCase(
            query_id="case-a",
            query="bayesian uncertainty",
            intent="Find method.",
            must_retrieve=[{"paper_id": "paper-a", "tag": "method"}],
            relevant=[{"paper_id": "paper-a", "tag": "method"}],
            acceptable=[],
            filters=SearchFilters(tag="method"),
            metrics_at=[1, 3],
        )

        results = evaluator.keyword_retriever(chunks, case, limit=3)

        self.assertEqual(results[0]["chunk"]["chunk_id"], "chunk-a")

    def test_vector_retriever_is_registered_and_uses_filters(self):
        chunks = [
            chunk("chunk-a", "Bayesian deep learning uncertainty method.", tags=["method"], chunk_index=1),
            chunk("chunk-b", "High-rate GNSS permanent displacement dataset.", tags=["dataset"], chunk_index=2),
        ]
        case = evaluator.EvalCase(
            query_id="case-a",
            query="bayesian uncertainty",
            intent="Find method.",
            must_retrieve=[{"paper_id": "paper-a", "tag": "method"}],
            relevant=[{"paper_id": "paper-a", "tag": "method"}],
            acceptable=[],
            filters=SearchFilters(tag="method"),
            metrics_at=[1, 3],
        )

        results = evaluator.evaluate_cases([case], chunks, retriever_name="vector")

        self.assertEqual(results["retriever"], "vector")
        self.assertEqual(results["per_query"][0]["retrieved_chunk_ids"][0], "chunk-a")
        self.assertEqual(results["summary"]["mean_hit@1"], 1.0)

    def test_hybrid_retriever_is_registered_and_uses_filters(self):
        self.assertIn("hybrid", evaluator.RETRIEVERS)
        chunks = [
            chunk("chunk-a", "Bayesian deep learning uncertainty method.", tags=["method"], chunk_index=1),
            chunk("chunk-b", "High-rate GNSS permanent displacement dataset.", tags=["dataset"], chunk_index=2),
        ]
        case = evaluator.EvalCase(
            query_id="case-a",
            query="bayesian uncertainty",
            intent="Find method.",
            must_retrieve=[{"paper_id": "paper-a", "tag": "method"}],
            relevant=[{"paper_id": "paper-a", "tag": "method"}],
            acceptable=[],
            filters=SearchFilters(tag="method"),
            metrics_at=[1, 3],
        )

        results = evaluator.evaluate_cases([case], chunks, retriever_name="hybrid")

        self.assertEqual(results["retriever"], "hybrid")
        self.assertEqual(results["per_query"][0]["retrieved_chunk_ids"][0], "chunk-a")
        self.assertEqual(results["summary"]["mean_hit@1"], 1.0)

    def test_evaluate_case_computes_hits_recall_and_mrr(self):
        chunks = [
            chunk("chunk-a", "Bayesian deep learning uncertainty method.", tags=["method"], chunk_index=1),
            chunk("chunk-b", "High-rate GNSS permanent displacement dataset.", tags=["dataset"], chunk_index=2),
        ]
        case = evaluator.EvalCase(
            query_id="case-a",
            query="bayesian uncertainty",
            intent="Find method.",
            must_retrieve=[{"paper_id": "paper-a", "tag": "method"}],
            relevant=[{"paper_id": "paper-a", "tag": "method"}],
            acceptable=[],
            filters=None,
            metrics_at=[1, 3, 5],
        )

        result = evaluator.evaluate_case(case, chunks, limit=5)

        self.assertEqual(result["hit@1"], 1)
        self.assertEqual(result["must_hit@1"], 1)
        self.assertEqual(result["recall@1"], 1.0)
        self.assertEqual(result["mrr"], 1.0)
        self.assertEqual(result["top_rank"], 1)
        self.assertEqual(result["retrieved_chunk_ids"][0], "chunk-a")

    def test_evaluate_case_reports_miss(self):
        chunks = [chunk("chunk-a", "Dataset text only.", tags=["dataset"], chunk_index=1)]
        case = evaluator.EvalCase(
            query_id="case-a",
            query="bayesian uncertainty",
            intent="Find method.",
            must_retrieve=[{"paper_id": "missing", "tag": "method"}],
            relevant=[{"paper_id": "missing", "tag": "method"}],
            acceptable=[],
            filters=None,
            metrics_at=[1, 3],
        )

        result = evaluator.evaluate_case(case, chunks, limit=3)

        self.assertEqual(result["hit@1"], 0)
        self.assertEqual(result["hit@3"], 0)
        self.assertEqual(result["mrr"], 0.0)
        self.assertIsNone(result["top_rank"])

    def test_evaluate_cases_computes_aggregate_metrics(self):
        chunks = [
            chunk("chunk-a", "Bayesian deep learning uncertainty method.", paper_id="paper-a", tags=["method"], chunk_index=1),
            chunk("chunk-b", "GNSS dataset.", paper_id="paper-b", tags=["dataset"], chunk_index=2),
        ]
        cases = [
            evaluator.EvalCase(
                query_id="hit",
                query="bayesian uncertainty",
                intent="Hit case.",
                must_retrieve=[{"paper_id": "paper-a"}],
                relevant=[{"paper_id": "paper-a"}],
                acceptable=[],
                filters=None,
                metrics_at=[1, 3, 5],
            ),
            evaluator.EvalCase(
                query_id="miss",
                query="unknown query",
                intent="Miss case.",
                must_retrieve=[{"paper_id": "missing"}],
                relevant=[{"paper_id": "missing"}],
                acceptable=[],
                filters=None,
                metrics_at=[1, 3, 5],
            ),
        ]

        results = evaluator.evaluate_cases(cases, chunks)

        self.assertEqual(results["summary"]["num_queries"], 2)
        self.assertEqual(results["summary"]["mean_hit@1"], 0.5)
        self.assertEqual(results["summary"]["mrr"], 0.5)
        self.assertEqual(results["summary"]["failed_queries"], ["miss"])


class RagRetrievalEvalReportTests(unittest.TestCase):
    def test_run_writes_markdown_and_json_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            chunks_path = tmp_path / "chunks.jsonl"
            eval_path = tmp_path / "eval.jsonl"
            report_path = tmp_path / "report.md"
            json_path = tmp_path / "results.json"
            write_jsonl(chunks_path, [chunk("chunk-a", "Bayesian deep learning uncertainty method.")])
            write_jsonl(eval_path, [eval_record()])

            results = evaluator.run(chunks_path=chunks_path, eval_set_path=eval_path, report_path=report_path, json_output_path=json_path)

            self.assertEqual(results["summary"]["num_queries"], 1)
            self.assertTrue(report_path.exists())
            self.assertTrue(json_path.exists())
            self.assertIn("# RAG 检索评测报告", report_path.read_text(encoding="utf-8"))
            self.assertIn("method_bayesian_uncertainty", report_path.read_text(encoding="utf-8"))
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["retriever"], "keyword")

    def test_cli_happy_path_writes_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            chunks_path = tmp_path / "chunks.jsonl"
            eval_path = tmp_path / "eval.jsonl"
            report_path = tmp_path / "report.md"
            json_path = tmp_path / "results.json"
            write_jsonl(chunks_path, [chunk("chunk-a", "Bayesian deep learning uncertainty method.")])
            write_jsonl(eval_path, [eval_record()])

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/evaluate_rag_retrieval.py",
                    "--chunks",
                    str(chunks_path),
                    "--eval-set",
                    str(eval_path),
                    "--report",
                    str(report_path),
                    "--json-output",
                    str(json_path),
                ],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Evaluated 1 queries", result.stdout)
            self.assertTrue(report_path.exists())
            self.assertTrue(json_path.exists())

    def test_cli_vector_retriever_writes_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            chunks_path = tmp_path / "chunks.jsonl"
            eval_path = tmp_path / "eval.jsonl"
            report_path = tmp_path / "report.md"
            json_path = tmp_path / "results.json"
            write_jsonl(chunks_path, [chunk("chunk-a", "Bayesian deep learning uncertainty method.")])
            write_jsonl(eval_path, [eval_record()])

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/evaluate_rag_retrieval.py",
                    "--chunks",
                    str(chunks_path),
                    "--eval-set",
                    str(eval_path),
                    "--report",
                    str(report_path),
                    "--json-output",
                    str(json_path),
                    "--retriever",
                    "vector",
                ],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Evaluated 1 queries", result.stdout)
            self.assertIn("with vector retriever", result.stdout)
            self.assertTrue(report_path.exists())
            self.assertTrue(json_path.exists())
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["retriever"], "vector")

    def test_cli_hybrid_retriever_writes_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            chunks_path = tmp_path / "chunks.jsonl"
            eval_path = tmp_path / "eval.jsonl"
            report_path = tmp_path / "report.md"
            json_path = tmp_path / "results.json"
            write_jsonl(chunks_path, [chunk("chunk-a", "Bayesian deep learning uncertainty method.")])
            write_jsonl(eval_path, [eval_record()])

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/evaluate_rag_retrieval.py",
                    "--chunks",
                    str(chunks_path),
                    "--eval-set",
                    str(eval_path),
                    "--report",
                    str(report_path),
                    "--json-output",
                    str(json_path),
                    "--retriever",
                    "hybrid",
                ],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Evaluated 1 queries", result.stdout)
            self.assertIn("with hybrid retriever", result.stdout)
            self.assertTrue(report_path.exists())
            self.assertTrue(json_path.exists())
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["retriever"], "hybrid")

    def test_cli_help_lists_hybrid_retriever(self):
        result = subprocess.run(
            [sys.executable, "scripts/evaluate_rag_retrieval.py", "--help"],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("hybrid", result.stdout)
        self.assertIn("keyword", result.stdout)

    def test_cli_strict_mode_fails_when_threshold_is_not_met(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            chunks_path = tmp_path / "chunks.jsonl"
            eval_path = tmp_path / "eval.jsonl"
            report_path = tmp_path / "report.md"
            write_jsonl(chunks_path, [chunk("chunk-a", "Dataset text only.", tags=["dataset"])])
            write_jsonl(eval_path, [eval_record(query="bayesian uncertainty", must_retrieve=[{"paper_id": "missing"}], relevant=[{"paper_id": "missing"}], filters={})])

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/evaluate_rag_retrieval.py",
                    "--chunks",
                    str(chunks_path),
                    "--eval-set",
                    str(eval_path),
                    "--report",
                    str(report_path),
                    "--strict",
                    "--min-hit-at-5",
                    "1.0",
                ],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("below threshold", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
