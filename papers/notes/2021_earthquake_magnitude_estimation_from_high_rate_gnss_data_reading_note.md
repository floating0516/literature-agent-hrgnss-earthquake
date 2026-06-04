# Earthquake Magnitude Estimation from High-Rate GNSS Data: A Case Study of the 2021 Mw 7.3 Maduo Earthquake｜Reading Note

## 1. Metadata

- Title: Earthquake Magnitude Estimation from High-Rate GNSS Data: A Case Study of the 2021 Mw 7.3 Maduo Earthquake
- Authors: Zhiyu Gao, Yanchuan Li, Xinjian Shan, Chuanhua Zhu
- Year: 2021
- Venue: Remote Sensing
- DOI: 10.3390/rs13214478
- URL / PDF: https://doi.org/10.3390/rs13214478
- Local PDF: `papers/raw_pdf/2021_earthquake_magnitude_estimation_from_high_rate_gnss_data.pdf`
- Parsed text: `papers/parsed_md/2021_earthquake_magnitude_estimation_from_high_rate_gnss_data.md`
- Paper ID: 2021_earthquake_magnitude_estimation_from_high_rate_gnss_data

## 2. One-sentence summary

这篇论文以 2021 年青海玛多 Mw 7.3 地震为例，使用 55 个 1 Hz 高频 GNSS 连续站数据，分别基于 PGD 和 PGV scaling 快速估计震级，得到最终 Mw 7.25 和 Mw 7.31，均与 USGS 报告的 Mw 7.3 基本一致。

## 3. Research problem

论文试图解决的问题是：在青藏高原大型地震场景下，高频 GNSS 数据中的 peak ground displacement, PGD 和 peak ground velocity, PGV 是否能够用于快速、可靠地估计矩震级，并为 geodetic-based earthquake early warning 提供可用震级信息。

更具体地，作者关注：

- 高频 GNSS 位移和速度波形是否能记录 2021 Mw 7.3 Maduo 地震的地震动特征；
- 基于 PGD 与 PGV 的经验回归模型能否得到与 USGS Mw 7.3 一致的震级；
- PGD 与 PGV 方法在稳定性、收敛时间和对台站数量的敏感性上有何差异；
- 在多数 GNSS 台站距离震中较远且分布不均匀时，震级估计仍能否用于早期预警。

## 4. Background and motivation

2021 年 5 月 21 日 18:04:13 UTC，中国青海省玛多县发生 Mw 7.3 地震，震中位于 98.34°E, 34.59°N，震源深度 17 km。该事件被认为发生在 Kunlunshankou–Jiangcuo Fault，是 2008 年 Mw 7.9 Wenchuan 地震以来中国大陆最大地震，对 Bayan Har block 近似稳定的传统认识提出挑战。

论文的技术背景是：传统地震仪器在大震早期预警中存在震级饱和、clip/off-scale 或加速度积分产生 baseline drift 等问题。GNSS 能直接测量长周期到静态位移的地表运动，因此可以缓解 M 7+ 地震震级估计饱和问题，并为 finite-fault slip 和 moment magnitude estimation 提供约束。

在实时 GNSS 处理方面，论文比较了 PPP、relative positioning 和 variometric approach 三类方法：PPP 需要精密轨道钟差并有 20–30 min 收敛/重收敛时间；relative positioning 精度高但依赖稳定参考站；variometric approach 使用广播星历实时估计速度，不需要参考站，但速度积分到位移可能产生误差累积。本文因此分别使用 relative positioning 获取位移波形，使用 variometric approach 获取速度时序，再比较 PGD 与 PGV 震级估计。

## 5. Data

- 事件：2021 Mw 7.3 Maduo earthquake；
- 发震时间：2021-05-21 18:04:13 UTC；
- 震中：98.34°E, 34.59°N；
- 震源深度：17 km；
- 区域：Maduo County, Qinghai Province, western China / Tibetan Plateau；
- 构造背景：Kunlunshankou–Jiangcuo Fault，位于 East Kunlun Fault 以南约 70–80 km，Bayan Har block 内部；
- 数据类型：high-rate GNSS displacement waveforms, high-rate GNSS velocity time series, PGD, PGV；
- 数据频率：1 Hz GNSS；
- 台站数量：55 个连续 high-rate GNSS stations，均在震中 550 km 内；
- 台网来源：14 个台站来自 Crustal Movement Observation Network of China, CMONOC，其余来自 Qinghai Continuously Operating Reference Stations, QHCORS；
- 参考站：SCYY station，位于四川省，距震中约 850 km；
- 处理软件与方法：GAMIT/GLOBK 的 TRACK module 用于 relative positioning；SNIVEL software package 用于 variometric approach；PPP 用于检查参考站是否受同震形变影响；
- 是否使用合成数据：未使用合成数据，本文使用 Maduo 地震实际 high-rate GNSS 观测；
- 训练/验证/测试划分：Not specified in provided text；
- 数据可复现信息：文中说明 high-rate GNSS data 由 China Earthquake Networks Center 和 Qinghai Institute of Basic Surveying and Mapping 提供；moment tensor solutions 来自 CNEC 和 USGS；TRACK 与 SNIVEL 软件来源给出链接，但原始 GNSS 数据下载入口和完整复现实验脚本未在 provided text 中明确给出。

## 6. Method

论文方法是基于高频 GNSS 观测的 PGD/PGV 震级估计流程，而不是深度学习或有限断层反演方法。

### 6.1 输入

- 55 个 high-rate GNSS stations 的 1 Hz 观测；
- 每个台站的三分量 displacement time series: north, east, up；
- 每个台站的三分量 velocity time series: north, east, up；
- 每个台站到震源的 hypocentral distance R；
- USGS 报告的 Mw 7.3 用作对比参考。

### 6.2 输出

- 每个 GNSS 台站的 PGD value；
- 每个 GNSS 台站的 PGV value；
- 每个台站随 epoch 更新的 PGD magnitude 和 PGV magnitude；
- 所有台站平均后的最终 PGD magnitude 与 PGV magnitude；
- 不同台站数量下的 magnitude stability 和 convergence time。

### 6.3 位移波形处理

作者使用 relative positioning method 获取每个高频 GNSS 台站的 displacement waveform：

- 软件：TRACK module in GAMIT/GLOBK；
- 轨道产品：IGS final orbit products；
- 天线模型：absolute antenna phase center model；
- 参考站：SCYY station；
- 未进行 displacement waveform 的 post-processing spatial filtering，以避免遮蔽同震信号；
- 使用 PPP 检查 SCYY 参考站，结果显示参考站未受同震形变影响。

### 6.4 速度时序处理

作者使用 variometric approach 获取每个台站的 velocity time series：

- 软件：SNIVEL software package；
- 使用 real-time broadcast ephemeris data；
- 使用 dual-frequency data 形成 L1 和 L2 narrow lanes 的线性组合；
- 目标是降低噪声并校正 ionospheric error 和 tropospheric delay；
- 不需要 IGS products 等外部数据。

### 6.5 PGD magnitude

三分量位移用于计算每个台站的 PGD：

- PGD 为 north/east/up 三分量位移平方和开方后的最大值；
- displacement components 单位为 meters；
- 使用 PGD 与 Mw 的经验关系：`log(PGD) = A + B × Mw + C × Mw × log(R)`；
- 使用 Ruhl et al. [26] 的回归系数：A = -5.919, B = 1.009, C = -0.145；
- 这些系数来自 29 个 Mw 6.0–9.0 moderate-to-large earthquakes 的 GNSS observational data；
- 每个台站每个 epoch 更新 Mw，直到 magnitude convergence；
- 最终 Mw 为所有 GNSS 台站估计震级的平均值。

### 6.6 PGV magnitude

三分量速度用于计算每个台站的 PGV：

- PGV 为 north/east/up 三分量速度平方和开方后的最大值；
- velocity components 单位为 m/s；
- 使用 PGV 与 Mw 的经验关系：`log(PGV) = A + B × Mw + C × Mw × log(R)`；
- 使用 Fang et al. [16] 的回归系数：A = -5.025, B = 0.741, C = -0.111；
- 这些系数来自 22 个 Mw 6.0–9.1 moderate-to-large earthquakes 的 GNSS observational data modeling；
- PGV magnitude 每个 epoch 更新，直到 convergence；
- 所有 GNSS 台站平均值作为 Maduo 地震最终 moment magnitude。

### 6.7 Baseline / comparison

- 主要对比对象：USGS 报告的 Mw 7.3；
- 方法间对比：PGD magnitude vs PGV magnitude；
- 稳定性对比：不同 high-rate GNSS station 数量下的 magnitude fluctuation 和 convergence time；
- Not specified in provided text: 没有与深度学习模型、实时有限断层反演结果或强震仪震级估计做直接数值 benchmark。

## 7. Evaluation metrics

论文使用或讨论的评价指标包括：

- 最终震级与 USGS Mw 7.3 的差异；
- PGD magnitude final estimate；
- PGV magnitude final estimate；
- PGD/PGV magnitude 的 absolute deviation；
- 不同台站的震级最大值、最小值和离散程度；
- PGD/PGV values 与 hypocentral distance 的衰减关系；
- magnitude evolution over time；
- first-alert time；
- convergence time；
- 不同 GNSS station number 对稳定性和收敛时间的影响；
- PGD 与 PGV 方法在稀疏台站条件下的稳定性差异；
- 对 geodetic-based EEW 的适用性。

## 8. Key results

- 使用 55 个 1 Hz high-rate GNSS continuous stations，PGD 和 PGV 方法均得到与 USGS Mw 7.3 一致的最终震级估计。
  Evidence: Abstract states “The final magnitude estimated from the PGD and PGV methods were Mw 7.25 and Mw 7.31, respectively.”

- PGD 最终平均震级为 Mw 7.25，略小于 USGS Mw 7.3，但被作者认为 reasonable。
  Evidence: Results section states “The final average magnitude was estimated at Mw 7.25, which is slightly smaller than the moment magnitude (Mw 7.3) reported by USGS...”

- PGV 最终平均震级为 Mw 7.31，略大于 PGD 结果，并与 USGS Mw 7.3 一致。
  Evidence: Results section states “The average magnitude after convergence was Mw 7.31... consistent with the magnitude (Mw 7.3) reported by USGS.”

- PGD magnitude 的台站间范围为 Mw 6.8 到 Mw 8.0，显示不同台站存在较大差异，可能与 site effects 和/或 radiation pattern 有关。
  Evidence: “We obtained a maximum and minimum value of PGD magnitude of Mw 8.0 and Mw 6.8... might be related to site effects and/or radiation pattern.”

- PGV magnitude 的台站间范围更大，最小 Mw 6.6，最大 Mw 8.7，说明 PGV 在不同台站间偏差更大。
  Evidence: “The maximum PGV magnitude was estimated at Mw 8.7, whereas the minimum was Mw 6.6.”

- 位移和速度波形振幅随 hypocentral distance 增大而逐渐减小；永久水平同震位移也随震源距增加而减小。
  Evidence: Results and Conclusions state “the amplitude of displacement and velocity waveforms gradually decreased with increasing hypocentral distance.”

- 对 Maduo 这类 strike-slip earthquake，vertical displacement 对地震不如 horizontal displacement 敏感，因此后续分析重点关注水平位移。
  Evidence: “vertical displacements were less sensitive... given the strike-slip focal mechanism... Therefore, we focus on horizontal displacements...”

- PGD magnitude 比 PGV magnitude 更稳定、波动更小；但最终 PGV magnitude Mw 7.31 比 PGD magnitude Mw 7.25 更接近 USGS Mw 7.3。
  Evidence: Discussion states “Compared with the PGV magnitudes, PGD magnitudes are more stable and fluctuate less. However, the final PGV magnitude (Mw 7.31) is closer to Mw 7.3...”

- 当只使用 4 个 GNSS 台站时，PGD 和 PGV 都低估震级；PGD 在约 8 个台站时可得到稳定震级，而 PGV 需要超过 15 个台站。
  Evidence: “in the case of four stations, both PGD and PGV underestimated the magnitude... PGD method can obtain a stable magnitude... about eight... PGV method requires more stations (>15).”

- 对 8 个震源距 170 km 内台站的分析显示，4 站时 PGD/PGV 收敛时间均为震后 50 s；8 站时收敛时间均为震后 73 s。
  Evidence: “when the number of GNSS stations was four, the convergence times... were all at 50 s... when... eight, the convergence times... were at 73 s...”

- 4 站条件下，PGD 方法在震后 6 s 得到 first alert，50 s 后收敛到 Mw 7.1；8 站条件下，震后 73 s 收敛到 Mw 7.5。
  Evidence: “Using four stations... first alert 6 s after the earthquake onset; 50 s later... Mw 7.1. When... eight... Mw 7.5... at 73 s...”

- 这些收敛时间长于约 40 s 的 source rupture time，主要因为几乎所有 GNSS 台站都处于远场；但 GNSS displacement time series 仍为 rapid finite-fault slip inversion 提供不可替代的约束。
  Evidence: “these convergence times are longer than the ~40 s of the source rupture... because almost all the GNSS stations were in the far-field... provide irreplaceable constraints for rapid finite-fault slip inversion.”

## 9. Strengths

- 使用真实 2021 Mw 7.3 Maduo 地震 high-rate GNSS 观测，而非合成数据；
- 同时评估 PGD 和 PGV 两类 GNSS 振幅指标，直接服务于 geodetic-based EEW；
- 数据覆盖 55 个连续台站，能够分析台站数量对震级稳定性和收敛时间的影响；
- 方法流程清楚：relative positioning 获取位移，variometric approach 获取速度，再分别使用已发表 scaling regression 估计 Mw；
- 给出可直接引用的定量结果：PGD Mw 7.25、PGV Mw 7.31、与 USGS Mw 7.3 的 absolute deviation 分别为 0.05 和 0.01 magnitude units；
- 明确讨论了稀疏 GNSS 台站场景下 PGD 相比 PGV 更稳定这一实用结论；
- 对中国大陆 / 青藏高原高频 GNSS 地震预警研究具有区域代表性；
- 讨论了 GNSS 与 seismic data integration 的必要性，对后续多源融合方法有启发。

## 10. Limitations

- 多数 high-rate GNSS stations 距震中较远且分布不均，导致收敛时间长于约 40 s 的 rupture duration；
- 本文震级估计依赖已有 PGD/PGV regression coefficients，未针对 Tibet / Maduo 区域重新训练或系统校准；
- PGV magnitude 在不同台站间波动较大，作者指出 PGV 与 moment magnitude 的 regression model 在处理 Tibet 地震时可能仍需改进；
- relative positioning 需要稳定参考站，尽管作者用 PPP 检查了 SCYY 未受同震形变影响，但实际实时系统中参考站依赖仍是潜在问题；
- variometric approach 虽适合稀疏台站和实时速度估计，但速度积分到位移可能造成 error accumulation；
- GNSS 采样率 1–10 Hz 低于强震仪 ≥50 Hz，可能损失高频信息并造成震级估计偏差；
- 没有提出新的物理震源模型或深度学习模型，主要是已有 scaling laws 的案例验证；
- 未直接评估真实 operational EEW 系统中的 telemetry latency、data dropout、实时数据质量控制和自动触发影响；
- 数据开放信息有限，provided text 未给出完整 GNSS 原始数据下载链接、处理参数文件或复现实验脚本；
- 对有限断层快速反演只作意义讨论，未实际运行 finite-fault slip inversion。

## 11. Relation to my research

```yaml
use_for_my_paper:
  introduction: true
  methods: true
  baseline: true
  discussion: true
  dataset: true
reason: "这篇论文是 HR-GNSS 在中国大陆 Mw 7+ 地震中进行 PGD/PGV 快速震级估计的直接案例，可用于支撑 GNSS 缓解大震震级饱和、比较 PGD 与 PGV 特征、讨论台站数量和远场分布对快速震级估计的影响，并可作为 deep learning 震级估计的传统 scaling-law baseline。"
```

具体启发：

- 可作为 Introduction 中论证 HR-GNSS 能用于 M 7+ earthquake magnitude estimation 的区域案例；
- 可作为 Methods 中传统 PGD/PGV scaling baseline，与深度学习模型进行对比；
- 可为输入特征设计提供参考：三分量位移、三分量速度、PGD、PGV、hypocentral distance、station number、horizontal-only signal；
- 可为 early warning 时间窗设计提供参考：4 站条件下 6 s first alert、50 s convergence；8 站条件下 73 s convergence；
- 可用于 Discussion 中讨论远场台站、稀疏台站和非均匀台站分布对 HR-GNSS 震级估计的限制；
- 对有限断层快速反演研究也有启发，因为作者指出 GNSS displacement time series 为 rapid finite-fault slip inversion 提供不可替代约束。

## 12. Useful citations or quotable ideas

- 高频 GNSS 能记录从长周期到静态位移的地表运动，因此可以缓解传统地震学方法在 M 7+ 地震中的震级饱和问题。
- 在 2021 Mw 7.3 Maduo 地震中，PGD 和 PGV 方法分别得到 Mw 7.25 和 Mw 7.31，说明 high-rate GNSS PGD/PGV 可给出与 USGS Mw 7.3 一致的快速震级估计。
- 多台站平均可以提高 GNSS scaling magnitude 的可靠性，因为单台站 PGD/PGV magnitude 可能受 site effects 和 radiation pattern 影响而显著偏离。
- 在 Maduo 事件中，PGD magnitude 比 PGV magnitude 更稳定，PGD 在约 8 个台站时可稳定，而 PGV 需要超过 15 个台站。
- 对 GNSS 台站稀疏地区，PGD 方法可能比 PGV 方法更适合早期预警应用。
- GNSS 采样率低于强震仪，可能损失高频信息，因此有效融合 geodetic data 与 seismic data 是后续必要方向。

## 13. Open questions

- 如果使用深度学习直接从多台站 HR-GNSS 位移/速度波形估计 Mw，能否比 PGD/PGV scaling 更早收敛或更稳定？
- 对青藏高原地震，是否需要建立区域化 PGD/PGV scaling relationship，而不是直接使用全球或其他区域经验系数？
- 如何把 station geometry、hypocentral distance、site effects 和 radiation pattern 显式加入震级估计模型的不确定性评估？
- 4 站条件下 6 s first alert 的 Mw 可靠性如何？早期低估是否可通过模型校正或置信度输出缓解？
- PGV 在不同台站间波动较大，是速度估计噪声、区域传播效应、site effects，还是 scaling model 不适配造成的？
- 如果近场 HR-GNSS 台站更密集，PGD/PGV 收敛时间能否短于 rupture duration，从而真正服务 before rupture end 的快速表征？
- 如何将本文 PGD/PGV 震级估计与 finite-fault rapid inversion 或 deep learning finite-source characterization 结合？

## 14. Extracted structured tags

```yaml
domain:
  - HR-GNSS
  - high-rate GNSS seismology
  - geodetic earthquake early warning
  - rapid magnitude estimation
  - Tibetan Plateau earthquakes
data_type:
  - 1Hz high-rate GNSS
  - displacement waveform
  - velocity time series
  - PGD
  - PGV
  - hypocentral distance
task:
  - earthquake magnitude estimation
  - PGD magnitude estimation
  - PGV magnitude estimation
  - geodetic-based earthquake early warning
  - station-number sensitivity analysis
method:
  - relative positioning
  - GAMIT/GLOBK TRACK
  - variometric approach
  - SNIVEL
  - PGD scaling regression
  - PGV scaling regression
  - multi-station magnitude averaging
input_window:
  - 1Hz
  - 6s first alert
  - 50s convergence with 4 stations
  - 73s convergence with 8 stations
  - ~40s source rupture duration
metrics:
  - final Mw estimate
  - absolute magnitude deviation
  - magnitude convergence time
  - first-alert time
  - station-number sensitivity
  - PGD/PGV fluctuation
  - consistency with USGS Mw
limitations:
  - far-field GNSS stations
  - uneven station distribution
  - reference station dependency
  - PGV regression uncertainty in Tibet
  - velocity integration error accumulation
  - low GNSS sampling rate relative to seismic data
  - limited reproducibility information
```

## 15. TODO: verify

- 回查原 PDF 和期刊页面，确认 DOI、URL、卷期页码和 citation 格式是否完整；
- 核查标题中 `GNSS` 大小写在正式出版物中的准确写法；
- 回查 Figure 5，确认 “four stations within current GNSS array” 与 “eight stations within 170 km” 的台站选择逻辑和距离阈值；
- 核查 4 站 first alert 6 s、50 s convergence、8 站 73 s convergence 的定义是否是以 earthquake onset 为零时刻；
- 确认 Conclusions 中 “absolute deviation of 0.05 and 0.01 magnitude units” 是否分别对应 PGD 和 PGV；
- 回查 Supplementary Figure S1，确认 SCYY 参考站 PPP 结果确实排除了同震形变影响；
- 若用于 dataset，应确认 CENC/QHCORS/CMONOC 高频 GNSS 数据是否可申请或公开下载；
- 若作为 baseline，应回查 Ruhl et al. [26] 与 Fang et al. [16] 的 regression coefficients、单位和适用震级范围。