import random
import sys
import time

import win32con
import win32gui
from pynput.mouse import Button, Controller

from print_info import *


def choose_my_minion(mine_index, mine_num):
    time.sleep(OPERATE_INTERVAL)
    x = 960 - (mine_num - 1) * 70 + mine_index * 140
    y = 600
    left_click(x, y)


def choose_opponent_minion(oppo_index, oppo_num):
    time.sleep(OPERATE_INTERVAL)
    x = 960 - (oppo_num - 1) * 70 + oppo_index * 140
    y = 400
    left_click(x, y)


def choose_oppo_hero():
    time.sleep(OPERATE_INTERVAL)
    left_click(960, 200)


def cancel_click():
    time.sleep(SMALL_OPERATE_INTERVAL)
    right_click(50, 400)


def test_click():
    time.sleep(SMALL_OPERATE_INTERVAL)
    left_click(50, 400)


def choose_card(card_index, card_num):
    x = START[card_num] + 65 + STEP[card_num] * card_index
    y = 980
    left_click(x, y)
    time.sleep(OPERATE_INTERVAL)


def click_middle():
    left_click(960, 500)


def choose_and_use_spell(card_index, card_num):
    choose_card(card_index, card_num)
    click_middle()


# 第[i]个随从左边那个空隙记为第[i]个gap
def put_minion(gap_index, minion_num):
    if minion_num >= 7:
        warning_print(f"Try to put a minion but there has already been {minion_num} minions")

    x = 960 - (minion_num - 1) * 70 + 140 * gap_index - 70
    y = 600
    left_click(x, y)
    time.sleep(OPERATE_INTERVAL)
    cancel_click()


def click_button(x, y, button):
    x += random.randint(-5, 5)
    y += random.randint(-5, 5)
    mouse = Controller()
    time.sleep(0.1)
    mouse.position = (x, y)
    time.sleep(0.1)
    mouse.press(button)
    time.sleep(0.1)
    mouse.release(button)


def left_click(x, y):
    click_button(x, y, Button.left)


def right_click(x, y):
    click_button(x, y, Button.right)


def match_opponent():
    # 一些奇怪的错误提示
    left_click(960, 650)
    time.sleep(OPERATE_INTERVAL)
    left_click(1400, 900)


def enter_battle_mode():
    # 一些奇怪的错误提示
    left_click(960, 650)
    time.sleep(OPERATE_INTERVAL)
    left_click(950, 320)


def commit_choose_card():
    left_click(960, 850)


def end_turn():
    left_click(1550, 500)


def emoj():
    emoj_list = [(800, 780), (1140, 780), (800, 680), (1150, 680)]
    right_click(960, 830)
    time.sleep(OPERATE_INTERVAL)
    x, y = emoj_list[random.randint(0, 3)]
    left_click(x, y)
    time.sleep(OPERATE_INTERVAL)


def use_skill():
    left_click(1150, 850)
    cancel_click()
    time.sleep(1)


def use_skill_point():
    left_click(1150, 850)
    time.sleep(OPERATE_INTERVAL)
    left_click(960, 850)
    cancel_click()
    time.sleep(1.5)


def minion_beat_minion(mine_index, mine_number, oppo_index, oppo_num):
    choose_my_minion(mine_index, mine_number)
    choose_opponent_minion(oppo_index, oppo_num)
    cancel_click()


def minion_beat_hero(mine_index, mine_number):
    choose_my_minion(mine_index, mine_number)
    choose_oppo_hero()
    cancel_click()


def hero_attack():
    left_click(960, 830)
    time.sleep(OPERATE_INTERVAL)
    left_click(960, 200)
    cancel_click()


def enter_HS():
    hwnd = win32gui.FindWindow(None, "战网")

    if hwnd == 0:
        error_print("未找到应用战网")
        sys.exit()

    left_click(180, 910)
    # 把战网客户端拉回前台以便点击
    win32gui.SetForegroundWindow(hwnd)
    win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
    time.sleep(1)

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    left_click(left + 180, bottom - 110)


if __name__ == "__main__":
    enter_HS()
