# Prompt 模板的作用说明与开源参考

> 本文解释为什么文献阅读 Agent 需要不同类型的 prompt 模板，并记录当前参考过的开源项目、Prompt/Skill 设计思路和可借鉴点。

---

## 1. 为什么需要 Prompt 模板？

在文献阅读 Agent 中，prompt 模板不是为了“写几句好看的提示词”，而是为了把不同阶段的任务标准化。

如果没有模板，Agent 每次读论文时输出格式、关注重点和证据要求都会不稳定。长期积累知识库时会出现几个问题：

1. 每篇阅读笔记字段不同，后续难以比较；
2. 有些论文总结了方法，有些只总结了结论；
3. 重要信息如数据、指标、局限、可复现性容易遗漏；
4. 跨文献综合时无法自动汇总；
5. 容易出现没有来源的强结论；
6. 后续 RAG chunk 缺少统一 metadata。

因此，prompt 模板的作用是把文献阅读流程拆成固定任务：

```text
摘要级筛选 → 单篇精读 → 跨文献综合 → 批判审查
```

每个模板都对应一个明确的 Agent 角色和产出格式。

---

## 2. 几类 Prompt 的作用

### 2.1 精读 Prompt：Paper Reading Prompt

文件：`paper_reading_prompt.md`

作用：

> 把一篇论文转化为结构化阅读卡片。

它关注的是单篇论文本身，包括：

- 研究问题；
- 背景动机；
- 数据；
- 方法；
- 评价指标；
- 主要结果；
- 优点；
- 局限；
- 与本人研究的关系；
- 可引用观点；
- 需要人工核查的内容。

为什么需要它：

- 保证每篇论文都按同一结构阅读；
- 方便后续横向比较；
- 方便自动提取 metadata 和 tags；
- 避免只生成泛泛摘要；
- 让阅读笔记直接服务于论文写作和研究设计。

适用阶段：

```text
PDF/全文解析完成后 → 对核心论文进行 Level 3 精读
```

---

### 2.2 综合 Prompt：Synthesis Prompt

文件：`synthesis_prompt.md`

作用：

> 把多篇论文合并成主题综述、方法对比和研究空白分析。

它不是逐篇复述，而是提取跨文献信息：

- 主要研究路线；
- 方法对比；
- 数据和 benchmark；
- 评价指标；
- 多篇论文共同支持的结论；
- 文献之间的冲突；
- 研究空白；
- 可检验假说；
- 对本人论文写作的帮助。

为什么需要它：

- RAG 检索只能找到片段，综合 prompt 负责组织知识；
- 论文写作需要的是“领域图景”，不是单篇摘要；
- 可以帮助从文献中生成研究问题和实验设计；
- 可以形成 `synthesis/` 目录下的综述型知识。

适用阶段：

```text
多篇阅读卡片完成后 → 生成主题综述 / 方法对比 / 假说清单
```

---

### 2.3 批判 Prompt：Critic Prompt

文件：`critic_prompt.md`

作用：

> 审查阅读笔记、综述或假说是否可靠。

它的角色类似审稿人或反对者，重点检查：

- 是否有伪造引用；
- 是否有无证据结论；
- 是否过度推断；
- 是否忽略关键局限；
- 假说是否可检验；
- 方法是否存在数据泄漏、区域偏差、baseline 不合理等问题；
- 结论是否符合 GNSS 和地震学物理常识。

为什么需要它：

- LLM 容易把合理推测写成确定事实；
- 文献综述最怕“看起来顺但没有证据”；
- 后续写 SRL paper 时必须避免伪造引用和 unsupported claims；
- 对科研来说，批判审查比单纯总结更重要。

适用阶段：

```text
阅读卡片或综述生成后 → 进入知识库前 / 写论文前进行审查
```

---

### 2.4 筛选 Prompt：Paper Screening Prompt

文件：`paper_screening_prompt.md`

作用：

> 根据标题和摘要判断论文是否值得继续读。

它对应 Level 1 初筛，主要输出：

- relevance score；
- keep / maybe / discard；
- matched topics；
- possible use；
- next action。

为什么需要它：

- 避免一开始下载大量低相关 PDF；
- 节约后续解析和精读成本；
- 为文献池建立优先级。

---

## 3. 开源项目和 Prompt/Skill 参考

以下参考主要用于借鉴工作流、证据追踪、结构化输出和批判审查方式。后续实现时可以继续深入阅读其仓库内容。

### 3.1 FutureHouse PaperQA / PaperQA2

链接：[Future-House/paper-qa](https://github.com/Future-House/paper-qa)

可借鉴点：

- 面向科学文献的 Agentic RAG；
- 支持本地论文索引、metadata 查询、retrieval、reranking；
- 强调 citation-grounded answers；
- 追踪 evidence chunks、relevance scores、source limits；
- 可接入 Semantic Scholar、Crossref、Unpaywall；
- 支持自定义 QA prompt、summary prompt、post-processing prompt；
- post prompt 可用于 critique answer。

对当前项目的启发：

> 文献问答和综述必须有证据来源，RAG 结果应保留 chunk metadata 和 citation，而不是让模型自由发挥。

建议后续重点参考：

- evidence selection；
- answer citation；
- summary prompt；
- answer critique/post-processing。

---

### 3.2 ByteDance DeerFlow systematic-literature-review Skill

链接：[bytedance/deer-flow systematic-literature-review skill](https://github.com/bytedance/deer-flow/blob/main/skills/public/systematic-literature-review/SKILL.md)

可借鉴点：

- 先明确 scope：主题、论文数量、时间范围、citation style、保存路径；
- 默认 20 篇论文，50 篇作为上限；
- 检索时先压缩成 2–3 个核心关键词，不要写很长 query；
- 用日期、类别等过滤条件缩小范围；
- 读取多篇论文时可分批，每批约 5 篇；
- 要求结构化 JSON 返回；
- 综合时关注 recurring lines of work、shared findings、disagreements、gaps；
- 如果文献太少或太混杂，要明确说明，不能强行总结主题。

对当前项目的启发：

> 系统性文献综述要先定义范围，再检索，再批量提取，再跨文献综合。综合部分必须比较和组合研究，而不是逐篇罗列。

已吸收到当前模板中的设计：

- `synthesis_prompt.md` 中的 main research lines、agreements、disagreements、research gaps；
- `paper_screening_prompt.md` 中的筛选和优先级判断；
- 后续可以借鉴其“每批约 5 篇”的批量处理策略。

---

### 3.3 NeuroDong Ai-Review-Prompt

链接：[NeuroDong/Ai-Review-Prompt](https://github.com/NeuroDong/Ai-Review-Prompt)

可借鉴点：

- 用固定 review schema 输出 Strengths、Weaknesses、Suggestions；
- 支持 PDF 页面图像输入，考虑图、公式、排版；
- 可比较不同 prompt 风格在同一篇论文上的表现；
- 强调公式、符号、图表质量、页面组织的检查；
- 可加入 few-shot 示例来稳定 review 风格；
- 包含对 PDF 隐藏指令攻击的检查意识。

对当前项目的启发：

> 批判 prompt 不应只说“这篇论文有什么局限”，还应像审稿人一样给出 major issues、minor issues、actionable revision plan，并检查图表、公式、方法合理性和潜在安全/污染问题。

已吸收到当前模板中的设计：

- `critic_prompt.md` 中的 major issues、minor issues、unsupported claims、citation check、methodological critique、geophysical plausibility check。

---

### 3.4 Stephen Turner paper summary prompt gist

链接：[Paper summary prompt gist](https://gist.github.com/stephenturner/44e5ca5301b05f06f375085f74c67f03)

可借鉴点：

- 两阶段流程：先提取，再精炼；
- 逐章节阅读；
- 保留具体细节和数字；
- 给关键点附 brief evidence quotes；
- 最后进行 overview/takeaway 级别整理；
- 固定输出结构，便于比较。

对当前项目的启发：

> 单篇论文精读不应只给 abstract-level summary，而应按章节提取关键点、数字和证据，再生成高层 takeaway。

已吸收到当前模板中的设计：

- `paper_reading_prompt.md` 中要求 key results 尽量包含定量信息和 evidence；
- 要求区分论文原始结论、归纳总结和研究启发。

---

### 3.5 Academic prompt collections

这些仓库适合作为后续扩展参考，但需要挑选后再吸收，不能直接无差别照搬。

- [bohyy/academic-ai-prompt](https://github.com/bohyy/academic-ai-prompt)：学术研究 prompt 集合，包含文献综述、论文查找和科研写作流程。
- [LeSinus/chatgpt-prompts-for-academic-writing](https://github.com/LeSinus/chatgpt-prompts-for-academic-writing)：学术写作 prompt 集合，含 literature review、研究规划等。
- [ahmetbersoz/chatgpt-prompts-for-academic-writing](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing)：学术写作 prompt 集合。
- [BevalZ/awesome-prompt-for-academic](https://github.com/BevalZ/awesome-prompt-for-academic)：academic prompt 资源整理。
- [GitHub topic: literature-review](https://github.com/topics/literature-review)：更多文献综述相关项目集合。

可借鉴点：

- 学术写作结构；
- literature review 组织方式；
- research gap 表述；
- introduction / related work 写法；
- 提问方式和审稿式检查清单。

注意：

> 这些集合质量参差不齐，后续应只吸收结构化、有证据意识、能减少幻觉的部分。

---

## 4. 当前 Prompt 设计吸收的共同原则

综合上面的参考，当前模板遵循以下原则：

1. **先筛选，再精读**：避免无差别下载和总结大量低相关论文。
2. **结构化输出**：所有阅读笔记使用统一字段，方便比较和 RAG。
3. **证据优先**：重要结论必须尽量附来源、章节或原文短句。
4. **跨文献综合而非罗列**：综合时提取主题、共识、冲突和空白。
5. **批判审查必不可少**：每份综述或假说进入知识库前应经过 Critic Agent。
6. **明确不确定性**：不知道就写不知道，证据不足就标 `TODO: verify`。
7. **面向本人研究目标**：所有模板都加入 HR-GNSS、地震学、深度学习和 SRL 写作相关字段。

---

## 5. 后续可以继续改进的方向

1. 增加 few-shot 示例，让不同论文的阅读卡片风格更稳定；
2. 增加 JSON schema 版本，方便自动化处理；
3. 为 GNSS/地震学单独设计更细的物理约束检查清单；
4. 增加 figure/table extraction prompt；
5. 增加 citation verification prompt；
6. 增加“论文写作转化 prompt”，把阅读卡片转成 Introduction / Related Work 段落。
