import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.download_pdfs import (
    DownloadConfig,
    choose_pdf_url,
    download_pdf,
    load_jsonl,
    make_pdf_filename,
    target_pdf_path,
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

    def test_download_pdf_rejects_non_pdf_response(self):
        record = {
            "title": "HTML landing page",
            "year": 2024,
            "doi": "10.1000/html",
            "pdf_url": "https://example.org/not-a-pdf",
        }

        class FakeResponse:
            def __init__(self, *, headers, data):
                self.headers = headers
                self._data = data

            def read(self):
                return self._data

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

        with tempfile.TemporaryDirectory() as tmp:
            config = DownloadConfig(pdf_dir=Path(tmp))
            with patch(
                "scripts.download_pdfs.urllib.request.urlopen",
                return_value=FakeResponse(
                    headers={"Content-Type": "text/html; charset=utf-8"},
                    data=b"<html>not a pdf</html>",
                ),
            ):
                result = download_pdf(record, config)

            self.assertEqual(result["download_status"], "failed")
            self.assertIsNone(result["downloaded_pdf"])
            self.assertFalse(any(Path(tmp).iterdir()))

    def test_same_year_title_different_doi_need_distinct_target_paths(self):
        record_one = {
            "year": 2024,
            "title": "Same Title",
            "doi": "10.1000/alpha",
        }
        record_two = {
            "year": 2024,
            "title": "Same Title",
            "doi": "10.1000/beta",
        }

        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            first_path = target_pdf_path(record_one, output_dir)
            first_path.write_bytes(b"%PDF-1.7\n")
            second_path = target_pdf_path(record_two, output_dir)

            self.assertNotEqual(first_path, second_path)


if __name__ == "__main__":
    unittest.main()
