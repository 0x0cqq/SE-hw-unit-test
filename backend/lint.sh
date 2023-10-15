# 使用 autopep8 对代码自动格式化
autopep8 --in-place --recursive .

# 使用 autoflake 对代码自动格式化
autoflake --in-place --recursive --remove-unused-variables .

# 使用 isort 对代码自动格式化
isort .

# 使用 flake8 检查代码风格
flake8