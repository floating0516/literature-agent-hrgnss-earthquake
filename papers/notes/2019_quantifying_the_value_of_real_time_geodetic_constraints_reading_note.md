# Quantifying the Value of Real-Time Geodetic Constraints for Earthquake Early Warning Using a Global Seismic and Geodetic Data Set｜Reading Note

## 1. Metadata

- Title: Quantifying the Value of Real-Time Geodetic Constraints for Earthquake Early Warning Using a Global Seismic and Geodetic Data Set
- Authors: C. J. Ruhl, D. Melgar, A. I. Chung, R. Grapenthin, R. M. Allen
- Year: 2019
- Venue: Journal of Geophysical Research: Solid Earth
- DOI: 10.1029/2018JB016935
- URL / PDF: https://doi.org/10.1029/2018JB016935
- Local PDF: `papers/raw_pdf/2019_quantifying_the_value_of_real_time_geodetic_constraints.pdf`
- Parsed text: `papers/parsed_md/2019_quantifying_the_value_of_real_time_geodetic_constraints.md`
- Paper ID: 2019_quantifying_the_value_of_real_time_geodetic_constraints

## 2. One-sentence summary

这篇论文使用全球 32 个 Mw ≥ 6 地震的地震与 GNSS 数据，在模拟实时环境中系统比较 seismic-only ElarmS 与 seismically triggered G-larmS 的震级、地面运动和预警时间表现，定量证明实时大地测量有限断层约束能显著改善大震 EEW 的震级非饱和估计、MMI 预警覆盖和 cost savings performance。

## 3. Research problem

论文试图解决的问题是：实时 GNSS / geodetic EEW 算法是否能在实际大震预警场景中，为传统 seismic point-source EEW 系统提供定量可证明的增益，尤其是在大震震级饱和、有限断层效应和地面运动预测方面。

具体问题包括：

- seismic EEW 使用 P 波早期信息时，在大震中容易低估震级；
- 点源假设难以刻画大震破裂有限性，导致强震区地面运动估计不足；
- GNSS 静态位移能提供不饱和震级和有限断层约束，但以往由于大震样本稀少，难以证明其对 EEW 的实际价值；
- 需要从 end-user ground-motion warning 角度，而不仅是震级误差角度，评估 geodetic EEW 是否更有用。

## 4. Background and motivation

论文背景是 EEW 的最终目标并不是只给出震级和震中，而是对用户所在位置的强地面运动进行及时预警。ShakeAlert 一类系统通常用震源参数加 ground-motion model 生成预警，因此震源位置、震级和 fault finiteness 的误差会直接影响最终地面运动估计。

传统 seismic point-source EEW 依赖惯性地震仪记录的 P 波早期特征，但在大震中存在两个关键问题：

1. **震级饱和**：大震近场高频加速度饱和，且由加速度积分到位移会引入误差，因此难以可靠测量超低频和静态位移；
2. **网络几何限制**：out-of-network 或 edge-of-network 事件可能因台站方位覆盖不足而被严重误定位或低估震级。

GNSS 被视为 strong-motion displacement sensor，能够观测长周期至 0 Hz 的永久静态位移，因此可用于估计不饱和 moment magnitude 和有限断层滑动。论文选择 G-larmS 作为代表性 geodetic EEW 算法，并与 ElarmS 进行 end-to-end replay 比较，目标是量化 GNSS 对大震 EEW 的实际增益。

## 5. Data

论文使用全球 32 个 Mw 6.0–9.0 地震或情景事件的数据集。

- 数据类型：
  - seismic acceleration / velocity waveforms；
  - high-rate GNSS displacement waveforms；
  - real 和 synthetic seismic/geodetic data；
  - 用于 MMI 评估的 seismic station records。
- 事件数量：32 个 Mw ≥ 6 事件；其中 29/32 个事件有 seismic data；29/32 个事件同时有 seismic 与 geodetic records（real 或 synthetic）。
- 震级范围：Mw6.0 Parkfield 2004 至 Mw9.0 Tohoku-oki 2011。
- 构造类型：以 subduction megathrust events 为主，也包括 continental strike-slip、intraplate normal 和其他非俯冲带事件。
- 研究区域：全球，包括 Japan、Chile、United States、Mexico、Ecuador、New Zealand、Nepal、Costa Rica、Greece 等。
- seismic data：
  - 共使用 7,589 three-component seismic records；
  - 部分来自 ShakeAlert test suite，部分来自各国地震机构；
  - 数据格式化为 miniseed 和 Earthworm tank-player files，用于 simulated real-time replay；
  - sampling rates 因仪器和网络不同，ShakeAlert test suite 中为 40–200 sps。
- geodetic data：
  - 共使用 4,545 three-component geodetic records；
  - real earthquake GNSS 来自 Melgar and Ruhl (2018) open data set；
  - displacement waveforms 使用 Geng et al. (2013) precise point positioning 方法统一计算；
  - 大多数 GNSS records 为 1 sps，少数事件有 5 sps，之后重采样为 1 sps 供 G-larmS 使用。
- synthetic data：
  - Mw8.7 Cascadia001300 synthetic megathrust event；
  - Mw7.0 Hayward4Hz synthetic strike-slip event；
  - Mw6.9 Nisqually 2001 使用真实 seismic data 和 synthetic GNSS displacement；
  - synthetic displacement 读入时加入 horizontal ±2.5 cm、vertical ±4.0 cm random noise。
- 数据可复现信息：
  - geodetic data published by Melgar and Ruhl (2018)；
  - seismic data permanently stored at Zenodo `https://zenodo.org/record/1469833`；
  - archive 中每个 event 有 station metadata、velocity / acceleration miniseed data。
- 训练/验证/测试划分：Not specified in provided text；该论文是 replay-based algorithm evaluation，不是机器学习训练。

## 6. Method

论文方法是模拟实时 replay，对 seismic-only 与 coupled seismic-geodetic EEW 系统进行端到端比较。

### 6.1 Overall workflow

1. 将每个地震的 seismic data replay 到 ElarmS，模拟实时估计 origin time、location、magnitude；
2. 使用 ElarmS first alert 生成 ShakeAlert XML message，触发 G-larmS；
3. G-larmS 使用 GNSS position time series 逐 epoch 估计 static offsets，并反演有限断层 slip；
4. 将 ElarmS、ElarmS-triggered G-larmS、Perfectly triggered G-larmS 的解转化为 predicted PGA / PGV / MMI time series；
5. 将预测 MMI 与观测 MMI 在每个 station 上按 threshold crossing 进行比较；
6. 分类 TP / TN / FP / FN alerts，并计算 warning time 和 cost savings performance metric Q。

### 6.2 ElarmS seismic baseline

- 算法：ElarmS，ShakeAlert seismic point-source algorithm EPIC 的相关版本；
- 输入：seismic acceleration / velocity waveform replay；
- 输出：origin time、epicentral location、magnitude、number of stations 等 alert parameters；
- 深度假设：固定 depth 或一组 depths，本研究使用 8 km 和 20 km；
- 触发条件：至少 3 个台站，且每个台站至少 0.2 s data，并满足 region-specific spatial constraints；
- 震级估计：基于 P wave amplitudes 和到 estimated epicenter 的距离。

### 6.3 G-larmS geodetic finite-fault algorithm

- 输入：real-time GNSS positioning time series；ElarmS 或 perfect trigger 提供的 origin time、hypocenter / epicenter、initial magnitude；
- 输出：static offsets、distributed finite-fault slip、epoch-by-epoch magnitude evolution、subfault slip components、简化 fault geometry for GM prediction；
- 算法：G-larmS，实时分析 GNSS position time series，估计 coseismic static offsets，并进行 finite-fault least-squares slip inversion；
- fault geometry：
  - 使用 region-specific a priori geometries；
  - 线性 fault 根据 ShakeAlert hypocenter 居中，并按 Wells & Coppersmith (1994) scaling relationships 对称增长；
  - 可使用 known catalog faults，例如 UCERF3、Slab1.0；
  - 每个 epoch 选择 data misfit 最小的 geometry。
- replay 实现：
  - offline 中分为 Offset Estimator (OE) 和 Parameter Estimator (PE) 两步；
  - OE 估计并存储 static offsets；
  - PE 读取 offset logs 并进行 finite-fault slip inversion。
- offset estimation：
  - 使用 XML event message 决定每个台站 offset estimation start time；
  - configurable wave speed 采用 5.2 km/s；
  - pre-start mean displacement 从 post-start average displacement 中扣除以估计 static offsets。
- G-larmS magnitude：
  - 每个 epoch 基于整体 fault geometry 和 slip amount 计算 magnitude；
  - 使用 slip > 10% maximum slip 的 subfault patches 生成 surface-projected perimeter；
  - hypocenter 即使低于 10% maximum slip 也纳入 perimeter；
  - 该 perimeter 用于计算 ground-motion prediction 所需的 Rjb 和 RRup。

### 6.4 Triggering experiments

- ElarmS-triggered G-larmS：使用 ElarmS first alert 的 magnitude、epicentral location、origin time 构建 XML message；为避免不现实的 geodetic early solution，移除早于 ElarmS first alert + one epoch 的 G-larmS solutions。
- Perfectly triggered G-larmS：假定精确知道 origin time、location 和 catalog depth；initial magnitude 设为 M6.0；用于评估 simulated real-time trigger 对解的退化程度。

### 6.5 Ground-motion and alert classification

- 观测 MMI：将 seismic waveforms 转换为 PGA 和 PGV envelopes，三分量取最大，再用 Worden et al. (2012) 转为 instrumental MMI time series；
- 预测 GM：使用 Abrahamson et al. (ASK14, 2014) GMPE；
- site term：使用 USGS slope-based global VS30 database；
- 变化参数：Mw、RJB、fault width W；其他 GMPE 参数保持一致；
- MMI thresholds：MMI 3–7；重点讨论 MMI 3、4、5；
- alert classes：TP、TN、FP、FN；
- warning time：观测 MMI threshold crossing time 减去预测 threshold crossing time；positive WT 才算 TP；negative WT 归入 late / missed alerts。

## 7. Evaluation metrics

论文使用的主要评价指标包括：

- magnitude error：prediction minus observation；
- first alert magnitude error、30 s magnitude error、final / 180 s magnitude error；
- first alert time；
- predicted vs observed MMI time series；
- MMI threshold crossing；
- warning time (WT)；
- true positive (TP)、true negative (TN)、false positive (FP)、false negative (FN) alert classification；
- median WT；
- missed alert rate / FN proportion；
- false positive proportion；
- cost savings performance metric Q；
- ground-motion accuracy in MMI space；
- sensitivity to alerting threshold MMI 3 / 4 / 5。

## 8. Key results

- G-larmS 相比 ElarmS 显著降低大震震级饱和，尤其在 M > 7.5 后 ElarmS error 随震级增大而恶化，而 G-larmS error 对震级更稳定。  
  Evidence: “ElarmS magnitude saturation above M7.5, while magnitude errors for G-larmS are more stable with respect to increasing magnitude.”

- ElarmS first alert、30 s 和 final magnitude errors 分别为 −1.0 ± 1.0、−0.71 ± 0.75、−0.50 ± 0.83；ElarmS-triggered G-larmS 分别为 −0.62 ± 0.86、−0.26 ± 0.73、−0.14 ± 0.65。  
  Evidence: “ElarmS magnitude errors are −1.0 ± 1.0 ... −0.50 ± 0.83 ... ElarmS-Triggered G-larmS magnitude errors are −0.62 ± 0.86 ... −0.14 ± 0.65.”

- 到 origin time 后 30 s，G-larmS 平均改善震级误差约 0.5 magnitude units。  
  Evidence: “G-larmS provides an improvement of ~0.5 magnitude units, on average, by 30 s after origin time for all events.”

- ElarmS first alerts 平均更快，为 22 ± 13.7 s；ElarmS-triggered G-larmS first alerts 平均为 31 ± 20.5 s。  
  Evidence: “Mean first alert times for ElarmS and ElarmS-Triggered G-larmS are 22 ± 13.7 s ... and 31 ± 20.5 s.”

- 使用 MMI 4 threshold，在全部 5,151 个 stations 中，ElarmS TP 为 10.4%，G-larmS TP 为 39.9%。  
  Evidence: “Using an alerting threshold of MMI 4, out of a total of 5,151 stations, ElarmS produced 10.4% TPs while ElarmS-Triggered G-larmS resulted in 39.9% TPs.”

- 对实际经历 MMI > 4 的 3,917 个 sites，ElarmS 只成功预警 536 个，即 13.7%；G-larmS 成功预警 2,055 个，即 52.3%。  
  Evidence: “Of the 3,917 sites that actually experienced shaking exceeding MMI 4, ElarmS alerted only 536 (13.7%), while G-larmS successfully alerted 2,055 (52.3%).”

- MMI 4 下，missed alerts 从 ElarmS 的 48.7% 降至 G-larmS 的 19.2%，但 false positives 从 1.2% 增至 13.4%。  
  Evidence: “missed alerts (FN), from 48.7% with ElarmS to 19.2% with G-larmS... FP alerts increase from 1.2% ... to 13.4%.”

- MMI 4 下，ElarmS median WT 为 18.9 ± 19.7 s；G-larmS median WT 为 55.8 ± 46.3 s，超过 ElarmS 的两倍。  
  Evidence: “ElarmS has a median WT of 18.9 ± 19.7 s. With G-larmS alerts, median WT increased to 55.8 ± 46.3 s.”

- G-larmS 的 warning time 对 MMI threshold 选择不如 ElarmS 敏感：MMI 4 为 55.8 s，MMI 3 和 5 分别为 52.4 s 和 54.4 s。  
  Evidence: “G-larmS results do not show the same relationship to MMI threshold choice: median WTs decrease from 55.8 s with a threshold of MMI 4 to 52.4 and 54.4 s when using thresholds of MMI 3 and 5.”

- cost savings performance Q 显示 geodetic solutions 对多种 cost ratio 用户具有更高价值，特别是 false alert tolerance 较低的用户；cost ratio 为 10 时，geodetic solutions 在 MMI 3–5 均为正。  
  Evidence: “geodetic solutions provide a higher cost savings value... particularly for less false alert tolerant users” and “positive for all MMIs between 3 and 5 using a cost ratio of 10.”

## 9. Strengths

- 使用全球 32 个 Mw ≥ 6 事件，是较大规模的 joint seismic-geodetic EEW replay benchmark；
- 同时评估 source magnitude accuracy 和 end-user ground-motion warning performance，而不是只比较震级误差；
- 将 geodetic EEW 的价值量化为 TP/TN/FP/FN、WT 和 cost savings metric Q，便于与用户行为和预警收益联系；
- 使用同一套 station/site 数据比较 ElarmS 与 G-larmS，使算法差异更可解释；
- 明确展示 GNSS 对大震震级饱和和有限断层效应的改善；
- 提供数据可复现信息，便于其他 geodetic / seismic EEW 算法开发者进行类似评估；
- 对 ShakeAlert 中 coupled seismic-geodetic architecture 的必要性给出强定量证据。

## 10. Limitations

- 只测试一个候选 geodetic finite-fault algorithm：G-larmS；BEFORES、G-FAST 等算法没有在同一框架中直接比较；
- 数据集只包含 M > 6 事件，因此统计结果可能只适用于较大震级和强地面运动场景；
- 不同事件的台站分布、距离范围和数据完整性不均匀，Q metric 的绝对值受数据集采样影响；
- GM estimates 使用 GMPE，source complexity 和 GM prediction uncertainty 会导致 false alerts 仍然存在；
- real-time timing 未包含数据传输和 issuing alert 的完整延迟，不过作者认为这些延迟通常较短；
- offline replay 中 G-larmS 分为 OE 和 PE 两步，不完全等同实时系统的同时估计实现；
- synthetic scenarios 和部分 synthetic GNSS data 可能与真实实时 GNSS 噪声和故障模式存在差异；
- 论文指出改进可能更多来自 fault finiteness 而不只是更准确的 moment magnitude，仍需进一步验证。

## 11. Relation to my research

```yaml
use_for_my_paper:
  introduction: true
  methods: true
  baseline: true
  discussion: true
  dataset: true
reason: "这篇论文是 HR-GNSS / geodetic EEW 相对于 seismic-only EEW 的关键定量证据，提供全球大震 benchmark、ElarmS 与 G-larmS baseline、MMI/WT/TP-FP-FN 评价框架，以及 GNSS 解决大震震级饱和和有限断层约束的直接论据。"
```

具体启发：

- 可作为 Introduction 中论证“seismic-only EEW 在大震中存在 magnitude saturation，GNSS static displacement 可提供不饱和约束”的核心引用；
- 可作为 Method / Baseline 中传统 coupled seismic-geodetic 系统的代表：ElarmS + G-larmS；
- 可为 deep learning HR-GNSS 大震快速震源表征设计评价指标：Mw error、30 s error、MMI threshold alerts、WT、TP/FN/FP、cost savings Q；
- 可作为 dataset 线索：Melgar and Ruhl (2018) GNSS data、Zenodo seismic data、32-event global benchmark；
- 对 Discussion 中比较深度学习模型与传统 finite-fault geodetic inversion 的优缺点很有价值；
- 对 SRL 短论文写作也有直接参考：结果表达清晰，将算法误差转化为用户侧预警收益。

## 12. Useful citations or quotable ideas

- GNSS 可被概念化为 strong-motion displacement sensors，能够测量最长周期直到 0 Hz 的 static / permanent offset。该观点来自 Introduction 中对 GNSS geodetic measurements 的描述。
- seismic point-source EEW 在大震中会发生 magnitude saturation，导致强地面运动区域被低估。该观点来自 Introduction 和 Tohoku-Oki 案例讨论。
- geodetic finite-fault algorithms 虽然 first alert 平均慢于 seismic algorithms，但能为大震提供更准确的 magnitude、slip distribution 和 ground-motion prediction。该观点来自 Results / Discussion。
- EEW 应被视为 ground-motion warning system，算法评价应在 station-level MMI threshold 和 warning time 空间中进行，而不仅是震源参数误差。该观点来自 Methods 3.3。
- coupled seismic-geodetic approach 能结合 seismic data 的早期短 WT 与 geodetic data 对远场强震区的长 WT、较准确预测。该观点来自 Discussion。

## 13. Open questions

- 如果用 deep learning 从 HR-GNSS waveforms / offsets 直接预测 Mw、finite fault 或 station-level MMI，能否比 G-larmS 更早达到同等 TP/FN 表现？
- 如何把 G-larmS 的有限断层输出作为 deep learning baseline 或 teacher model？
- 论文中 Q metric 对不同用户 cost ratio 很有意义，但实际用户的 cost ratio 如何估计？
- 对 M6–M7 中等事件，GNSS 初始解较慢且噪声较高，deep learning 是否能改善 early signal detectability？
- GNSS 的 false positive 增加是否能通过不确定性估计、Bayesian alerting 或多源数据融合降低？
- 改进主要来自 fault finiteness 还是 magnitude accuracy？后续实验应如何区分二者贡献？

## 14. Extracted structured tags

```yaml
domain:
  - GNSS
  - HR-GNSS
  - geodetic earthquake early warning
  - seismic earthquake early warning
  - ground-motion warning
  - rapid source characterization
data_type:
  - high-rate GNSS displacement
  - seismic acceleration waveform
  - seismic velocity waveform
  - synthetic displacement
  - synthetic seismic waveform
  - instrumental MMI time series
task:
  - earthquake early warning evaluation
  - magnitude estimation
  - finite-fault slip inversion
  - ground-motion prediction
  - station-level alert classification
  - warning time estimation
method:
  - ElarmS
  - G-larmS
  - GNSS static offset estimation
  - finite-fault inversion
  - MMI threshold approach
  - ASK14 GMPE
  - cost savings performance metric Q
input_window:
  - first alert
  - 30s
  - 180s
  - 1Hz GNSS
metrics:
  - magnitude error
  - first alert time
  - warning time
  - MMI threshold crossing
  - true positive
  - true negative
  - false positive
  - false negative
  - cost savings performance Q
limitations:
  - only M > 6 events
  - one geodetic algorithm tested
  - uneven station sampling
  - GMPE uncertainty
  - synthetic data limitations
  - offline replay simplification
  - increased false positives
```

## 15. TODO: verify

- 回查原 PDF 和 supporting information，确认 Table S1、S2、S3 中各事件逐项数值；
- 确认 Zenodo seismic dataset 链接 `https://zenodo.org/record/1469833` 是否仍可访问；
- 回查 Melgar and Ruhl (2018) geodetic open data set 的具体 DOI / 下载路径；
- 确认 corrected on 30 DEC 2020 后，在线版本是否对表格或数值有修改；
- 如果用于论文引用，需核查 Figure 3、Figure 7、Figure 8、Figure 10 的图号、caption 和页码；
- 需要进一步阅读 supporting information 中 Perfectly Triggered G-larmS 的详细比较。 
