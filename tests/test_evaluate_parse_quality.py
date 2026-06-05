import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import evaluate_parse_quality


GOOD_MARKDOWN = """# Example Paper

> Source PDF: `papers/raw_pdf/example.pdf`
> Parser: `pymupdf4llm`

---

## Abstract

High-rate GNSS observations provide robust coseismic displacement estimates for rapid earthquake source characterization. This section contains enough continuous scientific prose to represent a readable extracted paper body.

## 1. Introduction

Real-time GNSS seismology supports earthquake early warning by measuring large static offsets without magnitude saturation. The extracted Markdown preserves sections and paragraphs that can be reviewed before RAG chunking.

## 2. Method

The method combines displacement time series, geodetic inversion, and uncertainty estimation. The text is coherent, has normal line lengths, and does not contain unusual replacement characters or repeated extraction artifacts.
"""


class ParseQualityTests(unittest.TestCase):
    def test_good_markdown_passes_quality_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            md_path = Path(tmp) / "example.md"
            md_path.write_text(GOOD_MARKDOWN, encoding="utf-8")

            record = evaluate_parse_quality.evaluate_markdown(md_path)

        self.assertEqual(record["status"], "pass")
        self.assertGreaterEqual(record["score"], 80)
        self.assertEqual(record["parser"], "pymupdf4llm")
        self.assertEqual(record["source_pdf"], "papers/raw_pdf/example.pdf")
        self.assertTrue(record["checks"]["has_body"])

    def test_short_markdown_fails_quality_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            md_path = Path(tmp) / "short.md"
            md_path.write_text("# Short\n\nToo short.\n", encoding="utf-8")

            record = evaluate_parse_quality.evaluate_markdown(md_path)

        self.assertEqual(record["status"], "fail")
        self.assertLess(record["score"], 60)
        self.assertIn("document body is too short", record["reasons"])

    def test_reference_heavy_markdown_warns(self):
        references = "\n".join(f"[{index}] Reference title and journal information." for index in range(1, 35))
        markdown = GOOD_MARKDOWN + "\n## References\n\n" + references
        with tempfile.TemporaryDirectory() as tmp:
            md_path = Path(tmp) / "reference_heavy.md"
            md_path.write_text(markdown, encoding="utf-8")

            record = evaluate_parse_quality.evaluate_markdown(md_path)

        self.assertIn(record["status"], {"warn", "fail"})
        self.assertFalse(record["checks"]["low_reference_ratio"])
        self.assertIn("reference section dominates document", record["reasons"])

    def test_run_writes_jsonl_and_markdown_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = tmp_path / "parsed_md"
            output_path = tmp_path / "parse_quality.jsonl"
            report_path = tmp_path / "parse_quality_report.md"
            input_dir.mkdir()
            (input_dir / "example.md").write_text(GOOD_MARKDOWN, encoding="utf-8")

            records = evaluate_parse_quality.run(input_dir=input_dir, output_path=output_path, report_path=report_path)

            self.assertEqual(len(records), 1)
            self.assertTrue(output_path.exists())
            self.assertTrue(report_path.exists())
            payload = json.loads(output_path.read_text(encoding="utf-8").strip())
            self.assertEqual(payload["source_file"], str(input_dir / "example.md"))
            self.assertIn("# PDF 解析质量报告", report_path.read_text(encoding="utf-8"))

    def test_help_command_succeeds(self):
        result = subprocess.run(
            [sys.executable, "scripts/evaluate_parse_quality.py", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Evaluate parsed PDF Markdown quality", result.stdout)


if __name__ == "__main__":
    unittest.main()
