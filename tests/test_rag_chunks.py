import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import build_minimal_rag_chunks as rag_builder


class RagChunkBuilderTests(unittest.TestCase):
    def test_default_inputs_include_all_curated_reading_notes_and_syntheses(self):
        default_names = [path.name for path in rag_builder.DEFAULT_INPUTS]

        self.assertIn("2021_earthquake_magnitude_estimation_from_high_rate_gnss_data_reading_note.md", default_names)
        self.assertIn("2019_quantifying_the_value_of_real_time_geodetic_constraints_reading_note.md", default_names)
        self.assertIn("2020_bayesian_deep_learning_estimation_of_earthquake_location_from_reading_note.md", default_names)
        self.assertIn("HR-GNSS大震快速震源表征研究主线综述.md", default_names)

    def test_new_curated_files_have_specific_source_types(self):
        self.assertEqual(
            rag_builder.SOURCE_TYPE_BY_FILENAME[
                "2021_earthquake_magnitude_estimation_from_high_rate_gnss_data_reading_note.md"
            ],
            "reading_note",
        )
        self.assertEqual(
            rag_builder.SOURCE_TYPE_BY_FILENAME[
                "2019_quantifying_the_value_of_real_time_geodetic_constraints_reading_note.md"
            ],
            "reading_note",
        )
        self.assertEqual(
            rag_builder.SOURCE_TYPE_BY_FILENAME[
                "2020_bayesian_deep_learning_estimation_of_earthquake_location_from_reading_note.md"
            ],
            "reading_note",
        )
        self.assertEqual(
            rag_builder.SOURCE_TYPE_BY_FILENAME["HR-GNSS大震快速震源表征研究主线综述.md"],
            "synthesis",
        )

    def test_infer_tags_from_reading_note_sections(self):
        self.assertEqual(rag_builder.infer_tags("6. Method", ""), ["method"])
        self.assertEqual(rag_builder.infer_tags("5. Data", ""), ["dataset"])
        self.assertEqual(rag_builder.infer_tags("7. Evaluation metrics", ""), ["metric"])
        self.assertEqual(rag_builder.infer_tags("8. Key results", ""), ["result"])
        self.assertEqual(rag_builder.infer_tags("10. Limitations", ""), ["limitation"])
        self.assertEqual(rag_builder.infer_tags("11. Relation to my research", ""), ["relation_to_my_research"])
        self.assertEqual(rag_builder.infer_tags("12. Useful citations or quotable ideas", ""), ["citation_candidate"])
        self.assertEqual(rag_builder.infer_tags("13. Open questions", ""), ["future_work"])

    def test_build_chunks_adds_tags_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            note_path = Path(tmp) / "note.md"
            note_path.write_text(
                "# Test Note\n\n"
                "## 6. Method\n\n"
                "Bayesian deep learning method details for earthquake location and uncertainty.\n",
                encoding="utf-8",
            )

            chunks = rag_builder.build_chunks([note_path])

        self.assertEqual(chunks[0]["tags"], ["method"])

    def test_cli_exposes_parse_quality_filter_options(self):
        result = subprocess.run(
            [sys.executable, "scripts/build_minimal_rag_chunks.py", "--help"],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--quality-path", result.stdout)
        self.assertIn("--exclude-low-quality", result.stdout)
        self.assertIn("--min-quality-score", result.stdout)

    def test_cli_skips_low_quality_markdown_when_filter_options_are_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            good_path = tmp_path / "good.md"
            bad_path = tmp_path / "bad.md"
            output_path = tmp_path / "chunks.jsonl"
            report_path = tmp_path / "report.md"
            quality_path = tmp_path / "quality.jsonl"
            good_path.write_text(
                "# Good\n\n## Method\n\n"
                "Readable GNSS method text for chunking and retrieval. "
                "This paragraph is long enough to pass the minimal chunk length threshold and represent a useful parsed Markdown section.",
                encoding="utf-8",
            )
            bad_path.write_text("# Bad\n\n## Body\n\nLow quality parsed text that should be skipped.", encoding="utf-8")
            quality_records = [
                {"source_file": str(good_path), "status": "pass", "score": 90, "reasons": []},
                {"source_file": str(bad_path), "status": "fail", "score": 20, "reasons": ["document body is too short"]},
            ]
            quality_path.write_text("\n".join(json.dumps(record) for record in quality_records) + "\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_minimal_rag_chunks.py",
                    "--output",
                    str(output_path),
                    "--report",
                    str(report_path),
                    "--quality-path",
                    str(quality_path),
                    "--exclude-low-quality",
                    "--min-quality-score",
                    "60",
                    str(good_path),
                    str(bad_path),
                ],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            records = [json.loads(line) for line in output_path.read_text(encoding="utf-8").splitlines()]
            self.assertTrue(records)
            self.assertTrue(all(record["source_file"] != str(bad_path) for record in records))
            self.assertIn("质量过滤", report_path.read_text(encoding="utf-8"))

    def test_run_skips_low_quality_markdown_when_filter_is_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            good_path = tmp_path / "good.md"
            bad_path = tmp_path / "bad.md"
            output_path = tmp_path / "chunks.jsonl"
            report_path = tmp_path / "report.md"
            quality_path = tmp_path / "quality.jsonl"
            good_path.write_text(
                "# Good\n\n## Method\n\n"
                "Readable GNSS method text for chunking and retrieval. "
                "This paragraph is long enough to pass the minimal chunk length threshold and represent a useful parsed Markdown section.",
                encoding="utf-8",
            )
            bad_path.write_text("# Bad\n\n## Body\n\nLow quality parsed text that should be skipped.", encoding="utf-8")
            quality_records = [
                {"source_file": str(good_path), "status": "pass", "score": 90, "reasons": []},
                {"source_file": str(bad_path), "status": "fail", "score": 20, "reasons": ["document body is too short"]},
            ]
            quality_path.write_text("\n".join(json.dumps(record) for record in quality_records) + "\n", encoding="utf-8")

            chunks = rag_builder.run(
                input_paths=[good_path, bad_path],
                output_path=output_path,
                report_path=report_path,
                quality_path=quality_path,
                exclude_low_quality=True,
                min_quality_score=60,
            )

            self.assertTrue(chunks)
            self.assertTrue(all(chunk["source_file"] != str(bad_path) for chunk in chunks))
            report_text = report_path.read_text(encoding="utf-8")
            self.assertIn("质量过滤", report_text)
            self.assertIn("bad.md", report_text)


class RagChunkSearchTests(unittest.TestCase):
    def test_keyword_search_returns_ranked_matching_chunk_with_metadata(self):
        from scripts.search_rag_chunks import search_chunks

        chunks = [
            {
                "chunk_id": "chunk-a",
                "paper_id": "paper-a",
                "source_file": "papers/notes/a.md",
                "source_type": "reading_note",
                "section": "Method",
                "tags": ["method"],
                "text": "Bayesian deep learning estimates earthquake location uncertainty.",
            },
            {
                "chunk_id": "chunk-b",
                "paper_id": "paper-b",
                "source_file": "papers/notes/b.md",
                "source_type": "reading_note",
                "section": "Data",
                "tags": ["dataset"],
                "text": "High-rate GNSS captures permanent displacement.",
            },
        ]

        results = search_chunks(chunks, "bayesian uncertainty")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["chunk"]["chunk_id"], "chunk-a")
        self.assertGreater(results[0]["score"], 0)

    def test_keyword_search_filters_by_source_type_tag_and_paper_id(self):
        from scripts.search_rag_chunks import SearchFilters, search_chunks

        chunks = [
            {
                "chunk_id": "chunk-a",
                "paper_id": "paper-a",
                "source_file": "papers/notes/a.md",
                "source_type": "reading_note",
                "section": "Method",
                "tags": ["method"],
                "text": "GNSS magnitude method.",
            },
            {
                "chunk_id": "chunk-b",
                "paper_id": "paper-b",
                "source_file": "synthesis/b.md",
                "source_type": "synthesis",
                "section": "Limitations",
                "tags": ["limitation"],
                "text": "GNSS magnitude limitation.",
            },
        ]

        results = search_chunks(
            chunks,
            "GNSS magnitude",
            filters=SearchFilters(source_type="synthesis", tag="limitation", paper_id="paper-b"),
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["chunk"]["chunk_id"], "chunk-b")

    def test_cli_search_prints_chunk_id_source_and_excerpt(self):
        with tempfile.TemporaryDirectory() as tmp:
            chunks_path = Path(tmp) / "chunks.jsonl"
            chunks_path.write_text(
                json.dumps(
                    {
                        "chunk_id": "chunk-a",
                        "paper_id": "paper-a",
                        "source_file": "papers/notes/a.md",
                        "source_type": "reading_note",
                        "section": "Method",
                        "tags": ["method"],
                        "text": "Bayesian deep learning estimates earthquake location uncertainty.",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/search_rag_chunks.py",
                    "bayesian uncertainty",
                    "--chunks",
                    str(chunks_path),
                    "--limit",
                    "1",
                    "--source-type",
                    "reading_note",
                    "--tag",
                    "method",
                    "--paper-id",
                    "paper-a",
                ],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("chunk-a", result.stdout)
        self.assertIn("papers/notes/a.md", result.stdout)
        self.assertIn("tags: method", result.stdout)
        self.assertIn("Bayesian deep learning", result.stdout)

    def test_cli_search_json_output_returns_machine_readable_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            chunks_path = Path(tmp) / "chunks.jsonl"
            chunks_path.write_text(
                json.dumps(
                    {
                        "chunk_id": "chunk-a",
                        "paper_id": "paper-a",
                        "source_file": "papers/notes/a.md",
                        "source_type": "reading_note",
                        "section": "Method",
                        "tags": ["method"],
                        "text": "Bayesian deep learning estimates earthquake location uncertainty.",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/search_rag_chunks.py",
                    "bayesian uncertainty",
                    "--chunks",
                    str(chunks_path),
                    "--json",
                ],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload[0]["chunk"]["chunk_id"], "chunk-a")
        self.assertEqual(payload[0]["chunk"]["tags"], ["method"])


if __name__ == "__main__":
    unittest.main()
