# 修复 PyPI 认证问题

## 当前问题

您遇到了 403 Forbidden 错误，因为 twine 没有正确使用 API Token 认证。

## 立即解决方案

### 方法 1: 在当前终端设置环境变量（最快）

```bash
# 1. 获取您的 PyPI API Token（从 https://pypi.org/account/settings/）
# 2. 在当前终端设置环境变量
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-actual-token-here

# 3. 验证环境变量已设置
echo "Username: $TWINE_USERNAME"
echo "Password: ${TWINE_PASSWORD:0:10}..."

# 4. 重新上传
cd /Users/user/Desktop/repo/crypto_trading
python3 -m twine upload dist/*
```

### 方法 2: 使用交互式输入

```bash
cd /Users/user/Desktop/repo/crypto_trading
python3 -m twine upload dist/*
```

当提示时输入：
- **Username**: `__token__`（两个下划线，不是单个）
- **Password**: 您的 API token（格式：`pypi-...`）

### 方法 3: 创建 ~/.pypirc 文件

```bash
# 创建配置文件（替换为您的实际 token）
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers = pypi

[pypi]
username = __token__
password = pypi-your-actual-token-here
EOF

# 设置权限
chmod 600 ~/.pypirc

# 重新上传
cd /Users/user/Desktop/repo/crypto_trading
python3 -m twine upload dist/*
```

## 获取 API Token

1. 访问：https://pypi.org/account/login/
2. 登录后进入：**Account settings** > **API tokens**
3. 点击：**Add API token**
4. 设置：
   - Token name: `cyqnt-trd-upload`
   - Scope: 选择 "Entire account" 或特定项目
5. **复制 token**（格式：`pypi-...`，只显示一次！）

## 验证配置

运行以下命令验证环境变量：

```bash
echo "TWINE_USERNAME: $TWINE_USERNAME"
echo "TWINE_PASSWORD: ${TWINE_PASSWORD:0:15}..."
```

如果输出为空，说明环境变量未设置。

## 常见错误

### 错误 1: 仍然提示用户名/密码
- **原因**: 环境变量未设置或未生效
- **解决**: 确保在**同一个终端**中设置环境变量并运行上传命令

### 错误 2: 403 Forbidden
- **原因**: Token 无效或格式错误
- **解决**: 
  - 确保用户名是 `__token__`（两个下划线）
  - 确保 token 以 `pypi-` 开头
  - 检查 token 是否已过期或被删除

### 错误 3: 401 Unauthorized
- **原因**: Token 权限不足
- **解决**: 创建新 token 时选择 "Entire account" 权限

## 快速测试

```bash
# 设置 token（替换为您的实际 token）
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmcCJGI5YjY3YjE3LWE4YzEtNDY3ZC1hYjY3LWI5YjY3YjE3YjY3YjE3

# 测试上传到 TestPyPI（推荐先测试）
python3 -m twine upload --repository testpypi dist/*

# 如果成功，再上传到正式 PyPI
python3 -m twine upload dist/*
```



