from strategy import *

if __name__ == "__main__":
    log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)
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
