# 手动 PDF 匹配记录

> 该文件由 `scripts/match_manual_pdfs.py` 生成。仅匹配用户已经合法获得的本地 PDF，不联网、不绕过访问控制。

## 总览

- 模式：apply
- 手动 PDF 目录：papers/manual_pdf_inbox
- PDF 输出目录：papers/raw_pdf
- 结果文件：papers/pdf_download_results.jsonl
- 扫描 PDF：18
- 自动匹配：18
- 歧义：0
- 未匹配：0
- 已存在跳过：0

## 明细

| Source PDF | Matched Title | Year | Status | Target PDF | Method | Confidence | Note |
|---|---|---:|---|---|---|---|---|
| papers/manual_pdf_inbox/Geophysical Research Letters - 2015 - Geng - Real%E2%80%90time capture of seismic waves using high%E2%80%90rate multi%E2%80%90GNSS observations .pdf | Real‐time capture of seismic waves using high‐rate multi‐GNSS observations: Application to the 2015 <i> M <sub>w</sub> </i>  7.8 Nepal earthquake | 2015 | matched | papers/raw_pdf/2015_real_time_capture_of_seismic_waves_using_high.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/Geophysical Research Letters - 2017 - Melgar - Systematic Observations of the Slip Pulse Properties of Large Earthquake.pdf | Systematic Observations of the Slip Pulse Properties of Large Earthquake Ruptures | 2017 | matched | papers/raw_pdf/2017_systematic_observations_of_the_slip_pulse_properties_of.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/Geophysical Research Letters - 2017 - Ruhl - The value of real%E2%80%90time GNSS to earthquake early warning.pdf | The value of real‐time GNSS to earthquake early warning | 2017 | matched | papers/raw_pdf/2017_the_value_of_real_time_gnss_to_earthquake.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/Geophysical Research Letters - 2018 - Saunders - Augmenting Onshore GNSS Displacements With Offshore Observations to.pdf | Augmenting Onshore GNSS Displacements With Offshore Observations to Improve Slip Characterization for Cascadia Subduction Zone Earthquakes | 2018 | matched | papers/raw_pdf/2018_augmenting_onshore_gnss_displacements_with_offshore_observations_to.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/Geophysical Research Letters - 2022 - Chen - The 2021 Mw 7 4 Madoi Earthquake  An Archetype Bilateral Slip%E2%80%90Pulse Rupture.pdf | The 2021 <i>M</i><sub><i>w</i></sub> 7.4 Madoi Earthquake: An Archetype Bilateral Slip‐Pulse Rupture Arrested at a Splay Fault | 2022 | matched | papers/raw_pdf/2022_the_2021_i_m_i_sub_i_w.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/JGR Solid Earth - 2017 - Goldberg - Self%E2%80%90contained local broadband seismogeodetic early warning system  Detection and.pdf | Self‐contained local broadband seismogeodetic early warning system: Detection and location | 2017 | matched | papers/raw_pdf/2017_self_contained_local_broadband_seismogeodetic_early_warning_system.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/JGR Solid Earth - 2018 - Juhel - Earthquake Early Warning Using Future Generation Gravity Strainmeters.pdf | Earthquake Early Warning Using Future Generation Gravity Strainmeters | 2018 | matched | papers/raw_pdf/2018_earthquake_early_warning_using_future_generation_gravity_strainmeters.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/JGR Solid Earth - 2019 - Ruhl - Quantifying the Value of Real%E2%80%90Time Geodetic Constraints for Earthquake Early Warning Using.pdf | Quantifying the Value of Real‐Time Geodetic Constraints for Earthquake Early Warning Using a Global Seismic and Geodetic Data Set | 2019 | matched | papers/raw_pdf/2019_quantifying_the_value_of_real_time_geodetic_constraints.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/JGR Solid Earth - 2020 - Habboub - A Multiple Algorithm Approach to the Analysis of GNSS Coordinate Time Series for.pdf | A Multiple Algorithm Approach to the Analysis of GNSS Coordinate Time Series for Detecting Geohazards and Anomalies | 2020 | matched | papers/raw_pdf/2020_a_multiple_algorithm_approach_to_the_analysis_of.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/Journal of Geophysical Research  Solid Earth - 2011 - Colosimo - Real%E2%80%90time GPS seismology with a stand%E2%80%90alone receiver  A.pdf | Real-time GPS seismology with a stand-alone receiver: A preliminary feasibility demonstration | 2011 | matched | papers/raw_pdf/2011_real_time_gps_seismology_with_a_stand_alone.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/Toward Near_Field Tsunami Forecasting Along the Cascadia Subducti.pdf | Toward Near‐Field Tsunami Forecasting Along the Cascadia Subduction Zone Using Rapid GNSS Source Models | 2020 | matched | papers/raw_pdf/2020_toward_near_field_tsunami_forecasting_along_the_cascadia.pdf | title_year_strong | medium | Title and year matched strongly |
| papers/manual_pdf_inbox/feart-09-685879.pdf | FinDerS(+): Real-Time Earthquake Slip Profiles and Magnitudes Estimated from Backprojected Displacement with Consideration of Fault Source Maturity Gradient | 2021 | matched | papers/raw_pdf/2021_finders_real_time_earthquake_slip_profiles_and_magnitudes.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/ggu113.pdf | Real-time GNSS seismology using a single receiver | 2014 | matched | papers/raw_pdf/2014_real_time_gnss_seismology_using_a_single_receiver.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/ggy198.pdf | Detection of ground motions using high-rate GPS time-series | 2018 | matched | papers/raw_pdf/2018_detection_of_ground_motions_using_high_rate_gps.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/remotesensing-13-04478.pdf | Earthquake Magnitude Estimation from High-Rate GNSS Data: A Case Study of the 2021 Mw 7.3 Maduo Earthquake | 2021 | matched | papers/raw_pdf/2021_earthquake_magnitude_estimation_from_high_rate_gnss_data.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/s00190-020-01449-6.pdf | Regularized reconstruction of peak ground velocity and acceleration from very high-rate GNSS precise point positioning with applications to the 2013 Lushan Mw6.6 earthquake | 2021 | matched | papers/raw_pdf/2021_regularized_reconstruction_of_peak_ground_velocity_and_acceleration.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/sensors-18-03712.pdf | Stand-Alone GNSS Sensors as Velocity Seismometers: Real-Time Monitoring and Earthquake Detection | 2018 | matched | papers/raw_pdf/2018_stand_alone_gnss_sensors_as_velocity_seismometers_real.pdf | doi_exact | high | DOI matched exactly |
| papers/manual_pdf_inbox/sensors-21-00334-v2.pdf | Real-Time Coseismic Displacement Retrieval Based on Temporal Point Positioning with IGS RTS Correction Products | 2021 | matched | papers/raw_pdf/2021_real_time_coseismic_displacement_retrieval_based_on_temporal.pdf | doi_exact | high | DOI matched exactly |
