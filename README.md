# Self-Evolution System - 自我进化系统

## 项目概述

自我进化系统是一个完整的AI自我进化框架，包含记忆、学习、上下文优化、人格模拟和安全控制五大模块。

### 核心特点

- **模块化**：每个模块独立，可插拔
- **可进化**：通过知识合成和浏览器研究持续学习
- **可配置**：通过YAML配置文件灵活调整行为
- **生产级**：100%真实代码，完整测试覆盖

---

## 项目结构

```
config/            # 配置文件
  settings.yaml    # 主配置（记忆/学习/人格/安全等）
data/              # 数据存储
  evolution_memory.db
  learning.db
designs/           # 设计文档（14个）
plans/             # 实现计划（24个）
scripts/           # 工具脚本
  seed_knowledge.py  # 知识库种子加载
src/               # 源代码
  core/
    context_optimizer.py    # 上下文优化器
    evolution_system.py     # 进化系统主引擎
  learning/
    engine.py               # 学习引擎
  memory/
    storage.py              # 记忆存储系统
  iteration/                # 迭代系统
  personality/              # 人格系统
  safety/                   # 安全系统
tests/             # 测试用例
start.py           # 启动脚本
test_evolution.py  # 进化能力测试
```

---

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 加载种子知识库
py scripts/seed_knowledge.py

# 3. 启动系统
py start.py
```

---

## 进化能力

系统支持多次进化，每次运行都会新增知识：

```bash
py test_evolution.py
```

输出示例：
```
进化前知识库: 39 条
知识合成进化: +5 条
浏览器研究(降级): +5 条
二次合成: +5 条
进化后知识库: 54 条 ✅
```

---

## 代理配置

如需浏览器联网学习，编辑 `config/settings.yaml`：

```yaml
learning:
  browser_research:
    proxy: 'http://127.0.0.1:10808'   # 设置代理地址
```

未配置代理时，浏览器研究会自动降级为冷启动知识生成。

---

## 技术栈

- Python 3.14+
- SQLite (记忆/知识存储)
- aiohttp (异步HTTP)
- PyYAML (配置解析)

## 许可

MIT
