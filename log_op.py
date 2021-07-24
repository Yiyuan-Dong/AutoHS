import os
import re
import time
import copy
from constants.constants import *

# "D 04:23:18.0000001 GameState.DebugPrintPower() -     GameEntity EntityID=1"
GAME_STATE_PATTERN = re.compile(r"D [\d]{2}:[\d]{2}:[\d]{2}.[\d]{7} GameState.DebugPrintPower\(\) - (.+)")

# "GameEntity EntityID=1"
GAME_ENTITY_PATTERN = re.compile(r" *GameEntity EntityID=(\d+)")

# "Player EntityID=2 PlayerID=1 GameAccountId=[hi=112233445566778899 lo=223344556]"
PLAYER_PATTERN = re.compile(r" *Player EntityID=(\d+) PlayerID=(\d+).*")

# "FULL_ENTITY - Creating ID=89 CardID=EX1_538t"
# "FULL_ENTITY - Creating ID=90 CardID="
FULL_ENTITY_PATTERN = re.compile(r" *FULL_ENTITY - Creating ID=(\d+) CardID=(.*)")

# "SHOW_ENTITY - Updating Entity=90 CardID=NEW1_033o"
# "SHOW_ENTITY - Updating Entity=[entityName=UNKNOWN ENTITY [cardType=INVALID] id=32 zone=DECK zonePos=0 cardId= player=1] CardID=VAN_EX1_539"
SHOW_ENTITY_PATTERN = re.compile(r" *SHOW_ENTITY - Updating Entity=(.*) CardID=(.*) *")

# "BLOCK_START BlockType=DEATHS Entity=GameEntity EffectCardId=System.Collections.Generic.List`1[System.String] EffectIndex=0 Target=0 SubOption=-1 "
BLOCK_START_PATTERN = re.compile(r" *BLOCK_START BlockType=([A-Z]+) Entity=(.*) EffectCardId=.*")

# "BLOCK_END"
BlOCK_END_PATTERN = re.compile(r" *BLOCK_END *")

# "PlayerID=1, PlayerName=UNKNOWN HUMAN PLAYER"
PLAYER_ID_PATTERN = re.compile(r"PlayerID=(\d), PlayerName=(.*)")

# "TAG_CHANGE Entity=GameEntity tag=NEXT_STEP value=FINAL_WRAPUP "
TAG_CHANGE_PATTERN = re.compile(r" *TAG_CHANGE Entity=(.*) tag=(.*) value=(.*) *")

# "tag=ZONE value=DECK"
TAG_PATTERN = re.compile(r" *tag=(.*) value=(.*)")


class LineInfoContainer:
    def __init__(self, line_type, **kwargs):
        self.line_type = line_type
        self.info_dict = copy.copy(kwargs)

    def __str__(self):
        res = "line_type: " + str(self.line_type) + "\n"
        res += "info_dict\n"
        for key, value in self.info_dict.items():
            res += "\t" + str(key) + ": " + str(value) + "\n"


class LogInfoContainer:
    def __init__(self, log_type):
        self.log_type = log_type
        self.message_list = []

    def append_info(self, line_info):
        self.message_list.append(line_info)


def parse_line(line_str):
    match_obj = GAME_STATE_PATTERN.match(line_str)
    if match_obj is None:
        return

    line_str = match_obj.group(1)
    if line_str == "CREATE GAME":
        return LineInfoContainer(LOG_LINE_CREATE_GAME)

    return None


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
                        line_cantainer = parse_line(line)
                        if line_cantainer is not None:
                            log_container.append_info(line_cantainer)

                yield log_container

                if not os.path.exists(HEARTHSTONE_POWER_LOG_PATH):
                    yield LogInfoContainer(LOG_CONTAINER_ERROR)
                    break
