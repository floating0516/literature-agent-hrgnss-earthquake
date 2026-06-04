# Bayesian-Deep-Learning Estimation of Earthquake Location from Single-Station Observations｜Reading Note

## 1. Metadata

- Title: Bayesian-Deep-Learning Estimation of Earthquake Location from Single-Station Observations
- Authors: S. Mostafa Mousavi, Gregory C. Beroza
- Year: 2020（parsed text 中显示 arXiv:1912.01144v1, 3 Dec 2019；TODO: verify）
- Venue: arXiv preprint（TODO: verify 是否有正式发表版本）
- DOI: Not specified in provided text
- URL / PDF: arXiv:1912.01144v1（TODO: verify URL）
- Local PDF: `papers/raw_pdf/2020_bayesian_deep_learning_estimation_of_earthquake_location_from.pdf`
- Parsed text: `papers/parsed_md/2020_bayesian_deep_learning_estimation_of_earthquake_location_from.md`
- Paper ID: 2020_bayesian_deep_learning_estimation_of_earthquake_location_from

## 2. One-sentence summary

这篇论文提出一种 Bayesian deep learning 单台地震定位方法：用两个轻量神经网络分别从 1 分钟三分量地震波形估计震中距/P 波走时和反方位角，并进一步推算震中、发震时刻和深度，同时给出 epistemic / aleatory uncertainty 或置信区间。

## 3. Research problem

论文试图解决的问题是：在只有单台地震观测、台网稀疏或小震记录台站很少的情况下，能否直接从单台三分量波形快速估计地震位置、发震时刻和深度，并且量化预测不确定性。

具体问题包括：

- 传统和已有深度学习地震定位方法通常依赖多台站或区域特定台网配置；
- 既有单台深度学习方法多把距离、方位、震级、深度离散成分类任务，泛化能力和误差表现有限；
- 普通神经网络通常不提供可靠的模型置信度，而地震监测和预警需要知道哪些预测可信、哪些需要人工或后续算法处理。

## 4. Background and motivation

论文背景是机器学习已在地震检测、震相拾取、初动极性、去噪、事件判别和震相关联等任务上取得进展，但 earthquake location 仍然困难。已有单台 CNN 方法可以做事件/噪声分类、距离/方位/震级/深度分类，但论文指出这些方法泛化较差且误差较高；多台站深度学习定位方法虽然效果更好，但通常学习的是特定局部台网的 move-out pattern。

作者强调，不确定性对于机器学习预测可靠性至关重要。普通回归模型输出单个向量，分类模型 softmax 概率也不等同于模型置信度。Bayesian neural networks 可以通过对模型权重或预测分布的概率近似，估计 epistemic uncertainty 和 aleatory uncertainty，从而帮助识别不可靠预测。

因此，论文动机是把 single-station earthquake location 表述为 regression problem，并在 Bayesian framework 下给出快速震源表征及其不确定性。

## 5. Data

- 数据集：STanford EArthquake Dataset (STEAD)；
- 数据类型：全球 labeled 3-component seismic waveforms；
- 使用数据：只使用 earthquake waveforms，不使用非地震波形；
- 震中距范围：epicentral distances less than 110 km，摘要中也写 within 1 degree (~112 km)；
- 信噪比筛选：signal-to-noise ratio ≥ 25 dB；
- 台站方向筛选：只使用 north-south 和 east-west components 正确对齐地理方向的台站；
- 样本数量：约 150,000 waveforms；
- 训练/测试划分：80% training，20% testing；
- 波形长度：1 minute；
- 采样率：100 Hz；
- 滤波：band-pass filtered from 1–45 Hz；
- 研究区域：global dataset，location examples 包括 Asia、Africa、Central US、Nevada、San Juan island、Southern California、Alaska 等；
- 是否使用合成数据：Not specified in provided text；文中描述为真实 earthquake waveforms from STEAD；
- 数据可复现信息：提供 STEAD 引用，但 parsed text 未给出下载链接或代码仓库信息。

## 6. Method

论文将单台定位拆解为两个回归网络和一个几何推算步骤。

### 6.1 输入与输出

**dist-PT network**：

- 输入：`6000 × 4` matrix；
  - 前三列/通道为 1 分钟三分量波形，每秒 100 samples；
  - 第四个向量为 binary vector，P 到 S arrival times 之间置 1，其余为 0，用于突出最有信息量的波形片段；
- 输出：epicentral distance、P travel time，以及对应 aleatory uncertainty；
- 不确定性：通过 dropout posterior sampling 估计 epistemic uncertainty，并通过 customized loss function 学习 aleatory uncertainty。

**BAZ network**：

- 输入 1：`150 × 3` matrix，即 P arrival 前 0.5 s 到后 1 s 的三分量波形；
- 输入 2：`7 × 3` matrix，由同一时间窗内三分量波形的 covariance matrix、eigenvalues 和 eigenvectors 组成；
- 输出：back-azimuth angle 的 unit circle 坐标 `(cos θ, sin θ)`，测试时再转换为 back-azimuth angle；
- 不确定性：估计 epistemic uncertainty；未稳定估计 aleatory uncertainty。

### 6.2 模型或算法

- dist-PT network：multi-task temporal convolutional network；
  - 使用 1D causal dilated convolutions；
  - 使用 residual connections；
  - 11 个 dilational convolution layers；
  - dilation rate 每层加倍；
  - 每层 relu activation；
  - 每层 20 kernels，kernel size 6；
  - 末端两个 fully connected layers，每个为 linear activation 和 two neurons；
  - trainable parameters: 58,500；
  - dropout rate: 0.20。

- BAZ network：multi-input convolutional network；
  - 两个输入分支分别经过 4 个和 1 个 convolutional layers；
  - 后接两个 fully connected layers，分别为 100 和 2 neurons；
  - 除最后 fully connected layer 外，其余层使用 relu；
  - convolution kernel size 为 3；
  - kernels 数量在 20 到 64 之间；
  - trainable parameters: ~46,000；
  - convolutional layers 后 dropout rate 0.1；fully connected layers 后 dropout rate 0.3。

### 6.3 损失函数与不确定性

- Bayesian approximation：Monte Carlo dropout sampling；
- aleatory uncertainty：dist-PT network 通过 customized Bayesian neural network loss 学习 data-dependent variance；
- loss function 包含 regression residual term 和 uncertainty regularization term；
- predictive uncertainty 由 epistemic uncertainty 与 aleatory uncertainty 组合得到；
- BAZ network 因 angle orientation prediction 非欧氏空间问题，把 back-azimuth 表示为 unit circle 上的 `(cos θ, sin θ)`，避免直接使用普通 L2 loss 处理角度周期性。

### 6.4 位置、发震时刻和深度推算

- 用 predicted epicentral distance 和 predicted back-azimuth 估计 epicenter；
- 基于 distance 和 back-azimuth 的不确定性投影到 reference Earth model，计算 epicentral location error ellipse；
- 用 predicted P travel time 估计 origin time；
- 用 predicted P travel distance 与 epicentral distance 粗略估计 depth；
- 深度估计假设 P wave 沿 source-station straight-line path 传播，并采用 P-wave velocity 5.6 km/s；
- 多台单站观测可对同一事件的 estimates 做平均；文中示例使用 unweighted averaging。

### 6.5 Baseline / comparison

- 论文讨论并对比传统 single-station location methods 和 Lockman & Allen (2005) 的 single-station EEW 参数精度；
- 但 parsed text 未提供统一复现实验中的传统 baseline 表格或同数据集定量对比。

## 7. Evaluation metrics

论文使用的主要评价指标包括：

- epicentral distance mean error；
- epicentral distance standard deviation；
- P travel time mean error；
- P travel time standard deviation；
- back-azimuth mean error；
- coefficient of determination；
- prediction error 与 estimated uncertainty 的相关性；
- epicenter location mean error；
- origin time mean error；
- depth mean error；
- error ellipse / confidence interval；
- prediction errors 与 event magnitude、depth、SNR、catalog uncertainty、station-event distance 的关系。

## 8. Key results

- dist-PT network 对 P travel time 的估计表现最好，P travel time 的 mean error 为 0.03 s，standard deviation 为 0.66 s。  
  Evidence: Abstract states “P travel time with absolute mean errors of ... 0.03 s”; Results state “The network is able to estimate P travel time with a standard deviation of 0.66 second.”

- epicentral distance 的 mean error 为 0.23 km，standard deviation 为 5.42 km。  
  Evidence: Abstract states “epicentral distance ... with absolute mean errors of 0.23 km”; Results state “The mean error for epicentral distance estimates is 0.23 km with a standard deviation of 5.42 km.”

- back-azimuth estimation 的 coefficient of determination 为 0.87，mean error 约 1 degree。  
  Evidence: “a coefficient of determination of 0.87 for the regression results and a mean error rate of ~ 1 degree...”

- 在完整测试集上，最终 event-based estimates 的 epicenter、origin time 和 depth mean errors 分别为 7.3 km、0.4 s 和 6.7 km。  
  Evidence: Abstract and Results both state “mean errors of 7.3 km, 0.4 second, and 6.7 km respectively.”

- distance 和 P travel time 的 estimated uncertainties 与 prediction errors 存在正相关，aleatory uncertainty 比 epistemic uncertainty 更能反映误差。  
  Evidence: “There is some positive correlation between the estimated uncertainties and prediction errors...” and “the aleatory uncertainties reflect the errors better than the estimated epistemic uncertainties.”

- back-azimuth 的 epistemic uncertainty 与 prediction error 也有弱正相关，但 back-azimuth 是位置结果中最大的不确定性来源。  
  Evidence: “we still observe a weak positive correlation...” and “The largest uncertainty in location results is caused by uncertainties in the back-azimuth.”

- 单台预测在 Alaska 和 northern California 的区域图上能恢复总体地震活动空间格局，outliers sparse。  
  Evidence: “the predicted locations reveal the overall pattern of seismicity correctly, and that the outliers are sparse.”

- 大震事件倾向于具有更大的 prediction errors，作者认为可能与数据集中较大事件训练样本更稀疏有关。  
  Evidence: “Larger events tend to have larger prediction errors, which may be attributable to the more sparse training data for larger events in the dataset.”

- very shallow events 和 deeper than 20 km events 的 depth errors 更大。  
  Evidence: “Very shallow events and events deeper than 20 km have larger errors.”

## 9. Strengths

- 把 single-station earthquake location 从分类任务转为连续回归任务，更直接输出距离、走时和方位；
- 使用 Bayesian deep learning 框架显式估计不确定性，适合地震监测中判断预测可靠性；
- 方法只依赖单台三分量波形，在小震或台网稀疏区域有潜在应用价值；
- 使用全球 STEAD 数据集训练和测试，而非只在单一区域台网验证；
- 模型轻量，dist-PT network 约 58,500 参数，BAZ network 约 46,000 参数；
- 把 P travel time、epicentral distance、back-azimuth 组合起来估计 epicenter、origin time 和 depth，形成完整单台震源表征流程；
- 对误差来源进行了较细分析，包括 station-event distance、SNR、magnitude、depth、catalog uncertainty 和 predicted uncertainty；
- 对 EEW 和稀疏记录地震定位都有明确应用场景。

## 10. Limitations

- 输入依赖已知 P 和 S arrivals 或至少使用 arrival-time vector 来加速训练；虽然作者称无 picks 时也能表现良好，但 parsed text 未给出完整定量结果；
- 只使用震中距 <110 km、SNR ≥25 dB 且水平分量方向正确的波形，低 SNR、远震或复杂台站条件下泛化仍需验证；
- 当前方法不考虑与地理方向不一致的 station orientations，不适用于 borehole stations，因此不能利用 borehole instruments 的高 SNR 数据；
- back-azimuth 是最大误差来源，且 BAZ network 未能稳定估计 aleatory uncertainty；
- 深度估计不是端到端训练得到，而是基于 P travel distance 和 epicentral distance 的几何推算，并假设直线路径和 5.6 km/s P 波速度；
- 当前 depth estimation procedure 不适用于 regional 和 teleseismic distances，因为更复杂波传播和地球球形效应会影响估计；
- 大震样本较少导致较大事件预测误差更高；
- very shallow events 和 >20 km 深度事件的 depth errors 更大；
- parsed text 未提供代码仓库、完整训练细节、训练 epoch、optimizer、batch size 等可复现信息；
- 与传统方法的比较主要在讨论中陈述，未见统一 benchmark 表格。

## 11. Relation to my research

```yaml
use_for_my_paper:
  introduction: true
  methods: true
  baseline: true
  discussion: true
  dataset: false
reason: "这篇论文不是 HR-GNSS 论文，而是单台三分量地震波形的 Bayesian deep learning 震源定位研究；它可作为深度学习快速震源表征、不确定性估计、单台/少台观测定位和 EEW 场景的 Introduction 与 Method 参考，也可作为与 HR-GNSS deep learning 方法对比的 seismic-only baseline 思路。"
```

具体启发：

- 对 HR-GNSS + deep learning 大震快速震源表征，可借鉴其把复杂震源表征拆成多个可学习中间量再几何组合的设计；
- Bayesian / Monte Carlo dropout uncertainty 可用于 GNSS 位移模型的震级、位置、断层参数或质量控制；
- single-station / limited-observation 思路可迁移到“少量 GNSS 台站早期窗口”条件下的大震快速估计；
- 可在 Introduction 中引用其观点：深度学习地震任务需要输出不确定性，softmax 或单点回归不足以代表置信度；
- 可在 Discussion 中对比 seismic waveform-based source characterization 与 HR-GNSS displacement-based source characterization 的输入、时窗、物理含义和不确定性来源；
- 不适合作为 GNSS dataset 来源，因为文中使用 STEAD 三分量地震波形而非 GNSS 位移。

## 12. Useful citations or quotable ideas

- 单台地震定位可以被表述为 regression problem，通过分别估计 epicentral distance、P travel time 和 back-azimuth 来恢复震中、发震时刻和深度；该观点来自 Introduction 和 Results/Location Results。
- 普通深度学习模型通常不能捕获输出不确定性，classification probability 不等同于 model confidence；该观点来自 Introduction 中关于 uncertainty 的讨论。
- Bayesian neural networks 可以为地震快速表征提供 epistemic 和 aleatory uncertainty，从而识别不可靠预测；该观点来自 Introduction 和 Methods。
- back-azimuth uncertainty 是单台定位结果中最大的误差来源；该观点来自 Discussion and Conclusions。
- 单台深度学习定位对小震或台网稀疏区域有价值，因为小震最可能只被少数台站记录；该观点来自 Location Results。
- 使用 light neural networks 和高质量标签数据可以在相对有限参数量下获得全球数据集上的定位能力；该观点来自 Network Architecture 和 Discussion。

## 13. Open questions

- 如果把这种 Bayesian uncertainty estimation 迁移到 HR-GNSS，大震震级、破裂范围和有限断层参数的不确定性应如何定义和校准？
- 对 GNSS 位移输入，是否也可以拆分为多个中间任务，例如 PGD、静态 offset、方位、距离、Mw，再组合为震源参数？
- 在真实 EEW 中，P/S picks 或 GNSS 触发信息不准确时，类似 attention vector 的辅助输入会如何影响鲁棒性？
- 对大型俯冲带地震，单台或少台观测是否足以给出有用的早期震源约束，还是必须显式引入台网几何？
- back-azimuth 是该 seismic 方法最大误差来源；在 GNSS 位移场中，最大误差来源会是台站几何、垂向噪声、断层非唯一性，还是早期窗口不完整？
- 如何验证 Bayesian deep learning 输出的不确定性是否 calibrated，而不仅仅与误差弱相关？

## 14. Extracted structured tags

```yaml
domain:
  - seismology
  - earthquake location
  - earthquake early warning
  - Bayesian deep learning
  - single-station source characterization
data_type:
  - 3-component seismic waveform
  - STEAD
  - 1-minute seismogram
  - 100Hz waveform
  - P and S arrival indicator vector
task:
  - single-station earthquake location
  - epicentral distance estimation
  - P travel time estimation
  - back-azimuth estimation
  - origin time estimation
  - depth estimation
  - uncertainty estimation
method:
  - Bayesian neural network
  - Monte Carlo dropout
  - temporal convolutional network
  - causal dilated convolution
  - residual connection
  - multi-task learning
  - unit-circle angle regression
input_window:
  - 1min
  - 6000 samples
  - 0.5s before P arrival to 1s after P arrival
metrics:
  - epicentral distance mean error
  - P travel time mean error
  - back-azimuth mean error
  - epicenter mean error
  - origin time mean error
  - depth mean error
  - coefficient of determination
  - uncertainty-error correlation
limitations:
  - requires high-SNR selected waveforms
  - station orientation dependency
  - not applicable to borehole stations in current form
  - back-azimuth uncertainty dominates location error
  - no stable aleatory uncertainty for BAZ network
  - approximate depth estimation
  - limited large-event training data
  - incomplete reproducibility information in provided text
```

## 15. TODO: verify

- 确认该论文最终年份应写 2019、2020，还是正式发表年份；parsed text 只显示 arXiv:1912.01144v1, 3 Dec 2019，而文件名为 2020；
- 确认是否有正式期刊发表版本、DOI 和最终题名；
- 回查 arXiv URL 和 PDF 元数据；
- 核查 abstract 中 “absolute mean errors” 与 Results 中 “mean error” 的定义是否为 signed mean error、absolute mean error 或其他统计量；
- 回查 Figure 5–13 的图注和正文，确认 coefficient of determination、standard deviation、error distributions 的精确含义；
- 确认 dist-PT network 输入维度在原文中 “first three rows / last row” 是否应理解为 channels 而非 rows；
- 核查 BAZ network 的 `7 × 3` covariance/eigenvalue/eigenvector 特征构造细节；
- 确认 “The authors declare any competing interests.” 是否为 parsed text/OCR 错误，原文可能应为 no competing interests；
- 若用于论文引用，需要回到 PDF 获取页码、图号和公式编号。