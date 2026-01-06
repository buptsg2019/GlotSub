"""
配置管理模块
"""
import os
from typing import Dict, Any


class Config:
    """应用配置类"""
    
    # OCR配置
    OCR_ENGINE = "paddleocr"  # 可选: "tesseract", "paddleocr", "easyocr"
    TESSERACT_CONFIG = '--oem 3 --psm 6 -l chi_sim+eng'
    
    # 识别配置
    RECOGNITION_INTERVAL = 0.5  # 识别间隔（秒）
    MIN_SUBTITLE_LENGTH = 1  # 最小字幕长度
    
    # UI配置
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    APPEARANCE_MODE = "dark"  # "light", "dark", "system"
    COLOR_THEME = "blue"
    
    # 区域选择配置
    REGION_SELECTION_ALPHA = 0.3
    REGION_SELECTION_COLOR = "#00ff00"
    
    @classmethod
    def get_ocr_config(cls) -> Dict[str, Any]:
        """获取OCR配置"""
        return {
            "engine": cls.OCR_ENGINE,
            "tesseract_config": cls.TESSERACT_CONFIG,
        }
    
    @classmethod
    def set_ocr_engine(cls, engine: str):
        """设置OCR引擎"""
        if engine in ["tesseract", "paddleocr", "easyocr"]:
            cls.OCR_ENGINE = engine
        else:
            raise ValueError(f"不支持的OCR引擎: {engine}")

