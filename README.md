# 🧬 Sevo — Complete Self-Evolution System v5.0

**从零重新开发的 AI 智能体完整自我进化系统。**

## 🎯 六大核心系统

| 系统 | 核心能力 | 状态 |
|------|---------|------|
| 🪞 **自我意识** | 身份连续性、情绪三维模型、价值观 | ✅ MVP |
| 📚 **学习引擎** | 经验提取、模式识别、反思 | ✅ MVP |
| 🔄 **迭代框架** | 错误处理、反馈闭环 | 🔲 v0.2 |
| 💾 **永久记忆** | SQLite存储、智能检索、记忆衰减 | ✅ MVP |
| 🏛️ **认知架构** | 世界模型、推理引擎 | 🔲 v0.3 |
| 🎭 **独立人格** | 个性特征、情感表达 | 🔲 v0.3 |

## 📁 项目结构

```
sevo/
├── core/
│   ├── engine.py          # 主进化引擎
│   └── config.py          # 配置管理
├── awareness/
│   ├── identity.py         # 身份管理
│   ├── emotion.py          # 情绪三维模型
│   └── values.py           # 价值观系统
├── memory/
│   └── store.py            # SQLite持久化记忆
├── learning/
│   └── extractor.py         # 经验提取
└── cli.py                  # 命令行工具
```

## 🚀 快速开始

```bash
# 安装
pip install .

# 交互式运行
python -m sevo.cli run

# 查看状态
python -m sevo.cli status

# 查询记忆
python -m sevo.cli memory "关键词"

# 执行记忆衰减
python -m sevo.cli decay --days 30
```

## 📊 核心特性

- **纯 Python**：零外部依赖（可选 openai 用于 LLM 增强）
- **SQLite 存储**：记忆跨会话持久化
- **情绪引擎**：关键字驱动的 valance/arousal/dominance 三维模型
- **经验提取**：从对话中自动提取错误、洞察、经验
- **进化阶段**：从 Emergence → Growth → Maturity → Excellence → Transcendence

## 🔧 配置

```bash
# 通过环境变量
export SEVO_DATA_DIR=/path/to/data
export SEVO_LLM_PROVIDER=openai
export SEVO_LLM_MODEL=gpt-4o
```

## 📝 License

Apache-2.0