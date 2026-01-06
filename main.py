#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GlotSub - 轻量级字幕自动识别工具
主入口文件
"""
import customtkinter as ctk
from tkinter import messagebox
from glotsub.ui.main_window import MainWindow
from glotsub.utils.config import Config


def main():
    """主函数"""
    # 设置 CustomTkinter 外观
    ctk.set_appearance_mode(Config.APPEARANCE_MODE)
    ctk.set_default_color_theme(Config.COLOR_THEME)
    
    # 创建主窗口
    root = ctk.CTk()
    app = MainWindow(root)
    
    # 运行主循环
    root.mainloop()


if __name__ == "__main__":
    main()
