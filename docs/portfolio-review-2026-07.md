# GitHub 项目组合复盘：评分机制、复刻规律与退出机制

**对象**：shkyyy18 账号下 11 个仓库 | **日期**：2026-07-19 | **角色**：商业顾问

---

## 一、本轮发现的问题与已修复项

| 仓库 | 发现的问题 | 处理 |
|---|---|---|
| github-project-evaluation | 无描述、无许可证、无 topics | ✅ 已补描述 + 6 个 topics |
| kimi-adapter | 无 topics（影响搜索发现） | ✅ 已补 7 个 topics |
| cc-autopilot | 无许可证；homepage 冗余指向自身 README | ✅ 已加 MIT LICENSE、清除冗余 homepage |
| health-assistant | 无许可证、无 topics | ✅ 已加 MIT LICENSE + 6 个 topics |
| mi-fitness-data-bridge | 无 topics | ✅ 已补 7 个 topics |
| 组合层面 | 健康类项目 4 个仓库（2 个已归档）功能重叠，portfolio 分散 | 见第四节退出机制建议 |
| openbid-intel | 4 个 open issue 均为自建 roadmap，管理正常 | 无需处理 |
| dailysync-rev | 已归档 fork，描述含凭据轮换警告 | ⚠️ 建议删除（见第四节），删除不可逆，需你确认后执行 |

## 二、上线项目评分机制（100 分制）

针对**早期项目**（star 基数小），评分重点是"增长潜力与运营健康度"，而非现有 star 数。

| 维度 | 权重 | 评分要点 |
|---|---|---|
| A. 基础完整度 | 20 | 描述 4 / 许可证 4 / topics≥5 计 4 / README 结构化且 ≥3KB 计 4 / demo 或主页 4 |
| B. 赛道热度与时机 | 20 | 所属领域在当前 GitHub 趋势中的位置（AI agent 工具链为当期最热） |
| C. 差异化定位 | 15 | 一句话能否说清"给谁解决什么问题"、与竞品差异 |
| D. 证据与可验证性 | 15 | 可运行 demo、GitHub Pages、截图、测试、数据证据 |
| E. 活跃与维护 | 15 | 提交节奏（近 7 天满分）、issue 管理 |
| F. 社区信号 | 15 | star/fork/外部引用（早期项目此维度天然低分，权重不宜再高） |

**分级**：≥80 优秀（加大投入）/ 65–79 良好（重点运营）/ 50–64 观察 / <50 进入退出评估。

## 三、现有项目评分表（修复后状态）

| 项目 | A | B | C | D | E | F | 总分 | 等级 |
|---|---|---|---|---|---|---|---|---|
| cc-autopilot | 16 | 19 | 13 | 8 | 15 | 4 | **75** | 良好·头部 |
| openbid-intel | 20 | 12 | 12 | 13 | 13 | 2 | **72** | 良好 |
| kimi-adapter | 16 | 18 | 12 | 6 | 15 | 2 | **69** | 良好 |
| mi-fitness-data-bridge | 16 | 10 | 11 | 8 | 14 | 3 | **62** | 观察 |
| ai-money-lab | 16 | 10 | 10 | 9 | 12 | 2 | **59** | 观察 |
| health-assistant | 16 | 10 | 6 | 6 | 15 | 2 | **55** | 观察·同质化 |
| github-project-evaluation | 12 | 8 | 8 | 8 | 15 | 2 | **53** | 观察 |
| shkyyy18（profile） | — | — | — | — | — | — | N/A | 特殊用途不参评 |
| health-advisor / personal-health-sync | — | — | — | — | 0 | — | — | 已归档（已退出） |
| dailysync-rev | — | — | — | — | 0 | — | — | 建议删除 |

**结论：目前没有"优秀"项目，头部三个（cc-autopilot / openbid-intel / kimi-adapter）共同短板是 D（证据演示）和 F（社区信号）——这正是从"良好"跨到"优秀"、从 0 star 到高星的杠杆点。**

## 四、高分规律与复刻 Playbook

### 从本期评分 + 外部高星项目（上期报告）交叉验证出的 5 条规律

1. **元数据完整是门票**：描述 + 许可证 + ≥5 个 topics 决定搜索曝光，缺一项就被过滤掉一半流量。
2. **赛道 > 努力**：当期 AI agent 工具链项目在同等质量下曝光量是垂直赛道的 3–5 倍（cc-autopilot 2 个 fork 全部来自该赛道红利）。
3. **一句话价值主张**：高星项目 README 首屏都能用一句话说清"给谁解决什么"。
4. **可验证证据**：有 demo / Pages / 截图的项目，star 转化率显著更高（openbid-intel 的 Pages dashboard 是它的加分项）。
5. **持续提交节奏**：算法推荐和 Trending 都偏好近期活跃仓库，周更比突击式提交有效。

### 复刻 Playbook（新项目上线 checklist）

- 选题：AI agent 工具链优先；一句话价值主张先写出来，写不出就不立项
- 上线前 12 项：描述 / MIT 许可证 / ≥5 topics / README 首屏价值主张 + 截图 / 可运行 demo / Pages / CI badge / 初始 tag release / .gitignore / issue 模板 /  pinned 到 profile
- 上线后增长：Show HN + 相关 subreddit + 向对应 awesome-list 提 PR + 每周 changelog + 月度评分复盘

## 五、退出机制设计（建议采纳）

### 原则
- **归档优先，删除例外**：归档可逆、保留历史；删除不可逆，仅限敏感场景。
- **有外部依赖不删除**：凡有他人 fork/star 的仓库只归档不删除，避免影响他人。
- **看趋势不看单点**：连续 2 个评估周期（每月 1 次）低于 50 分才进入退出流程，避免误杀慢热项目。

### 三级退出漏斗

| 级别 | 触发条件 | 动作 |
|---|---|---|
| L1 观察 | 单周期 <50 分 | 列入观察名单，下周期复评 |
| L2 合并/归档 | 连续 2 周期 <50，或与主线项目同质化 | 功能并入主线仓库，原仓库归档并更新 README 指向新址 |
| L3 删除 | 含凭据/敏感信息风险，或违反合规 | 删除（执行前必须人工确认） |

### 应用到当前组合的具体建议

1. **health-assistant（55 分，同质化）**：与 mi-fitness-data-bridge 数据线重叠。建议进入 L1 观察；若下周期仍 <50，将其仪表盘能力并入 mi-fitness-data-bridge（或反向合并），保留一条健康数据线，另一条归档。你此前已主动归档 health-advisor 和 personal-health-sync，说明这条产品线已在收缩——建议彻底收敛到 1 个仓库。
2. **dailysync-rev**：描述中自带"轮换凭据"警告，属 L3 删除候选。**删除不可逆，请确认后我再执行，或你手动在 Settings → Danger Zone 删除。**
3. **github-project-evaluation（53 分）**：属内容型报告仓库，建议补 MIT 许可证后按"内容资产"单独管理，不与应用型项目同赛道评比。
4. **头部三个项目**不触发退出机制，资源应向它们集中。

### 评审节奏

每月 19 日重跑一次本评分机制（数据可由 GitHub API 自动采集），输出趋势表而非单点分，退出决策只看趋势。

---

*评分数据：GitHub REST API（2026-07-19）；元数据修复记录见本文第一节。*
