from FSM_action import system_exit, AutoHS_automata
import keyboard
from log_state import check_name
from print_info import print_info_init
from FSM_action import init
import tkinter as tk
from tkinter import messagebox

class GUI_config:
    def __init__(self):
        self.is_running = False

def start_functions():
    gui_config.is_running = True

    check_name()
    print_info_init()
    init()
    AutoHS_automata()

def mock_start_functions():
    # 创建一个隐藏的主窗口
    gui_config.is_running = True

    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 弹出提示框
    messagebox.showinfo("Mock Function", "Mock function called. No actual functionality executed. Entry: {}".format(entry.get()))

    # 销毁主窗口
    root.destroy()

def close_window():
    if gui_config.is_running:
        system_exit()
    root.quit()
    root.destroy()

if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+q", close_window)

    gui_config = GUI_config()

    # 创建主窗口
    root = tk.Tk()
    root.title("AutoHS GUI")

    # 设置主窗口大小
    root.geometry("600x300")  # 宽400，高300

    # 绑定窗口关闭事件
    root.protocol("WM_DELETE_WINDOW", close_window)

    # 创建并放置显示文字的文本框
    label = tk.Label(root, text="请输入数字：")
    label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    # 创建并放置输入框
    entry = tk.Entry(root, width=20)
    entry.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    # 创建并放置“开始”按钮
    start_button = tk.Button(root, text="开始", command=mock_start_functions, width=20, height=2)
    start_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

    # 创建并放置“退出”按钮
    exit_button = tk.Button(root, text="退出", command=root.quit, width=20, height=2)
    exit_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

    # 运行主循环
    root.mainloop()