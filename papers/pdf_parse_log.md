# PDF 解析记录

> 该文件由 `scripts/parse_pdfs.py` 生成。当前使用 `pdftotext -layout` 做轻量解析。

| PDF | Parsed Markdown | Status | Notes |
|---|---|---|---|
| `papers/raw_pdf/2020_bayesian_deep_learning_estimation_of_earthquake_location_from.pdf` | `papers/parsed_md/2020_bayesian_deep_learning_estimation_of_earthquake_location_from.md` | success |  |
| `papers/raw_pdf/2021_early_forecasting_of_tsunami_inundation_from_tsunami_and.pdf` | `papers/parsed_md/2021_early_forecasting_of_tsunami_inundation_from_tsunami_and.md` | success |  |
| `papers/raw_pdf/2021_early_warning_for_great_earthquakes_from_characterization_of.pdf` | `papers/parsed_md/2021_early_warning_for_great_earthquakes_from_characterization_of.md` | success |  |
| `papers/raw_pdf/2021_real_time_determination_of_earthquake_focal_mechanism_via.pdf` | `papers/parsed_md/2021_real_time_determination_of_earthquake_focal_mechanism_via.md` | success |  |
| `papers/raw_pdf/2024_rapid_estimation_of_source_parameters_for_the_2022.pdf` | `papers/parsed_md/2024_rapid_estimation_of_source_parameters_for_the_2022.md` | success |  |
| `papers/raw_pdf/2024_recent_advances_in_earthquake_seismology_using_machine_learning.pdf` | `papers/parsed_md/2024_recent_advances_in_earthquake_seismology_using_machine_learning.md` | success |  |
| `papers/raw_pdf/crowell_2016_cascadia_gfast.pdf` | `papers/parsed_md/crowell_2016_cascadia_gfast.md` | success |  |
| `papers/raw_pdf/kawamoto_2016_regard_kumamoto.pdf` | `papers/parsed_md/kawamoto_2016_regard_kumamoto.md` | success |  |
| `papers/raw_pdf/melgar_2019_realtime_hr_gnss_ridgecrest.pdf` | `papers/parsed_md/melgar_2019_realtime_hr_gnss_ridgecrest.md` | success |  |

## 解析质量说明

当前解析方式能快速提取正文，但可能存在以下问题：

- 双栏论文的阅读顺序可能局部混乱；
- 图表、公式、页眉页脚可能混入正文；
- 参考文献会被完整保留，后续精读时应避免把参考文献当作正文结论；
- 如果后续需要更高质量解析，可以接入 GROBID、Marker 或 PyMuPDF。
