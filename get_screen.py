"""
主体代码引自 Demon_Hunter 的CSDN博客, 博客URL:https://blog.csdn.net/zhuisui_woxin/article/details/84345036
"""

import win32gui
import win32ui
import win32con
import win32com.client
import win32api
import win32process
import numpy
import pickle
import cv2
from print_info import *

from constants.constants import *


def get_HS_hwnd():
    hwnd = win32gui.FindWindow(None, "炉石传说")
    if hwnd != 0:
        return hwnd

    hwnd = win32gui.FindWindow(None, "《爐石戰記》")
    if hwnd != 0:
        return hwnd

    hwnd = win32gui.FindWindow(None, "Hearthstone")
    return hwnd


def get_battlenet_hwnd():
    hwnd = win32gui.FindWindow(None, "战网")
    if hwnd != 0:
        return hwnd

    hwnd = win32gui.FindWindow(None, "Battle.net")
    return hwnd


def test_hs_available():
    return get_HS_hwnd() != 0


def move_window_foreground(hwnd, name=""):
    try:
        win32gui.BringWindowToTop(hwnd)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        if name != "":
            warn_print(f"Open {name}: {e}")
        else:
            warn_print(e)

    win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)


def max_diff(img, pixel_list):
    ans = 0
    for pair in pixel_list:
        diff = abs(int(img[pair[0]][pair[1]][1]) -
                   int(img[pair[0]][pair[1]][0]))
        ans = max(ans, diff)
        # print(img[pair[0]][pair[1]])

    return ans


def catch_screen(name=None):
    # 第一个参数是类名，第二个参数是窗口名字
    # hwnd -> Handle to a Window !
    # 如果找不到对应名字的窗口，返回0
    if name is not None:
        hwnd = win32gui.FindWindow(None, name)
    else:
        hwnd = get_HS_hwnd()

    if hwnd == 0:
        return

    width = 1960
    height = 1080
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框 DC device context
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    signedIntsArray = saveBitMap.GetBitmapBits(True)

    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    im_opencv = numpy.frombuffer(signedIntsArray, dtype='uint8')
    im_opencv.shape = (height, width, 4)

    return im_opencv


def get_state():
    hwnd = get_HS_hwnd()
    if hwnd == 0:
        return FSM_LEAVE_HS

    im_opencv = catch_screen()

    # 先y轴再x轴
    if list(im_opencv[1070][1090][:3]) == [23, 52, 105] or \
            list(im_opencv[305][705][:3]) == [21, 43, 95]:  # 万圣节主界面会变
        return FSM_MAIN_MENU
    if list(im_opencv[305][705][:3]) == [119, 122, 145]:  # 佣兵模式的营地
        return FSM_MERC_CAMP
    if list(im_opencv[305][705][:3]) == [242, 261, 181]:  # 选地图界面贫瘠之地
        return FSM_MERC_CHOOSE_MAP_1
    if list(im_opencv[305][705][:3]) == [44, 64, 39]:  # 选地图界面费伍德森林
        return FSM_MERC_CHOOSE_MAP_2
    if list(im_opencv[305][705][:3]) == [97, 46, 71]:  # 选地图界面冬泉谷
        return FSM_MERC_CHOOSE_MAP_3
    if list(im_opencv[305][705][:3]) == [44, 94, 205]:  # 选地图界面黑石山
        return FSM_MERC_CHOOSE_MAP_4
    if list(im_opencv[305][705][:3]) in [[47, 84, 117], [79, 128, 163]]:  # 选具体关卡
        return FSM_MERC_CHOOSE_COURSE
    if list(im_opencv[205][705][:3]) == [54, 97, 150]:  # 选择一支队伍
        return FSM_MERC_CHOOSE_TEAM
    if list(im_opencv[1005][705][:3]) == [159, 188, 217]:
        # 进入具体关卡但还没打, (705, 1005)对应`查看队伍`
        return FSM_MERC_ENTER_BATTLE
    if sum(abs(im_opencv[505][305][:3] - [86, 124, 111])) < 10:  # 进入战斗界面了, 这个点是状态栏白边
        return FSM_MERC_BATTLING
    if list(im_opencv[855][1205][:3]) == [141, 141, 141]:
        return FSM_MERC_CHOOSE_TREASURE
    if list(im_opencv[1070][1090][:3]) == [8, 18, 24]:
        return FSM_CHOOSING_HERO
    if list(im_opencv[1070][1090][:3]) == [17, 18, 19]:
        return FSM_MATCHING
    if list(im_opencv[860][960][:3]) == [71, 71, 71]:
        return FSM_CHOOSING_CARD

    return FSM_UNKNOWN
    # return FSM_BATTLING


def distingish_next_battle():
    im_opencv = catch_screen()

    digit_point = list(im_opencv[305][1505][:3])

    if digit_point == [126, 66, 63]:
        return BATTLE_BLESS_BLUE
    elif digit_point == [38, 151, 239]:
        return BATTLE_BLESS_RED
    elif digit_point == [181, 190, 198]:
        return BATTLE_BLESS_GREEN
    elif digit_point == [255, 187, 88]:
        return BATTLE_DOCTOR
    elif digit_point == [178, 119, 73]:
        return BATTLE_STRANGER
    elif digit_point == [136, 108, 44]:
        return BATTLE_DESTROY
    elif digit_point == [227, 65, 16]:
        return BATTLE_TELEPORT
    elif digit_point == [0, 4, 34]:
        return BATTLE_BOMB
    else:
        return BATTLE_NORMAL


# def image_hash(img):
#     img = Image.fromarray(img)
#     return imagehash.phash(img)
#
#
# def hash_diff(str1, str2):
#     return bin(int(str1, 16) ^ int(str2, 16))[2:].count("1")


def terminate_HS():
    hwnd = get_HS_hwnd()
    if hwnd == 0:
        return
    _, process_id = win32process.GetWindowThreadProcessId(hwnd)
    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, process_id)
    win32api.TerminateProcess(handle, 0)
    win32api.CloseHandle(handle)


def load_icon():
    with open("numpy_secret_icon", "rb") as f:
        return pickle.load(f)


def find_icon():
    img = catch_screen()
    template = load_icon()
    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return min_loc


def merc_can_battle():
    img = catch_screen()
    return list(img[810][1555][:3]) == [255, 255, 164]
