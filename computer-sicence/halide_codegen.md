# Halide DSL - 代码生成与优化

## Halide 是 DSL 吗？

✅ 是的。

Halide 是专为 **图像处理与数值计算** 设计的 DSL，它的理念是：

### 核心设计理念

  * **算法层（Algorithm）** ：只描述计算逻辑，比如卷积、模糊、锐化
  * **调度层（Schedule）** ：描述如何执行，比如并行化、向量化、分块、存储位置

### 优势

这样的设计使得：

  * 算法可以保持数学纯净
  * 调度部分可以单独针对硬件优化
  * 同一算法可以轻松适配不同的硬件平台（CPU、GPU、移动设备等）
  * 性能优化与算法逻辑解耦

## Halide 代码生成管道（CPU & GPU）

Halide 统一的代码生成流程，支持 CPU 和 GPU 目标：
    
    
    算法定义（Halide DSL）
       ↓
    调度搜索 + 代价模型（Cost Model）
       ↓
    Halide IR 优化（Loop nest / Vectorize / Parallelize）
       ↓
       ├─── CPU 路径 ────────────────┬─── GPU 路径 ──────────────┐
       ↓                              ↓
    LLVM IR 生成                 Lower to GPU Kernel IR
    （调用 LLVM API）            （Halide 内部 GPUIR）
       ↓                              ↓
    机器码                        生成 OpenCL C 源码字符串
    （x86 / ARM / NEON）         （kernel）
                                      ↓
                                 OpenCL Runtime API 编译
                                 （clBuildProgram）
                                      ↓
                                 GPU 二进制代码
                

### 共同阶段

  * **算法定义** ：用户用 Halide DSL 描述计算
  * **调度搜索** ：根据代价模型找到最优的执行策略
  * **Halide IR 优化** ： 
    * Loop nest：嵌套循环结构优化
    * Vectorize：向量化
    * Parallelize：并行化

### CPU 特定阶段

  * **LLVM IR 生成** ：将 Halide IR 转换为 LLVM 中间表示，调用 LLVM API
  * **机器码生成** ：针对不同架构（x86、ARM、NEON等）生成优化后的机器码

### GPU 特定阶段

  * **Lower to GPU Kernel IR** ： 
    * 将 Halide IR 转化为 GPU 友好的内部中间表示
    * 进行 GPU 特定的优化（分线程块、线程、内存层级等）
  * **生成 OpenCL C 源码** ： 
    * 从 GPU Kernel IR 生成 OpenCL C 源代码字符串
    * 包含 kernel 函数和内存访问模式
  * **OpenCL 编译运行** ： 
    * 通过 OpenCL Runtime API 调用 `clBuildProgram` 编译源码
    * 获得 GPU 二进制代码
    * 在运行时加载并执行

## Halide 算法优化策略

Halide 的算法优化思想融合了 **编译优化理论** 和 **自动调度（auto-scheduler）算法** ，主要包括：

### 主要优化策略对比

优化策略 | 理论依据 | 实现效果  
---|---|---  
**Loop Tiling** （循环分块） | 空间/时间局部性 | 减少 cache miss  
**Vectorization** （向量化） | SIMD 理论 | 提升并行吞吐率  
**Parallelization** （多线程） | Fork-Join Model | CPU 多核利用  
**Fusing/Splitting** | DAG 节点融合 | 减少中间内存  
**Storage Folding** | 数据重用 | 减少带宽压力  
**Auto-scheduler** | 代价模型 + 搜索 | 自动找到最优调度策略  
  
### 代价模型（Cost Model）

Halide 的 auto-scheduler 基于一个 **代价函数模型** ：

**代价函数：**

`C(S) = α · memory_access(S) + β · compute(S) + γ · parallel_overhead(S)`

其中：

  * `memory_access(S)`：内存访问成本（受缓存局部性影响）
  * `compute(S)`：计算成本（指令数、向量化程度等）
  * `parallel_overhead(S)`：并行化开销（线程同步、通信等）
  * `α, β, γ`：各项的权重系数（根据硬件特性调整）

### 自动调度搜索

通过搜索找到最优的调度策略：
    
    
    S* = argmin(C(S))   // 找到使代价函数最小的调度 S*
    
    搜索空间包括：
      - Loop order（循环顺序）
      - Tiling factors（分块大小）
      - Parallelization level（并行化粒度）
      - Vectorization width（向量宽度）
      - Storage location（存储位置）
      - Fusion/Split decisions（融合/分割决策）
                

### 不同自动调度库的优化方向

  * **Mullapudi 2016** ：基于随机森林学习历史性能数据，直接预测最优调度
  * **Li 2018** ：改进的特征工程，更好的泛化到新的计算模式
  * **Adams 2019** ：使用深度学习代价模型，更精准的性能预测，搜索策略更高效

## RK3588 实战经验 (1) - GPU自动调度器（Adams 2019）

Adams 2019 是 Halide 中最先进的自动调度器，位于 Halide 源码路径：`src/Autoscheduler/Adams2019`

### 调度策略：两个代价模型

  * **CPU Cost Model**
    * 基于深度神经网络学习 CPU 性能特征
    * 输入特征：loop nest 结构、内存访问模式、并行化策略等
    * 输出：执行时间预测
    * RK3588 CPU 架构：4×A76 + 4×A55 混合核心，模型需要适配大小核差异
  * **GPU Cost Model（实验性）**
    * 训练数据主要来自 NVIDIA GPU（CUDA 优化的数据）
    * RK3588 搭载 Mali-G610 GPU，与 NVIDIA 架构差异较大
    * 泛化性受限：OpenCL 与 CUDA 的计算模型、内存层级、warp/workgroup 调度机制不同
    * 建议在 RK3588 实际部署时，使用 CPU model 或针对 Mali-G610 重新训练 GPU model

## RK3588 实战经验 (2) - GPU手动调度 malloc_consolidate() 崩溃问题

### 错误现象

在 ARM Mali GPU 上使用 Halide 手动调度进行 GPU 计算时，程序崩溃并输出：
    
    
    malloc_consolidate(): invalid chunk size
    Aborted (core dumped)
                

### 根本原因

这个错误 **不是 Halide 算法本身崩溃** ，而是：

  * **OpenCL runtime（libmali）** 在 Halide AOT（Ahead-of-Time）编译模式下释放内存时出现问题
  * 具体表现为 **二次释放（double free）** ：内存被释放两次，导致堆损坏
  * 这是 **Halide OpenCL runtime 在 ARM Mali 上的已知 bug**
  * 在 libHalide.so < v17 版本中最为常见

### 问题分析

问题环节 | 详细说明  
---|---  
**发生阶段** | 程序结束或 GPU buffer 释放时（析构函数）  
**涉及组件** | libmali（ARM Mali OpenCL driver）、libHalide.so OpenCL backend  
**关键因素** | AOT 编译时的内存管理逻辑与 libmali 的释放机制不兼容  
**触发条件** | 手动调度 GPU 任务 + 大尺寸 buffer（>32MB）+ 频繁分配/释放  
  
## RK3588 实战经验 (3) - CPU自动调度 machine_params 最优配置计算

基于 RK3588 的硬件规格，为 4 个 A76 大核计算最优的 `machine_params` 设置。

### RK3588 A76 大核规格

硬件参数 | 规格  
---|---  
**CPU 型号** | ARM Cortex-A76（4 核）  
**主频** | 2.4 GHz  
**L1 缓存** | 32KB (Instruction) + 32KB (Data) = 64KB / 核  
**L2 缓存** | 1MB / 核（4 核共 4MB）  
**L3 缓存** | 4MB（系统级共享，所有核心共用）  
**总缓存容量** | L2 (4MB) + L3 (4MB) = **8MB**  
  
### machine_params 三参数计算

  1. **cores = 4**
     * 使用 4 个 A76 大核
     * 通过 Linux cpuset 或 taskset 隔离小核
  2. **memory_size 计算**
     * 代价模型评估数据在缓存中的重用性
     * 推荐值：**L2 + L3 缓存总和 = 8MB = 8388608 Bytes**
     * 保守策略：使用 L3 容量 4MB = 4194304 Bytes（避免 L2 竞争）
     * 激进策略：使用 8MB（允许充分利用 L2 缓存）
  3. **compute_capability 计算**
     * 相对基准处理器的性能系数
     * A76 @ 2.4GHz 的计算能力通常为基准的 **40-50 倍**
     * 更精确计算：基于 A76 指令集和 SIMD 能力 
       * A76 支持 NEON（128-bit SIMD），每周期可执行 2 条 FP32 指令
       * 相对基准单线程处理器，性能系数约 **45-50**

### 推荐配置方案

配置方案 | machine_params | 适用场景  
---|---|---  
**保守方案** | `4,4194304,45` | 只考虑 L3 缓存，避免 L2 竞争，适合复杂算法  
**平衡方案（推荐）** | `4,8388608,48` | **最优选择** ：充分利用 L2+L3，性能预测最准确  
**激进方案** | `4,8388608,50` | 充分利用大核性能，追求最大吞吐量  
**原始参考** | `4,16777216,40` | 原始 16MB 设置偏大（超出实际缓存），compute_capability 偏低  
  
### 详细分析

**为何推荐 4,8388608,48？**

  * **cores=4** ：只用 A76 大核，避免小核的不规则性
  * **memory_size=8388608** （8MB）： 
    * 等于 L2 + L3 总容量，代价模型会优化数据重用
    * 避免频繁访问主内存（DDR，延迟 ~100ns）
    * 充分利用 A76 的缓存预取能力
  * **compute_capability=48** ： 
    * A76 @ 2.4GHz 的相对性能系数
    * 基于：双发射 NEON FP32（每周期 2 ops）× 2.4GHz × SIMD 宽度
    * 相对基准单线程处理器的性能倍数约 48 倍
