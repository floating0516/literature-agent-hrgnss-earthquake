import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import compare_rag_retrieval as comparer


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


class CompareRagRetrievalTests(unittest.TestCase):
    def test_run_compares_keyword_vector_and_hybrid(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            chunks_path = tmp_path / "chunks.jsonl"
            eval_path = tmp_path / "eval.jsonl"
            report_path = tmp_path / "compare.md"
            json_path = tmp_path / "compare.json"
            write_jsonl(chunks_path, [chunk("chunk-a", "Bayesian deep learning uncertainty method.")])
            write_jsonl(eval_path, [eval_record()])

            results = comparer.run(
                chunks_path=chunks_path,
                eval_set_path=eval_path,
                report_path=report_path,
                json_output_path=json_path,
            )

            self.assertEqual(results["retrievers"], ["keyword", "vector", "hybrid"])
            self.assertEqual(set(results["runs"]), {"keyword", "vector", "hybrid"})
            self.assertIn("comparison_summary", results)
            self.assertIn("per_query_comparison", results)
            self.assertEqual(results["warnings"], [])
            self.assertEqual(results["comparison_summary"]["keyword"]["mean_hit@5"], 1.0)
            self.assertEqual(results["per_query_comparison"][0]["query_id"], "method_bayesian_uncertainty")
            self.assertTrue(report_path.exists())
            self.assertTrue(json_path.exists())
            self.assertIn("# RAG 检索对比报告", report_path.read_text(encoding="utf-8"))
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["retrievers"], ["keyword", "vector", "hybrid"])

    def test_cli_writes_markdown_and_json_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            chunks_path = tmp_path / "chunks.jsonl"
            eval_path = tmp_path / "eval.jsonl"
            report_path = tmp_path / "compare.md"
            json_path = tmp_path / "compare.json"
            write_jsonl(chunks_path, [chunk("chunk-a", "Bayesian deep learning uncertainty method.")])
            write_jsonl(eval_path, [eval_record()])

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/compare_rag_retrieval.py",
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
            self.assertIn("Compared 3 retrievers", result.stdout)
            self.assertIn("keyword", result.stdout)
            self.assertIn("vector", result.stdout)
            self.assertIn("hybrid", result.stdout)
            self.assertTrue(report_path.exists())
            self.assertTrue(json_path.exists())

    def test_cli_help_lists_strict_options(self):
        result = subprocess.run(
            [sys.executable, "scripts/compare_rag_retrieval.py", "--help"],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--strict", result.stdout)
        self.assertIn("--min-hit-at-5", result.stdout)
        self.assertIn("--min-mrr", result.stdout)

    def test_cli_strict_mode_fails_when_threshold_is_not_met(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            chunks_path = tmp_path / "chunks.jsonl"
            eval_path = tmp_path / "eval.jsonl"
            report_path = tmp_path / "compare.md"
            write_jsonl(chunks_path, [chunk("chunk-a", "Bayesian deep learning uncertainty method.")])
            write_jsonl(eval_path, [eval_record()])

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/compare_rag_retrieval.py",
                    "--chunks",
                    str(chunks_path),
                    "--eval-set",
                    str(eval_path),
                    "--report",
                    str(report_path),
                    "--strict",
                    "--min-hit-at-5",
                    "1.1",
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
