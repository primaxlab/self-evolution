# 🧬 Complete Self-Evolution System

> 整合 evolver-main + self-evolution + self-improving-agent + auto-reflection，实现 AI 助手完全自治进化。
>
> 兼容 [OpenClaw](https://openclaw.ai) 和 [Hermes Agent](https://hermes-agent.nousresearch.com) 两大平台。

---

## 📊 版本概况

| 分支 | 版本 | 技术栈 | 说明 |
|------|------|--------|------|
| [main](https://github.com/primaxlab/self-evolution) | **v5.0** | Python | 🆕 Sevo — 蓝图对齐的 Python 重写版 |
| [sevo-v5](https://github.com/primaxlab/self-evolution/tree/sevo-v5) | v5.0 | Python | 开发分支 |
| [main@v4.0](https://github.com/primaxlab/self-evolution/tree/47a802c) | v4.0 | JavaScript | JS 原始版（110 commits） |

> ⚠️ **注意**：本项目仍在积极开发中，API 和架构可能会发生变化。欢迎 Star 和 Issue 反馈！

---

## 🧠 Sevo v5.0 — Python 重写版

### 六大核心系统

| 系统 | 蓝图功能 | 实现状态 | 对齐度 |
|------|---------|---------|--------|
| 🪞 自我意识 (15项) | 身份、情绪(VAD)、价值观、OCEAN认知、动机、内省 | ✅ | **92%** |
| 🧠 认知架构 (22项) | 世界模型、推理引擎、元认知 | 🔲 v0.3 | — |
| 📚 学习引擎 (18项) | 经验提取、模式识别 | ✅ MVP | 20% |
| 🔄 迭代框架 (16项) | 错误处理、反馈闭环 | 🔲 v0.2 | — |
| 💾 永久记忆 (12项) | SQLite存储、检索、衰减 | ✅ MVP | 65% |
| 🎭 独立人格 (22项) | 个性、情感、道德判断 | 🔲 v0.3 | — |

### 项目结构

```
sevo/
├── core/                     # 进化引擎 + 配置
│   ├── engine.py             # 中心编排器
│   └── config.py             # 配置管理
├── awareness/                # 自我意识系统 ⭐
│   ├── awareness_system.py   # SelfAwarenessSystem 门面类
│   ├── identity.py           # 身份管理
│   ├── emotion.py            # 情绪三维模型 (VAD)
│   ├── values.py             # 价值观系统
│   ├── cognitive_style.py    # OCEAN大五认知风格
│   ├── motivation.py         # 内在动机 + 目标管理
│   └── introspection.py      # 内省系统
├── memory/
│   └── store.py              # SQLite持久化记忆
├── learning/
│   └── extractor.py          # 经验提取器
└── cli.py                    # 命令行工具

tests/                        # 51 个测试
├── test_awareness.py         # 自我意识系统 (28 tests)
├── test_engine.py            # 进化引擎 (5 tests)
├── test_emotion.py           # 情绪系统 (6 tests)
└── test_memory.py            # 记忆系统 (4 tests)
```

### 快速开始

```bash
# 安装
cd self-evolution-v5
pip install -e ".[dev]" --break-system-packages

# 交互式运行
python -m sevo.cli run

# 查看状态
python -m sevo.cli status

# 查询记忆
python -m sevo.cli memory "关键词"

# 运行测试
python -m pytest tests/ -v  # 51 passed
```

### 路线图

| 版本 | 目标 | 时间 |
|------|------|------|
| v5.0 | 完整基础框架 + 自我意识系统 | 2026-05 ✅ |
| v5.1 | 认知架构（世界模型 + 推理引擎 + 元认知） | 2026-05 |
| v5.2 | 学习引擎完整 + 记忆系统完善 | 2026-05 |
| v5.3 | 人格系统 + 迭代框架 | 2026-06 |
| v5.4 | 完全自治实现 | 2026-06 |

### 🎯 性能目标

- 身份连续性: >99%
- 学习效率: >90%
- 错误减少率: >90%
- 记忆保留率: >98%

---

## 📄 v4.0 JS 原始版 (参考)

<details>
<summary>展开查看 v4.0 JS 版本详情</summary>

### 概览

| 指标 | 数据 |
|------|------|
| 版本 | v4.0.0 |
| 核心功能 | **105项** |
| 源码文件 | 24个 |
| 技术栈 | JavaScript (Node.js ES Modules) |
| 许可证 | Apache-2.0 |

### 项目结构

```
├── complete_evolution.js      # 主入口
├── SKILL.md                   # 技能文档
├── ARCHITECTURE.md            # 架构设计
├── ROADMAP.md                 # 路线图
├── agents/
│   └── improvement_agent.js
├── core/
│   └── unified_evolution.js
├── engines/
│   └── evolution_engine.js    # A2A协议
├── scripts/
│   ├── self_awareness.js
│   ├── browser_research.js
│   └── error_handler.js
├── systems/
│   └── predictive_system.js
└── tests/
```

### 安装方式

**OpenClaw / Hermes Agent 技能安装：**
```bash
cp -r . ~/.hermes/skills/complete-self-evolution
```

**独立运行：**
```bash
npm install && npm start
# 测试: node tests/test_simple.js
```

</details>

---

## 📝 License

[Apache-2.0](https://opensource.org/licenses/Apache-2.0)