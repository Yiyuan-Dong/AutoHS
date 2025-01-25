"""
主体代码引自 Demon_Hunter 的CSDN博客, 博客URL:https://blog.csdn.net/zhuisui_woxin/article/details/84345036
"""
import sys
import cv2
import time
import math
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import window_utils
from constants.pixel_coordinate import *
from autohs_logger import *


PRINT_ALL_AREA_LIST = []
AREA_LIST = []
POINT_LIST = []


def get_sum(x):
    return int(x[0]) + int(x[1]) + int(x[2])


def add_line(img, width, height):
    for i in range(1, math.floor(width / 100) + 1):
        cv2.line(img, pt1=(i * 100, 0), pt2=(i * 100, height), color=(200, 200, 200), thickness=1)
        cv2.putText(img, str(i * 100), (i * 100 - 30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

    for i in range(1, math.floor(height / 100) + 1):
        cv2.line(img, pt1=(0, i * 100), pt2=(width, i * 100), color=(200, 200, 200), thickness=1)
        cv2.putText(img, str(i * 100), (0, i * 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

    return img


def add_point(img, point_list):
    for pair in point_list:
        print(str(pair) + " has color: " + str(img[pair[1]][pair[0]]))
        cv2.circle(img, pair, 1, (255, 0, 0), 2, 0)


def show_area(img, top_left, bottom_right, print_out=False):
    x1, y1 = top_left
    x2, y2 = bottom_right
    tmp_img = img[y1:y2, x1:x2]
    tmp_img = tmp_img.copy()

    if print_out:
        count = 0
        for line in tmp_img:
            for pixel in line:
                if pixel[1] > 230:
                    count += 1
        print(count)

    ratio = min(round(800 / (x2 - x1)), round(500 / (y2 - y1)))
    resized_x_length = (x2 - x1) * int(ratio)
    resized_y_length = int(resized_x_length * ((y2 - y1) / (x2 - x1)))
    tmp_img = cv2.resize(tmp_img, (resized_x_length, resized_y_length))

    font_size = int(ratio) / 8
    for x in range(x1, x2, 10):
        temp_x = int(resized_x_length / (x2 - x1) * (x - x1))
        cv2.line(tmp_img, pt1=(temp_x, 0), pt2=(temp_x, resized_y_length), color=(200, 200, 200), thickness=1)
        cv2.putText(tmp_img, str(x), (temp_x, 10), cv2.FONT_HERSHEY_COMPLEX, font_size, (0, 0, 255), 1)

    for y in range(y1, y2, 10):
        temp_y = int(resized_y_length * (y - y1) / (y2 - y1))
        cv2.line(tmp_img, pt1=(0, temp_y), pt2=(resized_x_length, temp_y), color=(200, 200, 200), thickness=1)
        cv2.putText(tmp_img, str(y), (0, temp_y + 5), cv2.FONT_HERSHEY_COMPLEX, font_size, (0, 255, 0), 1)

    cv2.imshow("area", tmp_img)
    cv2.waitKey(0)
    cv2.destroyWindow("area")

def simplify_image(image):
    # 将图像转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 使用高斯模糊来平滑图像
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    # 使用Canny边缘检测来提取图像的轮廓
    edges = cv2.Canny(blurred_image, 50, 150)
    # 将边缘图像转换回BGR格式
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    return edges_colored

def compare_images(imageA, imageB):
    # 计算结构相似性
    s = ssim(imageA, imageB, multichannel=True, channel_axis = 2)
    return s

if __name__ == "__main__":
    logger_init("DEBUG")

    if window_utils.test_hs_available():
        window_utils.move_window_foreground(window_utils.get_HS_hwnd(), "炉石传说")
    else:
        print("未找到炉石传说")
        exit()

    time.sleep(0.4)

    im_opencv = window_utils.take_snapshot()
    if im_opencv is None:
        print("截图失败")
        sys.exit(-1)

    # 检查图像是否有四个通道（包括 alpha 通道）
    if im_opencv.shape[2] == 4:
        # 将四通道图像转换为三通道 BGR 图像
        im_opencv = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2BGR)

    print(f"图片尺寸: {im_opencv.shape}")

    print("Current state: {}".format(window_utils.get_state()))

    add_line(im_opencv, WIDTH, HEIGHT)
    add_point(im_opencv, POINT_LIST)

    cv2.imshow("Full Screen", im_opencv)  # 显示
    cv2.waitKey(0)
    try:
        cv2.destroyWindow("Full Screen")
    except cv2.error as e:
        print(f"Error destroying window: {e}")

    cv2.waitKey(0)

    for area in AREA_LIST:
        if len(area) < 2 or len(area) > 3:
            print("[Usage]: ((left-top), (botton-right), [mouse-position])")
        top_left, bottom_right = area
        show_area(im_opencv, top_left, bottom_right)

    for area in PRINT_ALL_AREA_LIST:
        if len(area) < 2 or len(area) > 3:
            print("[Usage]: ((left-top), (botton-right), [mouse-position])")
        top_left, bottom_right = area
        show_area(im_opencv, top_left, bottom_right, print_out=True)

    cv2.destroyAllWindows()