GLSL layout 用法 | GLSL 示例 | C/C++ 类比 | 本质含义（给 C++ 程序员）  
---|---|---|---  
layout(location = N) | layout(location=0) in vec3 aPos; | struct 成员 offset / 函数参数序号 | 显式指定接口位置，等价“ABI 固定”  
layout(binding = N) | layout(binding=1) uniform sampler2D tex; | 数组索引 / 资源句柄槽位 | 显式指定资源绑定点  
layout(set = X, binding = Y) | layout(set=0,binding=0) uniform UBO {...} | struct namespace + index | Vulkan descriptor set / 分组资源表  
layout(std140) | layout(std140) uniform Block {...} | ABI 对齐规则（16B） | 类似固定 padding 的 C struct  
layout(std430) | layout(std430) buffer SSBO {...} | #pragma pack / 紧凑 struct | 更接近 C struct 的内存布局  
layout(offset = N) | layout(offset=64) uniform float x; | offsetof(struct, member) | 手动指定字段内存偏移  
layout(rgba32f) | layout(rgba32f) uniform image2D img; | struct Pixel { float r,g,b,a; } | 显式指定内存像素格式  
layout(local_size_x = 8) | layout(local_size_x=8) in; | thread block size | CUDA/OpenCL work-group 规模  
layout(row_major) | layout(row_major) uniform mat4 m; | 矩阵存储顺序 | 行优先 vs 列优先  
layout(early_fragment_tests) | layout(early_fragment_tests) in; | 编译期优化指令 | 强制提前深度/模板测试
