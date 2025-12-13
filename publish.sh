#!/bin/bash
# 打包并上传 cyqnt_trd 到 PyPI

set -e

echo "=========================================="
echo "打包并上传 cyqnt_trd 到 PyPI"
echo "=========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查是否在正确的目录
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}错误: 请在项目根目录运行此脚本${NC}"
    exit 1
fi

# 1. 清理旧的构建文件
echo -e "${YELLOW}步骤 1: 清理旧的构建文件...${NC}"
rm -rf build/
rm -rf dist/
rm -rf *.egg-info
rm -rf cyqnt_trd.egg-info
find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo -e "${GREEN}✓ 清理完成${NC}"

# 2. 检查必要的工具
echo -e "${YELLOW}步骤 2: 检查必要的工具...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 python3${NC}"
    exit 1
fi

if ! python3 -m pip show build &> /dev/null; then
    echo -e "${YELLOW}安装 build 工具...${NC}"
    python3 -m pip install --upgrade build
fi

if ! python3 -m pip show twine &> /dev/null; then
    echo -e "${YELLOW}安装 twine 工具...${NC}"
    python3 -m pip install --upgrade twine
fi
echo -e "${GREEN}✓ 工具检查完成${NC}"

# 3. 检查包配置
echo -e "${YELLOW}步骤 3: 检查包配置...${NC}"
python3 -c "import tomli; data = tomli.load(open('pyproject.toml', 'rb')); print(f\"包名: {data['project']['name']}\"); print(f\"版本: {data['project']['version']}\")" 2>/dev/null || \
python3 -c "import tomllib; data = tomllib.load(open('pyproject.toml', 'rb')); print(f\"包名: {data['project']['name']}\"); print(f\"版本: {data['project']['version']}\")" 2>/dev/null || \
echo "无法解析 pyproject.toml，请手动检查"
echo -e "${GREEN}✓ 配置检查完成${NC}"

# 4. 构建包
echo -e "${YELLOW}步骤 4: 构建包...${NC}"
python3 -m build
if [ $? -ne 0 ]; then
    echo -e "${RED}错误: 构建失败${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 构建完成${NC}"

# 5. 检查构建产物
echo -e "${YELLOW}步骤 5: 检查构建产物...${NC}"
ls -lh dist/
echo -e "${GREEN}✓ 检查完成${NC}"

# 6. 选择上传目标
echo ""
echo -e "${YELLOW}请选择上传目标:${NC}"
echo "1) TestPyPI (测试，推荐首次上传)"
echo "2) PyPI (正式发布)"
read -p "请输入选项 (1 或 2): " choice

if [ "$choice" == "1" ]; then
    REPOSITORY="--repository testpypi"
    echo -e "${YELLOW}将上传到 TestPyPI${NC}"
elif [ "$choice" == "2" ]; then
    REPOSITORY=""
    echo -e "${YELLOW}将上传到 PyPI (正式发布)${NC}"
    read -p "确认要上传到正式 PyPI 吗？(yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "已取消"
        exit 0
    fi
else
    echo -e "${RED}无效选项${NC}"
    exit 1
fi

# 7. 上传包
echo -e "${YELLOW}步骤 6: 上传包...${NC}"
echo -e "${YELLOW}注意: 需要使用 PyPI API Token（不是用户名/密码）${NC}"
echo -e "${YELLOW}请确保已设置环境变量：${NC}"
echo -e "${YELLOW}  export TWINE_USERNAME=__token__${NC}"
echo -e "${YELLOW}  export TWINE_PASSWORD=pypi-your-token-here${NC}"
echo ""
read -p "按 Enter 继续上传（或 Ctrl+C 取消）..."

# 检查是否设置了环境变量
if [ -z "$TWINE_USERNAME" ] || [ -z "$TWINE_PASSWORD" ]; then
    echo -e "${YELLOW}提示: 未检测到环境变量，将使用交互式输入${NC}"
    echo -e "${YELLOW}用户名请输入: __token__${NC}"
    echo -e "${YELLOW}密码请输入: 您的 PyPI API token${NC}"
fi

python3 -m twine upload $REPOSITORY dist/*

if [ $? -eq 0 ]; then
    echo -e "${GREEN}=========================================="
    echo -e "✓ 上传成功！${NC}"
    echo -e "${GREEN}=========================================="
    if [ "$choice" == "1" ]; then
        echo -e "${YELLOW}测试安装命令:${NC}"
        echo "pip install -i https://test.pypi.org/simple/ cyqnt-trd"
    else
        echo -e "${YELLOW}安装命令:${NC}"
        echo "pip install cyqnt-trd"
    fi
else
    echo -e "${RED}=========================================="
    echo -e "✗ 上传失败${NC}"
    echo -e "${RED}=========================================="
    exit 1
fi

