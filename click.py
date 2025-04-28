import time
from pynput.mouse import Button, Controller
import random
import sys

from constants.state_and_key import *
from autohs_logger import *
from window_utils import *
from config import autohs_config


def rand_sleep(interval):
    base_time = interval * 0.75
    rand_time = interval * 0.5 * random.random()  # avg = 0.25 * interval
    time.sleep(base_time + rand_time)


def click_button(x, y, button):
    # 随机化点击位置，看着更像人类操作
    x += random.randint(-5, 5)
    y += random.randint(-5, 5)
    mouse = Controller()
    rand_sleep(0.1)
    mouse.position = (x, y)
    rand_sleep(0.1)
    mouse.press(button)
    rand_sleep(0.1)
    mouse.release(button)


def left_click(x, y):
    click_button(x, y, Button.left)


def right_click(x, y):
    click_button(x, y, Button.right)


def choose_my_minion(mine_index, mine_num):
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.operate_interval)
    x = coors[COORDINATE_MID_X] + (mine_index * 2 - mine_num + 1) * coors[COORDINATE_HALF_MINION_GAP_X]
    y = coors[COORDINATE_MY_MINION_Y]
    left_click(x, y)


def choose_my_hero():
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.operate_interval)
    left_click(coors[COORDINATE_MID_X], coors[COORDINATE_MY_HERO_Y])


def choose_opponent_minion(oppo_index, oppo_num):
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.operate_interval)
    x = coors[COORDINATE_MID_X] + (oppo_index * 2 - oppo_num + 1) * coors[COORDINATE_HALF_MINION_GAP_X]
    y = coors[COORDINATE_OPPO_MINION_Y]
    left_click(x, y)


def choose_oppo_hero():
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.operate_interval)
    left_click(coors[COORDINATE_MID_X], coors[COORDINATE_OPPO_HERO_Y])


def cancel_click():
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.tiny_operate_interval)
    right_click(coors[COORDINATE_CANCEL_X], coors[COORDINATE_CANCEL_Y])


def test_click():
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.tiny_operate_interval)
    right_click(coors[COORDINATE_CANCEL_X], coors[COORDINATE_CANCEL_Y])


def choose_card(card_index, card_num):
    coors = autohs_config.click_coordinates
    hand_card_x = coors[COORDINATE_MY_HAND_X]

    rand_sleep(autohs_config.operate_interval)

    # TODO: 其实最多可以有12张手牌
    assert 0 <= card_index < card_num <= 10

    x = hand_card_x[card_num][card_index]
    y = coors[COORDINATE_MY_HAND_Y]

    left_click(x, y)


def replace_starting_card(card_index, hand_card_num):
    coors = autohs_config.click_coordinates
    start_card_x = coors[COORDINATE_START_CARD_X]

    assert hand_card_num in start_card_x
    assert card_index < len(start_card_x[hand_card_num])

    rand_sleep(autohs_config.operate_interval)
    left_click(start_card_x[hand_card_num][card_index], coors[COORDINATE_START_CARD_Y])


def click_middle():
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.operate_interval)
    left_click(coors[COORDINATE_MID_X], coors[COORDINATE_NO_OP_Y])

def click_main_menu_middle():
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.operate_interval)
    left_click(coors[COORDINATE_MID_X], coors[COORDINATE_MAIN_MENU_NO_OP_Y])

def click_setting():
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.operate_interval)
    left_click(coors[COORDINATE_SETTING_X], coors[COORDINATE_SETTING_Y])


def choose_and_use_spell(card_index, card_num):
    choose_card(card_index, card_num)
    click_middle()


def click_give_up():
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.operate_interval)
    left_click(coors[COORDINATE_GIVE_UP_X], coors[COORDINATE_GIVE_UP_Y])


# 第[i]个随从左边那个空隙记为第[i]个gap
def put_minion(gap_index, minion_num):
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.operate_interval)

    if minion_num >= 7:
        logger.warning(f"Try to put a minion but there has already been {minion_num} minions")

    x = coors[COORDINATE_MID_X] + (2 * gap_index - minion_num) * coors[COORDINATE_HALF_MINION_GAP_X]
    y = coors[COORDINATE_MY_MINION_Y]
    left_click(x, y)


def match_opponent():
    coors = autohs_config.click_coordinates

    # 一些奇怪的错误提示
    commit_error_report()
    rand_sleep(autohs_config.operate_interval)
    left_click(coors[COORDINATE_MATCH_OPPONENT_X], coors[COORDINATE_MATCH_OPPONENT_Y])


def enter_battle_mode():
    coors = autohs_config.click_coordinates

    # 一些奇怪的错误提示
    # commit_error_report()
    rand_sleep(autohs_config.operate_interval)
    left_click(coors[COORDINATE_MID_X], coors[COORDINATE_ENTER_BATTLE_Y])


def commit_choose_card():
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.operate_interval)
    left_click(coors[COORDINATE_MID_X], coors[COORDINATE_COMMIT_CHOOSE_START_CARD_Y])


def end_turn():
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.operate_interval)
    left_click(coors[COORDINATE_END_TURN_X], coors[COORDINATE_END_TURN_Y])


# TODO: Check it
def commit_error_report():
    coors = autohs_config.click_coordinates

    # 一些奇怪的错误提示
    left_click(coors[COORDINATE_ERROR_REPORT_X], coors[COORDINATE_ERROR_REPORT_Y])
    # 如果已断线, 点这里时取消
    left_click(coors[COORDINATE_DISCONNECTED_X], coors[COORDINATE_DISCONNECTED_Y])


def emoj(target=None):
    coors = autohs_config.click_coordinates
    emoj_list = coors[COORDINATE_EMOJ_LIST]

    right_click(coors[COORDINATE_MID_X], coors[COORDINATE_MY_HERO_Y])
    rand_sleep(autohs_config.operate_interval)

    if target is None:
        x, y = emoj_list[random.randint(1, 4)]
    else:
        x, y = emoj_list[target]
    left_click(x, y)
    rand_sleep(autohs_config.operate_interval)


def give_up_routine():
    # 打得不错
    emoj(1)
    click_setting()
    time.sleep(0.5)
    click_give_up()
    time.sleep(3)


def click_skill():
    coors = autohs_config.click_coordinates

    rand_sleep(autohs_config.operate_interval)
    left_click(coors[COORDINATE_SKILL_X], coors[COORDINATE_SKILL_Y])


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

def use_skill_point_oppo(oppo_index, oppo_num):
    click_skill()

    if oppo_index < 0:
        choose_oppo_hero()
    else:
        choose_opponent_minion(oppo_index, oppo_num)

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
        logger.error("未找到应用战网")
        sys.exit()

    move_window_foreground(battlenet_hwnd, "战网")

    rand_sleep(1)

    left, top, right, bottom = get_window_pos(battlenet_hwnd)
    left_click(left + 180, bottom - 110)
