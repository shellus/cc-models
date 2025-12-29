# AI CAD 工作台

使用 AI + CadQuery 通过对话生成可编辑的参数化 3D 模型，用于 3D 打印。

## 特点

- **文字描述生成模型**：向 AI 描述需求，自动生成 CadQuery 代码
- **增量修改**：查看效果后可以说"加宽 2mm"这样的增量调整
- **参数化设计**：所有尺寸以变量定义，易于调整
- **可编辑导出**：导出 STEP 格式，可在 SolidWorks/FreeCAD 中二次编辑
- **3D 打印就绪**：同时导出 STL 格式，可直接切片打印

## 环境搭建

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖（国内镜像）
PIP_INDEX_URL=https://mirrors.huaweicloud.com/repository/pypi/simple \
pip3 install cadquery-ocp cadquery jupyter-cadquery jupyterlab
```

## 项目结构

```
.
├── README.md
├── venv/                        # Python 虚拟环境
└── models/                      # 模型目录（每个模型一个子目录）
    └── relx-holder/             # 示例：悦刻烟弹底座
        ├── README.md            # 模型说明（需求、参考资料）
        ├── model.py             # 模型代码
        ├── preview.ipynb        # 模型预览（Jupyter）
        ├── model.step           # STEP 导出（可编辑）
        └── model.stl            # STL 导出（3D打印）
```

## 使用方法

### 1. 创建新模型

```bash
# 创建模型目录
mkdir -p models/my-new-model

# 复制模板（或手动创建）
cp -r models/relx-holder models/my-new-model
```

每个模型目录包含：

| 文件 | 用途 |
|------|------|
| `README.md` | 模型说明、需求、参考资料 |
| `model.py` | 模型代码（参数定义 + 建模逻辑） |
| `preview.ipynb` | Jupyter 预览（运行 model.py 并显示） |

model.py 模板：

```python
import cadquery as cq

# ========== 参数定义 ==========
width = 50
height = 30
depth = 10

# ========== 创建模型 ==========
result = cq.Workplane("XY").box(width, height, depth)

# ========== 导出 ==========
cq.exporters.export(result, "model.step")
cq.exporters.export(result, "model.stl")
print("模型已生成！")
```

preview.ipynb 模板：

```python
# Cell 1
from jupyter_cadquery import show, open_viewer
open_viewer("cadquery")

# Cell 2
%run model.py

# Cell 3
show(result)
```

### 2. 生成模型

```bash
source venv/bin/activate
cd models/my-new-model
python model.py
```

### 3. 预览模型

启动 Jupyter Lab：

```bash
source venv/bin/activate
jupyter lab --ip=0.0.0.0 --port=3002 --no-browser --allow-root
```

启动后终端会输出带 token 的访问链接，类似：

```
http://127.0.0.1:3002/lab?token=xxxx...
```

点击或复制该链接到浏览器，打开对应模型的 `preview.ipynb`，运行所有 cells 即可预览。

### 4. 增量修改

与 AI 对话进行调整：

```
你：凹槽深度改成 10mm
AI：[修改 model.py 中的参数]

你：底座加宽 5mm
AI：[修改 model.py 中的参数]
```

修改后在 Jupyter 中重新运行 `%run model.py` 和 `show(result)` 查看效果。

## 导出格式

| 格式 | 用途 |
|------|------|
| `.step` | 可在 SolidWorks/FreeCAD 中编辑 |
| `.stl` | 直接用于 3D 打印切片 |
| `.3mf` | 3D 打印（支持颜色/材料信息） |

## 现有模型

- [悦刻烟弹底座](models/relx-holder/) - 桌面烟弹收纳座

## 参考

- [CadQuery 文档](https://cadquery.readthedocs.io/)
- [jupyter-cadquery](https://github.com/bernhard-42/jupyter-cadquery)
