# 悦刻5代烟弹底座

桌面烟弹收纳底座，用于整齐存放悦刻5代（幻影）烟弹。

## 设计需求

1. **存放 5 个烟弹**：一排 5 个椭圆形凹槽
2. **轻松放入取出**：间隙配合，不卡弹
3. **无需精确对准**：顶部漏斗形倒角引导
4. **触摸识别**：每个插槽有不同凸起符号（- + × = ^），便于盲摸定位
5. **稳定放置**：底部平整贴合桌面
6. **美观圆润**：整体圆角处理
7. **不易积灰**：符号采用简单线条

## 烟弹尺寸参考

悦刻5代烟弹截面为椭圆形。尺寸根据主机规格推算：

- 主机尺寸（含烟弹）：112mm × 23mm × 10mm
- 烟弹截面推算：长轴约 11-12mm，短轴约 7-8mm

> **注意**：代码中的尺寸为推算值，建议实际测量后调整 `pod_long_axis` 和 `pod_short_axis` 参数。

**参考来源**：
- [悦刻官网产品规格](https://www.relxtech.com/)
- [RELX Infinity 设备评测](https://relxnow.com/blogs/user-reviews/device-review) - 主机尺寸 112mm × 23mm × 10mm

## 生成模型

```bash
cd models/relx-holder
python model.py
```

## 预览

在 Jupyter 中：

```python
%run models/relx-holder/model.py
show(result)
```

## 导出文件

| 文件 | 用途 |
|------|------|
| `model.step` | 可在 SolidWorks/FreeCAD 中编辑 |
| `model.stl` | 直接用于 3D 打印切片 |

## 打印建议

- **材料**：PLA / PETG
- **层高**：0.2mm
- **填充**：15-20%
- **支撑**：无需
- **方向**：底面朝下
