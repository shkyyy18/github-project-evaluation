# MVP 立项方案：llm-video-mcp（工作名）

**日期**：2026-07-20 | **状态**：立项评审 | **关联文档**：`idea-log-2026-07-20.md`（竞品评分）、`portfolio-review-2026-07.md`（评分机制与退出机制）

---

## 一句话价值主张

**给 coding agent（Claude Code / Cursor / Kimi Code 等）一个 MCP 工具，让任意 LLM 在 token 预算内真正"看"懂一段视频——本地抽帧 + 转录 + 时间线摘要，agent 原生调用，无需人工粘贴。**

竞品 claude-real-video 验证了"让 LLM 看视频"的需求，但它的产物是"给人搬到 LLM 面前的文件夹"；我们的产物是"agent 自己动手看的工具"。

---

## 竞品分析

### claude-real-video（HUANGCHIHHUNGLeo/claude-real-video）真实数据

数据采集：2026-07-20，`gh api repos/HUANGCHIHHUNGLeo/claude-real-video` + README 原文。

| 指标 | 值 |
|---|---|
| Stars / Forks | 1,753 / 142 |
| 创建时间 | 2026-06-30（约 20 天到 1.7k star，日均 ~88） |
| 许可证 | **MIT**（复刻无法律障碍，需保留归因） |
| 语言 / 打包 | Python 3.10+，PyPI 包名 `claude-real-video`（CLI 别名 `crv`） |
| 最新版本 | v0.7.15（2026-07-17），迭代极快（单日多个 patch release） |
| 外部验证 | HN 首页（item 48766005，README 自带徽章） |
| 架构 | 单仓 Python：yt-dlp 下载 → ffmpeg `select` 单遍场景检测 + 密度下限 → 滑窗双通道去重（全局 RGB 像素差 + v0.7.4 的 settled-local 局部检测）→ 字幕优先 / whisper 兜底转录（可选 faster-whisper）→ `frames/*.jpg` + `frames.json`（逐帧时间戳）+ `transcript.txt/.json` + `MANIFEST.txt` |

**它的真实能力边界（README 原文核实）**：

- 有：`--adaptive` 自适应慢变化场景、`--text-anchors` 字幕锚点强制帧、`--speakers` 本地说话人分离（45MB diarization 模型）、`--grid` 3×3 contact sheet、`--viewer` 本地 HTML 查看器、`--kb` 知识库落盘、`--why` 分析意图注入、本地 `crv-web` 页面、URL（yt-dlp）与本地文件双输入。
- 有但**粗糙的 token 控制**：只有 `--max-frames`（硬上限，默认 150）、`--scene` 阈值、`--fps-floor`、`--grid` 打包。**没有按目标模型上下文窗口/token 单价反推帧数与分辨率的机制**——用户得自己猜参数。
- **没有 MCP server**。它的 agent 集成是 skill 形态（`npx skills add`，兼容 agentskills.io 生态的 50+ host），工作流仍是"人粘贴视频链接 → agent 跑 CLI → 产物文件夹 → 模型读文件夹"。agent 不能按需、增量地调取"第 3 分 20 秒附近的帧"或"只要转录不要帧"。
- **时间线理解在付费墙后**：crv Pro（Capafy 售卖，$19 创始价 / 8 月 1 日起 $29）才提供镜头语言标注（pan/tilt/zoom/handheld）、节奏曲线、语音情绪、声音事件时间线、交互式事件时间线 viewer。免费版只给"看见了什么"，不给"怎么拍的/情绪如何"。

**弱点小结**（我们差异化的落点）：
1. 非 MCP 原生——skill 是"安装一段提示词"，不是结构化工具协议；无增量/按需查询能力。
2. token 经济性靠用户手调参数，不感知目标模型上下文窗口。
3. 时间线理解层（镜头/情绪/声音事件）被刻意放进 Pro 付费墙，开源复刻可直接覆盖。

### 模型原生视频能力的威胁评估

- **Gemini 已能原生读视频**，但 README 的对比仍然成立：固定 1fps 采样漏快剪、必须上传 Google、无本地隐私选项。短期内"固定间隔采样"的原生管线打不掉"场景感知抽帧"的质量优势。
- **真正的威胁是"原生视频 + 场景感知 + 免费"三者同时出现**。当前没有任何一家做到；一旦上游模型把场景感知采样做成默认且长视频免费（或 agent host 内置等效视频输入工具），本项目的存在理由消失。
- **窗口期判断：6–12 个月**。因此本项目定位是"窗口期套利 + 卡位 agent 多模态输入基础设施"，不是长期赛道。所有投入决策按 6 个月回收期评估。

---

## MVP 范围（一周 cuts）

### 做（In scope）

1. **抽帧管线**（可独立作为 CLI 用）：
   - 输入：本地文件 + URL（yt-dlp）。
   - ffmpeg 单遍场景检测（`select='gt(scene,threshold)'`）+ 密度下限（每秒至少 1 帧兜底）。
   - 滑窗帧去重：下采样 RGB 直方图/像素差，对比最近 N 帧（参考竞品公开描述自行实现，不抄代码）。
   - 输出：`frames/*.jpg` + `frames.json`（file / timestamp_sec / selection_reason）。
2. **转录**：faster-whisper（默认 `base`，可配 `tiny/turbo`），带 Silero VAD 门控（静音/纯音乐输出诚实的"无语音"而非幻觉文本）；输入视频自带 sidecar/内嵌字幕时优先用字幕。输出 `transcript.json`（带时间戳分段）。
3. **token 预算控制器**：输入 `token_budget`（如 8k/32k/128k）和目标模型配置（每帧估算 token、文本压缩比），自动反推：帧数上限 → 场景阈值/密度调整 → 必要时降分辨率或转 contact sheet（2×2/3×3 网格）→ 转录截断/摘要。这是核心差异化，必须有单测覆盖。
4. **MCP server**（Python `mcp` SDK，stdio transport）：
   - `analyze_video(path_or_url, token_budget, lang?)` → 返回结构化结果：帧引用（MCP image content 或落盘路径）、转录、时间线摘要。
   - `get_frames_at(path_or_url, timestamp, window?)` → 按需取某一时刻附近的帧（增量查看，竞品没有）。
   - `get_transcript(path_or_url, start?, end?)` → 只要文本。
   - 分析结果按视频内容哈希缓存，重复调用秒回。
5. **时间线理解层（开源版，对标其 Pro 的最小集）**：`timeline.json` —— 逐镜头表（起止时间、时长、cuts/min）、基于帧间运动矢量的简单镜头运动标签（static/pan/zoom 三分类起步）、转录与帧的时间戳对齐。不做情绪识别、不做声音事件分类（v0.2 再说）。

### 明确不做（Out of scope，MVP 阶段）

- ❌ 说话人分离（diarization）——竞品有，但有 45MB 模型依赖，非差异化点。
- ❌ 情绪/声音事件/镜头运动细分类（tilt/handheld）——Pro 深层功能，v0.2 候选。
- ❌ Web UI / viewer.html——MVP 只服务 agent 调用，不服务人。
- ❌ skill 形态分发（`npx skills add`）——我们只走 MCP 一条路，避免双线作战。
- ❌ 云端托管 / 批处理服务——商业化后置。
- ❌ 复刻其 `--adaptive` / settled-local 双通道去重——MVP 用单通道像素差，够 80% 场景。

---

## 技术架构草图

```
┌─ MCP client (Claude Code / Cursor / Kimi Code …)
│        │ stdio (JSON-RPC)
├────────┴──────────────────────────────────────────┐
│  llm-video-mcp server (Python)                    │
│  ├─ tools/analyze_video    ─┐                     │
│  ├─ tools/get_frames_at     │                     │
│  ├─ tools/get_transcript   ─┤                     │
│  │                          ▼                     │
│  │   ┌─ pipeline ─────────────────────────────┐   │
│  │   │ fetcher   (yt-dlp / local copy)        │   │
│  │   │ extractor (ffmpeg scene detect + floor)│   │
│  │   │ deduper   (sliding-window pixel diff)  │   │
│  │   │ transcriber (faster-whisper + VAD)     │   │
│  │   │ timeline  (shot table + motion labels) │   │
│  │   └────────────────────────────────────────┘   │
│  │                          ▼                     │
│  │   budget_controller (token_budget → 帧数/      │
│  │   分辨率/网格/转录截断 的参数反推)             │
│  │                          ▼                     │
│  │   cache/ (按视频内容 hash 缓存分析结果)        │
│  └──────────────────────────────────────────────  │
└───────────────────────────────────────────────────┘
```

### 依赖选型与理由

| 依赖 | 选型 | 理由 |
|---|---|---|
| 语言 | Python 3.10+ | 与竞品同生态，ffmpeg/whisper/MCP SDK 绑定最成熟；PyPI 分发即 CLI |
| 视频处理 | 系统 ffmpeg/ffprobe（subprocess） | 行业标准，竞品同选；不 pip 化，README 给出三平台安装命令（brew/apt/winget） |
| 下载 | yt-dlp | URL 输入的事实标准，竞品同选 |
| 转录 | **faster-whisper**（非 openai-whisper CLI） | 同模型数倍提速、VAD 门控防幻觉、Python API 直接调用（竞品也是 `[fast]` extra 才用它，我们设为默认）；模型可配 tiny→turbo |
| MCP | 官方 `mcp` Python SDK（stdio） | 官方协议实现，stdio 覆盖所有主流 coding agent host；暂不做 HTTP/SSE transport |
| 帧比较 | Pillow + numpy 下采样像素差 | 零额外 ML 依赖；不引入感知哈希（竞品 README 自述哈希对纯色/等亮度色盲，采纳其教训） |
| 分发 | PyPI `pip install` + `uvx` 一条命令跑 server | MCP host 配置里 `command: uvx llm-video-mcp` 是最低摩擦接入方式 |
| 许可证 | **MIT** | 与竞品对齐，最大化复用与传播 |

### 三点差异化 → 具体功能映射

| 差异化 | 落地功能 | 验收信号 |
|---|---|---|
| 1. MCP server 化 | 3 个 MCP tools（analyze/get_frames_at/get_transcript）+ `uvx` 一行接入 + 按内容 hash 缓存 | Claude Code 里贴一句"看看这个视频第 2 分钟讲了什么"，agent 自主调用 `get_frames_at` 完成，全程零人工搬运文件 |
| 2. token 预算自适应 | `token_budget` 参数 → 预算控制器反推帧数/分辨率/网格/转录长度；内置主流模型帧 token 估算表 | 给定 8k 与 128k 预算分析同一视频，帧数与输出体积显著不同且均不超预算（±10%） |
| 3. 开源时间线理解 | `timeline.json`：逐镜头表 + cuts/min + static/pan/zoom 标签 + 帧↔转录时间戳对齐 | 对标其 Pro `$19` 的核心卖点（镜头/节奏），开源免费；README 直接放对比表 |

---

## 验收标准（对齐 12 项上线 checklist）

仓库元数据与文档（对应组合复盘 playbook 的"上线前 12 项"）：

- [ ] 1. 仓库描述：一句话价值主张（≤120 字符）
- [ ] 2. MIT LICENSE 文件
- [ ] 3. ≥5 个 topics：`mcp-server` `llm` `video-analysis` `ffmpeg` `whisper` `claude-code` `coding-agent`
- [ ] 4. README 首屏：价值主张 + 30 秒内可复制的安装/接入命令 + 一张效果图
- [ ] 5. 可运行 demo：README 内嵌一条真实视频的分析结果摘录（帧数/转录片段/timeline 节选）
- [ ] 6. demo 视频或 GIF：60 秒内，真实安装 + 真实 agent 调用（对标竞品 HN 打法）
- [ ] 7. GitHub Pages：落地页（价值主张 + demo + 与竞品的对比表）
- [ ] 8. CI badge：GitHub Actions（lint + pytest，抽帧管线用 ≤10s 测试视频）
- [ ] 9. 初始 tag release：`v0.1.0`，release notes + demo 视频附件
- [ ] 10. `.gitignore`（Python + crv-out 类产物目录）
- [ ] 11. issue 模板（bug report / feature request）
- [ ] 12. pinned 到 shkyyy18 profile

功能验收（MVP 完成定义）：

- [ ] `uvx llm-video-mcp` 启动后，Claude Code 配置一次即可调用全部 3 个 tools
- [ ] 一段 5 分钟演讲视频，8k token 预算下端到端 <3 分钟完成（CPU，`base` whisper 模型）
- [ ] token 预算控制器单测：预算收紧时输出 token 估算单调下降且不破顶
- [ ] 静音视频输出"无语音"而非幻觉转录（VAD 门控生效）
- [ ] 时间线输出与人工抽查 3 个视频的镜头切分一致率 ≥90%

---

## 分发计划

| 阶段 | 渠道 | 动作 | 时机 |
|---|---|---|---|
| 首发 T0 | awesome-mcp / awesome-mcp-servers 列表 | 提 PR 收录（MCP 工具的默认被发现路径） | v0.1.0 release 当天 |
| T0 | r/LocalLLaMA + r/ClaudeCode（或 r/mcp） | 发帖：本地处理 + token 经济 + agent 原生三个点，附 demo GIF | 工作日美东上午（流量峰值） |
| T+3~7 天 | Show HN | 等 reddit/awesome 反馈修掉首发 bug 后再上；标题模板："Show HN: Let any coding agent watch videos via MCP (local, token-budgeted)"；避开竞品 HN 热度的正面撞车，强调 MCP 差异化而非"又一个抽帧器" | 有 ≥50 star 基础信号后 |
| 持续 | 每周 changelog + dev.to 长文（token 成本实测对比：固定 1fps vs 场景感知 vs 预算自适应） | 对标竞品的 marketing/devto 打法 | 每周 |
| 持续 | 月度评分复盘 | 按组合 100 分制评分，数据 `gh api` 采集 | 每月 19 日 |

---

## 退出条件（对齐三级退出漏斗）

**止损信号（任一出现即进入 L1 观察，两个周期不恢复即归档）**：

1. **上游降维（最致命）**：任一主流模型/agent host 在 6 个月内原生支持长视频输入，且同时满足 ①场景感知采样（非固定间隔）②免费或含在现有订阅内 ③可被 coding agent 直接调用——三者齐备即归档，不挣扎。
2. **竞品正面跟进**：claude-real-video 官方推出 MCP server 且覆盖 token 预算与时间线层（其迭代速度极快，单日 5 个 patch release，跟进风险真实存在）——届时评估是否转为给其提 PR 或合并。
3. **需求证伪**：上线 2 个评分周期（每月 19 日）后总分 <50 且 star <100，说明 MCP 化差异化不成立，归档止损。
4. **维护成本失控**：ffmpeg/yt-dlp/MCP 协议任何一方的 breaking change 导致周维护 >4 小时且社区无贡献者接棒。

**退出动作**：归档（不删除，遵循"归档优先、有外部依赖不删除"原则），README 更新指向继任方案（上游原生能力或竞品），Pages 保留作案例。

**演化出口（不行止损、上行的路）**：同一管线可扩展为"agent 多模态输入基础设施"——屏幕录像理解、会议理解、监控片段理解。若 v0.1 验证 token 预算控制器是真实痛点，可独立抽成通用库（任何多模态 agent 的上下文预算中间件），这比视频工具本身活得久。

---

## 风险与开放问题

### 风险

- **竞品迭代速度**（高）：v0.7.x 阶段单日多个 release，作者全职投入迹象明显（build in public + 付费产品闭环）。我们的窗口不是"它没想到"，而是"它忙着卖 Pro 顾不上 MCP"。
- **MCP 生态口味**（中）：MCP server 数量已泛滥（awesome-mcp 数百个），首发可能被淹没；demo 视频质量决定生死。
- **faster-whisper 模型体积**（低）：`turbo` 1.6GB 首次下载体验差；默认 `base` 缓解。
- **ffmpeg 系统依赖**（低，继承竞品已验证的解法）：三平台安装文档 + 启动时检测并给出友好报错。
- **版权合规**（低）：README 照抄竞品的免责声明立场——只下载有权下载的内容。

### 开放问题

1. **每帧 token 估算表从哪来**：各模型（Claude/GPT/Gemini/Kimi）图像 token 计价规则不同且会变，是内置静态表 + 允许用户覆盖，还是启动时联网拉取？倾向静态表 + `--model-config` 覆盖，避免网络依赖。
2. **MCP 返回帧的方式**：MCP image content（直接进上下文，简单）vs 落盘 + 返回路径（省 token，agent 需要时再读）？倾向两者都支持，`token_budget` 小时自动切落盘模式。
3. **是否做 HTTP transport**：stdio 覆盖单机 coding agent；远程/团队场景需要 HTTP。MVP 不做，看首发反馈。
4. **命名与商标**：`llm-video-mcp` 是工作名；竞品付费版在 Capafy 叫 "llm-real-video Pro"，名字需避开混淆，上线前定终名。
5. **与竞品的致谢与边界**：MIT 允许复刻，但我们自行实现（不复制其代码）；README 加致谢与"灵感来源"链接，既是伦理也是社区姿态（作者活跃于 X，正面关系有价值）。

---

*竞品数据采集：GitHub REST API（`gh api repos/HUANGCHIHHUNGLeo/claude-real-video` 及 README raw），2026-07-20。功能边界描述均以 README 原文为准。*
