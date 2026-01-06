"""
字幕管理模块
"""
import time
from typing import List, Callable, Optional


class SubtitleManager:
    """字幕管理器"""
    
    def __init__(self):
        self.subtitles: List[str] = []
        self.last_subtitle: str = ""
        self.on_subtitle_added: Optional[Callable[[str, str], None]] = None
    
    def add_subtitle(self, text: str) -> bool:
        """
        添加字幕
        
        Args:
            text: 字幕文本
            
        Returns:
            是否成功添加（如果与上次相同则不添加）
        """
        text = text.strip()
        if text and text != self.last_subtitle and len(text) > 0:
            self.subtitles.append(text)
            self.last_subtitle = text
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            
            if self.on_subtitle_added:
                self.on_subtitle_added(text, timestamp)
            
            return True
        return False
    
    def clear(self):
        """清空所有字幕"""
        self.subtitles.clear()
        self.last_subtitle = ""
    
    def get_all_text(self) -> str:
        """获取所有字幕文本（用双换行分隔）"""
        return "\n\n".join(self.subtitles)
    
    def get_count(self) -> int:
        """获取字幕数量"""
        return len(self.subtitles)
    
    def export_to_text(self, filename: str) -> bool:
        """
        导出为文本文件
        
        Args:
            filename: 文件名
            
        Returns:
            是否成功
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for i, subtitle in enumerate(self.subtitles, 1):
                    f.write(f"{i}. {subtitle}\n\n")
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False
    
    def export_to_srt(self, filename: str) -> bool:
        """
        导出为SRT字幕文件
        
        Args:
            filename: 文件名
            
        Returns:
            是否成功
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for i, subtitle in enumerate(self.subtitles, 1):
                    f.write(f"{i}\n")
                    f.write(f"00:00:00,000 --> 00:00:00,000\n")
                    f.write(f"{subtitle}\n\n")
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False

