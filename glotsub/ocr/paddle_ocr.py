"""
PaddleOCR实现（更好的中文支持）
"""
from PIL import Image
import numpy as np
from typing import Optional
from glotsub.ocr.ocr_engine import OCREngine


class PaddleOCR(OCREngine):
    """PaddleOCR引擎（更好的中文识别）"""
    
    def __init__(self):
        self._ocr = None
        self._available = None
    
    def _init_ocr(self):
        """初始化PaddleOCR"""
        if self._ocr is None:
            try:
                from paddleocr import PaddleOCR
                # 使用中英文模型
                self._ocr = PaddleOCR(
                    use_angle_cls=True,
                    lang='ch',  # 中文+英文
                    use_gpu=False,  # 默认使用CPU
                    show_log=False
                )
            except ImportError:
                self._ocr = None
            except Exception as e:
                print(f"PaddleOCR初始化失败: {e}")
                self._ocr = None
    
    def is_available(self) -> bool:
        """检查PaddleOCR是否可用"""
        if self._available is None:
            try:
                self._init_ocr()
                self._available = self._ocr is not None
            except Exception:
                self._available = False
        return self._available
    
    def recognize(self, image: Image.Image) -> Optional[str]:
        """
        使用PaddleOCR识别文字
        
        Args:
            image: PIL Image对象
            
        Returns:
            识别出的文本
        """
        if not self.is_available():
            return None
        
        try:
            # 转换PIL Image为numpy数组
            img_array = np.array(image)
            
            # PaddleOCR识别
            result = self._ocr.ocr(img_array, cls=True)
            
            if result and result[0]:
                # 提取所有识别文本
                texts = []
                for line in result[0]:
                    if line and len(line) >= 2:
                        text = line[1][0]  # 获取识别的文本
                        if text:
                            texts.append(text)
                
                # 合并文本
                text = "\n".join(texts).strip()
                return text if text else None
            return None
        except Exception as e:
            print(f"PaddleOCR识别错误: {e}")
            return None

