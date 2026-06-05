#!/usr/bin/env python3
"""Parse downloaded PDFs into lightweight Markdown text files.

Uses the local `pdftotext` command when available. The output is not meant to
preserve final publication layout perfectly; it is an intermediate text format
for paper-reading prompts and later RAG chunking.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = BASE_DIR / "papers" / "raw_pdf"
DEFAULT_OUTPUT_DIR = BASE_DIR / "papers" / "parsed_md"
DEFAULT_LOG = BASE_DIR / "papers" / "pdf_parse_log.md"


def markdown_header(pdf_path: Path, parser: str) -> str:
    title = pdf_path.stem.replace("_", " ").title()
    return (
        f"# {title}\n\n"
        f"> Source PDF: `papers/raw_pdf/{pdf_path.name}`\n"
        f"> Parser: `{parser}`\n\n"
        "---\n\n"
    )


def parse_with_pdftotext(pdf_path: Path, output_dir: Path) -> tuple[Path, str | None]:
    text_path = output_dir / f"{pdf_path.stem}.txt"
    md_path = output_dir / f"{pdf_path.stem}.md"

    try:
        subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf_path), str(text_path)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        return md_path, (exc.stderr or exc.stdout or str(exc)).strip()
    except FileNotFoundError as exc:
        return md_path, str(exc).strip()

    try:
        text = text_path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError as exc:
        return md_path, str(exc).strip()
    text_path.unlink(missing_ok=True)

    md = markdown_header(pdf_path, "pdftotext -layout -enc UTF-8") + "```text\n" + f"{text.strip()}\n" + "```\n"
    md_path.write_text(md, encoding="utf-8")
    return md_path, None


def parse_with_pymupdf4llm(pdf_path: Path, output_dir: Path) -> tuple[Path, str | None]:
    md_path = output_dir / f"{pdf_path.stem}.md"
    try:
        import pymupdf4llm
    except ImportError as exc:
        return md_path, f"pymupdf4llm is not installed: {exc}"

    try:
        markdown = pymupdf4llm.to_markdown(str(pdf_path))
    except Exception as exc:
        return md_path, str(exc).strip()

    md = markdown_header(pdf_path, "pymupdf4llm") + f"{markdown.strip()}\n"
    md_path.write_text(md, encoding="utf-8")
    return md_path, None


def parse_pdf(pdf_path: Path, output_dir: Path, backend: str = "pymupdf4llm") -> tuple[Path, str | None]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if backend == "pdftotext":
        return parse_with_pdftotext(pdf_path, output_dir)
    if backend == "pymupdf4llm":
        return parse_with_pymupdf4llm(pdf_path, output_dir)
    return output_dir / f"{pdf_path.stem}.md", f"Unknown PDF parse backend: {backend}"


def write_log(log_path: Path, results: list[tuple[Path, Path, str | None]], backend: str = "pymupdf4llm") -> None:
    lines = [
        "# PDF 解析记录",
        "",
        f"> 该文件由 `scripts/parse_pdfs.py` 生成。当前使用 `{backend}` 做轻量解析。",
        "",
        "| PDF | Parsed Markdown | Status | Notes |",
        "|---|---|---|---|",
    ]
    for pdf_path, md_path, error in results:
        status = "failed" if error else "success"
        notes = error.replace("\n", " ") if error else ""
        lines.append(
            f"| `papers/raw_pdf/{pdf_path.name}` | `papers/parsed_md/{md_path.name}` | {status} | {notes} |"
        )

    lines.extend([
        "",
        "## 解析质量说明",
        "",
        "当前解析方式能快速提取正文，但可能存在以下问题：",
        "",
        "- 双栏论文的阅读顺序可能局部混乱；",
        "- 图表、公式、页眉页脚可能混入正文；",
        "- 参考文献会被完整保留，后续精读时应避免把参考文献当作正文结论；",
        "- 如果后续需要更高质量解析，可以接入 GROBID、Marker 或 PyMuPDF。",
    ])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse PDFs into Markdown text files.")
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--backend", choices=["pymupdf4llm", "pdftotext"], default="pymupdf4llm")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pdfs = sorted(args.input_dir.glob("*.pdf"))
    results = []
    for pdf_path in pdfs:
        md_path, error = parse_pdf(pdf_path, args.output_dir, backend=args.backend)
        results.append((pdf_path, md_path, error))
        print(f"{pdf_path.name}: {'failed' if error else 'success'}")
    write_log(args.log, results, backend=args.backend)
    print(f"Parsed {len(results)} PDFs")
    print(f"Wrote log to {args.log}")


if __name__ == "__main__":
    main()
