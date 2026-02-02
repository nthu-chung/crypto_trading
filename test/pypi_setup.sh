export TWINE_USERNAME='__token__'
export TWINE_PASSWORD='pypi-your-token-here'



# 1. 安装工具
pip3 install --upgrade build twine

# 2. 清理
rm -rf build/ dist/ *.egg-info

# 3. 构建
python3 -m build

# 4. 检查
python3 -m twine check dist/*

# 5. 上传到 TestPyPI（测试）
python3 -m twine upload --repository testpypi dist/*

# 6. 测试安装
pip3 install -i https://test.pypi.org/simple/ cyqnt-trd

# 7. 上传到正式 PyPI
python3 -m twine upload dist/*