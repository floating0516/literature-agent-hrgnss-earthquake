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
    search_rag_chunks.py       # 关键词检索 RAG chunks
    vector_rag_retrieval.py    # 离线 deterministic lexical-vector 检索 baseline
    evaluate_rag_retrieval.py  # 用 curated eval set 评估 RAG 检索
    run_pipeline.py            # 串联搜索、筛选、下载、解析和 RAG 构建

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
    retrieval_eval_set.jsonl
    retrieval_eval_report.md
    retrieval_eval_results.json
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

## 环境准备

推荐使用 `uv` 复现 Python 依赖环境：

```bash
uv sync --locked
```

之后可以通过 `uv run` 运行脚本，例如：

```bash
uv run python scripts/parse_pdfs.py
```

当前默认 PDF 解析 backend 是 `pymupdf4llm`，依赖已记录在 `pyproject.toml` 和 `uv.lock` 中。`pdftotext` backend 仍可作为显式兼容选项使用，但它依赖系统命令。

---

## 可复现流程

### 一键运行 pipeline

可以使用总控脚本串联搜索、筛选、下载、解析和 RAG chunk 构建：

```bash
uv run python scripts/run_pipeline.py
```

常用局部运行示例：

```bash
uv run python scripts/run_pipeline.py --from-stage download --to-stage rag
uv run python scripts/run_pipeline.py --to-stage parse --dry-run
uv run python scripts/run_pipeline.py --match-manual --manual-dir papers/manual_pdf_inbox
uv run python scripts/run_pipeline.py --rag-include-parsed-md --rag-exclude-low-quality
```

说明：手动 PDF 匹配默认关闭，只有传入 `--match-manual` 时才会扫描用户本地已有 PDF；该步骤不联网、不绕过 paywall 或任何访问控制。`--dry-run` 只对支持 dry run 的阶段生效，例如下载和手动匹配。pipeline 默认在 `parse` 和 `rag` 之间运行 `parse_quality`，生成 PDF 解析质量报告；解析后的 PDF Markdown 不会默认进入 curated RAG 输入，只有显式传入 `--rag-include-parsed-md` 时才会加入，且可用 `--rag-exclude-low-quality` 跳过低质量文件。

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

合规说明：本项目不绕过 paywall。`manual_required` 表示元数据中没有可用开放 PDF URL，或现有元数据无法定位到开放 PDF，需要人工判断或补充；`failed` 表示已经有候选 URL，但远端拒绝、超时、返回非 PDF / 登录页等，需要人工检查。

对于用户已经通过学校/机构权限或其他合法方式手动下载的 PDF，可以先放入一个本地 inbox 目录，例如：

```text
papers/manual_pdf_inbox/
```

然后先运行手动 PDF 自动匹配的 dry run，检查脚本建议如何匹配和命名：

```bash
python3 scripts/match_manual_pdfs.py --manual-dir papers/manual_pdf_inbox --dry-run
```

确认无误后再执行 apply，把匹配成功的 PDF 复制到 canonical `papers/raw_pdf/` 文件名，并更新下载结果：

```bash
python3 scripts/match_manual_pdfs.py --manual-dir papers/manual_pdf_inbox --apply
```

该匹配步骤只扫描用户本地已有 PDF，不联网下载，不读取浏览器 cookie，不绕过 paywall、验证码、Cloudflare 或任何访问控制。无法唯一高置信匹配的 PDF 会保留在日志里供人工判断。

### 4. 解析 PDF

```bash
python3 scripts/parse_pdfs.py
```

输出：

```text
papers/parsed_md/*.md
papers/pdf_parse_log.md
```

### 5. 评估 PDF 解析质量

```bash
uv run python scripts/evaluate_parse_quality.py
```

输出：

```text
papers/parse_quality.jsonl
papers/parse_quality_report.md
```

该步骤会为 `papers/parsed_md/*.md` 生成 `pass` / `warn` / `fail` 质量状态和可解释指标，用作 PDF→RAG 之间的质量闸门。

### 6. 生成/维护单篇阅读卡片

阅读卡片保存在：

```text
papers/notes/
```

模板参考：

```text
prompts/paper_reading_prompt.md
```

### 7. 生成跨文献综合

当前三篇论文综合保存在：

```text
synthesis/三篇实时GNSS地震预警论文综合.md
```

模板参考：

```text
prompts/synthesis_prompt.md
```

### 8. 构建最小 RAG chunks

```bash
python3 scripts/build_minimal_rag_chunks.py
```

输出：

```text
rag/chunks.jsonl
rag/minimal_rag_build_report.md
```

### 9. 评估 RAG 检索

默认评估 keyword baseline：

```bash
uv run python scripts/evaluate_rag_retrieval.py \
  --retriever keyword \
  --chunks rag/chunks.jsonl \
  --eval-set rag/retrieval_eval_set.jsonl \
  --report rag/retrieval_eval_report.md \
  --json-output rag/retrieval_eval_results.json
```

也可以用同一评测集评估离线 deterministic lexical-vector baseline：

```bash
uv run python scripts/evaluate_rag_retrieval.py \
  --retriever vector \
  --chunks rag/chunks.jsonl \
  --eval-set rag/retrieval_eval_set.jsonl \
  --report rag/retrieval_eval_vector_report.md \
  --json-output rag/retrieval_eval_vector_results.json
```

还可以评估 keyword + vector 分数融合的 hybrid baseline：

```bash
uv run python scripts/evaluate_rag_retrieval.py \
  --retriever hybrid \
  --chunks rag/chunks.jsonl \
  --eval-set rag/retrieval_eval_set.jsonl \
  --report rag/retrieval_eval_hybrid_report.md \
  --json-output rag/retrieval_eval_hybrid_results.json
```

如需保留 keyword/vector/hybrid 对照报告，可分别输出到不同文件：

```bash
uv run python scripts/evaluate_rag_retrieval.py \
  --retriever keyword \
  --chunks rag/chunks.jsonl \
  --eval-set rag/retrieval_eval_set.jsonl \
  --report rag/retrieval_eval_keyword_report.md \
  --json-output rag/retrieval_eval_keyword_results.json
```

输出：

```text
rag/retrieval_eval_report.md
rag/retrieval_eval_results.json
rag/retrieval_eval_vector_report.md
rag/retrieval_eval_vector_results.json
rag/retrieval_eval_hybrid_report.md
rag/retrieval_eval_hybrid_results.json
```

该步骤使用 curated retrieval eval set 评估当前 RAG retrieval，不调用外部 API、embedding model 或 vector database。评测集每条 JSONL 记录包含 `query_id`、`query`、检索意图、目标 chunk metadata、可选过滤条件和 `metrics_at`。当前报告包含 `hit@k`、`must_hit@k`、`recall@k`、MRR 和失败 query 明细。`keyword` 是关键词计数 baseline；`vector` 是本地稀疏词频向量 + cosine similarity baseline；`hybrid` 是对 keyword 和 vector 候选做归一化分数融合的 baseline。这些 retriever 都不需要联网、下载模型或引入新依赖。后续本地 embedding 或 vector DB backend 可以复用同一 eval set。

如需一次性比较 keyword / vector / hybrid，可运行对比脚本：

```bash
uv run python scripts/compare_rag_retrieval.py \
  --chunks rag/chunks.jsonl \
  --eval-set rag/retrieval_eval_set.jsonl \
  --report rag/retrieval_compare_report.md \
  --json-output rag/retrieval_compare_results.json
```

输出：

```text
rag/retrieval_compare_report.md
rag/retrieval_compare_results.json
```

`compare_rag_retrieval.py` 只负责 orchestration：它复用同一 eval set 和现有 keyword / vector / hybrid retriever，生成一个总览对比表、逐 query 对比和 warning 列表。该对比流程同样完全离线、deterministic，不下载模型、不调用远程 API、不需要 vector database。

如需把多 retriever 检索质量作为回归检查，可以启用 compare strict mode：

```bash
uv run python scripts/compare_rag_retrieval.py \
  --chunks rag/chunks.jsonl \
  --eval-set rag/retrieval_eval_set.jsonl \
  --report rag/retrieval_compare_report.md \
  --json-output rag/retrieval_compare_results.json \
  --strict \
  --min-hit-at-5 0.80 \
  --min-mrr 0.50
```

如需把单个 retriever 的检索质量作为回归检查，可以启用原有 strict mode：

```bash
uv run python scripts/evaluate_rag_retrieval.py \
  --chunks rag/chunks.jsonl \
  --eval-set rag/retrieval_eval_set.jsonl \
  --report rag/retrieval_eval_report.md \
  --strict \
  --min-hit-at-5 0.80 \
  --min-mrr 0.50
```

---

## 当前已跑通结果

- OpenAlex 搜索：3 个 query，去重得到 44 篇候选，总耗时约 7 秒；
- 粗筛：Keep 21、Maybe 11、Discard 12；
- 下载并处理 3 篇核心实时 GNSS / HR-GNSS 论文；
- 生成 3 篇结构化 reading notes；
- 生成 1 篇三论文 synthesis；
- 构建 81 条最小 RAG chunks；
- 增加 RAG 检索评测集，可用 keyword / offline lexical-vector / hybrid retriever 生成 deterministic retrieval report。
