# 手动 PDF 匹配后的阅读优先级清单

> 依据当前 `papers/pdf_download_results.jsonl`、`papers/parsed_md/` 和已抽查的解析文本质量生成。目标是从已可读的 40 篇 PDF 中，优先选择最适合进入结构化 reading note 与后续 RAG 更新的论文。

---

## 当前状态

- 下载结果记录：32 条。
- 已有 PDF 的记录：31 条。
- 手动下载并自动匹配：18 条。
- 自动下载成功：1 条。
- 已存在本地 PDF 并跳过：12 条。
- 仍缺 PDF：1 条。
- 当前 `papers/parsed_md/` 中已解析 Markdown：40 篇。

仍缺 PDF 的论文：

| Year | Title | DOI | Status |
|---:|---|---|---|
| 2018 | G‐FAST Earthquake Early Warning Potential for Great Earthquakes in Chile | `10.1785/0220170180` | `manual_required` |

---

## 解析质量抽查结论

抽查文件：

- `papers/parsed_md/2021_earthquake_magnitude_estimation_from_high_rate_gnss_data.md`
- `papers/parsed_md/2019_quantifying_the_value_of_real_time_geodetic_constraints.md`
- `papers/parsed_md/2020_bayesian_deep_learning_estimation_of_earthquake_location_from.md`
- `papers/parsed_md/2015_real_time_capture_of_seismic_waves_using_high.md`

总体判断：

- 标题、作者、摘要、Introduction 等主体内容可读。
- DOI、citation、key points、abstract 大多保留。
- 多栏论文存在页眉、页脚、版权声明、下载水印和换页符干扰。
- 个别 PDF 有少量乱码或断词，例如标题换行、特殊字符、连字符。
- 目前质量足够用于第一轮 reading note，但生成 notes 时需要忽略页眉页脚、水印和 references 噪声。

---

## 第一批优先精读：建议 8 篇

这 8 篇覆盖当前主题的主线：HR-GNSS / real-time GNSS / geodetic EEW / rapid source characterization / deep learning source characterization。

### 1. Earthquake Magnitude Estimation from High-Rate GNSS Data: A Case Study of the 2021 Mw 7.3 Maduo Earthquake

- Year: 2021
- DOI: `10.3390/rs13214478`
- Parsed MD: `papers/parsed_md/2021_earthquake_magnitude_estimation_from_high_rate_gnss_data.md`
- Priority: P0
- 方向：high-rate GNSS、PGD/PGV、震级估计、Maduo earthquake。

选择理由：标题和方法直接对应当前主题，是第一批最应该精读的论文。

### 2. Quantifying the Value of Real-Time Geodetic Constraints for Earthquake Early Warning Using a Global Seismic and Geodetic Data Set

- Year: 2019
- DOI: `10.1029/2018JB016935`
- Parsed MD: `papers/parsed_md/2019_quantifying_the_value_of_real_time_geodetic_constraints.md`
- Priority: P0
- 方向：real-time geodetic constraints、EEW、global dataset、seismic/geodetic comparison。

选择理由：提供全球数据集和评价指标，适合为后续方法设计提供 benchmark 和问题定义。

### 3. Real-Time High-Rate GNSS Displacements: Performance Demonstration During the 2019 Ridgecrest, CA Earthquakes

- Year: 2019
- DOI: `10.31223/osf.io/pdxqw`
- Parsed MD: `papers/parsed_md/2019_real_time_high_rate_gnss_displacements_performance_demonstration.md`
- Priority: P0
- 方向：real-time HR-GNSS displacement、Ridgecrest earthquake、实时位移性能。

选择理由：已有 reading note，可作为新一轮 reading note 的格式参考，也能连接 HR-GNSS 数据处理与实际地震事件。

### 4. First result from the GEONET real-time analysis system (REGARD): the case of the 2016 Kumamoto earthquakes

- Year: 2016
- DOI: `10.1186/s40623-016-0564-4`
- Parsed MD: `papers/parsed_md/2016_first_result_from_the_geonet_real_time_analysis.md`
- Priority: P0
- 方向：REGARD、GEONET、实时 GNSS、震源模型估计。

选择理由：已有 reading note，是实时 GNSS 系统实现的代表文献，应纳入核心背景。

### 5. Demonstration of the Cascadia G-FAST Geodetic Earthquake Early Warning System for the Nisqually, Washington, Earthquake

- Year: 2016
- DOI: `10.1785/0220150255`
- Parsed MD: `papers/parsed_md/2016_demonstration_of_the_cascadia_g_fast_geodetic_earthquake.md`
- Priority: P1
- 方向：G-FAST、geodetic EEW、系统验证。

选择理由：已有 reading note，是 G-FAST 系统主线入口文献。

### 6. Real-time capture of seismic waves using high-rate multi-GNSS observations: Application to the 2015 Mw 7.8 Nepal earthquake

- Year: 2015
- DOI: `10.1002/2015GL067044`
- Parsed MD: `papers/parsed_md/2015_real_time_capture_of_seismic_waves_using_high.md`
- Priority: P1
- 方向：high-rate multi-GNSS、variometric approach、Nepal earthquake。

选择理由：适合补充 GNSS 波形和速度/位移估计方法背景。

### 7. The value of real-time GNSS to earthquake early warning

- Year: 2017
- DOI: `10.1002/2017GL074502`
- Parsed MD: `papers/parsed_md/2017_the_value_of_real_time_gnss_to_earthquake.md`
- Priority: P1
- 方向：real-time GNSS、EEW 价值评估。

选择理由：适合写 Introduction / Related Work，用来说明 GNSS 对大震预警的独特价值。

### 8. Bayesian-Deep-Learning Estimation of Earthquake Location from Single-Station Observations

- Year: 2020
- Parsed MD: `papers/parsed_md/2020_bayesian_deep_learning_estimation_of_earthquake_location_from.md`
- Priority: P1
- 方向：deep learning、Bayesian neural network、earthquake source characterization、uncertainty。

选择理由：虽然不是 GNSS 论文，但与 deep learning source characterization 和不确定性估计直接相关，可作为机器学习方法线的入口。

---

## 第二批候选阅读

| Priority | Year | Title | Parsed MD | Why |
|---|---:|---|---|---|
| P2 | 2011 | Real-time GPS seismology with a stand-alone receiver | `papers/parsed_md/2011_real_time_gps_seismology_with_a_stand_alone.md` | 早期实时 GPS seismology 代表文献 |
| P2 | 2014 | Real-time GNSS seismology using a single receiver | `papers/parsed_md/2014_real_time_gnss_seismology_using_a_single_receiver.md` | 可与 2011 年单接收机工作对比 |
| P2 | 2017 | Self-contained local broadband seismogeodetic early warning system: Detection and location | `papers/parsed_md/2017_self_contained_local_broadband_seismogeodetic_early_warning_system.md` | seismogeodetic 系统设计 |
| P2 | 2021 | FinDerS(+): Real-Time Earthquake Slip Profiles and Magnitudes Estimated from Backprojected Displacement | `papers/parsed_md/2021_finders_real_time_earthquake_slip_profiles_and_magnitudes.md` | slip profile 与 magnitude 实时估计 |
| P2 | 2020 | Toward Near-Field Tsunami Forecasting Along the Cascadia Subduction Zone Using Rapid GNSS Source Models | `papers/parsed_md/2020_toward_near_field_tsunami_forecasting_along_the_cascadia.md` | GNSS source model 到 tsunami forecasting |
| P2 | 2021 | Regularized reconstruction of peak ground velocity and acceleration from very high-rate GNSS PPP | `papers/parsed_md/2021_regularized_reconstruction_of_peak_ground_velocity_and_acceleration.md` | very high-rate GNSS PPP 与 PGV/PGA 重建 |
| P2 | 2018 | Stand-Alone GNSS Sensors as Velocity Seismometers | `papers/parsed_md/2018_stand_alone_gnss_sensors_as_velocity_seismometers_real.md` | GNSS velocity seismometer 方向 |
| P2 | 2022 | The 2021 Mw 7.4 Madoi Earthquake: An Archetype Bilateral Slip-Pulse Rupture | `papers/parsed_md/2022_the_2021_i_m_i_sub_i_w.md` | Madoi/Maduo 大震破裂过程背景 |

---

## 推荐下一步执行

建议下一步不要一次性生成 8 篇完整 reading notes，而是先做 3 篇 P0 新增/更新 notes，形成稳定模板：

1. `2021_earthquake_magnitude_estimation_from_high_rate_gnss_data.md`
2. `2019_quantifying_the_value_of_real_time_geodetic_constraints.md`
3. `2020_bayesian_deep_learning_estimation_of_earthquake_location_from.md`

原因：

- 第 1 篇直接对应 HR-GNSS magnitude estimation。
- 第 2 篇提供 real-time geodetic EEW 评价框架。
- 第 3 篇引入 deep learning source characterization 与 uncertainty。

完成这 3 篇后，再把已有 3 篇 notes 与新 notes 一起更新 RAG chunks，并写一篇小型 synthesis。