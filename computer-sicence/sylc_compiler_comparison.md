# SYCL 编译器 / 实现对比总览表（含硬件矩阵）

本页已更新：hipSYCL / OpenSYCL 的主线项目已合并并以 **AdaptiveCpp** 名义维护。表格反映这一变更，并保留其他实现的对比信息（截止 2025 年底）。

## 对比总览表

实现 / 编译器 | Windows 支持 | Linux 支持 | 支持硬件后端 | 标准支持度 | 生态成熟度 | 推荐场景  
---|---|---|---|---|---|---  
**DPC++ (oneAPI)** | ⭐⭐⭐⭐ 强 | ⭐⭐⭐⭐⭐ 非常强 | Intel CPU / Intel GPU；部分 NVIDIA / AMD（插件） | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 工业级、商用部署、Intel 平台优化  
**AdaptiveCpp (含原 hipSYCL / OpenSYCL)** | ⭐⭐⭐ 中等（Windows 支持逐步增强） | ⭐⭐⭐⭐⭐ 非常强（社区主力） | Intel / AMD / NVIDIA GPU；CPU (OpenMP)；通过 OpenCL/Vulkan 可覆盖 Arm Mali | ⭐⭐⭐⭐ | ⭐⭐⭐⭐（活跃开发 / 社区驱动） | 多厂商 GPU、跨平台部署、灵活后端选择（推荐首选）  
**ComputeCpp** | ⭐⭐ 中等 | ⭐⭐ 中等 | CPU / OpenCL GPU | ⭐⭐（旧标准） | ⭐⭐ 已减弱 | 遗留项目支持  
**triSYCL** | ⭐⭐ 测试为主 | ⭐⭐ 测试为主 | 部分 CPU / 研究平台 | ⭐⭐⭐（学术） | ⭐⭐ 小众 | 研究 / 原型验证  
**neoSYCL** | ❓ 依硬件而异 | ⭐⭐ 有限 | 特定加速器 / 定制硬件 | ⭐⭐ | ⭐⭐ | 特定硬件定制适配  
**SimSYCL** | ⭐⭐⭐ | ⭐⭐⭐ | CPU 模拟（用于功能测试） | ⭐⭐⭐⭐ | ⭐⭐ | 正确性模拟 / 学习  
  
注：AdaptiveCpp 为 hipSYCL / OpenSYCL 的合并/重命名主线；星级与成熟度为相对评估，基于 2025 年公开资料与社区活跃度。

## 支持硬件矩阵（汇总视图）

实现 | Intel CPU | Intel GPU | NVIDIA GPU | AMD GPU | FPGA | Arm Mali  
---|---|---|---|---|---|---  
**DPC++** | ✓✓✓ | ✓✓✓ | 插件（有限） | 插件（有限） | ✓✓✓（Intel FPGA / oneAPI） | ⭐（理论通过 OpenCL，但不推荐）  
**AdaptiveCpp** | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ | 在路上 | ⭐⭐（通过 OpenCL / Vulkan 路线；Linux 上有案例）  
**ComputeCpp** | ✓✓ | ✓（OpenCL） | 有限 | 有限 | 可行 | ⭐⭐⭐（OpenCL 后端，常见友好）  
**triSYCL** | ✓ | 部分 | ✗ | ✗ | 研究中 | ⭐（学术实验）  
**neoSYCL** | 有限 | 有限 | 限定环境 | 限定环境 | 特定支持 | ❓（视硬件而定）  
**SimSYCL** | CPU 模拟 | CPU 模拟 | CPU 模拟 | CPU 模拟 | ✗ | ✗  
  
提示：Arm Mali 的支持受驱动（OpenCL / Vulkan）影响很大；以 Linux + AArch64 的 open‑source 驱动（例如 Panfrost）为最佳实验平台。

如果你需要，我可以把这个 HTML 导出为 .html 文件供你下载，或把表格转换为 Markdown/CSV/Excel 格式。
