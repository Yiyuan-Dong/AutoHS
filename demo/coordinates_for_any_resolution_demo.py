import win32gui

# Coordinates for any resolution

# 读取炉石传说窗口坐标信息
# 以 1920*1080 的操作点位为基准，先将基准点位缩放至与窗口相同的高度，再修正偏移量
# 理论上支持任意比例的分辨率
# 全屏或是窗口都可以，还能无视 Windows 的百分比缩放

# 但现在的问题是，关于界面状态的判断还是依赖于图像识别
# 也许 GameNetLogger.log + LoadingScreen.log 可以告别图像识别
# GameNetLogger.log 记录了从点击开始到匹配结束的过程
# LoadingScreen.log 记录了所处的界面

# 或者是将截图区域动态化，来匹配 1080p 标准图片

def get_hs_window_info():
    hwnd = win32gui.FindWindow(None, None)

    # 枚举所有窗口，找到标题包含炉石传说的窗口
    def enum_windows_callback(hwnd, result):
        title = win32gui.GetWindowText(hwnd)
        for hs_name in ["Hearthstone", "炉石传说", "《爐石戰記》"]:
            if hs_name in title and win32gui.IsWindowVisible(hwnd):
                result.append(hwnd)

    hwnds = []
    win32gui.EnumWindows(enum_windows_callback, hwnds)

    if not hwnds:
        print("未找到炉石传说的窗口")
        return

    hwnd = hwnds[0]  # 取第一个匹配的窗口
    client_rect = win32gui.GetClientRect(hwnd)  # 客户区相对左上角
    client_pos = win32gui.ClientToScreen(hwnd, (0, 0))  # 客户区左上角在屏幕上的坐标

    client_left, client_top = client_pos
    client_width = client_rect[2] - client_rect[0]
    client_height = client_rect[3] - client_rect[1]

    # 返回炉石传说宽度、高度、位置X、位置Y
    return client_width, client_height, client_left, client_top

def convert_value_to_int(data):
    if isinstance(data, dict):
        return {k: convert_value_to_int(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_value_to_int(i) for i in data]
    elif isinstance(data, tuple):
        return tuple(convert_value_to_int(i) for i in data)
    elif isinstance(data, float):
        return int(data)

    # 将浮点型转为整型
    return data

hs_width, hs_height, hs_x, hs_y = get_hs_window_info()
rate = hs_height / 1080  # 缩放倍率
new_width, new_height= 1920 * rate, hs_height
mid_x, mid_y = hs_x + hs_width / 2, hs_y + hs_height / 2
hs_x, hs_y = mid_x - new_width / 2, mid_y - new_height / 2  # 偏移量

COORDINATES_ANY = {
    'mid_x': hs_x+960*rate,
    'mid_y': hs_y+540*rate,
    'half_minion_gap_x': 70*rate,  # 格子间距不需要加 hs_x
    'my_minion_y': hs_y+600*rate,
    'oppo_minion_y': hs_y+400*rate,
    'my_hero_tuple_y': hs_y+850*rate,
    'oppo_hero_tuple_y': hs_y+200*rate,
    'cancel_x': hs_x+270*rate,  # 适当修改了取消点击位置的 x 轴坐标，以兼容4:3画面
    'cancel_y': hs_y+400*rate,
    'my_hand_x': [
        [],
        [hs_x+885*rate],
        [hs_x+820*rate, hs_x+980*rate],
        [hs_x+750*rate, hs_x+890*rate, hs_x+1040*rate],
        [hs_x+690*rate, hs_x+820*rate, hs_x+970*rate, hs_x+1130*rate],
        [hs_x+680*rate, hs_x+780*rate, hs_x+890*rate, hs_x+1010*rate, hs_x+1130*rate],
        [hs_x+660*rate, hs_x+750*rate, hs_x+840*rate, hs_x+930*rate, hs_x+1020*rate, hs_x+1110*rate],
        [hs_x+660*rate, hs_x+733*rate, hs_x+810*rate, hs_x+885*rate, hs_x+965*rate, hs_x+1040*rate, hs_x+1120*rate],
        [hs_x+650*rate, hs_x+720*rate, hs_x+785*rate, hs_x+855*rate, hs_x+925*rate, hs_x+995*rate, hs_x+1060*rate, hs_x+1130*rate],
        [hs_x+650*rate, hs_x+710*rate, hs_x+765*rate, hs_x+825*rate, hs_x+880*rate, hs_x+950*rate, hs_x+1010*rate, hs_x+1070*rate, hs_x+1140*rate],
        [hs_x+647*rate, hs_x+700*rate, hs_x+750*rate, hs_x+800*rate, hs_x+860*rate, hs_x+910*rate, hs_x+970*rate, hs_x+1020*rate, hs_x+1070*rate, hs_x+1120*rate],
    ],
    'my_hand_y': hs_y+1000*rate,
    'start_card_x': {3: [hs_x+600*rate, hs_x+960*rate, hs_x+1320*rate], 5: [hs_x+600*rate, hs_x+850*rate, hs_x+1100*rate, hs_x+1350*rate]},
    'start_card_y': hs_y+500*rate,
    'no_op_y': hs_y+500*rate,
    'main_menu_no_op_y': hs_y+525*rate,
    'setting_x': hs_x+hs_width-44*rate,  # 设置按钮一般在右下角
    'setting_y': hs_y+hs_height-24*rate,  # 设置按钮一般在右下角
    'match_opponent_x': hs_x+1400*rate,
    'match_opponent_y': hs_y+900*rate,
    'enter_battle_y': hs_y+320*rate,
    'commit_choose_start_card_y': hs_y+850*rate,
    'end_turn_x': hs_x+1550*rate,
    'end_turn_y': hs_y+500*rate,
    'error_report_x': hs_x+1100*rate,
    'error_report_y': hs_y+820*rate,
    'disconnected_x': hs_x+960*rate,
    'disconnected_y': hs_y+650*rate,
    'emoj_list': [(hs_x+800*rate, hs_y+880*rate), (hs_x+800*rate, hs_y+780*rate), (hs_x+800*rate, hs_y+680*rate), (hs_x+1150*rate, hs_y+680*rate), (hs_x+1150*rate, hs_y+780*rate)],
    'skill_x': hs_x+1150*rate,
    'skill_y': hs_y+850*rate,
    'battlefield_range_x': (hs_x+400*rate, hs_x+1700*rate),
    'battlefield_range_y': (hs_y+350*rate, hs_y+800*rate),
    'give_up_x': hs_x+960*rate,
    'give_up_y': hs_y+380*rate,
}

COORDINATES_ANY = convert_value_to_int(COORDINATES_ANY)  # 最后还是取个整吧

if __name__ == "__main__":
    print(COORDINATES_ANY)