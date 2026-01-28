#!/bin/bash

# OCR 微服务 - 启动脚本

set -e

echo "======================================"
echo "🚀 启动 OCR 微服务"
echo "======================================"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "❌ 错误: 虚拟环境不存在"
    echo "请先运行: ./setup.sh"
    exit 1
fi

# 激活虚拟环境
echo "🔌 激活虚拟环境..."
source venv/bin/activate

# 检查依赖是否安装
if ! python -c "import paddleocr" 2>/dev/null; then
    echo "❌ 错误: 依赖未安装"
    echo "请先运行: ./setup.sh"
    exit 1
fi

echo "✅ 环境检查通过"
echo ""
echo "🌐 服务信息:"
echo "  - API 地址: http://localhost:8000"
echo "  - 文档地址: http://localhost:8000/docs"
echo "  - 健康检查: http://localhost:8000/"
echo ""
echo "💡 提示: 按 Ctrl+C 停止服务"
echo "======================================"
echo ""

# 启动服务
python app.py
