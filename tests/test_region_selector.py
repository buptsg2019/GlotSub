"""
区域选择器单元测试
"""
import unittest
import tkinter as tk
from glotsub.ui.region_selector import RegionSelector


class TestRegionSelector(unittest.TestCase):
    """区域选择器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口
        self.region_selected = False
        self.region_data = None
        self.cancelled = False
    
    def tearDown(self):
        """测试后清理"""
        if self.root:
            self.root.destroy()
    
    def _on_region_selected(self, region):
        """区域选择回调"""
        self.region_selected = True
        self.region_data = region
    
    def _on_cancelled(self):
        """取消回调"""
        self.cancelled = True
    
    def test_region_selector_creation(self):
        """测试区域选择器创建"""
        selector = RegionSelector(
            self.root,
            on_region_selected=self._on_region_selected,
            on_cancelled=self._on_cancelled
        )
        self.assertIsNotNone(selector)
        self.assertFalse(selector.is_selecting)
    
    def test_region_selector_start(self):
        """测试开始选择区域"""
        selector = RegionSelector(
            self.root,
            on_region_selected=self._on_region_selected,
            on_cancelled=self._on_cancelled
        )
        selector.start_selection()
        self.assertTrue(selector.is_selecting)
        self.assertIsNotNone(selector.region_window)
        self.assertIsNotNone(selector.canvas)
        
        # 清理
        selector._cleanup()
    
    def test_region_selector_cancel(self):
        """测试取消选择"""
        selector = RegionSelector(
            self.root,
            on_region_selected=self._on_region_selected,
            on_cancelled=self._on_cancelled
        )
        selector.start_selection()
        
        # 模拟取消
        selector._on_cancel()
        
        self.assertFalse(selector.is_selecting)
        self.assertTrue(self.cancelled)
        self.assertIsNone(selector.region_window)
    
    def test_region_selector_cleanup(self):
        """测试清理功能"""
        selector = RegionSelector(
            self.root,
            on_region_selected=self._on_region_selected,
            on_cancelled=self._on_cancelled
        )
        selector.start_selection()
        self.assertTrue(selector.is_selecting)
        self.assertIsNotNone(selector.region_window)
        
        selector._cleanup()
        
        self.assertFalse(selector.is_selecting)
        self.assertIsNone(selector.region_window)
    
    def test_region_selector_double_start(self):
        """测试重复启动选择（应该被忽略）"""
        selector = RegionSelector(
            self.root,
            on_region_selected=self._on_region_selected,
            on_cancelled=self._on_cancelled
        )
        selector.start_selection()
        initial_state = selector.is_selecting
        
        # 再次启动应该被忽略
        selector.start_selection()
        self.assertEqual(selector.is_selecting, initial_state)
        
        selector._cleanup()
    
    def test_region_selector_small_region(self):
        """测试选择过小的区域（应该被取消）"""
        selector = RegionSelector(
            self.root,
            on_region_selected=self._on_region_selected,
            on_cancelled=self._on_cancelled
        )
        selector.start_selection()
        
        # 模拟选择很小的区域
        selector.start_x = 100
        selector.start_y = 100
        
        # 创建模拟事件（区域太小）
        class MockEvent:
            def __init__(self):
                self.x_root = 105  # 只有5像素
                self.y_root = 105
        
        selector._on_end(MockEvent())
        
        # 应该被取消而不是选择
        self.assertTrue(self.cancelled)
        self.assertFalse(self.region_selected)
        self.assertIsNone(self.region_data)


if __name__ == "__main__":
    unittest.main()

