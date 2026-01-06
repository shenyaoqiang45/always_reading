# RK3588 + Mali GPU 上 USM 不可用分析

## 1\. 系统层次关系

  * **内核驱动（Kernel Driver）** ：`mali.ko`，管理硬件资源、GPU 内存和上下文，已成功加载。
  * **Vendor Driver（厂商驱动 / OpenCL Runtime）** ：ARM 提供的 Mali OpenCL runtime，负责将 OpenCL kernel 调度到 GPU。
  * **ICD Loader / libOpenCL.so** ：统一接口库，应用程序（SYCL / AdaptiveCpp）通过它调用 vendor driver。
  * **应用层（SYCL / AdaptiveCpp）** ：调用 USM 或 buffer 接口进行 GPU 计算。

## 2\. USM 不可用的原因

  * 内核驱动限制：虽然 `mali.ko` 加载成功，但不支持 USM 所需的内存管理特性（如 unified memory、large page allocation、memory group manager）。
  * Vendor driver 限制：Mali OpenCL runtime 对 ARM Mali GPU（尤其是 Valhall 架构 G610）尚未实现完整 USM 支持，只能使用 buffer + accessor。
  * AdaptiveCpp / SYCL 依赖：USM 功能要求 OpenCL runtime 支持统一内存（Shared / Host / Device），当前 runtime 不支持，因此 `malloc_shared` 调用会失败。
  * 硬件特性：部分嵌入式 GPU（如 Mali G610）受限于内存架构和驱动设计，不提供全功能统一共享内存。

## 3\. 结论

  * 在 RK3588 + Mali G610 平台上，GPU 驱动和 OpenCL runtime 已加载，可用 buffer + accessor 进行 SYCL / AdaptiveCpp 编程。
  * USM（`malloc_shared` / `malloc_device` 等）不可用，因为 vendor driver 和内核驱动都不支持该特性。
  * 解决办法： 
    * 使用 buffer + accessor 替代 USM
    * 或换用支持完整 USM 的 GPU（如 NVIDIA / AMD / Intel）
