# OpenManus 核心机制详解

## 1\. OpenManus 概述

OpenManus 是对闭源 Manus AI 的开源复现项目，由 MetaGPT 团队主导开发（原型仅用 3 小时完成）。它是一个模块化的多代理（multi-agent）AI Agent 框架，支持本地部署、多模型集成（如 Claude、GPT-4o、Qwen、Ollama 本地模型），无需邀请码即可使用。

核心目标：实现自主执行复杂任务（如旅行规划、股票分析、网站构建、数据处理），通过工具调用和迭代循环模拟人类操作。

主要仓库：https://github.com/FoundationAgents/OpenManus

## 2\. 整体架构

OpenManus 采用**模块化 + 分层 + 多代理** 设计，主要组件包括：

  * **Agent 层** ：各种代理（BaseAgent、ReActAgent、ToolCallAgent、PlanningAgent 等）
  * **LLM 层** ：大语言模型接口，支持多提供商
  * **Memory 层** ：上下文记忆管理
  * **Tool 层** ：工具集（浏览器自动化、代码执行、搜索、文件操作等）
  * **Flow 层** ：工作流编排（协调代理执行顺序）
  * **Prompt 层** ：提示模板管理

层次化代理结构：从基础代理逐步扩展到专项代理，形成“团队”协作。

## 3\. 两种执行模式（核心创新）

模式 | 入口 | 适用场景 | 特点  
---|---|---|---  
Direct Agent Mode（直接代理模式） | main.py | 简单任务 | 灵活、快速，直接由主代理处理  
Flow Orchestration Mode（流程编排模式） | run_flow.py | 复杂任务 | 结构化规划、多代理协作、更可靠  
  
## 4\. 多代理协作机制

类似于“项目团队”：

  * **主代理（Main Agent / Manus Agent）** ：接收用户任务、整体协调、决定执行模式
  * **规划代理（PlanningAgent）** ：任务分解、生成计划（e.g., todo.md）
  * **工具调用代理（ToolCallAgent）** ：执行具体行动、调用工具
  * **其他专项代理** ：如 Browser Agent、Coder Agent、Reporter Agent（可扩展）

协作方式：通过 Flow 工作流定义角色、工具权限、执行顺序、结果传递。支持动态分配代理，提高效率。

## 5\. 执行循环（Agent Loop）

基于 ReAct / CodeAct 风格的迭代循环：

  1. 分析任务：理解用户输入
  2. 规划：分解子任务、生成步骤计划
  3. 执行：调用工具（写代码执行、浏览网页等）
  4. 观察：获取工具输出、评估结果
  5. 迭代/验证：不满意则反馈重试或调整计划
  6. 最终输出：汇总结果（报告、文件等）

支持实时反馈：用户可查看代理思考过程、进度、生成文件。

## 6\. 工具集成与行动机制

采用 **CodeAct** 风格：代理生成可执行 Python 代码来交互环境。

核心工具：

  * 浏览器自动化（BrowserUseTool，基于 Playwright 等）
  * 代码执行器（PythonExecute）
  * Web 搜索（GoogleSearch）
  * 文件读写、规划工具等

工具统一 BaseTool 接口，便于扩展。

## 7\. 优势与扩展

  * 开源免费、本地运行、无云依赖（支持 Ollama）
  * 实时可视化进度、错误重试机制
  * 扩展项目：OpenManus-RL（强化学习优化）
  * 局限：早期版本稳定性不如原 Manus，但社区迭代迅速

参考日期：2025 年底，信息基于最新社区与仓库更新。

如需部署或二次开发，直接 clone 仓库配置 config.toml 即可运行！
