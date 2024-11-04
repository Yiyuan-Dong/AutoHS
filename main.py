from FSM_action import system_exit, AutoHS_automata
from log_state import check_name
from print_info import print_info_init
from FSM_action import init
import tkinter as tk
from tkinter import messagebox
from constants.constants import *
from config import *
import os
import keyboard


def is_integer(s):
    try:
        num = int(s)
        return num
    except ValueError:
        messagebox.showinfo("Warning", "请输入整数")
        return None

def check_hearthstone_path(path):
    if not os.path.exists(path):
        messagebox.showinfo("Warning", "炉石安装路径不存在")
        return False

    if not os.path.exists(os.path.join(path, "Hearthstone.exe")):
        messagebox.showinfo("Warning", "安装路径下未找到Hearthstone.exe")
        return False

    if not os.path.exists(os.path.join(path, "logs")):
        messagebox.showinfo("Warning", "安装路径下未找到logs文件夹")
        return False

    return True

def update_width(event):
    num = is_integer(entry_width.get())
    if num is not None:
        autohs_config.width = num

def update_height(event):
    num = is_integer(entry_height.get())
    if num is not None:
        autohs_config.height = num

def update_max_play_time(event):
    num = is_integer(entry_max_play_time.get())
    if num is not None:
        autohs_config.max_play_time = num

def update_max_win_count(event):
    num = is_integer(entry_max_win_count.get())
    if num is not None:
        autohs_config.max_win_count = num

def update_install_path(event):
    path = entry_path.get()
    if (check_hearthstone_path(path)):
        autohs_config.hearthstone_install_path = entry_path.get()

def update_player_name(event):
    autohs_config.player_name = entry_player_name.get()

def start_function():
    autohs_config.is_running = True

    check_name()
    print_info_init()
    init()
    AutoHS_automata()

def mock_start_function():
    # 创建一个隐藏的主窗口
    autohs_config.is_running = True

    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 弹出提示框
    messagebox.showinfo("Mock Function", "Mock function called. No actual functionality executed. Entry: {}".format(entry.get()))

    # 销毁主窗口
    root.destroy()

def close_window():
    if autohs_config.is_running:
        system_exit()
    root.quit()
    root.destroy()

def check_before_start():
    if autohs_config.is_running:
        messagebox.showinfo("Warning", "程序已在运行中，请勿重复启动。")
        return False

    if autohs_config.hearthstone_install_path == "":
        messagebox.showinfo("Warning", "请先设置炉石安装路径")
        return False

    if not check_hearthstone_path(autohs_config.hearthstone_install_path):
        return False

    if (autohs_config.width == 0 or autohs_config.height == 0):
        messagebox.showinfo("Warning", "请先设置屏幕分辨率")
        return False

    if autohs_config.max_win_count == 0 and autohs_config.max_play_time == 0:
        messagebox.showinfo("Warning", "警告：程序将无限制运行，可能导致账号被封。")

    mock_start_function()
    # start_function()

def add_label_and_entry(root, label_text, entry_text, bind_func):
    if not hasattr(add_label_and_entry, "row"):
        add_label_and_entry.row = 0
    else:
        add_label_and_entry.row += 1

    label = tk.Label(root, text=label_text)
    label.grid(row=add_label_and_entry.row, column=0, padx=10, pady=5, sticky="w")
    entry = tk.Entry(root, width=20)
    entry.grid(row=add_label_and_entry.row, column=1, padx=10, pady=5, sticky="w")
    entry.insert(0, entry_text)
    entry.bind("<Return>", bind_func)

    return entry

if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+q", close_window)

    autohs_config = AutoHSConfig()
    if autohs_config.width == 0:
        autohs_config.width = WIDTH
    if autohs_config.height == 0:
        autohs_config.height = HEIGHT

    root = tk.Tk()
    root.title("AutoHS GUI")
    root.geometry("500x300")
    root.protocol("WM_DELETE_WINDOW", close_window)

    entry_width = add_label_and_entry(root, "游戏水平像素数：", autohs_config.width, update_width)
    entry_height = add_label_and_entry(root, "游戏垂直像素数：", autohs_config.height, update_height)
    entry_max_play_time = add_label_and_entry(root, "最大游戏时间(分钟)：", autohs_config.max_play_time, update_max_play_time)
    entry_max_win_count = add_label_and_entry(root, "最大胜利场次：", autohs_config.max_win_count, update_max_win_count)
    entry_path = add_label_and_entry(root, "炉石安装路径：\n(例：D:\\Hearthstone)", autohs_config.hearthstone_install_path, update_install_path)
    entry_player_name = add_label_and_entry(root, "玩家名：", autohs_config.player_name, update_player_name)

    start_button = tk.Button(root, text="开始", command=check_before_start, width=20, height=1)
    start_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

    exit_button = tk.Button(root, text="退出", command=root.quit, width=20, height=1)
    exit_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")

    load_button = tk.Button(root, text="加载配置", command=autohs_config.load_config, width=20, height=1)
    load_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

    save_button = tk.Button(root, text="保存配置", command=autohs_config.save_config, width=20, height=1)
    save_button.grid(row=3, column=2, padx=10, pady=10, sticky="e")

    root.mainloop()