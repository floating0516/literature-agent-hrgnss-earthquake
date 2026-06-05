import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.parse_pdfs import main, parse_args, parse_pdf, write_log


class PdfParseTests(unittest.TestCase):
    def test_parse_pdf_returns_error_when_pdftotext_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            pdf_path = tmp_path / "paper.pdf"
            output_dir = tmp_path / "parsed_md"
            pdf_path.write_bytes(b"%PDF-1.7\n")

            with patch("scripts.parse_pdfs.subprocess.run", side_effect=FileNotFoundError("pdftotext")):
                md_path, error = parse_pdf(pdf_path, output_dir, backend="pdftotext")

            self.assertEqual(md_path, output_dir / "paper.md")
            self.assertIsNotNone(error)
            self.assertIn("pdftotext", error)
            self.assertFalse(md_path.exists())

    def test_parse_pdf_returns_error_when_text_output_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            pdf_path = tmp_path / "paper.pdf"
            output_dir = tmp_path / "parsed_md"
            pdf_path.write_bytes(b"%PDF-1.7\n")

            with patch("scripts.parse_pdfs.subprocess.run"):
                md_path, error = parse_pdf(pdf_path, output_dir, backend="pdftotext")

            self.assertEqual(md_path, output_dir / "paper.md")
            self.assertIsNotNone(error)
            self.assertIn("paper.txt", error)
            self.assertFalse(md_path.exists())

    def test_parse_pdf_writes_markdown_and_removes_intermediate_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            pdf_path = tmp_path / "high_rate_gnss.pdf"
            output_dir = tmp_path / "parsed_md"
            pdf_path.write_bytes(b"%PDF-1.7\n")

            def fake_pdftotext(command, **kwargs):
                text_path = Path(command[-1])
                text_path.write_text("  High-rate GNSS text.  \n", encoding="utf-8")

            with patch("scripts.parse_pdfs.subprocess.run", side_effect=fake_pdftotext):
                md_path, error = parse_pdf(pdf_path, output_dir, backend="pdftotext")

            self.assertIsNone(error)
            self.assertEqual(md_path, output_dir / "high_rate_gnss.md")
            self.assertFalse((output_dir / "high_rate_gnss.txt").exists())
            md_text = md_path.read_text(encoding="utf-8")
            self.assertIn("# High Rate Gnss", md_text)
            self.assertIn("Source PDF: `papers/raw_pdf/high_rate_gnss.pdf`", md_text)
            self.assertIn("High-rate GNSS text.", md_text)

    def test_parse_pdf_uses_pymupdf4llm_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            pdf_path = tmp_path / "default_backend.pdf"
            output_dir = tmp_path / "parsed_md"
            pdf_path.write_bytes(b"%PDF-1.7\n")
            fake_module = types.SimpleNamespace(to_markdown=lambda path: "Default backend markdown.")

            with patch.dict(sys.modules, {"pymupdf4llm": fake_module}):
                md_path, error = parse_pdf(pdf_path, output_dir)

            self.assertIsNone(error)
            md_text = md_path.read_text(encoding="utf-8")
            self.assertIn("Parser: `pymupdf4llm`", md_text)
            self.assertIn("Default backend markdown.", md_text)

    def test_parse_pdf_uses_pymupdf4llm_backend_for_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            pdf_path = tmp_path / "paper.pdf"
            output_dir = tmp_path / "parsed_md"
            pdf_path.write_bytes(b"%PDF-1.7\n")
            fake_module = types.SimpleNamespace(to_markdown=lambda path: "# Extracted\n\nGNSS markdown text.")

            with patch.dict(sys.modules, {"pymupdf4llm": fake_module}):
                md_path, error = parse_pdf(pdf_path, output_dir, backend="pymupdf4llm")

            self.assertIsNone(error)
            self.assertEqual(md_path, output_dir / "paper.md")
            md_text = md_path.read_text(encoding="utf-8")
            self.assertIn("Source PDF: `papers/raw_pdf/paper.pdf`", md_text)
            self.assertIn("Parser: `pymupdf4llm`", md_text)
            self.assertIn("# Extracted", md_text)
            self.assertIn("GNSS markdown text.", md_text)

    def test_parse_pdf_returns_error_when_pymupdf4llm_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            pdf_path = tmp_path / "paper.pdf"
            output_dir = tmp_path / "parsed_md"
            pdf_path.write_bytes(b"%PDF-1.7\n")

            with patch.dict(sys.modules, {"pymupdf4llm": None}):
                md_path, error = parse_pdf(pdf_path, output_dir, backend="pymupdf4llm")

            self.assertEqual(md_path, output_dir / "paper.md")
            self.assertIsNotNone(error)
            self.assertIn("pymupdf4llm", error)
            self.assertFalse(md_path.exists())


class PdfParseCliTests(unittest.TestCase):
    def test_parse_args_defaults_to_pymupdf4llm_backend(self):
        with patch.object(sys, "argv", ["parse_pdfs.py"]):
            args = parse_args()

        self.assertEqual(args.backend, "pymupdf4llm")

    def test_parse_args_accepts_pymupdf4llm_backend(self):
        with patch.object(sys, "argv", ["parse_pdfs.py", "--backend", "pymupdf4llm"]):
            args = parse_args()

        self.assertEqual(args.backend, "pymupdf4llm")

    def test_parse_args_accepts_single_pdf_path(self):
        with patch.object(sys, "argv", ["parse_pdfs.py", "--pdf", "papers/raw_pdf/example.pdf"]):
            args = parse_args()

        self.assertEqual(args.pdf, Path("papers/raw_pdf/example.pdf"))

    def test_main_parses_single_pdf_when_pdf_argument_is_provided(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = tmp_path / "raw_pdf"
            output_dir = tmp_path / "parsed_md"
            log_path = tmp_path / "pdf_parse_log.md"
            pdf_path = tmp_path / "one.pdf"
            pdf_path.write_bytes(b"%PDF-1.7\n")
            (input_dir / "ignored.pdf").parent.mkdir(parents=True)
            (input_dir / "ignored.pdf").write_bytes(b"%PDF-1.7\n")

            fake_module = types.SimpleNamespace(to_markdown=lambda path: f"Parsed {Path(path).name}.")
            argv = [
                "parse_pdfs.py",
                "--input-dir",
                str(input_dir),
                "--pdf",
                str(pdf_path),
                "--output-dir",
                str(output_dir),
                "--log",
                str(log_path),
            ]

            with patch.object(sys, "argv", argv), patch.dict(sys.modules, {"pymupdf4llm": fake_module}):
                main()

            self.assertTrue((output_dir / "one.md").exists())
            self.assertFalse((output_dir / "ignored.md").exists())
            log_text = log_path.read_text(encoding="utf-8")
            self.assertIn("one.pdf", log_text)
            self.assertNotIn("ignored.pdf", log_text)


class PdfParseLogTests(unittest.TestCase):
    def test_write_log_creates_parent_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            log_path = tmp_path / "logs" / "pdf_parse_log.md"
            pdf_path = tmp_path / "raw_pdf" / "example.pdf"
            md_path = tmp_path / "parsed_md" / "example.md"

            write_log(log_path, [(pdf_path, md_path, None)], backend="pymupdf4llm")

            self.assertTrue(log_path.exists())
            log_text = log_path.read_text(encoding="utf-8")
            self.assertIn("example.pdf", log_text)
            self.assertIn("success", log_text)
            self.assertIn("pymupdf4llm", log_text)

    def test_write_log_uses_actual_markdown_output_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            log_path = tmp_path / "logs" / "pdf_parse_log.md"
            pdf_path = tmp_path / "raw_pdf" / "example.pdf"
            md_path = tmp_path / "custom_output" / "example.md"

            write_log(log_path, [(pdf_path, md_path, None)])

            log_text = log_path.read_text(encoding="utf-8")
            self.assertIn(f"`{md_path}`", log_text)
            self.assertNotIn("papers/parsed_md/example.md", log_text)


if __name__ == "__main__":
    unittest.main()
