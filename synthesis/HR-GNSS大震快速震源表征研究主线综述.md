# HR-GNSS大震快速震源表征研究主线｜Literature Synthesis

> 本综述基于 6 篇 reading notes 与既有 synthesis 文档生成。写作原则是跨文献综合，而不是逐篇复述。文中将尽量区分：
>
> - **文献直接结论**：reading notes 中明确记录的论文结论或定量结果；
> - **跨文献归纳**：多篇文献共同支持、互补或形成的综合判断；
> - **研究启发**：面向 HR-GNSS + 大震快速震源表征 / deep learning / SRL 短论文的可操作思路。
>
> 不确定或需要回查原文页码、图号、正式版本的信息标注为 `TODO: verify`。

---

## 1. Executive summary

**文献直接结论。** 现有材料共同表明，HR-GNSS / real-time GNSS 在大震快速震源表征中的核心价值，是提供不易发生大震震级饱和的位移约束，尤其是 PGD、静态同震位移和有限断层反演所需的长周期至 0 Hz 信息。Crowell et al. (2016) 展示了 G-FAST 可在 seismic trigger 后用 GNSS 位移产生 PGD magnitude、CMT 和 finite-fault slip 输出；Kawamoto et al. (2016) 报告 REGARD 在 2016 Kumamoto 主震中约 58 s 给出初始有限断层模型、约 5 min 收敛；Melgar et al. (2019) 量化 Ridgecrest 真实端到端实时 HR-GNSS 位移质量与低延迟；Gao et al. (2021) 说明 Maduo Mw 7.3 地震中 PGD / PGV scaling 可得到接近 USGS Mw 7.3 的震级；Ruhl et al. (2019) 进一步从全球 32 个 Mw ≥ 6 事件 replay 证明 geodetic finite-fault constraints 可减轻 seismic-only EEW 的大震震级饱和，并改善 MMI 预警覆盖与 warning time；Mousavi & Beroza (2020 / TODO: verify) 虽非 GNSS 论文，但提供了 Bayesian deep learning、不确定性估计和少台观测快速震源表征的可迁移方法思路。

**跨文献归纳。** 这些论文形成了一条清晰研究主线：从“GNSS 为什么能补 seismic EEW 的短板”，到“实时 GNSS 如何进入 PGD / CMT / finite-fault 系统”，再到“真实端到端数据的误差、延迟和台站限制是什么”，最后走向“如何把 GNSS 位移、台站几何、缺测、时间窗和不确定性纳入下一代快速震源表征模型”。该主线说明，HR-GNSS 的优势不是单纯更早，而是在大震、中远场和强震区预测中提供更稳定的震级、有限断层和静态位移约束；其限制则集中在近场台站覆盖、垂向噪声、实时定位误差、台站 dropout、断层面非唯一性、先验依赖和真实 benchmark 不足。

**研究启发。** 如果面向 HR-GNSS 大震快速震源表征设计新方法，最有价值的切入点不是简单替代 PGD scaling，而是构建一个能处理多时间窗、多台站不规则输入、台站几何、实时噪声和不确定性的模型。深度学习模型需要与 PGD / PGV scaling、G-FAST、REGARD、G-larmS 等传统 baseline 对比，并在 10–15–20–30–60 s 等真实预警时间窗下报告 Mw error、finite-fault 参数误差、VR / misfit、MMI warning performance、dropout robustness 和 uncertainty calibration。

---

## 2. Main research lines

### 2.1 GNSS 作为大震非饱和震级约束

- **代表论文**：Crowell et al. (2016), Gao et al. (2021), Ruhl et al. (2019)。
- **文献直接结论**：
  - Crowell et al. (2016) 指出 seismic EEW 在 `M > 7` 时可能震级饱和，GNSS/geodetic observations 可提供额外非饱和约束；其 PGD magnitude 在约 30 s 后稳定到 Mw 6.7 ± 0.3，接近 Nisqually Mw 6.8。
  - Gao et al. (2021) 对 Maduo Mw 7.3 地震使用 55 个 1 Hz GNSS 台站，PGD 和 PGV 方法分别得到 Mw 7.25 和 Mw 7.31。
  - Ruhl et al. (2019) 显示 ElarmS 在 M > 7.5 后 magnitude error 随震级增大而恶化，而 G-larmS 的误差对震级更稳定；30 s 时 G-larmS 平均改善震级误差约 0.5 magnitude units。
- **跨文献归纳**：PGD / PGV / 静态位移构成 HR-GNSS 大震快速震级估计的最低层 baseline；它们不是最终源模型，但为后续 CMT、finite-fault 或神经网络提供强约束和可解释中间量。
- **适用场景**：Mw 6+ 尤其 Mw 7+ 事件；seismic-only 可能饱和或低估的场景；需要快速 Mw 的 EEW / hazard response。
- **局限**：PGD / PGV scaling 依赖经验系数、震源距、台站数量和区域适用性；单台站结果受 site effects、radiation pattern、垂向噪声影响；远场和稀疏台站会延迟收敛。

### 2.2 实时 GNSS 系统化反演：PGD → CMT → finite-fault

- **代表论文**：Crowell et al. (2016), Kawamoto et al. (2016), Ruhl et al. (2019)。
- **文献直接结论**：
  - G-FAST 包含 PGD magnitude/depth、CMT inversion、finite-fault slip inversion 三层输出；CMT 在考虑 latency 后约 43 s 可用、约 50 s 稳定。
  - REGARD 使用 GEONET 1 Hz RTK-GNSS，在 Kumamoto 主震中 58 s 得到初始 Mw 6.85、VR 80.8% 的有限断层模型，约 5 min 收敛到 Mw 6.96、VR 96.2%。
  - G-larmS 在全球 replay 中使用 GNSS offsets 与有限断层反演，相比 seismic-only ElarmS 改善大震震级和 ground-motion warning performance。
- **跨文献归纳**：传统实时 geodetic source characterization 通常是层级式流程：seismic trigger 提供 origin time / location / initial magnitude，GNSS 位移提供 PGD 和 offsets，再进入 CMT 或 finite-fault inversion。震级估计可在 15–30 s 尺度可用，更高维的机制、断层面和滑动分布通常需要 40–60 s 或更长。
- **适用场景**：已有 seismic trigger、台站覆盖较好、需要 fault extent / slip / MMI 预测的 operational EEW。
- **局限**：依赖先验断层几何或机制；fault-plane ambiguity 明显；单矩形断层难表示复杂破裂；近场台站和 station geometry 对结果影响大。

### 2.3 真实实时 HR-GNSS 数据质量、延迟和输入误差

- **代表论文**：Melgar et al. (2019), Kawamoto et al. (2016), Crowell et al. (2016)。
- **文献直接结论**：
  - Melgar et al. (2019) 对 Ridgecrest 端到端实时 HR-GNSS 表明：real-time vs post-processed PGD 差异标准差约 6.5 cm；horizontal-only PGD 差异标准差约 4.1 cm；coseismic offset 差异标准差约 4.3 cm；1 Hz vs 5 Hz PGD 差异标准差约 0.83 cm；平均 latency 约 1.4 s。
  - Crowell et al. (2016) 在 latency、noise、dropout 模拟中发现 PGD 约 30 s 后趋于稳定，其中 dropout 影响最大。
  - Kawamoto et al. (2016) 指出 real-time RTK positioning 可能受 multipath、data delay、low elevation cutoff 和 ambiguity resolution 影响。
- **跨文献归纳**：HR-GNSS 的数据传输/定位 latency 本身可低至秒级，但有效震源表征时间由信号到达、近场台站数量、offset 稳定性、噪声和模型复杂度共同决定。真实输入误差不能被忽略，应进入训练扰动、质量控制和 uncertainty 模块。
- **适用场景**：设计模型输入、噪声增强、实时质量控制、采样率选择。
- **局限**：Ridgecrest 分析中只有 9 个有明显信号的实时台站；不同构造环境、Mw 8–9 巨震和多台网条件下误差分布仍需验证。

### 2.4 从震源参数误差到用户侧预警收益

- **代表论文**：Ruhl et al. (2019)。
- **文献直接结论**：
  - 在 MMI 4 threshold 下，ElarmS 在 5,151 个 stations 中 TP 为 10.4%，ElarmS-triggered G-larmS TP 为 39.9%。
  - 对实际经历 MMI > 4 的 3,917 个 sites，ElarmS 成功预警 13.7%，G-larmS 成功预警 52.3%。
  - MMI 4 下 missed alerts 从 48.7% 降至 19.2%，但 false positives 从 1.2% 增至 13.4%。
  - Median WT 从 ElarmS 的 18.9 ± 19.7 s 增至 G-larmS 的 55.8 ± 46.3 s。
- **跨文献归纳**：大震快速震源表征的评价不应停在 Mw error 或 VR，而应扩展到 ground-motion warning：哪些站点/用户被提前预警、漏报和误报如何权衡、warning time 是否足够行动。
- **适用场景**：面向 EEW 系统、SRL 短论文的实验评价框架、与用户价值相关的 discussion。
- **局限**：目前在给定材料中，只有 Ruhl et al. (2019) 系统做了 MMI / TP / FP / FN / Q 评价；其他 HR-GNSS 案例多停留在震级、位移或有限断层 fit。

### 2.5 Bayesian / deep learning 快速震源表征与不确定性

- **代表论文**：Mousavi & Beroza (2020 / TODO: verify), 以及上述 GNSS 文献提供的 baseline 与数据约束。
- **文献直接结论**：
  - Mousavi & Beroza 使用 Bayesian deep learning 从单台三分量地震波形估计震中距、P 走时和反方位角，并给出 epistemic / aleatory uncertainty；测试集中 epicenter、origin time、depth mean errors 分别为 7.3 km、0.4 s、6.7 km。
  - 其结果显示 estimated uncertainties 与 prediction errors 有正相关，aleatory uncertainty 对部分任务更能反映误差。
- **跨文献归纳**：虽然该论文不是 GNSS 研究，但它补足了“下一代方法”维度：HR-GNSS 模型不应只输出 Mw 或断层参数点估计，而应输出 uncertainty / confidence，尤其在台站稀疏、dropout、fault-plane ambiguity 和早期时间窗下。
- **适用场景**：少台站 GNSS 早期窗口、Bayesian uncertainty、multi-task learning、geometry-aware 输出。
- **局限**：输入为 seismic waveform 而非 GNSS 位移；数据为 STEAD 高 SNR 近震波形，不可直接作为 HR-GNSS benchmark。

---

## 3. Method comparison table

| Method / line | Representative papers | Input data | Output | Strengths | Limitations | Relevance to my research |
|---|---|---|---|---|---|---|
| PGD scaling | Crowell et al. (2016); Gao et al. (2021); Ruhl et al. (2019) | 多台站 HR-GNSS 位移、PGD、hypocentral distance | Mw、depth / magnitude evolution | 快速、可解释、非饱和，适合 EEW baseline | 经验系数依赖区域和震级范围；受台站几何、site effects、垂向噪声影响 | 必选传统 baseline；可作为 DL 输入特征和中间监督 |
| PGV scaling / variometric velocity | Gao et al. (2021) | 1 Hz GNSS velocity time series、PGV、距离 | Mw evolution、最终 Mw | 可使用广播星历，实时性潜力高；Maduo 最终 Mw 接近 USGS | 台站间波动比 PGD 更大；需更多台站稳定；速度积分误差和区域 scaling 待验证 | 可作为 PGD 互补特征；适合比较位移 vs 速度输入 |
| G-FAST PGD + CMT + finite-fault | Crowell et al. (2016) | seismic trigger + synthetic high-rate GPS displacement / static offsets | Mw、depth、CMT、finite-fault slip | 系统框架完整；明确多层输出和时间尺度；测试 latency/noise/dropout | Nisqually 测试主要为合成位移；fault-plane ambiguity；依赖 seismic trigger | 可作为系统 baseline 与模型输出层级参考 |
| REGARD single rectangular fault inversion | Kawamoto et al. (2016) | GEONET 1 Hz RTK-GNSS positions；JMA EEW / displacement trigger；先验机制 | Mw、fault geometry、slip、VR | 真实 operational 案例；约 1 min 初估、约 5 min 收敛 | 单矩形简化；先验依赖；M6 级低 SNR；早期断层面不稳定 | 可作为 finite-fault benchmark 与先验依赖讨论依据 |
| G-larmS finite-fault EEW replay | Ruhl et al. (2019) | 全球 seismic + high-rate GNSS replay；ElarmS trigger；static offsets | Mw、finite-fault slip、MMI prediction、TP/FN/FP、WT、Q | 大样本全球 benchmark；从震源参数扩展到用户侧预警收益 | 只测试一个 geodetic algorithm；部分 synthetic；offline replay 简化；FP 增加 | 最适合作为 evaluation framework 和 coupled seismic-geodetic baseline |
| Real-time HR-GNSS performance assessment | Melgar et al. (2019) | Fastlane real-time 1 Hz GNSS；post-processed 1/5 Hz PPP | waveform / spectrum / PGD / offset / latency errors | 量化真实端到端输入误差和 latency | 非完整震源反演；台站样本少；preprint 版本需确认 | 为噪声模型、采样率、horizontal-only 特征提供依据 |
| Bayesian deep learning single-station source characterization | Mousavi & Beroza (2020 / TODO: verify) | STEAD 1 min 三分量 seismic waveform；P/S indicator | distance、P travel time、back-azimuth、location、origin time、depth、uncertainty | 输出不确定性；少台观测；轻量模型；multi-task 思路 | 非 GNSS；高 SNR 筛选；大震样本少；back-azimuth uncertainty 大 | 可迁移到 GNSS 的 uncertainty head、少台站鲁棒性和中间任务设计 |

---

## 4. Data and benchmark summary

| Paper | Data type | Region/events | Real/synthetic | Train/test split | Availability | Notes |
|---|---|---|---|---|---|---|
| Crowell et al. (2016) | synthetic high-rate GPS displacement；strong-motion-derived simulation；static offsets | 2001 Mw 6.8 Nisqually, Cascadia / Puget Sound | GNSS displacement 主要为 synthetic；使用真实强震记录和有限 GPS 参考 | Not applicable | Local PDF / parsed note；原数据可复现性需回查 | 26 个强震台站位置生成 synthetic displacement；每种扰动 1000 trials |
| Kawamoto et al. (2016) | GEONET 1 Hz RTK-GNSS positions；post-processed GNSS / InSAR comparison | 2016 Kumamoto Mj 6.5、Mj 6.4、Mj 7.3 | 真实 operational GNSS | Not applicable | GEONET 数据可用性需按日本机构规则确认；reading note 未给完整下载流程 | 真实系统案例；>1300 GEONET 台站，反演每次降采样至 200 站 |
| Melgar et al. (2019) | real-time 1 Hz GNSS；post-processed 1 Hz / 5 Hz PPP；PGD / offsets | 2019 Ridgecrest M6.4 / M7.1 | 真实端到端实时 + 后处理对比 | Not applicable | Note 记录 Zenodo miniSEED、UNAVCO offsets / RINEX；TODO: verify 正式版本与链接 | 约 700 NOTA 台站实时定位，分析 9 个有明显信号台站 |
| Gao et al. (2021) | 1 Hz high-rate GNSS displacement；velocity；PGD / PGV | 2021 Mw 7.3 Maduo, Qinghai / Tibetan Plateau | 真实 GNSS | Not applicable | 数据由 CENC、QHCORS / CMONOC 提供；公开下载入口不明确 | 55 个连续台站，均在 550 km 内；多数远场且分布不均 |
| Ruhl et al. (2019) | 全球 seismic acceleration / velocity；high-rate GNSS displacement；MMI time series；部分 synthetic | 32 个 Mw 6.0–9.0 全球事件/情景 | real + synthetic | Not applicable | seismic data at Zenodo；geodetic data from Melgar and Ruhl (2018) open data set；TODO: verify DOI | 7,589 seismic records；4,545 geodetic records；EEW replay benchmark |
| Mousavi & Beroza (2020 / TODO: verify) | STEAD 3-component seismic waveform；P/S indicator；labels | Global STEAD, epicentral distance <110 km, SNR ≥25 dB | 真实 seismic waveform | 80% train / 20% test | STEAD 引用；代码仓库和下载链接需回查 | 非 GNSS；约 150,000 waveforms；用于 DL uncertainty 方法借鉴 |

**跨文献归纳。** 当前材料中的 benchmark 可分为三类：

1. **系统/算法 replay benchmark**：Crowell et al. (2016)、Ruhl et al. (2019)。适合比较算法输出随时间演化和鲁棒性。
2. **真实 operational case study**：Kawamoto et al. (2016)、Melgar et al. (2019)、Gao et al. (2021)。适合提取误差水平、延迟、台站分布和区域适用性。
3. **深度学习方法 benchmark**：Mousavi & Beroza (2020 / TODO: verify)。非 GNSS，但适合迁移 uncertainty evaluation 和少台站设计。

**研究启发。** 如果构建 HR-GNSS deep learning benchmark，应优先整合 Ruhl et al. (2019) 的全球 geodetic / seismic 数据线索、Melgar et al. (2019) 的真实实时误差量化、Gao et al. (2021) 的区域 Mw 7+ 案例，并补充更多 Mw 8–9 俯冲带真实/合成场景。

---

## 5. Evaluation metrics

### 5.1 震源参数类

- **Mw error / absolute deviation**：评估快速震级是否接近 catalog / USGS / CMT。Crowell et al. (2016)、Gao et al. (2021)、Ruhl et al. (2019) 均使用或报告震级误差。
- **Magnitude evolution over time**：评估 first alert、30 s、final / 180 s 等时间点的震级收敛。Ruhl et al. (2019) 明确报告 first alert、30 s 和 final magnitude errors。
- **Depth / CMT parameter errors**：评估更高维震源参数。Crowell et al. (2016) 报告 CMT magnitude、depth、strike、dip、rake 的误差随时间下降。
- **Fault geometry consistency**：评估断层面、fault length / width / slip 是否与后处理 GNSS/InSAR/CMT 一致。Kawamoto et al. (2016) 使用后处理 GNSS/InSAR 和 JMA CMT 比较。

### 5.2 位移与数据质量类

- **PGD difference / standard deviation**：实时与后处理 PGD 差异，适合评估输入误差。Melgar et al. (2019) 报告三分量 PGD std 约 6.5 cm，horizontal-only 约 4.1 cm。
- **Coseismic offset difference**：评估静态位移可用于 finite-fault inversion 的可靠性。Melgar et al. (2019) 报告 offset std 约 4.3 cm。
- **Spectral bias / waveform agreement**：评估实时波形频域质量。Melgar et al. (2019) 发现 4–30 s period 为较好频段。
- **Latency**：评估数据流是否能满足实时预警。Melgar et al. (2019) 平均 latency 约 1.4 s。

### 5.3 反演质量与鲁棒性类

- **Variance reduction, VR**：传统反演系统常用 fit 指标。Kawamoto et al. (2016) 初始 VR 80.8%，最终 VR 96.2%。
- **Dropout / noise / latency sensitivity**：Crowell et al. (2016) 系统测试 latency、noise、dropout，发现 dropout 影响最大。
- **Station-number sensitivity**：Gao et al. (2021) 显示 PGD 约 8 个台站可稳定，PGV 需要 >15 个台站；4 站条件下容易低估。
- **Station geometry / near-field coverage**：多篇文献共同指出其重要性，但量化指标仍不足。可设计 azimuthal gap、nearest-station distance、near-field station count、mask ratio 等指标。

### 5.4 预警用户收益类

- **MMI threshold crossing**：将震源估计转化为用户侧地面运动预警。Ruhl et al. (2019) 使用 MMI 3–7，重点讨论 MMI 3、4、5。
- **TP / TN / FP / FN**：评估预警分类质量。Ruhl et al. (2019) 显示 G-larmS 降低 FN 但增加 FP。
- **Warning time, WT**：评估预警提前量。Ruhl et al. (2019) 在 MMI 4 下 G-larmS median WT 55.8 ± 46.3 s。
- **Cost savings performance metric Q**：将算法表现映射到用户成本收益。当前材料中主要由 Ruhl et al. (2019) 使用。

### 5.5 深度学习不确定性类

- **Prediction interval / uncertainty-error correlation**：Mousavi & Beroza (2020 / TODO: verify) 用于评估 Bayesian uncertainty 是否反映误差。
- **Calibration metrics**：给定材料未明确报告 GNSS deep learning calibration；后续应加入 reliability diagram、negative log-likelihood、expected calibration error、coverage probability 等。TODO: verify 可参考地震 Bayesian DL 文献。

---

## 6. Agreements across papers

- **Agreement 1：GNSS / HR-GNSS 能缓解大震震级饱和问题。**  
  Supporting papers: Crowell et al. (2016), Gao et al. (2021), Ruhl et al. (2019), Melgar et al. (2019)。  
  **性质**：文献直接结论 + 跨文献归纳。Crowell 和 Ruhl 明确讨论 seismic EEW 饱和；Gao 的 Maduo 案例给出 Mw 7.3 下 PGD/PGV 成功估计；Melgar 提供真实 HR-GNSS 数据质量支撑。

- **Agreement 2：PGD 是最稳固、最可解释的快速震级中间量。**  
  Supporting papers: Crowell et al. (2016), Melgar et al. (2019), Gao et al. (2021)。  
  **性质**：跨文献归纳。PGD 同时出现在系统 baseline、数据质量评估和区域案例中；Gao 显示 PGD 比 PGV 更稳定，Melgar 显示 horizontal-only PGD 更稳。

- **Agreement 3：更复杂的源参数需要更长时间窗和更多先验/台站约束。**  
  Supporting papers: Crowell et al. (2016), Kawamoto et al. (2016), Ruhl et al. (2019)。  
  **性质**：跨文献归纳。PGD 可在 15–30 s 可用；CMT / finite-fault 往往需要约 40–60 s 或数分钟收敛。

- **Agreement 4：台站几何、近场覆盖和 dropout 是关键限制。**  
  Supporting papers: Crowell et al. (2016), Kawamoto et al. (2016), Melgar et al. (2019), Gao et al. (2021), Ruhl et al. (2019)。  
  **性质**：跨文献归纳。不同论文从 dropout、近场台站、远场台站、台站样本和全球事件不均匀性角度反复指向同一问题。

- **Agreement 5：真实数据质量与实时误差必须进入模型设计。**  
  Supporting papers: Melgar et al. (2019), Kawamoto et al. (2016), Crowell et al. (2016)。  
  **性质**：文献直接结论 + 研究启发。Melgar 量化实时误差；Kawamoto 讨论 RTK 误差源；Crowell 通过模拟测试 noise / latency / dropout。

- **Agreement 6：仅报告震级误差不足，应连接到 warning time 和 ground-motion performance。**  
  Supporting papers: Ruhl et al. (2019)；其他论文间接支持。  
  **性质**：主要是 Ruhl 的文献直接结论，扩展为跨文献研究启发。

- **Agreement 7：不确定性估计是下一代快速表征模型的必要组成。**  
  Supporting papers: Mousavi & Beroza (2020 / TODO: verify), Ruhl et al. (2019), Crowell et al. (2016), Kawamoto et al. (2016)。  
  **性质**：研究启发。Mousavi & Beroza 直接提供 Bayesian DL uncertainty；GNSS 文献中的 fault-plane ambiguity、FP 增加、VR 和噪声问题说明点估计不够。

---

## 7. Disagreements or unresolved debates

1. **PGD 与 PGV 哪个更适合作为早期震级特征？**  
   - **文献直接结论**：Gao et al. (2021) 中 PGV 最终 Mw 7.31 更接近 USGS Mw 7.3，但 PGD 更稳定、台站需求更少；PGV 台站间范围更大。
   - **未解问题**：PGV 的不稳定是速度估计噪声、区域传播效应、site effects，还是 scaling law 不适配？不同区域和震级下是否一致？

2. **1 Hz 是否足够？**  
   - **文献直接结论**：Melgar et al. (2019) 对 Ridgecrest 发现 1 Hz vs 5 Hz PGD 差异 std 仅 0.83 cm，支持 1 Hz 对该 PGD 应用基本够用。
   - **未解问题**：对更近场、更大震级、更复杂破裂或需要 rupture evolution 的任务，1 Hz 是否仍足够？Gao et al. (2021) 也指出 GNSS 采样率低于强震仪，可能损失高频信息。

3. **geodetic EEW 的收益来自更准确 Mw，还是来自有限断层 finiteness？**  
   - **文献直接结论**：Ruhl et al. (2019) 指出 geodetic solutions 改善 ground-motion warning，但也提到改进可能更多来自 fault finiteness 而不只是 moment magnitude，仍需进一步验证。
   - **未解问题**：后续实验应分离 Mw accuracy、fault geometry 和 slip distribution 对 MMI / WT 的贡献。

4. **先验断层几何是帮助还是限制？**  
   - **文献直接结论**：REGARD 和 G-larmS 都使用先验机制、区域断层几何或 scaling relationships；Kawamoto et al. (2016) 显示早期 fault plane 可能不稳定，M6 事件强依赖先验。
   - **未解问题**：深度学习是否能降低先验依赖，还是会在训练数据中隐式学习同样的区域偏见？

5. **false positives 增加是否可接受？**  
   - **文献直接结论**：Ruhl et al. (2019) 中 G-larmS 降低 missed alerts，但 MMI 4 下 FP 从 1.2% 增至 13.4%。
   - **未解问题**：不同用户 cost ratio 下如何设定阈值？是否可通过 uncertainty calibration / Bayesian alerting 降低 FP？

6. **深度学习在 HR-GNSS 中的增益来自哪里？**  
   - **文献直接结论**：给定 GNSS 文献主要是传统 scaling / inversion；Mousavi & Beroza 提供 seismic DL uncertainty 思路，但非 GNSS。
   - **未解问题**：DL 能否在同等时间窗下显著优于 PGD / G-larmS？若不能，是否至少能提供更好的 uncertainty、fault-plane probability、dropout robustness 或快速 surrogate inversion？证据不足，需要继续查文献。

---

## 8. Research gaps

### 8.1 HR-GNSS 大震快速震源表征

- 当前材料充分覆盖 PGD、CMT、finite-fault 和 operational case，但缺少统一、多事件、多区域的 HR-GNSS 快速震源表征 benchmark，尤其缺少同一框架下比较 PGD / PGV / G-FAST / REGARD / G-larmS / deep learning 的实验。
- Mw 8–9 巨大俯冲带事件的真实实时 HR-GNSS 样本仍稀少，很多评估依赖 synthetic 或 replay。

### 8.2 深度学习模型泛化

- 给定材料中只有 Mousavi & Beroza 属于 deep learning，且输入是 seismic waveform。HR-GNSS deep learning 的跨区域泛化、跨台网泛化、跨震级泛化仍缺证据。
- 大震样本稀缺会导致 DL 模型对目标震级段学习不足；Mousavi & Beroza 也观察到较大事件预测误差可能因训练样本稀疏而增大。

### 8.3 台站几何和缺测影响

- 多篇论文都指出 station geometry、near-field coverage、dropout 关键，但缺少统一量化指标和系统消融实验。
- 未来模型应显式编码 station coordinates、epicentral distance、azimuth、azimuthal gap、nearest-station distance、station mask、latency mask。

### 8.4 Mw 饱和问题

- GNSS 缓解 seismic saturation 已有强证据，但 PGD / PGV scaling 自身是否会在特定范围、区域或台站几何下出现偏差，仍需更大样本验证。
- 对 M6–M7 边界事件，GNSS 信噪比与 seismic 方法优势如何切换，需要系统定义。

### 8.5 物理约束

- 传统方法有 Okada dislocation、fault scaling、GMPE 等明确物理结构；DL 若直接从位移到 Mw / slip，可能缺乏物理一致性。
- 研究空白是如何把 moment conservation、static displacement Green's functions、fault geometry constraints、non-negative slip、rupture speed prior 等引入神经网络或后处理。

### 8.6 不确定性估计

- GNSS 文献大量使用 VR、误差标准差、鲁棒性测试，但缺少 calibrated probabilistic output。
- Bayesian DL 提供方法启发，但尚需在 HR-GNSS 位移、PGD、offset 和 finite-fault 输出上验证 epistemic / aleatory uncertainty 的可解释性。

### 8.7 真实预警时间窗

- 文献中的关键时间尺度包括：PGD 约 15–30 s，CMT 约 43–50 s，REGARD 初始 finite-fault 58 s，G-larmS first alert 平均 31 s，Maduo 远场台站收敛 50–73 s。
- 缺口在于：不同输出目标在 5、10、15、20、30、60 s 的可达精度边界尚不清楚，尤其是 rupture duration 内是否能稳定估计 finite-source features。

---

## 9. Testable hypotheses

```yaml
- hypothesis: "在 10–30 s 早期时间窗内，加入 station geometry 与 dropout mask 的 HR-GNSS 模型，相比只使用位移/PGD 的模型，在跨事件 Mw 估计上具有更低误差和更好不确定性校准。"
  why_it_matters: "多篇文献指出 station geometry、near-field coverage 和 dropout 是实时 GNSS 表征的关键限制。"
  supporting_literature: ["Crowell et al. 2016", "Kawamoto et al. 2016", "Melgar et al. 2019", "Gao et al. 2021"]
  required_data: ["多事件 HR-GNSS 位移", "台站坐标", "震中/震源距", "台站缺测和延迟记录", "catalog Mw"]
  possible_experiment: "比较 waveform-only、PGD-only、geometry-aware、geometry+mask 模型在 10/15/20/30 s 的 Mw error 与 calibration。"
  evaluation_metrics: ["MAE/RMSE of Mw", "bias", "coverage probability", "ECE", "dropout sensitivity"]
  risks_or_confounders: ["大震样本少", "区域 scaling 差异", "近场台站数量与震级相关"]

- hypothesis: "Horizontal-only PGD / displacement 特征在真实实时 HR-GNSS 输入中比三分量 PGD 更稳健，但在某些机制或台站几何下可能损失垂向约束。"
  why_it_matters: "Melgar et al. 2019 显示 horizontal-only PGD std 小于三分量 PGD；Gao et al. 2021 对 Maduo strike-slip 也强调水平位移更敏感。"
  supporting_literature: ["Melgar et al. 2019", "Gao et al. 2021"]
  required_data: ["三分量实时与后处理 GNSS", "多机制事件", "PGD/offset 标签"]
  possible_experiment: "比较 3C、2C horizontal-only、learned channel weighting 三种输入在 Mw 和 offset 估计中的表现。"
  evaluation_metrics: ["Mw error", "PGD error", "offset error", "uncertainty calibration", "mechanism-stratified performance"]
  risks_or_confounders: ["垂向噪声区域差异", "俯冲带事件垂向信号可能更重要", "台站安装环境差异"]

- hypothesis: "PGD scaling 在 15–30 s 是强 baseline；深度学习模型若不能显著优于 PGD，仍可通过更好的 uncertainty / quality flag 提供实用价值。"
  why_it_matters: "Crowell et al. 2016 和 Melgar et al. 2019 支持 PGD 在早期可用；Mousavi & Beroza 2020 提供 uncertainty 思路。"
  supporting_literature: ["Crowell et al. 2016", "Melgar et al. 2019", "Mousavi & Beroza 2020"]
  required_data: ["PGD time evolution", "HR-GNSS waveforms", "catalog Mw", "real-time quality flags"]
  possible_experiment: "DL 与 PGD scaling 在相同台站、相同时间窗对比，并测试不确定性是否能识别大误差样本。"
  evaluation_metrics: ["Mw MAE", "30 s error", "negative log-likelihood", "AUROC for large-error detection", "coverage"]
  risks_or_confounders: ["PGD regression 已很强", "训练集信息泄漏", "catalog Mw 不确定性"]

- hypothesis: "对 finite-fault 输出，DL 的主要潜在优势不是最终反演精度，而是早期 fault-plane probability、rupture extent proxy 和快速 surrogate inversion。"
  why_it_matters: "Crowell et al. 2016 和 Kawamoto et al. 2016 都显示 fault-plane ambiguity / early finite-fault instability。"
  supporting_literature: ["Crowell et al. 2016", "Kawamoto et al. 2016", "Ruhl et al. 2019"]
  required_data: ["GNSS offsets/time series", "有限断层后验模型", "双断层面候选", "后处理 GNSS/InSAR slip models"]
  possible_experiment: "训练模型输出断层面概率、rupture extent class 或低维 slip representation，与传统 inversion 早期结果对比。"
  evaluation_metrics: ["fault-plane accuracy", "rupture extent IoU", "slip distribution correlation", "VR/misfit", "time-to-stable-solution"]
  risks_or_confounders: ["有限断层标签非唯一", "多模型反演差异", "训练数据以区域断层先验为主"]

- hypothesis: "将 HR-GNSS 震源表征评价从 Mw error 扩展到 MMI threshold / warning time，会改变模型优劣排序。"
  why_it_matters: "Ruhl et al. 2019 显示 geodetic solutions 在用户侧 warning performance 上显著改善，但也增加 false positives。"
  supporting_literature: ["Ruhl et al. 2019"]
  required_data: ["震源估计随时间", "station-level seismic intensity / MMI", "GMPE 或观测 MMI", "用户阈值"]
  possible_experiment: "同一组 HR-GNSS 模型同时按 Mw error 和 MMI warning metrics 排名，比较排序差异。"
  evaluation_metrics: ["TP/FN/FP", "median WT", "MMI error", "cost savings Q", "Mw error"]
  risks_or_confounders: ["GMPE uncertainty", "站点 VS30 误差", "用户 cost ratio 难估计"]

- hypothesis: "在远场或稀疏 GNSS 台网中，PGD 比 PGV 更早达到稳定震级；PGV 需要区域化 scaling 或 learned correction 才能发挥优势。"
  why_it_matters: "Gao et al. 2021 显示 PGD 更稳定，PGV 最终更接近 USGS 但台站间波动更大。"
  supporting_literature: ["Gao et al. 2021"]
  required_data: ["PGD/PGV time series", "不同区域 Mw 6–9 事件", "台站数量消融"]
  possible_experiment: "按台站数量、震源距和区域分别比较 PGD scaling、PGV scaling、PGD+PGV learned fusion。"
  evaluation_metrics: ["convergence time", "Mw MAE", "station-number sensitivity", "bias by distance", "variance across stations"]
  risks_or_confounders: ["速度处理方法不同", "区域传播路径差异", "PGV regression 适用范围"]
```

---

## 10. How this helps my paper

### Introduction

- 可用 Crowell et al. (2016) 和 Ruhl et al. (2019) 支撑问题动机：seismic-only EEW 在大震中存在震级饱和和点源假设限制，GNSS 静态/长周期位移提供非饱和约束。
- 可用 Kawamoto et al. (2016)、Melgar et al. (2019)、Gao et al. (2021) 说明 HR-GNSS 已在真实事件中展示 operational viability，包括 finite-fault 初估、实时位移质量和 Mw 7+ 震级估计。

### Related Work

- 按研究路线组织，而不是逐篇罗列：
  1. PGD / PGV scaling；
  2. geodetic EEW systems: G-FAST / REGARD / G-larmS；
  3. real-time HR-GNSS data quality；
  4. ground-motion warning evaluation；
  5. Bayesian / DL uncertainty for rapid source characterization。
- Mousavi & Beroza 可放在“deep learning source characterization / uncertainty”小节，而不是 GNSS 主线。

### Method

- 输入设计可包括：多台站三分量位移、horizontal-only 位移、PGD/PGV time evolution、static offset estimate、station coordinates、hypocentral distance、azimuth、station mask、latency / quality flag。
- 输出设计可分层：Mw → uncertainty → rupture extent / fault-plane probability → finite-fault / slip proxy。
- 可借鉴传统系统的层级结构：seismic trigger + GNSS displacement + source inversion / prediction。

### Experiment

- Baseline 至少包括 PGD scaling、PGV scaling、简单多台站平均、G-FAST / G-larmS-style finite-fault inversion（若可复现）、seismic-only 或 trigger-only baseline。
- 时间窗建议固定为 10、15、20、30、60 s，并报告 first alert 与 final performance。
- 消融实验应覆盖：station number、near-field station removal、dropout、noise injection、vertical removal、geometry encoding、uncertainty head。

### Discussion

- 可讨论 DL 是否真正优于传统 geodetic EEW，还是主要提供 faster surrogate、uncertainty 和鲁棒性。
- 可讨论 false positives 与 missed alerts 的权衡，避免只追求低 Mw error。
- 可强调真实实时数据误差和 operational constraints 是方法落地关键。

### Limitations

- 大震样本少、区域不均衡、synthetic-real gap、有限断层标签非唯一、GNSS 台站覆盖不均、实时误差分布不完整。
- 如果使用后处理数据训练，需要承认 real-time positioning noise / latency / dropout 可能造成域偏移。

---

## 11. Citation candidates

1. **Ruhl et al. (2019), JGR Solid Earth**  
   - **优先引用位置**：Introduction、Related Work、Evaluation。  
   - **用途**：最强的定量证据，说明 geodetic constraints 相对 seismic-only EEW 可改善大震震级、MMI warning、WT 和 cost savings。

2. **Crowell et al. (2016), SRL**  
   - **优先引用位置**：Introduction、Baseline、Method。  
   - **用途**：G-FAST 系统框架；PGD/CMT/finite-fault 层级输出；latency/noise/dropout 鲁棒性；Cascadia geodetic EEW。

3. **Kawamoto et al. (2016), Earth, Planets and Space**  
   - **优先引用位置**：Related Work、Benchmark、Discussion。  
   - **用途**：REGARD 真实 operational finite-fault 案例；Kumamoto 主震 58 s 初估、5 min 收敛；先验与断层面问题。

4. **Melgar et al. (2019), EarthArXiv / TODO: verify formal SRL version**  
   - **优先引用位置**：Data、Method、Discussion。  
   - **用途**：真实端到端实时 HR-GNSS 位移质量、PGD / offset 误差、latency、1 Hz vs 5 Hz、horizontal-only PGD。

5. **Gao et al. (2021), Remote Sensing**  
   - **优先引用位置**：Related Work、Baseline、Regional case。  
   - **用途**：Maduo Mw 7.3；PGD/PGV scaling；中国大陆/青藏高原 HR-GNSS 案例；台站数量对收敛影响。

6. **Mousavi & Beroza (2020 / TODO: verify)**  
   - **优先引用位置**：Deep learning / uncertainty subsection。  
   - **用途**：Bayesian deep learning、单台快速定位、不确定性估计；作为 HR-GNSS DL 方法设计的类比参考，而非 GNSS 证据。

---

## 12. TODO: next literature search

### 12.1 HR-GNSS / geodetic EEW 系统

- `G-larmS real-time GNSS earthquake early warning finite fault`
- `G-FAST geodetic earthquake early warning Cascadia subduction`
- `BEFORES Bayesian finite fault earthquake early warning GNSS`
- `REGARD GEONET real-time GNSS finite fault Kawamoto 2017`
- `ShakeAlert geodetic algorithms GNSS integration`

### 12.2 Seismogeodesy / GNSS + strong motion fusion

- `real-time seismogeodesy earthquake early warning`
- `GNSS strong motion fusion earthquake source characterization`
- `seismogeodetic finite fault inversion rapid tsunami warning`
- `Melgar seismogeodesy earthquake early warning GNSS accelerometer`

### 12.3 Deep learning source characterization

- `deep learning earthquake magnitude estimation high-rate GNSS`
- `deep learning rapid finite fault inversion GNSS`
- `graph neural network earthquake early warning station geometry`
- `transformer earthquake source characterization GNSS`
- `Bayesian deep learning earthquake early warning uncertainty calibration`

### 12.4 大震 / 巨震 benchmark

- `Tohoku 2011 high-rate GNSS real-time source inversion`
- `Chile 2010 Maule GNSS finite fault rapid inversion`
- `Cascadia megathrust synthetic GNSS earthquake early warning benchmark`
- `Alaska 2018 GNSS earthquake early warning finite fault`
- `tsunami warning GNSS finite fault rapid source`

### 12.5 评价指标与用户收益

- `earthquake early warning cost savings performance metric Q`
- `MMI threshold warning time true positive false negative earthquake early warning`
- `ground motion based earthquake early warning geodetic finite fault`
- `uncertainty calibration earthquake early warning deep learning`

---

## 13. 本综述的边界与可信度

**可信内容。** 本综述中的定量数值均来自指定 reading notes；跨文献归纳主要限于 6 篇材料之间的共同主题。对于 Crowell、Kawamoto、Melgar、Gao、Ruhl 的核心结论，reading notes 已记录 DOI、数据、方法和关键数值，适合用于论文选题和综述框架搭建。

**需要谨慎处。** Melgar et al. (2019) 在 note 中标为 EarthArXiv preprint submitted to SRL，正式发表版本需 `TODO: verify`。Mousavi & Beroza 的年份、venue、DOI、arXiv URL 也需 `TODO: verify`。所有用于正式论文引用的数值，都应回查 PDF 页码、图号、表号和原文上下文。

**最终研究启发。** 当前材料已经足够支撑一个以“HR-GNSS 如何从大震非饱和震级估计走向快速有限源表征”为主线的 SRL-style 研究叙事；下一步最关键的是补齐 HR-GNSS deep learning 文献和可复现实验 benchmark，而不是继续堆叠单事件 case study。
