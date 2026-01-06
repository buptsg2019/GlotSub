"""
OCR引擎接口
"""
from abc import ABC, abstractmethod
from PIL import Image
from typing import Optional


class OCREngine(ABC):
    """OCR引擎抽象基类"""
    
    @abstractmethod
    def recognize(self, image: Image.Image) -> Optional[str]:
        """
        识别图像中的文字
        
        Args:
            image: PIL Image对象
            
        Returns:
            识别出的文本，失败返回None
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        检查引擎是否可用
        
        Returns:
            是否可用
        """
        pass

