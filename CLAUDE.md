# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 必读

首先阅读 [README.md](README.md) 了解项目结构、环境搭建和使用方法。

## 常用命令

```bash
# 激活虚拟环境（每次操作前必须执行）
source venv/bin/activate

# 生成模型（仅预览参数）
python3 models/relx-holder/model.py

# 生成并导出 STEP/STL
python3 models/relx-holder/model.py --export

# 启动 Jupyter 预览
jupyter lab --ip=0.0.0.0 --port=3002 --no-browser --allow-root
```

## 开发经验

### 坐标系

- `box()` 默认在三个轴上居中（centered=(True,True,True)），Z 范围是 -h/2 到 +h/2
- 使用 `centered=(True, True, False)` 使底面在 z=0，顶面在 z=height
- 所有后续操作（凹槽、凸起）的 Z 坐标必须与主体一致

### union 悬空问题

添加凸起特征（如符号、studs）时，必须确保特征与主体在空间上有重叠：
- 从主体内部开始挤出，穿透到主体外部
- 例如：`z_start = base_height - 2`，`z_total = 2 + mark_height`

### fillet 顺序

1. 先做垂直边圆角 `.edges("|Z").fillet(r1)`
2. 再做顶部边圆角 `.edges(">Z").fillet(r2)`
3. 复杂几何体（union 后）做 fillet 可能失败，应在 union 前完成圆角

### loft 方向

- 第一个截面在底部，第二个在顶部
- 漏斗形开口：底部小、顶部大

### 调试方法

1. **自行运行验证**：修改代码后运行 `python model.py` 查看输出，不需要用户每次截图
2. **输出数值验证**：用 print 输出关键坐标，检查是否在预期范围内
3. **查阅文档**：遇到 CadQuery API 问题，使用 context7 MCP 查询 `/cadquery/cadquery` 文档
