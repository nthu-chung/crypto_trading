#!/bin/bash
# 快速设置 PyPI API Token

echo "=========================================="
echo "PyPI API Token 配置助手"
echo "=========================================="
echo ""

# 检查是否已有 token
if [ -n "$TWINE_PASSWORD" ]; then
    echo "✓ 检测到环境变量 TWINE_PASSWORD 已设置"
    echo "  当前 token 前缀: ${TWINE_PASSWORD:0:10}..."
    read -p "是否要更新 token？(y/n): " update
    if [ "$update" != "y" ]; then
        echo "保持当前配置"
        exit 0
    fi
fi

echo "请按照以下步骤获取 PyPI API Token："
echo ""
echo "1. 访问: https://pypi.org/account/login/"
echo "2. 登录后进入: Account settings > API tokens"
echo "3. 点击: Add API token"
echo "4. 设置 Token name（如: cyqnt-trd-upload）"
echo "5. 选择 Scope（Entire account 或特定项目）"
echo "6. 复制生成的 token（格式: pypi-...）"
echo ""
echo "=========================================="
echo ""

# 选择配置方式
echo "请选择配置方式："
echo "1) 使用环境变量（推荐，仅当前终端会话）"
echo "2) 创建 ~/.pypirc 文件（永久配置）"
read -p "请输入选项 (1 或 2): " choice

if [ "$choice" == "1" ]; then
    echo ""
    echo "请输入您的 PyPI API Token:"
    read -s token
    echo ""
    
    if [ -z "$token" ]; then
        echo "错误: Token 不能为空"
        exit 1
    fi
    
    # 验证 token 格式
    if [[ ! "$token" =~ ^pypi- ]]; then
        echo "警告: Token 应该以 'pypi-' 开头"
        read -p "是否继续？(y/n): " confirm
        if [ "$confirm" != "y" ]; then
            exit 1
        fi
    fi
    
    # 设置环境变量
    export TWINE_USERNAME=__token__
    export TWINE_PASSWORD="$token"
    
    echo ""
    echo "✓ 环境变量已设置（仅当前终端会话有效）"
    echo ""
    echo "要永久设置，请将以下内容添加到 ~/.zshrc 或 ~/.bashrc:"
    echo "  export TWINE_USERNAME=__token__"
    echo "  export TWINE_PASSWORD=\"$token\""
    echo ""
    echo "或者运行此脚本选择选项 2 创建 ~/.pypirc 文件"
    echo ""
    echo "现在可以运行上传命令："
    echo "  python3 -m twine upload dist/*"
    
elif [ "$choice" == "2" ]; then
    echo ""
    echo "请输入您的 PyPI API Token:"
    read -s token
    echo ""
    
    if [ -z "$token" ]; then
        echo "错误: Token 不能为空"
        exit 1
    fi
    
    # 验证 token 格式
    if [[ ! "$token" =~ ^pypi- ]]; then
        echo "警告: Token 应该以 'pypi-' 开头"
        read -p "是否继续？(y/n): " confirm
        if [ "$confirm" != "y" ]; then
            exit 1
        fi
    fi
    
    # 创建 ~/.pypirc 文件
    cat > ~/.pypirc << EOF
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = $token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = $token
EOF
    
    # 设置文件权限（仅所有者可读）
    chmod 600 ~/.pypirc
    
    echo ""
    echo "✓ ~/.pypirc 文件已创建"
    echo "  文件位置: ~/.pypirc"
    echo "  权限: 600 (仅所有者可读)"
    echo ""
    echo "现在可以运行上传命令："
    echo "  python3 -m twine upload dist/*"
    
else
    echo "无效选项"
    exit 1
fi

echo ""
echo "=========================================="


