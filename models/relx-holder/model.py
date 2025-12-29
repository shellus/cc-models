import cadquery as cq

# ========== 参数定义 ==========
# 悦刻5代烟弹尺寸（椭圆形截面，根据主机尺寸推算）
pod_long_axis = 11.5   # 烟弹长轴 mm
pod_short_axis = 7.5   # 烟弹短轴 mm
pod_count = 5          # 烟弹数量
slot_depth = 8         # 凹槽深度 mm
clearance = 0.2        # 间隙配合量 mm（凹槽比烟弹大，轻松放入取出）

# 计算实际凹槽尺寸（间隙配合，凹槽稍大）
slot_long = pod_long_axis + clearance   # 11.7mm
slot_short = pod_short_axis + clearance # 7.7mm

# 底座参数
slot_spacing = 16   # 凹槽间距 mm
base_padding = 8    # 边缘留白 mm
base_height = 12    # 底座总高度 mm
fillet_radius = 3   # 外圆角半径 mm（加大，更圆润）

# 开口导向参数（方便放入）
chamfer_top = 2.5   # 顶部倒角 mm（入口引导，漏斗形）

# ========== 计算底座尺寸 ==========
base_length = (pod_count - 1) * slot_spacing + 2 * base_padding + slot_long
base_width = slot_short + 2 * base_padding

# ========== 创建模型 ==========
# 1. 创建底座主体
base = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_height)
    .edges("|Z")  # 垂直边圆角
    .fillet(fillet_radius)
    .edges(">Z")  # 顶部边圆角
    .fillet(1.5)
)

# 2. 计算凹槽起始位置（居中排列）
start_x = -((pod_count - 1) * slot_spacing) / 2

# 3. 挖出5个椭圆形凹槽（带顶部倒角引导）
for i in range(pod_count):
    x_pos = start_x + i * slot_spacing

    # 主凹槽
    slot = (
        cq.Workplane("XY")
        .workplane(offset=base_height - slot_depth)
        .moveTo(x_pos, 0)
        .ellipse(slot_long / 2, slot_short / 2)
        .extrude(slot_depth + 1)
    )
    base = base.cut(slot)

    # 顶部开口倒角（漏斗形引导，方便放入）
    chamfer_slot = (
        cq.Workplane("XY")
        .workplane(offset=base_height - chamfer_top)
        .moveTo(x_pos, 0)
        .ellipse((slot_long / 2) + chamfer_top, (slot_short / 2) + chamfer_top)
        .workplane(offset=chamfer_top)
        .moveTo(x_pos, 0)
        .ellipse(slot_long / 2, slot_short / 2)
        .loft()
    )
    base = base.cut(chamfer_slot)

# 4. 在每个插槽之间添加凸起标志（简单符号：- + x = ^）
mark_height = 0.6      # 凸起高度 mm
mark_width = 0.8       # 线条宽度 mm
mark_len = 4           # 线条长度 mm

# 符号绘制函数
def add_mark_at(base, cx, cy, symbol):
    """在指定位置添加符号"""
    half = mark_len / 2

    if symbol == "-":  # 横线
        m = cq.Workplane("XY").workplane(offset=base_height).moveTo(cx, cy).rect(mark_len, mark_width).extrude(mark_height)
        base = base.union(m)

    elif symbol == "+":  # 十字
        m1 = cq.Workplane("XY").workplane(offset=base_height).moveTo(cx, cy).rect(mark_len, mark_width).extrude(mark_height)
        m2 = cq.Workplane("XY").workplane(offset=base_height).moveTo(cx, cy).rect(mark_width, mark_len).extrude(mark_height)
        base = base.union(m1).union(m2)

    elif symbol == "x":  # 叉号（两条对角线）
        m1 = cq.Workplane("XY").workplane(offset=base_height).center(cx, cy).rect(mark_len * 0.7, mark_width).extrude(mark_height).rotate((cx, cy, 0), (cx, cy, 1), 45)
        m2 = cq.Workplane("XY").workplane(offset=base_height).center(cx, cy).rect(mark_len * 0.7, mark_width).extrude(mark_height).rotate((cx, cy, 0), (cx, cy, 1), -45)
        base = base.union(m1).union(m2)

    elif symbol == "=":  # 双横线
        m1 = cq.Workplane("XY").workplane(offset=base_height).moveTo(cx, cy - 1).rect(mark_len, mark_width).extrude(mark_height)
        m2 = cq.Workplane("XY").workplane(offset=base_height).moveTo(cx, cy + 1).rect(mark_len, mark_width).extrude(mark_height)
        base = base.union(m1).union(m2)

    elif symbol == "^":  # V形（简单两条斜线）
        m1 = cq.Workplane("XY").workplane(offset=base_height).center(cx - 1.2, cy - 0.8).rect(mark_len * 0.5, mark_width).extrude(mark_height).rotate((cx - 1.2, cy - 0.8, 0), (cx - 1.2, cy - 0.8, 1), 45)
        m2 = cq.Workplane("XY").workplane(offset=base_height).center(cx + 1.2, cy - 0.8).rect(mark_len * 0.5, mark_width).extrude(mark_height).rotate((cx + 1.2, cy - 0.8, 0), (cx + 1.2, cy - 0.8, 1), -45)
        base = base.union(m1).union(m2)

    return base

# 5个插槽对应5个不同符号
symbols = ["-", "+", "x", "=", "^"]

for i in range(pod_count):
    x_pos = start_x + i * slot_spacing
    # 标志放在插槽前方（Y正方向），紧贴插槽边缘
    y_pos = (slot_short / 2) + chamfer_top + 2.5
    base = add_mark_at(base, x_pos, y_pos, symbols[i])

result = base

# ========== 显示/导出 ==========
show_object = result

cq.exporters.export(result, "model.step")
cq.exporters.export(result, "model.stl")

print("模型已生成！")
print(f"底座尺寸: {base_length:.1f} x {base_width:.1f} x {base_height} mm")
print(f"椭圆凹槽: {slot_long:.1f} x {slot_short:.1f} mm (间隙 +{clearance} mm)")
print(f"凹槽深度: {slot_depth} mm")
print(f"顶部倒角: {chamfer_top} mm（漏斗形引导）")
print(f"已导出: model.step, model.stl")
