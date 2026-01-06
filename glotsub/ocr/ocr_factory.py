"""
OCR引擎工厂
"""
from typing import Optional
from glotsub.ocr.ocr_engine import OCREngine
from glotsub.ocr.tesseract_ocr import TesseractOCR
from glotsub.ocr.paddle_ocr import PaddleOCR
from glotsub.utils.config import Config


class OCRFactory:
    """OCR引擎工厂类"""
    
    _engines = {
        "tesseract": TesseractOCR,
        "paddleocr": PaddleOCR,
    }
    
    @classmethod
    def create_engine(cls, engine_name: Optional[str] = None) -> Optional[OCREngine]:
        """
        创建OCR引擎实例
        
        Args:
            engine_name: 引擎名称，如果为None则使用配置中的默认引擎
            
        Returns:
            OCR引擎实例，如果不可用则返回None
        """
        if engine_name is None:
            engine_name = Config.OCR_ENGINE
        
        engine_class = cls._engines.get(engine_name.lower())
        if engine_class is None:
            print(f"不支持的OCR引擎: {engine_name}")
            # 尝试使用Tesseract作为后备
            engine_class = TesseractOCR
        
        engine = engine_class()
        if engine.is_available():
            return engine
        else:
            print(f"OCR引擎 {engine_name} 不可用")
            # 尝试其他可用引擎
            for name, cls in cls._engines.items():
                if name != engine_name.lower():
                    alt_engine = cls()
                    if alt_engine.is_available():
                        print(f"使用备用引擎: {name}")
                        return alt_engine
            return None

