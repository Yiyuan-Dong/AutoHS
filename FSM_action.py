import random
import click
import time
import get_screen
import sys
import cv2
from constants.constants import *
from state import State
from print_info import *
import keyboard

FSM_state = ""
turn_num = 0
time_snap = 0.0
game_count = 1


def print_out():
    global FSM_state
    global turn_num
    global time_snap
    global game_count

    if IF_PRINTOUT:
        sys_print("Entering " + FSM_state)
        if FSM_state == STRING_MYTURN:
            sys_print("    It is turn " + str(turn_num))

    if FSM_state == STRING_LEAVEHS:
        warning_print("Wow, What happened?")
        show_time(0.0)
        warning_print("Try to go back to HS")
        print()

    if FSM_state == STRING_MATCHING:
        sys_print("The " + str(game_count) + " game begins")
        game_count += 1
        turn_num = 0
        time_snap = show_time(time_snap)
        print()

    return


def ChoosingHeroAction():
    print_out()
    click.match_opponent()
    time.sleep(1)
    return STRING_MATCHING


def MatchingAction():
    print_out()
    local_state = STRING_MATCHING
    while local_state == STRING_MATCHING:
        time.sleep(STATE_CHECK_INTERVAL)
        local_state = get_screen.get_state()
    time.sleep(18)  # 18是一个经验数值...
    return STRING_CHOOSINGCARD


def ChoosingCardAction():
    print_out()
    # TODO: 选牌时要不要做点什么
    click.commit_choose_card()
    time.sleep(STATE_CHECK_INTERVAL)
    return STRING_NOTMYTURN


def NotMyTurnAction():
    print_out()
    global FSM_state
    while 1:
        click.cancel_click()
        click.test_click()
        time.sleep(STATE_CHECK_INTERVAL)
        FSM_state = get_screen.get_state()
        if FSM_state == STRING_NOTMYTURN:
            continue
        else:
            return FSM_state


def MyTurnAction():
    global turn_num
    turn_num += 1
    print_out()
    time.sleep(FRONT_ROPING_TIME)
    if_emoj = random.random()
    if if_emoj < EMOJ_RATE:
        click.emoj()

    mana_last = turn_num
    # mana_last = 10
    while True:
        state = State()
        if state.test_use_coin(mana_last):
            state.use_coin()
            continue

        delta_h, index, args = state.best_h_and_arg_within_mana(mana_last)
        if delta_h == 0:
            debug_print("不需要出牌")
            break
        mana_last -= state.use_card(index, *args)

        if mana_last < state.min_cost:
            break

    if mana_last >= 2:
        click.use_skill_point()

    last_index = -1
    for i in range(7):
        state.update_minions()
        state.debug_print_battlefield()
        mine_index, oppo_index = state.get_best_action()
        debug_print(f"我的决策是: mine_index: {mine_index}, oppo_index: {oppo_index}")

        if mine_index == -1 or last_index == mine_index:
            break
        if oppo_index == -1:
            click.minion_beat_hero(mine_index, state.mine_num)
        else:
            click.minion_beat_minion(mine_index, state.mine_num, oppo_index, state.oppo_num)
        last_index = mine_index

        time.sleep(1.5)

    time.sleep(BACK_ROPING_TIME)
    click.end_turn()
    time.sleep(STATE_CHECK_INTERVAL)

    return STRING_NOTMYTURN


# def UncertainAction():
#     log_out()
#     time.sleep(STATE_CHECK_INTERVAL)
#     click.flush_uncertain()
#     return ""

def LeaveHSAction():
    print_out()
    global FSM_state
    while FSM_state == STRING_LEAVEHS:
        click.enter_HS()
        time.sleep(15)
        FSM_state = get_screen.get_state()
    while FSM_state != STRING_CHOOSINGHERO:
        click.enter_battle_mode()
        time.sleep(10)
        FSM_state = get_screen.get_state()
    return FSM_state


def show_time(time_last):
    info_print("Now the time is " +
               time.strftime("%m-%d %H:%M:%S", time.localtime()))
    time_now = time.time()
    if time_last > 0:
        info_print("The last game last for : {} mins {} secs"
                   .format(int((time_now - time_last) // 60),
                           int(time_now - time_last) % 60))
    return time.time()


def AutoHS_automata():
    global FSM_state
    global turn_num

    while 1:
        if FSM_state == "":
            FSM_state = get_screen.get_state()
        # cv2.imwrite("./img/" + FSM_state + "/" +
        #             time.strftime("%m_%d_%H_%M_%S", time.localtime()) + ".jpg"
        #             , get_screen.catch_screen())
        FSM_state = eval(FSM_state + "Action")()


if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+q", sys.exit)
    FSM_state = get_screen.get_state()
    eval(FSM_state + "Action")()
