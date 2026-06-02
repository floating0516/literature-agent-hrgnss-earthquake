# 筛选前后结果对比

> 目的：比较 OpenAlex 原始候选结果和粗筛后的结果，观察结构健康监测、UAV、桥梁监测等噪声是否被过滤。

## 1. 筛选前

OpenAlex 原始去重候选数量：44。由于 query 中包含 `GNSS`、`early warning` 等通用词，原始结果中混入了一些噪声，例如结构健康监测、UAV、桥梁监测、云计算 early warning、普通 GNSS 动态监测等。

## 2. 筛选后

- Keep：21
- Maybe：11
- Discard：12

Keep 结果主要集中在 HR-GNSS、real-time GNSS、G-FAST、geodetic earthquake early warning、GNSS seismology、coseismic displacement、ShakeAlert/REGARD/FinDerS 等方向。

## 3. 噪声过滤示例

| Title | Noise terms | Decision | Reason |
|---|---|---|---|
| Real-time GNSS seismology using a single receiver | ionospheric | maybe | matched strong topic terms: high-rate gnss, real-time gnss, gnss seismology, coseismic displacement, coseismic displacements; possible noise terms: ionospheric |
| GNSS total variometric approach: first demonstration of a tool for real-time tsunami genesis estimation | ionospheric | maybe | possible noise terms: ionospheric |
| Quasi-4-dimension ionospheric modeling and its application in PPP | ionospheric | discard | matched strong topic terms: regard; matched high-value system/method terms: regard; possible noise terms: ionospheric |
| Low-Cost GNSS and Real-Time PPP: Assessing the Precision of the u-blox ZED-F9P for Kinematic Monitoring Applications | kinematic monitoring applications, low-cost gnss | discard | possible noise terms: kinematic monitoring applications, low-cost gnss |
| Recent Advances of Structures Monitoring and Evaluation Using GPS-Time Series Monitoring Systems: A Review | structural health monitoring | discard | possible noise terms: structural health monitoring |
| Tsunami risk communication and management: Contemporary gaps and challenges | tsunami risk communication | discard | possible noise terms: tsunami risk communication |
| A Review of Global Navigation Satellite System (GNSS)-Based Dynamic Monitoring Technologies for Structural Health Monitoring | structural health monitoring | discard | matched strong topic terms: high-rate gnss; possible noise terms: structural health monitoring |
| Tectonic Inheritance During Plate Boundary Evolution in Southern California Constrained From Seismic Anisotropy | tectonic inheritance, seismic anisotropy | discard | possible noise terms: tectonic inheritance, seismic anisotropy |
| Towards Fully Autonomous UAVs: A Survey | uav, fully autonomous uavs | discard | possible noise terms: uav, fully autonomous uavs |
| A Systematic Review of Existing Early Warning Systems’ Challenges and Opportunities in Cloud Computing Early Warning Systems | cloud computing, early warning systems’ challenges | discard | possible noise terms: cloud computing, early warning systems’ challenges |
| Review of Bridge Structural Health Monitoring Based on GNSS: From Displacement Monitoring to Dynamic Characteristic Identification | structural health monitoring, bridge structural health, bridge | discard | possible noise terms: structural health monitoring, bridge structural health, bridge |
| A vision monitoring system for multipoint deflection of large‐span bridge based on camera networking | bridge, deflection | discard | possible noise terms: bridge, deflection |

## 4. 保留结果示例

| Title | Strong terms | Decision | Fulltext |
|---|---|---|---|
| First result from the GEONET real-time analysis system (REGARD): the case of the 2016 Kumamoto earthquakes | regard, coseismic displacement, coseismic displacements, earthquake early warning | keep | open_pdf_found |
| Earthquake Magnitude Estimation from High-Rate GNSS Data: A Case Study of the 2021 Mw 7.3 Maduo Earthquake | high-rate gnss, real-time gnss, earthquake early warning, earthquake magnitude estimation, gnss displacement | keep | open_pdf_found |
| Real-Time High-Rate GNSS Displacements: Performance Demonstration During the 2019 Ridgecrest, CA Earthquakes | high-rate gnss, real-time gnss, earthquake source, gnss displacement, gnss displacements | keep | open_pdf_found |
| Demonstration of the Cascadia G‐FAST Geodetic Earthquake Early Warning System for the Nisqually, Washington, Earthquake | geodetic earthquake early warning, earthquake early warning | keep | open_pdf_found |
| Real-time GPS seismology with a stand-alone receiver: A preliminary feasibility demonstration | coseismic displacement, coseismic displacements | keep | open_pdf_found |
| Real‐time capture of seismic waves using high‐rate multi‐GNSS observations: Application to the 2015 <i> M <sub>w</sub> </i>  7.8 Nepal earthquake | earthquake early warning, tsunami forecasting, seismic waves | keep | open_pdf_found |
| G‐FAST Earthquake Early Warning Potential for Great Earthquakes in Chile | g-fast, earthquake early warning | keep | open_landing_page_or_oa_no_pdf |
| Real-Time Coseismic Displacement Retrieval Based on Temporal Point Positioning with IGS RTS Correction Products | high-rate gnss, coseismic displacement, coseismic displacements | keep | open_pdf_found |
| Augmenting Onshore GNSS Displacements With Offshore Observations to Improve Slip Characterization for Cascadia Subduction Zone Earthquakes | slip characterization, gnss displacement, gnss displacements | keep | open_pdf_found |
| Quantifying the Value of Real‐Time Geodetic Constraints for Earthquake Early Warning Using a Global Seismic and Geodetic Data Set | geodetic earthquake early warning, earthquake early warning | keep | open_pdf_found |
| Real-time automatic uncertainty estimation of coseismic single rectangular fault model using GNSS data | regard | keep | open_pdf_found |
| Validation of Peak Ground Velocities Recorded on Very-high rate GNSS Against NGA-West2 Ground Motion Models | high rate gnss, peak ground velocities | keep | open_pdf_found |
| The value of real‐time GNSS to earthquake early warning | earthquake early warning | keep | open_pdf_found |
| Research to improve ShakeAlert earthquake early warning products and their utility | earthquake early warning | keep | open_pdf_found |
| Self‐contained local broadband seismogeodetic early warning system: Detection and location | seismogeodetic | keep | open_pdf_found |

## 5. 结论

粗筛后，明显偏离地震学/GNSS 地震预警主题的结果被降级为 maybe 或 discard。保留结果的主题集中度明显高于 OpenAlex 原始结果。

当前脚本是规则型粗筛，不替代后续 LLM 精筛和人工判断。下一步可以对 Keep 和 Maybe 论文运行 `paper_screening_prompt.md`，进一步判断是否进入全文阅读。