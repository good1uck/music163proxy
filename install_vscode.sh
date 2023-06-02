#!/bin/bash

# 检查是否已经安装了 Homebrew
if ! command -v brew &> /dev/null; then
    echo "Homebrew 未安装，请先安装 Homebrew（https://brew.sh）后再运行该脚本。"
    exit 1
fi

# 检查是否已经安装了 Visual Studio Code
if command -v code &> /dev/null; then
    echo "Visual Studio Code 已经安装。"
    exit 0
fi

# 安装 Visual Studio Code
brew install --cask visual-studio-code

# 检查安装是否成功
if command -v code &> /dev/null; then
    echo "Visual Studio Code 安装成功！"
else
    echo "安装失败，请检查网络连接或稍后重试。"
fi