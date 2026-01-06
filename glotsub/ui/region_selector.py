"""
区域选择器模块（修复版本）
使用独立的tkinter窗口，避免与CustomTkinter冲突
"""
import tkinter as tk
from typing import Optional, Callable, Dict


class RegionSelector:
    """屏幕区域选择器"""
    
    def __init__(self, parent_window, on_region_selected: Optional[Callable[[Dict[str, int]], None]] = None,
                 on_cancelled: Optional[Callable[[], None]] = None):
        """
        初始化区域选择器
        
        Args:
            parent_window: 父窗口（用于隐藏）
            on_region_selected: 区域选择完成回调
            on_cancelled: 取消选择回调
        """
        self.parent_window = parent_window
        self.on_region_selected = on_region_selected
        self.on_cancelled = on_cancelled
        
        self.region_window: Optional[tk.Toplevel] = None
        self.canvas: Optional[tk.Canvas] = None
        self.start_x: Optional[int] = None
        self.start_y: Optional[int] = None
        self.rect_id: Optional[int] = None
        self.is_selecting = False
    
    def start_selection(self):
        """开始区域选择"""
        if self.is_selecting:
            return
        
        self.is_selecting = True
        
        # 隐藏父窗口
        if hasattr(self.parent_window, 'withdraw'):
            self.parent_window.withdraw()
        elif hasattr(self.parent_window, 'iconify'):
            self.parent_window.iconify()
        
        # 创建全屏透明窗口
        self.region_window = tk.Toplevel()
        self.region_window.attributes('-fullscreen', True)
        self.region_window.attributes('-alpha', 0.3)
        self.region_window.configure(bg='black')
        self.region_window.attributes('-topmost', True)
        self.region_window.overrideredirect(True)  # 移除窗口装饰
        
        # 创建画布
        self.canvas = tk.Canvas(
            self.region_window,
            highlightthickness=0,
            bg='black',
            cursor='crosshair'
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绑定事件
        self.canvas.bind('<Button-1>', self._on_start)
        self.canvas.bind('<B1-Motion>', self._on_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_end)
        self.region_window.bind('<Escape>', self._on_cancel)
        self.region_window.bind('<Button-1>', self._on_start)
        self.region_window.bind('<B1-Motion>', self._on_drag)
        self.region_window.bind('<ButtonRelease-1>', self._on_end)
        
        # 设置焦点
        self.region_window.focus_set()
        self.canvas.focus_set()
        
        # 重置状态
        self.start_x = None
        self.start_y = None
        self.rect_id = None
    
    def _on_start(self, event):
        """开始选择"""
        # 获取屏幕坐标
        if hasattr(event, 'x_root') and hasattr(event, 'y_root'):
            self.start_x = event.x_root
            self.start_y = event.y_root
        else:
            # 备用方案：使用窗口坐标
            self.start_x = self.region_window.winfo_x() + event.x
            self.start_y = self.region_window.winfo_y() + event.y
    
    def _on_drag(self, event):
        """拖动选择"""
        if self.start_x is None or self.start_y is None:
            return
        
        # 删除旧的矩形
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        
        # 获取当前屏幕坐标
        if hasattr(event, 'x_root') and hasattr(event, 'y_root'):
            current_x = event.x_root
            current_y = event.y_root
        else:
            # 备用方案
            current_x = self.region_window.winfo_x() + event.x
            current_y = self.region_window.winfo_y() + event.y
        
        # 转换为窗口坐标
        win_x1 = self.start_x - self.region_window.winfo_x()
        win_y1 = self.start_y - self.region_window.winfo_y()
        win_x2 = current_x - self.region_window.winfo_x()
        win_y2 = current_y - self.region_window.winfo_y()
        
        self.rect_id = self.canvas.create_rectangle(
            win_x1, win_y1, win_x2, win_y2,
            outline='#00ff00',
            width=3,
            fill='',
            stipple='gray50'
        )
    
    def _on_end(self, event):
        """结束选择"""
        if self.start_x is None or self.start_y is None:
            self._cleanup()
            return
        
        # 获取结束坐标
        if hasattr(event, 'x_root') and hasattr(event, 'y_root'):
            end_x = event.x_root
            end_y = event.y_root
        else:
            end_x = self.region_window.winfo_x() + event.x
            end_y = self.region_window.winfo_y() + event.y
        
        x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
        x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)
        
        # 确保区域有效
        if abs(x2 - x1) < 10 or abs(y2 - y1) < 10:
            self._cleanup()
            if self.on_cancelled:
                self.on_cancelled()
            return
        
        # 创建区域字典（mss格式）
        region = {
            'left': x1,
            'top': y1,
            'width': x2 - x1,
            'height': y2 - y1
        }
        
        self._cleanup()
        
        if self.on_region_selected:
            self.on_region_selected(region)
    
    def _on_cancel(self, event=None):
        """取消选择"""
        self._cleanup()
        if self.on_cancelled:
            self.on_cancelled()
    
    def _cleanup(self):
        """清理资源"""
        self.is_selecting = False
        
        if self.region_window:
            try:
                self.region_window.destroy()
            except:
                pass
            self.region_window = None
        
        # 恢复父窗口
        if hasattr(self.parent_window, 'deiconify'):
            self.parent_window.deiconify()
        elif hasattr(self.parent_window, 'update'):
            self.parent_window.update()

