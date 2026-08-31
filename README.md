# discover-skill（发现skill）

> Skill 市场每周都在膨胀，但"热门"不等于"值得装"——这个技能每天替你盯三个市场，只报变化、说清口径，并按你的行业告诉你先看哪个。

![Agent Skill](https://img.shields.io/badge/type-Agent%20Skill-blue) ![Runtime](https://img.shields.io/badge/runtime-Claude%20Code%20%2F%20Codex%20%2F%20OpenClaw%20%2F%20any%20SKILL.md%20agent-green) ![License](https://img.shields.io/badge/license-MIT-lightgrey) ![Language](https://img.shields.io/badge/output-%E4%B8%AD%E6%96%87-red)

**discover-skill** 是一个每日运行的 AI Skill 发现雷达：同时读取 [ClawHub](https://clawhub.com)、[skills.sh](https://www.skills.sh) Trending、[腾讯 SkillHub](https://skillhub.cn) 三个数据源（三源平权、各占独立板块），产出一分结构化中文榜单报告。它不堆"下载量 Top10"——那类存量榜天然僵化——而是抓**变化**（排名提升、增速、新进榜）、报**口径**（每个源怎么排的、数字是什么意思）、给**建议**（哪些技能值得关注，为什么）。

## 你什么时候需要它？

1. **你想每天花 3 分钟知道 skill 圈有什么动静**，而不是隔几周去市场里漫无目的地翻——"帮我看看 skill 圈最近有什么动静"一句话触发。
2. **你被"热门榜"骗过**：下载量 Top 永远是那几个老面孔，新好东西挤不进来——本技能只把"排名提升、下载增速、新进榜"当主角，存量只作背景。
3. **你想让发现结果贴合你自己**：默认按"通用知识工作者"画像评估，若你有行业背景（如地产营销、内容创作、开发运维），小结里每条"值得关注"会按「行业适配度 / 技能普适性 / 个人适配度」三维度标注——换一段画像即适配任何行业。

## 它会交付什么？

一份固定五板块结构的中文 Markdown 报告（`skill榜单-YYYY-MM-DD.md`）：

| 板块 | 内容 |
| --- | --- |
| 一、元数据说明 | 快照日期、三源并列、对比基准、limitations（诚实交代抓取缺口） |
| 二、ClawHub 榜单 | 2.1 平台健康度（先给结论）+ 2.2 排名提升榜 + 2.3 增速榜 + 2.4 新进榜 + 2.5 单日盲区提示 |
| 三、skills.sh Trending | 前 8-10 条，含中文简介与口径注记 |
| 四、腾讯 SkillHub 榜单 | 前 8-10 条，含中文简介与口径注记 |
| 五、今日榜单小结 | 值得关注技能清单（每条标注入选维度）+ 一句话总结 |

每条上榜技能都有一句**中文简介**，说清这个 skill 是干什么的——不认识英文名也能 3 秒判断要不要点开。

真实产物样例见 [`examples/skill榜单-2026-08-31.md`](examples/skill榜单-2026-08-31.md)（当日报告 + 两份原始快照 JSON，均为真实运行产物，非虚构样例）。

## 快速开始

把本目录复制到你的 agent 技能目录即可（无需任何依赖）：

```bash
# Claude Code / 大多数 SKILL.md 兼容 runtime
git clone <本仓库地址> ~/.claude/skills/discover-skill
# 或手动下载后放到项目的 skills/ 目录
```

也可以通过 `npx skills add <owner>/discover-skill`（vercel skills CLI）或 ClawHub 等目录安装（收录进行中）。

## 触发方式

装好后，下面这些话都会触发它：

- "发现skill"
- "生成今天的 skill 榜单"
- "最近什么 skill 在涨？"
- "有什么新 skill 值得看？"
- "ClawHub 榜单今天有什么变化？"
- "帮我看看 skill 圈最近有什么动静"
- "有没有适合做内容选题的 skill？"（触发"值得关注"评估）

## 它和同类有什么不同？

| | discover-skill | 按需扫描类雷达（如 skill-radar） | GitHub Trending 推送类 |
| --- | --- | --- | --- |
| 对象 | 专盯 **AI Skill** 市场 | AI Skill 市场（通用决策向） | 代码仓库，不针对 skill |
| 模式 | **每日固定栏目**（定时推送、快照对比） | 用户发起的按需扫描 | 每日拉一次 trending 页 |
| 数据源 | ClawHub + skills.sh + **腾讯 SkillHub**（中文生态） | 英语系目录为主 | github.com/trending |
| 口径处理 | 每个源的排序键/展示字段/已知坑都写成契约并持续注记 | 依赖目录自身口径 | 无 |
| 行业适配 | 默认通用画像，可按用户行业切换（附地产示例），"值得关注"按三维度标注 | 通用 | 无 |
| 持续性 | 自建每日快照，满样本后算真实增量 | 单次快照为 baseline | 单次快照 |

> 承认对手：按需扫描类雷达（[skill-radar](https://skills.cat/skills/dezhengz338-source/skill-radar)）在"验证与评分方法论"上更重，值得学；本技能选择把深度押在**每日栏目的口径契约与变化检测**上，两者互补而非替代。

## 安全边界

- **只读取数**：只通过 WebFetch 读取三个公开市场的页面/JSON，不登录、不写任何平台。
- **不安装技能**：发现结果只到"报告"为止，不负责安装、不执行任何被推荐技能的代码；安装与安全审查请交给专门技能（如 skill-vetter 类）。
- **例行写入需预授权**：每日报告写入项目约定的输出目录属定时任务既定流程；其他任何非例行写入会先停下来问你。
- **不编造**：简介依据不足时用保守表述并注明"详情以平台页面为准"；抓取缺口如实写进 limitations，缺历史切片时绝不把数字说成"日环比"。

## 文件结构

```
discover-skill/
├── SKILL.md              # 技能本体：取数通道、榜单规则、数据源契约、写作风格
├── README.md             # 本文件
├── test-prompts.json     # 3 个典型测试 prompt 与验收要点
├── examples/             # 真实运行产物（2026-08-31 期报告 + 两份 Day1 快照）
└── LICENSE               # MIT
```

## 验证与测试

- 3 个典型 prompt 见 [`test-prompts.json`](test-prompts.json)；运行后对照"验收要点"逐项核对。
- 活体对账：仓库里的 `examples/` 是 2026-08-31 的真实运行产物——当日报告、skills.sh 与 SkillHub 的 Day1 快照。任何改动 SKILL.md 的提交都应附带新一天的运行产物对比，或明确标注 dry_run。
- 数据源契约改动属于结构性变更：按 SKILL.md「数据源扩展」六项契约执行，缺一不接。

## 数据源与口径（本技能最有价值的沉淀）

- **ClawHub**：Convex `skills:listPublicPageV4`，累计下载存量榜——进榜门槛高（尾部数万）、排名天然稳定，"无变化"≠生态繁荣，所以本技能自建健康度指标（Top10 日增合计 vs 7 日均值，-30% 报警线）。
- **skills.sh Trending**：近期安装热度，HTML 解析无 JSON API；时间窗口径（24h vs This Week）用连续快照锁定中。
- **腾讯 SkillHub**：首页"近期飙升下载热榜"的**排序键是增速、展示字段是累计下载，两者不是一回事**；列表页与首页数字不一致，以首页为准。这些坑都是实测踩出来的，写在 SKILL.md 契约里。
- 取数通道约束：`*.github.io` 沙箱直连必失败，回退同仓库 `raw.githubusercontent.com` 地址。

## License

MIT
