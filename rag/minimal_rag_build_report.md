# 最小 RAG chunk 构建报告

> 该文件由 `scripts/build_minimal_rag_chunks.py` 生成，用于记录第一版 Markdown-first RAG 数据是否构建成功。

---

## 1. 输出文件

- Chunk JSONL: `rag/chunks.jsonl`
- Chunk 数量：182

---

## 2. 输入来源

| Source file | Source type | Chunks |
|---|---:|---:|
| `papers/notes/crowell_2016_cascadia_gfast_reading_note.md` | reading_note | 20 |
| `papers/notes/kawamoto_2016_regard_kumamoto_reading_note.md` | reading_note | 19 |
| `papers/notes/melgar_2019_realtime_hr_gnss_ridgecrest_reading_note.md` | reading_note | 16 |
| `papers/notes/2021_earthquake_magnitude_estimation_from_high_rate_gnss_data_reading_note.md` | reading_note | 22 |
| `papers/notes/2019_quantifying_the_value_of_real_time_geodetic_constraints_reading_note.md` | reading_note | 21 |
| `papers/notes/2020_bayesian_deep_learning_estimation_of_earthquake_location_from_reading_note.md` | reading_note | 20 |
| `synthesis/三篇实时GNSS地震预警论文综合.md` | synthesis | 26 |
| `synthesis/HR-GNSS大震快速震源表征研究主线综述.md` | synthesis | 38 |

---

## 3. 当前 chunk schema

```json
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
  "text": "chunk text"
}
```

---

## 4. 设计说明

- 当前版本按 Markdown heading 切分，优先保留阅读卡片和 synthesis 的语义结构；
- 暂不构建向量库，先生成可检查、可追溯的 JSONL；
- 每个 chunk 保留 `paper_id`、`source_file`、`section`，方便后续引用回原文；
- 每个 chunk 基于 section heading 和正文内容附加确定性 `tags`，便于按 method / dataset / result / limitation 等类型筛选；
- 长 section 会按段落进一步切分，避免单个 chunk 过长；
- 后续可以在此基础上接 Chroma/LanceDB 和 embedding model。

---

## 5. 下一步

1. 为 chunk 增加更细的 tags，例如 method / metric / limitation / dataset；
2. 接入 embedding，生成向量索引；
3. 写一个简单检索脚本，支持按关键词或向量查询；
4. 在生成综述时要求回答必须引用 `chunk_id` 和 `source_file`。
