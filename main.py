from controller.FSM_action import system_exit, AutoHS_automata
from controller.FSM_action import init
from tkinter import messagebox
from constants.pixel_coordinate import *
from config import *
from utils.window_utils import test_hs_available, test_battlenet_available, check_power_config, check_loading_screen_config
from utils.json_op import JSON_LAST_MODIFIED_TIME

ABNORMAL_WIDTH_HEIGHT_LIST = [(1707, 960), (2048, 1152), (1306, 720), (1536, 864)]
gui_is_running = False

def is_integer(s):
    try:
        num = int(s)
        return num
    except ValueError:
        messagebox.showinfo("Warning", "请输入整数")
        return None

def check_hearthstone_path(path):
    if PLATFORM == "Darwin":  # macOS
        # 在macOS上，炉石传说是一个应用程序包（.app）
        path = '/Applications/Hearthstone/Hearthstone.app'
        if not path.endswith(".app") and not os.path.exists(path):
            app_path = path if path.endswith(".app") else os.path.join(path, "Hearthstone.app")
            messagebox.showinfo("Warning", f"未找到炉石传说应用程序包: {app_path}")
            return False

        # 检查Logs文件夹路径
        logs_path = os.path.join(os.path.expanduser("/Applications/Hearthstone/Logs"))
        if not os.path.exists(logs_path):
            messagebox.showinfo("Warning", f"未找到炉石传说日志文件夹: {logs_path}")
            return False

        return True
    else:  # Windows 或其他平台
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

# def update_width(event):
#     num = is_integer(entry_width.get())
#     if num is not None:
#         autohs_config.width = num

# def update_height(event):
#     num = is_integer(entry_height.get())
#     if num is not None:
#         autohs_config.height = num

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
    autohs_config.user_name = entry_player_name.get()

def update_oppo_minion_delta_h_factor(event):
    num = None
    try:
        num = float(oppo_minion_delta_h_factor.get())
    except ValueError:
        messagebox.showinfo("Warning", "请输入浮点数")
        return None

    if num is not None:
        logger.info(f"设置 oppo_minion_delta_h_factor: {num}")
        autohs_config.oppo_minion_delta_h_factor = num

def update_oppo_hero_delta_h_factor(event):
    num = None
    try:
        num = float(oppo_hero_delta_h_factor.get())
    except ValueError:
        messagebox.showinfo("Warning", "请输入浮点数")
        return None

    if num is not None:
        logger.info(f"设置 oppo_hero_delta_h_factor: {num}")
        autohs_config.oppo_hero_delta_h_factor = num

def update_all():
    # update_width(None)
    # update_height(None)
    update_max_play_time(None)
    update_max_win_count(None)
    update_install_path(None)
    update_player_name(None)

def start_function():
    global gui_is_running
    gui_is_running = True

    init()
    AutoHS_automata()

def close_gui():
    global gui_is_running

    logger.info("关闭GUI")

    if gui_is_running:
        system_exit()

    # root.quit() will block until the main program exits
    root.quit()
    root.destroy()

    sys.exit(0)

def check_before_start():
    if not check_power_config():
        messagebox.showinfo("Warning", "未在炉石设置中找到Power.log相关配置，脚本无法运行")
        return False

    autohs_config.has_loading_screen = check_loading_screen_config()
    logger.info(f"has_loading_screen: {autohs_config.has_loading_screen}")

    if gui_is_running:
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

    if (autohs_config.user_name == ""):
        messagebox.showinfo("Warning", "请先设置玩家名")
        return False

    if not test_hs_available() and not test_battlenet_available():
        messagebox.showinfo("Warning", "未找到炉石传说或战网，请至少打开一个")
        return False

    if autohs_config.click_coordinates is None:
        messagebox.showinfo("Warning", "未找到对应分辨率的点击坐标")
        return False

    if autohs_config.max_win_count == 0 and autohs_config.max_play_time == 0:
        messagebox.showinfo("Warning", "警告：程序将无限制运行，可能导致账号被封。")

    start_function()

def add_label_and_entry(root, label_text, entry_text, bind_func):
    global next_text_row

    label = tk.Label(root, text=label_text)
    label.grid(row=next_text_row, column=0, padx=10, pady=5, sticky="ew")
    entry = tk.Entry(root, width=20)
    entry.grid(row=next_text_row, column=1, padx=10, pady=5, sticky="ew")
    entry.insert(0, entry_text)

    next_text_row += 1
    # entry.bind("<Leave>", bind_func)
    entry.bind("<Return>", bind_func)
    entry.bind("<Deactivate>", bind_func)

    return entry

def toggle_debug_log():
    if debug_button.config('text')[-1] == "调试日志：未启用":
        logger_init("DEBUG")
        autohs_config.debug_log_start = True
        debug_button.config(text="调试日志：已启用")
    else:
        logger_init("INFO")
        autohs_config.debug_log_start = False
        debug_button.config(text="调试日志：未启用")

def toggle_give_up_with_dignity():
    autohs_config.give_up_with_dignity = not autohs_config.give_up_with_dignity
    give_up_button.config(text=f"快攻智能投降：{'启用' if autohs_config.give_up_with_dignity else '未启用'}")


if __name__ == "__main__":
    if PLATFORM != "Darwin":  # macOS
        import keyboard
        keyboard.add_hotkey("ctrl+q", close_gui)

    logger_init()

    autohs_config.load_config()

    if autohs_config.debug_log_start:
        logger_init("DEBUG")

    autohs_config.exit_func = close_gui
    # if autohs_config.width == 0:
    #     autohs_config.width = WIDTH
    # if autohs_config.height == 0:
    #     autohs_config.height = HEIGHT
    autohs_config.width = WIDTH
    autohs_config.height = HEIGHT

    next_text_row = 0

    root = tk.Tk()
    root.title("AutoHS GUI")
    root.geometry("500x340")
    root.protocol("WM_DELETE_WINDOW", close_gui)

    # entry_width = add_label_and_entry(root, "游戏水平像素数：\n（不支持手动修改）", autohs_config.width, update_width)
    # entry_height = add_label_and_entry(root, "游戏垂直像素数：\n（不支持手动修改）", autohs_config.height, update_height)
    entry_max_play_time = add_label_and_entry(root, "最大游戏时间(分钟)：", autohs_config.max_play_time, update_max_play_time)
    entry_max_win_count = add_label_and_entry(root, "最大胜利场次：", autohs_config.max_win_count, update_max_win_count)
    entry_path = add_label_and_entry(root, "炉石安装路径：\n(例：D:\\Hearthstone)", autohs_config.hearthstone_install_path, update_install_path)
    entry_player_name = add_label_and_entry(root, "玩家名：", autohs_config.user_name, update_player_name)
    oppo_minion_delta_h_factor = add_label_and_entry(root, "解场相对权重：", autohs_config.oppo_minion_delta_h_factor, update_oppo_minion_delta_h_factor)
    oppo_hero_delta_h_factor = add_label_and_entry(root, "打脸相对权重：", autohs_config.oppo_hero_delta_h_factor, update_oppo_hero_delta_h_factor)

    start_button = tk.Button(root, text="开始", command=lambda: (update_all(), check_before_start()), width=20, height=1)
    start_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    exit_button = tk.Button(root, text="退出", command=close_gui, width=20, height=1)
    exit_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

    save_button = tk.Button(root, text="保存配置", command=lambda: (update_all(), autohs_config.save_config()), width=20, height=1)
    save_button.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

    if (WIDTH, HEIGHT) in ABNORMAL_WIDTH_HEIGHT_LIST:
        warning_label = tk.Label(root, text="警告：屏幕缩放比例疑似不为100%，\n可能导致程序异常", fg="red")
        warning_label.grid(row=next_text_row, column=0, padx=10, pady=5, sticky="ew")
    else:
        warning_label = tk.Label(root, text=f"屏幕像素数为{WIDTH}X{HEIGHT}", fg="gray")
        warning_label.grid(row=next_text_row, column=0, padx=10, pady=5, sticky="ew")

    if WIDTH == 1920 and HEIGHT == 1080:
        autohs_config.click_coordinates = COORDINATES_1920_1080
    elif WIDTH == 2560 and HEIGHT == 1440:
        autohs_config.click_coordinates = COORDINATES_2560_1440
    else:
        logger.error(f"未找到对应分辨率的点击坐标，当前分辨率为{WIDTH}X{HEIGHT}")

    hint_label = tk.Label(root, text="按Ctrl+Q可退出程序", fg="gray")
    hint_label.grid(row=next_text_row, column=2, padx=10, pady=5, sticky="ew")

    modified_time_label = tk.Label(root, text=f"cards.json最后更新时间：\n{JSON_LAST_MODIFIED_TIME}", fg="gray")
    modified_time_label.grid(row=next_text_row, column=1, padx=10, pady=5, sticky="ew")

    debug_button = tk.Button(root, text=f"调试日志：{'已启用' if autohs_config.debug_log_start else '未启用'}", command=toggle_debug_log, width=20, height=1)
    debug_button.grid(row=next_text_row + 1, column=2, padx=10, pady=10, sticky="ew")

    give_up_button = tk.Button(root, text=f"快攻智能投降：{'已启用' if autohs_config.give_up_with_dignity else '未启用'}", command=toggle_give_up_with_dignity, width=20, height=1)
    give_up_button.grid(row=next_text_row + 1, column=0, padx=10, pady=10, sticky="ew")

    root.mainloop()