"""
屏幕截图模块
"""
import mss
from PIL import Image
from typing import Optional, Dict


class ScreenshotCapture:
    """屏幕截图捕获类"""
    
    def __init__(self):
        self.sct = mss.mss()
    
    def capture_region(self, region: Dict[str, int]) -> Optional[Image.Image]:
        """
        截取指定区域
        
        Args:
            region: 区域字典，包含 'left', 'top', 'width', 'height'
            
        Returns:
            PIL Image对象，如果失败返回None
        """
        try:
            screenshot = self.sct.grab(region)
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            return img
        except Exception as e:
            print(f"截图失败: {e}")
            return None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'sct'):
            self.sct.close()

