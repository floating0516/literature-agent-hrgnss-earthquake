import json
import tempfile
import unittest
from pathlib import Path

from scripts.download_pdfs import (
    choose_pdf_url,
    load_jsonl,
    make_pdf_filename,
    write_jsonl,
)


class DownloadPdfPureFunctionTests(unittest.TestCase):
    def test_choose_pdf_url_prefers_top_level_pdf_url(self):
        record = {
            "title": "Example Paper",
            "pdf_url": "https://example.org/main.pdf",
            "best_oa_location": {"pdf_url": "https://example.org/oa.pdf"},
        }

        self.assertEqual(choose_pdf_url(record), "https://example.org/main.pdf")

    def test_choose_pdf_url_falls_back_to_best_oa_location(self):
        record = {
            "title": "Example Paper",
            "best_oa_location": {"pdf_url": "https://example.org/oa.pdf"},
        }

        self.assertEqual(choose_pdf_url(record), "https://example.org/oa.pdf")

    def test_choose_pdf_url_returns_none_without_pdf(self):
        record = {"title": "Closed Paper", "doi": "10.1234/closed"}

        self.assertIsNone(choose_pdf_url(record))

    def test_make_pdf_filename_uses_year_title_and_slug(self):
        record = {
            "year": 2024,
            "title": "Rapid Estimation of Source Parameters for the 2022 Event",
            "doi": "10.1000/example",
        }

        self.assertEqual(
            make_pdf_filename(record),
            "2024_rapid_estimation_of_source_parameters_for_the_2022.pdf",
        )

    def test_make_pdf_filename_falls_back_to_doi_slug(self):
        record = {"doi": "10.1000/ABC.Def-01"}

        self.assertEqual(make_pdf_filename(record), "10_1000_abc_def_01.pdf")

    def test_load_and_write_jsonl_round_trip(self):
        records = [
            {"title": "A", "pdf_url": "https://example.org/a.pdf"},
            {"title": "B", "pdf_url": None},
        ]

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "records.jsonl"
            write_jsonl(path, records)

            self.assertEqual(load_jsonl(path), records)
            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(json.loads(lines[0])["title"], "A")


if __name__ == "__main__":
    unittest.main()
