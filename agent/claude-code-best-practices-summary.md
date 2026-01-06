# 《Claude Code: Best practices for agentic coding》文章总结

这篇文章由 Anthropic 的 Boris Cherny 主笔，基于内部团队和外部用户经验，分享了使用 Claude Code（一个终端代理式编码工具）的有效模式。Claude Code 设计为低层级、无意见化的工具，提供灵活性，但需要用户开发自己的最佳实践。文章强调实验不同方式，并链接到详细文档。

## 1\. 自定义你的设置

优化 Claude Code 的上下文收集，以提升性能和安全性。

  * **创建 CLAUDE.md 文件** ：Claude 会自动加载此文件作为提示上下文。用于记录常用 bash 命令、核心文件、代码风格、测试指南、仓库规范等。示例包括 bash 命令列表、风格偏好（如使用 ES 模块）。可放置在仓库根目录、子目录、父目录或用户主目录。推荐提交到 git 共享，或用 CLAUDE.local.md 私有。运行 /init 命令可自动生成。
  * **优化 CLAUDE.md** ：像提示工程一样迭代它，可手动添加或用 # 键让 Claude 自动融入。Anthropic 常用提示改进器，并添加 "IMPORTANT" 等强调。
  * **管理允许工具列表** ：默认保守权限。可通过会话选择“始终允许”、/tools 命令、手动编辑 settings.json 或 CLI 标志自定义（如允许文件编辑或 git commit）。
  * **安装 gh CLI** ：便于 Claude 与 GitHub 交互（如创建 PR）。

## 2\. 为 Claude 提供更多工具

扩展 Claude 的能力。

  * **结合 bash 工具** ：Claude 继承 shell 环境，但需告知自定义工具（提供示例、--help 或记录在 CLAUDE.md）。
  * **使用 MCP（Model Context Protocol）** ：Claude 可连接 MCP 服务器获取复杂工具（如 Puppeteer 截图、Sentry）。通过项目/全局配置或 .mcp.json 添加。
  * **自定义斜杠命令** ：在 .claude/commands 目录存 Markdown 提示模板，支持 $ARGUMENTS 参数传递。示例：自动修复 GitHub 问题的命令，包括查看问题、实现更改、测试、创建 PR 等。可共享到团队。

## 3\. 尝试常见工作流

Claude Code 不强制流程，以下是社区验证的有效模式。

  * **探索、规划、编码、提交** ：先让 Claude 阅读文件/图像/URL（禁止立即写代码），制定计划（用 "think hard" 等触发深入思考），然后实现并提交。适用于复杂任务，可用子代理验证细节。
  * **编写测试、提交；编码、迭代、提交** （TDD 增强版）：先写测试（明确 TDD 以避免 mock），确认失败后提交；然后写代码迭代直到通过测试（可用子代理防过拟合）；最后提交代码。Claude 在有明确目标（如测试）时表现最佳。
  * **编写代码、截图结果、迭代** ：提供截图工具和视觉 mock，让 Claude 实现、截图、迭代直到匹配。迭代 2-3 次可显著提升质量。
  * **安全 YOLO 模式** ：用 --dangerously-skip-permissions 绕过权限，适合修复 lint 或生成样板。但风险高，建议在无网容器中运行。
  * **代码库问答** ：直接问问题（如“日志如何工作？”），Claude 会代理搜索代码库。Anthropic 用此加速新手入职。
  * **与 git/GitHub 交互** ：处理历史搜索、提交消息、rebase 冲突、创建 PR、解决审查评论等。

## 4\. 优化工作流通用建议

  * **指令更具体** ：详细描述优于模糊（如指定边缘案例、参考文件）。
  * **提供图像/URL/文件** ：粘贴截图、拖放或路径引用，提升视觉任务质量。
  * **早期纠错** ：要求先计划、用 Escape 中断、编辑历史。
  * **保持上下文专注** ：用 /clear 重置。
  * **使用检查列表** ：多步骤任务让 Claude 生成 Markdown 清单并逐一勾选。
  * **传入数据** ：复制粘贴、管道、文件读取或工具拉取。

## 5\. 无头模式自动化

用 -p 标志在 CI/钩子中运行，--output-format stream-json 输出 JSON。示例：问题分类、作为主观 linter。

## 6\. 多 Claude 并行工作流

  * 一个写代码、另一个审查。
  * 多仓库检出或 git worktrees 并行任务。
  * 无头模式扇出/管道化大任务。

文章结尾鼓励用户分享自己的实践，并指出这些模式源于真实使用，可作为起点实验。Claude 在有验证机制（如测试、截图）时质量提升显著，迭代是关键。

总结基于 Anthropic 官方博客《Claude Code: Best practices for agentic coding》  
生成时间：2026年1月3日
