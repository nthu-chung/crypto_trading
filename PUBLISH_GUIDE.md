# cyqnt_trd 打包和上传指南

本指南将帮助您将 `cyqnt_trd` 包打包并上传到 PyPI，使其可以通过 `pip install` 安装。

## 前置准备

### 1. 注册 PyPI 账户

- **TestPyPI** (测试环境): https://test.pypi.org/account/register/
- **PyPI** (正式环境): https://pypi.org/account/register/

### 2. 创建 API Token

1. 登录 PyPI 后，进入 **Account settings** > **API tokens**
2. 点击 **Add API token**
3. 设置 token 名称（如：`cyqnt-trd-upload`）
4. 选择作用域：
   - **TestPyPI**: 选择 "Entire account" 或特定项目
   - **PyPI**: 选择 "Entire account" 或特定项目
5. 复制生成的 token（格式：`pypi-...`，只显示一次，请妥善保存）

### 3. 安装必要工具

```bash
pip install --upgrade build twine
```

## 方法一：使用自动化脚本（推荐）

### 1. 配置 API Token

编辑 `.pypirc` 文件，将 token 填入：

```ini
[pypi]
username = __token__
password = pypi-your-actual-token-here

[testpypi]
username = __token__
password = pypi-your-test-token-here
```

或者使用环境变量（更安全）：

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-token-here
```

### 2. 运行发布脚本

```bash
chmod +x publish.sh
./publish.sh
```

脚本会自动：
- 清理旧的构建文件
- 检查必要工具
- 构建包
- 提示选择上传目标（TestPyPI 或 PyPI）
- 上传包

## 方法二：手动步骤

### 1. 清理旧的构建文件

```bash
rm -rf build/ dist/ *.egg-info cyqnt_trd.egg-info
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### 2. 构建包

```bash
python3 -m build
```

这会生成：
- `dist/cyqnt_trd-0.1.0.tar.gz` (源码包)
- `dist/cyqnt_trd-0.1.0-py3-none-any.whl` (wheel 包)

### 3. 检查构建产物

```bash
# 检查文件列表
python3 -m twine check dist/*

# 查看包内容（可选）
tar -tzf dist/cyqnt_trd-0.1.0.tar.gz | head -20
```

### 4. 上传到 TestPyPI（推荐首次上传）

```bash
python3 -m twine upload --repository testpypi dist/*
```

输入用户名和密码（或使用 token）：
- 用户名：`__token__`
- 密码：您的 PyPI API token

### 5. 测试安装

```bash
pip install -i https://test.pypi.org/simple/ cyqnt-trd
```

### 6. 上传到正式 PyPI

确认测试无误后，上传到正式 PyPI：

```bash
python3 -m twine upload dist/*
```

## 方法三：使用环境变量（最安全）

不创建 `.pypirc` 文件，直接使用环境变量：

```bash
# 设置环境变量
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-token-here

# 构建
python3 -m build

# 上传到 TestPyPI
python3 -m twine upload --repository testpypi dist/*

# 或上传到正式 PyPI
python3 -m twine upload dist/*
```

## 更新版本

每次更新版本时：

1. 更新 `pyproject.toml` 中的版本号：
   ```toml
   version = "0.1.1"  # 从 0.1.0 升级到 0.1.1
   ```

2. 更新 `cyqnt_trd/__init__.py` 中的版本号：
   ```python
   __version__ = "0.1.1"
   ```

3. 重新构建和上传：
   ```bash
   ./publish.sh
   ```

## 版本号规范

遵循 [语义化版本](https://semver.org/)：
- **主版本号** (1.0.0): 不兼容的 API 修改
- **次版本号** (0.1.0): 向后兼容的功能性新增
- **修订号** (0.0.1): 向后兼容的问题修正

## 验证安装

上传成功后，验证安装：

```bash
# 从 TestPyPI 安装
pip install -i https://test.pypi.org/simple/ cyqnt-trd

# 从正式 PyPI 安装
pip install cyqnt-trd

# 验证导入
python3 -c "import cyqnt_trd; print(cyqnt_trd.__version__)"
```

## 常见问题

### 1. 上传失败：包名已存在

如果包名已被占用，需要：
- 修改 `pyproject.toml` 中的 `name` 字段
- 或联系 PyPI 管理员

### 2. 上传失败：版本号已存在

每个版本号只能上传一次，需要：
- 更新 `pyproject.toml` 中的 `version` 字段
- 更新 `cyqnt_trd/__init__.py` 中的 `__version__`

### 3. 认证失败

- 检查 token 是否正确
- 确保 token 有正确的权限
- 检查 `.pypirc` 文件格式是否正确

### 4. 包安装后缺少文件

检查 `MANIFEST.in` 文件，确保包含所有必要的文件。

## 安全建议

1. **不要将 `.pypirc` 提交到 Git**：
   ```bash
   echo ".pypirc" >> .gitignore
   ```

2. **使用环境变量而不是文件存储 token**

3. **定期轮换 API token**

4. **使用 TestPyPI 进行测试**，确认无误后再上传到正式 PyPI

## 参考资源

- [Python Packaging User Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [PyPI Help](https://pypi.org/help/)



