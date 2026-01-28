#!/bin/bash

# OCR 微服务 - 环境初始化脚本
# 首次使用时运行此脚本安装依赖

set -e  # 遇到错误立即退出

echo "======================================"
echo "🔧 OCR 微服务 - 环境初始化"
echo "======================================"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📂 当前目录: $SCRIPT_DIR"

# 检查 Python 版本
echo ""
echo "🐍 检查 Python 版本..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3，请先安装 Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ 找到 $PYTHON_VERSION"

# 创建虚拟环境
echo ""
echo "📦 创建 Python 虚拟环境..."
if [ -d "venv" ]; then
    echo "⚠️  虚拟环境已存在，跳过创建"
else
    python3 -m venv venv
    echo "✅ 虚拟环境创建完成"
fi

# 激活虚拟环境
echo ""
echo "🔌 激活虚拟环境..."
source venv/bin/activate

# 升级 pip
echo ""
echo "⬆️  升级 pip..."
pip install --upgrade pip -q

# 安装依赖
echo ""
echo "📥 安装项目依赖（这可能需要几分钟）..."
pip install -r requirements.txt

echo ""
echo "======================================"
echo "✅ 环境初始化完成！"
echo "======================================"
echo ""
echo "📝 使用说明:"
echo "  1. 启动服务: ./start.sh"
echo "  2. 停止服务: 按 Ctrl+C"
echo "  3. 测试接口: ./test.sh"
echo ""
echo "🌐 服务地址:"
echo "  - API 地址: http://localhost:8000"
echo "  - 文档地址: http://localhost:8000/docs"
echo ""
