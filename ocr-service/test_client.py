"""
OCR 微服务 - 简单测试脚本
用于验证 OCR 功能是否正常工作
"""
import requests
import sys
from pathlib import Path


def test_health_check():
    """测试健康检查接口"""
    print("1️⃣  测试健康检查接口...")
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ 健康检查通过")
            print(f"   响应: {response.json()}")
            return True
        else:
            print(f"❌ 健康检查失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("   请确保服务已启动: ./start.sh")
        return False


def test_ocr(image_path):
    """测试 OCR 识别接口"""
    print(f"\n2️⃣  测试 OCR 识别接口...")
    print(f"   图片: {image_path}")
    
    if not Path(image_path).exists():
        print(f"❌ 图片不存在: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:8000/ocr/extract", files=files)
        
        if response.status_code == 200:
            result = response.json()
            texts = result['data']['texts']
            print(f"✅ OCR 识别成功，共识别出 {len(texts)} 行文字:")
            for i, text in enumerate(texts, 1):
                print(f"   {i}. {text}")
            return True
        else:
            print(f"❌ OCR 识别失败: HTTP {response.status_code}")
            print(f"   响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("🧪 OCR 微服务测试")
    print("=" * 50)
    print()
    
    # 测试健康检查
    if not test_health_check():
        sys.exit(1)
    
    # 测试 OCR（如果提供了图片路径）
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        if not test_ocr(image_path):
            sys.exit(1)
    else:
        print("\n💡 提示: 运行 'python test_client.py <图片路径>' 可测试 OCR 识别")
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过")
    print("=" * 50)
