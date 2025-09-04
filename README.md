# 🎨 FastDanbooruDataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Gallery-dl](https://img.shields.io/badge/powered%20by-gallery--dl-green.svg)](https://github.com/mikf/gallery-dl)

🚀 **快速从 Danbooru 下载对应的 tag 和图片，并自动高效处理成训练模型的数据集！**

专为 **Stable Diffusion LoRA 训练**、**机器学习**和 **AI 模型训练**设计的一站式数据集生成工具。

**FastDanbooruDataset** 基于强大的 [gallery-dl](https://github.com/mikf/gallery-dl) 引擎，提供现代化 Web 界面和智能数据集后处理功能，让您轻松构建高质量的训练数据集。

## ✨ 核心特性

###  **专为训练数据集设计**
-  **批量下载**：输入 Danbooru 标签，一键下载大量高质量图片
-  **标签配对**：自动下载图片对应的标签文件（.txt），完美适配训练需求
-  **智能处理**：自动配对图片和标签文件，生成训练就绪的数据集

###  **规范的后处理功能**
-  **标签标准化**：自动清理和格式化标签，移除无效字符
-  **标签编辑**：批量删除不需要的标签，添加自定义标签
-  **文件重命名**：智能重命名文件，保持图片和标签文件的配对关系
-  **目录整理**：自动处理未配对文件，保持数据集整洁

###  **用户友好的界面**
-  **Web 界面**：现代化的浏览器界面，无需命令行操作
-  **实时监控**：实时显示下载进度和处理状态
-  **高性能**：基于 gallery-dl 多线程下载，速度快效率高
-  **一键启动**：双击 launch.bat 即可启动，零配置使用

## 🚀 快速开始

### 系统要求

- Python 3.8 或更高版本
- Windows 10/11（推荐）或 Linux/macOS

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/Noyze-AI/FastDanbooruDataset.git
   cd FastDanbooruDataset
   ```

2. **一键启动**（Windows）
   ```bash
   # 双击运行或在命令行执行
   .\launch.bat
   ```

3. **手动启动**（所有平台）
   ```bash
   # 安装依赖
   pip install -r requirements.txt
   
   # 启动应用
   python app.py
   ```

4. **访问界面**
   
   打开浏览器访问：http://localhost:5678

## 📖 使用指南

#### 第一步：下载数据
1. 在 Web 界面输入 Danbooru 标签（如：`1girl`, `anime`, 等）
2. 设置下载目录（默认将分标签自动存储到项目的dataset文件夹）
3. 设置最大下载数量（1-1000张，根据训练需求）
4. 点击「开始下载」，系统自动下载图片和对应标签文件

#### 第二步：数据集后处理
1. **自动配对**：系统自动匹配图片(.jpg/.png)和标签(.txt)文件
2. **标签标准化**：清理标签格式，确保训练兼容性
3. **文件重命名**：统一编号命名格式，如 `1.jpg` 和 `1.txt`
4. **质量检查**：处理未配对文件，确保数据集完整性

#### 第三步：编辑标签
- **批量删除标签**：移除不需要的标签（如版权信息、艺术家名等）
- **批量模糊删除标签**：模糊检索，删除包含指定字段的标签，如 `bad` 
- **批量添加自定义标签**：为整个数据集添加特定标签

#### 第四步：训练就绪
- ✅ 图片和标签文件完美配对
- ✅ 标签格式标准化，兼容主流训练框架
- ✅ 文件命名规范，便于批量处理
- ✅ 数据集结构清晰，可直接用于 LoRA/模型训练



## ⚙️ 使用建议

### 📁 推荐的目录结构
```
dataset/
├── character_name/          # 角色训练数据集
│   ├── 1.jpg
│   ├── 1.txt
│   ├── 2.jpg
│   └── 2.txt
├── style_name/              # 风格训练数据集
└── concept_name/            # 概念训练数据集
```

### 🎯 标签选择建议
- **角色训练**：使用具体角色名 + 特征标签
- **风格训练**：使用艺术风格 + 技法标签  
- **概念训练**：使用概念词 + 相关描述标签
- **质量控制**：建议下载 50-200 张高质量图片

### ⚡ 性能优化
- 下载数量建议：初次使用 50-100 张，根据效果调整
- 网络环境：建议在网络稳定时进行大批量下载
- 存储空间：预留足够空间，平均每张图片 1-3MB


## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE.txt) 文件了解详情。

## 🎯 适用场景

### 🤖 AI 模型训练
- **Stable Diffusion LoRA 训练**：生成角色、风格、概念训练数据集
- **图像分类模型**：构建分类训练数据集
- **计算机视觉研究**：获取标注完整的图像数据
- **艺术风格学习**：收集特定风格的艺术作品

### 📊 数据集特点
- **高质量图片**：来自 Danbooru 的精选图片
- **详细标签**：每张图片都有对应的详细标签描述
- **标准格式**：兼容主流训练框架的数据格式
- **即用性强**：下载后可直接用于训练，无需额外处理

## 🔧 技术特性

- **基于 gallery-dl**：利用成熟稳定的下载引擎
- **多线程下载**：支持并发下载，提升效率
- **智能重试**：网络异常时自动重试
- **进度监控**：实时显示下载和处理进度
- **错误处理**：完善的异常处理和日志记录

## 🙏 致谢

- [gallery-dl](https://github.com/mikf/gallery-dl) - 强大的图片下载引擎
- [Danbooru](https://danbooru.donmai.us/) - 优质的图片数据源
- [Flask](https://flask.palletsprojects.com/) - 轻量级 Web 框架

## 📞 支持与反馈

如果您在使用过程中遇到问题或有改进建议，欢迎通过以下方式联系：

-  **问题反馈**：在项目中创建 Issue
- 💡 **功能建议**：欢迎提出新功能需求
- 🤝 **贡献代码**：欢迎提交 Pull Request

---

⭐ **如果这个项目有帮助到您快速构建训练数据集，或者您喜欢这个项目，请给个 Star 支持一下！**

