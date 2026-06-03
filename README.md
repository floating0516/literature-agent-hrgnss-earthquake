# AI Agent Reading Knowledge Base

本目录用于设计和实现一个面向科研文献阅读、RAG 知识库构建与研究假说生成的 Agent 原型。

当前已经跑通一个最小闭环：

```text
paper search → screening → legal full text → parsing → reading note → synthesis → RAG chunks
```

当前主题：**HR-GNSS + deep learning for rapid large-earthquake source characterization**。

---

## 目录结构

```text
AI_Agent_reading/
  README.md
  文献阅读Agent设计方案与实施目标.md

  configs/                     # 主题、数据源、筛选参数等配置
    topics.yaml
    sources.yaml

  prompts/                     # 文献筛选、精读、综合、批判审查 prompt 模板
    paper_screening_prompt.md
    paper_reading_prompt.md
    synthesis_prompt.md
    critic_prompt.md
    prompt_templates_explanation_and_references.md

  scripts/                     # 可复现流程脚本
    search_openalex.py         # 搜索候选论文元数据
    screen_candidates.py       # 规则粗筛与噪声过滤
    download_pdfs.py           # 自动下载元数据中已有的开放 PDF URL
    parse_pdfs.py              # PDF 转 Markdown
    build_minimal_rag_chunks.py# 从阅读卡片和综合文档生成 RAG chunks

  papers/                      # 当前主题的论文材料
    candidates.jsonl           # 搜索得到的候选元数据
    screened_candidates.jsonl  # 粗筛后的候选
    selected_papers.jsonl      # 入选论文
    search_summary.md
    screening_results.md
    screening_comparison.md
    core_papers_priority.md
    pdf_download_results.jsonl # PDF 下载结果明细
    pdf_download_log.md        # PDF 下载记录与人工处理清单
    pdf_parse_log.md
    openalex_test_results.md

    raw_pdf/                   # 合法获取的原始 PDF / 用户手动放入的 PDF
    parsed_md/                 # PDF 解析后的 Markdown 文本
    notes/                     # 单篇论文精读卡片
    metadata/                  # 后续可放单篇 YAML/JSON 元数据

  synthesis/                   # 跨文献综合、流程记录、方法对比、结果报告
    文献搜索逻辑与开放获取策略.md
    OpenAlex搜索性能测试与架构优势记录.md
    三篇论文流程跑通记录.md
    三篇实时GNSS地震预警论文综合.md
    文献阅读Agent最小流程完成报告.md

  rag/                         # RAG 数据层
    chunks.jsonl
    minimal_rag_build_report.md
    embeddings_config.yaml

  reference_nature_agent/      # 最初参考的三篇 Nature Agent 论文和阅读报告
    README.md
    *.pdf
    阅读报告.md
    三篇Nature-Agent论文对GNSS地震学的启发.md

  archive/                     # 过时或历史材料归档区；当前仅有说明文件
```

---

## 关键入口文档

- [文献阅读 Agent 设计方案与实施目标](文献阅读Agent设计方案与实施目标.md)
- [文献阅读 Agent 最小流程完成报告](synthesis/文献阅读Agent最小流程完成报告.md)
- [三篇实时 GNSS 地震预警论文综合](synthesis/三篇实时GNSS地震预警论文综合.md)
- [最小 RAG chunk 构建报告](rag/minimal_rag_build_report.md)

---

## 可复现流程

### 1. 搜索候选论文

```bash
python3 scripts/search_openalex.py
```

输出：

```text
papers/candidates.jsonl
papers/search_summary.md
```

### 2. 粗筛候选论文

```bash
python3 scripts/screen_candidates.py
```

输出：

```text
papers/screened_candidates.jsonl
papers/selected_papers.jsonl
papers/screening_results.md
papers/screening_comparison.md
```

### 3. 自动下载开放 PDF，并人工补充机构权限 PDF

先运行自动下载脚本，下载元数据中已经提供的开放 PDF URL：

```bash
python3 scripts/download_pdfs.py
```

输出：

```text
papers/raw_pdf/*.pdf
papers/pdf_download_results.jsonl
papers/pdf_download_log.md
```

如需只检查将执行的动作、不发起下载，可运行 dry run：

```bash
python3 scripts/download_pdfs.py --dry-run
```

合规说明：本项目不绕过 paywall；闭源论文、没有开放 PDF URL 的论文，或只能通过学校/机构权限访问的论文，都会记录为 `manual_required`。用户可在合法前提下手动下载后放入：

```text
papers/raw_pdf/
```

### 4. 解析 PDF

```bash
python3 scripts/parse_pdfs.py
```

输出：

```text
papers/parsed_md/*.md
papers/pdf_parse_log.md
```

### 5. 生成/维护单篇阅读卡片

阅读卡片保存在：

```text
papers/notes/
```

模板参考：

```text
prompts/paper_reading_prompt.md
```

### 6. 生成跨文献综合

当前三篇论文综合保存在：

```text
synthesis/三篇实时GNSS地震预警论文综合.md
```

模板参考：

```text
prompts/synthesis_prompt.md
```

### 7. 构建最小 RAG chunks

```bash
python3 scripts/build_minimal_rag_chunks.py
```

输出：

```text
rag/chunks.jsonl
rag/minimal_rag_build_report.md
```

---

## 当前已跑通结果

- OpenAlex 搜索：3 个 query，去重得到 44 篇候选，总耗时约 7 秒；
- 粗筛：Keep 21、Maybe 11、Discard 12；
- 下载并处理 3 篇核心实时 GNSS / HR-GNSS 论文；
- 生成 3 篇结构化 reading notes；
- 生成 1 篇三论文 synthesis；
- 构建 81 条最小 RAG chunks。
