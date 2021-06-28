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
from print_info import *
import click
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
    # 3.结束回合(绿): 像素值为(0~, 100+, 20+)
    # 4.对手回合: 像素值为(70+, 90+, 100~)
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
    # res_list = [count_my_cards_epoch(), count_my_cards_epoch()]
    #
    # while not res_list[-2] == res_list[-1] and len(res_list) < 10:
    #     res_list.append(count_my_cards_epoch())
    #
    # return res_list[-1]
    return count_my_cards_epoch()


def count_my_cards_epoch():
    mouse = Controller()
    last_part = numpy.zeros((200, 200, 3))
    last_part = last_part.astype(numpy.uint8)
    count = 0

    step = 30
    for x in range(590, 1281, step):
        mouse.position = (x, 1050)

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
    if count == 1:
        return 0
    return count - 2


def count_minions(img):
    gauss_img = cv2.GaussianBlur(img, (3, 3), 0)
    canny = cv2.Canny(gauss_img, 50, 150)

    flag_opponent = 0
    for i in range(7, 0, -1):
        baseline = 960 - i * 70
        part_canny = canny[390:490, baseline:baseline + 40]
        # print(sum(sum(part_canny > 0)))
        if sum(sum(part_canny > 0)) > 400:
            flag_opponent = i
            break

    flag_mine = 0
    for i in range(7, 0, -1):
        baseline = 960 - i * 70
        part_canny = canny[510:610, baseline:baseline + 40]
        # print(sum(sum(part_canny > 0)))
        if sum(sum(part_canny > 0)) > 100:
            flag_mine = i
            break

    return flag_opponent, flag_mine


def hash_diff(str1, str2):
    return bin(int(str1, 16) ^ int(str2, 16))[2:].count("1")


def identify_cards(card_num):
    if card_num > 10:
        warning_print(f"Invalid card unm {card_num}")
        card_num = 10

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

    click.cancel_click()
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
    if sum(sum(ret_img == 255)) < 80:
        ret_img = try_get_number_in_img(img, 230)
    if sum(sum(ret_img == 255)) < 80:
        ret_img = try_get_number_in_img(img, 200)
    if sum(sum(ret_img == 255)) < 80:
        ret_img = try_get_number_in_img(img, 180)
    return ret_img


def test_taunt(img, oppo_num, mine_num):
    oppo_baseline = 960 - 70 * (oppo_num - 1)
    mine_baseline = 960 - 70 * (mine_num - 1)

    oppo_res = []
    mine_res = []

    def test_card(card_part):
        count = 0
        for line in card_part:
            for pixel in line:
                # 有时会出现这种像素,在图上表现为一条意义不明的白线
                # 猜测是炉石游戏画面放缩时搞出来的问题
                if pixel[0] == pixel[1] == pixel[2]:
                    continue
                # 因为红色佳绿色会变成黄色,而炉石棋盘背景色是黄的,所以
                # 绿色色素(pixel[1])会比蓝色色素(pixel[0])要多,但是
                # 如果是嘲讽随从,会多出一圈灰色的边框,这个边框上三种像素
                # 较为平均
                # print(pixel[1], pixel[0])
                if int(pixel[1]) - int(pixel[0]) < 25:
                    count += 1
        # print(count)
        return count >= 5

    for i in range(oppo_num):
        card_baseline = oppo_baseline + 140 * i
        tmp = img[337:340, card_baseline - 53: card_baseline - 50]
        oppo_res.append(test_card(tmp))

    for i in range(mine_num):
        card_baseline = mine_baseline + 140 * i
        tmp = img[525:528, card_baseline - 53: card_baseline - 50]
        mine_res.append(test_card(tmp))

    return oppo_res, mine_res


def test_divine_shield():
    # 为什么要搞个循环呢,因为光环(比如团队领袖的加攻光环)也是黄色的,
    # 有时会影响圣盾的判断,所以多测几次,如果是光环的话不会每次都有光环
    img = catch_screen()
    oppo_num, mine_num = count_minions(img)
    oppo_res_1, mine_res_1 = test_divine_shield_epoch(img, oppo_num, mine_num)

    time.sleep(0.6)
    img = catch_screen()
    oppo_res_2, mine_res_2 = test_divine_shield_epoch(img, oppo_num, mine_num)

    time.sleep(0.6)
    img = catch_screen()
    oppo_res_3, mine_res_3 = test_divine_shield_epoch(img, oppo_num, mine_num)

    def combine(arr1, arr2, arr3):
        return [arr1[i] == arr2[i] == arr3[i] == True for i in range(len(arr1))]

    return combine(oppo_res_1, oppo_res_2, oppo_res_3), combine(mine_res_1, mine_res_2, mine_res_3)


def test_divine_shield_epoch(img, oppo_num, mine_num):
    oppo_baseline = 960 - 70 * (oppo_num - 1)
    mine_baseline = 960 - 70 * (mine_num - 1)

    oppo_res = []
    mine_res = []

    def test_pixel(pixel):
        # 圣盾是明黄色的,pixel[1]与pixel[0]差距很大
        return int(pixel[1]) - int(pixel[0]) > 80

    for i in range(oppo_num):
        card_baseline = oppo_baseline + i * 140
        # 这个点在攻击力的左边一点,选这个位置主要为了:
        # 1. 有圣盾是在圣盾里面
        # 2. 不在嘲讽框里面
        pixel = img[452, card_baseline - 60]
        oppo_res.append(test_pixel(pixel))

    for i in range(mine_num):
        card_baseline = mine_baseline + i * 140
        pixel = img[640, card_baseline - 60]
        mine_res.append(test_pixel(pixel))

    return oppo_res, mine_res


def find_closest(img_hash, hash_dict):
    min_diff = 64
    flag = -1
    for k, v in hash_dict.items():
        if hash_diff(k, str(img_hash)) < min_diff:
            min_diff = hash_diff(k, str(img_hash))
            flag = v

    return flag, min_diff


def get_attack_health(img, oppo, mine):
    steps_oppos = [0, 140, 140, 139, 139, 139, 139, 139]
    steps_mine = [0, 140, 140, 140, 140, 140, 140, 140]

    mine_baseline = 960 - int((mine - 1) * steps_mine[mine] / 2)
    oppo_baseline = 960 - int((oppo - 1) * steps_oppos[oppo] / 2)

    oppo_res = []
    mine_res = []

    for i in range(mine + oppo):
        if i < mine:
            baseline = mine_baseline + i * steps_mine[mine]
            attack_img = img[626:652, baseline - 47:baseline - 28]
            health_img = img[626:652, baseline + 29:baseline + 48]

        else:
            baseline = oppo_baseline + (i - mine) * steps_oppos[oppo]
            attack_img = img[438:464, baseline - 47:baseline - 28]
            health_img = img[438:464, baseline + 29:baseline + 48]

        grey_health_img = health_attack_number_in_img(health_img)
        grey_attack_img = health_attack_number_in_img(attack_img)

        attack_hash = image_hash(grey_attack_img)
        # print(f"attack: {attack_hash}, {find_closest(attack_hash, NUMBER_HASH)}")
        health_hash = image_hash(grey_health_img)
        # print(f"health: {health_hash}, {find_closest(health_hash, NUMBER_HASH)}")

        temp = (find_closest(attack_hash, NUMBER_HASH)[0], find_closest(health_hash, NUMBER_HASH)[0])

        if i < mine:
            mine_res.append(temp)
        else:
            oppo_res.append(temp)

    return oppo_res, mine_res


def test_available(img, mine_num):
    baseline = 960 - (mine_num - 1) * 70

    res = []
    for i in range(mine_num):
        card_baseline = baseline + 140 * i
        tmp_img = img[508:512, card_baseline - 20: card_baseline + 20]
        count = 0
        # 能动的随从都有绿色的边框,检测这个绿色的边框
        # 突袭绿色没有冲锋多
        for line in tmp_img:
            for pixel in line:
                if pixel[1] > 230:
                    count += 1
        # print(count)
        if count > 50:
            res.append(2)
        elif count > 30:
            res.append(1)
        else:
            res.append(0)

    return res
