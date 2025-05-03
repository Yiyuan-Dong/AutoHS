# Add the parent directory to sys.path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategy.strategy import *
from utils.autohs_logger import *
from utils.log_op import log_iter_func, parse_line
from utils.log_state import update_state
from config import autohs_config

HEARTHSTONE_POWER_LOG_PATH = "D:/HearthStone/Logs"
PLAYER_NAME = "江海寄余生"     # !!!请根据实际情况修改!!!

if __name__ == "__main__":
    logger_init("DEBUG")

    if PLAYER_NAME == "":
        logger.error("请设置PLAYER_NAME")
        sys.exit(-1)

    log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH, "Power.log", parse_line)
    autohs_config.user_name = PLAYER_NAME

    state = LogState()

    log_container = next(log_iter)
    if log_container.log_type == LOG_CONTAINER_ERROR:
        logger.info("未找到Power.log，请启动炉石并开始对战")

        sys.exit(-1)

    for x in log_container.message_list:
        update_state(state, x)

    with open("game_state_snapshot.txt", "w", encoding="utf8") as f:
        f.write(str(state))

    strategy_state = StrategyState(state)
    strategy_state.debug_print_out()
    logger.debug("当前最佳出牌抉择: ")
    strategy_state.best_h_index_arg()
    logger.debug("当前最佳随从攻击: ")
    strategy_state.get_best_attack_target()

    # 可以在选择起手手牌的时候使用，小透...
    logger.debug(f"我方手牌及牌库共有{state.num_my_card}张牌")
    logger.debug(f"对方手牌及牌库共有{state.num_oppo_card}张牌")