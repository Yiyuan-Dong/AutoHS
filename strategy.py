import click
import keyboard
import sys
import random

from card.basic_card import MinionNoPoint
from game_state import *
from log_op import *
from strategy_entity import *


class StrategyState:
    def __init__(self, game_state=None):
        self.oppo_minions = []
        self.oppo_graveyard = []
        self.my_minions = []
        self.my_hand_cards = []
        self.my_graveyard = []

        self.my_hero = None
        self.my_hero_power = None
        self.can_use_power = False
        self.my_weapon = None
        self.oppo_hero = None
        self.oppo_hero_power = None
        self.oppo_weapon = None
        self.oppo_hand_card_num = 0

        self.my_total_mana = int(game_state.my_entity.query_tag("RESOURCES"))
        self.my_used_mana = int(game_state.my_entity.query_tag("RESOURCES_USED"))
        self.my_temp_mana = int(game_state.my_entity.query_tag("TEMP_RESOURCES"))

        for entity in game_state.entity_dict.values():
            if entity.query_tag("ZONE") == "HAND":
                if game_state.is_my_entity(entity):
                    hand_card = entity.corresponding_entity
                    self.my_hand_cards.append(hand_card)
                else:
                    self.oppo_hand_card_num += 1

            elif entity.zone == "PLAY":
                if entity.cardtype == "MINION":
                    minion = entity.corresponding_entity
                    if game_state.is_my_entity(entity):
                        self.my_minions.append(minion)
                    else:
                        self.oppo_minions.append(minion)

                elif entity.cardtype == "HERO":
                    hero = entity.corresponding_entity
                    if game_state.is_my_entity(entity):
                        self.my_hero = hero
                    else:
                        self.oppo_hero = hero

                elif entity.cardtype == "HERO_POWER":
                    hero_power = entity.corresponding_entity
                    if game_state.is_my_entity(entity):
                        self.my_hero_power = hero_power
                    else:
                        self.oppo_hero_power = hero_power

                elif entity.cardtype == "WEAPON":
                    weapon = entity.corresponding_entity
                    if game_state.is_my_entity(entity):
                        self.my_weapon = weapon
                    else:
                        self.oppo_weapon = weapon

            elif entity.zone == "GRAVEYARD":
                if game_state.is_my_entity(entity):
                    self.my_graveyard.append(entity)
                else:
                    self.oppo_graveyard.append(entity)

        self.my_minions.sort(key=lambda temp: temp.zone_pos)
        self.oppo_minions.sort(key=lambda temp: temp.zone_pos)
        self.my_hand_cards.sort(key=lambda temp: temp.zone_pos)

        self.debug_print_out()

    def debug_print_battlefield(self):
        if not DEBUG_PRINT:
            return

        debug_print("对手英雄:")
        debug_print("    " + str(self.oppo_hero))
        debug_print(f"技能:")
        debug_print("    " + self.oppo_hero_power.name)
        if self.oppo_weapon:
            debug_print("头上有把武器:")
            debug_print("    " + str(self.oppo_weapon))
        if self.oppo_minion_num > 0:
            debug_print(f"对手有{self.oppo_minion_num}个随从:")
            for minion in self.oppo_minions:
                debug_print("    " + str(minion))
        else:
            debug_print(f"对手没有随从")
        debug_print(f"总卡费启发值: {self.oppo_heuristic_value}")

        debug_print()

        debug_print("我的英雄:")
        debug_print("    " + str(self.my_hero))
        debug_print(f"技能:")
        debug_print("    " + self.my_hero_power.name)
        if self.my_weapon:
            debug_print("头上有把武器:")
            debug_print("    " + str(self.my_weapon))
        if self.my_minion_num > 0:
            debug_print(f"我有{self.my_minion_num}个随从:")
            for minion in self.my_minions:
                debug_print("    " + str(minion))
        else:
            debug_print("我没有随从")
        debug_print(f"总卡费启发值: {self.my_heuristic_value}")

    def debug_print_out(self):
        if not DEBUG_PRINT:
            return

        debug_print(f"对手墓地:")
        debug_print("    " + ", ".join([entity.name for entity in self.oppo_graveyard]))
        debug_print(f"对手有{self.oppo_hand_card_num}张手牌")

        self.debug_print_battlefield()
        debug_print()

        debug_print(f"水晶: {self.my_last_mana}/{self.my_total_mana}")
        debug_print(f"我有{self.my_hand_card_num}张手牌:")
        for hand_card in self.my_hand_cards:
            debug_print(f"    [{hand_card.zone_pos}] {hand_card.name} "
                        f"cost:{hand_card.current_cost}")
        debug_print(f"我的墓地:")
        debug_print("    " + ", ".join([entity.name for entity in self.my_graveyard]))

    @property
    def my_last_mana(self):
        return self.my_total_mana - self.my_used_mana + self.my_temp_mana

    @property
    def oppo_minion_num(self):
        return len(self.oppo_minions)

    @property
    def my_minion_num(self):
        return len(self.my_minions)

    @property
    def my_hand_card_num(self):
        return len(self.my_hand_cards)

    # 用卡费体系算启发值
    @property
    def oppo_heuristic_value(self):
        total_h_val = self.oppo_hero.heuristic_val
        if self.oppo_weapon:
            total_h_val += self.oppo_weapon.heuristic_val
        for minion in self.oppo_minions:
            total_h_val += minion.heuristic_val
        return total_h_val

    @property
    def my_heuristic_value(self):
        total_h_val = self.my_hero.heuristic_val
        if self.my_weapon:
            total_h_val += self.my_weapon.heuristic_val
        for minion in self.my_minions:
            total_h_val += minion.heuristic_val
        return total_h_val

    @property
    def heuristic_value(self):
        return round(self.my_heuristic_value - self.oppo_heuristic_value, 3)

    @property
    def min_cost(self):
        minium = 100
        for hand_card in self.my_hand_cards:
            minium = min(minium, hand_card.current_cost)
        return minium

    @property
    def my_total_spell_power(self):
        return sum([minion.spell_power for minion in self.my_minions])

    @property
    def my_detail_hero_power(self):
        return self.my_hero_power.detail_hero_power

    def fight_between(self, oppo_index, my_index):
        oppo_minion = self.oppo_minions[oppo_index]
        my_minion = self.my_minions[my_index]

        if oppo_minion.get_damaged(my_minion.attack):
            self.oppo_minions.pop(oppo_index)

        if my_minion.get_damaged(oppo_minion.attack):
            self.my_minions.pop(my_index)

    def random_distribute_damage(self, damage, oppo_index_list, my_index_list):
        if len(oppo_index_list) == len(my_index_list) == 0:
            return

        random_x = random.randint(0, len(oppo_index_list) + len(my_index_list) - 1)

        if random_x < len(oppo_index_list):
            oppo_index = oppo_index_list[random_x]
            minion = self.oppo_minions[oppo_index]
            if minion.get_damaged(damage):
                self.oppo_minions.pop(oppo_index)
        else:
            my_index = my_index_list[random_x - len(oppo_index_list)]
            minion = self.my_minions[my_index]
            if minion.get_damaged(damage):
                self.my_minions.pop(my_index)

    def get_best_attack_target(self):
        could_attack_oppos = []
        has_taunt = False

        for i in range(len(self.oppo_minions)):
            if self.oppo_minions[i].taunt:
                could_attack_oppos.append(i)
                has_taunt = True

        if not has_taunt:
            could_attack_oppos = [i for i in range(len(self.oppo_minions))]

        max_delta_h_val = 0
        max_my_index = -1
        max_oppo_index = -1
        min_attack = 0

        for my_index, my_minion in enumerate(self.my_minions):
            if not my_minion.can_attack_minion:
                continue

            for oppo_index in could_attack_oppos:
                oppo_minion = self.oppo_minions[oppo_index]
                if oppo_minion.stealth:
                    continue

                tmp_delta_h_val = 0
                tmp_delta_h_val -= MY_DELTA_H_FACTOR * \
                                   my_minion.delta_h_after_damage(oppo_minion.attack)
                tmp_delta_h_val += OPPO_DELTA_H_FACTOR * \
                                   oppo_minion.delta_h_after_damage(my_minion.attack)

                if tmp_delta_h_val > max_delta_h_val or \
                        tmp_delta_h_val == max_delta_h_val and my_minion.attack < min_attack:
                    max_delta_h_val = tmp_delta_h_val
                    max_my_index = my_index
                    max_oppo_index = oppo_index
                    min_attack = my_minion.attack

                debug_print(f"攻击决策：[{my_index}]({my_minion})->"
                            f"[{oppo_index}]({oppo_minion}) delta_h_val: {tmp_delta_h_val}")

            # 如果没有墙,自己又能打脸,应该试一试
            if not has_taunt:
                if my_minion.can_beat_face:
                    face_delta_h = self.oppo_hero.delta_h_after_damage(my_minion.attack)
                    if face_delta_h > max_delta_h_val:
                        max_delta_h_val = face_delta_h
                        max_my_index = my_index
                        max_oppo_index = -1

                    debug_print(f"攻击决策：[{my_index}]({my_minion.name})打脸, "
                                f"delta_h_val:{face_delta_h}")

        return max_my_index, max_oppo_index

    def copy_new_one(self):
        # TODO: 有必要deepcopy吗
        tmp = copy.deepcopy(self)
        for i in range(self.oppo_minion_num):
            tmp.oppo_minions[i] = copy.deepcopy(self.oppo_minions[i])
        for i in range(self.my_minion_num):
            tmp.my_minions[i] = copy.deepcopy(self.my_minions[i])
        for i in range(self.my_hand_card_num):
            tmp.my_hand_cards[i] = copy.deepcopy(self.my_hand_cards[i])
        return tmp

    def best_h_index_arg(self):
        debug_print()
        best_delta_h = 0
        best_index = -1
        best_args = []

        for hand_card_index, hand_card in enumerate(self.my_hand_cards):
            delta_h = 0
            args = []

            if hand_card.current_cost > self.my_last_mana:
                debug_print(f"跳过第[{hand_card_index}]张卡牌({hand_card.name})")
                continue

            detail_card = hand_card.detail_card
            if detail_card is None:
                if hand_card.cardtype == CARD_MINION and not hand_card.battlecry:
                    delta_h, *args = MinionNoPoint.best_h_and_arg(self, hand_card_index)
                    debug_print(f"(默认行为) card[{hand_card_index}]({hand_card.name}) "
                                f"delta_h: {delta_h}, *args: {[]}")
                else:
                    debug_print(f"卡牌[{hand_card_index}]({hand_card.name})无法评判")
            else:
                delta_h, *args = detail_card.best_h_and_arg(self, hand_card_index)
                debug_print(f"(手写行为) card[{hand_card_index}]({hand_card.name}) "
                            f"delta_h: {delta_h}, *args: {args}")

            if delta_h > best_delta_h:
                best_delta_h = delta_h
                best_index = hand_card_index
                best_args = args

        debug_print(f"决策结果: best_delta_h:{best_delta_h}, "
                    f"best_index:{best_index}, best_args:{best_args}")
        debug_print()
        return best_delta_h, best_index, best_args

    # 会返回这张卡的cost
    def use_card(self, index, *args):
        hand_card = self.my_hand_cards[index]
        detail_card = hand_card.detail_card
        debug_print(f"将使用卡牌[{index}] {hand_card.name}")
        debug_print()

        if detail_card is None:
            MinionNoPoint.use_with_arg(self, index, *args)
        else:
            detail_card.use_with_arg(self, index, *args)

        self.my_hand_cards.pop(index)
        return hand_card.current_cost


if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+q", sys.exit)

    log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)
    state = GameState()

    while True:
        log_container = next(log_iter)
        if log_container.length > 0:
            for x in log_container.message_list:
                update_state(state, x)
            strategy_state = StrategyState(state)

            with open("game_state_snapshot.txt", "w", encoding="utf8") as f:
                f.write(str(state))

            mine_index, oppo_index = strategy_state.get_best_attack_target()
            debug_print(f"我的决策是: mine_index: {mine_index}, oppo_index: {oppo_index}")

            if mine_index != -1:
                if oppo_index == -1:
                    click.minion_beat_hero(mine_index, strategy_state.my_minion_num)
                else:
                    click.minion_beat_minion(mine_index, strategy_state.my_minion_num,
                                             oppo_index, strategy_state.oppo_minion_num)
