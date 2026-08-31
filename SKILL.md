---
name: discover-skill
description: "发现skill — 每日 AI Skill 发现雷达。触发词：发现skill、skill榜单、ClawHub 榜单、最近什么 skill 在涨、有什么新 skill、有什么值得装的 skill、skill 下载榜/增速榜/新进榜、帮我看看 skill 圈最近有什么动静、生成每日 skill 榜单。消费侧：用 WebFetch 读取三个数据源（ClawHub / skills.sh / 腾讯 SkillHub，三源平权），按五板块结构（一、元数据说明；二、ClawHub 榜单；三、skills.sh Trending 榜单；四、腾讯 SkillHub 榜单；五、今日榜单小结）输出中文 Markdown 报告：每条上榜技能附一句中文简介，小结给出值得关注技能及入选理由（行业适配度/技能普适性/个人适配度）。报告写入项目约定的输出目录。维护侧：扩展新数据源（SkillsMP、anthropics/skills 等）时，按本文件的数据源扩展契约执行。不要用于：AI 资讯/新闻聚合、评估某个信息源是否值得接入、安装某个具体 skill 本身（安全审查请交给专门的审查技能）。"
---

# 发现skill（discover-skill）

每日从公开 AI Skill 市场取数，生成中文榜单报告，帮助发现之前不知道的好用技能。已接入数据源（三源平权，各占报告一个独立板块）：ClawHub Top100（上游 LearnPrompt/skillrush-town 快照，本技能只消费、不落库）、skills.sh Trending、腾讯 SkillHub 热榜。

## 取数通道（实测约束）

- 只用 WebFetch 内部通道取数；禁止 curl/requests 直连 github.io（沙箱直连会被 SSL 阻断）。
- 实测可用：`https://raw.githubusercontent.com/<owner>/<repo>/main/<path>`。
- 实测不可用：`*.github.io` 直连返回 fetch failed；遇此情况回退到同仓库的 raw 地址。
- 接入新站点前，先做一次 WebFetch 连通性试探，并把结果写入 limitations。

## 消费侧用法（用户只想看榜时）

1. 取数据：ClawHub 快照 `https://raw.githubusercontent.com/LearnPrompt/skillrush-town/main/data/latest.json`；历史快照 `data/snapshots/<YYYY-MM-DD>.json`；日期列表 `data/dates.json`；官方日报 `data/reports/<date>.md`。
2. 按五板块结构成文（见「榜单结构」）：一、元数据说明；二、ClawHub 榜单；三、skills.sh Trending 榜单；四、腾讯 SkillHub 榜单；五、今日榜单小结。
3. 每个数据源板块中的每条上榜技能，必须有一句中文简介，说清这个 skill 是干什么的；简介依据不足时用保守表述并注明"详情以平台页面为准"，不得编造功能细节。
4. 今日榜单小结给出值得关注技能清单，每条标注入选维度（行业适配度/技能普适性/个人适配度，见「值得关注技能标准」），并附 `https://learnprompt.github.io/skillrush-town/?date=<snapshot_date>` 供用户自查。
5. 诚实转述 limitations 与 comparison_basis.note；缺历史切片时不得把数字表述为日环比。

## 每日榜单规则

固定产物：一份 Markdown 报告。标题《Skill 榜单 - YYYY-MM-DD》，文件名 `skill榜单-YYYY-MM-DD.md`；日期取数据快照日（snapshot_date），并在元数据中另行记录报告生成时间。

### 榜单结构（分源板块 v3，2026-08-31 定稿）

三个数据源各自独立成板块、平权呈现，**不区分主源与观察源**。固定五板块：

1. **一、元数据说明**：快照日期、抓取时间、三个数据源并列、对比基准、条目数、生成时间；limitations 全部收在本板块。
2. **二、ClawHub 榜单**：2.1 ClawHub 平台健康度（先给结论再看榜）+ 2.2 排名提升榜（rank_change > 0 全部条目，按提升幅度降序；不设"下载量 Top10"主榜）+ 2.3 下载增速榜（download_delta 降序前 10）+ 2.4 新进榜（prev_rank 为 null，为空写明"本期无新进榜"）。子榜间重合条目须标注。
3. **三、skills.sh Trending 榜单**：前 8-10 条，含中文简介与口径注记。
4. **四、腾讯 SkillHub 榜单**：首页"近期飙升下载热榜"前 8-10 条，含中文简介与口径注记。
5. **五、今日榜单小结**：值得关注技能清单（每条标注入选维度）+ 一句话总结（本期动态与口径锁定进度）。

通用要求：每个板块中每条上榜技能必须有一句中文简介。skills.sh 与 SkillHub 的每日快照仍存当前工作区的 `skill-discovery/snapshots/`（命名 `<source>-<YYYY-MM-DD>.json`），样本满后计算自有 delta。

### 榜单健康度（必做）

- 计算下载 Top10 条目当日 download_delta 合计，并与近 7 日均值对比（数据取自历史快照或官方日报；无历史时标注"样本不足"）。
- 合计值较 7 日均值下降超过 30% 或连续多日走低时，必须在 2.1 健康度小节提示：**"数据源活跃度下滑，榜单稳定性上升；'无变化'应解读为流量收缩而非生态繁荣，发现类结论请以增速榜与外部数据源为准。"**
- 健康度结论（上升/平稳/下滑 + 数值）固定写入 ClawHub 榜单板块的 2.1 小节。

### 条目字段

每个榜单条目包含：name、rank_change、downloads、download_delta、star_delta、summary。summary 必须翻译成中文，简洁准确。

### 元数据与 limitations

记录：snapshot_date、数据来源、comparison_basis、本期条目数、报告生成时间、limitations 原文。抓取不完整、字段异常等情况必须如实写入。

### 写入输出目录

- 报告写入项目约定的输出目录（每日定时任务的既定流程，视为用户预先授权）。
- 手动修改、覆盖历史报告或其他非例行写入，必须先向用户展示变更并获确认。

## 值得关注技能标准（今日榜单小结用）

数据信号（满足任一即成候选）：新进榜；download_delta 前 20 且 star_delta 前 30；排名上升 ≥ 8 位；连续多日爬升（单日 rank_change≈0 也会漏掉）；外部源热度信号。最多 10 个，若无则明确写"今日无可关注技能"。

每条必须标注入选维度（满足任一即可入选）：

- **行业适配度**：与用户所在行业的工作场景匹配。
- **技能普适性**：对任何知识工作者都有通用价值（如任务规划、文档处理、浏览器自动化）。
- **个人适配度**：与用户日常场景直接匹配。默认画像为**通用知识工作者**；若用户有行业背景，按其行业调整「行业适配度」判断（示例：地产行业数字化营销与运营策略线条，核心场景为用户洞察、活动策划、内容生产、客户运营、数据复盘）。**更换画像即可适配任何行业，其余规则不变。**

## 数据源扩展

技能按多源设计。接入任何新数据源前，必须先在本文件明确以下六项，缺一不接：

1. 请求契约（URL / method / 分页方式 / 字段）
2. 条目唯一键（slug、author/name 等）
3. 快照 schema，以及与存量数据的对齐方式
4. diff 语义（对比哪个字段、是否严格日环比）
5. limitations 处理与连通性实测结果
6. 验证方式（fixtures / mock，不依赖浏览器）

候选数据源与抓取难度（2026-08-31 实测结论，均经 WebFetch 连通性验证）：

### 已接入源契约（2026-08-31 接入）

**skills.sh Trending**

- 取数：WebFetch `https://www.skills.sh/trending`（HTML 解析，无 JSON API）；备选 `/hot`、`/`（All Time）。
- 条目键：`publisher/slug`；字段：name、publisher、installs。
- 口径：排序为近期安装热度；时间窗口导航标注 24h、页面标题写 This Week，**待快照锁定**，锁定前报告标注"近期口径（24h/周，待锁定）"。
- diff：自建每日快照存当前工作区的 `skill-discovery/snapshots/`，样本满前报告标注"暂无增量对比"；时间窗口径锁定前标注"近期口径（24h/周，待锁定）"。

**腾讯 SkillHub 热榜**

- 取数：WebFetch `https://skillhub.cn`（首页"近期飙升下载热榜"），必要时抓 `https://skillhub.cn/skills?sortBy=trending` 补充。
- 条目键：URL 中 slug（如 `beatra-ai/hot-topic-content-maker`）；字段：name、author、category、累计下载（展示值）。
- 口径：**排序键是"近期飙升"（增速），展示字段是累计下载，两者不是一回事**，报告中必须分开表述；实测证据：热榜中 6.5 万的条目排在 9.8 万之前，纯总量排序不会出现此序。完整列表页数字与首页热榜对不上（同一技能 45.9 万 vs 3446.1 万），以首页热榜为准，口径 3 天内锁定。
- diff：自建每日快照存当前工作区的 `skill-discovery/snapshots/`，样本满前报告标注"暂无增量对比"；持续核对首页与列表页数字差异及回落现象。

**三源平权规则**（2026-08-31 起）：三个已接入源在报告中各占独立板块、平权呈现，不再区分主源与观察源、不再设观察期；口径未锁定事项（skills.sh 时间窗、SkillHub 数字回落与首页/列表页差异）以各板块「口径注记」形式持续跟踪。

### 候选源（未接入）

| 候选 | 定位 | 难度 | 实测备注 |
| --- | --- | --- | --- |
| anthropics/skills | Anthropic 官方仓库 | ★☆☆ | ✅ GitHub API 可用（172k stars）；做"更新监控"而非每日榜 |
| SkillsMP | 最大聚合目录（190 万+） | ★★☆ | ✅ 可达：API 仅 search 端点，匿名 50 次/天、10 次/分；做榜需解析页面，更适合关键词发现 |
| awesome 合集 | ComposioHQ/awesome-claude-skills（74.1k stars）等 | ★★☆ | ✅ GitHub 搜索 API 可用；raw 直链 404（默认分支是 master 而非 main），取数前需确认分支与 README 文件名 |

实测经验：*.github.io 直连必失败（回退 raw.githubusercontent.com）；api.github.com、skills.sh、skillsmp.com、skillhub.cn（skillhub.tencent.com 跳转至此）均可用。

原则：一次只接一个源；接入后与现有榜并行观察 3 天，再决定是否并入主报告。

## ClawHub 口径（已接入源）

- 主榜单：Convex `api/query`，path `skills:listPublicPageV4`，args `sort=downloads, dir=desc, nonSuspiciousOnly=true, highlightedOnly=false, numItems=25`，按 nextCursor 连续 4 页拼接 Top100。
- `GET /api/v1/skills` 仅作诊断，不作主榜与对比依据；返回空 items 不代表页面无榜。
- 对比口径：与前一日快照严格日环比。
- ClawHub 榜为累计下载量存量榜：进榜门槛高（尾部约数万累计下载）、排名天然稳定；结论以增速榜和健康度为准，不要把"排名持平"当成"生态繁荣"。

## 写作风格

- 简介一律中文，简洁准确；不使用 AI 营销腔（"赋能""生态飞轮""一站式平台"等）。
- 每个上榜条目配一句中文简介，说清用途；依据不足时保守表述并注明，不编造细节。
- 优先给具体用例和数字，少给抽象判断。
- 今日榜单小结落到"值得关注技能清单 + 入选维度"，理由必须具体（说清对应哪个行业场景或通用场景）。

## 边界

- 不做 AI 资讯/新闻聚合。
- 不评估某个信息源值不值得接入。
- 不负责安装具体 skill 或其安全审查。
