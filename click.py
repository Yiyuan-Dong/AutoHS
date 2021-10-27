import win32gui
import win32api
import win32con
import pywintypes
import time
from pynput.mouse import Button, Controller
import random
import sys

from constants.constants import *
from print_info import *
from get_screen import *


def rand_sleep(interval):
    base_time = interval * 0.75
    rand_time = interval * 0.5 * random.random()  # avg = 0.25 * interval
    time.sleep(base_time + rand_time)


def click_button(x, y, button):
    x += random.randint(-5, 5)
    y += random.randint(-5, 5)
    mouse = Controller()
    rand_sleep(0.1)
    mouse.position = (x, y)
    rand_sleep(0.1)
    mouse.press(button)
    rand_sleep(0.1)
    mouse.release(button)


def wheel_mouse(delta_y):
    y = delta_y // abs(delta_y)
    for i in range(delta_y):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, y)


def fast_click_button(x, y, button):
    x += random.randint(-5, 5)
    y += random.randint(-5, 5)
    mouse = Controller()
    rand_sleep(0.04)
    mouse.position = (x, y)
    rand_sleep(0.04)
    mouse.press(button)
    rand_sleep(0.04)
    mouse.release(button)


def left_click(x, y):
    click_button(x, y, Button.left)


def fast_left_click(x, y):
    fast_click_button(x, y, Button.left)


def right_click(x, y):
    click_button(x, y, Button.right)


def choose_my_minion(mine_index, mine_num):
    rand_sleep(OPERATE_INTERVAL)
    x = 960 - (mine_num - 1) * 70 + mine_index * 140
    y = 600
    left_click(x, y)


def choose_my_hero():
    rand_sleep(OPERATE_INTERVAL)
    left_click(960, 850)


def choose_opponent_minion(oppo_index, oppo_num):
    rand_sleep(OPERATE_INTERVAL)
    x = 960 - (oppo_num - 1) * 70 + oppo_index * 140
    y = 400
    left_click(x, y)


def choose_oppo_hero():
    rand_sleep(OPERATE_INTERVAL)
    left_click(960, 200)


def cancel_click():
    rand_sleep(TINY_OPERATE_INTERVAL)
    right_click(50, 400)


def test_click():
    rand_sleep(TINY_OPERATE_INTERVAL)
    left_click(50, 400)


HAND_CARD_X = [
    [],  # 0
    [885],  # 1
    [820, 980],  # 2
    [750, 890, 1040],  # 3
    [690, 820, 970, 1130],  # 4
    [680, 780, 890, 1010, 1130],  # 5
    [660, 750, 840, 930, 1020, 1110],  # 6
    [660, 733, 810, 885, 965, 1040, 1120],  # 7
    [650, 720, 785, 855, 925, 995, 1060, 1130],  # 8
    [650, 710, 765, 825, 880, 950, 1010, 1070, 1140],  # 9
    [647, 700, 750, 800, 860, 910, 970, 1020, 1070, 1120]  # 10
]


def choose_card(card_index, card_num):
    rand_sleep(OPERATE_INTERVAL)

    assert 0 <= card_index < card_num <= 10
    # x = START[card_num] + 65 + STEP[card_num] * card_index
    x = HAND_CARD_X[card_num][card_index]

    y = 1000
    left_click(x, y)


STARTING_CARD_X = {
    3: [600, 960, 1320],
    5: [600, 850, 1100, 1350],
}


def replace_starting_card(card_index, hand_card_num):
    assert hand_card_num in STARTING_CARD_X
    assert card_index < len(STARTING_CARD_X[hand_card_num])

    rand_sleep(OPERATE_INTERVAL)
    left_click(STARTING_CARD_X[hand_card_num][card_index], 500)


def click_middle():
    rand_sleep(OPERATE_INTERVAL)
    left_click(960, 500)


def click_setting():
    rand_sleep(OPERATE_INTERVAL)
    left_click(1880, 1050)


def click_give_up():
    click_setting()
    time.sleep(0.5)
    left_click(960, 380)
    test_click()

def choose_and_use_spell(card_index, card_num):
    choose_card(card_index, card_num)
    click_middle()


# 第[i]个随从左边那个空隙记为第[i]个gap
def put_minion(gap_index, minion_num):
    rand_sleep(OPERATE_INTERVAL)

    if minion_num >= 7:
        warn_print(f"Try to put a minion but there has already been {minion_num} minions")

    x = 960 - (minion_num - 1) * 70 + 140 * gap_index - 70
    y = 600
    left_click(x, y)


def match_opponent():
    # 一些奇怪的错误提示
    commit_error_report()
    rand_sleep(OPERATE_INTERVAL)
    left_click(1400, 900)


def enter_battle_mode():
    # 一些奇怪的错误提示
    commit_error_report()
    rand_sleep(OPERATE_INTERVAL)
    left_click(950, 320)


def enter_mercenaries_mode():
    # 一些奇怪的错误提示
    commit_error_report()
    rand_sleep(OPERATE_INTERVAL)
    left_click(950, 470)


def commit_choose_card():
    rand_sleep(OPERATE_INTERVAL)
    left_click(960, 850)


def end_turn():
    rand_sleep(OPERATE_INTERVAL)
    left_click(1550, 500)


def commit_error_report():
    # 一些奇怪的错误提示
    left_click(1100, 820)
    # 如果已断线, 点这里时取消
    left_click(960, 650)


def emoj(target=None):
    emoj_list = [(800, 880), (800, 780), (800, 680), (1150, 680), (1150, 780)]
    right_click(960, 830)
    rand_sleep(OPERATE_INTERVAL)

    if target is None:
        x, y = emoj_list[random.randint(1, 4)]
    else:
        x, y = emoj_list[target]
    left_click(x, y)
    rand_sleep(OPERATE_INTERVAL)


def click_skill():
    rand_sleep(OPERATE_INTERVAL)
    left_click(1150, 850)


def use_skill_no_point():
    click_skill()
    cancel_click()


def use_skill_point_mine(my_index, my_num):
    click_skill()

    if my_index < 0:
        choose_my_hero()
    else:
        choose_my_minion(my_index, my_num)

    cancel_click()


def minion_beat_minion(mine_index, mine_number, oppo_index, oppo_num):
    choose_my_minion(mine_index, mine_number)
    choose_opponent_minion(oppo_index, oppo_num)
    cancel_click()


def minion_beat_hero(mine_index, mine_number):
    choose_my_minion(mine_index, mine_number)
    choose_oppo_hero()
    cancel_click()


def hero_beat_minion(oppo_index, oppo_num):
    choose_my_hero()
    choose_opponent_minion(oppo_index, oppo_num)
    cancel_click()


def hero_beat_hero():
    choose_my_hero()
    choose_oppo_hero()
    cancel_click()


def enter_HS():
    rand_sleep(1)

    if test_hs_available():
        move_window_foreground(get_HS_hwnd(), "炉石传说")
        return

    battlenet_hwnd = get_battlenet_hwnd()

    if battlenet_hwnd == 0:
        error_print("未找到应用战网")
        sys.exit()

    move_window_foreground(battlenet_hwnd, "战网")

    rand_sleep(1)

    left, top, right, bottom = win32gui.GetWindowRect(battlenet_hwnd)
    left_click(left + 180, bottom - 110)


def merc_travel():
    test_click()
    time.sleep(0.5)
    left_click(1000, 300)
    rand_sleep(2)


def merc_choose_map():
    left_click(1300, 750)
    rand_sleep(1)


def merc_choose_course():
    # 现在只有第六关
    left_click(1000, 700)
    left_click(1500, 850)
    rand_sleep(1)


def merc_choose_team():
    left_click(1400, 900)
    rand_sleep(0.4)
    left_click(850, 620)
    rand_sleep(1)


def merc_enter_battle():
    left_click(1500, 850)
    rand_sleep(0.5)


def merc_choose_mid_treasure():
    left_click(1150, 500)
    rand_sleep(0.4)
    left_click(1150, 850)
    rand_sleep(1)


MERC_HAND_CARD_X = {
    4: [750, 900, 1050, 1200],
    5: [750, 850, 950, 1080, 1200],
    6: [700, 800, 900, 1000, 1100, 1200],
}


def merc_click_hand_card(index, total_card):
    assert 6 >= total_card >= 4

    left_click(MERC_HAND_CARD_X[total_card][index], 1000)
    rand_sleep(0.1)
    left_click(1400, 600)
    rand_sleep(0.2)


def merc_click_ready():
    left_click(1580, 500)
    rand_sleep(1)


MERC_BATTLEGROUND_X = {
    3: [780, 950, 1130],
    4: [720, 880, 1040, 1200]
}


def merc_click_battleground_mine(index, total_num):
    assert total_num in [3, 4]

    left_click(MERC_BATTLEGROUND_X[total_num][index], 720)
    rand_sleep(0.2)


def merc_click_battleground_oppo(index, total_num):
    assert total_num in [3, 4]

    left_click(MERC_BATTLEGROUND_X[total_num][index], 300)
    rand_sleep(0.2)


MERC_SKILL_X = [750, 950, 1150]


def merc_click_skill(index):
    assert index <= 3
    left_click(MERC_SKILL_X[index], 500)
    left_click(MERC_SKILL_X[index], 500)
    rand_sleep(0.1)


def merc_give_up():
    left_click(860, 1005)
    rand_sleep(0.5)
    left_click(1100, 800)
    rand_sleep(0.5)
    left_click(800, 600)
    rand_sleep(0.5)
    for i in range(3):
        test_click()
        rand_sleep(0.2)

def merc_click_stranger():
    merc_enter_battle()
    time.sleep(2)
    left_click(960, 450)
    time.sleep(0.5)
    left_click(960, 750)
    time.sleep(2)
    for i in range(5):
        test_click()

def merc_click_no_battle():
    merc_enter_battle()
    time.sleep(1)
    for i in range(5):
        test_click()
