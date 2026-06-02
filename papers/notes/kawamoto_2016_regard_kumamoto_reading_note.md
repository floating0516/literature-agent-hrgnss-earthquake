# First result from the GEONET real-time analysis system (REGARD): the case of the 2016 Kumamoto earthquakes｜Reading Note

## 1. Metadata

- Title: First result from the GEONET real-time analysis system (REGARD): the case of the 2016 Kumamoto earthquakes
- Authors: Satoshi Kawamoto, Yohei Hiyama, Yusaku Ohta, Takuya Nishimura
- Year: 2016
- Venue: Earth, Planets and Space
- DOI: 10.1186/s40623-016-0564-4
- URL / PDF: https://earth-planets-space.springeropen.com/track/pdf/10.1186/s40623-016-0564-4
- Local PDF: `papers/raw_pdf/kawamoto_2016_regard_kumamoto.pdf`
- Parsed text: `papers/parsed_md/kawamoto_2016_regard_kumamoto.md`
- Paper ID: kawamoto_2016_regard_kumamoto

## 2. One-sentence summary

这篇论文报告了日本 GEONET 实时分析系统 REGARD 在 2016 Kumamoto 地震中的首次实际运行结果，展示了 RTK-GNSS 能在约 1 分钟内给出有限断层模型初估，并在约 5 分钟内收敛到与后处理 GNSS/InSAR 结果一致的震源模型。

## 3. Research problem

论文关注的问题是：基于日本 GEONET 的实时 GNSS 位移系统，能否在真实地震发生时快速估计震级、断层几何、有限断层参数和同震位移，从而服务于 GNSS-based earthquake early warning 和灾害响应。

## 4. Background and motivation

2016 Kumamoto 地震序列包括 4 月 14 日 Mj 6.5 前震、4 月 15 日 Mj 6.4 前震和 4 月 16 日 Mj 7.3 主震。传统 JMA EEW 可在数秒到数十秒内提供震中和震级，但快速了解震源范围对滑坡、火灾、余震、地表破裂等次生灾害判断很重要。

REGARD 的目标是利用 GEONET 超过 1300 个 GNSS 台站的实时定位结果，自动估计：

- 同震位移；
- 单矩形断层模型；
- 大震震级和震源范围；
- 未来可扩展到大震滑动分布模型。

## 5. Data

- 事件：2016 Kumamoto earthquakes；
  - April 14 foreshock: Mj 6.5；
  - April 15 foreshock: Mj 6.4；
  - April 16 mainshock: Mj 7.3。
- 数据源：GEONET real-time GNSS network；
- 台站数量：GEONET 超过 1300 站，图中主震近场使用周边台站；
- 数据类型：1 Hz real-time GNSS station positions；
- 定位方式：RTK-GNSS，使用 RTKLIB 2.4.2；
- 轨道信息：IGS ultra-rapid orbit predicted part；
- 对比数据：post-processed GNSS / GEONET F3 solution，InSAR-derived model，JMA CMT。

## 6. Method

REGARD 系统由三个子系统组成：

1. Real-time positioning subsystem；
2. Event detection subsystem；
3. Fault model inversion subsystem。

### 6.1 Real-time positioning

- GEONET 1 Hz real-time data stream；
- RTKLIB 2.4.2；
- dual-frequency phase and pseudo-range data；
- elevation cutoff angle 7°；
- 使用 IGS ultra-rapid orbit。

### 6.2 Event detection

事件由两类信息触发：

- JMA EEW；
- RAPiD-type displacement detection。

触发条件包括：

- JMA EEW magnitude > 7.0；或
- nearby GEONET stations short-term / long-term average discrepancy exceeds 10 cm。

### 6.3 Fault model inversion

- 模型：single rectangular fault model；
- 参数：9 个 fault parameters，包括 latitude、longitude、depth、length、width、strike、dip、rake、slip；
- 额外参数：east/north/vertical translation parameters，用于 common-mode noise；
- 先验：JMA EEW location/magnitude、Utsu scaling law、pre-assumed focal mechanism database；
- Green's function：Okada dislocation model in homogeneous half-space；
- 优化：Newton's method；
- 评价指标：variance reduction, VR；
- 为降低计算时间，每次 inversion 前减少到 200 个台站，其中包括 50 个近场台站和随机选取的 150 个台站；
- inversion 持续更新 5 分钟。

## 7. Evaluation metrics

- finite-fault model update time；
- moment magnitude estimate, Mw；
- variance reduction, VR；
- fault geometry 与后处理 GNSS/InSAR 模型是否一致；
- real-time vs post-processed displacement discrepancy；
- 是否能检测 M6-class foreshock coseismic displacements；
- 是否能在较低阈值下模拟估计 M6-class finite-fault model。

## 8. Key results

- REGARD 对 April 16 Mj 7.3 主震在 58 s 完成初始 finite-fault inversion，初始结果 Mw 6.85、VR 80.8%。
  Evidence: Table 1 shows `REGARD1` elapsed time 00:58, Mw 6.85, VR 80.8%。

- REGARD 在约 5 分钟内收敛到 Mw 6.96、VR 96.2%。
  Evidence: Table 1 shows `REGARD4` at 04:50 and `REGARD final` at 05:43 with Mw 6.96 and VR 96.2%。

- 最终断层模型与 Yarai et al. (2016) 基于后处理 GNSS 和 InSAR 的模型、JMA CMT Mw 7.0 基本一致。
  Evidence: “Our final fault model estimate is in good agreement with the Mw estimates described above...”

- 主震造成近场显著同震位移，例如 site 0701 水平位移约 96 cm、site 0465 约 75 cm，与 GEONET F3 后处理结果约 98 cm 和 76 cm 接近。
  Evidence: lines describing “Large horizontal displacements of ~96 cm... and ~75 cm...” and post-processed values。

- 两次 M6 级前震虽然没有触发实时有限断层反演，但 REGARD 捕捉到了显著同震位移。
  Evidence: “significant coseismic displacements caused by the two foreshocks could be detected by the REGARD system.”

- 对 April 14 Mj 6.5 前震的模拟降低阈值测试显示，第一 finite-fault model 可在 38 s 得到，Mw 5.94，50 s 更新到 Mw 6.11，最终 1 min 32 s 收敛到 Mw 6.12，与 JMA CMT Mw 6.2 大致一致。
  Evidence: “For the April 14 event... first finite-fault model was derived at 38 s... updated to 6.11 at 50 s... converged with Mw 6.12 at 1 m 32 s.”

- April 15 Mj 6.4 模拟中，模型强依赖单个近场台站和先验参数，说明 M6 级事件稳定断层参数估计仍困难。
  Evidence: “the model strongly depended on the a priori parameters and the displacement at station 1071...”

## 9. Strengths

- 这是 REGARD 系统对真实地震的首次 operational result；
- 使用日本密集 GEONET 网络，实际应用价值强；
- 清楚展示了实时 GNSS finite-fault inversion 的时间尺度：约 1 分钟初估、约 5 分钟收敛；
- 同时分析主震和前震，对不同震级阈值很有启发；
- 将实时结果与后处理 GNSS/InSAR/JMA CMT 对比，验证了模型合理性；
- 对 inland intraplate earthquakes 的 GNSS-based EEW 有重要意义。

## 10. Limitations

- 对主震最终稳定到正确 fault plane 需要额外约 4 分钟，早期模型可能陷入 conjugate fault plane；
- 单矩形断层模型过于简单，难以表达复杂多段破裂；
- M6 级前震信噪比较低，finite-fault model 不稳定；
- real-time RTK positioning 存在 multipath、data delay、low elevation cutoff 和 ambiguity resolution 造成的 apparent offsets；
- 模型强依赖 a priori focal mechanism database 和 JMA EEW 初始信息；
- 对 station geometry 和近场台站数量敏感。

## 11. Relation to my research

```yaml
use_for_my_paper:
  introduction: true
  methods: true
  baseline: true
  discussion: true
  dataset: false
reason: "这篇论文是实时 GNSS finite-fault estimation 的代表案例，能为 HR-GNSS + deep learning 大震快速震源表征提供系统 baseline、评价指标和关键时间尺度。"
```

具体启发：

- 可作为 Introduction 中说明实时 GNSS 已能参与快速断层模型估计的证据；
- 可作为 Methods/Benchmark 中的传统 finite-fault inversion baseline；
- 可为 deep learning 模型设计输出参数提供参考，例如 Mw、fault length、width、slip、VR；
- 对讨论台站分布、近场台站、实时定位误差、先验依赖很有价值。

## 12. Useful citations or quotable ideas

- REGARD demonstrated real-time finite-fault estimation for the 2016 Kumamoto mainshock, obtaining an initial Mw 6.85 model within 1 min and converging to Mw 6.96 within 5 min.
- Real-time GNSS can detect significant coseismic displacements from M6-class inland earthquakes, but stable finite-fault modeling is difficult when near-field station SNR is low.
- More accurate a priori information such as rapid CMT solutions may improve inland earthquake modeling.

## 13. Open questions

- 如果用深度学习模型替代或辅助 REGARD inversion，能否在前 1 分钟内更稳定地区分 fault plane？
- 如何把 VR、station geometry、near-field coverage 和 SNR 作为模型输入或置信度指标？
- 对 M6–M7 内陆地震，HR-GNSS 的可检测阈值和最佳输出形式是什么：Mw、fault extent、还是 coseismic offset field？
- 多段破裂或复杂断层几何下，单矩形模型作为 baseline 是否会系统偏差？

## 14. Extracted structured tags

```yaml
domain:
  - GNSS
  - geodetic earthquake early warning
  - real-time source characterization
data_type:
  - 1Hz RTK-GNSS positions
  - coseismic displacement
  - post-processed GNSS
  - InSAR comparison
task:
  - real-time magnitude estimation
  - rapid finite-fault estimation
  - coseismic displacement detection
  - earthquake early warning
method:
  - REGARD
  - RTK-GNSS
  - RTKLIB
  - single rectangular fault inversion
  - Okada dislocation model
  - Newton optimization
input_window:
  - 38s
  - 58s
  - 1min
  - 5min
metrics:
  - Mw estimate
  - variance reduction
  - elapsed time
  - displacement discrepancy
  - fault geometry consistency
limitations:
  - a priori dependency
  - station geometry
  - low SNR for M6 events
  - ambiguity resolution error
  - single rectangular fault simplification
```

## 15. TODO: verify

- 回查 PDF 表 1，确认 REGARD final 的 elapsed time 是否应写作 05:43；
- 确认 site 0701 / 0465 位移方向和数值；
- 若用于论文引用，应核查 Yarai et al. (2016) 的具体模型细节；
- 后续应阅读 Kawamoto et al. (2017) REGARD 系统完整论文。
