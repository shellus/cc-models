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
top_fillet = 1.5    # 顶部边圆角半径 mm

# 开口导向参数（方便放入）
chamfer_top = 1.5   # 顶部倒角 mm（入口引导，漏斗形，减小以避免相邻凹槽重叠）

# 符号参数
mark_height = 0.6   # 凸起高度 mm（高出顶面部分）
mark_width = 0.8    # 线条宽度 mm
mark_len = 4        # 线条长度 mm

# ========== 计算底座尺寸 ==========
base_length = (pod_count - 1) * slot_spacing + 2 * base_padding + slot_long
base_width = slot_short + 2 * base_padding
start_x = -((pod_count - 1) * slot_spacing) / 2

# ========== 符号绘制函数 ==========
def create_mark(cx, cy, symbol):
    """
    创建符号实体。
    符号从底座内部开始（base_height - top_fillet - 0.5），确保与底座重叠。
    """
    marks = []
    # 符号从顶面下方开始，确保与底座实体重叠
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

    elif symbol == "x":  # 叉号
        marks.append(
            cq.Workplane("XY").workplane(offset=z_start)
            .center(cx, cy).rect(mark_len * 0.7, mark_width).extrude(z_total)
            .rotate((cx, cy, 0), (cx, cy, 1), 45)
        )
        marks.append(
            cq.Workplane("XY").workplane(offset=z_start)
            .center(cx, cy).rect(mark_len * 0.7, mark_width).extrude(z_total)
            .rotate((cx, cy, 0), (cx, cy, 1), -45)
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
# 1. 创建底座主体（垂直边圆角 + 顶部边圆角）
# 注意：box() 默认居中，centered=(True,True,True)
# 设置 centered=(True,True,False) 使底面在 z=0，顶面在 z=base_height
base = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_height, centered=(True, True, False))
    .edges("|Z")
    .fillet(fillet_radius)
    .edges(">Z")
    .fillet(top_fillet)
)

# 2. 挖出椭圆形凹槽（带顶部倒角引导）
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

    # 顶部开口倒角（漏斗形引导：顶部大、底部小）
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

# 3. 添加符号（符号从底座内部穿出，确保连接）
# 符号放在凹槽和底座边缘之间的平坦区域
symbols = ["-", "+", "x", "=", "z"]
for i in range(pod_count):
    x_pos = start_x + i * slot_spacing
    # 符号放在凹槽漏斗边缘和底座边缘的中间位置
    funnel_edge = (slot_short / 2) + chamfer_top
    safe_edge = (base_width / 2) - top_fillet - 1  # 留出圆角和余量
    y_pos = (funnel_edge + safe_edge) / 2
    for mark in create_mark(x_pos, y_pos, symbols[i]):
        base = base.union(mark)

result = base

# ========== 输出信息 ==========
print("模型已生成！")
print(f"底座尺寸: {base_length:.1f} x {base_width:.1f} x {base_height} mm")
print(f"椭圆凹槽: {slot_long:.1f} x {slot_short:.1f} mm (间隙 +{clearance} mm)")
print(f"凹槽深度: {slot_depth} mm")
print(f"顶部倒角: {chamfer_top} mm（漏斗形引导）")
