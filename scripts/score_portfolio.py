#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""shkyyy18 GitHub 项目组合六维评分脚本（可重复运行的周评工具）。

用法：
    python scripts/score_portfolio.py                  # 打印本期 markdown 评分表（对比内置基线）
    python scripts/score_portfolio.py --date 2026-07-19  # 指定评分日期（默认今天）
    python scripts/score_portfolio.py --prev docs/weekly-score-2026-07-19.md
                                                       # 从上一份周评文件解析上期分数做环比
    python scripts/score_portfolio.py --json           # 同时输出原始 JSON 明细到 stderr

评分模型（百分制，六维）：
    A 基础完整度 20：描述 4 / 许可证 4 / topics>=5 计 4 / README>=3KB 计 4 / homepage 或 demo 4（自动）
    B 赛道热度   20：per-repo 配置（见下方 REPO_CONFIG）
    C 差异化定位 15：per-repo 配置
    D 证据可验证性 15：per-repo 配置为基础分；检测到 GitHub Pages 或 homepage/demo 自动 +2（封顶 15）
    E 活跃与维护 15：pushed_at 距今 <=7d 15 / <=14d 12 / <=30d 8 / <=60d 5 / <=90d 3 / 更久 1；archived 0（自动）
    F 社区信号   15：2 + stars + forks，封顶 15（自动）
分级：>=80 优秀 / 65-79 良好 / 50-64 观察 / <50 退出评估。

数据通过 `gh api`（subprocess）拉取；B/C/D 主观分维护在 REPO_CONFIG，调分即改这里。
profile 仓库（与账号同名）自动跳过；无配置的仓库列入"未纳入评分"。
"""

import argparse
import base64
import datetime as dt
import json
import re
import subprocess
import sys

OWNER = "shkyyy18"

# ---------------------------------------------------------------------------
# per-repo 主观配置：B 赛道热度(0-20) / C 差异化定位(0-15) / D 证据可验证性基础分(0-15)
# D 会在自动探测到 Pages 或 homepage/demo 时 +2（封顶 15）
# ---------------------------------------------------------------------------
REPO_CONFIG = {
    "cc-autopilot":              {"B": 19, "C": 13, "D": 8},
    "openbid-intel":             {"B": 12, "C": 12, "D": 13},
    "kimi-adapter":              {"B": 18, "C": 12, "D": 6},
    "mi-fitness-data-bridge":    {"B": 10, "C": 11, "D": 8},
    "ai-money-lab":              {"B": 10, "C": 10, "D": 9},
    "github-project-evaluation": {"B": 8,  "C": 8,  "D": 8},
}

# 内置基线：2026-07-19 期总分（--prev 未提供时使用）
BASELINE_DATE = "2026-07-19"
BASELINE = {
    "cc-autopilot": 75,
    "openbid-intel": 72,
    "kimi-adapter": 69,
    "mi-fitness-data-bridge": 62,
    "ai-money-lab": 59,
    "github-project-evaluation": 53,
}

GRADE_RULES = [(80, "优秀"), (65, "良好"), (50, "观察"), (0, "退出评估")]


def gh_api(endpoint, jq=None):
    """调用 gh api，返回解析后的 JSON；404 等错误返回 None。瞬时失败重试一次。"""
    cmd = ["gh", "api", endpoint]
    if jq:
        cmd += ["--jq", jq]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return proc.stdout.strip()


def fetch_repos():
    repos = gh_api(f"users/{OWNER}/repos?per_page=100&sort=pushed") or []
    return [r for r in repos if not r.get("fork")]


def fetch_repo_extras(name):
    """topics / README 大小 / Pages 状态，分别单独拉取。"""
    topics_obj = gh_api(f"repos/{OWNER}/{name}/topics")
    topics = (topics_obj or {}).get("names", [])
    readme = gh_api(f"repos/{OWNER}/{name}/readme")
    readme_size = (readme or {}).get("size", 0) if isinstance(readme, dict) else 0
    pages = gh_api(f"repos/{OWNER}/{name}/pages")
    has_pages = isinstance(pages, dict) and pages.get("status") is not None
    return topics, readme_size, has_pages


def score_a(repo, topics, readme_size):
    s = 0
    if repo.get("description"):
        s += 4
    if repo.get("license"):
        s += 4
    if len(topics) >= 5:
        s += 4
    if readme_size >= 3 * 1024:
        s += 4
    if repo.get("homepage"):
        s += 4
    return s  # 满分 20


def score_d(base, has_pages, homepage):
    return min(15, base + (2 if (has_pages or homepage) else 0))


def score_e(repo, today):
    if repo.get("archived"):
        return 0
    pushed = repo.get("pushed_at")
    if not pushed:
        return 1
    days = (today - dt.datetime.strptime(pushed, "%Y-%m-%dT%H:%M:%SZ").date()).days
    for limit, pts in [(7, 15), (14, 12), (30, 8), (60, 5), (90, 3)]:
        if days <= limit:
            return pts
    return 1


def score_f(repo):
    return min(15, 2 + repo.get("stargazers_count", 0) + repo.get("forks_count", 0))


def grade(total):
    for floor, label in GRADE_RULES:
        if total >= floor:
            return label
    return "退出评估"


def trend_arrow(current, previous):
    if previous is None:
        return "🆕 新纳入"
    diff = current - previous
    if diff > 0:
        return f"↑ +{diff}"
    if diff < 0:
        return f"↓ {diff}"
    return "→ 持平"


def parse_prev_scores(path):
    """从上一份周评 markdown 表格解析上期总分：取每行第 8 列（总分列）。"""
    scores = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|") or "---" in line:
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 8 or cells[0] in ("仓库", ""):
                continue
            m = re.fullmatch(r"\**(\d+(?:\.\d+)?)\**", cells[7])
            if m:
                scores[cells[0]] = float(m.group(1))
    return scores


def main():
    ap = argparse.ArgumentParser(description="shkyyy18 项目组合六维评分")
    ap.add_argument("--date", default=dt.date.today().isoformat(), help="评分日期，默认今天")
    ap.add_argument("--prev", help="上一份周评 markdown，用于环比（缺省用内置基线）")
    ap.add_argument("--json", action="store_true", help="把明细 JSON 打到 stderr")
    args = ap.parse_args()

    today = dt.date.fromisoformat(args.date)

    if args.prev:
        prev_scores = parse_prev_scores(args.prev)
        prev_label = f"上期（{args.prev}）"
    else:
        prev_scores = BASELINE
        prev_label = f"基线（{BASELINE_DATE} 期）"

    repos = fetch_repos()
    rows, skipped = [], []
    for repo in repos:
        name = repo["name"]
        if name == OWNER:  # profile 仓库跳过
            continue
        if name not in REPO_CONFIG:
            skipped.append(name)
            continue
        cfg = REPO_CONFIG[name]
        topics, readme_size, has_pages = fetch_repo_extras(name)
        a = score_a(repo, topics, readme_size)
        d = score_d(cfg["D"], has_pages, repo.get("homepage"))
        e = score_e(repo, today)
        f_ = score_f(repo)
        total = a + cfg["B"] + cfg["C"] + d + e + f_
        rows.append({
            "name": name, "A": a, "B": cfg["B"], "C": cfg["C"], "D": d,
            "E": e, "F": f_, "total": total, "grade": grade(total),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "topics": topics, "readme_bytes": readme_size, "pages": has_pages,
            "pushed_at": repo.get("pushed_at"),
        })

    rows.sort(key=lambda r: r["total"], reverse=True)

    out = []
    out.append(f"# 项目组合周评（{args.date}）")
    out.append("")
    out.append(f"账号 [{OWNER}](https://github.com/{OWNER}) 非 fork 仓库六维评分"
               f"（A 基础完整度 20 / B 赛道热度 20 / C 差异化定位 15 / D 证据可验证性 15 / E 活跃与维护 15 / F 社区信号 15）。")
    out.append(f"环比对象：{prev_label}。分级：≥80 优秀 / 65–79 良好 / 50–64 观察 / <50 退出评估。")
    out.append("")
    out.append("| 仓库 | A | B | C | D | E | F | 总分 | 分级 | 环比 |")
    out.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        prev = prev_scores.get(r["name"])
        out.append(
            f"| {r['name']} | {r['A']} | {r['B']} | {r['C']} | {r['D']} | {r['E']} | {r['F']} "
            f"| **{r['total']}** | {r['grade']} | {trend_arrow(r['total'], prev)} |"
        )
    out.append("")
    if skipped:
        out.append(f"未纳入评分（无 per-repo 配置或跳过）：{', '.join(skipped)}；profile 仓库 `{OWNER}` 不参与评分。")
        out.append("")
    out.append("---")
    out.append("")
    out.append("*由 `scripts/score_portfolio.py` 自动生成；B/C/D 主观分见脚本 REPO_CONFIG。*")

    print("\n".join(out))
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2), file=sys.stderr)


if __name__ == "__main__":
    main()
