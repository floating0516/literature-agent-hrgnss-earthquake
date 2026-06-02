# 筛选前后结果对比

> 目的：比较 OpenAlex 原始候选结果和粗筛后的结果，观察结构健康监测、UAV、桥梁监测等噪声是否被过滤。

## 1. 筛选前

OpenAlex 原始去重候选数量：285。由于 query 中包含 `GNSS`、`early warning` 等通用词，原始结果中混入了一些噪声，例如结构健康监测、UAV、桥梁监测、云计算 early warning、普通 GNSS 动态监测等。

## 2. 筛选后

- Keep：141
- Maybe：72
- Discard：72

Keep 结果主要集中在 HR-GNSS、real-time GNSS、G-FAST、geodetic earthquake early warning、GNSS seismology、coseismic displacement、ShakeAlert/REGARD/FinDerS 等方向。

## 3. 噪声过滤示例

| Title | Noise terms | Decision | Reason |
|---|---|---|---|
| Convergence Conditions for Ascent Methods | seismic anisotropy | keep | matched strong topic terms: earthquake source; matched deep-learning terms: deep learning, machine learning, neural network, neural networks, cnn; possible noise terms: seismic anisotropy |
| Real-time GNSS seismology using a single receiver | ionospheric | maybe | matched strong topic terms: high-rate gnss, real-time gnss, gnss seismology, coseismic displacement, coseismic displacements; matched source-characterization terms: fault slip, slip distribution; possible noise terms: ionospheric |
| Global Navigation Satellite Systems Seismology for the 2012 Mw 6.1 Emilia Earthquake: Exploiting the VADASE Algorithm | ionospheric | maybe | matched strong topic terms: gnss seismology, coseismic displacement, coseismic displacements; possible noise terms: ionospheric |
| A Systematic Review of Disaster Management Systems: Approaches, Challenges, and Future Directions | cloud computing | maybe | matched deep-learning terms: machine learning; possible noise terms: cloud computing |
| AI-Driven Innovations in Earthquake Risk Mitigation: A Future-Focused Perspective | structural health monitoring | maybe | matched deep-learning terms: artificial intelligence; possible noise terms: structural health monitoring |
| GNSS total variometric approach: first demonstration of a tool for real-time tsunami genesis estimation | ionospheric | maybe | possible noise terms: ionospheric |
| Ensemble Machine Learning of Random Forest, AdaBoost and XGBoost for Vertical Total Electron Content Forecasting | ionospheric | discard | matched deep-learning terms: machine learning; possible noise terms: ionospheric |
| Low-Cost GNSS and Real-Time PPP: Assessing the Precision of the u-blox ZED-F9P for Kinematic Monitoring Applications | kinematic monitoring applications, low-cost gnss | discard | possible noise terms: kinematic monitoring applications, low-cost gnss |
| Surface-to-space atmospheric waves from Hunga Tonga–Hunga Ha’apai eruption | ionospheric | discard | possible noise terms: ionospheric |
| The GUARDIAN system-a GNSS upper atmospheric real-time disaster information and alert network | ionospheric | discard | possible noise terms: ionospheric |
| Unmanned Aerial Vehicles for Search and Rescue: A Survey | uav | discard | possible noise terms: uav |
| On the Use of Unmanned Aerial Systems for Environmental Monitoring | bridge | discard | possible noise terms: bridge |

## 4. 保留结果示例

| Title | Categories | Strong / DL / Source terms | Decision | Fulltext |
|---|---|---|---|---|
| A Hybrid Deep Learning Model for Rapid Probabilistic Earthquake Source Parameter Estimation With Displacement Waveforms From a Flexible Set of Seismic or HR-GNSS Stations | finite_fault_source_inversion, deep_learning_eew, deep_learning_source_characterization | earthquake source, deep learning, neural network, convolutional neural network, cnn, source characterization, focal mechanism | keep | closed_or_manual_required |
| A Self-Supervised Deep Learning Approach for Blind Denoising and Waveform Coherence Enhancement in Distributed Acoustic Sensing Data | gnss_geodetic_eew, finite_fault_source_inversion, deep_learning_eew, deep_learning_source_characterization | regard, earthquake source, deep learning, neural network, neural networks, source characterization | keep | closed_or_manual_required |
| Accelerating low-frequency ground motion simulation for finite fault sources using neural networks | finite_fault_source_inversion, deep_learning_eew, deep_learning_source_characterization | earthquake source, finite fault, neural network, neural networks, rupture directivity, moment tensor, focal mechanism | keep | open_pdf_found |
| Bayesian-Deep-Learning Estimation of Earthquake Location From Single-Station Observations | finite_fault_source_inversion, deep_learning_eew, deep_learning_source_characterization | earthquake source, seismic waves, neural network, neural networks, convolutional neural network, source characterization | keep | open_pdf_found |
| Simultaneous magnitude and slip distribution characterization from high-rate GNSS using deep learning: case studies of the 2021 <i>M</i>w 7.4 Maduo and 2023 Turkey doublet events | gnss_geodetic_eew, finite_fault_source_inversion, deep_learning_eew, deep_learning_source_characterization, tsunami_large_earthquake | high-rate gnss, earthquake source, deep learning, neural network, slip distribution | keep | open_pdf_found |
| Automated Seismic Source Characterization Using Deep Graph Neural Networks | finite_fault_source_inversion, deep_learning_eew, deep_learning_source_characterization | earthquake early warning, machine learning, neural network, neural networks, graph neural network, source characterization | keep | open_pdf_found |
| Demonstration of the Cascadia G‐FAST Geodetic Earthquake Early Warning System for the Nisqually, Washington, Earthquake | gnss_geodetic_eew, seismogeodesy_fusion, finite_fault_source_inversion | geodetic earthquake early warning, earthquake early warning, source characterization, moment tensor | keep | open_pdf_found |
| Spatiotemporal Graph Convolutional Networks for Earthquake Source Characterization | finite_fault_source_inversion, deep_learning_eew, deep_learning_source_characterization | earthquake early warning, earthquake source, deep learning, machine learning, neural network, neural networks, source characterization | keep | open_pdf_found |
| Real-Time High-Rate GNSS Displacements: Performance Demonstration During the 2019 Ridgecrest, CA Earthquakes | gnss_geodetic_eew, finite_fault_source_inversion | high-rate gnss, real-time gnss, earthquake source, gnss displacement, source characterization | keep | open_pdf_found |
| PEGSGraph: A Graph Neural Network for Fast Earthquake Characterization Based on Prompt ElastoGravity Signals | deep_learning_eew, deep_learning_source_characterization, tsunami_large_earthquake | earthquake early warning, seismic waves, deep learning, machine learning, neural network, convolutional neural network, focal mechanism | keep | open_pdf_found |
| Real-Time High-Rate GNSS Displacements: Performance Demonstration during the 2019 Ridgecrest, California, Earthquakes | gnss_geodetic_eew, finite_fault_source_inversion | high-rate gnss, earthquake source, gnss displacement, gnss displacements, source characterization | keep | closed_or_manual_required |
| Temporal point positioning approach for real‐time GNSS seismology using a single receiver | gnss_geodetic_eew, finite_fault_source_inversion, tsunami_large_earthquake | gnss seismology, coseismic displacement, coseismic displacements, fault slip, slip distribution | keep | open_pdf_found |
| Grond - A probabilistic earthquake source inversion framework | finite_fault_source_inversion | earthquake source, finite fault, source inversion, moment tensor | keep | open_landing_page_or_oa_no_pdf |
| First result from the GEONET real-time analysis system (REGARD): the case of the 2016 Kumamoto earthquakes | gnss_geodetic_eew | regard, coseismic displacement, coseismic displacements, earthquake early warning | keep | open_pdf_found |
| G‐FAST Earthquake Early Warning Potential for Great Earthquakes in Chile | gnss_geodetic_eew, finite_fault_source_inversion, tsunami_large_earthquake | g-fast, earthquake early warning, moment tensor | keep | open_landing_page_or_oa_no_pdf |

## 5. 结论

粗筛后，明显偏离地震学/GNSS 地震预警主题的结果被降级为 maybe 或 discard。保留结果的主题集中度明显高于 OpenAlex 原始结果。

当前脚本是规则型粗筛，不替代后续 LLM 精筛和人工判断。下一步可以对 Keep 和 Maybe 论文运行 `paper_screening_prompt.md`，进一步判断是否进入全文阅读。