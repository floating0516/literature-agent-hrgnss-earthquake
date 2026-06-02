# Demonstration of the Cascadia G-FAST Geodetic Earthquake Early Warning System for the Nisqually, Washington, Earthquake｜Reading Note

## 1. Metadata

- Title: Demonstration of the Cascadia G-FAST Geodetic Earthquake Early Warning System for the Nisqually, Washington, Earthquake
- Authors: Brendan W. Crowell, David A. Schmidt, Paul Bodin, John E. Vidale, Joan Gomberg, J. Renate Hartog, Victor C. Kress, Timothy I. Melbourne, Marcelo Santillan, Sarah E. Minson, Dylan G. Jamison
- Year: 2016
- Venue: Seismological Research Letters
- DOI: 10.1785/0220150255
- URL / PDF: https://www.geodesy.cwu.edu/about/pubs/Crowell_Etal_2016.pdf
- Local PDF: `papers/raw_pdf/crowell_2016_cascadia_gfast.pdf`
- Parsed text: `papers/parsed_md/crowell_2016_cascadia_gfast.md`
- Paper ID: crowell_2016_cascadia_gfast

## 2. One-sentence summary

这篇论文展示了 Cascadia 地区 G-FAST geodetic earthquake early warning 系统的原型性能：系统利用实时 GPS 位移，通过 PGD scaling、CMT 和有限断层滑动反演，在模拟的 2001 Mw 6.8 Nisqually 地震中快速估计震级、深度和震源参数。

## 3. Research problem

论文试图解决的问题是：传统基于地震波的 EEW 在大震中可能出现震级饱和，而高频 GNSS/GPS 位移不易饱和，因此能否将实时 GPS 位移加入 ShakeAlert 一类 EEW 系统，提供更稳健的大震震级和震源参数估计。

论文中的关键表述包括：

- 地震 EEW 常见问题是大震震级估计饱和，尤其是 `M > 7` 时；
- geodetic observations 提供了不随大震饱和的额外约束；
- G-FAST 的目标是在 seismic trigger 后利用 GPS 位移提供 PGD magnitude/depth、CMT 和 finite-fault slip model。

## 4. Background and motivation

论文背景是 Cascadia subduction environment 需要同时应对浅源地壳地震、深部板内地震和潜在巨大俯冲带地震。单纯依赖 P-wave 或强震仪积分位移可能受限于震级饱和、高通滤波和大震破裂持续时间。

G-FAST 作为 Pacific Northwest 的 geodetic EEW module，定位在 ShakeAlert seismic algorithms 之后：

1. ShakeAlert / ElarmS 先检测事件并提供初始 origin time、location、magnitude；
2. G-FAST 接收触发；
3. 使用实时 GPS time series 估计 PGD magnitude/depth；
4. 使用 static offsets 估计 CMT；
5. 进一步做 finite-fault slip inversion。

## 5. Data

论文使用的是 2001 Mw 6.8 Nisqually, Washington 地震的模拟测试数据。

- 地震事件：2001 Mw 6.8 Nisqually earthquake；
- 区域：Puget Sound / Cascadia / Pacific Northwest；
- 真实观测：PNSN strong-motion records、有限 GPS 静态位移参考；
- 模拟数据：在 26 个强震台站位置生成 synthetic displacement waveforms；
- 合成方法：frequency–wavenumber integration method；
- 源模型：中心位于 PNSN hypocenter，深度约 51.9 km，strike 350°，dip 70°，rake -90°，length 23 km，width 10 km，magnitude 6.8；
- 模拟扰动：latency、noise、dropouts、latency + noise + dropouts；
- 试验次数：每种模拟条件进行 1000 trials。

## 6. Method

G-FAST 系统包括两个主要部分：

1. 连续运行的数据聚合与缓存；
2. 收到 seismic alert 后触发的 modeling suite。

核心模块包括：

### 6.1 PGD magnitude and depth estimation

- 使用 peak ground displacement 与 hypocentral distance 的 scaling relationship；
- PGD 定义为三分量位移 Euclidean norm 的最大值；
- 使用 3 km/s travel-time mask；
- 至少 4 个 GPS 台站进入 mask 后才估计震级；
- 使用距离加权；
- 对 source depth 做 0–100 km 的 grid search，用 variance reduction 最大化选择深度；
- 重新标定 PGD scaling coefficients，得到 magnitude uncertainty 约 0.17 magnitude units。

### 6.2 CMT inversion

- 使用快速得到的 static offsets；
- 在 homogeneous half-space 中求解 moment tensor；
- 用 ElarmS epicenter，深度通过 VR grid search；
- CMT 用于确定 fault orientation。

### 6.3 Finite-fault slip inversion

- 使用 CMT 确定的两个 nodal planes；
- 用 Okada dislocation formulation 计算 Green's functions；
- fault size 由 CMT magnitude scaling relationship 给出；
- 用 Laplacian regularization；
- 选择 misfit 最小的 fault plane。

### 6.4 Robustness simulations

测试四种场景：

1. latency；
2. high-rate GPS station noise；
3. data dropouts；
4. latency + noise + dropouts。

## 7. Evaluation metrics

论文使用的主要指标包括：

- first-alert time；
- magnitude estimate over time；
- depth estimate over time；
- variance reduction, VR；
- CMT parameter errors: magnitude, depth, strike, dip, rake；
- finite-fault magnitude evolution；
- slip model fit；
- 对 latency/noise/dropouts 的鲁棒性。

## 8. Key results

- PGD magnitude estimates in the ideal case are available 17 s after origin time, about 4 s after ElarmS.
  Evidence: “first magnitude estimates from PGD are available 17 s after the OT, trailing ElarmS by about 4 s.”

- 在 Seattle 约 60 km 外，PGD 更新可在强震动到达前约 6 s 提供。
  Evidence: “the arrival of strong shaking in Seattle... is at 23 s after OT... an updated warning from PGD is available 6 s prior to strong shaking.”

- PGD magnitude estimates 在约 30 s 后稳定，稳定估计为 Mw 6.7 ± 0.3，接近真实 Mw 6.8。
  Evidence: “The stable magnitude estimate (> 30 s) from PGD (M 6.7 ± 0.3) ... close to the true magnitude of 6.8.”

- latency、noise、dropouts 四种模拟下，PGD magnitude/depth 都能在约 30 s 后趋于稳定，dropouts 对结果影响最大。
  Evidence: “All four simulations produce stable estimates of magnitude after about 30 s... Dropouts have the greatest impact...”

- CMT results 在考虑 latency 后约 43 s 可用，并在约 50 s 后稳定。
  Evidence: “The CMT results are available by 43 s after OT when considering latency and stabilize after ∼50 s.”

- CMT 参数在 60 s 后误差显著降低，45 s 时误差约为 0.1 magnitude units、17 km depth、35.5° strike、12.9° dip、22° rake，60 s 后至少降低三倍。
  Evidence: “We find errors of 0.1 magnitude units, 17 km depth, 35.5° in strike, 12.9° in dip, and 22° in rake. By 60 s after OT, these errors decrease by at least a factor of 3.”

- finite-fault magnitude estimates 约为 Mw 6.7，比 CMT 更接近真实震级。
  Evidence: “the magnitude derived from the finite fault (∼6.7) is much closer to the real magnitude.”

- G-FAST 对该深部事件的 slip inversion 没能正确判定 fault plane，这是系统局限。
  Evidence: “The slip inversion was not capable of ascertaining the correct fault plane for this deep event.”

## 9. Strengths

- 明确展示了 geodetic EEW 与 seismic EEW 的结合方式；
- 同时测试了 PGD、CMT 和 finite-fault slip inversion；
- 对 latency、noise、dropouts 做了系统鲁棒性模拟；
- 讨论了 G-FAST 与 G-larmS、BEFORES、ShakeAlert 的关系；
- 给出了关键时间尺度：PGD 约 17–30 s，CMT 约 43–50 s；
- 对 HR-GNSS / real-time GPS 在 EEW 中的作用有直接启发。

## 10. Limitations

- 主要基于 synthetic displacements，而非完整真实 HR-GNSS 观测；
- Nisqually 是 Mw 6.8 深部板内地震，不代表巨大俯冲带事件；
- 2001 年实际 GPS 台站数量较少，模拟使用强震台站位置生成位移；
- slip inversion 在 fault-plane ambiguity 上存在问题；
- GPS-only 在区域距离下对 M < 6 事件检测能力有限；
- 结果依赖 seismic trigger 和 ElarmS 初始事件信息；
- station density、station geometry 和 telemetry robustness 对结果有重要影响。

## 11. Relation to my research

```yaml
use_for_my_paper:
  introduction: true
  methods: true
  baseline: true
  discussion: true
  dataset: false
reason: "这篇论文是 geodetic EEW / G-FAST 的代表性系统论文，直接说明实时 GNSS 位移如何用于 PGD 震级估计、CMT、有限断层反演和 ShakeAlert 集成。它可作为 HR-GNSS 大震快速震源表征研究的重要背景和 baseline 参考。"
```

具体启发：

- 可作为 Introduction 中论证“GNSS 能缓解大震震级饱和”的引用；
- 可作为 Method 中 PGD scaling、CMT、finite-fault inversion baseline 的参考；
- 可作为 Discussion 中讨论 latency、noise、dropout、station geometry 的依据；
- 对后续 Agent 自动搜索 HR-GNSS 特征和模型很有价值，因为它已经明确了评分指标和鲁棒性因素。

## 12. Useful citations or quotable ideas

- Seismic EEW 的大震震级估计存在 saturation 问题，GNSS/geodetic observations 可提供不饱和约束。
- PGD scaling 可快速估计 magnitude 和 depth，但受 noise、dropout、latency 和 station distribution 影响。
- geodetic algorithms 在较大震级下应获得更高权重，而低震级时 seismic algorithms 更可靠。
- G-FAST、G-larmS、BEFORES 等 geodetic EEW 算法需要与 ShakeAlert DecisionModule 结合，而不是孤立运行。

## 13. Open questions

- 对更大 Mw 8–9 俯冲带地震，G-FAST 的 PGD/CMT/finite-fault 模块在真实实时数据下表现如何？
- 如何自动判断 geodetic magnitude 何时应替代或修正 seismic magnitude？
- 如何把 station geometry、dropout、latency 和 SNR 显式加入深度学习模型或评分函数？
- 对 deep learning HR-GNSS 震源表征来说，是否可以把 G-FAST 输出作为 baseline 或辅助标签？

## 14. Extracted structured tags

```yaml
domain:
  - GNSS
  - geodetic earthquake early warning
  - real-time GPS seismology
data_type:
  - synthetic high-rate GPS displacement
  - strong-motion data
  - coseismic offsets
task:
  - magnitude estimation
  - source depth estimation
  - CMT estimation
  - finite-fault slip inversion
  - earthquake early warning
method:
  - G-FAST
  - PGD scaling
  - CMT inversion
  - finite-fault inversion
  - Okada dislocation model
input_window:
  - 17s
  - 30s
  - 43s
  - 50s
metrics:
  - first-alert time
  - magnitude error
  - depth error
  - variance reduction
  - CMT parameter error
  - robustness to latency/noise/dropouts
limitations:
  - synthetic displacement data
  - station geometry
  - fault-plane ambiguity
  - detectability limit for M < 6
  - dependency on seismic trigger
```

## 15. TODO: verify

- 回到 PDF 检查 PGD regression coefficients 的排版和符号是否完整；
- 确认 `M 6.7 ± 0.3` 中 ± 符号是否来自 OCR 正确解析；
- 若后续写论文引用，需回查原 PDF 页码和图号；
- 若作为 baseline，需要进一步阅读 Crowell et al. (2013)、Melgar et al. (2015)、Minson et al. (2014)。
