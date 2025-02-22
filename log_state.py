import sys

from log_op import *
from json_op import *
from autohs_logger import *
import constants.state_and_key
from config import autohs_config

class LogState:
    def __init__(self):
        self.game_entity_id = 0
        self.player_id_map_dict = {}
        self.my_name = ""
        self.oppo_name = ""
        self.my_player_id = "0"
        self.oppo_player_id = "0"
        self.entity_dict = {}
        self.current_update_id = 0

    def __str__(self):
        res = \
            f"""GameState:
    game_entity_id: {self.game_entity_id}
    my_name: {self.my_name}
    oppo_name: {self.oppo_name}
    my_player_id: {self.my_player_id}
    oppo_player_id: {self.oppo_player_id}
    current_update_id: {self.current_update_id}
    entity_keys: {[list(self.entity_dict.keys())]}

"""
        key_list = list(self.entity_dict.keys())
        key_list.sort(key=int)

        for key in key_list:
            if key == self.game_entity_id:
                res += "GameState-"
            elif key == self.my_entity_id:
                res += "MyEntity-"
            elif key == self.oppo_entity_id:
                res += "OppoEntity-"
            res += f"[{str(key)}]\n"
            res += str(self.entity_dict[key])
            res += "\n"

        return res

    @property
    def num_my_card(self):
        count = 0
        for entity in self.entity_dict.values():
            if entity.query_tag("CONTROLLER") == self.my_player_id:
                if entity.query_tag("ZONE") in ["HAND", "DECK"]:
                    count += 1
        return count

    @property
    def num_oppo_card(self):
        count = 0
        for entity in self.entity_dict.values():
            if entity.query_tag("CONTROLLER") == self.oppo_player_id:
                if entity.query_tag("ZONE") in ["HAND", "DECK"]:
                    count += 1
        return count

    @property
    def is_end(self):
        return self.game_state == "COMPLETE"

    @property
    def current_update_entity(self):
        return self.entity_dict[self.current_update_id]

    @property
    def game_entity(self):
        return self.entity_dict[self.game_entity_id]

    @property
    # 这不是my_player_id, 而是指代表我这个玩家的那个entity的index
    def my_entity_id(self):
        return self.player_id_map_dict.get(self.my_player_id, 0)

    @property
    def my_entity(self):
        return self.entity_dict[self.my_entity_id]

    @property
    def oppo_entity_id(self):
        return self.player_id_map_dict.get(self.oppo_player_id, 0)

    @property
    def oppo_entity(self):
        return self.entity_dict[self.oppo_entity_id]

    @property
    def is_my_turn(self):
        return self.my_entity.query_tag("CURRENT_PLAYER") == "1"

    @property
    def my_remaining_mana(self):
        return self.my_entity.query_tag("RESOURCES") - \
               self.my_entity.query_tag("RESOURCES_USED")

    @property
    def game_step(self):
        return self.game_entity.query_tag("STEP")

    @property
    def game_state(self):
        return self.game_entity.query_tag("STATE")

    @property
    def game_num_turns_in_play(self):
        return int(self.game_entity.query_tag("NUM_TURNS_IN_PLAY"))

    @property
    def available(self):
        return self.game_entity_id != 0

    def flush(self):
        self.__init__()

    def add_entity(self, entity_id, entity):
        assert entity_id.isdigit()
        self.entity_dict[entity_id] = entity

    def set_game_entity(self, game_entity_id, game_entity):
        self.game_entity_id = game_entity_id
        self.add_entity(game_entity_id, game_entity)

    def fetch_game_entity(self):
        return self.entity_dict[self.game_entity_id]

    def add_player_entity(self, player_entity_id, player_id, player_entity):
        self.add_entity(player_entity_id, player_entity)
        self.player_id_map_dict[player_id] = player_entity_id

    def is_my_entity(self, entity):
        return entity.query_tag("CONTROLLER") == self.my_player_id


class Entity:
    def __init__(self):
        self.tag_dict = {}

    def __str__(self):
        res = ""
        for key, value in self.tag_dict.items():
            res += f"\t{key}: {value}\n"
        return res

    def set_tag(self, tag, val):
        self.tag_dict[tag] = val

    def query_tag(self, tag, default_val="0"):
        return self.tag_dict.get(tag, default_val)

    @property
    def cardtype(self):
        return self.query_tag("CARDTYPE")

    @property
    def zone(self):
        return self.query_tag("ZONE")


class GameEntity(Entity):
    pass


class PlayerEntity(Entity):
    pass


class CardEntity(Entity):
    def __init__(self, card_id):
        super().__init__()
        self.card_id = card_id

    def __str__(self):
        return "cardID: " + self.card_id + "\n" + \
               "name: " + self.name + "\n" + \
               super().__str__()

    @property
    def name(self):
        return query_json_get_name(self.card_id)

    def update_card_id(self, card_id):
        self.card_id = card_id


def update_state(state : LogState, line_info_container):
    if line_info_container.line_type == LOG_LINE_CREATE_GAME:
        logger.debug("新的对局开始，刷新状态")
        state.flush()

    if line_info_container.line_type == LOG_LINE_GAME_ENTITY:
        game_entity = GameEntity()
        game_entity_id = line_info_container.info_dict["entity"]

        state.current_update_id = game_entity_id
        state.add_entity(game_entity_id, game_entity)
        state.game_entity_id = game_entity_id

    if line_info_container.line_type == LOG_LINE_PLAYER_ENTITY:
        player_entity = PlayerEntity()
        player_entity_id = line_info_container.info_dict["entity"]
        player_id = line_info_container.info_dict["player"]

        state.current_update_id = player_entity_id
        state.add_player_entity(player_entity_id, player_id, player_entity)

    if line_info_container.line_type == LOG_LINE_FULL_ENTITY:
        card_id = line_info_container.info_dict["card"]
        card_entity_id = line_info_container.info_dict["entity"]
        card_entity = CardEntity(card_id)

        state.current_update_id = card_entity_id
        state.add_entity(card_entity_id, card_entity)

    if line_info_container.line_type == LOG_LINE_SHOW_ENTITY:
        card_id = line_info_container.info_dict["card"]
        card_entity_id = line_info_container.info_dict["entity"]

        card_entity = state.entity_dict[card_entity_id]
        card_entity.update_card_id(card_id)
        state.current_update_id = card_entity_id

    if line_info_container.line_type == LOG_LINE_CHANGE_ENTITY:
        card_id = line_info_container.info_dict["card"]
        card_entity_id = line_info_container.info_dict["entity"]

        card_entity = state.entity_dict[card_entity_id]
        card_entity.update_card_id(card_id)
        state.current_update_id = card_entity_id

    if line_info_container.line_type == LOG_LINE_TAG_CHANGE:
        entity_string = line_info_container.info_dict["entity"]

        # 情形一 "TAG_CHANGE Entity=GameEntity"
        if entity_string == "GameEntity":
            entity_id = state.game_entity_id

        # 情形二 "TAG_CHANGE Entity=Example#51234"
        elif not entity_string.isdigit():
            # 关于为什么用 "in" 而非 "==", 因为我总是懒得输入后面的数字
            if autohs_config.user_name in entity_string:
                entity_id = state.my_entity_id
                if entity_string != state.my_name:
                    state.my_name = entity_string
            else:
                if state.oppo_name != "" and entity_string not in state.oppo_name and state.oppo_name != "UNKNOWN HUMAN PLAYER":
                    logger.error(f"我方用户名无法匹配，请检查是否正确配置用户名，当前配置{autohs_config.user_name}，双方用户名{entity_string}和{state.oppo_name}")
                entity_id = state.oppo_entity_id
                if entity_string != state.oppo_name:
                    state.oppo_name = entity_string

            assert int(entity_id) <= 3

        # 情形三 "TAG_CHANGE Entity=[entityName=UNKNOWN ENTITY [cardType=INVALID] id=14 ...]"
        # 此时的EntityId已经被提取出来了
        else:
            entity_id = entity_string

        if entity_id not in state.entity_dict:
            logger.warning(f"Invalid entity_id: {entity_id}")
            logger.warning(f"Current line container: {line_info_container}")
            return False

        tag = line_info_container.info_dict["tag"]
        value = line_info_container.info_dict["value"]

        state.entity_dict[entity_id].set_tag(tag, value)

    if line_info_container.line_type == LOG_LINE_TAG:
        tag = line_info_container.info_dict["tag"]
        value = line_info_container.info_dict["value"]

        # 在对战的一开始的时候, 对手的任何牌对你都是不可见的.
        # 故而在日志中发现的第一个不是英雄, 不是英雄技能, 而且
        # 你知道它的 CardID 的 Entity 一定是你的牌. 利用这
        # 张牌确定双方的 PlayerID
        if state.my_player_id == "0":
            if tag == "CARDTYPE" \
                    and value not in ["HERO", "HERO_POWER", "PLAYER", "GAME"] \
                    and "CONTROLLER" in state.current_update_entity.tag_dict:
                state.my_player_id = state.current_update_entity.query_tag("CONTROLLER")
                # 双方PlayerID, 一个是1, 一个是2
                state.oppo_player_id = str(3 - int(state.my_player_id))
                logger.debug(f"my_player_id: {state.my_player_id}")

        state.current_update_entity.set_tag(tag, value)

    if line_info_container.line_type == LOG_LINE_PLAYER_ID:
        player_id = line_info_container.info_dict["player"]
        player_name = line_info_container.info_dict["name"]

        # 我发现用这里的信息很不靠谱, 正常情况下的两个player_name
        # 应该对手的是"UNKNOWN HUMAN PLAYER", 你的是自己的用户名,
        # 但有时两个都是"UNKNOWN HUMAN PLAYER", 有时又都是已知.
        # 所以只拿来做校验

        # 下面这种情况明显是发生了错误. 一般会出现在在对战过程中关闭炉石
        # 再重新启动炉石. 此时在构建过程中看到的第一个确切的卡可能是对手
        # 场上的怪而非我自己的手牌, 进而误判 my_player_id
        if player_id == state.oppo_player_id and \
                autohs_config.user_name in player_name:
            logger.warning("my_player_id may be wrong")
            state.my_player_id, state.oppo_player_id = \
                state.oppo_player_id, state.my_player_id

    return True