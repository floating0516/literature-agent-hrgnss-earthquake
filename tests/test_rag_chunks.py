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


class RagChunkSearchTests(unittest.TestCase):
    def test_keyword_search_returns_ranked_matching_chunk_with_metadata(self):
        from scripts.search_rag_chunks import search_chunks

        chunks = [
            {
                "chunk_id": "chunk-a",
                "source_file": "papers/notes/a.md",
                "source_type": "reading_note",
                "section": "Method",
                "text": "Bayesian deep learning estimates earthquake location uncertainty.",
            },
            {
                "chunk_id": "chunk-b",
                "source_file": "papers/notes/b.md",
                "source_type": "reading_note",
                "section": "Data",
                "text": "High-rate GNSS captures permanent displacement.",
            },
        ]

        results = search_chunks(chunks, "bayesian uncertainty")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["chunk"]["chunk_id"], "chunk-a")
        self.assertGreater(results[0]["score"], 0)

    def test_cli_search_prints_chunk_id_source_and_excerpt(self):
        with tempfile.TemporaryDirectory() as tmp:
            chunks_path = Path(tmp) / "chunks.jsonl"
            chunks_path.write_text(
                json.dumps(
                    {
                        "chunk_id": "chunk-a",
                        "source_file": "papers/notes/a.md",
                        "source_type": "reading_note",
                        "section": "Method",
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
                ],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("chunk-a", result.stdout)
        self.assertIn("papers/notes/a.md", result.stdout)
        self.assertIn("Bayesian deep learning", result.stdout)


if __name__ == "__main__":
    unittest.main()
