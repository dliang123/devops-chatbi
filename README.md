# 🚀 DevEfficiency-ChatBI: 研发效能领域的智能决策大脑

> **打破数据孤岛，让研发效能数据“开口说话”。**

**DevEfficiency-ChatBI** 是一款专为研发效能领域打造的智能助手。基于 **Multi-Agent** 架构，它能够理解复杂的研发管理语境，通过自然语言对话直接调取 Jira、GitHub、GitLab、SonarQube 及内部数据库中的指标，并生成深度的效能分析报告。

---

## 🌟 核心亮点

* **🎯 深度行业上下文**：内置研发效能（DevOps/DORA）指标模型，理解“需求交付周期”、“代码合并频率”及“发布成功率”等专业术语。
* **🤖 多智能体协同 (Multi-Agent)**：基于 **LangGraph** 构建动态工作流。通过 Intent-Agent（意图识别）、SQL-Agent（自动写数）、Checker-Agent（SQL 安全校验）及 Analyst-Agent（数据挖掘）的协同，确保结果的精准性。
* **🛠️ 实时工具链集成**：利用 **LangChain** 的工具调用能力，支持实时查询研发工具链数据，而非仅仅依赖历史快照。
* **⚡ 极速响应**：后端由 **FastAPI** 驱动，支持流式输出（Streaming），提供毫秒级的交互体验。
* **🛡️ 企业级安全**：多层级 SQL 注入防护与敏感数据脱敏逻辑，保障核心资产安全。

---

## 🏗️ 技术栈

* **LLM 编排**: [LangChain](https://github.com/langchain-ai/langchain) / [LangGraph](https://github.com/langchain-ai/langgraph) (用于管理复杂的循环状态机)
* **API 框架**: [FastAPI](https://fastapi.tiangolo.com/) (高性能异步 Web 服务)
* **向量检索**: ChromaDB / Pinecone (用于效能知识库 RAG)
* **UI 展示**: Streamlit / Next.js (支持图表渲染与对话交互)

---

## 🚀 为什么加入我们？

在研发效能领域，数据往往散落在各个系统中，管理者和开发者很难快速获取直观的洞察。
我们正在做一件**极具挑战性**的事情：**让复杂的 SQL 逻辑和效能模型，对所有研发成员透明。**

**我们需要这样的你：**

* **AI 爱好者**：探索如何用 LangGraph 处理更复杂的 Agent 循环纠错逻辑。
* **研发效能专家**：帮助我们定义更科学的效能评估 Prompt。
* **后端极客**：优化 FastAPI 的并发处理与异步任务流。

---

## 📅 路线图 (Roadmap)

* [ ] 🟢 **v0.1**: 实现基础 SQL 生成与数据查询。
* [ ] 🟡 **v0.2**: 引入 Multi-Agent 架构，增强复杂意图拆解。
* [ ] ⚪ **v0.3**: 支持自定义研发效能看板导出。
* [ ] ⚪ **v0.4**: 适配钉钉/企微等办公平台。

---

## 🤝 参与贡献

1. **Fork** 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 开启 **Pull Request**


