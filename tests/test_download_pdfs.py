import json
import socket
import sys
import tempfile
import threading
import unittest
import urllib.request
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.download_pdfs import (
    DownloadConfig,
    choose_pdf_url,
    download_pdf,
    load_jsonl,
    make_pdf_filename,
    run,
    target_pdf_path,
    write_jsonl,
)


class StaticResponseHandler(BaseHTTPRequestHandler):
    routes = {}

    def do_GET(self):
        response = self.routes.get(self.path)
        if response is None:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(response["status"])
        self.send_header("Content-Type", response["content_type"])
        self.send_header("Content-Length", str(len(response["body"])))
        self.end_headers()
        self.wfile.write(response["body"])

    def log_message(self, format, *args):
        return


class LocalHttpServer:
    def __init__(self, routes):
        self._routes = routes
        self._server = None
        self._thread = None
        self.base_url = None

    def __enter__(self):
        handler = type("ConfiguredStaticResponseHandler", (StaticResponseHandler,), {"routes": self._routes})
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        host, port = self._server.server_address
        self.base_url = f"http://{host}:{port}"
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        self._wait_until_ready()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=5)
        return False

    def url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _wait_until_ready(self):
        host, port = self._server.server_address
        with socket.create_connection((host, port), timeout=5):
            return


@contextmanager
def no_proxy_url_opener():
    previous_opener = urllib.request._opener
    urllib.request._opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        yield
    finally:
        urllib.request._opener = previous_opener


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

    def test_download_pdf_rejects_html_response(self):
        record = {
            "title": "HTML landing page",
            "year": 2024,
            "doi": "10.1000/html",
        }

        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "raw_pdf"
            with LocalHttpServer(
                {
                    "/not-a-pdf": {
                        "status": 200,
                        "content_type": "text/html; charset=utf-8",
                        "body": b"<html>not a pdf</html>",
                    }
                }
            ) as server:
                config = DownloadConfig(pdf_dir=output_dir)
                with no_proxy_url_opener():
                    result = download_pdf(
                        {**record, "pdf_url": server.url("/not-a-pdf")},
                        config,
                    )

            self.assertEqual(result["download_status"], "failed")
            self.assertIsNone(result["downloaded_pdf"])
            self.assertIn("Non-PDF response", result["download_note"])
            self.assertEqual(list(output_dir.iterdir()), [])

    def test_download_pdf_saves_pdf_bytes(self):
        record = {
            "title": "Download me",
            "year": 2024,
            "doi": "10.1000/pdf",
        }
        pdf_bytes = b"%PDF-1.7\nlocal test pdf\n"

        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "raw_pdf"
            with LocalHttpServer(
                {
                    "/paper.pdf": {
                        "status": 200,
                        "content_type": "application/pdf",
                        "body": pdf_bytes,
                    }
                }
            ) as server:
                config = DownloadConfig(pdf_dir=output_dir)
                with no_proxy_url_opener():
                    result = download_pdf(
                        {**record, "pdf_url": server.url("/paper.pdf")},
                        config,
                    )

            expected_path = output_dir / make_pdf_filename(record)
            self.assertEqual(result["download_status"], "downloaded")
            self.assertEqual(result["downloaded_pdf"], str(expected_path))
            self.assertEqual(expected_path.read_bytes(), pdf_bytes)

    def test_run_writes_results_and_markdown_log(self):
        pdf_bytes = b"%PDF-1.7\nrun test pdf\n"

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_path = tmp_path / "selected_papers.jsonl"
            output_path = tmp_path / "results" / "download_results.jsonl"
            log_path = tmp_path / "logs" / "pdf_download_log.md"
            pdf_dir = tmp_path / "pdfs"

            with LocalHttpServer(
                {
                    "/paper.pdf": {
                        "status": 200,
                        "content_type": "application/pdf",
                        "body": pdf_bytes,
                    }
                }
            ) as server:
                records = [
                    {
                        "title": "Download me",
                        "year": 2024,
                        "doi": "10.1000/pdf",
                        "pdf_url": server.url("/paper.pdf"),
                    },
                    {
                        "title": "Needs manual handling",
                        "year": 2023,
                        "doi": "10.1000/manual",
                    },
                ]
                write_jsonl(input_path, records)
                config = DownloadConfig(
                    input_path=input_path,
                    output_path=output_path,
                    log_path=log_path,
                    pdf_dir=pdf_dir,
                )
                with no_proxy_url_opener():
                    results = run(config)

            self.assertEqual(len(results), 2)
            self.assertEqual(load_jsonl(output_path), results)
            log_text = log_path.read_text(encoding="utf-8")
            self.assertIn("## 总览", log_text)
            self.assertIn("- 下载成功：1", log_text)
            self.assertIn("- 需要人工处理：1", log_text)
            self.assertIn(f"- 输入文件：{input_path}", log_text)
            self.assertIn(f"- PDF 输出目录：{pdf_dir}", log_text)
            self.assertIn(f"- 结果文件：{output_path}", log_text)
            self.assertIn(f"- 日志文件：{log_path}", log_text)
            self.assertIn(str(pdf_dir / "2024_download_me.pdf"), log_text)

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

    def test_download_pdf_skips_existing_suffixed_target_when_overwrite_disabled(self):
        record_one = {
            "year": 2024,
            "title": "Same Title",
            "doi": "10.1000/alpha",
            "pdf_url": "https://example.org/alpha.pdf",
        }
        record_two = {
            "year": 2024,
            "title": "Same Title",
            "doi": "10.1000/beta",
            "pdf_url": "https://example.org/beta.pdf",
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
            output_dir = Path(tmp)
            config = DownloadConfig(pdf_dir=output_dir, overwrite=False)
            base_path = output_dir / make_pdf_filename(record_two)
            base_path.write_bytes(b"%PDF-base\n")
            suffix_path = target_pdf_path(record_two, output_dir)
            suffix_path.write_bytes(b"%PDF-existing-suffix\n")

            with patch(
                "scripts.download_pdfs.urllib.request.urlopen",
                return_value=FakeResponse(
                    headers={"Content-Type": "application/pdf"},
                    data=b"%PDF-new-download\n",
                ),
            ):
                result = download_pdf(record_two, config)

            self.assertEqual(result["download_status"], "skipped_existing")
            self.assertEqual(result["downloaded_pdf"], str(suffix_path))
            self.assertEqual(suffix_path.read_bytes(), b"%PDF-existing-suffix\n")


if __name__ == "__main__":
    unittest.main()
