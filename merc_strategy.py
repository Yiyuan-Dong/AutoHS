from log_state import *
from log_op import *


class MercState:
    def __init__(self, log_state=None):
        self.ai_battle_minions = []
        self.my_hand_minions = []
        self.my_battle_minions = []

        for entity_id in sorted(log_state.entity_dict, key=int):
            entity = log_state.entity_dict[entity_id]
            if entity.cardtype == "MINION":
                if entity.query_tag("CONTROLLER") == "3":
                    self.my_hand_minions.append(entity)
                elif entity.query_tag("CONTROLLER") == "2":
                    self.ai_battle_minions.append(entity)
                else:
                    self.my_battle_minions.append(entity)

        self.game_complete = log_state.entity_dict["1"].query_tag("STATE") == "COMPLETE"

    def __str__(self):
        ret = f"GameState: "
        if self.game_complete:
            ret += "Complete\n"
        else:
            ret += "Running\n"

        ret += "我方场上随从:"
        for my_battle_minion in self.my_battle_minions:
            ret += my_battle_minion.name + " "
        ret += "\n"

        ret += "我方手牌随从:"
        for my_hand_minion in self.my_hand_minions:
            ret += my_hand_minion.name + " "
        ret += "\n"

        ret += "敌方随从:"
        for ai_minion in self.ai_battle_minions:
            ret += ai_minion.name + " "
        ret += "\n"

        return ret

    @property
    def my_minion_num(self):
        return len(self.my_battle_minions)

    @property
    def oppo_minion_num(self):
        return len(self.ai_battle_minions)
