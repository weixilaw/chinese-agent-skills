# chinese-agent-skills 🇨🇳

精选中文 Agent Skills 合集 + 一键安装器。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](scripts/install.py)
[![Skills](https://img.shields.io/badge/Skills-4%20中文-orange.svg)](#-收录的-skills)
[![Tools](https://img.shields.io/badge/支持-8%20种%20AI%20工具-purple.svg)](#-支持的-ai-工具)

[English](#english) | [技能目录](#-收录的-skills) | [一键安装](#-一键安装) | [使用案例](#-跟-ai-这么说) | [FAQ](#️-常见问题)

## 简介

Agent Skills 是 Anthropic 发起、现已成为开放标准（[agentskills.io](https://agentskills.io)）的 AI 能力包格式：一份 `SKILL.md` 告诉 AI 怎么做一件事。但市面上的 skill 绝大多数是英文的，中文用户能直接用的很少。

这个仓库做了两件事：

1. **精选原创中文 skills**：为中文高频场景编写、开箱即用的 skills（合同审查、会议纪要、小红书文案、直播复盘）。
2. **一键安装器**：一条命令把 skill 装到你电脑上所有已安装的 AI 工具（Claude Code、Codex、Cursor、Gemini CLI、OpenCode……），零依赖，只需要 Python 3。

## ✨ 特性

- 🇨🇳 原生中文 skills，针对中文场景调优（中文合同、中文会议记录、中文社媒文案）
- 📦 一键安装到所有 AI 工具，自动检测已安装的工具
- 🐍 零依赖：安装器只用 Python 标准库，无需 npm / pip 装任何东西
- ✅ 安装前按 Agent Skills 开放标准校验 `SKILL.md`（name 与目录名一致、description 完整）
- 🔄 覆盖安装、卸载、预演（`--dry-run`）都支持

## 🚀 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/weixilaw/chinese-agent-skills/main/install.sh | bash
```

常用参数（透传给安装器）：

```bash
# 只装某几个 skill，且跳过确认
curl -fsSL https://raw.githubusercontent.com/weixilaw/chinese-agent-skills/main/install.sh | bash -s -- --skills contract-review,meeting-minutes -y

# 只装到指定工具
bash install.sh --tools claude-code,codex -y

# 先预演，看会装到哪里
bash install.sh --dry-run
```

> ⚠️ 管道安装前请先阅读 [`install.sh`](install.sh) 与 [`scripts/install.py`](scripts/install.py)，确认你信任其内容。

## 🔧 手动安装

```bash
git clone https://github.com/weixilaw/chinese-agent-skills.git
cd chinese-agent-skills
python3 scripts/install.py -y            # 安装全部 skill
python3 scripts/install.py list          # 查看自带 skills
python3 scripts/install.py tools         # 查看检测到的 AI 工具
python3 scripts/install.py remove <name> # 卸载某个 skill
python3 scripts/install.py validate <dir> # 校验一个 skill 目录是否符合开放标准
```

也可以用 GitHub 官方的 `gh skill`（GitHub CLI v2.90+）安装本仓库的 skills：

```bash
gh skill install weixilaw/chinese-agent-skills
```

## 📚 收录的 Skills

| Skill | 一句话用途 | 跟 AI 这么说 |
|---|---|---|
| [`contract-review`](skills/contract-review/SKILL.md) | 审查中文合同：识别高/中/低风险条款，给出修改建议与谈判要点 | "帮我审查这份租赁合同，标出对我不利的条款" |
| [`meeting-minutes`](skills/meeting-minutes/SKILL.md) | 把杂乱的会议记录/语音转录整理成结构化纪要：决议、待办（负责人+截止时间）、待确认事项 | "把这段会议录音转文字整理成纪要，待办要标负责人" |
| [`xiaohongshu-copy`](skills/xiaohongshu-copy/SKILL.md) | 写小红书种草/干货文案：3 个备选标题公式 + 正文结构 + 标签，自带合规红线 | "给我写一篇防晒霜种草笔记，要 3 个标题备选" |
| [`douyin-livestream-review`](skills/douyin-livestream-review/SKILL.md) | 复盘知识类直播：数据核对方法、转化漏斗定位、话术诊断 | "复盘我昨晚的直播，看看观众为什么留不住" |

每个 skill 都是一个独立文件夹（含 `SKILL.md`），可单独复制到任何支持 Agent Skills 的工具中使用。

## 💬 跟 AI 这么说

装好后，直接用自然语言让 AI 干活。下面是每个 skill 的实测可用说法，复制改关键词就行：

**合同审查**
> "这份《软件开发合同》对方发来的，帮我审查一遍，重点看付款、知识产权和违约责任，标出高风险条款并给修改建议"

**会议纪要**
> "这是今天项目例会的录音转文字（粘贴内容），整理成纪要：决议事项、待办（负责人+截止时间）、下次要确认的事"

**小红书文案**
> "写一篇'通勤包推荐'的种草笔记，3 个标题备选，正文按痛点-种草-避雷结构，标签给 8 个，别用极限词"

**直播复盘**
> "我昨晚播了 2 小时，场观 300，平均停留 1 分钟，帮我按转化漏斗定位问题出在哪一环"

## 🚫 做不到什么

诚实地说清楚边界，免得你期望错位：

- **不是律师 / 会计师 / 医生的替代品**：`contract-review` 给的是风险提示和谈判思路，**不构成法律意见**；标的额大或案情复杂请务必咨询执业律师。
- **不联网核实事实**：skill 不会帮你查法律法规是否更新、判例是否真实，关键引用请自己核对原文。
- **不保证文案爆款**：`xiaohongshu-copy` 给的是结构和合规写法，流量还看选题和账号权重。
- **不读取你的私密文件**：skill 只处理你主动粘贴/提供的内容，不会扫描你的电脑。

## 🛠 支持的 AI 工具

安装器通过检测配置目录判断工具是否已安装，并写入对应的个人技能目录：

| 工具 | 检测标记 | 写入的技能目录 |
|---|---|---|
| Claude Code | `~/.claude` | `~/.claude/skills` |
| Codex CLI | `~/.codex` | `~/.codex/skills`、`~/.agents/skills` |
| Cursor | `~/.cursor` | `~/.cursor/skills`、`~/.agents/skills` |
| Gemini CLI | `~/.muse` | `~/.gemini/skills`、`~/.agents/skills` |
| OpenCode | `~/.config/opencode` | `~/.config/opencode/skills`、`~/.agents/skills` |
| GitHub Copilot | `~/.copilot` | `~/.copilot/skills`、`~/.agents/skills` |
| OpenClaw | `~/.openclaw` | `~/.openclaw/skills` |
| 通用 | — | `~/.agents/skills`（多数新工具都会读取） |

未检测到任何工具时，默认安装到通用目录 `~/.agents/skills`。

**数据来源声明**：上表目录依据各工具官方文档核实（Claude Code、OpenAI Codex、Google Gemini CLI、OpenCode 官方文档等），核实时间 2026-10。各工具版本迭代可能调整目录，如发现过时欢迎提 Issue。

## ⚠️ 常见问题

**Q: 装完 skill，怎么确认生效了？**
A: 跑 `python3 scripts/install.py list` 看已安装列表；或者直接跟 AI 说"列出你可用的 skills"，看它能不能报出名字。

**Q: 我只想用其中一个 skill，不想全装？**
A: `bash install.sh --skills contract-review -y`，只装指定的。

**Q: 换电脑/重装后 skill 还在吗？**
A: 不在。skill 装在各工具的个人目录里，重装工具会丢。重新跑一遍一键安装即可（幂等，覆盖安装）。

**Q: skill 和 MCP 有什么区别？**
A: MCP 是给 AI 接外部数据源和工具的"线"（比如接数据库、接 API）；Skill 是教 AI 做一件事的"说明书"。两者互补，不冲突。

**Q: 我能把自己写的 skill 贡献进来吗？**
A: 欢迎！看下面的[贡献指南](#-贡献指南)，`validate` 通过就可以提 PR。

**Q: 这些 skill 会上传我的数据吗？**
A: 不会。skill 是本地 Markdown 文件，安装器也是本地运行，不联网、不收集任何信息。

## 🤝 贡献指南

欢迎贡献新的中文 skill！

1. Fork 本仓库，在 `skills/` 下新建文件夹（小写字母/数字/连字符，如 `my-skill`）。
2. 文件夹内必须包含 `SKILL.md`，开头为 YAML frontmatter，且 `name` 与文件夹名一致、`description` 一句话说清用途与触发场景（不超过 1024 字符）。
3. 用安装器自检：`python3 scripts/install.py validate skills/my-skill`。
4. 提交 Pull Request，说明这个 skill 解决什么中文场景问题。

## 📅 更新日志

### v1.0 (2026-10-18)
- 首发：4 个原创中文 skills（合同审查、会议纪要、小红书文案、直播复盘）
- 一键安装器：支持 8 种 AI 工具自动检测、零依赖、dry-run 预演、卸载

## ⚠️ 免责声明

- `contract-review`（合同审查）skill 为 AI 辅助工具，输出仅供参考，**不构成法律意见**；标的额较大或案情复杂的合同，请务必咨询执业律师。
- 运行一键安装脚本前请先阅读脚本内容；本项目不对因使用 skills 产生的任何结果负责。

## 📄 License

MIT License，详见 [LICENSE](LICENSE)。

---

<a id="english"></a>
## English

A curated collection of **Chinese-language Agent Skills** plus a zero-dependency one-click installer.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Agent Skills ([agentskills.io](https://agentskills.io), initiated by Anthropic, now an open standard) is a format that teaches AI agents how to do a specific task via a `SKILL.md` file. Most skills out there are English-only — this repo provides production-ready skills written natively in Chinese for high-frequency Chinese scenarios (contract review, meeting minutes, Xiaohongshu copywriting, livestream review), plus an installer that deploys them to every AI tool on your machine (Claude Code, Codex, Cursor, Gemini CLI, OpenCode, …) with a single command. Python 3 only, no other dependencies.

```bash
curl -fsSL https://raw.githubusercontent.com/weixilaw/chinese-agent-skills/main/install.sh | bash
```

Alternatively, with GitHub CLI v2.90+: `gh skill install weixilaw/chinese-agent-skills`

**Disclaimer**: the `contract-review` skill is an AI assistant tool for reference only and does not constitute legal advice. For high-value or complex contracts, consult a licensed attorney.

Licensed under MIT. See [LICENSE](LICENSE).
