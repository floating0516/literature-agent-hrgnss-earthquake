# 文献阅读 Agent 设计方案与实施目标

> 目标：设计并逐步实现一个面向科研文献阅读、知识库构建和研究假说生成的 Agent 系统。  
> 当前优先场景：围绕 GNSS、HR-GNSS、地震学、深度学习、大震快速震源表征等方向，自动检索、筛选、阅读、整理文献，并形成可持续扩展的 RAG 知识库。  
> 参考思想：Robin、Co-Scientist、ERA 三类 AI for Science Agent 系统。

---

## 1. 总体判断：这个方向是否可行？

这个方向是可行的，而且非常适合当前知识库的组织方式。

当前目录中已经包含三篇 Nature Agent 论文及其阅读报告：

- Robin：强调“文献—假说—实验/数据分析—假说更新”的科研闭环。
- Co-Scientist：强调多 Agent 假说生成、反思、排名和进化。
- ERA：强调把科学任务定义为可评分问题，然后通过 LLM + 搜索自动改进方法。

这些思想可以迁移到文献阅读与知识库构建任务中。文献阅读 Agent 不应只是“下载 PDF 并总结”，而应被设计成一个持续运行的科研辅助系统：

> 文献检索 → 文献筛选 → PDF/全文解析 → 单篇精读 → RAG 知识库构建 → 跨文献综合 → 假说生成 → 人类校验 → 知识库更新。

最终目标不是简单生成摘要，而是帮助研究者形成：

- 结构化阅读笔记；
- 主题综述；
- 方法对比表；
- 数据集和指标整理；
- 研究空白分析；
- 可检验假说；
- 与本人研究方向直接相关的引用与论证材料。

---

## 2. 核心目标

### 2.1 总目标

构建一个面向科研场景的 Literature-to-Knowledge / Literature-to-Hypothesis Agent：

> 从大量文献中自动提取方法、数据、指标、结论、局限和可检验假说，并整理成可查询、可追踪、可复用的 Markdown + RAG 知识库。

### 2.2 当前阶段目标

当前阶段不追求一次性实现完整系统，而是先完成一个可运行的最小闭环：

> 输入一个研究主题，自动或半自动检索 20–50 篇论文元数据，筛选 5–10 篇核心论文，对 3–5 篇进行精读，生成结构化阅读卡片和一篇主题综述，并把结果保存到当前知识库。

### 2.3 优先研究主题

第一阶段建议围绕以下主题展开：

> HR-GNSS + deep learning for rapid large-earthquake source characterization

中文表述：

> 基于高频 GNSS 与深度学习的大震快速震源表征。

相关子主题包括：

- HR-GNSS 快速震级估计；
- GNSS 地震预警；
- PGD scaling；
- G-FAST / BEFORES 等传统方法；
- 有限断层快速反演；
- 深度学习震源参数估计；
- Mw 饱和问题；
- 台站几何与台站覆盖影响；
- GNSS 与强震仪/地震波形多模态融合；
- 物理约束神经网络；
- 不确定性估计与模型泛化。

---

## 3. 设计原则

### 3.1 不先盲目下载大量文献

不建议一开始无差别下载几百或几千篇 PDF。更合理的流程是：

> 先检索元数据 → 再筛选相关论文 → 再下载开放获取全文 → 再精读核心论文。

原因包括：

1. 版权问题：应优先使用合法开放获取版本，例如 arXiv、EarthArXiv、开放期刊、Unpaywall 可获取 PDF。
2. 质量问题：无差别下载会引入大量低相关文献，降低 RAG 质量。
3. 成本问题：PDF 解析、embedding、精读都需要计算和 token 成本。
4. 重复问题：同一论文可能存在 DOI、arXiv、出版社页面等多个版本。

推荐策略：

> 先搜索 500 篇元数据 → 初筛 100 篇 → 下载 30–50 篇核心全文 → 精读 10–20 篇 → 再扩展引用网络。

MVP 阶段可以更小：

> 搜索 20–50 篇 → 筛选 5–10 篇 → 精读 3–5 篇。

### 3.2 分级阅读

不是所有论文都需要全文精读。建议采用三级阅读：

| 等级 | 阅读范围 | 用途 |
|---|---|---|
| Level 1 | 标题、摘要、关键词 | 初筛、建立候选列表 |
| Level 2 | 摘要、方法、结果、结论 | 判断是否值得精读 |
| Level 3 | 全文精读、提取方法/数据/指标/局限 | 核心文献卡片、综述引用 |

Agent 应该先判断一篇论文属于哪个级别，再决定是否进入全文处理。

### 3.3 所有结论必须可追踪

文献知识库必须避免“看起来像引用但实际无来源”的问题。

原则：

- 每个重要结论都应绑定来源论文；
- 尽量保留 DOI、URL、section、页码或 chunk id；
- 区分“文献原文结论”“跨文献综合推断”和“Agent 假说”；
- 对不确定内容标记 `TODO: verify`；
- 不允许 Agent 编造引用或补全不存在的文献信息。

建议所有输出按证据级别标注：

```text
[直接来自文献]
[基于多篇文献综合推断]
[Agent 假说，需要验证]
```

### 3.4 Markdown 优先，RAG 辅助

当前知识库以 Markdown 文件为主，因此第一版系统应优先产出 Markdown，而不是只把信息放进数据库。

推荐组合：

> Markdown 阅读卡片 + YAML metadata + 本地向量库。

这样既方便人工阅读和修改，也方便后续 RAG 检索。

---

## 4. 总体系统架构

推荐的系统架构如下：

```text
                ┌────────────────────┐
                │   Research Goal     │
                │  研究问题/关键词     │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ Literature Search   │
                │ 文献搜索 Agent       │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ Screening & Ranking │
                │ 初筛和排序 Agent     │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ PDF Parsing         │
                │ PDF解析与结构化      │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ Paper Reading       │
                │ 单篇精读 Agent       │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ RAG Knowledge Base  │
                │ 向量库 + Markdown    │
                └─────────┬──────────┘
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Synthesis    │  │ Hypothesis   │  │ Critic       │
│ 综述生成      │  │ 假说生成      │  │ 批判审查      │
└──────────────┘  └──────────────┘  └──────────────┘
        ↓                 ↓                 ↓
        └─────────────────┼─────────────────┘
                          ↓
                ┌────────────────────┐
                │ Human Review        │
                │ 人类科学判断         │
                └────────────────────┘
```

---

## 5. Agent 分工设计

### 5.1 Search Agent：文献检索 Agent

职责：

- 根据研究主题生成检索式；
- 调用文献数据库 API；
- 获取标题、摘要、作者、年份、DOI、引用数、开放 PDF 链接；
- 去重并保存元数据。

候选数据源：

- Semantic Scholar API；
- OpenAlex API；
- Crossref API；
- arXiv API；
- EarthArXiv；
- NASA ADS；
- Unpaywall，用于查找开放获取 PDF。

输出示例：

```yaml
title:
authors:
year:
doi:
venue:
abstract:
url:
pdf_url:
source:
citation_count:
keywords:
```

### 5.2 Screening Agent：文献筛选 Agent

职责：

- 阅读标题、摘要和关键词；
- 判断与研究主题的相关性；
- 对文献进行标签化；
- 决定 keep / maybe / discard；
- 给出筛选理由。

输出示例：

```yaml
relevance_score: 1-5
decision: keep / maybe / discard
topic_tags:
  - HR-GNSS
  - earthquake early warning
  - deep learning
reason: |
  该论文使用高频 GNSS 位移波形进行快速震级估计，和当前主题高度相关。
```

### 5.3 PDF Parser：全文解析模块

职责：

- 下载合法开放获取 PDF；
- 提取正文、图注、参考文献；
- 尽可能识别章节结构；
- 将 PDF 转换为 Markdown 或结构化文本。

候选工具：

| 工具 | 用途 |
|---|---|
| PyMuPDF / fitz | 快速提取 PDF 文本 |
| GROBID | 解析学术论文结构和参考文献 |
| Marker | PDF 转 Markdown |
| Nougat | 对复杂论文 PDF/OCR 有帮助 |
| Unstructured | 通用文档解析和分块 |

第一版推荐：

> PyMuPDF + Marker；后续再考虑 GROBID。

### 5.4 Reading Agent：单篇论文精读 Agent

职责：

- 对核心论文进行结构化精读；
- 提取研究问题、数据、方法、结果、指标、局限；
- 判断与本人研究方向的关系；
- 形成 Markdown 阅读卡片。

阅读卡片模板：

```markdown
# Paper Reading Note

## Metadata
- Title:
- Authors:
- Year:
- DOI:
- Venue:
- URL:

## One-sentence summary

## Research problem

## Data

## Method

## Key results

## Evaluation metrics

## Strengths

## Limitations

## Relation to my research

## Useful citations

## Open questions

## Tags
```

### 5.5 Knowledge Base Agent：知识库构建 Agent

职责：

- 将阅读卡片保存为 Markdown；
- 提取 YAML metadata；
- 对全文和阅读笔记分块；
- 构建向量索引；
- 保留 chunk 来源信息。

每个 chunk 建议保留：

```yaml
paper_id:
title:
year:
doi:
section:
chunk_id:
tags:
source_file:
```

### 5.6 Synthesis Agent：跨文献综合 Agent

职责：

- 从多篇论文中总结主题脉络；
- 生成方法对比表；
- 总结数据集、指标、局限；
- 为论文 Introduction / Related Work / Discussion 提供素材。

典型问题：

- HR-GNSS 快速震级估计的主要方法有哪些？
- PGD scaling、G-FAST、有限断层快速反演和深度学习方法有什么差异？
- 哪些论文讨论了 Mw 饱和问题？
- 哪些方法适合快速大震源表征？
- 当前文献中还缺少什么？

### 5.7 Hypothesis Agent：假说生成 Agent

职责：

- 根据文献空白生成可检验假说；
- 将假说转化为潜在实验设计；
- 标记所需数据、方法和评分指标。

示例假说：

- HR-GNSS 前 30–120 秒位移增长率比单一 PGD 更能预测最终 Mw；
- 台站方位覆盖指标可以降低大震震级低估风险；
- 加入物理约束的深度学习模型在跨区域泛化中优于纯数据驱动模型；
- GNSS + 强震仪多模态融合在早期时间窗内比单一 GNSS 更稳定。

### 5.8 Critic Agent：批判审查 Agent

职责：

- 检查阅读笔记和综合结论是否有证据；
- 识别过度推断；
- 检查引用是否真实；
- 从审稿人角度质疑假说是否可验证、是否新颖、是否有物理意义。

---

## 6. RAG 知识库设计

### 6.1 第一版技术选型

推荐第一版采用：

> Markdown + YAML metadata + Chroma 或 LanceDB。

原因：

- Markdown 符合当前知识库习惯；
- YAML 方便存储结构化元数据；
- Chroma / LanceDB 易于本地部署；
- 后续可迁移到 Qdrant 或 PostgreSQL + pgvector。

### 6.2 向量库中应保存的信息

每个 chunk 应包含：

```yaml
paper_id: ""
title: ""
authors: []
year: null
doi: ""
section: ""
chunk_id: ""
text: ""
tags: []
source_type: "abstract / fulltext / reading_note"
source_file: ""
```

### 6.3 检索方式

不要只依赖向量检索，建议同时支持：

1. 向量检索：找语义相关段落；
2. 关键词检索：找 `PGD`, `G-FAST`, `BEFORES`, `Mw saturation` 等术语；
3. 元数据过滤：按年份、主题、方法、数据类型筛选；
4. 手工 Markdown 链接：方便人工维护。

---

## 7. 针对 GNSS 与地震学的专用字段

由于当前重点是 HR-GNSS、地震学和深度学习，建议每篇论文额外提取以下字段：

```yaml
domain:
  - GNSS
  - earthquake early warning
  - source characterization

earthquake_type:
  - crustal
  - subduction
  - megathrust

data_type:
  - HR-GNSS
  - static GNSS displacement
  - strong motion
  - seismic waveform
  - InSAR
  - synthetic data

task:
  - magnitude estimation
  - source location
  - finite fault inversion
  - rupture extent estimation
  - event detection

method:
  - PGD scaling
  - finite fault inversion
  - MLP
  - LSTM
  - Transformer
  - GNN
  - physics-informed model

input_window:
  - 10s
  - 30s
  - 60s
  - 120s

metrics:
  - Mw MAE
  - location error
  - rupture length error
  - warning time
  - robustness

limitations:
  - station coverage
  - regional bias
  - small dataset
  - synthetic-real gap
  - magnitude saturation

use_for_my_paper:
  introduction: true
  method: false
  discussion: true
  baseline: true
```

---

## 8. 推荐目录结构

建议在当前 `AI_Agent_reading/` 目录下逐步形成以下结构：

```text
AI_Agent_reading/
  README.md

  papers/
    raw_pdf/
      *.pdf

    parsed_md/
      *.md

    metadata/
      *.yaml

    notes/
      *_reading_note.md

  synthesis/
    阅读报告.md
    三篇Nature-Agent论文对GNSS地震学的启发.md
    文献阅读Agent设计方案与实施目标.md
    HR-GNSS快速震源表征文献综述.md

  rag/
    chroma_db/
    chunks.jsonl
    embeddings_config.yaml

  prompts/
    paper_screening_prompt.md
    paper_reading_prompt.md
    synthesis_prompt.md
    critic_prompt.md

  scripts/
    search_papers.py
    download_open_access_pdf.py
    parse_pdf.py
    build_rag_index.py
    query_rag.py

  configs/
    topics.yaml
    sources.yaml
```

当前文档可以作为系统设计的起点。后续可以先新建 `prompts/`、`configs/` 和 `papers/notes/`，再逐步补齐脚本。

---

## 9. MVP：最小可行系统

### 9.1 MVP 目标

第一版不追求全自动大规模系统，而是实现一个小闭环：

> 输入一个研究主题，搜索 20–50 篇论文元数据，筛选 5–10 篇，下载或整理 3–5 篇核心开放全文，生成阅读卡片，构建一个小型 RAG，并输出一篇主题综述。

### 9.2 MVP 输入

示例主题：

```text
HR-GNSS and deep learning for rapid large earthquake source characterization
```

### 9.3 MVP 输出

```text
papers/metadata/*.yaml
papers/parsed_md/*.md
papers/notes/*_reading_note.md
rag/chunks.jsonl
synthesis/HR-GNSS快速震源表征文献综述.md
```

### 9.4 MVP 成功标准

MVP 是否成功，可以用以下标准判断：

1. 能自动或半自动找到一批主题相关论文；
2. 能筛选出明显相关的核心论文；
3. 能对至少 3 篇论文生成结构化阅读卡片；
4. 能回答基于这些论文的问题，并给出来源；
5. 能生成一份主题综述草稿；
6. 生成结果没有明显伪造引用；
7. 人工修改成本低于从零阅读整理。

---

## 10. 分阶段实施计划

### 阶段 0：整理设计文档与目标

目标：

- 保存当前系统设计；
- 明确第一阶段研究主题；
- 确定目录结构和输出格式。

产出：

- `文献阅读Agent设计方案与实施目标.md`

状态：当前阶段。

### 阶段 1：建立目录结构和模板

任务：

- 新建 `papers/`、`synthesis/`、`prompts/`、`configs/`、`rag/`、`scripts/`；
- 编写阅读卡片模板；
- 编写筛选 prompt、精读 prompt、综合 prompt、批判 prompt；
- 编写主题配置文件。

产出：

- `prompts/paper_screening_prompt.md`
- `prompts/paper_reading_prompt.md`
- `prompts/synthesis_prompt.md`
- `prompts/critic_prompt.md`
- `configs/topics.yaml`
- `configs/sources.yaml`

### 阶段 2：文献检索与元数据保存

任务：

- 使用 Semantic Scholar / OpenAlex / Crossref 搜索论文；
- 保存论文元数据；
- 去重；
- 初步按相关性排序。

产出：

- `papers/metadata/*.yaml`
- `papers/candidates.csv` 或 `papers/candidates.jsonl`

### 阶段 3：文献筛选

任务：

- 根据标题、摘要、关键词进行初筛；
- 给出 keep / maybe / discard；
- 为每篇论文生成标签和相关性评分。

产出：

- `papers/screening_results.md`
- `papers/selected_papers.yaml`

### 阶段 4：PDF 获取与解析

任务：

- 优先下载开放获取 PDF；
- 将 PDF 转为 Markdown；
- 保存原始 PDF 和解析文本；
- 对无法获取全文的论文，只保存元数据和摘要。

产出：

- `papers/raw_pdf/*.pdf`
- `papers/parsed_md/*.md`

### 阶段 5：单篇论文精读

任务：

- 对 3–5 篇核心论文生成阅读卡片；
- 提取方法、数据、指标、局限和可引用观点；
- 标记与本人研究的关系。

产出：

- `papers/notes/*_reading_note.md`

### 阶段 6：构建小型 RAG

任务：

- 对 parsed text 和 reading notes 进行分块；
- 建立 embedding；
- 保存 chunk metadata；
- 支持基于来源的问答。

产出：

- `rag/chunks.jsonl`
- `rag/chroma_db/` 或 `rag/lancedb/`

### 阶段 7：跨文献综合与研究假说生成

任务：

- 总结 HR-GNSS 快速震源表征文献脉络；
- 整理方法对比表；
- 整理数据和评价指标；
- 生成研究空白；
- 生成可检验假说；
- 用 Critic Agent 审查输出。

产出：

- `synthesis/HR-GNSS快速震源表征文献综述.md`
- `synthesis/HR-GNSS方法对比表.md`
- `synthesis/可检验研究假说.md`

---

## 11. 第一阶段推荐执行顺序

建议按以下顺序执行：

1. 保存本设计文档；
2. 建立目录结构；
3. 写 prompt 模板；
4. 写 `topics.yaml`，明确第一批主题关键词；
5. 手动或半自动收集第一批 20–50 篇论文元数据；
6. 进行摘要级筛选；
7. 选择 3 篇核心论文进行自动精读测试；
8. 根据输出质量修订 prompt；
9. 再扩大到 10 篇；
10. 构建第一版 RAG；
11. 生成第一份主题综述。

---

## 12. 当前明确的执行目标

### 总目标

> 构建一个面向 GNSS 与地震学研究的文献阅读 Agent，使其能够从文献中提取方法、数据、指标、结论和研究空白，并服务于 HR-GNSS + deep learning 大震快速震源表征研究。

### 近期目标

> 在当前 `AI_Agent_reading/` 知识库中，先完成一个小型原型：围绕 HR-GNSS 快速震源表征，整理 3–5 篇核心论文，生成结构化阅读卡片、文献筛选表和一份综述草稿。

### 后续目标

> 在原型稳定后，逐步增加自动检索、PDF 解析、RAG 检索、跨文献综合、假说生成和批判审查能力。

---

## 13. 一句话总结

这个系统的核心不是“批量下载 PDF 并总结”，而是：

> 建立一个可追踪、可评分、可迭代的科研文献 Agent，把文献阅读转化为结构化知识库、主题综述和可检验研究假说。
