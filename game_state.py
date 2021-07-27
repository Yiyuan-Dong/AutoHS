from json_op import *
from log_op import *

JSON_DICT = read_json()


class GameState:
    def __init__(self):
        self.game_entity_id = 0
        self.player_id_map_dict = {}
        self.my_name = ""
        self.oppo_name = ""
        self.my_player_id = 0
        self.oppo_player_id = 0
        self.entity_dict = {}
        self.current_update_id = 0

    def __str__(self):
        res = "--------------------\n"
        res += "State:"
        res += f"""
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

    @property
    def current_update_entity(self):
        return self.entity_dict[self.current_update_id]

    @property
    def game_entity(self):
        return self.entity_dict[self.game_entity_id]

    @property
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
        return self.my_entity.query_tag("CURRENT_PLAYER") == 1

    @property
    def my_last_mana(self):
        return self.my_entity.query_tag("RESOURCES") - \
               self.my_entity.query_tag("RESOURCES_USED")

    @property
    def game_step(self):
        return self.game_entity.query("STEP")

    @property
    def game_state(self):
        return self.game_entity.query("STATE")


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

    def query_tag(self, tag):
        return self.tag_dict.get(tag, 0)


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

    def update_card_id(self, card_id):
        self.card_id = card_id

    @property
    def name(self):
        temp = JSON_DICT.get(self.card_id, None)
        if temp:
            return temp["name"]
        else:
            return "Unknown"


def update_state(state, line_info_container):
    if line_info_container.line_type == LOG_LINE_CREATE_GAME:
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

    if line_info_container.line_type == LOG_LINE_TAG_CHANGE:
        entity_string = line_info_container.info_dict["entity"]

        # 情形一 "TAG_CHANGE Entity=GameEntity"
        if entity_string == "GameEntity":
            entity_id = state.game_entity_id
        # 情形二 "TAG_CHANGE Entity=Example#51234"
        elif not entity_string.isdigit():
            if entity_string == state.my_name:
                entity_id = state.my_entity_id
            else:
                entity_id = state.oppo_entity_id
                if entity_string != state.oppo_name:
                    state.oppo_name = entity_string

            assert int(entity_id) <= 3
        # 情形三 "TAG_CHANGE Entity=[entityName=UNKNOWN ENTITY [cardType=INVALID] id=14 ...]"
        # 此时的EntityId已经被提取出来了
        else:
            entity_id = entity_string

        tag = line_info_container.info_dict["tag"]
        value = line_info_container.info_dict["value"]

        state.entity_dict[entity_id].set_tag(tag, value)

    if line_info_container.line_type == LOG_LINE_TAG:
        tag = line_info_container.info_dict["tag"]
        value = line_info_container.info_dict["value"]
        state.current_update_entity.set_tag(tag, value)

    if line_info_container.line_type == LOG_LINE_PLAYER_ID:
        player_id = line_info_container.info_dict["player"]
        player_name = line_info_container.info_dict["name"]

        # 比如 "旅店老板", "UNKNOWN HUMAN PLAYER" (PVP时不会立刻显示对手昵称)
        if "#" not in player_name:
            state.oppo_player_id = player_id
        else:
            state.my_name = player_name
            state.my_player_id = player_id


if __name__ == "__main__":
    log_iter = log_iter_func("./Power.log")
    log_container = next(log_iter)
    state = GameState()

    for x in log_container.message_list:
        # print(x)
        update_state(state, x)
    print(state)
