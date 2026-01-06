# 3 个月 Vulkan 学习路线（以通用计算为主，图形计算为辅）

基于 Windows 10/11 + NVIDIA GeForce GTX 1660 环境调整。路线聚焦 GPGPU（通用计算），次要覆盖图形。利用 C++、OpenCL、CUDA C、VSCode 和 CMake 基础。环境：LunarG Vulkan SDK 1.4+、Vulkan-Hpp、VMA、RenderDoc、NVIDIA Nsight。优先现代特性（Vulkan 1.3+）。

## 路线原则

  * **Compute 优先** ：前 1.5 个月 80% 时间用于 GPGPU，利用您的 CUDA/OpenCL 背景跳过并行基础。
  * **图形整合** ：后半引入渲染作为 Compute 的可视化输出（e.g., Compute 生成纹理后渲染）。
  * **优化** ：每周性能剖析（用 Tracy 或 Nsight），目标减少 CPU 开销。
  * **跨平台** ：从 Windows 开始，Month 3 测试 WSL2（Linux 子系统）。

## 详细路线

月份/周次 | 目标与关键主题 | 实践任务（每周目标，Windows 调整） | 推荐资源（2025 年更新）  
---|---|---|---  
**Month 1: 基础与通用计算核心**  
(Weeks 1-4: 构建 Compute 管道，映射 CUDA/OpenCL 概念) | 掌握 Vulkan 初始化、Compute Pipeline 和基本 Dispatch；缓冲区/内存管理；同步与多线程。理解 SPIR-V 着色器（从 GLSL 编写，类似 CUDA C）。 |  \- Week 1: 环境设置（安装 SDK + 驱动），VSCode + CMake 项目创建。Dispatch 简单 Compute Shader（向量加法，类似 CUDA kernel）。用 Nsight 检查 GPU 负载。  
\- Week 2: SSBO/Uniform Buffer 与 VMA 分配；主机-设备传输（staging buffers）。实现矩阵乘法，比较 Vulkan vs. CUDA 性能（Windows Task Manager 监控）。  
\- Week 3: 同步（栅栏、信号量、屏障）；多 Dispatch 链。构建 N-body 模拟（10k 粒子）。启用验证层调试。  
\- Week 4: 子组操作（subgroups）和共享内存优化。添加错误处理（验证层）。测试 GTX 1660 极限（e.g., 内存分配 <6GB）。  |  \- Vulkan Tutorial Compute 章节：基础 Dispatch。  
\- Udemy "GPU Computing in Vulkan"：从 VSCode 到 Compute Shader 项目。  
\- TheMaister 博客 "Compute-First Mindset"：针对 CUDA 背景的学习建议。  
\- NVIDIA Vulkan Developer 页面：GTX 1660 GPGPU 入门。   
**Month 2: 高级 Compute 与图形引入**  
(Weeks 5-8: 深化 GPGPU，桥接到图形管道) | 高级扩展（如绑定less 描述符、缓冲设备地址 BDA）；多队列/线程；图形基础（交换链、渲染通道，作为 Compute 输出可视化）。 |  \- Week 5: 绑定less 资源与描述符更新；Compute 子组扩展。实现图像处理（如 Gaussian Blur）。用 Nsight 优化内存访问。  
\- Week 6: 多阶段 Compute（e.g., FFT 或 ML 前向传播）；集成 Torch-Vulkan（AI 加速）。Windows DLL 路径配置。  
\- Week 7: 引入图形：交换链创建（GLFW for Windows 窗口），Compute 生成纹理后渲染（e.g., Mandelbulb 分形）。避免 RT 扩展。  
\- Week 8: 动态渲染（取代固定通道）；图形同步与 Compute 交互（e.g., 粒子模拟可视化）。测试 1080p 性能。  |  \- Sascha Willems GitHub Samples：高级 Compute 示例。  
\- YouTube "GPU Accelerated Computing with Vulkan & Kompute"：跨厂商 GPGPU 优化。  
\- VkGuide.dev：现代 Compute 与图形桥接。  
\- Reddit r/vulkan 讨论：Vulkan vs. OpenCL for GPGPU on GTX 1660。   
**Month 3: 项目整合、优化与扩展**  
(Weeks 9-12: 端到端应用，性能调优) | 构建完整项目；性能优化（occupancy、内存一致性）；跨领域扩展（如 AI/ML 或嵌入式）；图形增强 Compute 项目。 |  \- Week 9: 项目1 - GPU 蒙特卡洛模拟（Compute 核心），添加 ImGui UI（Windows 兼容）。  
\- Week 10: 项目2 - 简单渲染器（图形次要）：Compute 生成场景后渲染（e.g., 射线追踪混合，软件 fallback）。  
\- Week 11: 优化：减少绘制调用，基准测试（FLOPS vs. CUDA）。用 Nsight Systems 剖析 GTX 1660 瓶颈。  
\- Week 12: 扩展：SYCL/Vulkan 融合（AI）；WSL2 测试 Linux 兼容。开源贡献或社区反馈。  |  \- "Vulkan 3D Graphics Rendering Cookbook"：项目案例。  
\- Modular 博客：OpenCL/CUDA 替代方案，Vulkan portability on Windows。  
\- Khronos Vulkan.org/learn：2025 路线图与扩展。  
\- Hacker News "Learn CUDA to Professional Level"：类似 GPGPU 灵感。   
  
## 额外 Windows + GTX 1660 建议

  * **安装顺序** ：1. NVIDIA 驱动；2. Vulkan SDK；3. VSCode 扩展（C/C++、CMake）；4. 库如 GLFW、GLM（via vcpkg or CMake FetchContent）。
  * **常见问题** ：如果 Dispatch 失败，检查驱动版本（用 GPU-Z）。GTX 1660 热管理：用 MSI Afterburner 监控温度（<80°C）。
  * **基准** ：用 Geekbench Vulkan 测试初始性能（~22,000 分），追踪进步。
  * **社区** ：NVIDIA Forums 的 Vulkan 板块；Discord #vulkan for Windows 调试。

数据截至 2025 年 12 月 18 日。更多详情请参考 [Khronos Vulkan 官网](https://www.khronos.org/vulkan/) 或 NVIDIA 开发者页面。
