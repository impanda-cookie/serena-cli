# 📦 发布到 PyPI

本指南将帮助你将 Serena CLI 发布到 Python Package Index (PyPI)。

## 🎯 发布前准备

### 1. 安装发布工具

```bash
pip install build twine
```

### 2. 配置 PyPI 账户

#### 注册 PyPI 账户
1. 访问 [PyPI](https://pypi.org/account/register/) 注册账户
2. 访问 [Test PyPI](https://test.pypi.org/account/register/) 注册测试账户

#### 获取 API Token
1. 在 PyPI 账户设置中创建 API Token
2. 在 Test PyPI 账户设置中创建 API Token
3. 保存这些 Token 用于发布

### 3. 配置认证

创建 `~/.pypirc` 文件：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

## 🚀 发布流程

### 方法 1: 使用发布脚本（推荐）

```bash
# 发布到 Test PyPI
python scripts/publish.py --test

# 发布到正式 PyPI
python scripts/publish.py

# 跳过测试
python scripts/publish.py --skip-tests

# 跳过构建
python scripts/publish.py --skip-build
```

### 方法 2: 手动发布

#### 1. 构建包
```bash
# 清理之前的构建
rm -rf dist/ build/ *.egg-info/

# 构建包
python -m build
```

#### 2. 检查包
```bash
# 检查构建的包
python -m twine check dist/*
```

#### 3. 发布到 Test PyPI
```bash
# 先发布到测试环境
python -m twine upload --repository testpypi dist/*
```

#### 4. 测试安装
```bash
# 从 Test PyPI 安装测试
pip install --index-url https://test.pypi.org/simple/ serena-cli

# 测试功能
serena-cli --version
serena-cli --help
```

#### 5. 发布到正式 PyPI
```bash
# 发布到正式环境
python -m twine upload dist/*
```

## 🔄 自动化发布

### GitHub Actions

项目已配置 GitHub Actions 工作流，支持：

1. **标签触发**: 推送 `v*` 标签时自动发布
2. **手动触发**: 在 GitHub Actions 页面手动触发
3. **多 Python 版本测试**: 支持 Python 3.8-3.12
4. **自动发布**: 测试通过后自动发布到 PyPI

#### 使用 GitHub Actions 发布

1. **推送标签**:
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. **手动触发**:
   - 访问 GitHub Actions 页面
   - 选择 "Publish to PyPI" 工作流
   - 点击 "Run workflow"
   - 输入版本号和是否先发布到 Test PyPI

### 配置 GitHub Secrets

在 GitHub 仓库设置中添加以下 Secrets：

- `PYPI_API_TOKEN`: PyPI API Token
- `TEST_PYPI_API_TOKEN`: Test PyPI API Token

## 📋 发布检查清单

### 发布前检查

- [ ] 所有测试通过
- [ ] 代码质量检查通过
- [ ] 文档更新完成
- [ ] 版本号已更新
- [ ] CHANGELOG.md 已更新
- [ ] Git 标签已创建

### 发布后检查

- [ ] 包在 PyPI 上可见
- [ ] 可以正常安装
- [ ] 所有功能正常工作
- [ ] 文档链接正确
- [ ] GitHub Release 已创建

## 🐛 常见问题

### 1. 认证失败

**问题**: `HTTPError: 401 Client Error: Unauthorized`

**解决方案**:
- 检查 API Token 是否正确
- 确认 Token 有上传权限
- 验证 `~/.pypirc` 配置

### 2. 包名冲突

**问题**: `HTTPError: 400 Client Error: File already exists`

**解决方案**:
- 更新版本号
- 删除之前的构建文件
- 重新构建和发布

### 3. 依赖问题

**问题**: 构建失败或依赖缺失

**解决方案**:
- 检查 `pyproject.toml` 配置
- 验证所有依赖版本
- 运行 `pip install -e .` 测试安装

## 📚 相关资源

- [PyPI 官方文档](https://packaging.python.org/tutorials/packaging-projects/)
- [Test PyPI 文档](https://test.pypi.org/help/)
- [Python 打包用户指南](https://packaging.python.org/guides/)
- [setuptools 文档](https://setuptools.pypa.io/)

## 🎉 发布成功

发布成功后，用户可以通过以下方式安装：

```bash
# 安装最新版本
pip install serena-cli

# 安装特定版本
pip install serena-cli==1.0.0

# 升级到最新版本
pip install --upgrade serena-cli
```

---

**提示**: 建议先在 Test PyPI 上测试，确认无误后再发布到正式 PyPI。
