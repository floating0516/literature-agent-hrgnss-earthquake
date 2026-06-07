# RAG 检索评测报告

> 该文件由 `scripts/evaluate_rag_retrieval.py` 生成，用于评估当前 RAG 检索是否能找回人工标注的目标 chunks。

## Summary

- Retriever: keyword
- Chunks: `rag/chunks.jsonl`
- Eval set: `rag/retrieval_eval_set.jsonl`
- Queries: 10
- mean_hit@1: 0.700
- mean_hit@3: 0.900
- mean_hit@5: 1.000
- MRR: 0.808

## Per-query results

| Query ID | hit@1 | hit@3 | hit@5 | must_hit@5 | MRR | Top rank | Top retrieved |
|---|---:|---:|---:|---:|---:|---:|---|
| `bayesian_location_uncertainty_method` | 0 | 1 | 1 | 1 | 0.333 | 3 | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__01_01_311f69b3337a` |
| `maduo_magnitude_estimation_result` | 1 | 1 | 1 | 1 | 1.000 | 1 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__15_01_22088c7accec` |
| `geodetic_constraints_warning_value` | 0 | 1 | 1 | 1 | 0.500 | 2 | `2019_quantifying_the_value_of_real_time_geodetic_constraints__01_01_71ec45c1a4a7` |
| `regard_kumamoto_fault_inversion` | 1 | 1 | 1 | 1 | 1.000 | 1 | `kawamoto_2016_regard_kumamoto__12_01_e4ed11b96500` |
| `ridgecrest_hr_gnss_performance` | 1 | 1 | 1 | 1 | 1.000 | 1 | `melgar_2019_realtime_hr_gnss_ridgecrest__01_01_4259037d4e2a` |
| `gnss_dataset_displacement` | 1 | 1 | 1 | 1 | 1.000 | 1 | `hr_gnss_rapid_source_characterization_synthesis__09_01_b60078695e8a` |
| `evaluation_metrics_warning_error` | 1 | 1 | 1 | 1 | 1.000 | 1 | `hr_gnss_rapid_source_characterization_synthesis__24_01_a4f6490ff558` |
| `limitations_sparse_generalization` | 1 | 1 | 1 | 1 | 1.000 | 1 | `2019_quantifying_the_value_of_real_time_geodetic_constraints__20_01_21f5f282a8d3` |
| `synthesis_deep_learning_source_characterization` | 1 | 1 | 1 | 1 | 1.000 | 1 | `three_paper_realtime_gnss_synthesis__19_01_89944ffd4a73` |
| `gfast_pgd_finite_fault_magnitude` | 0 | 0 | 1 | 1 | 0.250 | 4 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__15_01_22088c7accec` |

## Failures

No failed queries.
