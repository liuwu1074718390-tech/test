"""
PaddleOCR 工具类
封装 PaddleOCR 的常用功能
"""
from paddleocr import PaddleOCR
import os


class PaddleOCRUtil:
    def __init__(self, use_gpu=False, ocr_version='PP-OCRv4'):
        """
        初始化 PaddleOCR 工具类
        
        参数:
            use_gpu (bool): 是否使用 GPU 进行推理，默认 False（使用 CPU）
            ocr_version (str): OCR 模型版本，默认 'PP-OCRv4'
        """
        print(f"🔧 初始化 PaddleOCR (版本: {ocr_version}, GPU: {use_gpu})")
        
        self.ocr = PaddleOCR(
            use_angle_cls=True,  # 启用文字方向分类
            lang="ch",           # 中文识别
            use_gpu=use_gpu,
            ocr_version=ocr_version,
            show_log=False       # 关闭详细日志
        )
        
        print("✅ PaddleOCR 初始化完成")

    def perform_ocr(self, file_path):
        """
        对图片或 PDF 执行 OCR 识别
        
        参数:
            file_path (str): 图片或 PDF 文件路径
            
        返回:
            list: 识别结果列表。
                  如果是图片，返回: [[坐标, (文字, 置信度)], ...]
                  如果是 PDF，返回: [ [[坐标, (文字, 置信度)], ...], ... ] (每一项对应一页)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 执行 OCR 识别
        # PaddleOCR 默认支持 PDF，如果输入是 PDF，会返回每页的结果列表
        result = self.ocr.ocr(file_path, cls=True)
        
        if not result:
            return []
        
        return result

    def extract_text_with_meta(self, file_path):
        """
        提取文字、坐标、置信度和页码
        
        返回格式:
        [
            {
                "page_num": 1,
                "lines": [
                    {"text": "xxx", "confidence": 0.99, "coordinates": [[x1,y1],...]},
                    ...
                ]
            },
            ...
        ]
        """
        ocr_result = self.perform_ocr(file_path)
        
        if not ocr_result:
            return []
            
        # 统一处理结果（图片和 PDF）
        # 如果是图片，ocr_result 结构是 [ [[box, (text, conf)], ...] ]
        # 如果是 PDF，ocr_result 结构是 [ [[box, (text, conf)], ...], [[box, (text, conf)], ...], ... ]
        
        final_results = []
        for i, page_result in enumerate(ocr_result):
            if page_result is None: # 某些页可能识别为空
                continue
                
            lines = []
            for line in page_result:
                if line:
                    coords, (text, confidence) = line
                    lines.append({
                        "text": text,
                        "confidence": round(float(confidence), 4),
                        "coordinates": coords
                    })
            
            final_results.append({
                "page_num": i + 1,
                "lines": lines
            })
            
        return final_results

    def extract_text_only(self, image_path):
        """
        仅提取图片中的文字内容（不包含坐标和置信度）
        
        参数:
            image_path (str): 图片文件路径
            
        返回:
            list: 文字列表
        """
        ocr_result = self.perform_ocr(image_path)
        
        if not ocr_result:
            return []
        
        # 提取文字内容
        text_lines = [line[1][0] for line in ocr_result if line]
        return text_lines
