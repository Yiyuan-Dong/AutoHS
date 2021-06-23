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
import math
from pynput.mouse import Button, Controller

WIDTH = 1920

HEIGHT = 1080
NAME = "炉石传说"
POINT_LIST = [(1560, 510)]
AREA_LIST = [((1500, 470), (1580, 530))]


def get_sum(x):
    return int(x[0]) + int(x[1]) + int(x[2])


def add_line(img, width, height):
    for i in range(1, math.floor(width / 100) + 1):
        cv2.line(img, pt1=(i * 100, 0), pt2=(i * 100, height), color=(200, 200, 200), thickness=1)
        cv2.putText(img, str(i * 100), (i * 100 - 30, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

    for i in range(1, math.floor(height / 100) + 1):
        cv2.line(img, pt1=(0, i * 100), pt2=(width, i * 100), color=(200, 200, 200), thickness=1)
        cv2.putText(img, str(i * 100), (0, i * 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

    return img


def add_point(img, point_list):
    for pair in point_list:
        print(str(pair) + " has color: " + str(img[pair[1]][pair[0]]))
        cv2.circle(img, pair, 1, (255, 0, 0), 2, 0)


def show_area(img, left_top, right_bottom):
    x1, y1 = left_top
    x2, y2 = right_bottom
    tmp_img = img[y1:y2, x1:x2]
    tmp_img = tmp_img.copy()
    resized_x_length = (x2 - x1) * 10
    resized_y_length = int(resized_x_length * ((y2 - y1) / (x2 - x1)))
    tmp_img = cv2.resize(tmp_img, (resized_x_length, resized_y_length))

    for x in range(x1, x2, 10):
        temp_x = int(resized_x_length / (x2 - x1) * (x - x1))
        cv2.line(tmp_img, pt1=(temp_x, 0), pt2=(temp_x, resized_y_length), color=(200, 200, 200), thickness=1)
        cv2.putText(tmp_img, str(x), (temp_x - 20, 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)

    for y in range(y1, y2, 10):
        temp_y = int(resized_y_length * (y - y1) / (y2 - y1))
        cv2.line(tmp_img, pt1=(0, temp_y), pt2=(resized_x_length, temp_y), color=(200, 200, 200), thickness=1)
        cv2.putText(tmp_img, str(y), (0, temp_y + 5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)

    # cv2.imshow("im_opencv_3", tmp_img)
    # cv2.waitKey(0)


def main():
    # 第一个参数是类名，第二个参数是窗口名字
    # hwnd -> Handle to a Window !
    hwnd = win32gui.FindWindow(None, NAME)
    if hwnd == 0:
        return "wtf"
    width = WIDTH
    height = HEIGHT
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

    add_line(im_opencv, 1920, 1080)
    add_point(im_opencv, POINT_LIST)

    cv2.imshow("im_opencv", im_opencv)  # 显示
    cv2.waitKey(0)

    for area in AREA_LIST:
        top_left, right_bottom = area
        show_area(im_opencv, top_left, right_bottom)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
