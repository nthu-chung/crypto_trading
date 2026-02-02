export TWINE_USERNAME='__token__'
export TWINE_PASSWORD='pypi-AgEIcHlwaS5vcmcCJDUzM2Q3N2Y2LTU0YWQtNGM2MS1hZjhiLTQ1ZTcyY2VhODRmOAACKlszLCJmYmY3YzkzNS1lMDkxLTQzOWMtOTRjOS1hNmUxMDA2ZjM5YzUiXQAABiDJ0pa4RnkjcXd6ZPh6O4FAuDD5xUgUYTcdkNFqIOoE2w'



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