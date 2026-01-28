import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.paddle_ocr_util import PaddleOCRUtil

def extract_text_from_image(image_path):
    print(f"正在处理图片: {image_path}")
    
    # Initialize OCR
    ocr_util = PaddleOCRUtil(ocr_version='PP-OCRv5', use_gpu=False)
    
    # Perform OCR
    results = ocr_util.perform_ocr(image_path)
    
    print("\n=== OCR 提取结果 ===\n")
    
    all_texts = []
    for idx, line in enumerate(results, 1):
        box, (text, conf) = line
        print(f"{idx}. {text} (置信度: {conf:.4f})")
        all_texts.append(text)
    
    print("\n=== 完整文本 ===\n")
    full_text = "\n".join(all_texts)
    print(full_text)
    
    return full_text

if __name__ == "__main__":
    image_path = "../iShot_2026-01-28_11.26.59.png"
    extract_text_from_image(image_path)
