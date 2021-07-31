"""
主体代码引自 Demon_Hunter 的CSDN博客, 博客URL:https://blog.csdn.net/zhuisui_woxin/article/details/84345036
"""

import win32gui
import win32ui
import win32con
import win32api
import win32process
import numpy
import imagehash
from PIL import Image

from constants.constants import *

step = STEP
start = START


def test_hs_available():
    return win32gui.FindWindow(None, "炉石传说") != 0


def max_diff(img, pixel_list):
    ans = 0
    for pair in pixel_list:
        diff = abs(int(img[pair[0]][pair[1]][1]) -
                   int(img[pair[0]][pair[1]][0]))
        ans = max(ans, diff)
        # print(img[pair[0]][pair[1]])

    return ans


def catch_screen(name="炉石传说"):
    # 第一个参数是类名，第二个参数是窗口名字
    # hwnd -> Handle to a Window !
    # 如果找不到对应名字的窗口，返回0
    hwnd = win32gui.FindWindow(None, name)
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
    hwnd = win32gui.FindWindow(None, "炉石传说")
    if hwnd == 0:
        return FSM_LEAVE_HS

    im_opencv = catch_screen()

    if list(im_opencv[1070][1090]) == [23, 52, 105, 255]:
        return FSM_MAIN_MENU
    if list(im_opencv[1070][1090]) == [8, 18, 24, 255]:
        return FSM_CHOOSING_HERO
    if list(im_opencv[1070][1090]) == [17, 18, 19, 255]:
        return FSM_MATCHING
    if list(im_opencv[860][960]) == [71, 71, 71, 255]:
        return FSM_CHOOSING_CARD

    return FSM_BATTLING


def image_hash(img):
    img = Image.fromarray(img)
    return imagehash.phash(img)


def hash_diff(str1, str2):
    return bin(int(str1, 16) ^ int(str2, 16))[2:].count("1")


def terminate_HS():
    hwnd = win32gui.FindWindow(None, "炉石传说")
    _, process_id = win32process.GetWindowThreadProcessId(hwnd)
    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, process_id)
    win32api.TerminateProcess(handle, 0)
    win32api.CloseHandle(handle)


if __name__ == "__main__":
    print(get_state())
