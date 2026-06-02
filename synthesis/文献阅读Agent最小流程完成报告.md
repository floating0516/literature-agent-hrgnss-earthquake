# 文献阅读 Agent 最小流程完成报告

> 目的：总结本轮从文献搜索到 RAG chunk 的完整最小流程，明确已经跑通了什么、生成了哪些材料、得到什么结果，以及后续如何扩展。

---

## 1. 本轮目标

本轮目标是先不追求大规模自动化，而是验证一个可落地的文献阅读 Agent 最小闭环：

```text
开放 API 搜索
→ 候选论文元数据整理
→ 粗筛与噪声过滤
→ 核心论文优先级排序
→ 合法 PDF 获取 / 人工下载标记
→ PDF 解析
→ 单篇精读卡片
→ 跨文献综合
→ 最小 RAG chunk
→ 流程结果报告
```

当前主题是：

> HR-GNSS + deep learning for rapid large-earthquake source characterization  
> 高频 GNSS 与深度学习用于大震快速震源表征

---

## 2. 当前流程状态总表

| 阶段 | 状态 | 主要产出 |
|---|---|---|
| 设计方案 | 已完成 | `文献阅读Agent设计方案与实施目标.md` |
| 目录结构 | 已完成 | `papers/`, `prompts/`, `synthesis/`, `rag/`, `scripts/`, `configs/` |
| Prompt 模板 | 已完成 | `prompts/*_prompt.md` |
| 开源参考整理 | 已完成 | `prompts/prompt_templates_explanation_and_references.md` |
| 搜索逻辑设计 | 已完成 | `synthesis/文献搜索逻辑与开放获取策略.md` |
| OpenAlex 性能测试 | 已完成 | `synthesis/OpenAlex搜索性能测试与架构优势记录.md` |
| 轻量搜索脚本 | 已完成 | `scripts/search_openalex.py` |
| 候选元数据搜索 | 已完成 | `papers/candidates.jsonl`, `papers/search_summary.md` |
| 粗筛脚本 | 已完成 | `scripts/screen_candidates.py` |
| 筛选与噪声对比 | 已完成 | `papers/screening_results.md`, `papers/screening_comparison.md` |
| 核心论文优先级 | 已完成 | `papers/core_papers_priority.md` |
| PDF 下载 | 已完成 | `papers/raw_pdf/*.pdf`, `papers/pdf_download_log.md` |
| PDF 解析脚本 | 已完成 | `scripts/parse_pdfs.py` |
| PDF 解析结果 | 已完成 | `papers/parsed_md/*.md`, `papers/pdf_parse_log.md` |
| 单篇精读卡片 | 已完成 | `papers/notes/*_reading_note.md` |
| 三篇流程记录 | 已完成 | `synthesis/三篇论文流程跑通记录.md` |
| 跨文献综合 | 已完成 | `synthesis/三篇实时GNSS地震预警论文综合.md` |
| 最小 RAG chunk 脚本 | 已完成 | `scripts/build_minimal_rag_chunks.py` |
| 最小 RAG chunk 数据 | 已完成 | `rag/chunks.jsonl`, `rag/minimal_rag_build_report.md` |

---

## 3. 已生成的核心材料

### 3.1 方案与配置

- `文献阅读Agent设计方案与实施目标.md`  
  保存了最初的 Agent 设计、目标、角色分工、RAG 结构、MVP 路线。

- `configs/topics.yaml`  
  保存当前主题、关键词和筛选默认参数。

- `configs/sources.yaml`  
  保存开放元数据源、开放全文策略和合规原则。

- `rag/embeddings_config.yaml`  
  保存后续 embedding / vector DB 的占位配置。

### 3.2 Prompt 模板

- `prompts/paper_screening_prompt.md`  
  用于摘要级初筛，判断 keep / maybe / discard。

- `prompts/paper_reading_prompt.md`  
  用于单篇精读，生成结构化 reading note。

- `prompts/synthesis_prompt.md`  
  用于跨文献综合，抽取共识、分歧、研究空白和假说。

- `prompts/critic_prompt.md`  
  用于批判性检查，避免编造引用、过度概括和 unsupported claims。

- `prompts/prompt_templates_explanation_and_references.md`  
  整理了开源 paper-reading / literature-review prompt 与 Skill 参考。

### 3.3 搜索与筛选材料

- `scripts/search_openalex.py`  
  轻量 OpenAlex 搜索脚本，不下载 PDF，只保存 metadata、OA status、PDF URL。

- `papers/candidates.jsonl`  
  第一批候选论文元数据。

- `papers/search_summary.md`  
  搜索结果摘要。

- `scripts/screen_candidates.py`  
  规则粗筛脚本，先过滤明显噪声，再交给后续 LLM 精筛。

- `papers/screening_results.md`  
  筛选结果。

- `papers/screening_comparison.md`  
  筛选前后对比，明确 structural health monitoring、UAV、bridge monitoring 等噪声被过滤。

### 3.4 三篇论文材料

已处理三篇核心论文：

1. Crowell et al. 2016 Cascadia G-FAST
   - PDF：`papers/raw_pdf/crowell_2016_cascadia_gfast.pdf`
   - 解析：`papers/parsed_md/crowell_2016_cascadia_gfast.md`
   - 阅读卡片：`papers/notes/crowell_2016_cascadia_gfast_reading_note.md`

2. Kawamoto et al. 2016 REGARD Kumamoto
   - PDF：`papers/raw_pdf/kawamoto_2016_regard_kumamoto.pdf`
   - 解析：`papers/parsed_md/kawamoto_2016_regard_kumamoto.md`
   - 阅读卡片：`papers/notes/kawamoto_2016_regard_kumamoto_reading_note.md`

3. Melgar et al. 2019 Ridgecrest HR-GNSS
   - PDF：`papers/raw_pdf/melgar_2019_realtime_hr_gnss_ridgecrest.pdf`
   - 解析：`papers/parsed_md/melgar_2019_realtime_hr_gnss_ridgecrest.md`
   - 阅读卡片：`papers/notes/melgar_2019_realtime_hr_gnss_ridgecrest_reading_note.md`

### 3.5 综合与 RAG 材料

- `synthesis/三篇论文流程跑通记录.md`  
  记录搜索、筛选、下载、解析、阅读卡片的第一轮闭环。

- `synthesis/三篇实时GNSS地震预警论文综合.md`  
  对三篇论文进行跨文献 synthesis，比较方法、指标、限制和对 HR-GNSS + DL 的启发。

- `scripts/build_minimal_rag_chunks.py`  
  从阅读卡片和 synthesis 文档生成最小 RAG chunks。

- `rag/chunks.jsonl`  
  当前最小 RAG 数据，共 81 个 chunks。

- `rag/minimal_rag_build_report.md`  
  RAG chunk 构建报告，记录输入来源、schema 和下一步。

---

## 4. 本轮实际得到的结果

### 4.1 搜索速度可接受

OpenAlex 作为第一版 metadata search 入口是可行的。

已记录的测试结果：

- 3 个 query；
- 每个 query 20 条；
- 去重后得到 44 篇候选；
- 总耗时约 7 秒。

结论：

> 第一版文献搜索不是瓶颈，可以先用 OpenAlex 做广覆盖 metadata search，再按需要扩展 Semantic Scholar、Crossref、Unpaywall 或 NASA ADS。

### 4.2 粗筛确实能减少噪声

第一批候选中混入了：

- structural health monitoring；
- UAV；
- bridge monitoring；
- cloud computing early warning；
- machine vision deflection monitoring。

修正 query leakage 后，粗筛结果为：

- Keep：21；
- Maybe：11；
- Discard：12。

结论：

> 规则粗筛 + prompt 精筛是必要的。开放搜索很快，但噪声不可避免，必须有第一层过滤。

### 4.3 合法全文策略可行，但不能保证自动下载所有论文

采用的合规策略是：

1. 用 OpenAlex / Unpaywall / arXiv / EarthArXiv / publisher OA 查找合法全文；
2. 如果能获得 OA PDF URL，则尝试下载；
3. 如果下载失败或论文闭源，则标记为 manual download；
4. 用户可通过学校 / 机构认证合法下载后放入 `papers/raw_pdf/`；
5. Agent 只处理本地 PDF，不绕过 paywall。

本轮结果：

- 成功下载 3 篇 PDF；
- Maduo MDPI 论文自动下载失败，HTTP 403 或返回 HTML，已记录为人工处理类问题。

结论：

> 自动下载是辅助能力，不应依赖它保证 100% 获取全文。系统应把 closed/manual 状态作为正常路径处理。

### 4.4 PDF 解析能跑通，但不是最终质量

当前使用：

```text
pdftotext -layout -enc UTF-8
```

结果：

- 三篇 PDF 均成功解析为 Markdown；
- 解析文本足够支持本轮精读卡片；
- 但双栏顺序、图表、公式、页眉页脚仍可能有噪声。

结论：

> `pdftotext` 足够用于 MVP。后续追求高质量时再接 GROBID、Marker、PyMuPDF 或 publisher XML。

### 4.5 单篇精读卡片结构可用

三篇阅读卡片均包含统一字段：

- metadata；
- one-sentence summary；
- research problem；
- background；
- data；
- method；
- evaluation metrics；
- key results；
- strengths；
- limitations；
- relation to my research；
- useful citations；
- open questions；
- structured tags；
- TODO verify。

结论：

> 当前 prompt template 能把论文转换成可积累、可检索、可综合的知识单元。

### 4.6 三篇论文综合产出了可用研究判断

跨文献综合得到的核心判断：

> 实时 GNSS / HR-GNSS 已经可以在数十秒到数分钟尺度内为地震预警和快速震源表征提供不易震级饱和的位移约束，但性能高度依赖 latency、noise、dropout、台站几何、近场覆盖、震级大小和先验断层信息。

对 HR-GNSS + deep learning 的直接启发：

- 输入应包含 displacement time series、PGD、horizontal-only PGD、static offset、station geometry、dropout mask、latency；
- 输出可分层设计：Mw → source geometry proxy → finite-fault / slip representation；
- baseline 至少包括 PGD scaling、G-FAST、REGARD-style inversion；
- 训练扰动应包含 latency、noise、dropout、vertical degradation、missing near-field stations；
- 评价指标应包含 first-alert time、Mw error、PGD error、offset error、VR、station geometry sensitivity。

### 4.7 最小 RAG 数据已经生成

当前 RAG 版本：

- 输入：三篇阅读卡片 + 一篇三论文 synthesis；
- 输出：`rag/chunks.jsonl`；
- chunk 数量：81；
- chunk schema 包含：
  - `chunk_id`；
  - `paper_id`；
  - `title`；
  - `source_file`；
  - `source_type`；
  - `section`；
  - `section_level`；
  - `chunk_index`；
  - `section_index`；
  - `part_index`；
  - `char_count`；
  - `text`。

结论：

> 当前已经从“文献 PDF”推进到“结构化 RAG 语料”。虽然还没有向量库，但知识库最小数据层已经跑通。

---

## 5. 当前最小 Agent 工作流已经具备的能力

### 5.1 已具备

1. **主题配置**  
   能用 `configs/topics.yaml` 记录当前研究主题和关键词。

2. **开放搜索**  
   能通过 OpenAlex 快速获取候选论文 metadata。

3. **OA / PDF 状态记录**  
   能记录 PDF URL、OA 状态和 manual download 状态。

4. **粗筛去噪**  
   能过滤明显偏离主题的结构健康监测、UAV、桥梁监测等噪声。

5. **核心论文优先级**  
   能根据主题相关性选择第一批精读论文。

6. **PDF 解析**  
   能把本地 PDF 转为 Markdown 文本。

7. **结构化精读**  
   能把单篇论文转为统一 reading note。

8. **跨文献综合**  
   能比较多篇论文的共同指标、方法差异、限制和研究启发。

9. **最小 RAG chunk**  
   能把 reading notes 和 synthesis 转为 JSONL chunks，作为后续检索基础。

10. **流程记录**  
   能记录每次性能测试、筛选效果和流程结果。

### 5.2 暂未具备

1. 尚未接入向量数据库；
2. 尚未接入 embedding model；
3. 尚未实现 RAG query 脚本；
4. 尚未进行 LLM-based 精筛自动化；
5. 尚未批量处理 20–50 篇全文；
6. 尚未覆盖 deep learning 文献线；
7. 尚未做正式论文综述级 synthesis；
8. 尚未实现 citation/page-level verification。

---

## 6. 当前研究层面的初步收获

从三篇论文中，当前至少得到以下研究判断：

### 6.1 GNSS 对大震 EEW 的价值明确

GNSS/geodetic observations 的核心价值是：

- 不易出现大震震级饱和；
- 能直接提供静态位移；
- 能补充 seismic EEW；
- 能支持 PGD、CMT、finite-fault 等不同层级 source characterization。

### 6.2 时间窗应成为模型设计核心

不同任务的可用时间尺度不同：

- latency 本身可低至秒级；
- PGD/Mw 可在 15–30 s 进入可用状态；
- CMT/finite-fault 往往需要 40–60 s 或数分钟更稳定。

因此后续 DL 模型应按时间窗评估：

```text
10 s → 15 s → 20 s → 30 s → 60 s → 5 min
```

### 6.3 PGD 是必须保留的 baseline 和特征

PGD 在三篇论文中都处于核心位置。后续不能只做 black-box DL，而应至少与 PGD scaling 对比。

### 6.4 台站几何和 dropout 是关键问题

三篇论文都显示 station geometry / near-field coverage / dropout 会影响结果。因此模型不能假设固定、完整、规则排列的台站输入。

### 6.5 Deep learning 的可能价值点

根据当前三篇 baseline 文献，DL 的潜在价值不是简单替代所有传统方法，而可能在于：

- 更早期稳定估计 Mw；
- 在 station dropout 下保持鲁棒；
- 处理 fault-plane ambiguity；
- 学习非线性 station geometry 权重；
- 输出 uncertainty / confidence；
- 融合 GNSS 与 seismic trigger 信息。

---

## 7. 当前限制

1. 文献数量仍然很少，只有 3 篇精读；
2. 深度学习方向尚未纳入第一批精读；
3. 当前 PDF 解析质量为 MVP 级别；
4. reading note 中关键数值正式引用前需要回查 PDF；
5. RAG 只有 JSONL chunk，还没有 embedding 和检索接口；
6. 自动下载论文受 OA 链接、403、publisher 策略影响；
7. 当前 synthesis 适合内部研究规划，不应直接作为正式综述文本使用。

---

## 8. 推荐下一轮任务

为了把这个 Agent 从“最小流程跑通”推进到“可支撑研究写作”，下一轮建议按以下顺序做：

### 8.1 增加 deep learning 文献线

新增搜索 queries：

```text
"deep learning" "earthquake magnitude estimation"
"deep learning" "earthquake source characterization"
"deep learning" "finite fault inversion"
"neural network" "earthquake early warning"
"GNSS" "deep learning" earthquake
"seismogeodesy" "deep learning"
```

目标：补齐当前主题中 DL 方法侧的空白。

### 8.2 第二批精读 5–10 篇

优先选择：

1. deep learning earthquake magnitude / EEW；
2. rapid finite-fault inversion；
3. seismogeodetic fusion；
4. G-larmS / BEFORES / tsunami GNSS source inversion；
5. Mw 8–9 subduction earthquake GNSS applications。

### 8.3 建立 RAG 检索接口

在当前 `rag/chunks.jsonl` 基础上：

1. 先写关键词检索脚本；
2. 再接 embedding；
3. 再接 Chroma 或 LanceDB；
4. 要求所有 RAG 回答引用 `chunk_id` 和 `source_file`。

### 8.4 做 citation verification

正式写论文前，增加一个校验流程：

- 每个关键数值必须回到 PDF；
- 记录 page / figure / table；
- unsupported claims 标记为 TODO；
- 不编造 citation。

---

## 9. 最终结论

本轮已经把文献阅读 Agent 的最小流程跑通，结果如下：

1. **搜索能跑通**：OpenAlex 搜索快，适合作为第一入口；
2. **筛选能跑通**：粗筛能过滤 structural health monitoring、UAV、bridge monitoring 等噪声；
3. **全文获取路径能跑通**：OA PDF 自动下载可用，但 closed/manual download 必须作为正常分支；
4. **PDF 解析能跑通**：`pdftotext` 足够支持 MVP；
5. **精读能跑通**：三篇论文已生成统一 reading notes；
6. **综合能跑通**：已生成三篇实时 GNSS 论文 synthesis；
7. **RAG 数据层能跑通**：已生成 81 条最小 chunks；
8. **结果记录能跑通**：已记录性能、架构优势、筛选效果、流程状态和限制。

因此，当前系统已经从一个想法变成了一个可扩展的原型：

```text
paper search → screening → legal full text → parsing → reading note → synthesis → RAG chunks
```

下一步的关键不是重新设计流程，而是扩大文献规模，补齐 deep learning 方向，并把 `rag/chunks.jsonl` 接入可查询的检索模块。
