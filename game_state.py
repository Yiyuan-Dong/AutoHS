from log_op import *


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

    def add_entity(self, entity_id, entity):
        self.entity_dict[entity_id] = entity

    def set_game_entity(self, game_entity_id, game_entity):
        self.game_entity_id = game_entity_id
        self.add_entity(game_entity_id, game_entity)

    def fetch_game_entity(self):
        return self.entity_dict[self.game_entity_id]

    def add_player_entity(self, player_entity_id, player_id, player_entity):
        self.add_entity(player_entity_id, player_entity)
        self.player_id_map_dict[player_id] = player_entity_id

    @property
    def current_entity(self):
        return self.entity_dict[self.current_update_id]


class Entity:
    def __init__(self):
        self.tag_dict = {}

    def set_tag(self, tag, val):
        self.tag_dict[tag] = val

    def query_tag(self, tag):
        return self.tag_dict[tag]


class GameEntity(Entity):
    pass


class PlayerEntity(Entity):
    pass

class CardEntity(Entity):
    def __init__(self, card_id):
        super().__init__()
        self.card_id = card_id

    def update_card_id(self, card_id):
        self.card_id = card_id


def update_state(state, line_info_container):
    if line_info_container.log_type == LOG_LINE_CREATE_GAME:
        state = GameState()

    if line_info_container.log_type == LOG_LINE_GAME_ENTITY:
        game_entity = GameEntity()
        game_entity_id = line_info_container.info_dict["entity"]

        state.current_update_id = game_entity_id
        state.add_entity(game_entity_id, game_entity)

    if line_info_container.log_type == LOG_LINE_PLAYER_ENTITY:
        player_entity = PlayerEntity()
        player_entity_id = line_info_container.info_dict["entity"]
        player_id = line_info_container.info_dict["player"]

        state.current_update_id = player_entity_id
        state.add_player_entity(player_entity_id, player_id, player_entity)

    if line_info_container.log_type == LOG_LINE_FULL_ENTITY:
        card_id = line_info_container.info_dict["card"]
        card_entity_id = line_info_container.info_dict["entity"]
        card_entity = CardEntity(card_id)

        state.current_update_id = card_entity_id
        state.add_entity(card_entity_id, card_entity)

    if line_info_container.log_type == LOG_LINE_SHOW_ENTITY:
        card_id = line_info_container.info_dict["card"]
        card_entity_id = line_info_container.info_dict["entity"]

        card_entity = state.entity_dict[card_entity_id]
        card_entity.update_card_id(card_id)
        state.current_update_id = card_entity_id

    if line_info_container.log_type == LOG_LINE_TAG_CHANGE:
        entity_string = line_info_container.info_dict["entity"]
        if entity_string == "GameEntity":
            entity_id = state.game_entity_id
        elif "#" in entity_string:
            if entity_string == state.my_name:
                entity_id = state.my_player_id
            else:
                entity_id = state.oppo_player_id
                if entity_string != state.oppo_name:
                    state.oppo_name = entity_string
        else:
            entity_id = entity_string

        tag = line_info_container.info_dict["tag"]
        value = line_info_container.info_dict["value"]

        state.entity_dict[entity_id].set_tag(tag, value)

    if line_info_container.log_type == LOG_LINE_TAG:
        tag = line_info_container.info_dict["tag"]
        value = line_info_container.info_dict["value"]
        state.current_entity.set_tag(tag, value)

    if line_info_container.log_type == LOG_LINE_PLAYER_ID:
        player_id = line_info_container.info_dict["player"]
        player_name = line_info_container.info_dict["name"]

        # 比如 "旅店老板", "UNKNOWN HUMAN PLAYER" (PVP时不会立刻显示对手昵称)
        if "#" not in player_name:
            state.oppo_player_id = player_id
        else:
            state.my_name = player_name
            state.my_player_id = player_id


