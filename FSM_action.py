import random
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
game_state = GameState()
log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)


def init():
    global game_state, log_iter
    game_state = GameState()
    log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)


def update_game_state():
    log_container = next(log_iter)
    if log_container.log_type == LOG_CONTAINER_ERROR:
        return False

    for log_line_container in log_container.message_list:
        ok = update_state(game_state, log_line_container)
        # if not ok:
        #     return False

    if DEBUG_PRINT:
        with open("game_state_snapshot.txt", "w", encoding="utf8") as f:
            f.write(str(game_state))

    # 注意如果Power.log没有更新, 这个函数依然会返回. 应该考虑到game_state只是被初始化
    # 过而没有进一步更新的可能
    if game_state.game_entity_id == 0:
        return False

    return True


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

    if FSM_state == FSM_CHOOSING_CARD:
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
    loop_count = 0

    while True:
        time.sleep(STATE_CHECK_INTERVAL)

        ok = update_game_state()
        if ok:
            if not game_state.is_end:
                return FSM_CHOOSING_CARD

        curr_state = get_screen.get_state()
        if curr_state == FSM_CHOOSING_HERO:
            return FSM_CHOOSING_HERO

        loop_count += 1
        if loop_count >= 80:
            return FSM_ERROR


def ChoosingCardAction():
    print_out()
    # TODO: 选牌时要不要做点什么
    time.sleep(20)
    loop_count = 0

    while True:
        click.commit_choose_card()
        ok = update_game_state()
        if not ok:
            return FSM_ERROR
        if game_state.game_num_turns_in_play > 0:
            return FSM_BATTLING
        if game_state.is_end:
            return FSM_QUITTING_BATTLE

        loop_count += 1
        if loop_count >= 50:
            return FSM_ERROR
        time.sleep(STATE_CHECK_INTERVAL)


def Battling():
    global win_count
    global game_state

    print_out()

    not_mine_count = 0
    mine_count = 0
    last_controller_is_me = False

    while True:
        if quitting_flag:
            sys.exit(0)

        ok = update_game_state()
        if not ok:
            return FSM_ERROR

        if game_state.is_end:
            if game_state.my_entity.query_tag("PLAYSTATE") == "WON":
                win_count += 1
                info_print("你赢得了这场对战")
            else:
                info_print("你输了")
            return FSM_QUITTING_BATTLE

        if not game_state.is_my_turn:
            last_controller_is_me = False
            mine_count = 0

            not_mine_count += 1
            if not_mine_count >= 400:
                return FSM_ERROR

            # time.sleep(0.5)
            continue

        # 接下来考虑在我的回合的出牌逻辑
        if not last_controller_is_me:
            time.sleep(7)
            if game_state.game_num_turns_in_play <= 2:
                click.emoj(0)
            else:
                if random.random() < EMOJ_RATE:
                    click.emoj()

        last_controller_is_me = True
        not_mine_count = 0
        mine_count += 1
        if mine_count >= 20:
            if mine_count >= 40:
                return FSM_ERROR
            click.end_turn()
            click.commit_error_report()
            click.cancel_click()
            time.sleep(STATE_CHECK_INTERVAL)
        # time.sleep(0.5)

        strategy_state = StrategyState(game_state)

        # 考虑要不要出牌
        delta_h, index, args = strategy_state.best_h_index_arg()
        if delta_h > 0:
            strategy_state.use_card(index, *args)
            continue

        # 考虑要不要用技能
        hero_power = strategy_state.my_detail_hero_power
        if hero_power and strategy_state.my_last_mana >= 2:
            delta_h, *args = hero_power.best_h_and_arg(strategy_state, -1)
            debug_print(str(delta_h) + str(args))
            if delta_h > 0:
                hero_power.use_with_arg(strategy_state, -1, *args)
                continue

        # 考虑随从怎么打架
        mine_index, oppo_index = strategy_state.get_best_attack_target()

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
    print_out()

    loop_count = 0
    while True:
        if quitting_flag:
            sys.exit(0)

        state = get_screen.get_state()
        if state in [FSM_CHOOSING_HERO, FSM_LEAVE_HS]:
            return state
        click.cancel_click()
        click.test_click()
        click.commit_error_report()

        loop_count += 1
        if loop_count >= 15:
            return FSM_ERROR

        time.sleep(STATE_CHECK_INTERVAL)


def GoBackHSAction():
    global FSM_state

    print_out()
    time.sleep(10)
    while not get_screen.test_hs_available():
        click.enter_HS()
        time.sleep(10)

    # 有时候炉石进程会直接重写Power.log, 这时应该重新创建文件操作句柄
    init()

    return FSM_MAIN_MENU


def MainMenuAction():
    print_out()

    time.sleep(30)

    while True:
        click.enter_battle_mode()
        time.sleep(5)

        state = get_screen.get_state()

        # 重新连接对战之类的
        if state == FSM_BATTLING:
            ok = update_game_state()
            if ok and game_state.available:
                return FSM_BATTLING
        if state == FSM_CHOOSING_HERO:
            return FSM_CHOOSING_HERO


def HandleErrorAction():
    print_out()

    if not get_screen.test_hs_available():
        return FSM_LEAVE_HS
    else:
        click.commit_error_report()
        click.click_setting()
        time.sleep(0.5)
        # 先尝试点认输
        click.left_click(960, 380)

        get_screen.terminate_HS()
        time.sleep(STATE_CHECK_INTERVAL)

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
        FSM_LEAVE_HS: GoBackHSAction,
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

    QuittingBattle()
