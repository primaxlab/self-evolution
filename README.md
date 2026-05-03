# 🧬 完整自我进化系统 v4.0


> ⚠️ **注意**：本项目仍在积极开发中，部分功能尚未完善，API 和架构可能会发生变化。欢迎 Star 和 Issue 反馈！

> 整合 evolver-main + self-evolution + self-improving-agent + auto-reflection，实现AI助手完全自治进化。
> 
> 兼容 [OpenClaw](https://openclaw.ai) 和 [Hermes Agent](https://hermes-agent.nousresearch.com) 两大平台。

## 📊 概览

| 指标 | 数据 |
|------|------|
| 版本 | v4.0.0 |
| 核心功能 | **105项** |
| 源码文件 | 24个 |
| 技术栈 | JavaScript (Node.js ES Modules) |
| 许可证 | Apache-2.0 |
| 技能标准 | [agentskills.io](https://agentskills.io) |

## 🧠 六大核心系统

### 1. 自我意识系统 (15项功能)
身份连续性、价值观管理、情绪智能、认知风格配置

### 2. 自我学习引擎 (18项功能)
实时研究、知识管理、迁移学习、多源知识融合

### 3. 自我迭代框架 (16项功能)
错误处理、反馈闭环、持续优化、A/B测试

### 4. 永久记忆系统 (12项功能)
跨会话记忆、智能检索、隐私保护

### 5. 认知形态架构 (22项功能)
世界模型、高级推理、元认知、自适应优化

### 6. 独立人格系统 (22项功能)
个性发展、情感表达、道德判断、成长轨迹

## 🏗️ 四层架构

```
┌─────────────────────────────────┐
│        应用层 (Application)       │  用户交互界面
├─────────────────────────────────┤
│        服务层 (Service)           │  协调各核心组件
├─────────────────────────────────┤
│        核心层 (Core)              │  自我意识/学习/迭代/记忆
├─────────────────────────────────┤
│        数据层 (Data)              │  持久化存储
└─────────────────────────────────┘
```

## 📁 项目结构

```
├── complete_evolution.js      # 主入口（整合四大模块）
├── SKILL.md                   # 技能文档
├── ARCHITECTURE.md            # 架构设计
├── ROADMAP.md                 # 路线图 v4.0 → v4.4
├── agents/
│   └── improvement_agent.js   # 改进代理
├── core/
│   └── unified_evolution.js   # 统一进化核心
├── engines/
│   └── evolution_engine.js    # A2A协议进化引擎
├── scripts/
│   ├── self_awareness.js      # 自我意识系统
│   ├── browser_research.js    # 浏览器研究
│   └── error_handler.js       # 错误处理
├── systems/
│   └── predictive_system.js   # 预测系统
└── tests/                     # 测试文件
```


## ⚙️ 自定义配置

首次使用前，请替换以下占位符为你自己的信息：

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `<ai-name>` | 你的 AI 助手名字 | `"your-ai-name"` |
| `<owner-name>` | 你的名字 | `"your-name"` |
| `<relationship>` | 你与 AI 的关系 | `"助手"`、`"伙伴"` |

这些占位符出现在以下文件中：
- `ARCHITECTURE.md` — 身份数据结构示例
- `scripts/self_awareness.js` — 自我意识系统配置

搜索 `<ai-name>` 即可找到所有需要替换的位置。

## 🚀 快速开始

### 方式一：作为 OpenClaw 技能安装（推荐）

将此目录复制到 OpenClaw 的 `skills/` 目录下，即可作为技能使用：

```bash
# 复制到 OpenClaw skills 目录
cp -r . /path/to/openclaw/skills/complete-self-evolution
```

在 OpenClaw 中即可使用完整自我进化功能。

### 方式二：作为 Hermes Agent 技能安装

将此目录复制到 Hermes Agent 的 `~/.hermes/skills/` 目录下：

```bash
# 复制到 Hermes Agent skills 目录
cp -r . ~/.hermes/skills/complete-self-evolution
```

安装后在 Telegram / Discord / CLI 中使用：
```
/complete-self-evolution
```

### 方式三：独立运行

```bash
# 1. 安装依赖
npm install

# 2. 启动进化系统
npm start

# 3. 运行测试
node tests/test_simple.js
```

> ⚠️ 独立运行需要配置 A2A_NODE_ID 环境变量。

## 📦 下载

| 方式 | 链接 | 说明 |
|------|------|------|
| GitHub Release | [ZIP 下载](https://github.com/primaxlab/-/releases/download/v4.0/complete-self-evolution-v4.zip) | 139KB，解压即用 |
| 源码 | https://github.com/primaxlab/- | 直接查看代码 |

## 🗺️ 路线图

| 版本 | 目标 | 时间 |
|------|------|------|
| v4.0 | 完整基础框架 | 2026-04 |
| v4.1 | 重要功能实现 | 2026-04 |
| v4.2 | 标准能力部署 | 2026-05 |
| v4.3 | 高级智能集成 | 2026-05 |
| v4.4 | 完全自治实现 | 2026-06 |

## 🎯 性能目标

- 身份连续性: >99%
- 学习效率: >90%
- 错误减少率: >90%
- 记忆保留率: >98%

## 📝 License

[Apache-2.0](https://opensource.org/licenses/Apache-2.0)
