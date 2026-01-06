"""
Tesseract OCR实现
"""
import pytesseract
import numpy as np
import cv2
from PIL import Image
from typing import Optional
from glotsub.ocr.ocr_engine import OCREngine
from glotsub.utils.config import Config


class TesseractOCR(OCREngine):
    """Tesseract OCR引擎"""
    
    def __init__(self):
        self.config = Config.TESSERACT_CONFIG
        self._available = None
    
    def is_available(self) -> bool:
        """检查Tesseract是否可用"""
        if self._available is None:
            try:
                pytesseract.get_tesseract_version()
                self._available = True
            except Exception:
                self._available = False
        return self._available
    
    def recognize(self, image: Image.Image) -> Optional[str]:
        """
        使用Tesseract识别文字
        
        Args:
            image: PIL Image对象
            
        Returns:
            识别出的文本
        """
        if not self.is_available():
            return None
        
        try:
            # 图像预处理
            img_array = np.array(image)
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # 二值化处理
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # 形态学操作去除噪点
            kernel = np.ones((1, 1), np.uint8)
            binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            
            # OCR识别
            text = pytesseract.image_to_string(binary, config=self.config).strip()
            return text if text else None
        except Exception as e:
            print(f"Tesseract识别错误: {e}")
            return None

