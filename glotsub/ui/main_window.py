"""
主窗口模块
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
import time
from typing import Optional, Dict
from glotsub.ui.region_selector import RegionSelector
from glotsub.core.screenshot import ScreenshotCapture
from glotsub.core.subtitle_manager import SubtitleManager
from glotsub.ocr.ocr_factory import OCRFactory
from glotsub.utils.config import Config


class MainWindow:
    """主窗口类"""
    
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title("GlotSub - 字幕识别工具")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        
        # 核心组件
        self.subtitle_manager = SubtitleManager()
        self.subtitle_manager.on_subtitle_added = self._on_subtitle_added
        
        self.ocr_engine = None
        self.screenshot_capture: Optional[ScreenshotCapture] = None
        self.region_selector: Optional[RegionSelector] = None
        
        # 状态变量
        self.is_running = False
        self.is_paused = False
        self.monitor_region: Optional[Dict[str, int]] = None
        self.recognition_thread: Optional[threading.Thread] = None
        
        # UI组件
        self.region_label = None
        self.start_btn = None
        self.stop_btn = None
        self.select_btn = None
        self.subtitle_text = None
        self.count_label = None
        self.status_label = None
        
        self._setup_ui()
        self._init_ocr()
    
    def _setup_ui(self):
        """设置用户界面"""
        # 主容器
        main_container = ctk.CTkFrame(self.root, corner_radius=0)
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # 顶部标题栏
        title_frame = ctk.CTkFrame(main_container, corner_radius=0, fg_color=("gray90", "gray13"))
        title_frame.pack(fill="x", padx=0, pady=0)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🎬 GlotSub 字幕识别工具",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=15)
        
        # 控制面板区域
        control_panel = ctk.CTkFrame(main_container, corner_radius=10)
        control_panel.pack(fill="x", padx=20, pady=(20, 10))
        
        # 第一行：区域选择
        region_frame = ctk.CTkFrame(control_panel, fg_color="transparent")
        region_frame.pack(fill="x", padx=15, pady=10)
        
        self.select_btn = ctk.CTkButton(
            region_frame,
            text="📍 选择识别区域",
            command=self._select_region,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=35,
            corner_radius=8
        )
        self.select_btn.pack(side="left", padx=5)
        
        self.region_label = ctk.CTkLabel(
            region_frame,
            text="未选择区域",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50")
        )
        self.region_label.pack(side="left", padx=15)
        
        # 第二行：控制按钮
        button_frame = ctk.CTkFrame(control_panel, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=10)
        
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="▶️ 开始识别",
            command=self._toggle_recognition,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=35,
            corner_radius=8,
            fg_color=("gray75", "gray25"),
            state="disabled"
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="⏹️ 停止识别",
            command=self._stop_recognition,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=35,
            corner_radius=8,
            fg_color=("gray75", "gray25"),
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5)
        
        # 第三行：操作按钮
        action_frame = ctk.CTkFrame(control_panel, fg_color="transparent")
        action_frame.pack(fill="x", padx=15, pady=10)
        
        clear_btn = ctk.CTkButton(
            action_frame,
            text="🗑️ 清空列表",
            command=self._clear_subtitles,
            font=ctk.CTkFont(size=12),
            height=32,
            corner_radius=8,
            fg_color=("gray70", "gray30")
        )
        clear_btn.pack(side="left", padx=5)
        
        copy_btn = ctk.CTkButton(
            action_frame,
            text="📋 复制全部",
            command=self._copy_all,
            font=ctk.CTkFont(size=12),
            height=32,
            corner_radius=8,
            fg_color=("gray70", "gray30")
        )
        copy_btn.pack(side="left", padx=5)
        
        export_btn = ctk.CTkButton(
            action_frame,
            text="💾 导出文件",
            command=self._export_subtitles,
            font=ctk.CTkFont(size=12),
            height=32,
            corner_radius=8,
            fg_color=("gray70", "gray30")
        )
        export_btn.pack(side="left", padx=5)
        
        # 字幕列表区域
        list_container = ctk.CTkFrame(main_container, corner_radius=10)
        list_container.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        # 字幕列表标题
        list_header = ctk.CTkFrame(list_container, fg_color="transparent")
        list_header.pack(fill="x", padx=15, pady=(15, 10))
        
        list_label = ctk.CTkLabel(
            list_header,
            text="📝 识别的字幕列表",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        list_label.pack(side="left")
        
        self.count_label = ctk.CTkLabel(
            list_header,
            text="(0 条)",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50")
        )
        self.count_label.pack(side="left", padx=10)
        
        # 滚动文本框显示字幕
        self.subtitle_text = ctk.CTkTextbox(
            list_container,
            wrap="word",
            font=ctk.CTkFont(size=12, family="Microsoft YaHei"),
            corner_radius=8,
            border_width=2,
            border_color=("gray70", "gray30")
        )
        self.subtitle_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # 状态栏
        status_frame = ctk.CTkFrame(main_container, corner_radius=0, fg_color=("gray85", "gray15"))
        status_frame.pack(fill="x", side="bottom", padx=0, pady=0)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="就绪",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.status_label.pack(side="left", padx=15, pady=8)
    
    def _init_ocr(self):
        """初始化OCR引擎"""
        self.ocr_engine = OCRFactory.create_engine()
        if not self.ocr_engine:
            messagebox.showerror(
                "错误",
                "未检测到可用的OCR引擎！\n\n"
                "请安装以下之一：\n"
                "1. Tesseract OCR（推荐用于快速启动）\n"
                "2. PaddleOCR（推荐用于中文识别，需安装：pip install paddlepaddle paddleocr）\n\n"
                "安装后将相应程序添加到系统PATH"
            )
    
    def _select_region(self):
        """选择识别区域"""
        if self.is_running:
            messagebox.showwarning("警告", "请先停止识别！")
            return
        
        self.status_label.configure(text="请在屏幕上拖动鼠标选择识别区域（按ESC取消）")
        
        # 创建区域选择器
        self.region_selector = RegionSelector(
            self.root,
            on_region_selected=self._on_region_selected,
            on_cancelled=self._on_region_cancelled
        )
        self.region_selector.start_selection()
    
    def _on_region_selected(self, region: Dict[str, int]):
        """区域选择完成回调"""
        self.monitor_region = region
        x1, y1 = region['left'], region['top']
        x2, y2 = x1 + region['width'], y1 + region['height']
        
        self.region_label.configure(
            text=f"区域: ({x1},{y1}) - ({x2},{y2})",
            text_color=("green", "#4ade80")
        )
        self.start_btn.configure(state="normal", fg_color=None)
        self.status_label.configure(text=f"区域已选择: {region['width']}x{region['height']} 像素")
    
    def _on_region_cancelled(self):
        """区域选择取消回调"""
        self.status_label.configure(text="区域选择已取消")
    
    def _toggle_recognition(self):
        """开始/暂停识别"""
        if not self.is_running:
            if self.monitor_region is None:
                messagebox.showwarning("警告", "请先选择识别区域！")
                return
            
            if not self.ocr_engine:
                messagebox.showerror("错误", "OCR引擎不可用！")
                return
            
            self.is_running = True
            self.is_paused = False
            self.start_btn.configure(text="⏸️ 暂停识别", fg_color=("gray75", "gray25"))
            self.stop_btn.configure(state="normal", fg_color=None)
            self.select_btn.configure(state="disabled")
            self.status_label.configure(text="正在识别中...")
            
            # 启动识别线程
            self.recognition_thread = threading.Thread(target=self._recognition_loop, daemon=True)
            self.recognition_thread.start()
        else:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.start_btn.configure(text="▶️ 继续识别")
                self.status_label.configure(text="已暂停")
            else:
                self.start_btn.configure(text="⏸️ 暂停识别")
                self.status_label.configure(text="正在识别中...")
    
    def _stop_recognition(self):
        """停止识别"""
        if self.is_running:
            self.is_running = False
            self.is_paused = False
            self.start_btn.configure(text="▶️ 开始识别", fg_color=("gray75", "gray25"))
            self.stop_btn.configure(state="disabled", fg_color=("gray75", "gray25"))
            self.select_btn.configure(state="normal")
            self.status_label.configure(text="识别已停止")
    
    def _recognition_loop(self):
        """识别循环（在独立线程中运行）"""
        with ScreenshotCapture() as capture:
            while self.is_running:
                if not self.is_paused and self.monitor_region:
                    try:
                        # 截取指定区域
                        img = capture.capture_region(self.monitor_region)
                        if img and self.ocr_engine:
                            # 识别文字
                            text = self.ocr_engine.recognize(img)
                            if text:
                                self.subtitle_manager.add_subtitle(text)
                    except Exception as e:
                        error_msg = f"识别错误: {e}"
                        print(error_msg)
                        self.root.after(0, lambda: self.status_label.configure(text=error_msg))
                
                time.sleep(Config.RECOGNITION_INTERVAL)
        
        # 循环结束，恢复按钮状态
        self.root.after(0, self._recognition_stopped)
    
    def _recognition_stopped(self):
        """识别停止后的UI更新"""
        self.start_btn.configure(text="▶️ 开始识别", fg_color=("gray75", "gray25"))
        self.stop_btn.configure(state="disabled", fg_color=("gray75", "gray25"))
        self.select_btn.configure(state="normal")
        self.status_label.configure(text="识别已停止")
    
    def _on_subtitle_added(self, text: str, timestamp: str):
        """字幕添加回调（在UI线程中调用）"""
        self.root.after(0, lambda: self._update_subtitle_display(text, timestamp))
    
    def _update_subtitle_display(self, text: str, timestamp: str):
        """更新字幕显示"""
        self.subtitle_text.insert("end", f"[{timestamp}] {text}\n\n")
        self.subtitle_text.see("end")
        self.count_label.configure(text=f"({self.subtitle_manager.get_count()} 条)")
        self.status_label.configure(text=f"已识别 {self.subtitle_manager.get_count()} 条字幕")
    
    def _clear_subtitles(self):
        """清空字幕列表"""
        if messagebox.askyesno("确认", "确定要清空所有字幕吗？"):
            self.subtitle_manager.clear()
            self.subtitle_text.delete("1.0", "end")
            self.count_label.configure(text="(0 条)")
            self.status_label.configure(text="列表已清空")
    
    def _copy_all(self):
        """复制所有字幕"""
        if self.subtitle_manager.get_count() == 0:
            messagebox.showinfo("提示", "没有可复制的内容")
            return
        
        import pyperclip
        text = self.subtitle_manager.get_all_text()
        pyperclip.copy(text)
        messagebox.showinfo("成功", f"已复制 {self.subtitle_manager.get_count()} 条字幕到剪贴板")
        self.status_label.configure(text="字幕已复制到剪贴板")
    
    def _export_subtitles(self):
        """导出字幕到文件"""
        if self.subtitle_manager.get_count() == 0:
            messagebox.showinfo("提示", "没有可导出的内容")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("文本文件", "*.txt"),
                ("字幕文件", "*.srt"),
                ("所有文件", "*.*")
            ],
            title="保存字幕文件"
        )
        
        if filename:
            success = False
            if filename.endswith('.srt'):
                success = self.subtitle_manager.export_to_srt(filename)
            else:
                success = self.subtitle_manager.export_to_text(filename)
            
            if success:
                messagebox.showinfo("成功", f"字幕已导出到: {filename}")
                self.status_label.configure(text=f"已导出到: {filename}")
            else:
                messagebox.showerror("错误", "导出失败")

