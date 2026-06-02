#!/usr/bin/env python3
"""Rule-based coarse screening for OpenAlex candidate papers.

This is a lightweight first-pass screener that mimics the intent of the
paper_screening_prompt template without calling an LLM yet. It is designed to
remove obvious noise before deeper prompt-based or human screening.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = BASE_DIR / "papers" / "candidates.jsonl"
DEFAULT_OUTPUT = BASE_DIR / "papers" / "screened_candidates.jsonl"
DEFAULT_SELECTED = BASE_DIR / "papers" / "selected_papers.jsonl"
DEFAULT_REPORT = BASE_DIR / "papers" / "screening_results.md"
DEFAULT_COMPARISON = BASE_DIR / "papers" / "screening_comparison.md"

STRONG_POSITIVE = [
    "high-rate gnss",
    "high rate gnss",
    "real-time gnss",
    "real time gnss",
    "geodetic earthquake early warning",
    "gnss seismology",
    "g-fast",
    "g fast",
    "regard",
    "coseismic displacement",
    "coseismic displacements",
    "earthquake early warning",
    "earthquake magnitude estimation",
    "earthquake source",
    "finite fault",
    "slip characterization",
    "gnss displacement",
    "gnss displacements",
    "seismogeodetic",
    "tsunami forecasting",
    "peak ground velocities",
    "seismic waves",
]

DEEP_LEARNING_POSITIVE = [
    "deep learning",
    "machine learning",
    "neural network",
    "neural networks",
    "convolutional neural network",
    "cnn",
    "lstm",
    "transformer",
    "graph neural network",
    "gnn",
    "artificial intelligence",
    "ai-based",
]

SOURCE_CHARACTERIZATION_POSITIVE = [
    "source characterization",
    "source characterisation",
    "source inversion",
    "finite fault inversion",
    "rapid source",
    "rupture extent",
    "rupture directivity",
    "fault slip",
    "slip distribution",
    "moment tensor",
    "focal mechanism",
]

MODERATE_POSITIVE = [
    "gnss",
    "gps",
    "earthquake",
    "seismic",
    "seismology",
    "source determination",
    "source models",
    "warning",
    "magnitude",
    "displacement",
    "rupture",
    "slip",
    "tsunami",
    "ppp",
]

NOISE = [
    "structural health monitoring",
    "bridge structural health",
    "bridge",
    "uav",
    "fully autonomous uavs",
    "deflection",
    "cloud computing",
    "ionospheric",
    "kinematic monitoring applications",
    "low-cost gnss",
    "tectonic inheritance",
    "seismic anisotropy",
    "tsunami risk communication",
    "early warning systems’ challenges",
    "machine vision",
]

HIGH_VALUE_METHODS = [
    "g-fast",
    "regard",
    "shakealert",
    "finder",
    "g-larms",
    "befores",
    "fastlane",
    "rtklib",
]

CATEGORY_RULES = {
    "gnss_geodetic_eew": [
        "high-rate gnss",
        "real-time gnss",
        "geodetic earthquake early warning",
        "gnss seismology",
        "g-fast",
        "regard",
        "gnss displacement",
        "gps seismology",
    ],
    "seismogeodesy_fusion": [
        "seismogeodetic",
        "accelerometer",
        "strong motion",
        "gps and accelerometer",
        "gnss and accelerometer",
        "seismic and geodetic",
    ],
    "finite_fault_source_inversion": [
        "finite fault",
        "source inversion",
        "source characterization",
        "source characterisation",
        "rupture extent",
        "fault slip",
        "slip distribution",
        "moment tensor",
    ],
    "deep_learning_eew": [
        "deep learning",
        "machine learning",
        "neural network",
        "earthquake early warning",
        "magnitude estimation",
    ],
    "deep_learning_source_characterization": [
        "deep learning",
        "machine learning",
        "neural network",
        "source characterization",
        "source inversion",
        "finite fault inversion",
        "rupture",
    ],
    "tsunami_large_earthquake": [
        "tsunami",
        "great earthquake",
        "subduction",
        "near-field tsunami",
        "mw 8",
        "mw 9",
    ],
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def record_text(record: dict[str, Any]) -> str:
    # Do not include search_query here. Query text contains target terms such as
    # "G-FAST" or "earthquake early warning" and would falsely boost off-topic
    # papers that only appeared because of broad search matching.
    fields = [
        record.get("title") or "",
        record.get("abstract") or "",
        record.get("venue") or "",
    ]
    return "\n".join(fields).lower()


def classify_record(text: str) -> list[str]:
    categories = []
    for category, terms in CATEGORY_RULES.items():
        matched = [term for term in terms if term in text]
        if category.startswith("deep_learning"):
            has_ml = any(term in text for term in DEEP_LEARNING_POSITIVE)
            has_earthquake_context = any(term in text for term in ["earthquake", "seismic", "magnitude", "early warning", "rupture", "source"])
            if has_ml and has_earthquake_context and matched:
                categories.append(category)
        elif matched:
            categories.append(category)
    return categories or ["other"]


def score_record(record: dict[str, Any]) -> dict[str, Any]:
    text = record_text(record)
    title = (record.get("title") or "").lower()

    matched_strong = [term for term in STRONG_POSITIVE if term in text]
    matched_moderate = [term for term in MODERATE_POSITIVE if term in text]
    matched_noise = [term for term in NOISE if term in text]
    matched_methods = [term for term in HIGH_VALUE_METHODS if term in text]
    matched_deep_learning = [term for term in DEEP_LEARNING_POSITIVE if term in text]
    matched_source_terms = [term for term in SOURCE_CHARACTERIZATION_POSITIVE if term in text]
    categories = classify_record(text)

    score = 0
    score += 2 * len(matched_strong)
    score += min(4, len(matched_moderate))
    score += 2 * len(matched_methods)
    score += 2 * min(3, len(matched_deep_learning))
    score += 2 * min(3, len(matched_source_terms))
    score += min(3, (record.get("cited_by_count") or 0) // 50)
    score -= 3 * len(matched_noise)

    # Guardrails: title-only obvious off-topic papers should be filtered even if
    # they contain generic GNSS/early warning terms.
    if any(term in title for term in ["uav", "bridge", "structural health", "cloud computing"]):
        score -= 6

    if "earthquake" in text and ("gnss" in text or "gps" in text or "geodetic" in text):
        score += 3

    if matched_deep_learning and any(term in text for term in ["earthquake", "seismic", "magnitude", "early warning", "rupture", "source"]):
        score += 3

    if matched_source_terms and any(term in text for term in ["earthquake", "seismic", "gnss", "gps", "geodetic"]):
        score += 2

    if score >= 8:
        decision = "keep"
        priority = "high"
        next_action = "read_full_text"
    elif score >= 4:
        decision = "maybe"
        priority = "medium"
        next_action = "read_abstract_or_methods_first"
    else:
        decision = "discard"
        priority = "low"
        next_action = "keep_metadata_only"

    if matched_noise and decision == "keep" and not matched_methods and not matched_deep_learning:
        decision = "maybe"
        priority = "medium"
        next_action = "manual_check_needed"

    reasons = []
    if matched_strong:
        reasons.append("matched strong topic terms: " + ", ".join(matched_strong[:6]))
    if matched_deep_learning:
        reasons.append("matched deep-learning terms: " + ", ".join(matched_deep_learning[:6]))
    if matched_source_terms:
        reasons.append("matched source-characterization terms: " + ", ".join(matched_source_terms[:6]))
    if matched_methods:
        reasons.append("matched high-value system/method terms: " + ", ".join(matched_methods))
    if matched_noise:
        reasons.append("possible noise terms: " + ", ".join(matched_noise[:5]))
    if not reasons:
        reasons.append("weak or generic match to current topic")

    return {
        "relevance_score": max(1, min(5, round(score / 3))),
        "raw_score": score,
        "reading_priority": priority,
        "decision": decision,
        "reason": "; ".join(reasons),
        "matched_strong_terms": matched_strong,
        "matched_moderate_terms": matched_moderate,
        "matched_deep_learning_terms": matched_deep_learning,
        "matched_source_characterization_terms": matched_source_terms,
        "matched_noise_terms": matched_noise,
        "categories": categories,
        "next_action": next_action,
    }


def screen(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    screened = []
    for record in records:
        enriched = dict(record)
        enriched["screening"] = score_record(record)
        screened.append(enriched)
    return sorted(
        screened,
        key=lambda item: (
            item["screening"]["decision"] != "keep",
            -(item["screening"]["raw_score"]),
            -(item.get("cited_by_count") or 0),
        ),
    )


def markdown_escape(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def write_report(path: Path, screened: list[dict[str, Any]]) -> None:
    counts = {decision: sum(1 for r in screened if r["screening"]["decision"] == decision) for decision in ["keep", "maybe", "discard"]}
    lines = [
        "# 候选论文粗筛结果",
        "",
        "> 该文件由 `scripts/screen_candidates.py` 生成。当前为规则型粗筛，用于在正式 LLM 精筛前过滤明显噪声。",
        "",
        "## 总览",
        "",
        f"- 输入候选论文：{len(screened)}",
        f"- Keep：{counts['keep']}",
        f"- Maybe：{counts['maybe']}",
        f"- Discard：{counts['discard']}",
        "",
    ]

    for decision in ["keep", "maybe", "discard"]:
        lines.extend([
            f"## {decision.upper()}",
            "",
            "| # | Score | Categories | Year | Cited | Title | DOI | Fulltext | Reason |",
            "|---:|---:|---|---:|---:|---|---|---|---|",
        ])
        items = [r for r in screened if r["screening"]["decision"] == decision]
        for index, record in enumerate(items, 1):
            s = record["screening"]
            categories = ", ".join(s.get("categories", []))
            lines.append(
                f"| {index} | {s['relevance_score']} | {markdown_escape(categories)} | {record.get('year') or ''} | {record.get('cited_by_count') or 0} | "
                f"{markdown_escape(record.get('title'))} | {markdown_escape(record.get('doi'))} | "
                f"{record.get('fulltext_status')} | {markdown_escape(s['reason'])} |"
            )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def write_comparison(path: Path, records: list[dict[str, Any]], screened: list[dict[str, Any]]) -> None:
    noise_examples = [r for r in screened if r["screening"].get("matched_noise_terms")]
    kept = [r for r in screened if r["screening"]["decision"] == "keep"]
    discarded = [r for r in screened if r["screening"]["decision"] == "discard"]
    maybe = [r for r in screened if r["screening"]["decision"] == "maybe"]

    lines = [
        "# 筛选前后结果对比",
        "",
        "> 目的：比较 OpenAlex 原始候选结果和粗筛后的结果，观察结构健康监测、UAV、桥梁监测等噪声是否被过滤。",
        "",
        "## 1. 筛选前",
        "",
        f"OpenAlex 原始去重候选数量：{len(records)}。由于 query 中包含 `GNSS`、`early warning` 等通用词，原始结果中混入了一些噪声，例如结构健康监测、UAV、桥梁监测、云计算 early warning、普通 GNSS 动态监测等。",
        "",
        "## 2. 筛选后",
        "",
        f"- Keep：{len(kept)}",
        f"- Maybe：{len(maybe)}",
        f"- Discard：{len(discarded)}",
        "",
        "Keep 结果主要集中在 HR-GNSS、real-time GNSS、G-FAST、geodetic earthquake early warning、GNSS seismology、coseismic displacement、ShakeAlert/REGARD/FinDerS 等方向。",
        "",
        "## 3. 噪声过滤示例",
        "",
        "| Title | Noise terms | Decision | Reason |",
        "|---|---|---|---|",
    ]

    for record in noise_examples[:12]:
        s = record["screening"]
        lines.append(
            f"| {markdown_escape(record.get('title'))} | {', '.join(s['matched_noise_terms'])} | "
            f"{s['decision']} | {markdown_escape(s['reason'])} |"
        )

    lines.extend([
        "",
        "## 4. 保留结果示例",
        "",
        "| Title | Categories | Strong / DL / Source terms | Decision | Fulltext |",
        "|---|---|---|---|---|",
    ])

    for record in kept[:15]:
        s = record["screening"]
        terms = s.get("matched_strong_terms", [])[:4] + s.get("matched_deep_learning_terms", [])[:4] + s.get("matched_source_characterization_terms", [])[:4]
        lines.append(
            f"| {markdown_escape(record.get('title'))} | {markdown_escape(', '.join(s.get('categories', [])))} | {markdown_escape(', '.join(terms))} | "
            f"{s['decision']} | {record.get('fulltext_status')} |"
        )

    lines.extend([
        "",
        "## 5. 结论",
        "",
        "粗筛后，明显偏离地震学/GNSS 地震预警主题的结果被降级为 maybe 或 discard。保留结果的主题集中度明显高于 OpenAlex 原始结果。",
        "",
        "当前脚本是规则型粗筛，不替代后续 LLM 精筛和人工判断。下一步可以对 Keep 和 Maybe 论文运行 `paper_screening_prompt.md`，进一步判断是否进入全文阅读。",
    ])

    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coarse-screen candidate papers.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--selected", type=Path, default=DEFAULT_SELECTED)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--comparison", type=Path, default=DEFAULT_COMPARISON)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = load_jsonl(args.input)
    screened = screen(records)
    selected = [r for r in screened if r["screening"]["decision"] in {"keep", "maybe"}]

    write_jsonl(args.output, screened)
    write_jsonl(args.selected, selected)
    write_report(args.report, screened)
    write_comparison(args.comparison, records, screened)

    counts = {decision: sum(1 for r in screened if r["screening"]["decision"] == decision) for decision in ["keep", "maybe", "discard"]}
    print(f"Screened {len(screened)} records: keep={counts['keep']}, maybe={counts['maybe']}, discard={counts['discard']}")
    print(f"Saved screened records to {args.output}")
    print(f"Saved selected records to {args.selected}")
    print(f"Saved report to {args.report}")
    print(f"Saved comparison to {args.comparison}")


if __name__ == "__main__":
    main()
