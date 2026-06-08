# RAG 检索对比报告

> 该文件由 `scripts/compare_rag_retrieval.py` 生成，用于比较 keyword / vector / hybrid retriever 在同一评测集上的表现。

## Summary

- Chunks: `rag/chunks.jsonl`
- Eval set: `rag/retrieval_eval_set.jsonl`
- Retrievers: keyword, vector, hybrid

| Retriever | Queries | mean_hit@1 | mean_hit@3 | mean_hit@5 | mean_must_hit@5 | mean_recall@5 | MRR | Failed queries |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| keyword | 39 | 0.897 | 0.974 | 1.000 | 1.000 | 1.000 | 0.934 | 0 |
| vector | 39 | 0.897 | 1.000 | 1.000 | 0.974 | 0.987 | 0.940 | 1 |
| hybrid | 39 | 0.872 | 0.923 | 0.974 | 0.949 | 0.949 | 0.909 | 2 |

## Per-query comparison

| Query ID | Best by MRR | Keyword top/rank/MRR | Vector top/rank/MRR | Hybrid top/rank/MRR |
|---|---|---|---|---|
| `bayesian_location_uncertainty_method` | vector, hybrid | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__01_01_311f69b3337a` / 3 / 0.333 | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__05_01_569f4684ac43` / 1 / 1.000 | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__05_01_569f4684ac43` / 1 / 1.000 |
| `maduo_magnitude_estimation_result` | keyword | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__15_01_22088c7accec` / 1 / 1.000 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__04_01_0792e932b9e5` / 2 / 0.500 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__04_01_0792e932b9e5` / 5 / 0.200 |
| `geodetic_constraints_warning_value` | vector | `2019_quantifying_the_value_of_real_time_geodetic_constraints__01_01_71ec45c1a4a7` / 2 / 0.500 | `2019_quantifying_the_value_of_real_time_geodetic_constraints__08_01_40ab20d67b06` / 1 / 1.000 | `2019_quantifying_the_value_of_real_time_geodetic_constraints__01_01_71ec45c1a4a7` / 2 / 0.500 |
| `regard_kumamoto_fault_inversion` | keyword, vector, hybrid | `kawamoto_2016_regard_kumamoto__12_01_e4ed11b96500` / 1 / 1.000 | `kawamoto_2016_regard_kumamoto__10_01_805d7ceb0889` / 1 / 1.000 | `kawamoto_2016_regard_kumamoto__10_01_805d7ceb0889` / 1 / 1.000 |
| `ridgecrest_hr_gnss_performance` | keyword, vector, hybrid | `melgar_2019_realtime_hr_gnss_ridgecrest__01_01_4259037d4e2a` / 1 / 1.000 | `melgar_2019_realtime_hr_gnss_ridgecrest__01_01_4259037d4e2a` / 1 / 1.000 | `melgar_2019_realtime_hr_gnss_ridgecrest__01_01_4259037d4e2a` / 1 / 1.000 |
| `gnss_dataset_displacement` | keyword, vector, hybrid | `hr_gnss_rapid_source_characterization_synthesis__09_01_b60078695e8a` / 1 / 1.000 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__06_01_de409b8f2009` / 1 / 1.000 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__06_01_de409b8f2009` / 1 / 1.000 |
| `evaluation_metrics_warning_error` | keyword, vector, hybrid | `hr_gnss_rapid_source_characterization_synthesis__24_01_a4f6490ff558` / 1 / 1.000 | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__12_01_558c82756c99` / 1 / 1.000 | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__12_01_558c82756c99` / 1 / 1.000 |
| `limitations_sparse_generalization` | keyword, vector, hybrid | `2019_quantifying_the_value_of_real_time_geodetic_constraints__20_01_21f5f282a8d3` / 1 / 1.000 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__17_01_6426b833f07d` / 1 / 1.000 | `2019_quantifying_the_value_of_real_time_geodetic_constraints__20_01_21f5f282a8d3` / 1 / 1.000 |
| `synthesis_deep_learning_source_characterization` | keyword, vector, hybrid | `three_paper_realtime_gnss_synthesis__19_01_89944ffd4a73` / 1 / 1.000 | `three_paper_realtime_gnss_synthesis__19_01_89944ffd4a73` / 1 / 1.000 | `three_paper_realtime_gnss_synthesis__19_01_89944ffd4a73` / 1 / 1.000 |
| `gfast_pgd_finite_fault_magnitude` | vector, hybrid | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__15_01_22088c7accec` / 4 / 0.250 | `crowell_2016_cascadia_gfast__07_01_b20320f4ad09` / 1 / 1.000 | `crowell_2016_cascadia_gfast__13_01_822f8149f7c5` / 1 / 1.000 |
| `gfast_pgd_depth_method` | keyword, vector, hybrid | `crowell_2016_cascadia_gfast__19_01_d77a5bd79d4a` / 1 / 1.000 | `crowell_2016_cascadia_gfast__05_01_6625575fc339` / 1 / 1.000 | `crowell_2016_cascadia_gfast__05_01_6625575fc339` / 1 / 1.000 |
| `gfast_robustness_latency_dropout_dataset` | keyword, vector, hybrid | `crowell_2016_cascadia_gfast__11_01_f288530d771f` / 1 / 1.000 | `crowell_2016_cascadia_gfast__11_01_f288530d771f` / 1 / 1.000 | `crowell_2016_cascadia_gfast__11_01_f288530d771f` / 1 / 1.000 |
| `gfast_limitations_station_distribution` | keyword, vector, hybrid | `crowell_2016_cascadia_gfast__15_01_21b969147f3a` / 1 / 1.000 | `crowell_2016_cascadia_gfast__15_01_21b969147f3a` / 1 / 1.000 | `crowell_2016_cascadia_gfast__15_01_21b969147f3a` / 1 / 1.000 |
| `regard_real_time_positioning_dataset` | keyword, vector, hybrid | `kawamoto_2016_regard_kumamoto__08_01_1ae9d0a5c57d` / 1 / 1.000 | `kawamoto_2016_regard_kumamoto__08_01_1ae9d0a5c57d` / 1 / 1.000 | `kawamoto_2016_regard_kumamoto__08_01_1ae9d0a5c57d` / 1 / 1.000 |
| `regard_variance_reduction_metric` | keyword, vector, hybrid | `kawamoto_2016_regard_kumamoto__18_01_778f5a610fc5` / 1 / 1.000 | `kawamoto_2016_regard_kumamoto__17_01_7b4688dcc8d8` / 1 / 1.000 | `kawamoto_2016_regard_kumamoto__11_01_af9b9b9c3bc5` / 1 / 1.000 |
| `regard_kumamoto_operational_result` | keyword, vector, hybrid | `kawamoto_2016_regard_kumamoto__12_01_e4ed11b96500` / 1 / 1.000 | `kawamoto_2016_regard_kumamoto__12_01_e4ed11b96500` / 1 / 1.000 | `kawamoto_2016_regard_kumamoto__12_01_e4ed11b96500` / 1 / 1.000 |
| `ridgecrest_fastlane_data_source` | keyword, vector, hybrid | `melgar_2019_realtime_hr_gnss_ridgecrest__15_01_8b633cba8527` / 1 / 1.000 | `melgar_2019_realtime_hr_gnss_ridgecrest__06_01_6bdc2d98e2ce` / 1 / 1.000 | `melgar_2019_realtime_hr_gnss_ridgecrest__06_01_6bdc2d98e2ce` / 1 / 1.000 |
| `ridgecrest_pgd_offset_metric` | keyword, vector, hybrid | `melgar_2019_realtime_hr_gnss_ridgecrest__15_01_8b633cba8527` / 1 / 1.000 | `melgar_2019_realtime_hr_gnss_ridgecrest__08_01_1ac86fe00d4b` / 1 / 1.000 | `melgar_2019_realtime_hr_gnss_ridgecrest__08_01_1ac86fe00d4b` / 1 / 1.000 |
| `ridgecrest_real_time_waveform_result` | keyword, vector, hybrid | `melgar_2019_realtime_hr_gnss_ridgecrest__09_01_b72868671304` / 1 / 1.000 | `melgar_2019_realtime_hr_gnss_ridgecrest__03_01_4080627fabf0` / 1 / 1.000 | `melgar_2019_realtime_hr_gnss_ridgecrest__09_01_b72868671304` / 1 / 1.000 |
| `ridgecrest_vertical_noise_limitation` | keyword, vector, hybrid | `melgar_2019_realtime_hr_gnss_ridgecrest__15_01_8b633cba8527` / 1 / 1.000 | `melgar_2019_realtime_hr_gnss_ridgecrest__11_01_c8b8dbe10615` / 1 / 1.000 | `melgar_2019_realtime_hr_gnss_ridgecrest__11_01_c8b8dbe10615` / 1 / 1.000 |
| `maduo_pgd_pgv_scaling_method` | keyword, vector, hybrid | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__15_01_22088c7accec` / 1 / 1.000 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__19_01_b37ac4ee0d8a` / 1 / 1.000 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__15_01_22088c7accec` / 1 / 1.000 |
| `maduo_high_rate_station_dataset` | keyword, vector, hybrid | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__06_01_de409b8f2009` / 1 / 1.000 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__06_01_de409b8f2009` / 1 / 1.000 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__06_01_de409b8f2009` / 1 / 1.000 |
| `maduo_convergence_metric` | keyword, vector, hybrid | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__21_01_9850895f1172` / 1 / 1.000 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__14_01_40b925bfbe7e` / 1 / 1.000 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__14_01_40b925bfbe7e` / 1 / 1.000 |
| `maduo_station_geometry_limitation` | keyword, vector, hybrid | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__21_01_9850895f1172` / 1 / 1.000 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__17_01_6426b833f07d` / 1 / 1.000 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__17_01_6426b833f07d` / 1 / 1.000 |
| `geodetic_global_dataset` | keyword, vector, hybrid | `2019_quantifying_the_value_of_real_time_geodetic_constraints__01_01_71ec45c1a4a7` / 1 / 1.000 | `2019_quantifying_the_value_of_real_time_geodetic_constraints__01_01_71ec45c1a4a7` / 1 / 1.000 | `2019_quantifying_the_value_of_real_time_geodetic_constraints__01_01_71ec45c1a4a7` / 1 / 1.000 |
| `geodetic_elarms_glarms_method` | keyword, vector, hybrid | `2019_quantifying_the_value_of_real_time_geodetic_constraints__10_01_9e2d3145e1a4` / 1 / 1.000 | `2019_quantifying_the_value_of_real_time_geodetic_constraints__07_01_6f3e71c55736` / 1 / 1.000 | `2019_quantifying_the_value_of_real_time_geodetic_constraints__10_01_9e2d3145e1a4` / 1 / 1.000 |
| `geodetic_cost_savings_metric` | keyword, vector, hybrid | `2019_quantifying_the_value_of_real_time_geodetic_constraints__20_01_21f5f282a8d3` / 1 / 1.000 | `2019_quantifying_the_value_of_real_time_geodetic_constraints__08_01_40ab20d67b06` / 1 / 1.000 | `2019_quantifying_the_value_of_real_time_geodetic_constraints__13_01_7fc9c2fd7ba6` / 1 / 1.000 |
| `bayesian_location_training_data` | keyword, vector, hybrid | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__02_01_aedd3ab5f948` / 1 / 1.000 | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__16_01_e74ab6cba68e` / 1 / 1.000 | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__16_01_e74ab6cba68e` / 1 / 1.000 |
| `bayesian_uncertainty_metric` | keyword, vector, hybrid | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__19_01_b3c54a2a1c03` / 1 / 1.000 | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__12_01_558c82756c99` / 1 / 1.000 | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__12_01_558c82756c99` / 1 / 1.000 |
| `bayesian_generalization_limitation` | keyword, vector, hybrid | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__19_01_b3c54a2a1c03` / 1 / 1.000 | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__16_01_e74ab6cba68e` / 1 / 1.000 | `2020_bayesian_deep_learning_estimation_of_earthquake_location_from__16_01_e74ab6cba68e` / 1 / 1.000 |
| `synthesis_gnss_vs_seismic_saturation` | keyword, vector, hybrid | `hr_gnss_rapid_source_characterization_synthesis__09_01_b60078695e8a` / 1 / 1.000 | `hr_gnss_rapid_source_characterization_synthesis__20_01_d4648ad3b81a` / 1 / 1.000 | `hr_gnss_rapid_source_characterization_synthesis__09_01_b60078695e8a` / 1 / 1.000 |
| `synthesis_hr_gnss_training_data_gap` | keyword, vector, hybrid | `hr_gnss_rapid_source_characterization_synthesis__07_01_bdc50f2b966e` / 1 / 1.000 | `hr_gnss_rapid_source_characterization_synthesis__18_01_060f29dac829` / 1 / 1.000 | `hr_gnss_rapid_source_characterization_synthesis__07_01_bdc50f2b966e` / 1 / 1.000 |
| `synthesis_research_relation_deep_learning` | keyword, vector, hybrid | `hr_gnss_rapid_source_characterization_synthesis__08_01_7fa0a5ed6b3e` / 1 / 1.000 | `hr_gnss_rapid_source_characterization_synthesis__08_01_7fa0a5ed6b3e` / 1 / 1.000 | `hr_gnss_rapid_source_characterization_synthesis__08_01_7fa0a5ed6b3e` / 1 / 1.000 |
| `synthesis_future_work_uncertainty` | keyword, vector, hybrid | `hr_gnss_rapid_source_characterization_synthesis__08_01_7fa0a5ed6b3e` / 1 / 1.000 | `three_paper_realtime_gnss_synthesis__06_01_1cc5f9325fee` / 1 / 1.000 | `hr_gnss_rapid_source_characterization_synthesis__31_01_b90c31eb8132` / 1 / 1.000 |
| `synthesis_dataset_sources_for_modeling` | keyword, vector, hybrid | `hr_gnss_rapid_source_characterization_synthesis__09_01_b60078695e8a` / 1 / 1.000 | `hr_gnss_rapid_source_characterization_synthesis__30_01_f8600a78b119` / 1 / 1.000 | `hr_gnss_rapid_source_characterization_synthesis__09_01_b60078695e8a` / 1 / 1.000 |
| `cross_paper_pgd_magnitude_comparison` | keyword, hybrid | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__15_01_22088c7accec` / 1 / 1.000 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__08_01_dff38bf2a362` / 2 / 0.500 | `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data__19_01_b37ac4ee0d8a` / 1 / 1.000 |
| `cross_paper_latency_warning_time` | keyword, vector | `2019_quantifying_the_value_of_real_time_geodetic_constraints__20_01_21f5f282a8d3` / 1 / 1.000 | `hr_gnss_rapid_source_characterization_synthesis__36_01_3cf125586fc6` / 1 / 1.000 | `2019_quantifying_the_value_of_real_time_geodetic_constraints__01_01_71ec45c1a4a7` / 4 / 0.250 |
| `cross_paper_station_geometry_limitation` | keyword, vector | `hr_gnss_rapid_source_characterization_synthesis__24_01_a4f6490ff558` / 3 / 0.333 | `three_paper_realtime_gnss_synthesis__12_01_a48c42c3ad4e` / 3 / 0.333 | `three_paper_realtime_gnss_synthesis__12_01_a48c42c3ad4e` /  / 0.000 |
| `cross_paper_training_dataset_candidates` | keyword | `melgar_2019_realtime_hr_gnss_ridgecrest__15_01_8b633cba8527` / 1 / 1.000 | `melgar_2019_realtime_hr_gnss_ridgecrest__04_01_c28185c6e055` / 3 / 0.333 | `melgar_2019_realtime_hr_gnss_ridgecrest__01_01_4259037d4e2a` / 2 / 0.500 |

## Warnings

No warnings.

## Failed queries by retriever

- **keyword**: None
- **vector**: geodetic_constraints_warning_value
- **hybrid**: geodetic_constraints_warning_value, cross_paper_station_geometry_limitation
