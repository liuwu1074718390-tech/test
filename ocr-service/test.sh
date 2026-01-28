#!/bin/bash

# OCR 微服务 - 接口测试脚本

echo "======================================"
echo "🧪 OCR 微服务接口测试"
echo "======================================"

# 检查服务是否运行
echo "📡 检查服务状态..."
if ! curl -s http://localhost:8000/ > /dev/null; then
    echo "❌ 错误: 服务未运行"
    echo "请先运行: ./start.sh"
    exit 1
fi

echo "✅ 服务正在运行"
echo ""

# 测试健康检查接口
echo "1️⃣  测试健康检查接口..."
echo "GET http://localhost:8000/"
curl -s http://localhost:8000/ | python3 -m json.tool
echo ""
echo ""

# 测试 OCR 接口（需要提供测试图片）
echo "2️⃣  测试 OCR 识别接口..."
echo "提示: 请将测试图片放在当前目录，命名为 test.jpg"
echo ""

if [ -f "test.jpg" ]; then
    echo "POST http://localhost:8000/ocr/extract"
    curl -X POST \
      -F "file=@test.jpg" \
      http://localhost:8000/ocr/extract | python3 -m json.tool
    echo ""
else
    echo "⚠️  未找到测试图片 test.jpg，跳过 OCR 测试"
    echo ""
    echo "💡 使用方法:"
    echo "  curl -X POST -F 'file=@your_image.jpg' http://localhost:8000/ocr/extract"
fi

echo ""
echo "======================================"
echo "✅ 测试完成"
echo "======================================"
echo ""
echo "📖 更多接口文档请访问: http://localhost:8000/docs"
echo ""
