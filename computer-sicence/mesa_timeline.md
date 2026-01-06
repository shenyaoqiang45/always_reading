# Mesa 项目（Mesa 3D Graphics Library）发展时间线

Mesa项目是一个开源的3D图形库，主要提供对OpenGL、Vulkan、OpenGL ES等图形API的实现。它是Linux系统中最重要的开源图形驱动组件之一，支持多种GPU硬件（如Intel、AMD、NVIDIA的开源驱动），并从最初的软件渲染发展到现代硬件加速。 

## 主要发展时间线

  * **1993年8月** ：项目创始人Brian Paul开始业余开发Mesa，作为一个简单的OpenGL-like 3D图形库，最初受VOGL（IRIS GL子集仿真库）启发。当时项目无正式名称，仅为个人兴趣。
  * **1994年11月** ：Brian Paul联系SGI（OpenGL规范制定者）获得许可，允许公开分发（但不能在名称中使用“Open”或“GL”）。
  * **1995年2月** ：Mesa 1.0正式在互联网上发布。迅速受到欢迎，用户开始贡献补丁和新功能，项目名称“Mesa”由此确立。
  * **1997年3月** ：Mesa 2.2发布，支持3dfx Voodoo显卡（通过Glide库）。
  * **1999年** ：Mesa成为XFree86中DRI（Direct Rendering Infrastructure）项目的核心组件，支持多种硬件加速驱动（如3dfx、3Dlabs、Intel、Matrox、ATI）。
  * **2001年10月** ：Mesa 4.0发布，实现OpenGL 1.3规范。
  * **2001年11月** ：Brian Paul联合创办Tungsten Graphics公司，专注于Mesa和相关图形开发。
  * **2002年11月** ：Mesa 5.0发布，实现OpenGL 1.4规范。
  * **2003年1月** ：Mesa 6.0发布，实现OpenGL 1.5规范，并支持GL_ARB_vertex_program和GL_ARB_fragment_program扩展。
  * **2007年6月** ：Mesa 7.0发布，实现OpenGL 2.1规范和OpenGL Shading Language（GLSL）。
  * **2008年** ：Tungsten Graphics员工开发Gallium3D（新的GPU抽象层），极大简化驱动开发。Tungsten Graphics被VMware收购。Gallium3D于2009年起正式集成到Mesa中，目前用于多数现代驱动（如Nouveau、Intel Iris、AMD Radeon）。
  * **2015-2016年** ：开始支持Vulkan API，Intel驱动率先实现初始支持。
  * **2016年7月** ：Mesa 12.0发布，支持OpenGL 4.3和Intel GPU的Vulkan初始支持。
  * **2018年** ：通过Google Summer of Code项目启动VirGL（虚拟机软件驱动）的Vulkan支持。
  * **2023年** ：Mesa 23.x系列引入更多现代特性，如AMD RADV驱动支持光线追踪（Ray Tracing）、Apple Asahi驱动支持OpenGL 3.1等。
  * **至今（2025年）** ：Mesa持续更新，目前最新版本为25.x系列（年份-based版本方案从2017年起采用），支持OpenGL 4.6、Vulkan 1.3+等高级规范，并通过Zink驱动实现OpenGL over Vulkan。项目托管于freedesktop.org，由全球社区和厂商（如Intel、AMD、Valve）共同维护。

Mesa从一个简单的软件渲染库，逐步演变为Linux图形栈的核心，填补了早期OpenGL硬件支持的空白，并推动了开源图形驱动的发展。它在Linux桌面、游戏（通过Wine/Proton）、嵌入式系统和虚拟化中广泛应用。
