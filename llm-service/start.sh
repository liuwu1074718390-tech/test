#!/bin/bash

# LLM 服务启动脚本

# 1. 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 正在创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📥 正在安装依赖..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 2. 启动服务
echo "🚀 启动 Qwen3-235B 服务..."
python app.py
