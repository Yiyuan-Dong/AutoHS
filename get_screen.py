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
from autohs_logger import *

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

def test_battlenet_available():
    return get_battlenet_hwnd() != 0

def move_window_foreground(hwnd, name=""):
    try:
        win32gui.BringWindowToTop(hwnd)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        if name != "":
            logger.warning(f"Open {name}: {e}")
        else:
            logger.warning(e)

    win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)


def max_diff(img, pixel_list):
    ans = 0
    for pair in pixel_list:
        diff = abs(int(img[pair[0]][pair[1]][1]) -
                   int(img[pair[0]][pair[1]][0]))
        ans = max(ans, diff)
        # print(img[pair[0]][pair[1]])

    return ans

# This function used to take the snapshot of a specific process,
# but I found it does not work well now. So now it just take the
# snapshot of the frontend window.
def take_snapshot():
    width = WIDTH
    height = HEIGHT

    # Get the snapshot of the desktop
    hwnd = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    signedIntsArray = saveBitMap.GetBitmapBits(True)

    # Release the resources
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    im_opencv = numpy.frombuffer(signedIntsArray, dtype='uint8')
    im_opencv.shape = (height, width, 4)

    # Create a writable copy of the array
    im_opencv = im_opencv.copy()

    return im_opencv


def pixel_very_similar(im_opencv, y, x, expected_val):
    img_val = im_opencv[y][x][:3]

    diff = abs(img_val[0] - expected_val[0]) + \
           abs(img_val[1] - expected_val[1]) + \
           abs(img_val[2] - expected_val[2])

    if diff <= 3:
        return True

    return False

def get_state():
    hwnd = get_HS_hwnd()
    if hwnd == 0:
        return FSM_LEAVE_HS

    im_opencv = take_snapshot()

    if pixel_very_similar(im_opencv, 1070, 1090, [20, 51, 103]) or \
            pixel_very_similar(im_opencv, 305, 705, [21, 43, 95]):  # 万圣节主界面会变
        return FSM_MAIN_MENU
    elif pixel_very_similar(im_opencv, 1070, 1090, [8, 18, 24]):
        return FSM_CHOOSING_HERO
    elif pixel_very_similar(im_opencv, 1070, 1090, [17, 18, 19]):
        return FSM_MATCHING
    elif pixel_very_similar(im_opencv, 860, 960, [71, 71, 71]):
        return FSM_CHOOSING_CARD
    else:
        return FSM_BATTLING

def terminate_HS():
    hwnd = get_HS_hwnd()
    if hwnd == 0:
        return
    _, process_id = win32process.GetWindowThreadProcessId(hwnd)
    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, process_id)
    win32api.TerminateProcess(handle, 0)
    win32api.CloseHandle(handle)
