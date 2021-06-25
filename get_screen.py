"""
主体代码引自 Demon_Hunter 的CSDN博客, 博客URL:https://blog.csdn.net/zhuisui_woxin/article/details/84345036
"""

import win32gui
import win32ui
import win32con
import win32api
import cv2
import time
import FSM_action
import time
import numpy
import imagehash
from PIL import Image
from pynput.mouse import Button, Controller
from constants.constants import *
from constants.hash_vals import *

step = STEP
start = START


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
    # hwnd -> Handle to a Window !
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
        return FSM_action.STRING_NOTMYTURN
    else:
        return FSM_action.STRING_MYTURN


def test_card_with_x(img, x, step, show_img=False):
    left_part = img[600:800, x - 100 - step: x + 100 - step]
    right_part = img[600:800, x - 100:x + 100]

    if show_img:
        cv2.imshow("left", left_part)
        cv2.imshow("right", right_part)
        cv2.waitKey()

    return left_part[:, :, :3], right_part[:, :, :3]


def image_hash(img):
    img = Image.fromarray(img)
    return imagehash.phash(img)


def get_card_hash(total_num, index):
    mouse = Controller()

    x1 = start[total_num] + index * step[total_num]
    x2 = start[total_num] + index * step[total_num] + 200
    mouse_pos = (x1 + 65, 1000)

    mouse.position = mouse_pos
    time.sleep(CARD_APPEAR_INTERVAL)
    img = catch_screen()

    card_img = img[600:800, x1:x2, ]

    # cv2.imshow("test", card_img)
    # cv2.waitKey()

    return image_hash(card_img)


def count_my_cards():
    res_list = [count_my_cards_epoch(), count_my_cards_epoch()]

    while not res_list[-2] == res_list[-1] and len(res_list) < 10:
        res_list.append(count_my_cards_epoch())

    return res_list[-1]


def count_my_cards_epoch():
    mouse = Controller()
    last_part = numpy.zeros((200, 200, 3))
    last_part = last_part.astype(numpy.uint8)
    count = 0

    step = 30
    for x in range(590, 1281, step):
        mouse.position = (x, 1030)

        # 必须睡眠一小会儿,否则手牌详情还没跳出来就开始了截图
        time.sleep(CARD_APPEAR_INTERVAL)

        img = catch_screen()

        left_part, right_part = test_card_with_x(img, x, step)

        last_image = Image.fromarray(last_part)
        last_hash = imagehash.phash(last_image)
        curr_image = Image.fromarray(left_part)
        curr_hash = imagehash.phash(curr_image)

        # 使用图片哈希去判断上一个位置的右图片与当前位置的左图片是否一样,
        # 如果哈希值很接近,认为这是来自同一张卡牌的,否则认为有两张牌
        if last_hash - curr_hash > 18:
            count += 1

        last_part = right_part

    cv2.destroyAllWindows()

    # print(count - 2)
    # 减二因为: 从0矩阵到棋盘背景会加一; 从最后一张图到棋盘背景也会加一
    return count - 2


def count_minions():
    img = catch_screen()
    img = cv2.GaussianBlur(img, (3, 3), 0)
    canny = cv2.Canny(img, 50, 150)

    flag_opponent = 0
    for i in range(7, 0, -1):
        baseline = 960 - i * 70
        part_canny = canny[390:490, baseline:baseline + 40]
        if sum(sum(part_canny > 0)) > 100:
            flag_opponent = i
            break

    flag_mine = 0
    for i in range(7, 0, -1):
        baseline = 960 - i * 70
        part_canny = canny[510:610, baseline:baseline + 40]
        if sum(sum(part_canny > 0)) > 100:
            flag_mine = i
            break

    return flag_opponent, flag_mine


def hash_diff(str1, str2):
    return bin(int(str1, 16) ^ int(str2, 16))[2:].count("1")


def identify_cards(card_num):
    area_list = [((start[card_num] + step[card_num] * i, 600),
                  (start[card_num] + 200 + step[card_num] * i, 800),
                  (start[card_num] + 65 + step[card_num] * i, 1000)
                  ) for i in range(card_num)]

    result = []
    mouse = Controller()

    for i in range(len(area_list)):
        area = area_list[i]
        top_left, bottom_right, mouse_pos = area
        mouse.position = mouse_pos
        time.sleep(CARD_APPEAR_INTERVAL)

        card_hash = get_card_hash(card_num, i)
        min_diff = 64
        name = ""
        for k, v in CARD_HASH_INFO.items():
            temp_diff = hash_diff(k, str(card_hash))
            if temp_diff < min_diff:
                min_diff = temp_diff
                name = v

        result.append(name)

    return result


# 输入的彩色攻击/血量数字图,返回黑白的数字图片.
# 可以识别纯红色受伤血量和纯绿色buff过的数值
def try_get_number_in_img(img, threshold):
    grey_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    green_mask = cv2.inRange(img, (0, threshold, 0, 255), (0, 255, 0, 255))
    red_mask = cv2.inRange(img, (0, 0, threshold, 255), (0, 0, 255, 255))
    _, ret_img = cv2.threshold(grey_img, threshold, 255, cv2.THRESH_BINARY)
    ret_img = ret_img + red_mask + green_mask

    return ret_img


def health_attack_number_in_img(img):
    ret_img = try_get_number_in_img(img, 254)
    if sum(sum(ret_img == 255)) < 20:
        ret_img = try_get_number_in_img(img, 200)
    if sum(sum(ret_img == 255)) < 20:
        ret_img = try_get_number_in_img(img, 180)
    return ret_img
