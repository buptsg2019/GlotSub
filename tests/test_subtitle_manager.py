"""
字幕管理器单元测试
"""
import unittest
import os
import tempfile
from glotsub.core.subtitle_manager import SubtitleManager


class TestSubtitleManager(unittest.TestCase):
    """字幕管理器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.manager = SubtitleManager()
        self.added_subtitles = []
    
    def _on_subtitle_added(self, text, timestamp):
        """字幕添加回调"""
        self.added_subtitles.append((text, timestamp))
    
    def test_add_subtitle(self):
        """测试添加字幕"""
        self.manager.on_subtitle_added = self._on_subtitle_added
        
        result = self.manager.add_subtitle("测试字幕1")
        self.assertTrue(result)
        self.assertEqual(self.manager.get_count(), 1)
        self.assertEqual(len(self.added_subtitles), 1)
    
    def test_add_duplicate_subtitle(self):
        """测试添加重复字幕"""
        self.manager.add_subtitle("测试字幕")
        result = self.manager.add_subtitle("测试字幕")
        self.assertFalse(result)
        self.assertEqual(self.manager.get_count(), 1)
    
    def test_clear(self):
        """测试清空字幕"""
        self.manager.add_subtitle("字幕1")
        self.manager.add_subtitle("字幕2")
        self.assertEqual(self.manager.get_count(), 2)
        
        self.manager.clear()
        self.assertEqual(self.manager.get_count(), 0)
        self.assertEqual(self.manager.last_subtitle, "")
    
    def test_get_all_text(self):
        """测试获取所有文本"""
        self.manager.add_subtitle("字幕1")
        self.manager.add_subtitle("字幕2")
        
        text = self.manager.get_all_text()
        self.assertIn("字幕1", text)
        self.assertIn("字幕2", text)
    
    def test_export_to_text(self):
        """测试导出为文本文件"""
        self.manager.add_subtitle("测试字幕1")
        self.manager.add_subtitle("测试字幕2")
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            filename = f.name
        
        try:
            result = self.manager.export_to_text(filename)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(filename))
            
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("测试字幕1", content)
                self.assertIn("测试字幕2", content)
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_export_to_srt(self):
        """测试导出为SRT文件"""
        self.manager.add_subtitle("测试字幕1")
        self.manager.add_subtitle("测试字幕2")
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.srt') as f:
            filename = f.name
        
        try:
            result = self.manager.export_to_srt(filename)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(filename))
            
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("测试字幕1", content)
                self.assertIn("测试字幕2", content)
                self.assertIn("00:00:00,000 --> 00:00:00,000", content)
        finally:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == "__main__":
    unittest.main()

