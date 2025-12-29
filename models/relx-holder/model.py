import cadquery as cq

# ========== 核心参数（以烟弹尺寸为基准） ==========
# 悦刻5代烟弹尺寸
pod_long_axis = 18.3   # 烟弹长轴 mm
pod_short_axis = 9.4   # 烟弹短轴 mm
clearance = 0.2        # 间隙配合量 mm（凹槽比烟弹大）

# 布局参数
pod_count = 5              # 烟弹数量
wall_between_slots = 5     # 凹槽之间壁厚 mm
edge_padding = 8           # 边缘留白 mm（凹槽边缘到底座边缘）

# 深度参数
slot_depth = 10            # 凹槽深度 mm（实际插入深度）
bottom_thickness = 4       # 凹槽底部厚度 mm
chamfer_top = 1.5          # 顶部倒角 mm（额外增加，漏斗形引导）

# 圆角参数
fillet_radius = 3          # 外圆角半径 mm
top_fillet = 1.5           # 顶部边圆角半径 mm

# 符号参数
mark_height = 0.6          # 凸起高度 mm
mark_width = 0.8           # 线条宽度 mm
mark_len = 4               # 线条长度 mm

# ========== 自动计算尺寸 ==========
# 凹槽尺寸
slot_long = pod_long_axis + clearance
slot_short = pod_short_axis + clearance

# 凹槽中心间距
slot_spacing = slot_long + wall_between_slots

# 底座尺寸
base_height = bottom_thickness + slot_depth + chamfer_top
base_length = pod_count * slot_long + (pod_count - 1) * wall_between_slots + 2 * edge_padding
base_width = slot_short + 2 * edge_padding

# 凹槽起始X坐标（居中排列）
start_x = -((pod_count - 1) * slot_spacing) / 2

# ========== 符号绘制函数 ==========
def create_mark(cx, cy, symbol):
    """
    创建符号实体。
    符号从底座内部开始，确保与底座重叠。
    """
    marks = []
    z_start = base_height - 2  # 从顶面下方2mm开始
    z_total = 2 + mark_height  # 穿透到顶面+凸出高度

    if symbol == "-":  # 横线
        marks.append(
            cq.Workplane("XY").workplane(offset=z_start)
            .moveTo(cx, cy).rect(mark_len, mark_width).extrude(z_total)
        )

    elif symbol == "+":  # 十字
        marks.append(
            cq.Workplane("XY").workplane(offset=z_start)
            .moveTo(cx, cy).rect(mark_len, mark_width).extrude(z_total)
        )
        marks.append(
            cq.Workplane("XY").workplane(offset=z_start)
            .moveTo(cx, cy).rect(mark_width, mark_len).extrude(z_total)
        )

    elif symbol == "N":  # N形
        # 左竖线
        marks.append(
            cq.Workplane("XY").workplane(offset=z_start)
            .moveTo(cx - mark_len * 0.35, cy).rect(mark_width, mark_len).extrude(z_total)
        )
        # 右竖线
        marks.append(
            cq.Workplane("XY").workplane(offset=z_start)
            .moveTo(cx + mark_len * 0.35, cy).rect(mark_width, mark_len).extrude(z_total)
        )
        # 斜线（从左上到右下）
        marks.append(
            cq.Workplane("XY").workplane(offset=z_start)
            .center(cx, cy).rect(mark_width, mark_len * 1.1).extrude(z_total)
            .rotate((cx, cy, 0), (cx, cy, 1), 35)
        )

    elif symbol == "=":  # 双横线
        marks.append(
            cq.Workplane("XY").workplane(offset=z_start)
            .moveTo(cx, cy - 1).rect(mark_len, mark_width).extrude(z_total)
        )
        marks.append(
            cq.Workplane("XY").workplane(offset=z_start)
            .moveTo(cx, cy + 1).rect(mark_len, mark_width).extrude(z_total)
        )

    elif symbol == "z":  # Z形
        # 上横线
        marks.append(
            cq.Workplane("XY").workplane(offset=z_start)
            .moveTo(cx, cy + mark_len * 0.3).rect(mark_len, mark_width).extrude(z_total)
        )
        # 下横线
        marks.append(
            cq.Workplane("XY").workplane(offset=z_start)
            .moveTo(cx, cy - mark_len * 0.3).rect(mark_len, mark_width).extrude(z_total)
        )
        # 斜线
        marks.append(
            cq.Workplane("XY").workplane(offset=z_start)
            .center(cx, cy).rect(mark_len * 0.9, mark_width).extrude(z_total)
            .rotate((cx, cy, 0), (cx, cy, 1), -45)
        )

    return marks

# ========== 创建模型 ==========
# 1. 创建底座主体
base = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_height, centered=(True, True, False))
    .edges("|Z")
    .fillet(fillet_radius)
    .edges(">Z")
    .fillet(top_fillet)
)

# 2. 挖出椭圆形凹槽
for i in range(pod_count):
    x_pos = start_x + i * slot_spacing

    # 主凹槽（从底部厚度位置开始挖）
    slot = (
        cq.Workplane("XY")
        .workplane(offset=bottom_thickness)
        .moveTo(x_pos, 0)
        .ellipse(slot_long / 2, slot_short / 2)
        .extrude(slot_depth + chamfer_top + 1)  # 穿透顶部
    )
    base = base.cut(slot)

    # 顶部开口倒角（漏斗形引导）
    chamfer_slot = (
        cq.Workplane("XY")
        .workplane(offset=base_height - chamfer_top)
        .moveTo(x_pos, 0)
        .ellipse(slot_long / 2, slot_short / 2)  # 底部：与凹槽同尺寸
        .workplane(offset=chamfer_top)
        .moveTo(x_pos, 0)
        .ellipse((slot_long / 2) + chamfer_top, (slot_short / 2) + chamfer_top)  # 顶部：扩大
        .loft()
    )
    base = base.cut(chamfer_slot)

# 3. 添加符号
symbols = ["-", "+", "N", "=", "z"]
for i in range(pod_count):
    x_pos = start_x + i * slot_spacing
    # 符号放在凹槽漏斗边缘和底座边缘的中间位置
    funnel_edge = (slot_short / 2) + chamfer_top
    safe_edge = (base_width / 2) - top_fillet - 1
    y_pos = (funnel_edge + safe_edge) / 2
    for mark in create_mark(x_pos, y_pos, symbols[i]):
        base = base.union(mark)

result = base

# ========== 输出信息 ==========
print("模型已生成！")
print(f"底座尺寸: {base_length:.1f} x {base_width:.1f} x {base_height:.1f} mm")
print(f"凹槽尺寸: {slot_long:.1f} x {slot_short:.1f} mm")
print(f"凹槽间距: {slot_spacing:.1f} mm（中心到中心）")
print(f"凹槽深度: {slot_depth} mm + 倒角 {chamfer_top} mm")
print(f"底部厚度: {bottom_thickness} mm")
