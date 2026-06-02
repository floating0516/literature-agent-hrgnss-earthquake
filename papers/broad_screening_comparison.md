# 筛选前后结果对比

> 目的：比较 OpenAlex 原始候选结果和粗筛后的结果，观察结构健康监测、UAV、桥梁监测等噪声是否被过滤。

## 1. 筛选前

OpenAlex 原始去重候选数量：285。由于 query 中包含 `GNSS`、`early warning` 等通用词，原始结果中混入了一些噪声，例如结构健康监测、UAV、桥梁监测、云计算 early warning、普通 GNSS 动态监测等。

## 2. 筛选后

- Keep：82
- Maybe：100
- Discard：103

Keep 结果主要集中在 HR-GNSS、real-time GNSS、G-FAST、geodetic earthquake early warning、GNSS seismology、coseismic displacement、ShakeAlert/REGARD/FinDerS 等方向。

## 3. 噪声过滤示例

| Title | Noise terms | Decision | Reason |
|---|---|---|---|
| Real-time GNSS seismology using a single receiver | ionospheric | maybe | matched strong topic terms: high-rate gnss, real-time gnss, gnss seismology, coseismic displacement, coseismic displacements; possible noise terms: ionospheric |
| Global Navigation Satellite Systems Seismology for the 2012 Mw 6.1 Emilia Earthquake: Exploiting the VADASE Algorithm | ionospheric | maybe | matched strong topic terms: gnss seismology, coseismic displacement, coseismic displacements; possible noise terms: ionospheric |
| Convergence Conditions for Ascent Methods | seismic anisotropy | maybe | matched strong topic terms: earthquake source; possible noise terms: seismic anisotropy |
| GNSS total variometric approach: first demonstration of a tool for real-time tsunami genesis estimation | ionospheric | maybe | possible noise terms: ionospheric |
| A Systematic Review of Disaster Management Systems: Approaches, Challenges, and Future Directions | cloud computing | discard | possible noise terms: cloud computing |
| Low-Cost GNSS and Real-Time PPP: Assessing the Precision of the u-blox ZED-F9P for Kinematic Monitoring Applications | kinematic monitoring applications, low-cost gnss | discard | possible noise terms: kinematic monitoring applications, low-cost gnss |
| Surface-to-space atmospheric waves from Hunga Tonga–Hunga Ha’apai eruption | ionospheric | discard | possible noise terms: ionospheric |
| Ensemble Machine Learning of Random Forest, AdaBoost and XGBoost for Vertical Total Electron Content Forecasting | ionospheric | discard | possible noise terms: ionospheric |
| The GUARDIAN system-a GNSS upper atmospheric real-time disaster information and alert network | ionospheric | discard | possible noise terms: ionospheric |
| AI-Driven Innovations in Earthquake Risk Mitigation: A Future-Focused Perspective | structural health monitoring | discard | possible noise terms: structural health monitoring |
| Unmanned Aerial Vehicles for Search and Rescue: A Survey | uav | discard | possible noise terms: uav |
| On the Use of Unmanned Aerial Systems for Environmental Monitoring | bridge | discard | possible noise terms: bridge |

## 4. 保留结果示例

| Title | Strong terms | Decision | Fulltext |
|---|---|---|---|
| First result from the GEONET real-time analysis system (REGARD): the case of the 2016 Kumamoto earthquakes | regard, coseismic displacement, coseismic displacements, earthquake early warning | keep | open_pdf_found |
| Earthquake Magnitude Estimation from High-Rate GNSS Data: A Case Study of the 2021 Mw 7.3 Maduo Earthquake | high-rate gnss, real-time gnss, earthquake early warning, earthquake magnitude estimation, gnss displacement | keep | open_pdf_found |
| Real-Time High-Rate GNSS Displacements: Performance Demonstration During the 2019 Ridgecrest, CA Earthquakes | high-rate gnss, real-time gnss, earthquake source, gnss displacement, gnss displacements | keep | open_pdf_found |
| REGARD: A new GNSS‐based real‐time finite fault modeling system for GEONET | regard, coseismic displacement, finite fault | keep | closed_or_manual_required |
| Real-Time High-Rate GNSS Displacements: Performance Demonstration during the 2019 Ridgecrest, California, Earthquakes | high-rate gnss, earthquake source, gnss displacement, gnss displacements | keep | closed_or_manual_required |
| Earthquake magnitude scaling using seismogeodetic data | coseismic displacement, coseismic displacements, seismogeodetic | keep | open_pdf_found |
| Demonstration of the Cascadia G‐FAST Geodetic Earthquake Early Warning System for the Nisqually, Washington, Earthquake | geodetic earthquake early warning, earthquake early warning | keep | open_pdf_found |
| Quasi real‐time fault model estimation for near‐field tsunami forecasting based on RTK‐GPS analysis: Application to the 2011 Tohoku‐Oki earthquake (<i>M</i><sub>w</sub> 9.0) | coseismic displacement, tsunami forecasting | keep | open_pdf_found |
| Earthquake magnitude calculation without saturation from the scaling of peak ground displacement | earthquake early warning, earthquake source | keep | open_pdf_found |
| Real-time GPS seismology with a stand-alone receiver: A preliminary feasibility demonstration | coseismic displacement, coseismic displacements | keep | open_pdf_found |
| A new seismogeodetic approach applied to GPS and accelerometer observations of the 2012 Brawley seismic swarm: Implications for earthquake early warning | earthquake early warning, seismogeodetic | keep | open_pdf_found |
| Rupture kinematics of 2020 January 24 Mw 6.7 Doğanyol-Sivrice, Turkey earthquake on the East Anatolian Fault Zone imaged by space geodesy | high-rate gnss, earthquake source, peak ground velocities | keep | closed_or_manual_required |
| Real‐time capture of seismic waves using high‐rate multi‐GNSS observations: Application to the 2015 <i> M <sub>w</sub> </i>  7.8 Nepal earthquake | earthquake early warning, tsunami forecasting, seismic waves | keep | open_pdf_found |
| Temporal point positioning approach for real‐time GNSS seismology using a single receiver | gnss seismology, coseismic displacement, coseismic displacements | keep | open_pdf_found |
| G‐FAST Earthquake Early Warning Potential for Great Earthquakes in Chile | g-fast, earthquake early warning | keep | open_landing_page_or_oa_no_pdf |

## 5. 结论

粗筛后，明显偏离地震学/GNSS 地震预警主题的结果被降级为 maybe 或 discard。保留结果的主题集中度明显高于 OpenAlex 原始结果。

当前脚本是规则型粗筛，不替代后续 LLM 精筛和人工判断。下一步可以对 Keep 和 Maybe 论文运行 `paper_screening_prompt.md`，进一步判断是否进入全文阅读。