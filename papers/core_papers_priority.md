# 核心论文精筛优先级

> 基于 `papers/screening_results.md` 的规则粗筛结果，进一步人工/规则综合判断，选择最适合进入第一轮全文解析和精读测试的核心论文。

---

## 1. 精筛目标

从 44 篇 OpenAlex 候选论文中，优先选择与以下主题最相关的论文：

- HR-GNSS / high-rate GNSS；
- real-time GNSS / real-time GPS seismology；
- geodetic earthquake early warning；
- G-FAST / REGARD / ShakeAlert；
- coseismic displacement；
- earthquake magnitude estimation；
- rapid source characterization。

第一轮不追求覆盖所有方向，而是选 3 篇适合测试完整流程的论文：

```text
PDF 下载 → PDF 解析 → 单篇精读 → 阅读卡片 → 后续 RAG
```

---

## 2. 第一优先级：建议立即下载并精读

### 1. Demonstration of the Cascadia G-FAST Geodetic Earthquake Early Warning System for the Nisqually, Washington, Earthquake

- Year: 2016
- DOI: 10.1785/0220150255
- Fulltext: open PDF found
- PDF: https://www.geodesy.cwu.edu/about/pubs/Crowell_Etal_2016.pdf
- 方向：G-FAST、geodetic earthquake early warning、实时 GNSS 预警系统。

选择理由：

- 与 G-FAST 和 geodetic EEW 高度相关；
- 属于系统级论文，适合理解 GNSS 地震预警框架；
- 对后续 HR-GNSS 快速震源表征有直接背景价值。

---

### 2. First result from the GEONET real-time analysis system (REGARD): the case of the 2016 Kumamoto earthquakes

- Year: 2016
- DOI: 10.1186/s40623-016-0564-4
- Fulltext: open PDF found
- PDF: https://earth-planets-space.springeropen.com/track/pdf/10.1186/s40623-016-0564-4
- 方向：REGARD、实时 GNSS、同震位移、震源参数估计。

选择理由：

- REGARD 是日本 GEONET 实时分析系统，对 GNSS 快速震源估计非常重要；
- 案例是 2016 Kumamoto earthquakes，适合分析系统如何在真实事件中表现；
- 和 HR-GNSS / rapid source characterization 直接相关。

---

### 3. Earthquake Magnitude Estimation from High-Rate GNSS Data: A Case Study of the 2021 Mw 7.3 Maduo Earthquake

- Year: 2021
- DOI: 10.3390/rs13214478
- Fulltext: open PDF found
- PDF: https://www.mdpi.com/2072-4292/13/21/4478/pdf?version=1636370455
- 方向：HR-GNSS、震级估计、Maduo earthquake。

选择理由：

- 标题直接对应 high-rate GNSS + earthquake magnitude estimation；
- 与用户关注的 HR-GNSS 大震快速震源表征高度一致；
- 适合作为第一批精读样本。

---

## 3. 第二优先级：后续建议阅读

### 4. The value of real-time GNSS to earthquake early warning

- Year: 2017
- DOI: 10.1002/2017GL074502
- Fulltext: open PDF found
- 方向：real-time GNSS、earthquake early warning。

选择理由：

- 高引用；
- 适合写 Introduction / Related Work；
- 可帮助论证实时 GNSS 对 EEW 的价值。

### 5. Quantifying the Value of Real-Time Geodetic Constraints for Earthquake Early Warning Using a Global Seismic and Geodetic Data Set

- Year: 2019
- DOI: 10.1029/2018JB016935
- Fulltext: open PDF found
- 方向：real-time geodetic constraints、global dataset、EEW。

选择理由：

- 有全球地震与大地测量数据集；
- 适合提取评价指标和跨区域泛化思路。

### 6. Real-time GPS seismology with a stand-alone receiver: A preliminary feasibility demonstration

- Year: 2011
- DOI: 10.1029/2010JB007941
- Fulltext: open PDF found
- 方向：real-time GPS seismology、单站实时可行性。

选择理由：

- 较早的实时 GPS seismology 代表文献；
- 高引用；
- 适合作为历史背景。

### 7. Real-time GNSS seismology using a single receiver

- Year: 2014
- DOI: 10.1093/gji/ggu113
- Fulltext: open PDF found
- 方向：single receiver GNSS seismology。

选择理由：

- 与实时 GNSS seismology 相关；
- 可与 2011 年 GPS seismology 论文对比。

### 8. Real-Time High-Rate GNSS Displacements: Performance Demonstration During the 2019 Ridgecrest, CA Earthquakes

- Year: 2019
- DOI: 10.31223/osf.io/pdxqw
- Fulltext: open PDF found
- 方向：HR-GNSS、实时位移、Ridgecrest earthquakes。

选择理由：

- 直接讨论实时高频 GNSS 位移表现；
- 适合作为 HR-GNSS 数据处理和实际事件表现的参考。

### 9. Real-time capture of seismic waves using high-rate multi-GNSS observations: Application to the 2015 Mw 7.8 Nepal earthquake

- Year: 2015
- DOI: 10.1002/2015GL067044
- Fulltext: open PDF found
- 方向：high-rate multi-GNSS、地震波捕捉、Nepal earthquake。

选择理由：

- 与 high-rate GNSS 地震波观测相关；
- 对大震场景有参考价值。

### 10. G-FAST Earthquake Early Warning Potential for Great Earthquakes in Chile

- Year: 2018
- DOI: 10.1785/0220170180
- Fulltext: open landing page or OA no PDF
- 方向：G-FAST、大震预警、Chile。

选择理由：

- 与 G-FAST 大震应用高度相关；
- 当前 OpenAlex 没直接给 PDF，可后续通过 DOI/Unpaywall 或手动获取。

---

## 4. 第一轮精读建议

第一轮建议先精读 3 篇，覆盖不同系统/场景：

| Priority | Paper | Why |
|---:|---|---|
| 1 | Cascadia G-FAST demonstration | G-FAST / geodetic EEW 系统代表 |
| 2 | REGARD Kumamoto first result | 日本 GEONET 实时 GNSS 源估计系统代表 |
| 3 | Maduo high-rate GNSS magnitude estimation | 直接对应 HR-GNSS 震级估计 |

这样第一轮可以同时覆盖：

- 系统框架；
- 实时 GNSS 震源估计；
- high-rate GNSS 震级估计；
- 实际事件案例。

---

## 5. 后续策略

1. 先下载第一优先级 3 篇 PDF；
2. 解析成 Markdown；
3. 用 `prompts/paper_reading_prompt.md` 生成阅读卡片；
4. 再根据阅读质量决定是否扩展到第二优先级论文；
5. 如果后续需要补充深度学习相关论文，应另开搜索线，例如：
   - `deep learning earthquake magnitude estimation`
   - `deep learning earthquake early warning`
   - `machine learning GNSS earthquake magnitude`
