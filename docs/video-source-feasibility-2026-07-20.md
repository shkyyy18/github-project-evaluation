# llm-video-mcp 视频源可行性实测报告

- 日期：2026-07-20
- 目的：立项前验证主流视频平台能否被程序化获取（管线：yt-dlp 下载 → ffmpeg 抽帧 → whisper 转录）
- 环境：Windows 11 + Git Bash，yt-dlp 装在隔离 venv（`_spike/venv`）
- 方法：仅 `--skip-download` / `-J` 取元数据，不下载完整视频；每个平台测 1–2 个真实 URL
- 所有结论均来自本机真实命令输出或真实检索，未做臆测

## 1. 环境

| 组件 | 版本 / 状态 |
|---|---|
| yt-dlp | **2026.07.04**（隔离 venv，pip 最新） |
| ffmpeg | ✅ 系统已装，`ffmpeg version 8.1.2-full_build`（WinGet 安装，Gyan build），无需额外安装 |
| python | 系统 python + `_spike/venv` |

yt-dlp 共 1752 个提取器（`--list-extractors` 行数）。

## 2. 提取器支持面（`yt-dlp --list-extractors` 实测）

| 平台 | 官方提取器 | 提取器名 |
|---|---|---|
| YouTube | ✅ | `youtube` 系列 |
| TikTok | ✅ | `TikTok`, `vm.tiktok`（部分子提取器标记 CURRENTLY BROKEN） |
| Bilibili | ✅ | `BiliBili` 系列 |
| 抖音 Douyin | ✅ | `Douyin` |
| 快手 Kuaishou | ❌ | 无（`kwai`/`kuaishou` 均无匹配） |
| 西瓜视频 | ✅ | `Ixigua` |
| 小红书 | ✅ | `XiaoHongShu` |
| 微信视频号 | ❌ | 无（`wechat`/`channels` 无匹配） |
| 优酷 | ✅ | `youku` |
| 腾讯视频 | ✅ | `vqq:video`, `wetv` 系列 |
| 爱奇艺 | ✅ | `iqiyi` |
| 微博视频 | ✅ | `Weibo`, `WeiboVideo` |

## 3. 实测探测结果（本机，中国大陆网络环境）

| 平台 | 测试 URL | 结果 | 关键信息 |
|---|---|---|---|
| YouTube | `youtube.com/watch?v=BaW_jenozKc` | ❌ | `timed out` 重试 3 次失败 —— **本机网络不可达**，非提取器问题 |
| TikTok | `tiktok.com/@cookierun_dev/video/7039716639834656002` | ❌ | `timed out`（网络不可达）+ 提示需安装 impersonation 依赖 |
| Bilibili | `bilibili.com/video/BV1bK411W797` | ✅ | 12 formats，时长 90s，**无需登录/cookie** |
| 抖音（网页长链） | `douyin.com/video/6950251282489675042` | ❌ | `Fresh cookies (not necessarily logged in) are needed` |
| 抖音（分享短链） | `v.douyin.com/L5pbfdP/` | ❌ | 短链**成功 302 解析**出视频 ID 6914948781100338440，随后同上 cookie 报错 |
| 快手 | `kuaishou.com/short-video/...` / `v.kuaishou.com/...` | ❌ | 无提取器，generic 兜底报 `Unsupported URL` |
| 西瓜视频 | `ixigua.com/6996881461559165471` | ❌ | `Cookies (not necessarily logged in) are needed` |
| 小红书 | `xiaohongshu.com/explore/6411cf99000000001300b6d9`（2 个 URL） | ❌ | `No video formats found!`（匿名访问页面不返回视频流，疑需 cookie） |
| 优酷 | `v.youku.com/v_show/id_XOTUxMzg4NDMy.html` | ✅ | 7 formats，时长 702s（另一个 URL 为加密视频报 `-2002 已加密`，属个例） |
| 腾讯视频 | `v.qq.com/x/page/q326831cny0.html` | ✅ | 8 formats，无需登录 |
| 爱奇艺 | `iqiyi.com/v_19rrojlavg.html`（2 个 URL） | ❌ | `Can't find any video` —— 提取器对当前站点结构失效/正片 DRM |
| 微博视频 | `weibo.com/7827771738/N4xlMvjhI` | ✅ | 4 formats，时长 918s，无需登录 |

## 4. 视频号专项

**yt-dlp 不支持微信视频号**（2026.07.04 版本无提取器，检索其 issue 区也无官方支持计划）。视频号自 2023 年起对视频流加密 + 鉴权，纯 URL 抓取不可行。当前可行技术路线（来自真实检索）：

1. **PC 微信注入式下载器** —— [ltaoo/wx_channels_download](https://github.com/ltaoo/wx_channels_download)、[nobiyou/wx_channel](https://github.com/nobiyou/wx_channel)（支持加密视频解密）
   - 门槛：需 PC 微信登录态；对微信版本敏感（新版 4.1 需走「收藏页」迂回）；部分需管理员权限
   - 条款风险：中-高（注入第三方进程，明确违反微信软件许可）；工程复杂度：高，且随微信版本升级频繁失效
2. **代理抓包/嗅探** —— res-downloader、「万能嗅探」等：本地起 MITM 代理 + 安装根证书，播放视频号时嗅探视频地址
   - 门槛：需安装根证书、微信登录态；条款风险：中；工程复杂度：中（证书 + 代理 + 解密逻辑）
3. **第三方解析 API / 小程序** —— 灰色在线服务，稳定性差、随时失效，不适合作为开源项目依赖
   - 门槛：低但不可靠；条款风险：高

**结论：视频号没有干净、稳定、合规的程序化获取路径，不适合纳入本项目支持范围。**

## 5. 平台支持矩阵与结论

| 平台 | 提取器 | 实测 | 需登录/cookie | 备注 |
|---|---|---|---|---|
| Bilibili | ✅ | ✅ 成功 | 否 | **首选支持** |
| 腾讯视频 | ✅ | ✅ 成功 | 否 | 可支持 |
| 优酷 | ✅ | ✅ 成功 | 否 | 部分视频加密，属个例 |
| 微博视频 | ✅ | ✅ 成功 | 否 | 可支持 |
| YouTube | ✅ | ✅ 代理复测成功（31 formats，2026-07-20 经 127.0.0.1:19077） | 否 | 直连不通，走代理即可用；建议本项目支持配置代理 |
| TikTok | ✅ | ⚠️ 有条件可行（2026-07-20 二轮深度复测定性） | — | 根因是代理出口在香港被 TikTok 区域重定向（302→`/hk/about`），非提取器失效；换非 HK 出口预期可用但本机无法验证，见第 7 节 |
| 抖音 | ✅ | ⚠️ 短链解析 OK，取流需 cookie | 是（fresh cookie，不必登录） | 见下 |
| 西瓜 | ✅ | ❌ 需 cookie | 是 | 同抖音（字节系反爬） |
| 小红书 | ✅ | ❌ 无格式返回 | 疑似需要 | 提取器对匿名访问失效 |
| 爱奇艺 | ✅ | ❌ 提取器失效 | — | 正片 DRM，不建议支持 |
| 快手 | ❌ | ❌ Unsupported URL | — | 不支持 |
| 微信视频号 | ❌ | — | — | **明确不支持** |

### 对抖音的明确结论

- 分享短链（`v.douyin.com/xxx`）**可以被 yt-dlp 正确解析**到视频 ID，链路本身可用；
- 但字节系反爬要求 fresh cookie（不要求登录）。可行路径：
  1. **主路径**：接受用户提供的 cookie（yt-dlp `--cookies-from-browser` 或 cookies.txt），抖音/西瓜即可走通；
  2. **兜底路径**：提示用户手动下载视频后传入本地文件路径（本项目管线对本地文件天然支持）；
  3. 无 cookie 直取在当前版本**不可行**，不要作为设计假设。
- 2026-07-20 `--cookies-from-browser` 补测（见第 6 节）：本机 Edge/Chrome 运行中 cookie 数据库被独占锁定，yt-dlp 无法读取（已知上游 issue #7271），Firefox 未安装。**该路径在本机未验证成功**，工程上需引导用户关闭浏览器一次或使用 cookies.txt 导出。

### 对视频号的明确结论

- **明确不支持在线获取**；文档中写明"视频号请提供本地视频文件路径"，只接受本地文件作为输入。注入/抓包路线有合规风险且维护成本高，不应进入本项目范围。

### 对 llm-video-mcp 的设计建议

- 第一梯队（开箱即用）：Bilibili、腾讯视频、优酷、微博；
- 第二梯队（需配置）：抖音/西瓜（cookie）、YouTube（代理，2026-07-20 代理复测已成功）、TikTok（代理 + 非 HK 出口节点，见第 7 节）；
- 明确不支持：视频号、快手、爱奇艺（DRM/提取器失效）、小红书（暂缓）；
- 所有平台统一兜底：接受本地文件路径 —— 这应作为一等公民输入方式写进 MCP 接口。

## 6. 代理复测（2026-07-20，系统代理 http://127.0.0.1:19077）

用户开启 VPN 后复测（`https_proxy`/`http_proxy` 环境变量，yt-dlp 已确认代理生效：`Proxy map: {'http': ..., 'https': ...}`）：

| 平台 | 复测结果 | 关键信息 |
|---|---|---|
| YouTube | ✅ 成功 | `youtube.com/watch?v=dQw4w9WgXcQ`：31 formats、时长 213s、无需登录。首次测试的 `BaW_jenozKc` 报 "Video unavailable" 为该视频本身状态，换公开视频即成功。另有提示：无 JS runtime（deno）时部分格式可能缺失，建议项目侧装 deno |
| TikTok | ❌ 失败（根因在第 7 节定性为区域重定向） | 3 个真实 URL 均报 `Unexpected response from webpage request`，堆栈止于 `tiktok.py` `_solve_challenge_and_set_cookies`；已在 venv 安装 `curl_cffi 0.15.0`（impersonation 依赖）后重测仍失败 |
| 抖音（`--cookies-from-browser`） | ⚠️ 未能完成验证 | Edge、Chrome 均在运行，cookie SQLite 数据库被独占锁定（Python 直 copy 与 PowerShell `FileShare.ReadWrite` 均 PermissionError），yt-dlp 报 `Could not copy Chrome cookie database`（上游已知 issue #7271）；Firefox 未安装。**未读取/记录任何 cookie 内容**。可行解法：用户关闭浏览器后重试，或用浏览器扩展导出 cookies.txt 走 `--cookies` |

### 抖音 cookie 路径最终结论

- yt-dlp 的 `--cookies-from-browser` 机制本身支持 Chromium 系浏览器，本机验证的**唯一阻塞是浏览器运行时独占锁**；
- 对本项目（本地工具、agent 调用）的工程建议：① 文档引导用户在抓取抖音前关闭浏览器一次（锁释放后即可借用 fresh cookie，无需登录态导出）；② 更稳的做法是支持用户粘贴/放置 cookies.txt（一次导出、长期复用，不受浏览器锁影响）；③ 本地文件兜底保留。

## 7. TikTok 深度复测 + 抖音 cookie 复测（2026-07-20 第二轮）

### TikTok 深度复测：根因定位

穷尽以下路径后完成定性（全程经代理 127.0.0.1:19077，仅取元数据）：

| 尝试 | 结果 |
|---|---|
| 升级 yt-dlp 2026.07.04 → nightly `2026.07.14.233956`（`pip install -U --pre`） | 仍报 `Unexpected response from webpage request` |
| 换 URL 形态：3 个网页长链（hankgreen1 / leenabhushan / cookierun_dev） | 同样报错 |
| `vm.tiktok.com` 短链 | 测试码 404（未获得有效短链，未形成有效样本） |
| `--impersonate chrome` | 同样报错 |
| gh api 检索 yt-dlp 仓库 tiktok 相关 issue（15+ 条 open） | 无同症状系统性故障报告；TikTok 提取器维护活跃，多为常规 bug |

**根因实锤（curl 直接验证，与 yt-dlp 无关）**：

```text
$ curl -L "https://www.tiktok.com/@hankgreen1/video/7047596209028074758"
HTTP 200, final: https://www.tiktok.com/hk/about   ← 视频页被 302 到"香港不可用"说明页
$ curl ipinfo.io → 194.99.79.32, Hong Kong (AS199524 G-Core Labs)
```

- 本机 VPN 出口在**香港**，而 TikTok 不对香港提供服务，所有视频页被重定向到 `/hk/about`；yt-dlp 拿到的不是挑战页也不是视频页，因此报 "Unexpected response" —— 这是**出口节点区域问题，不是提取器失效**。
- 结论修正：**TikTok 有条件可行**。yt-dlp 提取器本身正常（issue 区无系统性故障），只需把代理出口切到 TikTok 提供服务地区（美/日/新等）。本机只有一个 HK 出口，未能实测验证非 HK 场景——这是唯一保留的不确定性。
- 对本项目：TikTok 支持 = 代理 + 出口区域要求，文档写明即可，无需特殊代码。

### 抖音 cookie 路径复测

- 2026-07-20 第二轮检查：Edge、Chrome 进程**仍在运行**（tasklist 确认），cookie 数据库仍被独占锁定，`--cookies-from-browser` 无法执行，本轮**仍未能实锤**。
- 维持第 6 节结论：机制可行、唯一阻塞是浏览器运行时锁；推荐 cookies.txt 作为主路径（一次导出、不受锁影响），本地文件兜底。

## 附：复现方式

```bash
python -m venv _spike/venv && _spike/venv/Scripts/python -m pip install -U yt-dlp
_spike/venv/Scripts/python -m yt_dlp --list-extractors
_spike/venv/Scripts/python -m yt_dlp --no-playlist --skip-download -J <URL>
```
