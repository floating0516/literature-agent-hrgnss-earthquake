# 扩大规模候选论文优先清单

> 基于 broad search + 规则粗筛生成。该清单用于第二批人工/LLM 精筛和全文精读优先级判断。

## 1. 总览

- 输入候选：285
- Keep：82
- Maybe：100
- Discard：103

## 2. 类别覆盖（Keep + Maybe）

- gnss_geodetic: 145
- source_fault: 96
- eew: 89
- deep_learning_or_ml: 58
- tsunami: 44
- named_system: 27

## A. GNSS / geodetic EEW 核心线

| # | Decision | Year | Cited | Fulltext | Title | DOI | Reason |
|---:|---|---:|---:|---|---|---|---|
| 1 | keep | 2016 | 65 | open_pdf_found | First result from the GEONET real-time analysis system (REGARD): the case of the 2016 Kumamoto earthquakes | 10.1186/s40623-016-0564-4 | matched strong topic terms: regard, coseismic displacement, coseismic displacements, earthquake early warning; matched high-value system/method terms: regard |
| 2 | keep | 2021 | 30 | open_pdf_found | Earthquake Magnitude Estimation from High-Rate GNSS Data: A Case Study of the 2021 Mw 7.3 Maduo Earthquake | 10.3390/rs13214478 | matched strong topic terms: high-rate gnss, real-time gnss, earthquake early warning, earthquake magnitude estimation, gnss displacement |
| 3 | keep | 2019 | 7 | open_pdf_found | Real-Time High-Rate GNSS Displacements: Performance Demonstration During the 2019 Ridgecrest, CA Earthquakes | 10.31223/osf.io/pdxqw | matched strong topic terms: high-rate gnss, real-time gnss, earthquake source, gnss displacement, gnss displacements |
| 4 | keep | 2017 | 88 | closed_or_manual_required | REGARD: A new GNSS‐based real‐time finite fault modeling system for GEONET | 10.1002/2016jb013485 | matched strong topic terms: regard, coseismic displacement, finite fault; matched high-value system/method terms: regard |
| 5 | keep | 2019 | 64 | closed_or_manual_required | Real-Time High-Rate GNSS Displacements: Performance Demonstration during the 2019 Ridgecrest, California, Earthquakes | 10.1785/0220190223 | matched strong topic terms: high-rate gnss, earthquake source, gnss displacement, gnss displacements |
| 6 | keep | 2013 | 125 | open_pdf_found | Earthquake magnitude scaling using seismogeodetic data | 10.1002/2013gl058391 | matched strong topic terms: coseismic displacement, coseismic displacements, seismogeodetic |
| 7 | keep | 2016 | 111 | open_pdf_found | Demonstration of the Cascadia G‐FAST Geodetic Earthquake Early Warning System for the Nisqually, Washington, Earthquake | 10.1785/0220150255 | matched strong topic terms: geodetic earthquake early warning, earthquake early warning; matched high-value system/method terms: shakealert |
| 8 | keep | 2011 | 240 | open_pdf_found | Quasi real‐time fault model estimation for near‐field tsunami forecasting based on RTK‐GPS analysis: Application to the 2011 Tohoku‐Oki earthquake (<i>M</i><sub>w</sub> 9.0) | 10.1029/2011jb008750 | matched strong topic terms: coseismic displacement, tsunami forecasting |
| 9 | keep | 2015 | 165 | open_pdf_found | Earthquake magnitude calculation without saturation from the scaling of peak ground displacement | 10.1002/2015gl064278 | matched strong topic terms: earthquake early warning, earthquake source |
| 10 | keep | 2011 | 150 | open_pdf_found | Real-time GPS seismology with a stand-alone receiver: A preliminary feasibility demonstration | 10.1029/2010jb007941 | matched strong topic terms: coseismic displacement, coseismic displacements |
| 11 | keep | 2013 | 150 | open_pdf_found | A new seismogeodetic approach applied to GPS and accelerometer observations of the 2012 Brawley seismic swarm: Implications for earthquake early warning | 10.1002/ggge.20144 | matched strong topic terms: earthquake early warning, seismogeodetic |
| 12 | keep | 2015 | 68 | open_pdf_found | Real‐time capture of seismic waves using high‐rate multi‐GNSS observations: Application to the 2015 <i> M <sub>w</sub> </i>  7.8 Nepal earthquake | 10.1002/2015gl067044 | matched strong topic terms: earthquake early warning, tsunami forecasting, seismic waves |
| 13 | keep | 2013 | 56 | open_pdf_found | Temporal point positioning approach for real‐time GNSS seismology using a single receiver | 10.1002/2013gl057818 | matched strong topic terms: gnss seismology, coseismic displacement, coseismic displacements |
| 14 | keep | 2018 | 53 | open_landing_page_or_oa_no_pdf | G‐FAST Earthquake Early Warning Potential for Great Earthquakes in Chile | 10.1785/0220170180 | matched strong topic terms: g-fast, earthquake early warning; matched high-value system/method terms: g-fast |
| 15 | keep | 2017 | 19 | open_pdf_found | GPS Seismology for a moderate magnitude earthquake: Lessons learned from the analysis of the 31 October 2013 ML 6.4 Ruisui (Taiwan) earthquake | 10.4401/ag-7399 | matched strong topic terms: regard, seismic waves; matched high-value system/method terms: regard |
| 16 | keep | 2021 | 10 | open_pdf_found | Real-Time Coseismic Displacement Retrieval Based on Temporal Point Positioning with IGS RTS Correction Products | 10.3390/s21020334 | matched strong topic terms: high-rate gnss, coseismic displacement, coseismic displacements |
| 17 | keep | 2018 | 8 | open_pdf_found | Augmenting Onshore GNSS Displacements With Offshore Observations to Improve Slip Characterization for Cascadia Subduction Zone Earthquakes | 10.1029/2018gl078233 | matched strong topic terms: slip characterization, gnss displacement, gnss displacements |
| 18 | keep | 2016 | 89 | open_pdf_found | Local tsunami warnings: Perspectives from recent large events | 10.1002/2015gl067100 | matched strong topic terms: earthquake early warning, earthquake source |
| 19 | keep | 2019 | 78 | open_pdf_found | Unravelling the contribution of early postseismic deformation using sub-daily GNSS positioning | 10.1038/s41598-019-39038-z | matched strong topic terms: regard; matched high-value system/method terms: regard |
| 20 | keep | 2014 | 67 | open_landing_page_or_oa_no_pdf | Review on Near-Field Tsunami Forecasting from Offshore Tsunami Data and Onshore GNSS Data for Tsunami Early Warning | 10.20965/jdr.2014.p0339 | matched strong topic terms: real-time gnss, tsunami forecasting |

## B. finite-fault / source characterization 线

| # | Decision | Year | Cited | Fulltext | Title | DOI | Reason |
|---:|---|---:|---:|---|---|---|---|
| 1 | keep | 2016 | 65 | open_pdf_found | First result from the GEONET real-time analysis system (REGARD): the case of the 2016 Kumamoto earthquakes | 10.1186/s40623-016-0564-4 | matched strong topic terms: regard, coseismic displacement, coseismic displacements, earthquake early warning; matched high-value system/method terms: regard |
| 2 | keep | 2021 | 30 | open_pdf_found | Earthquake Magnitude Estimation from High-Rate GNSS Data: A Case Study of the 2021 Mw 7.3 Maduo Earthquake | 10.3390/rs13214478 | matched strong topic terms: high-rate gnss, real-time gnss, earthquake early warning, earthquake magnitude estimation, gnss displacement |
| 3 | keep | 2019 | 7 | open_pdf_found | Real-Time High-Rate GNSS Displacements: Performance Demonstration During the 2019 Ridgecrest, CA Earthquakes | 10.31223/osf.io/pdxqw | matched strong topic terms: high-rate gnss, real-time gnss, earthquake source, gnss displacement, gnss displacements |
| 4 | keep | 2017 | 88 | closed_or_manual_required | REGARD: A new GNSS‐based real‐time finite fault modeling system for GEONET | 10.1002/2016jb013485 | matched strong topic terms: regard, coseismic displacement, finite fault; matched high-value system/method terms: regard |
| 5 | keep | 2019 | 64 | closed_or_manual_required | Real-Time High-Rate GNSS Displacements: Performance Demonstration during the 2019 Ridgecrest, California, Earthquakes | 10.1785/0220190223 | matched strong topic terms: high-rate gnss, earthquake source, gnss displacement, gnss displacements |
| 6 | keep | 2013 | 125 | open_pdf_found | Earthquake magnitude scaling using seismogeodetic data | 10.1002/2013gl058391 | matched strong topic terms: coseismic displacement, coseismic displacements, seismogeodetic |
| 7 | keep | 2016 | 111 | open_pdf_found | Demonstration of the Cascadia G‐FAST Geodetic Earthquake Early Warning System for the Nisqually, Washington, Earthquake | 10.1785/0220150255 | matched strong topic terms: geodetic earthquake early warning, earthquake early warning; matched high-value system/method terms: shakealert |
| 8 | keep | 2011 | 240 | open_pdf_found | Quasi real‐time fault model estimation for near‐field tsunami forecasting based on RTK‐GPS analysis: Application to the 2011 Tohoku‐Oki earthquake (<i>M</i><sub>w</sub> 9.0) | 10.1029/2011jb008750 | matched strong topic terms: coseismic displacement, tsunami forecasting |
| 9 | keep | 2015 | 165 | open_pdf_found | Earthquake magnitude calculation without saturation from the scaling of peak ground displacement | 10.1002/2015gl064278 | matched strong topic terms: earthquake early warning, earthquake source |
| 10 | keep | 2013 | 150 | open_pdf_found | A new seismogeodetic approach applied to GPS and accelerometer observations of the 2012 Brawley seismic swarm: Implications for earthquake early warning | 10.1002/ggge.20144 | matched strong topic terms: earthquake early warning, seismogeodetic |
| 11 | keep | 2020 | 81 | closed_or_manual_required | Rupture kinematics of 2020 January 24 Mw 6.7 Doğanyol-Sivrice, Turkey earthquake on the East Anatolian Fault Zone imaged by space geodesy | 10.1093/gji/ggaa345 | matched strong topic terms: high-rate gnss, earthquake source, peak ground velocities |
| 12 | keep | 2018 | 125 | open_landing_page_or_oa_no_pdf | Grond - A probabilistic earthquake source inversion framework | 10.5880/gfz.2.1.2018.003 | matched strong topic terms: earthquake source, finite fault |
| 13 | keep | 2018 | 8 | open_pdf_found | Augmenting Onshore GNSS Displacements With Offshore Observations to Improve Slip Characterization for Cascadia Subduction Zone Earthquakes | 10.1029/2018gl078233 | matched strong topic terms: slip characterization, gnss displacement, gnss displacements |
| 14 | keep | 2022 | 51 | closed_or_manual_required | The 29 July 2021 <i>M</i><sub><i>W</i></sub> 8.2 Chignik, Alaska Peninsula Earthquake Rupture Inferred From Seismic and Geodetic Observations: Re‐Rupture of the Western 2/3 of the 1938 Rupture Zone | 10.1029/2021gl096004 | matched strong topic terms: gnss displacement, gnss displacements |
| 15 | keep | 2019 | 19 | open_pdf_found | Seismogeodetic P‐wave Amplitude: No Evidence for Strong Determinism | 10.1029/2019gl083624 | matched strong topic terms: earthquake source, seismogeodetic |
| 16 | keep | 2024 | 6 | open_pdf_found | Simultaneous magnitude and slip distribution characterization from high-rate GNSS using deep learning: case studies of the 2021 <i>M</i>w 7.4 Maduo and 2023 Turkey doublet events | 10.1093/gji/ggae140 | matched strong topic terms: high-rate gnss, earthquake source |
| 17 | keep | 2008 | 341 | open_pdf_found | Heterogeneous coupling of the Sumatran megathrust constrained by geodetic and paleogeodetic measurements | 10.1029/2007jb004981 | weak or generic match to current topic |
| 18 | keep | 2016 | 305 | open_pdf_found | The role of space-based observation in understanding and responding to active tectonics and earthquakes | 10.1038/ncomms13844 | weak or generic match to current topic |
| 19 | keep | 2023 | 222 | open_pdf_found | Sub- and super-shear ruptures during the 2023 Mw 7.8 and Mw 7.6 earthquake doublet in SE Türkiye | 10.26443/seismica.v2i3.387 | weak or generic match to current topic |
| 20 | keep | 2021 | 94 | closed_or_manual_required | A Self-Supervised Deep Learning Approach for Blind Denoising and Waveform Coherence Enhancement in Distributed Acoustic Sensing Data | 10.1109/tnnls.2021.3132832 | matched strong topic terms: regard, earthquake source; matched high-value system/method terms: regard |

## C. deep learning / machine learning 线

| # | Decision | Year | Cited | Fulltext | Title | DOI | Reason |
|---:|---|---:|---:|---|---|---|---|
| 1 | keep | 2018 | 304 | open_pdf_found | Machine Learning Seismic Wave Discrimination: Application to Earthquake Early Warning | 10.1029/2018gl077870 | matched strong topic terms: earthquake early warning, seismic waves |
| 2 | keep | 2024 | 6 | open_pdf_found | Simultaneous magnitude and slip distribution characterization from high-rate GNSS using deep learning: case studies of the 2021 <i>M</i>w 7.4 Maduo and 2023 Turkey doublet events | 10.1093/gji/ggae140 | matched strong topic terms: high-rate gnss, earthquake source |
| 3 | keep | 2021 | 94 | closed_or_manual_required | A Self-Supervised Deep Learning Approach for Blind Denoising and Waveform Coherence Enhancement in Distributed Acoustic Sensing Data | 10.1109/tnnls.2021.3132832 | matched strong topic terms: regard, earthquake source; matched high-value system/method terms: regard |
| 4 | keep | 2023 | 53 | closed_or_manual_required | A Hybrid Deep Learning Model for Rapid Probabilistic Earthquake Source Parameter Estimation With Displacement Waveforms From a Flexible Set of Seismic or HR-GNSS Stations | 10.1109/tgrs.2023.3334729 | matched strong topic terms: earthquake source |
| 5 | keep | 2020 | 150 | open_pdf_found | Bayesian-Deep-Learning Estimation of Earthquake Location From Single-Station Observations | 10.1109/tgrs.2020.2988770 | matched strong topic terms: earthquake source, seismic waves |
| 6 | keep | 2023 | 79 | open_pdf_found | Magnitude estimation and ground motion prediction to harness fiber optic distributed acoustic sensing for earthquake early warning | 10.1038/s41598-023-27444-3 | matched strong topic terms: earthquake early warning, earthquake source |
| 7 | keep | 2024 | 9 | open_pdf_found | The Linked Complexity of Coseismic and Postseismic Faulting Revealed by Seismo‐Geodetic Dynamic Inversion of the 2004 Parkfield Earthquake | 10.1029/2024jb029410 | matched strong topic terms: g fast |
| 8 | keep | 2021 | 2 | open_pdf_found | Early warning for great earthquakes from characterization of crustal deformation patterns with deep learning | 10.31223/x5nw21 | matched strong topic terms: earthquake early warning |
| 9 | keep | 2020 | 148 | open_pdf_found | Automated Seismic Source Characterization Using Deep Graph Neural Networks | 10.1029/2020gl088690 | matched strong topic terms: earthquake early warning |
| 10 | keep | 2021 | 105 | closed_or_manual_required | A Deep Learning Model for Earthquake Parameters Observation in IoT System-Based Earthquake Early Warning | 10.1109/jiot.2021.3114420 | matched strong topic terms: earthquake early warning |
| 11 | keep | 2022 | 42 | open_pdf_found | Spatiotemporal Graph Convolutional Networks for Earthquake Source Characterization | 10.1029/2022jb024401 | matched strong topic terms: earthquake early warning, earthquake source |
| 12 | keep | 2022 | 37 | open_pdf_found | Instantaneous tracking of earthquake growth with elastogravity signals | 10.1038/s41586-022-04672-7 | matched strong topic terms: earthquake source, seismic waves |
| 13 | keep | 2022 | 35 | open_pdf_found | Early Peak Ground Acceleration Prediction for On-Site Earthquake Early Warning Using LSTM Neural Network | 10.3389/feart.2022.911947 | matched strong topic terms: earthquake early warning, seismic waves |
| 14 | keep | 2024 | 29 | open_pdf_found | Peak ground acceleration prediction for on-site earthquake early warning with deep learning | 10.1038/s41598-024-56004-6 | matched strong topic terms: earthquake early warning, seismic waves |
| 15 | keep | 2025 | 3 | open_pdf_found | PEGSGraph: A Graph Neural Network for Fast Earthquake Characterization Based on Prompt ElastoGravity Signals | 10.1029/2024jh000360 | matched strong topic terms: earthquake early warning, seismic waves |
| 16 | keep | 2023 | 3 | open_pdf_found | Accelerating low-frequency ground motion simulation for finite fault sources using neural networks | 10.1093/gji/ggad239 | matched strong topic terms: earthquake source, finite fault |
| 17 | maybe | 2024 | 160 | open_pdf_found | Flood Detection with SAR: A Review of Techniques and Datasets | 10.3390/rs16040656 | matched strong topic terms: regard; matched high-value system/method terms: regard |
| 18 | maybe | 2018 | 137 | open_pdf_found | Reliable Real‐Time Seismic Signal/Noise Discrimination With Machine Learning | 10.1029/2018jb016661 | matched strong topic terms: earthquake early warning |
| 19 | maybe | 2021 | 105 | open_pdf_found | Deep-Learning-Based Earthquake Detection for Fiber-Optic Distributed Acoustic Sensing | 10.1109/jlt.2021.3138724 | matched strong topic terms: seismic waves |
| 20 | maybe | 2024 | 80 | open_pdf_found | Recent advances in earthquake seismology using machine learning | 10.1186/s40623-024-01982-0 | weak or generic match to current topic |

## D. tsunami / 大震快速响应线

| # | Decision | Year | Cited | Fulltext | Title | DOI | Reason |
|---:|---|---:|---:|---|---|---|---|
| 1 | keep | 2011 | 240 | open_pdf_found | Quasi real‐time fault model estimation for near‐field tsunami forecasting based on RTK‐GPS analysis: Application to the 2011 Tohoku‐Oki earthquake (<i>M</i><sub>w</sub> 9.0) | 10.1029/2011jb008750 | matched strong topic terms: coseismic displacement, tsunami forecasting |
| 2 | keep | 2015 | 165 | open_pdf_found | Earthquake magnitude calculation without saturation from the scaling of peak ground displacement | 10.1002/2015gl064278 | matched strong topic terms: earthquake early warning, earthquake source |
| 3 | keep | 2011 | 150 | open_pdf_found | Real-time GPS seismology with a stand-alone receiver: A preliminary feasibility demonstration | 10.1029/2010jb007941 | matched strong topic terms: coseismic displacement, coseismic displacements |
| 4 | keep | 2015 | 68 | open_pdf_found | Real‐time capture of seismic waves using high‐rate multi‐GNSS observations: Application to the 2015 <i> M <sub>w</sub> </i>  7.8 Nepal earthquake | 10.1002/2015gl067044 | matched strong topic terms: earthquake early warning, tsunami forecasting, seismic waves |
| 5 | keep | 2013 | 56 | open_pdf_found | Temporal point positioning approach for real‐time GNSS seismology using a single receiver | 10.1002/2013gl057818 | matched strong topic terms: gnss seismology, coseismic displacement, coseismic displacements |
| 6 | keep | 2018 | 53 | open_landing_page_or_oa_no_pdf | G‐FAST Earthquake Early Warning Potential for Great Earthquakes in Chile | 10.1785/0220170180 | matched strong topic terms: g-fast, earthquake early warning; matched high-value system/method terms: g-fast |
| 7 | keep | 2018 | 8 | open_pdf_found | Augmenting Onshore GNSS Displacements With Offshore Observations to Improve Slip Characterization for Cascadia Subduction Zone Earthquakes | 10.1029/2018gl078233 | matched strong topic terms: slip characterization, gnss displacement, gnss displacements |
| 8 | keep | 2016 | 89 | open_pdf_found | Local tsunami warnings: Perspectives from recent large events | 10.1002/2015gl067100 | matched strong topic terms: earthquake early warning, earthquake source |
| 9 | keep | 2019 | 78 | open_pdf_found | Unravelling the contribution of early postseismic deformation using sub-daily GNSS positioning | 10.1038/s41598-019-39038-z | matched strong topic terms: regard; matched high-value system/method terms: regard |
| 10 | keep | 2014 | 67 | open_landing_page_or_oa_no_pdf | Review on Near-Field Tsunami Forecasting from Offshore Tsunami Data and Onshore GNSS Data for Tsunami Early Warning | 10.20965/jdr.2014.p0339 | matched strong topic terms: real-time gnss, tsunami forecasting |
| 11 | keep | 2019 | 19 | open_pdf_found | Seismogeodetic P‐wave Amplitude: No Evidence for Strong Determinism | 10.1029/2019gl083624 | matched strong topic terms: earthquake source, seismogeodetic |
| 12 | keep | 2024 | 6 | open_pdf_found | Simultaneous magnitude and slip distribution characterization from high-rate GNSS using deep learning: case studies of the 2021 <i>M</i>w 7.4 Maduo and 2023 Turkey doublet events | 10.1093/gji/ggae140 | matched strong topic terms: high-rate gnss, earthquake source |
| 13 | keep | 2008 | 341 | open_pdf_found | Heterogeneous coupling of the Sumatran megathrust constrained by geodetic and paleogeodetic measurements | 10.1029/2007jb004981 | weak or generic match to current topic |
| 14 | keep | 2018 | 81 | open_pdf_found | Seafloor crustal deformation data along the subduction zones around Japan obtained by GNSS-A observations | 10.1038/sdata.2018.182 | matched strong topic terms: earthquake source |
| 15 | keep | 2014 | 70 | open_pdf_found | tFISH/RAPiD: Rapid improvement of near‐field tsunami forecasting based on offshore tsunami data by incorporating onshore GNSS data | 10.1002/2014gl059863 | matched strong topic terms: tsunami forecasting |
| 16 | keep | 2020 | 375 | open_pdf_found | MOWLAS: NIED observation network for earthquake, tsunami and volcano | 10.1186/s40623-020-01250-x | matched strong topic terms: earthquake early warning |
| 17 | keep | 2013 | 140 | open_pdf_found | Intense interface seismicity triggered by a shallow slow slip event in the Central Ecuador subduction zone | 10.1002/jgrb.50216 | weak or generic match to current topic |
| 18 | keep | 2018 | 30 | open_pdf_found | Broadband Velocities and Displacements From Integrated GPS and Accelerometer Data for High‐Rate Seismogeodesy | 10.1029/2018gl079425 | matched strong topic terms: seismic waves |
| 19 | keep | 2017 | 22 | open_pdf_found | Self‐contained local broadband seismogeodetic early warning system: Detection and location | 10.1002/2016jb013766 | matched strong topic terms: seismogeodetic |
| 20 | keep | 2020 | 16 | open_pdf_found | Toward Near‐Field Tsunami Forecasting Along the Cascadia Subduction Zone Using Rapid GNSS Source Models | 10.1029/2020jb019636 | matched strong topic terms: tsunami forecasting |

## 3. 建议第二批优先精读 Top 10

| # | Year | Cited | Fulltext | Title | DOI | Why |
|---:|---:|---:|---|---|---|---|
| 1 | 2021 | 30 | open_pdf_found | Earthquake Magnitude Estimation from High-Rate GNSS Data: A Case Study of the 2021 Mw 7.3 Maduo Earthquake | 10.3390/rs13214478 | gnss_geodetic, eew, source_fault |
| 2 | 2017 | 88 | closed_or_manual_required | REGARD: A new GNSS‐based real‐time finite fault modeling system for GEONET | 10.1002/2016jb013485 | gnss_geodetic, source_fault, named_system |
| 3 | 2013 | 125 | open_pdf_found | Earthquake magnitude scaling using seismogeodetic data | 10.1002/2013gl058391 | gnss_geodetic, eew, source_fault |
| 4 | 2011 | 240 | open_pdf_found | Quasi real‐time fault model estimation for near‐field tsunami forecasting based on RTK‐GPS analysis: Application to the 2011 Tohoku‐Oki earthquake (<i>M</i><sub>w</sub> 9.0) | 10.1029/2011jb008750 | gnss_geodetic, source_fault, tsunami, named_system |
| 5 | 2015 | 165 | open_pdf_found | Earthquake magnitude calculation without saturation from the scaling of peak ground displacement | 10.1002/2015gl064278 | gnss_geodetic, eew, source_fault, tsunami |
| 6 | 2011 | 150 | open_pdf_found | Real-time GPS seismology with a stand-alone receiver: A preliminary feasibility demonstration | 10.1029/2010jb007941 | gnss_geodetic, eew, tsunami |
| 7 | 2013 | 150 | open_pdf_found | A new seismogeodetic approach applied to GPS and accelerometer observations of the 2012 Brawley seismic swarm: Implications for earthquake early warning | 10.1002/ggge.20144 | gnss_geodetic, eew, source_fault |
| 8 | 2020 | 81 | closed_or_manual_required | Rupture kinematics of 2020 January 24 Mw 6.7 Doğanyol-Sivrice, Turkey earthquake on the East Anatolian Fault Zone imaged by space geodesy | 10.1093/gji/ggaa345 | gnss_geodetic, source_fault |
| 9 | 2015 | 68 | open_pdf_found | Real‐time capture of seismic waves using high‐rate multi‐GNSS observations: Application to the 2015 <i> M <sub>w</sub> </i>  7.8 Nepal earthquake | 10.1002/2015gl067044 | gnss_geodetic, eew, tsunami |
| 10 | 2013 | 56 | open_pdf_found | Temporal point positioning approach for real‐time GNSS seismology using a single receiver | 10.1002/2013gl057818 | gnss_geodetic, source_fault, tsunami |
