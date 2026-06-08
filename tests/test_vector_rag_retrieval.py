import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.search_rag_chunks import SearchFilters
from scripts import vector_rag_retrieval as vector_search


def chunk(
    chunk_id: str,
    text: str,
    *,
    paper_id: str = "paper-a",
    source_type: str = "reading_note",
    section: str = "Method",
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


class VectorRagRetrievalTests(unittest.TestCase):
    def test_vector_search_returns_keyword_compatible_result_shape(self):
        chunks = [chunk("chunk-a", "Bayesian uncertainty method for earthquake location.")]

        results = vector_search.vector_search_chunks(chunks, "bayesian uncertainty", limit=1)

        self.assertEqual(len(results), 1)
        self.assertIn("score", results[0])
        self.assertIn("chunk", results[0])
        self.assertEqual(results[0]["chunk"]["chunk_id"], "chunk-a")
        self.assertGreater(results[0]["score"], 0)

    def test_vector_search_ranks_matching_chunk_first(self):
        chunks = [
            chunk("chunk-a", "High-rate GNSS earthquake displacement dataset.", tags=["dataset"], chunk_index=1),
            chunk("chunk-b", "Bayesian deep learning estimates earthquake location uncertainty.", tags=["method"], chunk_index=2),
        ]

        results = vector_search.vector_search_chunks(chunks, "bayesian uncertainty earthquake", limit=2)

        self.assertEqual(results[0]["chunk"]["chunk_id"], "chunk-b")
        self.assertGreater(results[0]["score"], results[1]["score"])

    def test_vector_search_filters_by_source_type_tag_and_paper_id(self):
        chunks = [
            chunk("chunk-a", "GNSS magnitude method.", paper_id="paper-a", source_type="reading_note", tags=["method"]),
            chunk("chunk-b", "GNSS magnitude limitation.", paper_id="paper-b", source_type="synthesis", tags=["limitation"]),
        ]

        results = vector_search.vector_search_chunks(
            chunks,
            "GNSS magnitude",
            filters=SearchFilters(source_type="synthesis", tag="limitation", paper_id="paper-b"),
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["chunk"]["chunk_id"], "chunk-b")

    def test_vector_search_returns_empty_list_for_no_token_overlap(self):
        chunks = [chunk("chunk-a", "Bayesian uncertainty method.")]

        results = vector_search.vector_search_chunks(chunks, "volcano tsunami", limit=3)

        self.assertEqual(results, [])

    def test_vector_search_uses_deterministic_tie_breakers(self):
        chunks = [
            chunk("chunk-c", "GNSS magnitude method.", chunk_index=2),
            chunk("chunk-b", "GNSS magnitude method.", chunk_index=1),
            chunk("chunk-a", "GNSS magnitude method.", chunk_index=1),
        ]

        results = vector_search.vector_search_chunks(chunks, "GNSS magnitude", limit=3)

        self.assertEqual([result["chunk"]["chunk_id"] for result in results], ["chunk-a", "chunk-b", "chunk-c"])

    def test_hybrid_search_returns_keyword_compatible_result_shape(self):
        chunks = [chunk("chunk-a", "Bayesian uncertainty method for earthquake location.")]

        results = vector_search.hybrid_search_chunks(chunks, "bayesian uncertainty", limit=1)

        self.assertEqual(len(results), 1)
        self.assertIn("score", results[0])
        self.assertIn("chunk", results[0])
        self.assertEqual(results[0]["chunk"]["chunk_id"], "chunk-a")
        self.assertGreater(results[0]["score"], 0)

    def test_hybrid_search_fuses_keyword_and_vector_signals(self):
        chunks = [
            chunk("chunk-a", "Bayesian Bayesian Bayesian method.", section="Background", tags=["background"], chunk_index=1),
            chunk("chunk-b", "Bayesian uncertainty earthquake location method.", section="Method", tags=["method"], chunk_index=2),
        ]

        results = vector_search.hybrid_search_chunks(chunks, "bayesian uncertainty method", limit=2)

        self.assertEqual(results[0]["chunk"]["chunk_id"], "chunk-b")
        self.assertGreater(results[0]["score"], results[1]["score"])

    def test_hybrid_search_includes_keyword_and_vector_candidates(self):
        chunks = [
            chunk("chunk-a", "GNSS magnitude method.", tags=["method"], chunk_index=1),
            chunk("chunk-b", "High-rate displacement observations.", tags=["dataset"], chunk_index=2),
        ]

        results = vector_search.hybrid_search_chunks(chunks, "GNSS displacement", limit=2)

        self.assertEqual({result["chunk"]["chunk_id"] for result in results}, {"chunk-a", "chunk-b"})

    def test_hybrid_search_filters_by_source_type_tag_and_paper_id(self):
        chunks = [
            chunk("chunk-a", "GNSS magnitude method.", paper_id="paper-a", source_type="reading_note", tags=["method"]),
            chunk("chunk-b", "GNSS magnitude limitation.", paper_id="paper-b", source_type="synthesis", tags=["limitation"]),
        ]

        results = vector_search.hybrid_search_chunks(
            chunks,
            "GNSS magnitude",
            filters=SearchFilters(source_type="synthesis", tag="limitation", paper_id="paper-b"),
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["chunk"]["chunk_id"], "chunk-b")

    def test_hybrid_search_returns_empty_list_for_no_token_overlap(self):
        chunks = [chunk("chunk-a", "Bayesian uncertainty method.")]

        results = vector_search.hybrid_search_chunks(chunks, "volcano tsunami", limit=3)

        self.assertEqual(results, [])

    def test_hybrid_search_uses_deterministic_tie_breakers(self):
        chunks = [
            chunk("chunk-c", "GNSS magnitude method.", chunk_index=2),
            chunk("chunk-b", "GNSS magnitude method.", chunk_index=1),
            chunk("chunk-a", "GNSS magnitude method.", chunk_index=1),
        ]

        results = vector_search.hybrid_search_chunks(chunks, "GNSS magnitude", limit=3)

        self.assertEqual([result["chunk"]["chunk_id"] for result in results], ["chunk-a", "chunk-b", "chunk-c"])

    def test_cosine_similarity_handles_empty_vectors(self):
        self.assertEqual(vector_search.cosine_similarity({}, {}), 0.0)
        self.assertEqual(vector_search.cosine_similarity({"gnss": 1.0}, {}), 0.0)


if __name__ == "__main__":
    unittest.main()
