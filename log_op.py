import os
import re
import time

from constants.constants import *

#　例子: "D 16:54:18.3314307 GameState.DebugPrintPower() -     GameEntity EntityID=1"
GAME_STATE_PATTERN = re.compile(r"D [\d]{2}:[\d]{2}:[\d]{2}.[\d]{7} GameState.DebugPrintPower\(\) - (.+)")

class LineInfoContainer:
    def __init__(self):
        pass


class LogInfoContainer:
    def __init__(self, info_type):
        self.info_type = info_type
        self.message_list = []

    def append_info(self, line_info):
        self.message_list.append(line_info)


def parse_line(log_container, line_str):
    match_obj = GAME_STATE_PATTERN.match(line_str)
    if match_obj is None:
        return

    line_str = match_obj.group(1)



def log_iter():
    while True:
        if not os.path.exists(HEARTHSTONE_POWER_LOG_PATH):
            yield LogInfoContainer(LOG_CONTAINER_ERROR)
            continue

        with open(HEARTHSTONE_POWER_LOG_PATH, "r", encoding="utf8") as f:
            while True:

                empty_line_count = 0
                log_container = LogInfoContainer(LOG_CONTAINER_INFO)

                while True:
                    line = f.readline()

                    if line == "":
                        time.sleep(0.1)
                        empty_line_count += 1
                        if empty_line_count == 3:
                            break
                    else:
                        empty_line_count = 0
                        parse_line(log_container, line)

                yield log_container

                if not os.path.exists(HEARTHSTONE_POWER_LOG_PATH):
                    yield LogInfoContainer(LOG_CONTAINER_ERROR)
                    break
