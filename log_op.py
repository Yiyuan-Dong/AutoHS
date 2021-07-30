import os
import re
import time
import copy
from constants.constants import *

# "D 04:23:18.0000001 GameState.DebugPrintPower() -     GameEntity EntityID=1"
GAME_STATE_PATTERN = re.compile(r"D [\d]{2}:[\d]{2}:[\d]{2}.[\d]{7} GameState.DebugPrint(Game|Power)\(\) - (.+)")

# "GameEntity EntityID=1"
GAME_ENTITY_PATTERN = re.compile(r" *GameEntity EntityID=(\d+)")

# "Player EntityID=2 PlayerID=1 GameAccountId=[hi=112233445566778899 lo=223344556]"
PLAYER_PATTERN = re.compile(r" *Player EntityID=(\d+) PlayerID=(\d+).*")

# "FULL_ENTITY - Creting ID=89 CardID=EX1_538t"
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
# "PlayerID=2, PlayerName=Example#51234"
PLAYER_ID_PATTERN = re.compile(r"PlayerID=(\d+), PlayerName=(.*)")

# "TAG_CHANGE Entity=GameEntity tag=NEXT_STEP value=FINAL_WRAPUP "
# "TAG_CHANGE Entity=Example#51234 tag=467 value=4 "
# "TAG_CHANGE Entity=[entityName=UNKNOWN ENTITY [cardType=INVALID] id=14 zone=DECK zonePos=0 cardId= player=1] tag=ZONE value=HAND "
TAG_CHANGE_PATTERN = re.compile(r" *TAG_CHANGE Entity=(.*) tag=(.*) value=(.*) ")

# "tag=ZONE value=DECK"
TAG_PATTERN = re.compile(r" *tag=(.*) value=(.*)")


class LineInfoContainer:
    def __init__(self, line_type, **kwargs):
        self.line_type = line_type
        self.info_dict = copy.copy(kwargs)

    def __str__(self):
        res = "line_type: " + str(self.line_type) + "\n"
        if len(self.info_dict) > 0:
            res += "info_dict\n"
            for key, value in self.info_dict.items():
                res += "\t" + str(key) + ": " + str(value) + "\n"
        return res


class LogInfoContainer:
    def __init__(self, log_type):
        self.log_type = log_type
        self.message_list = []

    def append_info(self, line_info):
        self.message_list.append(line_info)

    @property
    def length(self):
        return len(self.message_list)


def fetch_entity_id(input_string):
    if input_string[0] != "[":
        return input_string

    # 去除前后的 "[", "]"
    kv_list = input_string[1:-1]

    # 提取成形如 [... , "id=233" , ...]的格式
    kv_list = kv_list.split(" ")

    for item in kv_list:
        if item[:3] == "id=":
            return item[3:]


def parse_line(line_str):
    match_obj = GAME_STATE_PATTERN.match(line_str)
    if match_obj is None:
        return

    line_str = match_obj.group(2)

    if line_str == "CREATE_GAME":
        return LineInfoContainer(LOG_LINE_CREATE_GAME)

    match_obj = TAG_CHANGE_PATTERN.match(line_str)
    if match_obj is not None:
        return LineInfoContainer(
            LOG_LINE_TAG_CHANGE,
            entity=fetch_entity_id(match_obj.group(1)),
            tag=match_obj.group(2),
            value=match_obj.group(3),
        )

    match_obj = TAG_PATTERN.match(line_str)
    if match_obj is not None:
        return LineInfoContainer(
            LOG_LINE_TAG,
            tag=match_obj.group(1),
            value=match_obj.group(2)
        )

    match_obj = GAME_ENTITY_PATTERN.match(line_str)
    if match_obj is not None:
        return LineInfoContainer(
            LOG_LINE_GAME_ENTITY,
            entity=match_obj.group(1)
        )

    match_obj = PLAYER_PATTERN.match(line_str)
    if match_obj is not None:
        return LineInfoContainer(
            LOG_LINE_PLAYER_ENTITY,
            entity=match_obj.group(1),
            player=match_obj.group(2)
        )

    match_obj = FULL_ENTITY_PATTERN.match(line_str)
    if match_obj is not None:
        return LineInfoContainer(
            LOG_LINE_FULL_ENTITY,
            entity=match_obj.group(1),
            card=match_obj.group(2)
        )

    match_obj = SHOW_ENTITY_PATTERN.match(line_str)
    if match_obj is not None:
        return LineInfoContainer(
            LOG_LINE_SHOW_ENTITY,
            entity=fetch_entity_id(match_obj.group(1)),
            card=match_obj.group(2)
        )

    match_obj = BLOCK_START_PATTERN.match(line_str)
    if match_obj is not None:
        return LineInfoContainer(
            LOG_LINE_BLOCK_START,
            type=match_obj.group(1),
            card=match_obj.group(2)
        )

    match_obj = BlOCK_END_PATTERN.match(line_str)
    if match_obj is not None:
        return LineInfoContainer(
            LOG_LINE_BLOCK_END
        )

    match_obj = PLAYER_ID_PATTERN.match(line_str)
    if match_obj is not None:
        return LineInfoContainer(
            LOG_LINE_PLAYER_ID,
            player=match_obj.group(1),
            name=match_obj.group(2)
        )

    return None


def log_iter_func(path=HEARTHSTONE_POWER_LOG_PATH):
    while True:
        if not os.path.exists(path):
            yield LogInfoContainer(LOG_CONTAINER_ERROR)
            continue

        with open(path, "r", encoding="utf8") as f:
            while True:

                empty_line_count = 0
                log_container = LogInfoContainer(LOG_CONTAINER_INFO)

                while True:
                    line = f.readline()

                    if line == "":
                        time.sleep(0.2)
                        empty_line_count += 1
                        if empty_line_count == 2:
                            break
                    else:
                        empty_line_count = 0
                        line_container = parse_line(line)
                        if line_container is not None:
                            log_container.append_info(line_container)

                yield log_container

                if not os.path.exists(path):
                    yield LogInfoContainer(LOG_CONTAINER_ERROR)
                    break


if __name__ == "__main__":
    line_str = input()
    print(parse_line(line_str))
