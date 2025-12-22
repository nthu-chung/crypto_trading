#!/bin/bash
# 使用 API Token 上传到 PyPI

set -e

echo "=========================================="
echo "PyPI 上传助手（使用 API Token）"
echo "=========================================="
echo ""

# 检查是否已设置环境变量
if [ -n "$TWINE_USERNAME" ] && [ -n "$TWINE_PASSWORD" ]; then
    echo "✓ 检测到环境变量已设置"
    echo "  Username: $TWINE_USERNAME"
    echo "  Password: ${TWINE_PASSWORD:0:15}..."
    echo ""
    read -p "是否使用当前环境变量？(y/n): " use_env
    if [ "$use_env" == "y" ]; then
        TOKEN="$TWINE_PASSWORD"
    else
        echo ""
        echo "请输入您的 PyPI API Token:"
        read -s TOKEN
        export TWINE_USERNAME=__token__
        export TWINE_PASSWORD="$TOKEN"
    fi
else
    echo "⚠️  环境变量未设置"
    echo ""
    echo "请按照以下步骤获取 PyPI API Token："
    echo "1. 访问: https://pypi.org/account/login/"
    echo "2. 登录后进入: Account settings > API tokens"
    echo "3. 点击: Add API token"
    echo "4. 复制生成的 token（格式: pypi-...）"
    echo ""
    echo "请输入您的 PyPI API Token:"
    read -s TOKEN
    
    if [ -z "$TOKEN" ]; then
        echo "错误: Token 不能为空"
        exit 1
    fi
    
    # 验证 token 格式
    if [[ ! "$TOKEN" =~ ^pypi- ]]; then
        echo "警告: Token 应该以 'pypi-' 开头"
        read -p "是否继续？(y/n): " confirm
        if [ "$confirm" != "y" ]; then
            exit 1
        fi
    fi
    
    # 设置环境变量
    export TWINE_USERNAME=__token__
    export TWINE_PASSWORD="$TOKEN"
fi

echo ""
echo "=========================================="
echo "选择上传目标:"
echo "1) TestPyPI (测试，推荐首次上传)"
echo "2) PyPI (正式发布)"
read -p "请输入选项 (1 或 2): " choice

if [ "$choice" == "1" ]; then
    REPOSITORY="--repository testpypi"
    echo ""
    echo "将上传到 TestPyPI"
elif [ "$choice" == "2" ]; then
    REPOSITORY=""
    echo ""
    echo "将上传到 PyPI (正式发布)"
    read -p "确认要上传到正式 PyPI 吗？(yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "已取消"
        exit 0
    fi
else
    echo "无效选项"
    exit 1
fi

echo ""
echo "=========================================="
echo "开始上传..."
echo "=========================================="

# 检查 dist 目录
if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
    echo "错误: dist 目录为空，请先运行构建命令"
    echo "运行: python3 -m build"
    exit 1
fi

# 上传
python3 -m twine upload $REPOSITORY dist/*

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ 上传成功！"
    echo "=========================================="
    if [ "$choice" == "1" ]; then
        echo ""
        echo "测试安装命令:"
        echo "  pip install -i https://test.pypi.org/simple/ cyqnt-trd"
    else
        echo ""
        echo "安装命令:"
        echo "  pip install cyqnt-trd"
    fi
else
    echo ""
    echo "=========================================="
    echo "✗ 上传失败"
    echo "=========================================="
    echo ""
    echo "可能的原因:"
    echo "1. Token 无效或已过期"
    echo "2. 包名或版本号已存在"
    echo "3. 网络连接问题"
    echo ""
    echo "请检查错误信息并重试"
    exit 1
fi


