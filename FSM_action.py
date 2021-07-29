import sys
import time

import keyboard

import click
import get_screen
from strategy import StrategyState
from game_state import *

FSM_state = ""
time_snap = 0.0
game_count = 0
win_count = 0
quitting_flag = False
LOG_ITER = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)


def system_exit():
    global quitting_flag
    quitting_flag = True
    sys_print(f"一共完成了{game_count}场对战, 赢了{win_count}场")
    sys.exit(0)


def print_out():
    global FSM_state
    global time_snap
    global game_count

    if IF_PRINTOUT:
        sys_print("Entering State " + str(FSM_state))

    if FSM_state == FSM_LEAVE_HS:
        warning_print("Wow, What happened?")
        show_time(0.0)
        warning_print("Try to go back to HS")
        print()

    if FSM_state == FSM_MATCHING:
        sys_print("The " + str(game_count + 1) + " game begins")
        game_count += 1
        time_snap = show_time(time_snap)

    return


def ChoosingHeroAction():
    print_out()
    click.match_opponent()
    time.sleep(1)
    return FSM_MATCHING


def MatchingAction():
    print_out()
    local_state = FSM_MATCHING
    while local_state == FSM_MATCHING:
        time.sleep(STATE_CHECK_INTERVAL)
        local_state = get_screen.get_state()

    if local_state in [FSM_CHOOSING_HERO, FSM_LEAVE_HS]:
        return local_state

    time.sleep(18)  # 18是一个经验数值...
    return FSM_CHOOSING_CARD


def ChoosingCardAction():
    print_out()
    # TODO: 选牌时要不要做点什么
    click.commit_choose_card()
    time.sleep(STATE_CHECK_INTERVAL)
    return FSM_BATTLING


def Battling():
    global win_count

    print_out()
    game_state = GameState()
    not_mine_count = 0
    action_in_one_turn = 0
    last_controller_is_me = False

    while True:
        if quitting_flag:
            sys.exit(0)

        log_container = next(LOG_ITER)
        if log_container.log_type == LOG_CONTAINER_ERROR:
            return FSM_ERROR

        for x in log_container.message_list:
            update_state(game_state, x)

        if DEBUG_PRINT:
            with open("game_state_snapshot.txt", "w", encoding="utf8") as f:
                f.write(str(game_state))

        if game_state.is_end:
            if game_state.my_entity.query_tag("PLAYSTATE") == "WON":
                win_count += 1
            return FSM_QUITTING_BATTLE

        if not game_state.is_my_turn:
            last_controller_is_me = False
            not_mine_count += 1
            action_in_one_turn = 0
            if not_mine_count == 1000:
                return FSM_ERROR

            # time.sleep(0.5)
            continue

        # 接下来考虑在我的回合的出牌逻辑
        if not last_controller_is_me:
            time.sleep(4)

        last_controller_is_me = True
        not_mine_count = 0
        action_in_one_turn += 1
        if action_in_one_turn == 16:
            click.end_turn()
            time.sleep(STATE_CHECK_INTERVAL)
        # time.sleep(0.5)

        strategy_state = StrategyState(game_state)

        # 考虑要不要出牌
        delta_h, index, args = strategy_state.best_h_index_arg()
        if delta_h <= 0:
            debug_print("不需要出牌")
        else:
            strategy_state.use_card(index, *args)
            continue

        # 考虑要不要用技能
        if strategy_state.my_last_mana >= 2 \
                and not strategy_state.my_hero_power.exhausted:
            click.use_skill_point()
            continue

        # 考虑随从怎么打架
        mine_index, oppo_index = strategy_state.get_best_attack_target()
        debug_print(f"我的决策是: mine_index: {mine_index}, oppo_index: {oppo_index}")

        if mine_index != -1:
            if oppo_index == -1:
                click.minion_beat_hero(mine_index, strategy_state.my_minion_num)
            else:
                click.minion_beat_minion(mine_index, strategy_state.my_minion_num,
                                         oppo_index, strategy_state.oppo_minion_num)
        else:
            click.end_turn()
            time.sleep(STATE_CHECK_INTERVAL)


def QuittingBattle():
    count = 0
    while True:
        if quitting_flag:
            sys.exit(0)

        state = get_screen.get_state()
        if state in [FSM_CHOOSING_HERO, FSM_LEAVE_HS]:
            return state
        click.cancel_click()
        click.test_click()
        click.left_click(960, 650)
        count += 1
        if count == 50:
            return HandleErrorAction()
        time.sleep(STATE_CHECK_INTERVAL)


def LeaveHSAction():
    print_out()
    global FSM_state
    while FSM_state == FSM_LEAVE_HS:
        click.enter_HS()
        time.sleep(15)
        FSM_state = get_screen.get_state()
    return FSM_state


def MainMenuAction():
    print_out()
    state = get_screen.get_state()
    while state == FSM_MAIN_MENU:
        click.enter_battle_mode()
        time.sleep(5)
        state = get_screen.get_state()
    return state


def HandleErrorAction():
    print_out()

    if not get_screen.test_hs_available():
        return LeaveHSAction()
    else:
        while get_screen.get_state() != FSM_LEAVE_HS:
            click.click_setting()
            time.sleep(0.5)
            # 先点认输
            click.left_click(960, 380)

            time.sleep(10)
            for i in range(3):
                click.test_click()
                click.cancel_click()

            click.click_setting()
            time.sleep(0.5)
            # 再点退出
            click.left_click(960, 470)
            time.sleep(6)

        return FSM_LEAVE_HS


def show_time(time_last):
    info_print("Now the time is " +
               time.strftime("%m-%d %H:%M:%S", time.localtime()))
    time_now = time.time()
    if time_last > 0:
        info_print("The last game last for : {} mins {} secs"
                   .format(int((time_now - time_last) // 60),
                           int(time_now - time_last) % 60))
    return time.time()


def FSM_dispatch(next_state):
    dispatch_dict = {
        FSM_LEAVE_HS: LeaveHSAction,
        FSM_MAIN_MENU: MainMenuAction,
        FSM_CHOOSING_HERO: ChoosingHeroAction,
        FSM_MATCHING: MatchingAction,
        FSM_CHOOSING_CARD: ChoosingCardAction,
        FSM_BATTLING: Battling,
        FSM_ERROR: HandleErrorAction,
        FSM_QUITTING_BATTLE: QuittingBattle,
    }

    if next_state not in dispatch_dict:
        error_print("Unknown state!")
        sys.exit()
    else:
        return dispatch_dict[next_state]()


def AutoHS_automata():
    global FSM_state

    while 1:
        if quitting_flag:
            sys.exit(0)
        if FSM_state == "":
            FSM_state = get_screen.get_state()
        FSM_state = FSM_dispatch(FSM_state)


if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+q", system_exit)

    Battling()
