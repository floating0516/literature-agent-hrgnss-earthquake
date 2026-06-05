import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import call, patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import run_pipeline


class RunPipelineCliTests(unittest.TestCase):
    def test_parse_args_defaults_to_full_pipeline_without_manual_match(self):
        with patch.object(sys, "argv", ["run_pipeline.py"]):
            args = run_pipeline.parse_args()

        self.assertEqual(args.from_stage, "search")
        self.assertEqual(args.to_stage, "rag")
        self.assertFalse(args.match_manual)
        self.assertEqual(args.parse_backend, "pymupdf4llm")

    def test_selected_stages_respect_from_and_to_stage(self):
        with patch.object(sys, "argv", ["run_pipeline.py", "--from-stage", "download", "--to-stage", "parse"]):
            args = run_pipeline.parse_args()

        self.assertEqual(run_pipeline.selected_stages(args), ["download", "parse"])

    def test_selected_stages_include_manual_match_only_when_requested(self):
        with patch.object(sys, "argv", ["run_pipeline.py", "--from-stage", "download", "--to-stage", "parse", "--match-manual"]):
            args = run_pipeline.parse_args()

        self.assertEqual(run_pipeline.selected_stages(args), ["download", "match_manual", "parse"])

    def test_skip_flags_remove_matching_stages(self):
        with patch.object(sys, "argv", ["run_pipeline.py", "--skip-download", "--skip-parse"]):
            args = run_pipeline.parse_args()

        self.assertEqual(run_pipeline.selected_stages(args), ["search", "screen", "rag"])

    def test_help_command_succeeds(self):
        result = subprocess.run(
            [sys.executable, "scripts/run_pipeline.py", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Run the literature-reading pipeline", result.stdout)
        self.assertIn("--from-stage", result.stdout)
        self.assertIn("--parse-backend", result.stdout)


class RunPipelineExecutionTests(unittest.TestCase):
    def test_pipeline_runs_selected_stages_in_order(self):
        events = []

        with (
            patch("scripts.run_pipeline.run_search", side_effect=lambda args: events.append("search")),
            patch("scripts.run_pipeline.run_screen", side_effect=lambda args: events.append("screen")),
            patch("scripts.run_pipeline.run_download", side_effect=lambda args: events.append("download")),
            patch("scripts.run_pipeline.run_manual_match", side_effect=lambda args: events.append("match_manual")),
            patch("scripts.run_pipeline.run_parse", side_effect=lambda args: events.append("parse")),
            patch("scripts.run_pipeline.run_rag", side_effect=lambda args: events.append("rag")),
            patch.object(sys, "argv", ["run_pipeline.py", "--match-manual"]),
        ):
            run_pipeline.main()

        self.assertEqual(events, ["search", "screen", "download", "match_manual", "parse", "rag"])

    def test_pipeline_skips_manual_match_by_default(self):
        events = []

        with (
            patch("scripts.run_pipeline.run_search", side_effect=lambda args: events.append("search")),
            patch("scripts.run_pipeline.run_screen", side_effect=lambda args: events.append("screen")),
            patch("scripts.run_pipeline.run_download", side_effect=lambda args: events.append("download")),
            patch("scripts.run_pipeline.run_manual_match", side_effect=lambda args: events.append("match_manual")),
            patch("scripts.run_pipeline.run_parse", side_effect=lambda args: events.append("parse")),
            patch("scripts.run_pipeline.run_rag", side_effect=lambda args: events.append("rag")),
            patch.object(sys, "argv", ["run_pipeline.py"]),
        ):
            run_pipeline.main()

        self.assertEqual(events, ["search", "screen", "download", "parse", "rag"])

    def test_dry_run_is_passed_to_download_config(self):
        with patch("scripts.run_pipeline.download_pdfs.run") as run_download, patch.object(
            sys,
            "argv",
            ["run_pipeline.py", "--from-stage", "download", "--to-stage", "download", "--dry-run"],
        ):
            run_pipeline.main()

        config = run_download.call_args.args[0]
        self.assertTrue(config.dry_run)

    def test_parse_backend_is_passed_to_parse_stage(self):
        with patch("scripts.run_pipeline.parse_pdfs.run") as run_parse, patch.object(
            sys,
            "argv",
            ["run_pipeline.py", "--from-stage", "parse", "--to-stage", "parse", "--parse-backend", "pdftotext"],
        ):
            run_pipeline.main()

        self.assertEqual(run_parse.call_args.kwargs["backend"], "pdftotext")


if __name__ == "__main__":
    unittest.main()
