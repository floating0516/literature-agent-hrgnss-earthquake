# OpenAlex 搜索性能测试与架构优势记录

> 目的：记录文献阅读 Agent 在开放 API 元数据搜索阶段的初步性能测试结果、架构优势，以及后续类似测试应如何记录。

---

## 1. 测试背景

在设计文献阅读 Agent 时，曾担心如果同时调用多个文献数据库 API，会导致流程过重、耗时过长、开发复杂度过高。

因此先进行了一个轻量测试：

- 只使用 OpenAlex API；
- 只测试 3 个与 HR-GNSS / geodetic earthquake early warning / G-FAST 相关的 query；
- 每个 query 只取前 5 条结果；
- 记录搜索速度、命中数量、开放获取状态和 PDF URL 情况。

测试目的不是完成正式文献收集，而是回答：

> 只用开放 API 做第一轮元数据搜索，会不会太慢？能不能快速得到有用候选论文和 OA/PDF 信息？

---

## 2. 测试 Query

本次测试使用 3 个 query：

```text
"high-rate GNSS" earthquake early warning
"geodetic earthquake early warning"
"G-FAST" GNSS earthquake
```

这些 query 覆盖了三类核心方向：

1. 高频 GNSS 与地震预警；
2. 大地测量地震预警；
3. G-FAST 等实时 GNSS 快速震源估计系统。

---

## 3. 性能结果

| Query | 命中数量 | 请求耗时 |
|---|---:|---:|
| `"high-rate GNSS" earthquake early warning` | 188 | 3.3 秒 |
| `"geodetic earthquake early warning"` | 46 | 1.5 秒 |
| `"G-FAST" GNSS earthquake` | 61 | 2.1 秒 |

结论：

> OpenAlex 元数据搜索速度非常快。对于第一批 20–50 篇候选论文收集，搜索阶段不会成为主要时间瓶颈。

即使正式搜索中使用 3–5 个 query，每个 query 获取 20–50 条结果，预计耗时仍然在几十秒到几分钟级别。

真正的时间成本更可能出现在：

- 文献筛选；
- PDF 下载；
- PDF 解析；
- 单篇精读；
- 跨文献综合；
- 人工核查闭源文献。

---

## 4. OpenAlex 字段优势

OpenAlex 不仅返回基础元数据，也返回开放获取相关字段。例如：

```yaml
open_access:
  is_oa:
  oa_status:
best_oa_location:
  pdf_url:
```

这些字段可以直接服务于后续流程：

1. 判断论文是否开放获取；
2. 判断开放类型，如 gold、green、bronze、closed；
3. 获取可能的 PDF URL；
4. 对没有开放 PDF 的论文标记人工下载。

这说明第一版系统可以先使用 OpenAlex 完成两个任务：

> 元数据搜索 + 初步合法全文线索获取。

后续如果需要更稳妥，再用 Unpaywall 对 DOI 做二次查找。

---

## 5. 架构优势

当前文献阅读 Agent 架构的优势主要体现在以下几点。

### 5.1 搜索阶段轻量

第一版不同时接入多个复杂数据源，而是先采用：

```text
OpenAlex → 候选论文元数据 → OA/PDF 初步判断
```

这样可以快速跑通流程，避免过早陷入 API key、出版社权限、TDM 协议和机构认证问题。

### 5.2 搜索和全文获取解耦

系统明确区分：

- metadata search；
- legal full-text discovery；
- manual full-text acquisition；
- local PDF parsing；
- RAG ingestion。

这样即使某篇论文闭源，也不会阻塞整个流程。

处理方式是：

```yaml
fulltext_status: open_pdf_found / closed_or_manual_required / unknown
```

对于闭源但重要的论文，由用户通过学校权限合法下载，再放入本地目录。

### 5.3 可渐进扩展

第一版只用 OpenAlex。后续如果发现覆盖不足，可以逐步增加：

- Unpaywall：补充合法开放 PDF；
- Semantic Scholar：补充引用网络和 AI/ML 论文发现；
- Crossref：补 DOI 和出版元数据；
- NASA ADS：补地球物理方向文献；
- Zotero：接入用户手动下载的文献库。

这种结构避免了一开始就设计过重。

### 5.4 适合当前知识库工作流

搜索结果可以直接保存为：

```text
papers/candidates.jsonl
papers/search_summary.md
```

后续再进入：

```text
papers/metadata/
papers/raw_pdf/
papers/parsed_md/
papers/notes/
rag/
synthesis/
```

这和当前 Markdown 知识库结构兼容。

---

## 6. 后续性能测试记录规范

以后遇到类似性能测试，建议统一记录以下内容。

### 6.1 测试目的

说明本次测试想回答什么问题，例如：

- 搜索速度是否足够快？
- PDF 下载是否稳定？
- PDF 解析是否准确？
- RAG 构建是否耗时？
- 精读 prompt 是否成本过高？

### 6.2 测试输入

记录：

- query；
- 数据源；
- 请求数量；
- 参数；
- 测试样本规模。

### 6.3 性能指标

至少记录：

- 总耗时；
- 单请求耗时；
- 命中数量；
- 成功数量；
- 失败数量；
- 平均耗时；
- 异常情况。

### 6.4 结果质量

不仅记录速度，还要记录质量：

- 结果是否相关；
- 是否有 DOI；
- 是否有摘要；
- 是否有 OA 状态；
- 是否有 PDF URL；
- 是否出现明显噪声结果。

### 6.5 架构结论

每次测试后都应回答：

1. 这个环节是否值得自动化？
2. 是否会成为瓶颈？
3. 是否需要缓存？
4. 是否需要换 API 或增加备用数据源？
5. 是否需要人工介入？

### 6.6 保存位置

类似性能测试可以保存在：

```text
synthesis/*性能测试*.md
papers/*test_results*.md
```

如果是脚本生成的结果，可以同时保留机器可读文件和 Markdown 摘要。

---

## 7. 当前结论

本次测试支持以下决策：

1. 第一版搜索脚本先只接 OpenAlex；
2. 每个 query 可以取 20 条，不会明显浪费时间；
3. 先保存候选元数据和 OA/PDF 状态，不急着下载全文；
4. 后续用 Unpaywall 做 DOI 级合法全文补查；
5. 对闭源核心论文标记人工下载即可；
6. 当前架构设计是合理的，搜索阶段足够轻量。

---

## 8. 一句话总结

> OpenAlex 作为第一轮开放元数据搜索源速度很快、字段足够有用，适合当前文献阅读 Agent 的轻量 MVP；系统架构应保持“快速搜索、合法全文发现、闭源人工补充、本地 PDF 接入 RAG”的渐进式设计。
