# 🚀 Serena CLI

[English](README.md) | [中文](README_CN.md)

**Serena CLI** 是一个强大的命令行工具，用于快速启用和配置 Serena 编码代理工具。它提供了完整的项目管理和配置功能，支持 MCP 协议和直接的 CLI 命令。

## ✨ 特性

- 🚀 **快速启用**: 一键在项目中启用 Serena
- 🔍 **智能检测**: 自动识别项目类型、结构、语言
- ⚙️ **配置管理**: 全局和项目级配置管理
- 🎯 **MCP 支持**: 与 Cursor、VSCode 等 IDE 集成
- 🐍 **Python 友好**: 支持 Python 3.8+ 环境
- 📊 **状态监控**: 实时查看 Serena 服务状态
- 🔧 **环境检查**: 自动检测兼容性和依赖

## 🚀 快速开始

### 📦 PyPI 安装（最简单）

```bash
# 直接安装最新版本
pip install serena-cli

# 或者指定版本
pip install serena-cli==1.0.0

# 安装后直接使用
serena-cli --help
```

### 🎯 一键安装（推荐）

#### Unix/Linux/macOS
```bash
# 下载项目
git clone https://github.com/impanda-cookie/serena-cli.git
cd serena-cli

# 一键安装
chmod +x install.sh
./install.sh
```

#### Windows
```bash
# 下载项目
git clone https://github.com/impanda-cookie/serena-cli.git
cd serena-cli

# 一键安装
install.bat
```

#### 跨平台 Python 脚本
```bash
# 下载项目
git clone https://github.com/impanda-cookie/serena-cli.git
cd serena-cli

# 一键安装
python install.py
```

### 🔧 手动安装

```bash
# 克隆项目
git clone https://github.com/impanda-cookie/serena-cli.git
cd serena-cli

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -e .
```

### 📱 基本使用

```bash
# 检查环境
serena-cli check-env

# 查看项目信息
serena-cli info

# 查看状态
serena-cli status

# 编辑配置
serena-cli config

# 查看帮助
serena-cli --help
```

## 🔧 主要命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `check-env` | 检查环境兼容性 | `serena-cli check-env` |
| `info` | 获取项目信息 | `serena-cli info` |
| `status` | 查询 Serena 状态 | `serena-cli status` |
| `config` | 编辑配置 | `serena-cli config` |
| `enable` | 启用 Serena | `serena-cli enable` |
| `mcp-tools` | 显示 MCP 工具 | `serena-cli mcp-tools` |

## 🎮 MCP 集成

### 🚀 智能启动向导

```bash
# 启动智能 MCP 服务器向导（推荐）
serena-cli start-mcp-server
```

**新功能：智能启动向导！**
`start-mcp-server` 命令现在会启动智能向导，自动：
- 🔍 检查您的环境
- 📦 安装缺失的依赖（uv、uvx、pip）
- 🎯 检测可用的 AI 编程工作台
- ⚙️ 为所选平台配置 MCP 设置
- ✅ 验证配置并提供使用指导

### 在 Cursor 中使用

```python
# 启用 Serena
@mcp serena_enable

# 查询状态
@mcp serena_status

# 编辑配置
@mcp edit_config
```

### 在 VSCode 中使用

```python
# 启用 Serena
@mcp serena_enable

# 查询状态
@mcp serena_status

# 编辑配置
@mcp edit_config
```

## ⚙️ 配置

### 全局配置

配置文件位置：`~/.serena-cli/config.yml`

```yaml
default_context: "ide-assistant"
install_method: "uv"
log_level: "INFO"
auto_start: true
port: 24282
```

### 项目配置

配置文件位置：`.serena-cli/project.yml`

```yaml
project_name: "your-project"
serena_context: "ide-assistant"
read_only: false
included_tools:
  - find_symbol
  - read_file
  - execute_shell_command
```

## 🔍 故障排除

### 常见问题

1. **命令未找到**: 确保虚拟环境已激活并重新安装
2. **Python 版本不兼容**: 使用 Python 3.11-3.12
3. **MCP 服务器启动失败**: 使用 CLI 命令作为替代

### 获取帮助

```bash
# 查看帮助
serena-cli --help

# 检查环境
serena-cli check-env

# 查看日志
tail -f ~/.serena-cli/logs/serena-cli.log
```

## 📚 文档

- [快速开始指南](QUICK_START.md) - 5分钟快速上手（中文）
- [Quick Start Guide](QUICK_START_EN.md) - 5分钟快速上手（English）
- [详细使用说明](usage_instructions.md) - 完整功能文档（中文）
- [Usage Instructions](usage_instructions_EN.md) - 完整功能文档（English）
- [项目状态报告](PROJECT_STATUS.md) - 开发进度和状态

## 🛠️ 开发

### 环境设置

```bash
# 克隆项目
git clone https://github.com/impanda-cookie/serena-cli.git
cd serena-cli

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装开发依赖
pip install -e .
pip install pytest black isort
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_project_detector.py

# 代码格式化
black src/
isort src/
```

### 项目结构

```
serena-cli/
├── src/serena_cli/          # 源代码
│   ├── __init__.py          # 包初始化
│   ├── cli.py               # 命令行界面
│   ├── mcp_server.py        # MCP 服务器
│   ├── serena_manager.py    # Serena 管理
│   ├── project_detector.py  # 项目检测
│   └── config_manager.py    # 配置管理
├── tests/                   # 测试文件
├── docs/                    # 文档
├── examples/                # 示例
├── install.py               # 一键安装脚本（Python）
├── install.sh               # 一键安装脚本（Unix/Linux/macOS）
├── install.bat              # 一键安装脚本（Windows）
├── pyproject.toml          # 项目配置
└── README.md               # 项目说明
```

## 🤝 贡献

我们欢迎所有形式的贡献！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Serena](https://github.com/oraios/serena) - 强大的 AI 编码代理工具
- [MCP](https://modelcontextprotocol.io/) - 模型上下文协议
- [Click](https://click.palletsprojects.com/) - Python 命令行界面库
- [Rich](https://rich.readthedocs.io/) - 终端美化输出库

## 📞 联系我们

- 项目主页: [GitHub Repository](https://github.com/impanda-cookie/serena-cli)
- 问题反馈: [GitHub Issues](https://github.com/impanda-cookie/serena-cli/issues)
- 讨论交流: [GitHub Discussions](https://github.com/impanda-cookie/serena-cli/discussions)

---

**Serena CLI** - 让 Serena 管理变得简单高效！ 🚀

如果这个项目对你有帮助，请给我们一个 ⭐️！

**Made with ❤️ by Panda**
