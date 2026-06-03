import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.download_pdfs import make_pdf_filename
from scripts.match_manual_pdfs import (
    ManualMatchConfig,
    extract_doi_candidates,
    load_jsonl,
    match_manual_pdfs,
    normalize_doi,
    write_jsonl,
)


class ManualPdfMatchTests(unittest.TestCase):
    def test_normalize_doi_removes_url_prefix_and_case_noise(self):
        self.assertEqual(normalize_doi(" https://doi.org/10.1000/ABC.Def. "), "10.1000/abc.def")
        self.assertEqual(normalize_doi("doi:10.5555/Example-01,"), "10.5555/example-01")

    def test_extract_doi_candidates_from_filename(self):
        candidates = extract_doi_candidates("manual copy 10.1000_example-01 final.pdf")

        self.assertIn("10.1000/example-01", candidates)

    def test_doi_filename_match_updates_failed_record_on_apply(self):
        records = [
            {
                "title": "Interrupted Paper",
                "year": 2024,
                "doi": "10.1000/interrupted",
                "download_status": "failed",
                "download_note": "HTTP Error 403: Forbidden",
            }
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            results_path = tmp_path / "results.jsonl"
            manual_dir = tmp_path / "manual"
            raw_dir = tmp_path / "raw_pdf"
            log_path = tmp_path / "manual_pdf_match_log.md"
            manual_dir.mkdir()
            manual_pdf = manual_dir / "publisher_copy_10.1000_interrupted.pdf"
            manual_pdf.write_bytes(b"%PDF-manual\n")
            write_jsonl(results_path, records)

            summary = match_manual_pdfs(
                ManualMatchConfig(
                    input_path=tmp_path / "selected.jsonl",
                    results_path=results_path,
                    manual_dir=manual_dir,
                    pdf_dir=raw_dir,
                    log_path=log_path,
                    apply=True,
                )
            )

            updated = load_jsonl(results_path)
            target = raw_dir / make_pdf_filename(records[0])
            self.assertEqual(summary["matched"], 1)
            self.assertTrue(target.exists())
            self.assertTrue(manual_pdf.exists())
            self.assertEqual(updated[0]["download_status"], "matched_manual")
            self.assertEqual(updated[0]["download_source"], "manual_pdf")
            self.assertEqual(updated[0]["manual_match_method"], "doi_exact")
            self.assertEqual(updated[0]["manual_match_confidence"], "high")
            self.assertEqual(updated[0]["downloaded_pdf"], str(target))
            self.assertEqual(updated[0]["manual_pdf_source"], str(manual_pdf))

    def test_title_year_match_copies_to_canonical_pdf_on_apply(self):
        records = [
            {
                "title": "Rapid Estimation of Source Parameters",
                "year": 2022,
                "doi": "10.1000/rapid",
                "download_status": "manual_required",
            }
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            results_path = tmp_path / "results.jsonl"
            manual_dir = tmp_path / "manual"
            raw_dir = tmp_path / "raw_pdf"
            manual_dir.mkdir()
            manual_pdf = manual_dir / "2022 rapid estimation source parameters final.pdf"
            manual_pdf.write_bytes(b"%PDF-title\n")
            write_jsonl(results_path, records)

            summary = match_manual_pdfs(
                ManualMatchConfig(
                    results_path=results_path,
                    manual_dir=manual_dir,
                    pdf_dir=raw_dir,
                    log_path=tmp_path / "log.md",
                    apply=True,
                )
            )

            updated = load_jsonl(results_path)
            target = raw_dir / make_pdf_filename(records[0])
            self.assertEqual(summary["matched"], 1)
            self.assertTrue(target.exists())
            self.assertEqual(updated[0]["download_status"], "matched_manual")
            self.assertEqual(updated[0]["manual_match_method"], "title_year_strong")

    def test_ambiguous_title_match_does_not_copy_or_update_results(self):
        records = [
            {"title": "Rapid Tsunami Warning", "year": 2020, "doi": "10.1/a", "download_status": "failed"},
            {"title": "Rapid Tsunami Warning", "year": 2020, "doi": "10.1/b", "download_status": "manual_required"},
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            results_path = tmp_path / "results.jsonl"
            manual_dir = tmp_path / "manual"
            raw_dir = tmp_path / "raw_pdf"
            manual_dir.mkdir()
            (manual_dir / "2020 rapid tsunami warning.pdf").write_bytes(b"%PDF-ambiguous\n")
            write_jsonl(results_path, records)

            summary = match_manual_pdfs(
                ManualMatchConfig(
                    results_path=results_path,
                    manual_dir=manual_dir,
                    pdf_dir=raw_dir,
                    log_path=tmp_path / "log.md",
                    apply=True,
                )
            )

            self.assertEqual(summary["ambiguous"], 1)
            self.assertFalse(raw_dir.exists())
            self.assertEqual(load_jsonl(results_path), records)

    def test_dry_run_does_not_copy_or_update_results(self):
        records = [
            {"title": "Dry Run Paper", "year": 2024, "doi": "10.1000/dry-run", "download_status": "failed"}
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            results_path = tmp_path / "results.jsonl"
            manual_dir = tmp_path / "manual"
            raw_dir = tmp_path / "raw_pdf"
            manual_dir.mkdir()
            (manual_dir / "10.1000_dry-run.pdf").write_bytes(b"%PDF-dry\n")
            write_jsonl(results_path, records)

            summary = match_manual_pdfs(
                ManualMatchConfig(
                    results_path=results_path,
                    manual_dir=manual_dir,
                    pdf_dir=raw_dir,
                    log_path=tmp_path / "log.md",
                    apply=False,
                )
            )

            self.assertEqual(summary["matched"], 1)
            self.assertFalse(raw_dir.exists())
            self.assertEqual(load_jsonl(results_path), records)

    def test_existing_target_without_overwrite_is_not_replaced(self):
        records = [
            {"title": "Existing Target", "year": 2024, "doi": "10.1000/existing", "download_status": "failed"}
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            results_path = tmp_path / "results.jsonl"
            manual_dir = tmp_path / "manual"
            raw_dir = tmp_path / "raw_pdf"
            manual_dir.mkdir()
            raw_dir.mkdir()
            target = raw_dir / make_pdf_filename(records[0])
            target.write_bytes(b"%PDF-existing\n")
            (manual_dir / "10.1000_existing.pdf").write_bytes(b"%PDF-new\n")
            write_jsonl(results_path, records)

            summary = match_manual_pdfs(
                ManualMatchConfig(
                    results_path=results_path,
                    manual_dir=manual_dir,
                    pdf_dir=raw_dir,
                    log_path=tmp_path / "log.md",
                    apply=True,
                    overwrite=False,
                )
            )

            self.assertEqual(summary["skipped_existing"], 1)
            self.assertEqual(target.read_bytes(), b"%PDF-existing\n")
            self.assertEqual(load_jsonl(results_path), records)

    def test_only_failed_and_manual_required_records_are_considered_by_default(self):
        records = [
            {"title": "Already Downloaded", "year": 2024, "doi": "10.1000/downloaded", "download_status": "downloaded"},
            {"title": "Needs Manual", "year": 2024, "doi": "10.1000/manual", "download_status": "manual_required"},
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            results_path = tmp_path / "results.jsonl"
            manual_dir = tmp_path / "manual"
            raw_dir = tmp_path / "raw_pdf"
            manual_dir.mkdir()
            (manual_dir / "10.1000_downloaded.pdf").write_bytes(b"%PDF-downloaded\n")
            (manual_dir / "10.1000_manual.pdf").write_bytes(b"%PDF-manual\n")
            write_jsonl(results_path, records)

            summary = match_manual_pdfs(
                ManualMatchConfig(
                    results_path=results_path,
                    manual_dir=manual_dir,
                    pdf_dir=raw_dir,
                    log_path=tmp_path / "log.md",
                    apply=True,
                )
            )

            updated = load_jsonl(results_path)
            self.assertEqual(summary["matched"], 1)
            self.assertEqual(updated[0]["download_status"], "downloaded")
            self.assertEqual(updated[1]["download_status"], "matched_manual")
            self.assertFalse((raw_dir / make_pdf_filename(records[0])).exists())
            self.assertTrue((raw_dir / make_pdf_filename(records[1])).exists())

    def test_match_log_records_unmatched_manual_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            results_path = tmp_path / "results.jsonl"
            manual_dir = tmp_path / "manual"
            log_path = tmp_path / "log.md"
            manual_dir.mkdir()
            (manual_dir / "unknown.pdf").write_bytes(b"%PDF-unknown\n")
            write_jsonl(results_path, [])

            summary = match_manual_pdfs(
                ManualMatchConfig(
                    results_path=results_path,
                    manual_dir=manual_dir,
                    pdf_dir=tmp_path / "raw_pdf",
                    log_path=log_path,
                    apply=False,
                )
            )

            self.assertEqual(summary["unmatched"], 1)
            log_text = log_path.read_text(encoding="utf-8")
            self.assertIn("unknown.pdf", log_text)
            self.assertIn("unmatched", log_text)

    def test_cli_script_runs_directly_from_project_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            results_path = tmp_path / "results.jsonl"
            manual_dir = tmp_path / "manual"
            raw_dir = tmp_path / "raw_pdf"
            log_path = tmp_path / "log.md"
            manual_dir.mkdir()
            write_jsonl(
                results_path,
                [
                    {
                        "title": "CLI Smoke Paper",
                        "year": 2024,
                        "doi": "10.1000/cli-smoke",
                        "download_status": "failed",
                    }
                ],
            )
            (manual_dir / "10.1000_cli-smoke.pdf").write_bytes(b"%PDF-cli\n")

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/match_manual_pdfs.py",
                    "--results",
                    str(results_path),
                    "--manual-dir",
                    str(manual_dir),
                    "--pdf-dir",
                    str(raw_dir),
                    "--log",
                    str(log_path),
                    "--dry-run",
                ],
                cwd=PROJECT_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Matched: 1", result.stdout)
            self.assertTrue(log_path.exists())
            self.assertFalse(raw_dir.exists())


if __name__ == "__main__":
    unittest.main()
