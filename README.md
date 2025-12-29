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
├── CLAUDE.md                    # AI 开发指南
├── venv/                        # Python 虚拟环境
└── models/                      # 模型目录（每个模型一个子目录）
    └── relx-holder/             # 示例：悦刻烟弹底座
        ├── README.md            # 模型说明（需求、参考资料）
        ├── model.py             # 模型代码
        └── preview.ipynb        # 模型预览（Jupyter）
```

## 使用方法

### 1. 创建新模型

```bash
mkdir -p models/my-new-model
cp -r models/relx-holder models/my-new-model
```

### 2. 预览模型

```bash
source venv/bin/activate
jupyter lab --ip=0.0.0.0 --port=3002 --no-browser --allow-root
```

打开 `preview.ipynb`，依次运行：
1. `open_viewer()` - 打开 3D 视图
2. `%run model.py` - 生成模型
3. `show(result)` - 预览
4. 导出 cell - 确认后导出 STEP/STL

## 导出格式

| 格式 | 用途 |
|------|------|
| `.step` | 可在 SolidWorks/FreeCAD 中编辑 |
| `.stl` | 直接用于 3D 打印切片 |

## 现有模型

- [悦刻烟弹底座](models/relx-holder/) - 桌面烟弹收纳座

## 开发

使用 AI 辅助开发时，参考 [CLAUDE.md](CLAUDE.md) 了解 CadQuery 开发经验。

## 参考

- [CadQuery 文档](https://cadquery.readthedocs.io/)
- [jupyter-cadquery](https://github.com/bernhard-42/jupyter-cadquery)
