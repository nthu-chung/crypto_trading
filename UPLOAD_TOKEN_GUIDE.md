# PyPI 上传认证指南

## 问题说明

PyPI 已不再支持用户名/密码认证，必须使用 **API Token**。

## 解决方案

### 方法 1: 使用环境变量（推荐）

这是最安全和推荐的方法：

```bash
# 设置环境变量
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-actual-token-here

# 然后运行上传
python3 -m twine upload dist/*
```

### 方法 2: 使用 .pypirc 文件

编辑 `~/.pypirc` 文件（注意：不是项目目录下的 `.pypirc`）：

```ini
[pypi]
username = __token__
password = pypi-your-actual-token-here

[testpypi]
username = __token__
password = pypi-your-test-token-here
```

**重要**：
- 文件位置：`~/.pypirc`（用户主目录）
- 用户名必须是：`__token__`（两个下划线）
- password 是您的 API token（以 `pypi-` 开头）

### 方法 3: 交互式输入

运行上传命令时，twine 会提示输入：
- Username: `__token__`
- Password: 您的 API token

## 获取 API Token

1. 登录 PyPI: https://pypi.org/account/login/
2. 进入 **Account settings** > **API tokens**
3. 点击 **Add API token**
4. 设置：
   - Token name: 例如 `cyqnt-trd-upload`
   - Scope: 选择 "Entire account" 或特定项目
5. 复制 token（格式：`pypi-...`，只显示一次！）

## 测试上传

### 1. 先上传到 TestPyPI 测试

```bash
# 设置 TestPyPI token
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-test-token-here

# 上传到 TestPyPI
python3 -m twine upload --repository testpypi dist/*
```

### 2. 测试安装

```bash
pip install -i https://test.pypi.org/simple/ cyqnt-trd
```

### 3. 确认无误后上传到正式 PyPI

```bash
# 设置正式 PyPI token
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-production-token-here

# 上传到正式 PyPI
python3 -m twine upload dist/*
```

## 快速修复当前问题

如果您刚才遇到了 403 错误，请按以下步骤操作：

```bash
# 1. 获取您的 PyPI API token（从 PyPI 网站）

# 2. 设置环境变量
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-token-here

# 3. 重新上传
cd /Users/user/Desktop/repo/crypto_trading
python3 -m twine upload dist/*
```

## 安全提示

1. **不要将 token 提交到 Git**
2. **不要将 token 分享给他人**
3. **定期轮换 token**
4. **使用环境变量而不是文件存储 token**

## 常见错误

### 错误 1: 403 Forbidden
- **原因**: 使用了用户名/密码而不是 API token
- **解决**: 使用 `__token__` 作为用户名，token 作为密码

### 错误 2: 401 Unauthorized
- **原因**: Token 无效或已过期
- **解决**: 重新生成 token

### 错误 3: 400 Bad Request
- **原因**: 包名或版本号已存在
- **解决**: 更新版本号或使用不同的包名



