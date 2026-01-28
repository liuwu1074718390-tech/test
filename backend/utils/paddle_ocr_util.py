from paddleocr import PaddleOCR
import os

class PaddleOCRUtil:
    def __init__(self, use_gpu=False, ocr_version='PP-OCRv4'):
        """
        Initialize the PaddleOCR utility.
        
        Args:
            use_gpu (bool): Whether to use GPU for inference. Defaults to False (CPU).
            ocr_version (str): The OCR model version to use. Defaults to 'PP-OCRv4'.
                               Pass 'PP-OCRv5' if confirmed available in installed package.
                               (Given 2026 date, PP-OCRv5 should be standard, but defaulting to passed arg).
        """
        # Initialize PaddleOCR with Chinese language support, angle classification, and CPU/GPU setting
        # 'use_mp' (multiprocess) can be adjusted if needed, but default is usually fine.
        # 'show_log' can be set to False to reduce noise.
        self.ocr = PaddleOCR(
            use_textline_orientation=True, 
            lang="ch", 
            ocr_version=ocr_version
        )

    def perform_ocr(self, image_path):
        """
        Perform OCR on the given image path.
        
        Args:
            image_path (str): Path to the image file.
            
        Returns:
            list: A list of result lines. Each line contains [coords, [text, confidence]].
                  Or formatted text if preferred. For raw result, we return the list.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
            
        # cls=True ensures angle classification is run (if enabled in init)
        result = self.ocr.ocr(image_path)
        
        # Adapt PaddleOCR 3.x / PaddleX output structure
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
            # PaddleX format: result[0] is a dict with 'rec_texts', 'rec_scores', 'dt_polys'
            data = result[0]
            texts = data.get('rec_texts', [])
            scores = data.get('rec_scores', [])
            boxes = data.get('dt_polys', []) # or rec_polys
            
            parsed_result = []
            for box, text, score in zip(boxes, texts, scores):
                # Convert numpy array box to list
                if hasattr(box, 'tolist'):
                    box = box.tolist()
                parsed_result.append([box, (text, score)])
            return parsed_result
            
        # Fallback for legacy format if structure is different
        if not result:
            return []
            
        # Legacy/Other format handling: result[0] is the list of lines
        return result[0]

    def extract_text_only(self, image_path):
        """
        Extract only the text content from the image, ignoring coordinates and confidence.
        
        Args:
            image_path (str): Path to the image file.
            
        Returns:
            list: List of strings found in the image.
        """
        ocr_result = self.perform_ocr(image_path)
        if not ocr_result:
            return []
            
        # line structure: [coords, (text, conf)]
        text_lines = [line[1][0] for line in ocr_result if line]
        return text_lines
