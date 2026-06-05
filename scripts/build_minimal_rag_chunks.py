#!/usr/bin/env python3
"""Build a minimal Markdown-first RAG chunk file for the literature-reading Agent.

This script intentionally keeps the first version simple:
- input: curated Markdown reading notes and synthesis documents
- output: rag/chunks.jsonl
- chunking: section-based, with light paragraph fallback for long sections

It does not build a vector database yet. The goal is to make the knowledge
base inspectable and reusable before adding Chroma/LanceDB later.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = BASE_DIR / "rag" / "chunks.jsonl"
DEFAULT_REPORT = BASE_DIR / "rag" / "minimal_rag_build_report.md"

DEFAULT_INPUTS = [
    BASE_DIR / "papers" / "notes" / "crowell_2016_cascadia_gfast_reading_note.md",
    BASE_DIR / "papers" / "notes" / "kawamoto_2016_regard_kumamoto_reading_note.md",
    BASE_DIR / "papers" / "notes" / "melgar_2019_realtime_hr_gnss_ridgecrest_reading_note.md",
    BASE_DIR / "papers" / "notes" / "2021_earthquake_magnitude_estimation_from_high_rate_gnss_data_reading_note.md",
    BASE_DIR / "papers" / "notes" / "2019_quantifying_the_value_of_real_time_geodetic_constraints_reading_note.md",
    BASE_DIR / "papers" / "notes" / "2020_bayesian_deep_learning_estimation_of_earthquake_location_from_reading_note.md",
    BASE_DIR / "synthesis" / "三篇实时GNSS地震预警论文综合.md",
    BASE_DIR / "synthesis" / "HR-GNSS大震快速震源表征研究主线综述.md",
]

PAPER_ID_BY_FILENAME = {
    "crowell_2016_cascadia_gfast_reading_note.md": "crowell_2016_cascadia_gfast",
    "kawamoto_2016_regard_kumamoto_reading_note.md": "kawamoto_2016_regard_kumamoto",
    "melgar_2019_realtime_hr_gnss_ridgecrest_reading_note.md": "melgar_2019_realtime_hr_gnss_ridgecrest",
    "2021_earthquake_magnitude_estimation_from_high_rate_gnss_data_reading_note.md": "2021_earthquake_magnitude_estimation_from_high_rate_gnss_data",
    "2019_quantifying_the_value_of_real_time_geodetic_constraints_reading_note.md": "2019_quantifying_the_value_of_real_time_geodetic_constraints",
    "2020_bayesian_deep_learning_estimation_of_earthquake_location_from_reading_note.md": "2020_bayesian_deep_learning_estimation_of_earthquake_location_from",
    "三篇实时GNSS地震预警论文综合.md": "three_paper_realtime_gnss_synthesis",
    "HR-GNSS大震快速震源表征研究主线综述.md": "hr_gnss_rapid_source_characterization_synthesis",
}

SOURCE_TYPE_BY_FILENAME = {
    "crowell_2016_cascadia_gfast_reading_note.md": "reading_note",
    "kawamoto_2016_regard_kumamoto_reading_note.md": "reading_note",
    "melgar_2019_realtime_hr_gnss_ridgecrest_reading_note.md": "reading_note",
    "2021_earthquake_magnitude_estimation_from_high_rate_gnss_data_reading_note.md": "reading_note",
    "2019_quantifying_the_value_of_real_time_geodetic_constraints_reading_note.md": "reading_note",
    "2020_bayesian_deep_learning_estimation_of_earthquake_location_from_reading_note.md": "reading_note",
    "三篇实时GNSS地震预警论文综合.md": "synthesis",
    "HR-GNSS大震快速震源表征研究主线综述.md": "synthesis",
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
MAX_CHARS = 3500
MIN_CHARS = 80


@dataclass
class Section:
    heading: str
    level: int
    text: str


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[`*_｜|:：/\\]+", "-", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-") or "section"


def stable_hash(text: str, length: int = 12) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:length]


def parse_sections(markdown: str) -> list[Section]:
    sections: list[Section] = []
    current_heading = "document"
    current_level = 0
    current_lines: list[str] = []

    for line in markdown.splitlines():
        match = HEADING_RE.match(line)
        if match:
            if current_lines:
                sections.append(
                    Section(
                        heading=current_heading,
                        level=current_level,
                        text="\n".join(current_lines).strip(),
                    )
                )
            current_level = len(match.group(1))
            current_heading = match.group(2).strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append(
            Section(
                heading=current_heading,
                level=current_level,
                text="\n".join(current_lines).strip(),
            )
        )

    return [section for section in sections if len(section.text.strip()) >= MIN_CHARS]


def split_long_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    paragraphs = re.split(r"\n\s*\n", text)
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if len(paragraph) > max_chars:
            if current:
                chunks.append("\n\n".join(current))
                current = []
                current_len = 0
            for start in range(0, len(paragraph), max_chars):
                chunks.append(paragraph[start : start + max_chars])
            continue

        projected = current_len + len(paragraph) + 2
        if current and projected > max_chars:
            chunks.append("\n\n".join(current))
            current = [paragraph]
            current_len = len(paragraph)
        else:
            current.append(paragraph)
            current_len = projected

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def infer_title(markdown: str, path: Path) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def display_path(path: Path) -> str:
    try:
        return path.relative_to(BASE_DIR).as_posix()
    except ValueError:
        return str(path)


def infer_tags(section_heading: str, text: str) -> list[str]:
    normalized = f"{section_heading}\n{text}".lower()
    tag_rules = [
        ("method", ["method", "方法", "model", "algorithm", "模型", "算法"]),
        ("dataset", ["data", "dataset", "数据", "benchmark"]),
        ("metric", ["metric", "evaluation", "评价", "评估", "指标"]),
        ("result", ["result", "key result", "结果", "发现"]),
        ("limitation", ["limitation", "局限", "不足", "challenge"]),
        ("relation_to_my_research", ["relation to my research", "my research", "我的研究"]),
        ("citation_candidate", ["citation", "quotable", "引用", "可引用"]),
        ("future_work", ["open question", "future", "todo", "下一步", "问题"]),
        ("background", ["background", "motivation", "背景", "动机"]),
    ]

    tags = []
    for tag, keywords in tag_rules:
        if any(keyword in normalized for keyword in keywords):
            tags.append(tag)
    return tags or ["general"]


def build_chunks(paths: Iterable[Path]) -> list[dict[str, object]]:
    chunks: list[dict[str, object]] = []

    for path in paths:
        markdown = path.read_text(encoding="utf-8")
        title = infer_title(markdown, path)
        paper_id = PAPER_ID_BY_FILENAME.get(path.name, path.stem)
        source_type = SOURCE_TYPE_BY_FILENAME.get(path.name, "markdown")
        relative_path = display_path(path)

        for section_index, section in enumerate(parse_sections(markdown), start=1):
            parts = split_long_text(section.text)
            for part_index, part in enumerate(parts, start=1):
                chunk_seed = f"{paper_id}|{section.heading}|{section_index}|{part_index}|{part}"
                chunk_id = f"{paper_id}__{section_index:02d}_{part_index:02d}_{stable_hash(chunk_seed)}"
                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "paper_id": paper_id,
                        "title": title,
                        "source_file": relative_path,
                        "source_type": source_type,
                        "section": section.heading,
                        "section_level": section.level,
                        "tags": infer_tags(section.heading, part),
                        "chunk_index": len(chunks) + 1,
                        "section_index": section_index,
                        "part_index": part_index,
                        "char_count": len(part),
                        "text": part,
                    }
                )

    return chunks


def write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_report(path: Path, chunks: list[dict[str, object]], output_path: Path) -> None:
    by_source: dict[str, list[dict[str, object]]] = {}
    for chunk in chunks:
        by_source.setdefault(str(chunk["source_file"]), []).append(chunk)

    lines = [
        "# 最小 RAG chunk 构建报告",
        "",
        "> 该文件由 `scripts/build_minimal_rag_chunks.py` 生成，用于记录第一版 Markdown-first RAG 数据是否构建成功。",
        "",
        "---",
        "",
        "## 1. 输出文件",
        "",
        f"- Chunk JSONL: `{output_path.relative_to(BASE_DIR).as_posix()}`",
        f"- Chunk 数量：{len(chunks)}",
        "",
        "---",
        "",
        "## 2. 输入来源",
        "",
        "| Source file | Source type | Chunks |",
        "|---|---:|---:|",
    ]

    for source_file, source_chunks in by_source.items():
        source_type = source_chunks[0]["source_type"]
        lines.append(f"| `{source_file}` | {source_type} | {len(source_chunks)} |")

    lines.extend(
        [
            "",
            "---",
            "",
            "## 3. 当前 chunk schema",
            "",
            "```json",
            json.dumps(
                {
                    "chunk_id": "stable id from paper_id + section + content hash",
                    "paper_id": "paper or synthesis identifier",
                    "title": "document title",
                    "source_file": "relative markdown path",
                    "source_type": "reading_note / synthesis / markdown",
                    "section": "markdown heading",
                    "section_level": "heading level",
                    "tags": "deterministic section/content tags such as method, dataset, metric, result, limitation",
                    "chunk_index": "global order in chunks.jsonl",
                    "section_index": "order within source document",
                    "part_index": "split index if section is long",
                    "char_count": "text length",
                    "text": "chunk text",
                },
                ensure_ascii=False,
                indent=2,
            ),
            "```",
            "",
            "---",
            "",
            "## 4. 设计说明",
            "",
            "- 当前版本按 Markdown heading 切分，优先保留阅读卡片和 synthesis 的语义结构；",
            "- 暂不构建向量库，先生成可检查、可追溯的 JSONL；",
            "- 每个 chunk 保留 `paper_id`、`source_file`、`section`，方便后续引用回原文；",
            "- 每个 chunk 基于 section heading 和正文内容附加确定性 `tags`，便于按 method / dataset / result / limitation 等类型筛选；",
            "- 长 section 会按段落进一步切分，避免单个 chunk 过长；",
            "- 后续可以在此基础上接 Chroma/LanceDB 和 embedding model。",
            "",
            "---",
            "",
            "## 5. 下一步",
            "",
            "1. 为 chunk 增加更细的 tags，例如 method / metric / limitation / dataset；",
            "2. 接入 embedding，生成向量索引；",
            "3. 写一个简单检索脚本，支持按关键词或向量查询；",
            "4. 在生成综述时要求回答必须引用 `chunk_id` 和 `source_file`。",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    input_paths: list[Path] | None = None,
    output_path: Path = DEFAULT_OUTPUT,
    report_path: Path = DEFAULT_REPORT,
) -> list[dict[str, object]]:
    raw_input_paths = input_paths if input_paths is not None else DEFAULT_INPUTS
    resolved_inputs = [path if path.is_absolute() else BASE_DIR / path for path in raw_input_paths]
    missing = [path for path in resolved_inputs if not path.exists()]
    if missing:
        missing_list = "\n".join(str(path) for path in missing)
        raise SystemExit(f"Missing input files:\n{missing_list}")

    chunks = build_chunks(resolved_inputs)
    resolved_output = output_path if output_path.is_absolute() else BASE_DIR / output_path
    resolved_report = report_path if report_path.is_absolute() else BASE_DIR / report_path
    write_jsonl(resolved_output, chunks)
    write_report(resolved_report, chunks, resolved_output)
    print(f"Wrote {len(chunks)} chunks to {resolved_output}")
    print(f"Wrote report to {resolved_report}")
    return chunks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build minimal RAG chunks from curated Markdown notes.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output JSONL path. Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT,
        help=f"Report Markdown path. Default: {DEFAULT_REPORT}",
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        default=DEFAULT_INPUTS,
        help="Markdown files to chunk. Defaults to curated reading notes and synthesis documents.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(
        input_paths=args.inputs,
        output_path=args.output,
        report_path=args.report,
    )


if __name__ == "__main__":
    main()
