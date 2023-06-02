#!/bin/bash

# 安装 Homebrew（如果尚未安装）
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 更新 Homebrew
echo "Updating Homebrew..."
brew update

# 安装 Python
echo "Installing Python..."
brew install python

# 显示 Python 版本
echo "Python version:"
python --version