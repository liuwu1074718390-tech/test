import sys
import os
from PIL import Image, ImageDraw

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.paddle_ocr_util import PaddleOCRUtil

def create_test_image(path):
    # Create a white image
    img = Image.new('RGB', (400, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    # Add text (using default font, might be small but readable for OCR)
    # If default font is not good, we depend on system. 
    # But usually easy text is fine.
    d.text((10, 40), "PaddleOCR Test 123", fill=(0, 0, 0))
    img.save(path)
    print(f"Created test image at {path}")

def test_ocr():
    image_path = "test_ocr_sample.png"
    create_test_image(image_path)
    
    print("Initializing PaddleOCRUtil...")
    try:
        # Request PP-OCRv5 as planned
        ocr_util = PaddleOCRUtil(ocr_version='PP-OCRv5', use_gpu=False)
        
        print(f"Running OCR on {image_path}...")
        results = ocr_util.perform_ocr(image_path)
        
        print("\nOCR Results:")
        found_text = []
        for line in results:
            text = line[1][0]
            conf = line[1][1]
            print(f" - Text: '{text}', Confidence: {conf:.4f}")
            found_text.append(text)
            
        # verification
        full_text = " ".join(found_text)
        if "PaddleOCR" in full_text or "Test" in full_text:
            print("\nSUCCESS: OCR detected expected text!")
        else:
            print("\nWARNING: OCR did not detect expected text. Check image or model.")
            
    except Exception as e:
        print(f"\nERROR during OCR execution: {e}")
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)
            print("Cleaned up test image.")

if __name__ == "__main__":
    test_ocr()
