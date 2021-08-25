import random
import sys
import time

import keyboard

import click
import get_screen
from strategy import StrategyState
from game_state import *

FSM_state = ""
time_begin = 0.0
game_count = 0
win_count = 0
quitting_flag = False
game_state = GameState()
log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)
choose_hero_count = 0

def init():
    global game_state, log_iter

    # 有时候炉石退出时python握着Power.log的读锁, 因而炉石无法
    # 删除Power.log. 而当炉石重启时, 炉石会从头开始写Power.log,
    # 但此时python会读入完整的Power.log, 并在原来的末尾等待新的写入. 那
    # 样的话python就一直读不到新的log. 状态机进而卡死在匹配状态(不
    # 知道对战已经开始)
    # 这里是试图在每次初始化文件句柄的时候删除已有的炉石日志. 如果要清空的
    # 日志是关于当前打开的炉石的, 那么炉石会持有此文件的写锁, 使脚本无法
    # 清空日志. 这使得脚本不会清空有意义的日志
    if os.path.exists(HEARTHSTONE_POWER_LOG_PATH):
        try:
            file_handle = open(HEARTHSTONE_POWER_LOG_PATH, "w")
            file_handle.seek(0)
            file_handle.truncate()
            info_print("Success to truncate Power.log")
        except OSError:
            warn_print("Fail to truncate Power.log, maybe someone is using it")
    else:
        info_print("Power.log does not exist")

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

    if DEBUG_FILE_WRITE:
        with open("./log/game_state_snapshot.txt", "w", encoding="utf8") as f:
            f.write(str(game_state))

    # 注意如果Power.log没有更新, 这个函数依然会返回. 应该考虑到game_state只是被初始化
    # 过而没有进一步更新的可能
    if game_state.game_entity_id == 0:
        return False

    return True


def system_exit():
    global quitting_flag

    sys_print(f"一共完成了{game_count}场对战, 赢了{win_count}场")
    print_info_close()

    quitting_flag = True

    sys.exit(0)


def print_out():
    global FSM_state
    global time_begin
    global game_count

    sys_print("Enter State " + str(FSM_state))

    if FSM_state == FSM_LEAVE_HS:
        warn_print("HearthStone not found! Try to go back to HS")

    if FSM_state == FSM_CHOOSING_CARD:
        game_count += 1
        sys_print("The " + str(game_count) + " game begins")
        time_begin = time.time()

    if FSM_state == FSM_QUITTING_BATTLE:
        sys_print("The " + str(game_count) + " game ends")
        time_now = time.time()
        if time_begin > 0:
            info_print("The last game last for : {} mins {} secs"
                       .format(int((time_now - time_begin) // 60),
                               int(time_now - time_begin) % 60))

    return


def ChoosingHeroAction():
    global choose_hero_count

    # 有时脚本会卡在某个地方, 从而在FSM_Matching
    # 和FSM_CHOOSING_HERO之间反复横跳. 这时候要
    # 重启炉石
    # choose_hero_count会在每一次开始留牌时重置
    choose_hero_count += 1
    if choose_hero_count >= 20:
        return FSM_ERROR

    print_out()
    time.sleep(2)
    click.match_opponent()
    time.sleep(1)
    return FSM_MATCHING


def MatchingAction():
    print_out()
    loop_count = 0

    while True:
        if quitting_flag:
            sys.exit(0)

        time.sleep(STATE_CHECK_INTERVAL)

        click.commit_error_report()

        ok = update_game_state()
        if ok:
            if not game_state.is_end:
                return FSM_CHOOSING_CARD

        curr_state = get_screen.get_state()
        if curr_state == FSM_CHOOSING_HERO:
            return FSM_CHOOSING_HERO

        loop_count += 1
        if loop_count >= 60:
            warn_print("Time out in Matching Opponent")
            return FSM_ERROR


def ChoosingCardAction():
    global choose_hero_count
    choose_hero_count = 0

    print_out()
    time.sleep(21)
    loop_count = 0
    has_print = 0

    while True:
        ok = update_game_state()

        if not ok:
            return FSM_ERROR
        if game_state.game_num_turns_in_play > 0:
            return FSM_BATTLING
        if game_state.is_end:
            return FSM_QUITTING_BATTLE

        strategy_state = StrategyState(game_state)
        hand_card_num = strategy_state.my_hand_card_num

        # 等待被替换的卡牌 ZONE=HAND
        # 注意后手时幸运币会作为第五张卡牌算在手牌里, 故只取前四张手牌
        # 但是后手时 hand_card_num 仍然是 5
        for my_hand_index, my_hand_card in \
                enumerate(strategy_state.my_hand_cards[:4]):
            detail_card = my_hand_card.detail_card

            if detail_card is None:
                should_keep_in_hand = \
                    my_hand_card.current_cost <= REPLACE_COST_BAR
            else:
                should_keep_in_hand = \
                    detail_card.keep_in_hand(strategy_state, my_hand_index)

            if not has_print:
                debug_print(f"手牌-[{my_hand_index}]({my_hand_card.name})"
                            f"是否保留: {should_keep_in_hand}")

            if not should_keep_in_hand:
                click.replace_starting_card(my_hand_index, hand_card_num)

        has_print = 1

        click.commit_choose_card()

        loop_count += 1
        if loop_count >= 60:
            warn_print("Time out in Choosing Opponent")
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

        # 在对方回合等就行了
        if not game_state.is_my_turn:
            last_controller_is_me = False
            mine_count = 0

            not_mine_count += 1
            if not_mine_count >= 400:
                warn_print("Time out in Opponent's turn")
                return FSM_ERROR

            continue

        # 接下来考虑在我的回合的出牌逻辑

        # 如果是这个我的回合的第一次操作
        if not last_controller_is_me:
            time.sleep(4)
            # 在游戏的第一个我的回合, 发一个你好
            # game_num_turns_in_play在每一个回合开始时都会加一, 即
            # 后手放第一个回合这个数是2
            if game_state.game_num_turns_in_play <= 2:
                click.emoj(0)
            else:
                # 在之后每个回合开始时有概率发表情
                if random.random() < EMOJ_RATIO:
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

        debug_print("-" * 60)
        strategy_state = StrategyState(game_state)
        strategy_state.debug_print_out()

        # 考虑要不要出牌
        index, args = strategy_state.best_h_index_arg()

        # index == -1 代表使用技能, -2 代表不出牌
        if index != -2:
            strategy_state.use_best_entity(index, args)
            continue

        # 如果不出牌, 考虑随从怎么打架
        my_index, oppo_index = strategy_state.get_best_attack_target()

        # my_index == -1代表英雄攻击, -2 代表不攻击
        if my_index != -2:
            strategy_state.my_entity_attack_oppo(my_index, oppo_index)
        else:
            click.end_turn()
            time.sleep(STATE_CHECK_INTERVAL)


def QuittingBattle():
    print_out()

    time.sleep(5)

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
    time.sleep(3)

    while not get_screen.test_hs_available():
        if quitting_flag:
            sys.exit(0)
        click.enter_HS()
        time.sleep(10)

    # 有时候炉石进程会直接重写Power.log, 这时应该重新创建文件操作句柄
    init()

    return FSM_MAIN_MENU


def MainMenuAction():
    print_out()

    time.sleep(30)

    while True:
        if quitting_flag:
            sys.exit(0)

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
        time.sleep(2)

        get_screen.terminate_HS()
        time.sleep(STATE_CHECK_INTERVAL)

        return FSM_LEAVE_HS


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

    init()
