# 快速上传指南

## 当前问题

您遇到了 403 Forbidden 错误，因为 PyPI 需要使用 API Token 而不是用户名/密码。

## 快速解决（3步）

### 步骤 1: 获取 API Token

1. 访问 https://pypi.org/account/login/ 并登录
2. 进入 **Account settings** > **API tokens**
3. 点击 **Add API token**
4. 设置 Token name（如：`cyqnt-trd-upload`）
5. 选择 Scope（Entire account 或特定项目）
6. **复制 token**（格式：`pypi-...`，只显示一次！）

### 步骤 2: 配置 Token

**方式 A：使用快速配置脚本（推荐）**

```bash
cd /Users/user/Desktop/repo/crypto_trading
./setup_pypi_token.sh
```

脚本会引导您完成配置。

**方式 B：手动设置环境变量**

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-actual-token-here
```

**方式 C：创建 ~/.pypirc 文件**

```bash
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers = pypi

[pypi]
username = __token__
password = pypi-your-actual-token-here
EOF

chmod 600 ~/.pypirc
```

### 步骤 3: 重新上传

```bash
cd /Users/user/Desktop/repo/crypto_trading
python3 -m twine upload dist/*
```

## 重要提示

- **用户名必须是**：`__token__`（两个下划线）
- **Password 是**：您的 API token（不是账户密码）
- **Token 格式**：`pypi-...`（以 `pypi-` 开头）

## 测试上传（推荐）

首次上传建议先测试：

```bash
# 1. 上传到 TestPyPI
python3 -m twine upload --repository testpypi dist/*

# 2. 测试安装
pip install -i https://test.pypi.org/simple/ cyqnt-trd

# 3. 确认无误后上传到正式 PyPI
python3 -m twine upload dist/*
```

## 验证安装

上传成功后，其他人可以通过以下命令安装：

```bash
pip install cyqnt-trd
```



