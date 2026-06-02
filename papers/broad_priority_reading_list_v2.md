# 增强筛选后的扩大候选优先清单

> 使用增强版 `screen_candidates.py` 生成，新增 deep learning/source characterization 正向词和主题分类。

## 1. 总览

- 输入候选：285
- keep: 141
- maybe: 72
- discard: 72

## 2. Keep + Maybe 主题覆盖

- other: 63
- tsunami_large_earthquake: 58
- deep_learning_eew: 56
- deep_learning_source_characterization: 56
- finite_fault_source_inversion: 37
- gnss_geodetic_eew: 36
- seismogeodesy_fusion: 23

## GNSS / geodetic EEW 核心线

| # | Decision | Score | Year | Cited | Fulltext | Title | DOI |
|---:|---|---:|---:|---:|---|---|---|
| 1 | keep | 5 | 2021 | 94 | closed_or_manual_required | A Self-Supervised Deep Learning Approach for Blind Denoising and Waveform Coherence Enhancement in Distributed Acoustic Sensing Data | 10.1109/tnnls.2021.3132832 |
| 2 | keep | 5 | 2024 | 6 | open_pdf_found | Simultaneous magnitude and slip distribution characterization from high-rate GNSS using deep learning: case studies of the 2021 <i>M</i>w 7.4 Maduo and 2023 Turkey doublet events | 10.1093/gji/ggae140 |
| 3 | keep | 5 | 2013 | 56 | open_pdf_found | Temporal point positioning approach for real‐time GNSS seismology using a single receiver | 10.1002/2013gl057818 |
| 4 | keep | 5 | 2018 | 53 | open_landing_page_or_oa_no_pdf | G‐FAST Earthquake Early Warning Potential for Great Earthquakes in Chile | 10.1785/0220170180 |
| 5 | keep | 5 | 2021 | 30 | open_pdf_found | Earthquake Magnitude Estimation from High-Rate GNSS Data: A Case Study of the 2021 Mw 7.3 Maduo Earthquake | 10.3390/rs13214478 |
| 6 | keep | 5 | 2024 | 6 | open_pdf_found | Fault geometry invariance and dislocation potential in antiplane crustal deformation: physics-informed simultaneous solutions | 10.1186/s40645-024-00654-7 |
| 7 | keep | 5 | 2017 | 88 | closed_or_manual_required | REGARD: A new GNSS‐based real‐time finite fault modeling system for GEONET | 10.1002/2016jb013485 |
| 8 | keep | 5 | 2022 | 51 | closed_or_manual_required | The 29 July 2021 <i>M</i><sub><i>W</i></sub> 8.2 Chignik, Alaska Peninsula Earthquake Rupture Inferred From Seismic and Geodetic Observations: Re‐Rupture of the Western 2/3 of the 1938 Rupture Zone | 10.1029/2021gl096004 |
| 9 | keep | 5 | 2017 | 19 | open_pdf_found | GPS Seismology for a moderate magnitude earthquake: Lessons learned from the analysis of the 31 October 2013 ML 6.4 Ruisui (Taiwan) earthquake | 10.4401/ag-7399 |
| 10 | keep | 5 | 2011 | 150 | open_pdf_found | Real-time GPS seismology with a stand-alone receiver: A preliminary feasibility demonstration | 10.1029/2010jb007941 |
| 11 | keep | 5 | 2020 | 81 | closed_or_manual_required | Rupture kinematics of 2020 January 24 Mw 6.7 Doğanyol-Sivrice, Turkey earthquake on the East Anatolian Fault Zone imaged by space geodesy | 10.1093/gji/ggaa345 |
| 12 | keep | 4 | 2021 | 10 | open_pdf_found | Real-Time Coseismic Displacement Retrieval Based on Temporal Point Positioning with IGS RTS Correction Products | 10.3390/s21020334 |
| 13 | keep | 4 | 2018 | 8 | open_pdf_found | Augmenting Onshore GNSS Displacements With Offshore Observations to Improve Slip Characterization for Cascadia Subduction Zone Earthquakes | 10.1029/2018gl078233 |
| 14 | keep | 4 | 2019 | 78 | open_pdf_found | Unravelling the contribution of early postseismic deformation using sub-daily GNSS positioning | 10.1038/s41598-019-39038-z |
| 15 | keep | 4 | 2014 | 67 | open_landing_page_or_oa_no_pdf | Review on Near-Field Tsunami Forecasting from Offshore Tsunami Data and Onshore GNSS Data for Tsunami Early Warning | 10.20965/jdr.2014.p0339 |

## Seismogeodesy / GNSS + strong motion 融合线

| # | Decision | Score | Year | Cited | Fulltext | Title | DOI |
|---:|---|---:|---:|---:|---|---|---|
| 1 | keep | 5 | 2022 | 51 | closed_or_manual_required | The 29 July 2021 <i>M</i><sub><i>W</i></sub> 8.2 Chignik, Alaska Peninsula Earthquake Rupture Inferred From Seismic and Geodetic Observations: Re‐Rupture of the Western 2/3 of the 1938 Rupture Zone | 10.1029/2021gl096004 |
| 2 | keep | 5 | 2013 | 125 | open_pdf_found | Earthquake magnitude scaling using seismogeodetic data | 10.1002/2013gl058391 |
| 3 | keep | 5 | 2017 | 19 | open_pdf_found | GPS Seismology for a moderate magnitude earthquake: Lessons learned from the analysis of the 31 October 2013 ML 6.4 Ruisui (Taiwan) earthquake | 10.4401/ag-7399 |
| 4 | keep | 5 | 2013 | 150 | open_pdf_found | A new seismogeodetic approach applied to GPS and accelerometer observations of the 2012 Brawley seismic swarm: Implications for earthquake early warning | 10.1002/ggge.20144 |
| 5 | keep | 5 | 2015 | 68 | open_pdf_found | Real‐time capture of seismic waves using high‐rate multi‐GNSS observations: Application to the 2015 <i> M <sub>w</sub> </i>  7.8 Nepal earthquake | 10.1002/2015gl067044 |
| 6 | keep | 4 | 2016 | 50 | closed_or_manual_required | Seismogeodesy Using GPS and Low‐Cost MEMS Accelerometers: Perspectives for Earthquake Early Warning and Rapid Response | 10.1785/0120160062 |
| 7 | keep | 4 | 2019 | 38 | open_pdf_found | Quantifying the Value of Real‐Time Geodetic Constraints for Earthquake Early Warning Using a Global Seismic and Geodetic Data Set | 10.1029/2018jb016935 |
| 8 | keep | 4 | 2019 | 19 | open_pdf_found | Seismogeodetic P‐wave Amplitude: No Evidence for Strong Determinism | 10.1029/2019gl083624 |
| 9 | keep | 4 | 2024 | 13 | open_pdf_found | The Multi‐Segment Complexity of the 2024 MW ${M}_{W}$ 7.5 Noto Peninsula Earthquake Governs Tsunami Generation | 10.1029/2024gl109790 |
| 10 | keep | 4 | 2023 | 10 | open_pdf_found | Validation of Peak Ground Velocities Recorded on Very-high rate GNSS Against NGA-West2 Ground Motion Models | 10.26443/seismica.v2i1.239 |
| 11 | keep | 3 | 2023 | 222 | open_pdf_found | Sub- and super-shear ruptures during the 2023 Mw 7.8 and Mw 7.6 earthquake doublet in SE Türkiye | 10.26443/seismica.v2i3.387 |
| 12 | keep | 3 | 2023 | 125 | open_pdf_found | Complex multi-fault rupture and triggering during the 2023 earthquake doublet in southeastern Türkiye | 10.1038/s41467-023-41404-5 |
| 13 | keep | 3 | 2018 | 30 | open_pdf_found | Broadband Velocities and Displacements From Integrated GPS and Accelerometer Data for High‐Rate Seismogeodesy | 10.1029/2018gl079425 |
| 14 | keep | 3 | 2017 | 22 | open_pdf_found | Self‐contained local broadband seismogeodetic early warning system: Detection and location | 10.1002/2016jb013766 |
| 15 | keep | 3 | 2024 | 9 | open_pdf_found | The Linked Complexity of Coseismic and Postseismic Faulting Revealed by Seismo‐Geodetic Dynamic Inversion of the 2004 Parkfield Earthquake | 10.1029/2024jb029410 |

## Finite-fault / source characterization 线

| # | Decision | Score | Year | Cited | Fulltext | Title | DOI |
|---:|---|---:|---:|---:|---|---|---|
| 1 | keep | 5 | 2023 | 53 | closed_or_manual_required | A Hybrid Deep Learning Model for Rapid Probabilistic Earthquake Source Parameter Estimation With Displacement Waveforms From a Flexible Set of Seismic or HR-GNSS Stations | 10.1109/tgrs.2023.3334729 |
| 2 | keep | 5 | 2021 | 94 | closed_or_manual_required | A Self-Supervised Deep Learning Approach for Blind Denoising and Waveform Coherence Enhancement in Distributed Acoustic Sensing Data | 10.1109/tnnls.2021.3132832 |
| 3 | keep | 5 | 2023 | 3 | open_pdf_found | Accelerating low-frequency ground motion simulation for finite fault sources using neural networks | 10.1093/gji/ggad239 |
| 4 | keep | 5 | 2020 | 150 | open_pdf_found | Bayesian-Deep-Learning Estimation of Earthquake Location From Single-Station Observations | 10.1109/tgrs.2020.2988770 |
| 5 | keep | 5 | 2024 | 6 | open_pdf_found | Simultaneous magnitude and slip distribution characterization from high-rate GNSS using deep learning: case studies of the 2021 <i>M</i>w 7.4 Maduo and 2023 Turkey doublet events | 10.1093/gji/ggae140 |
| 6 | keep | 5 | 2020 | 148 | open_pdf_found | Automated Seismic Source Characterization Using Deep Graph Neural Networks | 10.1029/2020gl088690 |
| 7 | keep | 5 | 2022 | 42 | open_pdf_found | Spatiotemporal Graph Convolutional Networks for Earthquake Source Characterization | 10.1029/2022jb024401 |
| 8 | keep | 5 | 2013 | 56 | open_pdf_found | Temporal point positioning approach for real‐time GNSS seismology using a single receiver | 10.1002/2013gl057818 |
| 9 | keep | 5 | 2018 | 125 | open_landing_page_or_oa_no_pdf | Grond - A probabilistic earthquake source inversion framework | 10.5880/gfz.2.1.2018.003 |
| 10 | keep | 5 | 2018 | 53 | open_landing_page_or_oa_no_pdf | G‐FAST Earthquake Early Warning Potential for Great Earthquakes in Chile | 10.1785/0220170180 |
| 11 | keep | 5 | 2024 | 6 | open_pdf_found | Fault geometry invariance and dislocation potential in antiplane crustal deformation: physics-informed simultaneous solutions | 10.1186/s40645-024-00654-7 |
| 12 | keep | 5 | 2017 | 88 | closed_or_manual_required | REGARD: A new GNSS‐based real‐time finite fault modeling system for GEONET | 10.1002/2016jb013485 |
| 13 | keep | 5 | 2022 | 51 | closed_or_manual_required | The 29 July 2021 <i>M</i><sub><i>W</i></sub> 8.2 Chignik, Alaska Peninsula Earthquake Rupture Inferred From Seismic and Geodetic Observations: Re‐Rupture of the Western 2/3 of the 1938 Rupture Zone | 10.1029/2021gl096004 |
| 14 | keep | 5 | 2023 | 33 | open_pdf_found | Earthquake Early Warning Starting From 3 s of Records on a Single Station With Machine Learning | 10.1029/2023jb026575 |
| 15 | keep | 5 | 2023 | 21 | open_pdf_found | Seismic Source Characterization From GNSS Data Using Deep Learning | 10.1029/2022jb024930 |

## Deep learning source characterization 线

| # | Decision | Score | Year | Cited | Fulltext | Title | DOI |
|---:|---|---:|---:|---:|---|---|---|
| 1 | keep | 5 | 2023 | 53 | closed_or_manual_required | A Hybrid Deep Learning Model for Rapid Probabilistic Earthquake Source Parameter Estimation With Displacement Waveforms From a Flexible Set of Seismic or HR-GNSS Stations | 10.1109/tgrs.2023.3334729 |
| 2 | keep | 5 | 2021 | 94 | closed_or_manual_required | A Self-Supervised Deep Learning Approach for Blind Denoising and Waveform Coherence Enhancement in Distributed Acoustic Sensing Data | 10.1109/tnnls.2021.3132832 |
| 3 | keep | 5 | 2023 | 3 | open_pdf_found | Accelerating low-frequency ground motion simulation for finite fault sources using neural networks | 10.1093/gji/ggad239 |
| 4 | keep | 5 | 2020 | 150 | open_pdf_found | Bayesian-Deep-Learning Estimation of Earthquake Location From Single-Station Observations | 10.1109/tgrs.2020.2988770 |
| 5 | keep | 5 | 2024 | 6 | open_pdf_found | Simultaneous magnitude and slip distribution characterization from high-rate GNSS using deep learning: case studies of the 2021 <i>M</i>w 7.4 Maduo and 2023 Turkey doublet events | 10.1093/gji/ggae140 |
| 6 | keep | 5 | 2020 | 148 | open_pdf_found | Automated Seismic Source Characterization Using Deep Graph Neural Networks | 10.1029/2020gl088690 |
| 7 | keep | 5 | 2022 | 42 | open_pdf_found | Spatiotemporal Graph Convolutional Networks for Earthquake Source Characterization | 10.1029/2022jb024401 |
| 8 | keep | 5 | 2025 | 3 | open_pdf_found | PEGSGraph: A Graph Neural Network for Fast Earthquake Characterization Based on Prompt ElastoGravity Signals | 10.1029/2024jh000360 |
| 9 | keep | 5 | 2021 | 133 | open_pdf_found | Real-time determination of earthquake focal mechanism via deep learning | 10.1038/s41467-021-21670-x |
| 10 | keep | 5 | 2021 | 105 | closed_or_manual_required | A Deep Learning Model for Earthquake Parameters Observation in IoT System-Based Earthquake Early Warning | 10.1109/jiot.2021.3114420 |
| 11 | keep | 5 | 2024 | 29 | open_pdf_found | Peak ground acceleration prediction for on-site earthquake early warning with deep learning | 10.1038/s41598-024-56004-6 |
| 12 | keep | 5 | 2024 | 6 | open_pdf_found | Fault geometry invariance and dislocation potential in antiplane crustal deformation: physics-informed simultaneous solutions | 10.1186/s40645-024-00654-7 |
| 13 | keep | 5 | 2018 | 304 | open_pdf_found | Machine Learning Seismic Wave Discrimination: Application to Earthquake Early Warning | 10.1029/2018gl077870 |
| 14 | keep | 5 | 2018 | 137 | open_pdf_found | Reliable Real‐Time Seismic Signal/Noise Discrimination With Machine Learning | 10.1029/2018jb016661 |
| 15 | keep | 5 | 2021 | 105 | open_pdf_found | Deep-Learning-Based Earthquake Detection for Fiber-Optic Distributed Acoustic Sensing | 10.1109/jlt.2021.3138724 |

## Deep learning / ML EEW 方法线

| # | Decision | Score | Year | Cited | Fulltext | Title | DOI |
|---:|---|---:|---:|---:|---|---|---|
| 1 | keep | 5 | 2023 | 53 | closed_or_manual_required | A Hybrid Deep Learning Model for Rapid Probabilistic Earthquake Source Parameter Estimation With Displacement Waveforms From a Flexible Set of Seismic or HR-GNSS Stations | 10.1109/tgrs.2023.3334729 |
| 2 | keep | 5 | 2021 | 94 | closed_or_manual_required | A Self-Supervised Deep Learning Approach for Blind Denoising and Waveform Coherence Enhancement in Distributed Acoustic Sensing Data | 10.1109/tnnls.2021.3132832 |
| 3 | keep | 5 | 2023 | 3 | open_pdf_found | Accelerating low-frequency ground motion simulation for finite fault sources using neural networks | 10.1093/gji/ggad239 |
| 4 | keep | 5 | 2020 | 150 | open_pdf_found | Bayesian-Deep-Learning Estimation of Earthquake Location From Single-Station Observations | 10.1109/tgrs.2020.2988770 |
| 5 | keep | 5 | 2024 | 6 | open_pdf_found | Simultaneous magnitude and slip distribution characterization from high-rate GNSS using deep learning: case studies of the 2021 <i>M</i>w 7.4 Maduo and 2023 Turkey doublet events | 10.1093/gji/ggae140 |
| 6 | keep | 5 | 2020 | 148 | open_pdf_found | Automated Seismic Source Characterization Using Deep Graph Neural Networks | 10.1029/2020gl088690 |
| 7 | keep | 5 | 2022 | 42 | open_pdf_found | Spatiotemporal Graph Convolutional Networks for Earthquake Source Characterization | 10.1029/2022jb024401 |
| 8 | keep | 5 | 2025 | 3 | open_pdf_found | PEGSGraph: A Graph Neural Network for Fast Earthquake Characterization Based on Prompt ElastoGravity Signals | 10.1029/2024jh000360 |
| 9 | keep | 5 | 2021 | 133 | open_pdf_found | Real-time determination of earthquake focal mechanism via deep learning | 10.1038/s41467-021-21670-x |
| 10 | keep | 5 | 2021 | 105 | closed_or_manual_required | A Deep Learning Model for Earthquake Parameters Observation in IoT System-Based Earthquake Early Warning | 10.1109/jiot.2021.3114420 |
| 11 | keep | 5 | 2024 | 29 | open_pdf_found | Peak ground acceleration prediction for on-site earthquake early warning with deep learning | 10.1038/s41598-024-56004-6 |
| 12 | keep | 5 | 2024 | 6 | open_pdf_found | Fault geometry invariance and dislocation potential in antiplane crustal deformation: physics-informed simultaneous solutions | 10.1186/s40645-024-00654-7 |
| 13 | keep | 5 | 2018 | 304 | open_pdf_found | Machine Learning Seismic Wave Discrimination: Application to Earthquake Early Warning | 10.1029/2018gl077870 |
| 14 | keep | 5 | 2018 | 137 | open_pdf_found | Reliable Real‐Time Seismic Signal/Noise Discrimination With Machine Learning | 10.1029/2018jb016661 |
| 15 | keep | 5 | 2021 | 105 | open_pdf_found | Deep-Learning-Based Earthquake Detection for Fiber-Optic Distributed Acoustic Sensing | 10.1109/jlt.2021.3138724 |

## Tsunami / 大震快速响应线

| # | Decision | Score | Year | Cited | Fulltext | Title | DOI |
|---:|---|---:|---:|---:|---|---|---|
| 1 | keep | 5 | 2024 | 6 | open_pdf_found | Simultaneous magnitude and slip distribution characterization from high-rate GNSS using deep learning: case studies of the 2021 <i>M</i>w 7.4 Maduo and 2023 Turkey doublet events | 10.1093/gji/ggae140 |
| 2 | keep | 5 | 2025 | 3 | open_pdf_found | PEGSGraph: A Graph Neural Network for Fast Earthquake Characterization Based on Prompt ElastoGravity Signals | 10.1029/2024jh000360 |
| 3 | keep | 5 | 2013 | 56 | open_pdf_found | Temporal point positioning approach for real‐time GNSS seismology using a single receiver | 10.1002/2013gl057818 |
| 4 | keep | 5 | 2018 | 53 | open_landing_page_or_oa_no_pdf | G‐FAST Earthquake Early Warning Potential for Great Earthquakes in Chile | 10.1785/0220170180 |
| 5 | keep | 5 | 2021 | 100 | open_pdf_found | Early forecasting of tsunami inundation from tsunami and geodetic observation data with convolutional neural networks | 10.1038/s41467-021-22348-0 |
| 6 | keep | 5 | 2011 | 240 | open_pdf_found | Quasi real‐time fault model estimation for near‐field tsunami forecasting based on RTK‐GPS analysis: Application to the 2011 Tohoku‐Oki earthquake (<i>M</i><sub>w</sub> 9.0) | 10.1029/2011jb008750 |
| 7 | keep | 5 | 2015 | 165 | open_pdf_found | Earthquake magnitude calculation without saturation from the scaling of peak ground displacement | 10.1002/2015gl064278 |
| 8 | keep | 5 | 2011 | 150 | open_pdf_found | Real-time GPS seismology with a stand-alone receiver: A preliminary feasibility demonstration | 10.1029/2010jb007941 |
| 9 | keep | 5 | 2015 | 68 | open_pdf_found | Real‐time capture of seismic waves using high‐rate multi‐GNSS observations: Application to the 2015 <i> M <sub>w</sub> </i>  7.8 Nepal earthquake | 10.1002/2015gl067044 |
| 10 | keep | 5 | 2021 | 2 | open_pdf_found | Early warning for great earthquakes from characterization of crustal deformation patterns with deep learning | 10.31223/x5nw21 |
| 11 | keep | 4 | 2013 | 140 | open_pdf_found | Intense interface seismicity triggered by a shallow slow slip event in the Central Ecuador subduction zone | 10.1002/jgrb.50216 |
| 12 | keep | 4 | 2022 | 37 | open_pdf_found | Instantaneous tracking of earthquake growth with elastogravity signals | 10.1038/s41586-022-04672-7 |
| 13 | keep | 4 | 2016 | 32 | open_pdf_found | <i>W</i> phase source inversion using high‐rate regional GPS data for large earthquakes | 10.1002/2016gl068302 |
| 14 | keep | 4 | 2016 | 25 | open_pdf_found | Retrieving real-time co-seismic displacements using GPS/GLONASS: a preliminary report from the September 2015<i>M</i><sub>w</sub>8.3 Illapel earthquake in Chile | 10.1093/gji/ggw190 |
| 15 | keep | 4 | 2018 | 8 | open_pdf_found | Augmenting Onshore GNSS Displacements With Offshore Observations to Improve Slip Characterization for Cascadia Subduction Zone Earthquakes | 10.1029/2018gl078233 |

## 9. 建议第二批精读 10 篇（平衡主题覆盖）

| # | Theme | Year | Cited | Fulltext | Title | DOI |
|---:|---|---:|---:|---|---|---|
| 1 | deep_learning_source_characterization | 2023 | 3 | open_pdf_found | Accelerating low-frequency ground motion simulation for finite fault sources using neural networks | 10.1093/gji/ggad239 |
| 2 | deep_learning_source_characterization | 2020 | 150 | open_pdf_found | Bayesian-Deep-Learning Estimation of Earthquake Location From Single-Station Observations | 10.1109/tgrs.2020.2988770 |
| 3 | deep_learning_source_characterization | 2024 | 6 | open_pdf_found | Simultaneous magnitude and slip distribution characterization from high-rate GNSS using deep learning: case studies of the 2021 <i>M</i>w 7.4 Maduo and 2023 Turkey doublet events | 10.1093/gji/ggae140 |
| 4 | gnss_geodetic_eew | 2013 | 56 | open_pdf_found | Temporal point positioning approach for real‐time GNSS seismology using a single receiver | 10.1002/2013gl057818 |
| 5 | gnss_geodetic_eew | 2021 | 30 | open_pdf_found | Earthquake Magnitude Estimation from High-Rate GNSS Data: A Case Study of the 2021 Mw 7.3 Maduo Earthquake | 10.3390/rs13214478 |
| 6 | seismogeodesy_fusion | 2013 | 125 | open_pdf_found | Earthquake magnitude scaling using seismogeodetic data | 10.1002/2013gl058391 |
| 7 | finite_fault_source_inversion | 2020 | 148 | open_pdf_found | Automated Seismic Source Characterization Using Deep Graph Neural Networks | 10.1029/2020gl088690 |
| 8 | finite_fault_source_inversion | 2022 | 42 | open_pdf_found | Spatiotemporal Graph Convolutional Networks for Earthquake Source Characterization | 10.1029/2022jb024401 |
| 9 | tsunami_large_earthquake | 2025 | 3 | open_pdf_found | PEGSGraph: A Graph Neural Network for Fast Earthquake Characterization Based on Prompt ElastoGravity Signals | 10.1029/2024jh000360 |
| 10 | deep_learning_eew | 2021 | 133 | open_pdf_found | Real-time determination of earthquake focal mechanism via deep learning | 10.1038/s41467-021-21670-x |
