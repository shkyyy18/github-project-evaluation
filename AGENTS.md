# AGENTS.md — github-project-evaluation

## 项目定位

GitHub 高星项目 / shkyyy18 自有项目组合的商业价值评估报告库：以六维评分模型对项目打分并产出 Markdown 报告，附一个可重复运行的周评脚本（`scripts/score_portfolio.py`）。

## 技术栈

- 纯 Python 3 单脚本（`scripts/score_portfolio.py`），仅标准库；运行时外部依赖是 GitHub CLI `gh`（subprocess 调 `gh api`）
- 其余全部是 Markdown 内容资产 + JSON 数据；无 pyproject、无测试、无 lint、无 CI

## 常用命令

```bash
python scripts/score_portfolio.py [--date YYYY-MM-DD] [--prev docs/weekly-score-XXXX-XX-XX.md] [--json]
# 前提：本机已安装并登录 gh CLI
```

## 本仓库 agent 的搜索范围与要求

- 只允许改动本仓库；**`docs/` 是内容资产**：历史报告（周评、调研、复盘、运营日志）只能追加，不得删改——写错了用"追加勘误"的方式修正，保持历史可追溯。
- `data/top20.json` 是 README 报告的原始数据源，更新时必须保留原始 API 返回结构。
- `README.md` 的 Top 20 评估表是手工/半自动产物，**不要**声称它能由脚本重新生成；能自动化的只有 `score_portfolio.py` 的周评。
- `score_portfolio.py` 中 `REPO_CONFIG` 的 B/C/D 维主观分改动：必须在当周周评报告中说明调整理由。
- 全局协作规则文档 `docs/agent-collab-rules.md` 由本仓维护，各仓库 AGENTS.md 引用它；修改它时需注意别破坏各仓引用。

## 升级建议有效性 / 采纳规则（本仓定制）

1. 凡涉及历史报告内容更正的建议：一律以追加勘误实现，**不采纳**任何删改历史文件的建议（除非含敏感信息泄露，属安全问题立即处理）。
2. 评分模型（六维权重、口径）变更：必须在当周周评中写明变更理由与生效日期，且不回溯修改历史周评分数。
3. `score_portfolio.py` 改动：保持仅标准库 + `gh` 依赖，不得引入第三方包；改完用 `--date` 对历史基线重跑一次确认输出稳定。
4. 新增报告/调研文档：有效即可直接追加进 `docs/`，文件名带日期（`YYYY-MM-DD`），遵循现有命名风格。
5. 跨仓库协作规则的变更（`docs/agent-collab-rules.md`）：需同步检查 7 个仓库 AGENTS.md 的引用是否仍然成立。

## 升级建议 backlog

（暂无。各仓库的升级建议收录在各自 AGENTS.md 的 backlog 小节；跨仓库建议收录在 `docs/agent-collab-rules.md` 的全局 backlog。）
