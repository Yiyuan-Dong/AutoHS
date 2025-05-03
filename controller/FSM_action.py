import random
from utils import window_utils
import cv2
from controller import controller
from strategy.strategy import StrategyState
from utils.log_state import *
from loguru import logger
from config import PLATFORM
from constants.state_and_key import *

FSM_state = ""
time_begin = 0.0
game_count = 0
win_count = 0
quitting_flag = False
log_state = LogState()
log_iter = None
log_iter_loading_screen = None
choose_hero_count = 0
last_state_in_log = SCREEN_MODE_STARTUP


def init():
    global log_state, log_iter, log_iter_loading_screen, choose_hero_count, autohs_config
    if PLATFORM == "Darwin":
        log_path = "/Applications/Hearthstone/Logs"
    else:
        log_path = os.path.join(autohs_config.hearthstone_install_path , "Logs")

    logger.debug("初始化日志状态")
    log_state = LogState()
    last_state_in_log = SCREEN_MODE_STARTUP
    log_iter = log_iter_func(log_path, "Power.log", parse_line)
    log_iter_loading_screen = log_iter_func(log_path, "LoadingScreen.log", parse_line_loading_screen)
    choose_hero_count = 0

def get_state_from_log():
    global log_iter_loading_screen, last_state_in_log

    if not window_utils.test_hs_available():
        return FSM_LEAVE_HS

    log_container = next(log_iter_loading_screen)
    if log_container.log_type == LOG_CONTAINER_ERROR:
        return FSM_ERROR

    for log_line_container in log_container.message_list:
        if log_line_container.line_type == LOG_LINE_MODE_CHANGE:
            prev_state = log_line_container.info_dict["prev_mode"]
            curr_state = log_line_container.info_dict["curr_mode"]

            if (prev_state != last_state_in_log):
                logger.error(f"日志状态不连续，记录状态:{last_state_in_log}，日志状态{prev_state}->{curr_state}")

            last_state_in_log = curr_state

    screen_state_to_fsm = {
        SCREEN_MODE_STARTUP: FSM_WAIT_MAIN_MENU,
        SCREEN_MODE_LOGIN: FSM_WAIT_MAIN_MENU,
        SCREEN_MODE_HUB: FSM_MAIN_MENU,
        SCREEN_MODE_TOURNAMENT: FSM_CHOOSING_HERO,
        SCREEN_MODE_COLLECTIONMANAGER: FSM_ERROR,
        SCREEN_MODE_GAMEPLAY: FSM_CHOOSING_CARD,       # 如果已经留过牌了，则会进入对战状态
        SCREEN_MODE_TRAVEN_BRAWL: FSM_ERROR,
        SCREEN_MODE_BACON: FSM_ERROR,
    }

    if last_state_in_log in screen_state_to_fsm:
        if screen_state_to_fsm[last_state_in_log] == FSM_ERROR:
            logger.error(f"游戏进入错误状态: {last_state_in_log}")
            return FSM_ERROR
        else:
            logger.debug(f"通过日志获取游戏状态: {last_state_in_log} -> {screen_state_to_fsm[last_state_in_log]}")
            return screen_state_to_fsm[last_state_in_log]
    else:
        logger.error(f"未知的游戏状态: {last_state_in_log}")
        return FSM_ERROR

def update_log_state():
    log_container = next(log_iter)
    if log_container.log_type == LOG_CONTAINER_ERROR:
        return False

    for log_line_container in log_container.message_list:
        ok = update_state(log_state, log_line_container)
        # if not ok:
        #     return False

    # 注意如果Power.log没有更新, 这个函数依然会返回. 应该考虑到game_state只是被初始化
    # 过而没有进一步更新的可能
    if log_state.game_entity_id == 0:
        return False

    return True


last_decision = None
repeat_count = 0

def check_repeat_decision(hash_code):
    global last_decision
    global repeat_count

    if last_decision == hash_code:
        repeat_count += 1
        if repeat_count >= 10:
            logger.error("连续10次相同操作，一定是哪里出了问题")
            return True
    else:
        last_decision = hash_code
        repeat_count = 0

    return False


def clear_decision():
    global last_decision
    global repeat_count

    last_decision = None
    repeat_count = 0


def system_exit():
    global quitting_flag

    quitting_flag = True
    logger.info(f"一共完成了{game_count}场对战, 赢了{win_count}场")


start_play_time = time.time()

def ChoosingHeroAction():
    global choose_hero_count
    global start_play_time

    if autohs_config.max_play_time > 0 and time.time() - start_play_time > autohs_config.max_play_time * 60:
        logger.info("已经达到最大游玩时间，退出脚本")
        window_utils.terminate_HS()
        autohs_config.exit_func()

    if autohs_config.max_win_count > 0 and win_count >= autohs_config.max_win_count:
        logger.info("已经达到最大胜利场次，退出脚本")
        window_utils.terminate_HS()
        autohs_config.exit_func()

    # 有时脚本会卡在某个地方, 从而在FSM_Matching
    # 和FSM_CHOOSING_HERO之间反复横跳. 这时候要
    # 重启炉石
    # choose_hero_count会在每一次开始留牌时重置
    choose_hero_count += 1
    if choose_hero_count >= 20:
        return FSM_ERROR

    time.sleep(2)
    controller.game.matchOpponent()
    time.sleep(1)
    return FSM_MATCHING_OPPONENT


def MatchingAction():
    loop_count = 0

    while True:
        if quitting_flag:
            return

        time.sleep(autohs_config.state_check_interval)
        controller.game.commitErrorReport()
        # click.commit_error_report()

        ok = update_log_state()
        if ok:
            if not log_state.is_end:
                return FSM_CHOOSING_CARD

        curr_state = window_utils.get_state()
        if curr_state == FSM_CHOOSING_HERO:
            return FSM_CHOOSING_HERO

        loop_count += 1
        if loop_count >= 60:
            logger.warning("Time out in Matching Opponent")
            return FSM_ERROR


def ChoosingCardAction():
    global choose_hero_count
    global game_count
    global time_begin

    choose_hero_count = 0

    game_count += 1
    logger.info("第" + str(game_count) + "场对战开始")
    time_begin = time.time()

    time.sleep(21)
    loop_count = 0
    has_print = 0

    while True:
        if quitting_flag:
            return FSM_ERROR

        ok = update_log_state()

        if not ok:
            return FSM_ERROR
        if log_state.game_num_turns_in_play > 0:
            return FSM_BATTLING
        if log_state.is_end:
            return FSM_QUITTING_BATTLE

        strategy_state = StrategyState(log_state)
        hand_card_num = strategy_state.my_hand_card_num

        # 等待被替换的卡牌 ZONE=HAND
        # 注意后手时幸运币会作为第五张卡牌算在手牌里, 故只取前四张手牌
        # 但是后手时 hand_card_num 仍然是 5
        for my_hand_index, my_hand_card in \
                enumerate(strategy_state.my_hand_cards[:4]):
            detail_card = my_hand_card.detail_card

            if detail_card is None:
                should_keep_in_hand = \
                    my_hand_card.current_cost <= autohs_config.replace_cost_bar
            else:
                should_keep_in_hand = \
                    detail_card.keep_in_hand(strategy_state, my_hand_index)

            if not has_print:
                logger.debug(f"手牌-[{my_hand_index}]({my_hand_card.name})"
                            f"是否保留: {should_keep_in_hand}")

            if not should_keep_in_hand:
                controller.cards.replaceStartingCard(my_hand_index, hand_card_num)

        has_print = 1

        controller.game.commitChooseCard()

        loop_count += 1
        if loop_count >= 60:
            logger.warning("Time out in Choosing Opponent")
            return FSM_ERROR
        time.sleep(autohs_config.state_check_interval)


def Battling():
    global win_count
    global log_state

    not_mine_count = 0
    mine_count = 0
    last_controller_is_me = False

    while True:
        if quitting_flag:
            return

        ok = update_log_state()
        if not ok:
            return FSM_ERROR

        if log_state.is_end:
            if log_state.my_entity.query_tag("PLAYSTATE") == "WON":
                win_count += 1
                logger.info("你赢得了这场对战")
            else:
                logger.info("你输了")
            return FSM_QUITTING_BATTLE

        # 在对方回合等就行了
        if not log_state.is_my_turn:
            last_controller_is_me = False
            mine_count = 0

            not_mine_count += 1
            if not_mine_count >= 400:
                logger.warning("Time out in Opponent's turn")
                return FSM_ERROR

            continue

        # 接下来考虑在我的回合的出牌逻辑
        logger.debug("-" * 60)
        strategy_state = StrategyState(log_state)
        strategy_state.debug_print_out()

        # 如果是这个我的回合的第一次操作
        if not last_controller_is_me:
            window_utils.wait_battlefield_stable(autohs_config, 5, 40)
            clear_decision()
            # 在游戏的第一个我的回合, 发一个你好
            # game_num_turns_in_play在每一个回合开始时都会加一, 即
            # 后手放第一个回合这个数是2
            if log_state.game_num_turns_in_play <= 2:
                controller.game.useEmoj(0)
                # click.emoj(0)
            else:
                # 在之后每个回合开始时有概率发表情
                if random.random() < autohs_config.emoj_ratio:
                    controller.game.useEmoj()
                if autohs_config.give_up_with_dignity and strategy_state.should_give_up():
                    controller.game.giveUpRoutine()
                    # 脚本应通过读取日志进入FSM_QUITTING_BATTLE状态
                    continue

        last_controller_is_me = True
        not_mine_count = 0
        mine_count += 1

        if mine_count >= 20:
            if mine_count >= 40:
                return FSM_ERROR
            controller.game.endTurn()
            controller.game.commitErrorReport()
            controller.game.cancelClick()
            time.sleep(autohs_config.state_check_interval)

        # 考虑要不要出牌
        index, args = strategy_state.best_h_index_arg()

        # index == -1 代表使用技能, -2 代表不出牌
        if index != -2:
            if check_repeat_decision(hash("card" + str(index) + str(args))):
                return FSM_ERROR
            strategy_state.use_best_entity(index, args)
            continue

        # 如果不出牌, 考虑随从怎么打架
        my_index, oppo_index = strategy_state.get_best_attack_target()

        # my_index == -1 代表英雄攻击, -2 代表不攻击
        if my_index != -2:
            if check_repeat_decision(hash("attack" + str(my_index) + str(oppo_index))):
                return FSM_ERROR
            strategy_state.my_entity_attack_oppo(my_index, oppo_index)
        else:
            if autohs_config.give_up_with_dignity and strategy_state.will_die_next_turn():
                controller.game.giveUpRoutine()
            else:
                controller.game.endTurn()
                time.sleep(autohs_config.state_check_interval)


def QuittingBattle():
    global game_count
    global time_begin

    logger.info("第" + str(game_count) + "场对战结束")
    time_now = time.time()
    if time_begin > 0:
        logger.info("本场对战用时: {0}分{1}秒"
                    .format(int((time_now - time_begin) // 60),
                            int(time_now - time_begin) % 60))

    time.sleep(5)

    loop_count = 0
    while True:
        if quitting_flag:
            return FSM_ERROR

        state = window_utils.get_state()
        if state in [FSM_CHOOSING_HERO, FSM_LEAVE_HS]:
            return state
        controller.game.cancelClick()
        controller.game.commitErrorReport()

        loop_count += 1
        if loop_count >= 15:
            return FSM_ERROR

        time.sleep(autohs_config.state_check_interval)


def GoBackHSAction():
    global FSM_state

    logger.warning("找不到炉石传说进程，尝试通过战网重新启动")

    time.sleep(3)

    while not window_utils.test_hs_available():
        if quitting_flag:
            return FSM_ERROR
        controller.game.enterHS()
        # click.enter_HS()
        time.sleep(10)

    # 有时候炉石进程会直接重写Power.log, 这时应该重新创建文件操作句柄
    init()

    return FSM_WAIT_MAIN_MENU


def MainMenuAction():
    time.sleep(3)

    while True:
        if quitting_flag:
            return FSM_ERROR

        controller.game.enterBattleMode()
        time.sleep(5)

        state = window_utils.get_state()

        # 重新连接对战之类的
        if state == FSM_BATTLING:
            ok = update_log_state()
            if ok and log_state.available:
                return FSM_BATTLING
        if state == FSM_CHOOSING_HERO:
            return FSM_CHOOSING_HERO


def WaitMainMenu():

    while get_state_from_log() != FSM_MAIN_MENU:
        if quitting_flag:
            return FSM_ERROR

        controller.game.clickMainMenuMiddle()
        time.sleep(5)

    return FSM_MAIN_MENU


def HandleErrorAction():
    global log_state

    logger.warning("开始异常记录")
    curr_date_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    with open("autohs_log/" + curr_date_time + "_game_state_snapshot.txt", "w", encoding="utf8") as f:
        f.write(str(log_state))
    im_opencv = window_utils.take_snapshot()
    if im_opencv is not None:
        cv2.imwrite("autohs_log/" + curr_date_time + "_error.png", im_opencv)

    if not window_utils.test_hs_available():
        return FSM_LEAVE_HS
    else:
        controller.game.commitErrorReport()
        controller.game.giveUpRoutine()

        window_utils.terminate_HS()
        time.sleep(autohs_config.state_check_interval)

        return FSM_LEAVE_HS


def FSM_dispatch(next_state):
    dispatch_dict = {
        FSM_LEAVE_HS: GoBackHSAction,
        FSM_MAIN_MENU: MainMenuAction,
        FSM_CHOOSING_HERO: ChoosingHeroAction,
        FSM_MATCHING_OPPONENT: MatchingAction,
        FSM_CHOOSING_CARD: ChoosingCardAction,
        FSM_BATTLING: Battling,
        FSM_ERROR: HandleErrorAction,
        FSM_QUITTING_BATTLE: QuittingBattle,
        FSM_WAIT_MAIN_MENU: WaitMainMenu,
    }

    if next_state not in dispatch_dict:
        logger.error("Unknown state!")
        sys.exit()
    else:
        return dispatch_dict[next_state]()


def AutoHS_automata():
    global FSM_state

    if window_utils.test_hs_available():
        hs_hwnd = window_utils.get_HS_hwnd()
        window_utils.move_window_foreground(hs_hwnd)
        time.sleep(0.5)

    while 1:
        if quitting_flag:
            return
        if FSM_state == "":
            FSM_state = get_state_from_log()
        logger.debug("下一个状态: " + str(FSM_state))
        FSM_state = FSM_dispatch(FSM_state)