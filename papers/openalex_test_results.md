# OpenAlex 小规模试跑结果

> 目的：测试用开放 API 做第一轮元数据搜索是否耗时，以及能否直接拿到开放全文线索。

## 测试方式

使用 OpenAlex API，对 3 条小 query 各取前 5 条结果：

1. `"high-rate GNSS" earthquake early warning`
2. `"geodetic earthquake early warning"`
3. `"G-FAST" GNSS earthquake`

每条 query 返回：标题、年份、引用数、DOI、开放获取状态、best OA location PDF URL。

## 速度

单条 query 大约 1.5–3.3 秒。

- `"high-rate GNSS" earthquake early warning`：约 3.3 秒，命中 188 条
- `"geodetic earthquake early warning"`：约 1.5 秒，命中 46 条
- `"G-FAST" GNSS earthquake`：约 2.1 秒，命中 61 条

结论：小规模 20–50 篇元数据搜索不会很浪费时间。即使 5 条搜索线，每条取 20–50 条，主要耗时也在几十秒到几分钟级别，瓶颈不在 metadata 搜索，而在后续筛选、PDF 解析和精读。

## 试跑发现

OpenAlex 结果中已经包含较有用的字段：

```yaml
open_access:
  is_oa:
  oa_status:
best_oa_location:
  pdf_url:
```

这说明第一版可以先用 OpenAlex 做：

1. 元数据搜索；
2. 开放获取状态判断；
3. 初步 PDF URL 获取；
4. 后续再用 Unpaywall 补充和校验。

## 示例结果

### Query 1: `"high-rate GNSS" earthquake early warning`

命中 188 条。

代表结果：

1. Local Tsunami Warnings and the role of high-rate GNSS in Earthquake Early Warning  
   - Year: 2016
   - OA: closed
   - DOI: None
   - PDF: None

2. Real-time high rate GNSS techniques for earthquake monitoring and early warning  
   - Year: 2015
   - OA: green
   - DOI: https://doi.org/10.14279/depositonce-4585
   - PDF / OA location: http://depositonce.tu-berlin.de/handle/11303/4882

3. Earthquake Magnitude Estimation from High-Rate GNSS Data: A Case Study of the 2021 Mw 7.3 Maduo Earthquake  
   - Year: 2021
   - OA: gold
   - DOI: https://doi.org/10.3390/rs13214478
   - PDF: https://www.mdpi.com/2072-4292/13/21/4478/pdf?version=1636370455

4. Real-time GNSS seismology using a single receiver  
   - Year: 2014
   - OA: bronze
   - DOI: https://doi.org/10.1093/gji/ggu113
   - PDF: https://academic.oup.com/gji/article-pdf/198/1/72/17175629/ggu113.pdf

5. GNSS for Quasi-Real-Time Earthquake Source Determination in Eastern Tibet: A Prototype System toward Early Warning Applications  
   - Year: 2021
   - OA: closed
   - DOI: https://doi.org/10.1785/0220190244
   - PDF: None

### Query 2: `"geodetic earthquake early warning"`

命中 46 条。

代表结果：

1. Demonstration of the Cascadia G-FAST Geodetic Earthquake Early Warning System for the Nisqually, Washington, Earthquake  
   - Year: 2016
   - OA: green
   - DOI: https://doi.org/10.1785/0220150255
   - PDF: https://www.geodesy.cwu.edu/about/pubs/Crowell_Etal_2016.pdf

2. Quantifying the Value of Real-Time Geodetic Constraints for Earthquake Early Warning Using a Global Seismic and Geodetic Data Set  
   - Year: 2019
   - OA: bronze
   - DOI: https://doi.org/10.1029/2018jb016935
   - PDF: https://agupubs.onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2018JB016935

3. The value of real-time GNSS to earthquake early warning  
   - Year: 2017
   - OA: bronze
   - DOI: https://doi.org/10.1002/2017gl074502
   - PDF: https://agupubs.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2017GL074502

### Query 3: `"G-FAST" GNSS earthquake`

命中 61 条。

代表结果：

1. G-FAST Earthquake Early Warning Potential for Great Earthquakes in Chile  
   - Year: 2018
   - OA: green
   - DOI: https://doi.org/10.1785/0220170180
   - PDF: None in OpenAlex result

2. Revised technical implementation plan for the ShakeAlert system—An earthquake early warning system for the West Coast of the United States  
   - Year: 2018
   - OA: diamond
   - DOI: https://doi.org/10.3133/ofr20181155
   - PDF: https://pubs.usgs.gov/of/2018/1155/ofr20181155.pdf

3. First result from the GEONET real-time analysis system (REGARD): the case of the 2016 Kumamoto earthquakes  
   - Year: 2016
   - OA: gold
   - DOI: https://doi.org/10.1186/s40623-016-0564-4
   - PDF: https://earth-planets-space.springeropen.com/track/pdf/10.1186/s40623-016-0564-4

## 结论

1. 只用 OpenAlex 先做第一轮搜索是可行的。
2. 搜索速度不慢，不会成为主要时间成本。
3. OpenAlex 已能返回不少 OA 状态和 PDF URL。
4. 但 OpenAlex 的 PDF URL 可能不完整，有些 green OA 只有 landing page 或没有 PDF，因此后续最好用 Unpaywall 对 DOI 再补查一次。
5. 为了避免流程过复杂，第一版可以不同时接入太多 API：
   - 第一轮：OpenAlex；
   - 第二步：Unpaywall 查 DOI 的开放全文；
   - 第三步：对闭源核心论文标记人工下载。
