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
| YouTube | ✅ | ❌ 网络不可达 | — | 提取器正常；本机（大陆网络）不通，用户有代理时可走 `--proxy` |
| TikTok | ✅ | ❌ 网络不可达 | — | 同上；另需 `curl_cffi` impersonation 依赖 |
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

### 对视频号的明确结论

- **明确不支持在线获取**；文档中写明"视频号请提供本地视频文件路径"，只接受本地文件作为输入。注入/抓包路线有合规风险且维护成本高，不应进入本项目范围。

### 对 llm-video-mcp 的设计建议

- 第一梯队（开箱即用）：Bilibili、腾讯视频、优酷、微博；
- 第二梯队（需配置）：抖音/西瓜（cookie）、YouTube/TikTok（代理 + impersonation 依赖）；
- 明确不支持：视频号、快手、爱奇艺（DRM/提取器失效）、小红书（暂缓）；
- 所有平台统一兜底：接受本地文件路径 —— 这应作为一等公民输入方式写进 MCP 接口。

## 附：复现方式

```bash
python -m venv _spike/venv && _spike/venv/Scripts/python -m pip install -U yt-dlp
_spike/venv/Scripts/python -m yt_dlp --list-extractors
_spike/venv/Scripts/python -m yt_dlp --no-playlist --skip-download -J <URL>
```
