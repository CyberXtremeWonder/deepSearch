# DeepSearch Agent

> 基于 DeepAgents 构建的深度研究（Deep Research）多智能体系统。

DeepSearch Agent 面向复杂的深度研究场景，通过 **主智能体 + 专家子智能体** 的多智能体架构，根据任务需要自动选择不同的信息来源，包括公开互联网、结构化数据库、RAGFlow 私有知识库以及用户上传的附件。

系统不仅能够完成信息检索，还可以进一步进行内容分析、结果汇总，并将最终研究结果生成 **Markdown / PDF** 等交付形式。

---

## ✨ 项目简介

传统的大语言模型应用通常采用：

```text
用户问题 → LLM → 最终回答
```

这种模式在面对复杂研究任务时容易受到知识时效性、数据来源以及上下文长度等限制。

DeepSearch Agent 将复杂任务拆分为多个专业环节，通过主智能体统一规划和调度不同的专家子智能体，使系统能够根据任务需求访问不同的数据源：

```text
                         用户任务
                            │
                            ▼
                   ┌─────────────────┐
                   │    主智能体      │
                   │  Task Planner   │
                   └────────┬────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
      ┌────────────┐ ┌────────────┐ ┌────────────┐
      │ 网络搜索助手 │ │ 数据库查询助手│ │ RAGFlow助手 │
      │   Tavily    │ │    MySQL   │ │  RAGFlow   │
      └──────┬─────┘ └──────┬─────┘ └──────┬─────┘
             │              │              │
             ▼              ▼              ▼
          公共网络        结构化数据       私有知识库
             │              │              │
             └──────────────┼──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  主智能体汇总 │
                     └───────┬──────┘
                             │
                             ▼
                    Markdown / PDF / Answer
```

---

# 🚀 项目特点

## 1. 一主三从的多智能体架构

采用 **One Master + Three Specialists** 的设计。

### 主智能体

主智能体负责整个任务生命周期：

- 理解用户任务
- 分析任务需求
- 制定研究计划
- 判断需要哪些数据来源
- 调度不同专家子智能体
- 汇总多个子任务结果
- 生成最终回答
- 根据需要生成 Markdown / PDF

主智能体并不直接承担所有检索工作，而是作为整个研究流程的 **Orchestrator（任务编排器）**。

### 专家子智能体

系统目前包含三个主要专家：

| 智能体 | 数据来源 | 主要职责 |
|---|---|---|
| 网络搜索助手 | Tavily | 公开互联网信息检索 |
| 数据库查询助手 | MySQL | 结构化业务数据查询 |
| RAGFlow 助手 | RAGFlow | 私有非结构化知识库检索 |

此外，主智能体还可以直接读取用户上传的附件。

---

# 🔍 多来源信息检索

DeepSearch Agent 不依赖模型自身的知识进行“裸答”，而是根据任务需求调用不同的数据源。

## 🌐 互联网搜索

使用 Tavily 获取公开互联网信息。

适用于：

- 最新新闻
- 行业信息
- 技术资料
- 公司信息
- 学术资料
- 产品信息
- 实时公开数据

网络搜索助手负责从不同角度进行检索，并将结果返回给主智能体进行进一步分析。

---

## 🗄️ 结构化数据库

使用 MySQL 作为结构化数据源。

数据库助手负责：

- 数据库结构分析
- 表结构查询
- 字段理解
- SQL 查询
- 业务数据分析
- 查询结果整理

典型流程：

```text
用户问题
   ↓
数据库 Schema 分析
   ↓
生成 SQL
   ↓
执行 SQL
   ↓
返回结构化结果
```

---

## 📚 RAGFlow 私有知识库

通过 RAGFlow 查询企业内部非结构化知识。

适用于：

- 企业内部文档
- 技术文档
- 产品资料
- 业务规范
- PDF / Word 文档
- 企业知识库

典型流程：

```text
用户任务
   ↓
主智能体
   ↓
RAGFlow 助手
   ↓
私有知识库检索
   ↓
返回相关文档内容
   ↓
主智能体分析
```

---

## 📎 用户上传附件

用户可以直接上传文件。

主智能体可以通过文件工具读取用户提供的资料，并将其与：

- 互联网搜索结果
- MySQL 数据
- RAGFlow 知识

进行综合分析。

因此系统能够支持：

```text
用户问题
   +
上传 PDF / Markdown / 文本等资料
   +
互联网资料
   +
数据库数据
   +
企业知识库
   ↓
综合研究
```

---

# 📄 从检索到交付

项目不仅实现了信息检索，还实现了完整的研究结果交付链路。

```text
用户任务
    ↓
任务分析
    ↓
研究规划
    ↓
调用专家智能体
    ↓
多来源信息检索
    ↓
结果分析与整合
    ↓
生成最终报告
    ↓
┌───────────────┐
│ Answer        │
│ Markdown      │
│ PDF           │
└───────────────┘
```

系统可以根据任务需要生成：

- 普通回答
- Markdown 文档
- PDF 报告

因此整个项目不是单纯的 Prompt Demo，而是一个完整的：

**Agent → Tool → Data → Result → Artifact**

工作流。

---

# 📡 长任务实时监控

深度研究任务通常需要较长的执行时间，因此项目使用：

- FastAPI
- WebSocket
- Monitor / Event

实现任务执行过程的实时推送。

前端可以实时获取：

```text
任务创建
    ↓
主智能体开始执行
    ↓
调用网络搜索助手
    ↓
网络搜索完成
    ↓
调用数据库助手
    ↓
数据库查询完成
    ↓
调用 RAGFlow 助手
    ↓
生成最终报告
    ↓
任务完成
```

监控事件包括：

- 工具调用
- 子智能体调用
- 工作目录创建
- 检索结果
- 任务状态
- 任务完成
- 任务取消
- 异常信息
- 文件生成

用户无需长时间等待一个最终结果，可以实时观察 Deep Research 的执行过程。

---

# 🔐 会话级上下文隔离

项目针对多用户、多任务场景设计了会话级上下文隔离机制。

通过：

```text
thread_id
session_dir
ContextVar
```

实现不同任务之间的上下文隔离。

每个研究任务拥有独立的：

```text
thread_id
session_dir
工作文件
中间结果
最终产物
```

深层工具无需显式层层传递 session 信息，也可以通过 `ContextVar` 获取当前会话上下文。

核心设计示例：

```python
_session_dir_ctx = ContextVar(
    "_session_dir",
    default=None
)

_thread_id_ctx = ContextVar(
    "_thread_id",
    default=None
)
```

这种设计可以避免不同用户或不同任务之间出现文件和上下文混用的问题。

---

# 🏗️ 系统架构

整体采用前后端分离设计：

```text
┌─────────────────────────────────────────────┐
│                   Frontend                  │
│                   React                     │
│                                             │
│  Task UI │ Monitor │ Upload │ Download      │
└───────────────────┬─────────────────────────┘
                    │
              HTTP / WebSocket
                    │
┌───────────────────▼─────────────────────────┐
│                   Backend                   │
│                  FastAPI                    │
│                                             │
│  Task API │ WebSocket │ File │ Agent       │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
             ┌──────────────┐
             │  DeepAgents  │
             │              │
             │ Main Agent   │
             └───────┬──────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   Tavily Agent   DB Agent   RAGFlow Agent
        │            │            │
        ▼            ▼            ▼
    Internet       MySQL       RAGFlow
```

---

# 🛠️ 技术栈

## Backend

- Python
- FastAPI
- WebSocket
- DeepAgents
- AsyncIO

## AI / Agent

- DeepAgents
- LLM
- Tavily
- RAGFlow

## Data

- MySQL
- RAGFlow
- 用户上传文件

## Frontend

- React
- WebSocket
- HTTP API

## Deployment

- Docker
- Docker Compose

---

# 📂 项目结构

```text
deepsearch-agent/
│
├── app/
│   ├── agent/
│   │   ├── main_agent.py
│   │   └── ...
│   │
│   ├── tools/
│   │   └── ...
│   │
│   ├── api/
│   │   └── ...
│   │
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── docker/
│   └── ...
│
├── tests/
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── ...
```

> 实际目录结构请以项目当前代码为准。

---

# ⚙️ 环境要求

建议环境：

```text
Python >= 3.10
Node.js >= 18
MySQL
Docker
Docker Compose
```

同时需要配置相关外部服务：

- LLM API
- Tavily API
- MySQL
- RAGFlow

---

# 🔧 配置环境变量

复制环境变量模板：

```bash
cp .env.example .env
```

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

根据实际环境配置：

```env
# LLM
LLM_MODEL_ID=
LLM_API_KEY=
LLM_BASE_URL=

# Tavily
TAVILY_API_KEY=

# MySQL
MYSQL_HOST=
MYSQL_PORT=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_DATABASE=

# RAGFlow
RAGFLOW_BASE_URL=
RAGFLOW_API_KEY=
```

> 实际环境变量名称请以项目中的 `.env.example` 为准。

**不要将 `.env`、API Key、数据库密码等敏感信息提交到 Git 仓库。**

---

# ▶️ 快速开始

## 1. 克隆项目

```bash
git clone https://github.com/CyberXtremeWonder/deepSearch.git
cd deepSearch
```

---

## 2. 安装 Python 依赖

项目使用 `uv` 管理 Python 环境：

```bash
uv sync
```

运行：

```bash
uv run python -m app.agent.main_agent
```

---

## 3. 安装前端依赖

进入前端目录：

```bash
cd frontend
```

安装依赖：

```bash
npm install
```

启动：

```bash
npm run dev
```

---

## 4. 启动后端

返回项目根目录：

```bash
cd ..
```

根据项目实际入口启动，例如：

```bash
uv run python -m app.agent.main_agent
```

或者：

```bash
uv run uvicorn app.main:app --reload
```

---

# 🧪 典型任务

例如用户提出：

> 分析某行业最近三年的发展趋势，并结合公司内部销售数据和内部技术文档给出研究报告。

主智能体可能执行：

```text
1. 分析任务
      ↓
2. 制定研究计划
      ↓
3. 调用 Tavily
   搜索行业公开资料
      ↓
4. 调用 MySQL Agent
   查询公司销售数据
      ↓
5. 调用 RAGFlow Agent
   查询内部技术文档
      ↓
6. 综合分析多来源信息
      ↓
7. 生成研究结论
      ↓
8. 生成 Markdown
      ↓
9. 转换 PDF
      ↓
10. 返回最终报告
```

最终用户得到的不只是一个模型回答，而是一份经过多来源信息检索和综合分析后的研究结果。

---

# 🎯 项目核心能力

| 能力 | 支持 |
|---|---|
| 多智能体协作 | ✅ |
| 主智能体任务规划 | ✅ |
| 专家智能体调度 | ✅ |
| 互联网搜索 | ✅ |
| MySQL 查询 | ✅ |
| RAGFlow 检索 | ✅ |
| 用户附件读取 | ✅ |
| Markdown 生成 | ✅ |
| PDF 生成 | ✅ |
| WebSocket 实时监控 | ✅ |
| 长任务执行 | ✅ |
| 任务取消 | ✅ |
| 异常监控 | ✅ |
| 会话上下文隔离 | ✅ |
| Docker 部署 | ✅ |

---

# 🔮 后续规划

- [ ] 支持更多搜索引擎
- [ ] 增加学术论文搜索 Agent
- [ ] 增加代码分析 Agent
- [ ] 增加浏览器操作 Agent
- [ ] 增加更多数据库类型
- [ ] 增加多模态文档理解
- [ ] 增加研究报告引用管理
- [ ] 增加任务暂停 / 恢复
- [ ] 增加 Agent 执行轨迹回放
- [ ] 增加任务成本与 Token 统计
- [ ] 增加多用户权限管理
- [ ] 增加 Docker Compose 一键部署

---

# 💡 项目定位

DeepSearch Agent 的核心目标不是构建一个简单的 ChatBot，而是构建一个能够完成：

> **任务理解 → 研究规划 → 多源检索 → 专家协作 → 信息分析 → 结果汇总 → 文档生成**

完整闭环的 **Deep Research Agent**。

通过多智能体架构，将 LLM 的推理能力与互联网、数据库、私有知识库以及用户文件结合起来，使模型从单纯的“回答问题”进一步转变为能够**自主执行复杂研究任务的智能系统**。

---

# 📄 License

本项目主要用于学习、研究和技术交流。

