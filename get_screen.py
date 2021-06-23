"""
主体代码引自 Demon_Hunter 的CSDN博客, 博客URL:https://blog.csdn.net/zhuisui_woxin/article/details/84345036
"""

import win32gui
import win32ui
import win32con
import win32api
import cv2
import numpy
import time
import FSM_action


def max_diff(img, pixel_list):
    ans = 0
    for pair in pixel_list:
        diff = abs(int(img[pair[0]][pair[1]][1]) -
                   int(img[pair[0]][pair[1]][0]))
        ans = max(ans, diff)
        # print(img[pair[0]][pair[1]])

    return ans


def catch_screen():
    # 第一个参数是类名，第二个参数是窗口名字
    hwnd = win32gui.FindWindow(None, "炉石传说")
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
        return FSM_action.STRING_LEAVEHS

    im_opencv = catch_screen()

    if list(im_opencv[1070][1090]) == [8, 18, 24, 255]:
        return FSM_action.STRING_CHOOSINGHERO
    if list(im_opencv[1070][1090]) == [17, 18, 19, 255]:
        return FSM_action.STRING_MATCHING
    if list(im_opencv[860][960]) == [71, 71, 71, 255]:
        return FSM_action.STRING_CHOOSINGCARD

    # 我觉得这里有必要解释一下
    # (1560, 510) / (1550, 510) 这两个点在 结束回合/对手回合 那个按钮的下方
    # 它大概有四种情况:
    # 像素值(B, G, R)
    # 1.卡牌特效/选牌阶段: 整个屏幕边缘都是灰暗的, 像素值约为 (30~, 30~, 30~)
    # 2.结束回合(黄): 像素值为(0~, 120+, 130+)
    # 3.结束回合(绿):像素值为(0~, 100+, 20+)
    # 4.对手回合:像素值为(70+, 90+, 100~)
    # 所以通过蓝像素与红像素的差值判断

    diff = max_diff(im_opencv, [(510, 1560), (510, 1550)])
    if diff < 50:
        return FSM_action.STRING_NOTMINE
    else:
        return FSM_action.STRING_MYTURN
