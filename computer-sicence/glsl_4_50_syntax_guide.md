# GLSL 4.50 规范 - OpenGL着色语言主要语法指南

**说明：** 本文档介绍GLSL 4.50版本的核心语法特性，适用于现代OpenGL开发。 

## 1\. 基本数据类型

### 标量类型

类型 | 描述 | 示例  
---|---|---  
`void` | 空类型，用于函数返回 | `void main() { }`  
`bool` | 布尔值 | `bool flag = true;`  
`int` | 有符号整数（32位） | `int count = 10;`  
`uint` | 无符号整数（32位） | `uint id = 5u;`  
`float` | 单精度浮点数（32位） | `float value = 1.5;`  
`double` | 双精度浮点数（64位） | `double precise = 1.5lf;`  
  
### 向量类型

**浮点向量：**
    
    
    vec2  v2;    // 2维向量
    vec3  v3;    // 3维向量 (最常用)
    vec4  v4;    // 4维向量

**整数向量：**
    
    
    ivec2  iv2;   // 有符号整数向量
    ivec3  iv3;
    ivec4  iv4;
    uvec2  uv2;   // 无符号整数向量
    uvec3  uv3;
    uvec4  uv4;

**双精度向量：**
    
    
    dvec2  dv2;
    dvec3  dv3;
    dvec4  dv4;

**布尔向量：**
    
    
    bvec2  bv2;
    bvec3  bv3;
    bvec4  bv4;

### 矩阵类型

**浮点矩阵：**
    
    
    // 列主序矩阵（Column-Major）
    mat2   m2;      // 2x2矩阵
    mat3   m3;      // 3x3矩阵 (常用于法向量变换)
    mat4   m4;      // 4x4矩阵 (最常用)
    mat2x3 m23;     // 2列3行矩阵
    mat3x2 m32;     // 3列2行矩阵

GLSL矩阵采用列主序（Column-Major）存储，这与某些其他图形库（如某些数学库）不同。 

## 2\. 采样器类型（Sampler Types）

采样器类型 | 描述 | 用途  
---|---|---  
`sampler1D` | 1D纹理采样器 | 一维纹理查询  
`sampler2D` | 2D纹理采样器 | 二维纹理查询（最常用）  
`sampler3D` | 3D纹理采样器 | 三维体积纹理查询  
`samplerCube` | 立方体纹理采样器 | 环境贴图、天空盒  
`samplerCubeArray` | 立方体纹理数组采样器 | 多个立方体纹理  
`sampler1DArray` | 1D纹理数组采样器 | 多个1D纹理  
`sampler2DArray` | 2D纹理数组采样器 | 多个2D纹理  
`samplerBuffer` | 缓冲纹理采样器 | 访问缓冲对象数据  
`sampler2DMS` | 多重采样2D纹理采样器 | 多重采样抗锯齿纹理  
`samplerCubeShadow` | 立方体阴影采样器 | 立方体阴影贴图  
  
### 整数采样器

用于访问整数格式的纹理：
    
    
    isampler1D, isampler2D, isampler3D
    isamplerCube, isamplerBuffer
    isampler1DArray, isampler2DArray

### 无符号整数采样器

用于访问无符号整数格式的纹理：
    
    
    usampler1D, usampler2D, usampler3D
    usamplerCube, usamplerBuffer
    usampler1DArray, usampler2DArray

## 3\. 变量限定符（Qualifiers）

### 存储限定符

限定符 | 描述 | 示例  
---|---|---  
`const` | 编译时常量 | `const float PI = 3.14159;`  
`in` | 输入变量（vertex/fragment attribute） | `in vec3 position;`  
`out` | 输出变量 | `out vec4 FragColor;`  
`inout` | 既输入又输出的参数 | `void modifyVec(inout vec3 v) { }`  
`uniform` | 统一变量（CPU→GPU常量） | `uniform mat4 uModel;`  
`buffer` | 着色器存储缓冲对象 | `buffer { vec4 data[]; } buf;`  
  
### 精度限定符
    
    
    // 仅在片段着色器中使用
    precision highp float;      // 高精度浮点
    precision mediump float;    // 中精度浮点
    precision lowp float;       // 低精度浮点
    
    // 变量级别
    highp vec4 position;
    mediump vec3 normal;
    lowp vec4 color;

### 插值限定符
    
    
    // 在vertex→fragment传递中指定插值方式
    smooth in vec3 vertexColor;      // 平滑插值（默认）
    flat in int vertexID;            // 不插值
    noperspective in vec3 texCoord;  // 不透视插值

### 不变量限定符
    
    
    // 确保多个着色器间相同输入产生相同输出
    invariant gl_Position;
    invariant out vec3 vNormal;

## 4\. 内置变量

### 顶点着色器（Vertex Shader）
    
    
    // 输出变量（必需）
    out gl_PerVertex {
        vec4 gl_Position;       // 裁剪空间顶点位置
        float gl_PointSize;     // 点精灵大小
        float gl_ClipDistance[]; // 用户定义裁剪距离
        float gl_CullDistance[]; // 用户定义剔除距离
    };
    
    // 输入变量
    in int gl_VertexID;         // 顶点索引
    in int gl_InstanceID;       // 实例索引
    in int gl_BaseVertex;       // 基础顶点偏移
    in int gl_BaseInstance;     // 基础实例偏移
    in int gl_DrawID;           // 绘制命令索引

### 片段着色器（Fragment Shader）
    
    
    // 输入变量（由光栅化提供）
    in vec4 gl_FragCoord;       // 片段位置 (x, y, z, 1/w)
    in bool gl_FrontFacing;     // 是否面向前方
    in float gl_FragDepth;      // 片段深度（可写入）
    in vec2 gl_PointCoord;      // 点精灵坐标 [0, 1]
    in int gl_SampleID;         // 多重采样ID
    in vec2 gl_SamplePosition;  // 采样点位置
    in int gl_Layer;            // 几何着色器层数
    in int gl_ViewportIndex;    // 视口索引
    
    // 输出变量
    out vec4 FragColor;         // 最终片段颜色（声明名称可自定义）

## 5\. 运算符（Operators）

### 算术运算符
    
    
    vec3 a = vec3(1.0, 2.0, 3.0);
    vec3 b = vec3(4.0, 5.0, 6.0);
    
    // 逐元素运算
    vec3 add = a + b;           // 加法
    vec3 sub = a - b;           // 减法
    vec3 mul = a * b;           // 逐元素乘法
    vec3 div = a / b;           // 逐元素除法
    vec3 mod = mod(a, b);       // 逐元素模运算
    
    // 标量与向量
    vec3 scaled = a * 2.0;      // 缩放

### 关系与逻辑运算符
    
    
    // 关系运算符（返回bvec）
    bvec3 less = lessThan(a, b);           // <
    bvec3 greater = greaterThan(a, b);     // >
    bvec3 lessEq = lessThanEqual(a, b);    // <=
    bvec3 greaterEq = greaterThanEqual(a, b); // >=
    bvec3 eq = equal(a, b);                // ==
    bvec3 neq = notEqual(a, b);            // !=
    
    // 逻辑运算符
    bool result = any(bvec3(true, false, true));   // 或
    bool result = all(bvec3(true, true, true));    // 与
    bvec3 inverted = not(bvec3(true, false, true)); // 非

### 访问操作符
    
    
    vec4 color = vec4(1.0, 0.5, 0.2, 1.0);
    
    // 成分访问
    float x = color.x;          // color[0]
    float y = color.y;          // color[1]
    float z = color.z;          // color[2]
    float w = color.w;          // color[3]
    
    // RGB访问
    vec3 rgb = color.rgb;       // 获取rgb分量
    float r = color.r;
    
    // RGBA访问
    float a = color.a;          // 透明度
    
    // 灵活重排（Swizzle）
    vec3 bgr = color.bgr;       // 反向rgb
    vec4 rrrr = color.rrrr;     // 复制分量
    vec2 xy = color.xy;

## 6\. 函数

### 基本函数语法
    
    
    // 函数定义
    returnType functionName(type param1, type param2) {
        // 函数体
        return result;
    }
    
    // 示例
    float lerp(float a, float b, float t) {
        return a * (1.0 - t) + b * t;
    }
    
    // 调用
    float result = lerp(1.0, 5.0, 0.5);  // 返回 3.0

### 参数限定符
    
    
    // in - 输入参数（默认）
    void process(in vec3 input) { }
    
    // out - 输出参数
    void getData(out vec3 result) {
        result = vec3(1.0);
    }
    
    // inout - 输入输出参数
    void modify(inout vec3 value) {
        value *= 2.0;
    }

### 常用内置函数

#### 三角函数
    
    
    float angle = radians(45.0);
    float s = sin(angle);
    float c = cos(angle);
    float t = tan(angle);
    float a = asin(0.5);           // 反正弦
    float as = atan(y, x);         // 两参数反正切

#### 指数和对数函数
    
    
    float exp_val = exp(x);        // e^x
    float exp2_val = exp2(x);      // 2^x
    float log_val = log(x);        // ln(x)
    float log2_val = log2(x);      // log₂(x)
    float sqrt_val = sqrt(x);      // 平方根
    float inv_sqrt = inversesqrt(x); // 1/√x
    float pow_val = pow(x, y);     // x^y

#### 绝对值和符号函数
    
    
    float abs_val = abs(x);        // 绝对值
    float sign_val = sign(x);      // 符号(-1, 0, 1)

#### 最小值、最大值、夹紧
    
    
    float minVal = min(a, b);      // 最小值
    float maxVal = max(a, b);      // 最大值
    float clamped = clamp(x, minVal, maxVal); // 夹紧到范围
    float mixed = mix(a, b, t);    // 线性插值: a + t*(b-a)
    float stepped = step(edge, x);  // 阶跃函数

#### 向量函数
    
    
    vec3 v = vec3(1.0, 2.0, 3.0);
    vec3 n = normalize(v);         // 单位化向量
    float len = length(v);         // 向量长度
    float dist = distance(v1, v2); // 向量距离
    float dp = dot(v1, v2);        // 点积
    vec3 cp = cross(v1, v2);       // 叉积（3D向量）
    float reflected = reflect(i, n); // 反射向量
    vec3 refracted = refract(i, n, eta); // 折射向量

#### 矩阵函数
    
    
    mat4 m = mat4(1.0);            // 单位矩阵
    mat4 transpose_m = transpose(m); // 矩阵转置
    float det = determinant(m);    // 行列式
    mat4 inv_m = inverse(m);       // 矩阵求逆
    float outerProduct(vec2 u, vec3 v); // 外积

#### 纹理采样函数
    
    
    uniform sampler2D texture0;
    
    // 基础纹理采样
    vec4 color = texture(texture0, vec2(0.5, 0.5));
    
    // 带偏移的采样
    vec4 color = textureOffset(texture0, uv, ivec2(1, 0));
    
    // 带LOD的采样
    vec4 color = textureLod(texture0, uv, lod);
    
    // 投影采样
    vec4 color = textureProj(texture0, vec3(uv, w));
    
    // 纹理大小
    int width = textureSize(texture0, 0).x;

## 7\. 控制流语句

### 条件语句
    
    
    // if-else 语句
    if (condition) {
        // 真分支
    } else if (condition2) {
        // 另一条件
    } else {
        // 默认分支
    }
    
    // 三元运算符
    float result = condition ? valueA : valueB;

### 循环语句
    
    
    // for 循环
    for (int i = 0; i < 10; i++) {
        sum += data[i];
    }
    
    // while 循环
    int count = 0;
    while (count < maxCount) {
        count++;
    }
    
    // do-while 循环
    do {
        value = compute();
    } while (value < threshold);

### 跳转语句
    
    
    // break - 跳出循环
    for (int i = 0; i < 100; i++) {
        if (data[i] == target) break;
    }
    
    // continue - 进入下一迭代
    for (int i = 0; i < 10; i++) {
        if (skip[i]) continue;
        process(i);
    }
    
    // discard - 片段着色器中放弃该片段
    if (alpha < 0.5) discard;
    
    // return - 函数返回
    if (error) return;

## 8\. 完整着色器示例

### 顶点着色器
    
    
    #version 450 core
    
    // 输入顶点属性
    layout(location = 0) in vec3 position;
    layout(location = 1) in vec3 normal;
    layout(location = 2) in vec2 texCoord;
    
    // uniform 变量
    uniform mat4 uModel;
    uniform mat4 uView;
    uniform mat4 uProjection;
    
    // 输出到片段着色器
    out VS_OUT {
        vec3 fragPos;
        vec3 normal;
        vec2 texCoord;
    } vs_out;
    
    void main() {
        // 变换到世界空间
        vs_out.fragPos = vec3(uModel * vec4(position, 1.0));
        vs_out.normal = normalize(mat3(uModel) * normal);
        vs_out.texCoord = texCoord;
        
        // 变换到裁剪空间
        gl_Position = uProjection * uView * vec4(vs_out.fragPos, 1.0);
    }

### 片段着色器
    
    
    #version 450 core
    
    // 输入来自顶点着色器
    in VS_OUT {
        vec3 fragPos;
        vec3 normal;
        vec2 texCoord;
    } fs_in;
    
    // uniform 纹理和光源
    uniform sampler2D uDiffuseMap;
    uniform vec3 uLightPos;
    uniform vec3 uCameraPos;
    
    // 输出
    out vec4 FragColor;
    
    void main() {
        // 采样纹理
        vec4 texColor = texture(uDiffuseMap, fs_in.texCoord);
        
        // 计算光照（Phong模型）
        vec3 norm = normalize(fs_in.normal);
        vec3 lightDir = normalize(uLightPos - fs_in.fragPos);
        float diff = max(dot(norm, lightDir), 0.0);
        
        // 反光
        vec3 viewDir = normalize(uCameraPos - fs_in.fragPos);
        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
        
        // 组合颜色
        vec3 ambient = texColor.rgb * 0.2;
        vec3 diffuse = texColor.rgb * diff;
        vec3 specular = vec3(1.0) * spec;
        
        FragColor = vec4(ambient + diffuse + specular, texColor.a);
    }

## 9\. 高级特性

### 几何着色器（Geometry Shader）
    
    
    #version 450 core
    
    layout(triangles) in;                      // 输入类型
    layout(triangle_strip, max_vertices=3) out; // 输出类型和最大数量
    
    in VS_OUT {
        vec3 color;
    } gs_in[];
    
    out GS_OUT {
        vec3 color;
    } gs_out;
    
    void main() {
        for(int i = 0; i < gl_in.length(); i++) {
            gl_Position = gl_in[i].gl_Position;
            gs_out.color = gs_in[i].color;
            EmitVertex();
        }
        EndPrimitive();
    }

### 计算着色器（Compute Shader）
    
    
    #version 450 core
    
    layout(local_size_x = 8, local_size_y = 8) in;
    
    layout(binding = 0, rgba32f) uniform image2D imgOutput;
    
    void main() {
        ivec2 pixel = ivec2(gl_GlobalInvocationID.xy);
        
        vec4 color = vec4(0.0, 1.0, 0.5, 1.0);
        imageStore(imgOutput, pixel, color);
    }

### 曲面细分着色器（Tessellation Shaders）
    
    
    // Tessellation Control Shader
    #version 450 core
    
    layout(vertices = 3) out;
    
    void main() {
        if(gl_InvocationID == 0) {
            gl_TessLevelOuter[0] = 4.0;  // 外部细分级别
            gl_TessLevelOuter[1] = 4.0;
            gl_TessLevelOuter[2] = 4.0;
            gl_TessLevelInner[0] = 4.0;  // 内部细分级别
        }
        gl_out[gl_InvocationID].gl_Position = 
            gl_in[gl_InvocationID].gl_Position;
    }

### 接口块（Interface Blocks）
    
    
    // 顶点着色器中定义
    out VS_OUT {
        vec3 fragPos;
        vec3 normal;
        vec2 texCoord;
        flat int materialID;  // 不插值
    } vs_out;
    
    // 片段着色器中使用相同结构
    in VS_OUT {
        vec3 fragPos;
        vec3 normal;
        vec2 texCoord;
        flat int materialID;
    } fs_in;

### Uniform 块（Uniform Block）
    
    
    layout(std140) uniform MatricesBlock {
        mat4 projection;
        mat4 view;
        mat4 model;
    } matrices;
    
    layout(std140) uniform LightBlock {
        vec3 position;
        float intensity;
        vec3 color;
        float radius;
    } lights[4];

### Shader Storage Buffer Object（SSBO）
    
    
    layout(std430, binding = 0) buffer ParticleBuffer {
        vec4 particles[];  // 动态大小数组
    } ssbo;
    
    void main() {
        uint idx = gl_GlobalInvocationID.x;
        ssbo.particles[idx] = vec4(1.0);
    }

## 10\. 最佳实践和注意事项

### 性能优化建议

  * **避免分支** ：着色器中的 if/else 会导致所有 lane 执行两个分支
  * **使用 swizzle 而非索引** ：`v.xyz` 比 `v[0], v[1], v[2]` 更高效
  * **早期 discard** ：在片段着色器中尽早放弃片段以启用层次 Z 剔除
  * **减少纹理查询** ：纹理采样是昂贵操作，应最小化数量
  * **使用低精度类型** ：在移动设备上使用 mediump/lowp 以提高性能
  * **避免循环内纹理采样** ：如可能，在循环外进行采样

### 常见错误

**错误 1：** 忘记 #version 指令 
    
    
    #version 450 core  // GLSL 4.50 必需

**错误 2：** 混淆矩阵乘法顺序 
    
    
    // 正确：列向量左乘矩阵
    vec4 projected = matrix * vec4(position, 1.0);
    
    // 错误：
    vec4 projected = vec4(position, 1.0) * matrix;

**错误 3：** 在片段着色器使用精度限定符 
    
    
    // 只在可编程管线某些环节有效
    precision highp float;

**错误 4：** 数组越界 
    
    
    // GLSL 中不会自动检查数组越界，导致未定义行为

### 调试技巧

  * 使用 `FragColor = vec4(normalize(normal), 1.0);` 可视化法向量
  * 使用 `FragColor = vec4(vec3(depth), 1.0);` 可视化深度
  * 使用 `FragColor = texture(texture, texCoord);` 验证纹理坐标
  * 使用编译器警告和错误信息定位问题
  * RenderDoc 和 NVIDIA Nsight 等工具用于深度调试

## 11\. GLSL 4.50 新增特性

### Enhanced Layout Qualifiers
    
    
    // 显式指定 layout 位置
    layout(location = 0, index = 0) out vec4 color;
    layout(location = 1, index = 0) out vec4 normal;

### Bindless Texture Access
    
    
    layout(bindless_image) uniform imageBuffer images[];
    layout(bindless_sampler) uniform samplerBuffer samplers[];
    
    // 在着色器中直接使用句柄
    vec4 color = texture(samplers[index], uv);

### GL_ARB_ES3_1_compatibility
    
    
    // 支持 OpenGL ES 3.1 兼容特性
    // 用于跨平台开发

### Enhanced Derivative Control
    
    
    // 更精细的导数控制
    float dx = dFdx(value);           // x 方向导数
    float dy = dFdy(value);           // y 方向导数
    float dxCoarse = dFdxCoarse(value); // 粗粒度导数
    float dyFine = dFdyFine(value);     // 细粒度导数

## 12\. 参考资源

  * **Khronos OpenGL 规范：** 官方GLSL标准
  * **GLSL 4.50 完整规范：** https://registry.khronos.org/
  * **LearnOpenGL（learnopengl.com）：** 优秀教程资源
  * **Shader Toy（shadertoy.com）：** 着色器实验平台
  * **GPU Gems 系列：** 高级渲染技术
  * **Real-Time Rendering：** 权威图形学教材

文档最后更新：2025年12月22日

GLSL 4.50 规范参考 | OpenGL Shading Language
