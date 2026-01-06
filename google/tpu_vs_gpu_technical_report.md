# TPU 与 NVIDIA GPU（CUDA）对比与 Systolic Array 运行机制

**作者：** （自动生成） **目的：** 对比 TPU 与 GPU 的设计哲学、编译链与硬件执行机制，并通过 Systolic Array 的逐周期示例（2×2）解释脉动阵列如何完成矩阵乘法。

## 1\. 概要

本报告总结如下要点：

  * TPU 与 GPU 都通过大量并行硬件单元实现矩阵与标量运算加速，但设计哲学、可编程性与执行模型不同。
  * TPU 编译链把高层算子逐步下沉（TensorFlow → XLA-HLO → LLVM IR → TPU HLO → TPU 指令），大量算子最终被合成为 MAC（multiply–accumulate）风格的阵列操作。
  * Systolic Array 是一种时序（clocked）数据流阵列：每个 MAC 单元执行标量乘加，数据沿固定方向脉动流动，矩阵乘法由大量标量 MAC 的逐周期协作完成。
  * "tile" 对应的就是脉动阵列（Systolic Array）的物理计算块大小，TPU 会把整个矩阵分成一块块 tile，每个 tile 在阵列上以时序脉冲方式流入、计算、流出。

## 2\. Google TPU 与 NVIDIA GPU（CUDA）对比

对比维度| Google TPU| NVIDIA GPU (CUDA)  
---|---|---  
设计目标| 专用深度学习矩阵运算加速（高吞吐、低内存带宽需求）| 通用并行计算（图形渲染、AI、科学计算等）  
硬件单元| Systolic Array（大规模 MAC 阵列，如 128×128）| 大量 CUDA 核心 + SM（调度/缓存/特殊单元）  
执行模型| 静态编译调度、fused computation、流水化数据流| 动态 kernel 调度、线程块/warp 并发执行  
数据流与内存| Tile 化、在片上 SRAM 重用、DMA 到 HBM| 层级缓存（L1/L2/Shared/Global）、较频繁的全局内存访问  
可编程性| 较窄但高效 —— 由 XLA 编译并下沉成矩阵指令| 高度可编程（CUDA C++/PTX）  
适合的算子| 矩阵乘法、卷积、transformer dot-product 等线性代数密集型| 广泛（图形、物理、AI、数值计算）  
  
## 3\. TPU 编译链条（从高层到硬件）

层级 | 说明 | 是否仍保留复杂操作  
---|---|---  
**Python + TensorFlow/Keras/JAX** | 用户使用 Python 编写高层神经网络模型，调用 TensorFlow、Keras 或 JAX API 定义计算图 | ✅ 有复杂算子（卷积、激活、池化等）  
**XLA HLO** | XLA 编译器将 Python 代码转换为标准化的中间表示 HLO，使用 HLO 指令集（基于 MLIR 标准） | ⚙️ 主要剩线性代数运算（矩阵乘法、加法、reshape、broadcast等）  
**LLVM IR** | 某些优化路径下转换为 LLVM 中间表示，支持标准 LLVM 优化 passes | ⚙️ 多为乘法、加法、访存等标量/向量算术指令  
**TPU HLO / TPU IR** | 专用的 TPU 指令集，针对 Systolic Array 硬件优化，支持 bfloat16、int8 等数据类型 | ⚙️ 乘加为主，合并为大型矩阵运算块  
**TPU 微码 / 硬件指令流** | 最终转换为 TPU 芯片可执行的微码，控制 DMA、阵列调度和数据流 | ✅ 几乎只剩 乘法+加法（MAC指令）  
  
### 算子执行模式对比

层级 | 是否"一算子一执行" | 说明  
---|---|---  
**TensorFlow算子层（TF Graph）** | ❌ 否 | 会被融合、简化（如卷积+激活+加偏置）  
**XLA HLO 层** | ⚙️ 部分是 | HLO op 通常代表一个"逻辑算子"（如dot_general、add、relu）  
**TPU编译后（TPU Executable）** | ⚙️ 由编译器融合多个HLO为一个"computation" | 例如多个 add/relu/reshape 会融合进一次矩阵乘法执行块  
**硬件执行层** | ✅ 是"编译好的执行段"顺序执行 | 每个段（program fragment）都是一个有序、预编排好的指令流  
  
编程语言：主要使用 Python（TensorFlow 2.x, JAX）；标准：XLA HLO 基于 MLIR（Multi-Level IR）标准，支持 OpenXLA 生态。实际实现随 TPU 版本（v2/v3/v4/v5）略有差异，但编译流程保持一致。

## 4\. TPU 硬件执行机制（高层视角）

执行由三部分协同完成：

  * **Host（或 runtime）** ：负责调度、加载执行单元、传递参数和触发 DMA。
  * **On-chip memory / Buffer（SRAM）** ：存放 tile 数据、部分和（partial sums）、中间结果以减少对 HBM 的访问。
  * **Systolic Array** ：时序阵列做实际的乘加运算。

执行流程（简化）：Host 下发 fused computation → DMA 将 tile 拉入 on-chip SRAM → 控制器按固定时序将 tile 的 A 与 B 列/行注入阵列 → 阵列进行多拍累加 → 结果写回 SRAM/HBM → Host 发起下一个 fused computation。

## 5\. Systolic Array（脉动阵列）运行机制要点

  * **每个 MAC 是标量运算单元** ：执行 P_out = P_in + A × B。
  * **数据以时钟脉动流动** ：A 从左到右，B 从上到下，部分和沿固定路径累积。
  * **时序展开（pipeline）** ：阵列需要若干时钟来“填充”（ramp-up）与“排空”（drain），但一旦 pipeline 满载，吞吐接近每拍输出。
  * **Tile 化与数据重用** ：编译器按阵列大小对矩阵分块，尽量在片上复用 A/B 数据，降低带宽压力。

## 5.1 按时钟周期看数据流动

### 矩阵相乘基础

矩阵相乘：

**C = A × B**

其中：

**A = [a₁₁ a₁₂; a₂₁ a₂₂], B = [b₁₁ b₁₂; b₂₁ b₂₂]**

目标是得到：

**Cᵢⱼ = Σₖ Aᵢₖ × Bₖⱼ**

时钟周期 | MAC11 输入 | MAC21 输入 | MAC12 输入 | MAC22 输入 | 说明  
---|---|---|---|---|---  
t=1 | A₁₁,B₁₁ |  |  |  | 阵列开始填充  
t=2 | A₁₂,B₂₁ | A₂₁,B₁₁ | A₁₁,B₁₂ |  | 第一行/列开始传播  
t=3 |  | A₂₂,B₂₁ | A₁₂,B₂₂ | A₂₁,B₁₂ | 全阵列激活，开始累加  
t=4 |  |  | A₂₂,B₂₂ | A₂₂,B₂₂ | 结果逐步输出  
t=5 |  |  |  | 输出最后结果 | pipeline 排空  
  
### 时序总结

填充阶段：需要 N + M - 1 = 3 个时钟周期（2+2−1），数据逐步注入阵列

排空阶段：再需要约 2 拍（让最后的数据流完并截断）

总时钟数 ≈ 5

💡 一旦阵列"pipeline"充满，后续连续矩阵块就能以"每时钟输出一个结果"的高吞吐率运行。

## 6\. 编译器优化与实际工程考虑

  * **算子融合（Fusion）** ：将连续的点乘/加/激活算子合并为单个 fused computation，减少调度与中间写回。
  * **Tile 大小选择** ：受阵列尺寸、内存带宽、数据类型（bfloat16/int8/FP16）影响。
  * **Buffer reuse** ：尽量在 SRAM 中复用数据，避免 HBM 往返造成带宽瓶颈。
  * **精度与数值稳定性** ：低精度（bfloat16/int8）提升吞吐同时需要注意累加精度与缩放策略。

## 7\. 结语与扩展阅读方向

TPU 的设计把硬件与编译器配合做到了极致：通过静态编译、tile 化和脉动阵列，把高层线性代数操作下沉为极高效的 MAC 流水线。GPU 则以灵活可编程和广泛适配性著称。两者各有侧重，常见的工程实践是根据目标负载选择最合适的硬件或混合使用。

如果你需要，我可以：

  * 将本 HTML 导出为可下载文件（或 PPT / PDF）。
  * 把示意图扩展成更细的每拍帧动画（逐帧 SVG 或 GIF）。
  * 把报告扩展为更学术的格式，添加参考文献和引用。

自动生成 · 若需定制或补充实例（如 128×128 tile 调度示例或 XLA HLO 具体样例），请告知。
