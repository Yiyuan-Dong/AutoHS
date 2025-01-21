import click
import keyboard
import sys
import random

from card.basic_card import MinionNoPoint
from log_state import *
from log_op import *
from strategy_entity import *
from typing import List


class StrategyState:
    def __init__(self, log_state=None):
        self.oppo_minions: List[StrategyMinion] = []
        self.oppo_graveyard: List[StrategyEntity] = []
        self.my_minions: List[StrategyMinion] = []
        self.my_hand_cards: List[StrategyEntity] = []
        self.my_graveyard: List[StrategyEntity] = []

        self.my_hero: StrategyHero = None
        self.my_hero_power: StrategyHeroPower = None
        self.can_use_power: bool = False
        self.my_weapon: StrategyWeapon = None
        self.oppo_hero: StrategyHero = None
        self.oppo_hero_power: StrategyHeroPower = None
        self.oppo_weapon: StrategyWeapon = None
        self.oppo_hand_card_num: int = 0

        self.my_total_mana: int = int(log_state.my_entity.query_tag("RESOURCES"))
        self.my_used_mana: int = int(log_state.my_entity.query_tag("RESOURCES_USED"))
        self.my_temp_mana: int = int(log_state.my_entity.query_tag("TEMP_RESOURCES"))

        for entity in log_state.entity_dict.values():
            if entity.query_tag("ZONE") == "HAND":
                if log_state.is_my_entity(entity):
                    hand_card = entity.generate_strategy_entity(log_state)
                    self.my_hand_cards.append(hand_card)
                else:
                    self.oppo_hand_card_num += 1

            elif entity.zone == "PLAY":
                if entity.cardtype == "MINION":
                    minion = entity.generate_strategy_entity(log_state)
                    if log_state.is_my_entity(entity):
                        self.my_minions.append(minion)
                    else:
                        self.oppo_minions.append(minion)

                elif entity.cardtype == "HERO":
                    hero = entity.generate_strategy_entity(log_state)
                    if log_state.is_my_entity(entity):
                        self.my_hero = hero
                    else:
                        self.oppo_hero = hero

                # 好吧，有些时候英雄技能会在对局中被替换掉，比如暗黑主教本尼迪塔斯的开局效果。
                # 不过在 python 的 3.7 版本之后，字典的遍历顺序是按照插入顺序的，后出现的技能
                # 会覆盖掉先出现的技能，完美。
                elif entity.cardtype == "HERO_POWER":
                    hero_power = entity.generate_strategy_entity(log_state)
                    if log_state.is_my_entity(entity):
                        self.my_hero_power = hero_power
                    else:
                        self.oppo_hero_power = hero_power

                elif entity.cardtype == "WEAPON":
                    weapon = entity.generate_strategy_entity(log_state)
                    if log_state.is_my_entity(entity):
                        self.my_weapon = weapon
                    else:
                        self.oppo_weapon = weapon

            elif entity.zone == "GRAVEYARD":
                if log_state.is_my_entity(entity):
                    self.my_graveyard.append(entity)
                else:
                    self.oppo_graveyard.append(entity)

        self.my_minions.sort(key=lambda temp: temp.zone_pos)
        self.oppo_minions.sort(key=lambda temp: temp.zone_pos)
        self.my_hand_cards.sort(key=lambda temp: temp.zone_pos)

    def debug_print_battlefield(self):
        logger.debug("对手英雄:")
        logger.debug("    " + str(self.oppo_hero))
        logger.debug(f"技能:")
        logger.debug("    " + self.oppo_hero_power.name + " 费用：" + str(self.oppo_hero_power.current_cost))
        if self.oppo_weapon:
            logger.debug("头上有把武器:")
            logger.debug("    " + str(self.oppo_weapon))
        if self.oppo_minion_num > 0:
            logger.debug(f"对手有{self.oppo_minion_num}个随从:")
            for minion in self.oppo_minions:
                logger.debug("    " + str(minion))
        else:
            logger.debug(f"对手没有随从")
        logger.debug(f"总卡费启发值: {self.oppo_heuristic_value}")

        logger.debug("--------------------")

        logger.debug("我的英雄:")
        logger.debug("    " + str(self.my_hero))
        logger.debug(f"技能:")
        logger.debug("    " + self.my_hero_power.name + " 费用：" + str(self.my_hero_power.current_cost))
        if self.my_weapon:
            logger.debug("头上有把武器:")
            logger.debug("    " + str(self.my_weapon))
        if self.my_minion_num > 0:
            logger.debug(f"我有{self.my_minion_num}个随从:")
            for minion in self.my_minions:
                logger.debug("    " + str(minion))
        else:
            logger.debug("我没有随从")
        logger.debug(f"总卡费启发值: {self.my_heuristic_value}")

    def debug_print_out(self):
        if len(self.oppo_graveyard) > 0:
            logger.debug(f"对手墓地:")
            logger.debug("    " + ", ".join([entity.name for entity in self.oppo_graveyard]))
        else:
            logger.debug(f"对手墓地为空")

        logger.debug(f"对手有{self.oppo_hand_card_num}张手牌")

        self.debug_print_battlefield()
        logger.debug("--------------------")

        logger.debug(f"水晶: {self.my_remaining_mana}/{self.my_total_mana}")
        logger.debug(f"我有{self.my_hand_card_num}张手牌:")
        for hand_card in self.my_hand_cards:
            logger.debug(f"    [{hand_card.zone_pos}] {hand_card.name} "
                        f"cost:{hand_card.current_cost}")
        if len(self.my_graveyard) > 0:
            logger.debug(f"我的墓地:")
            logger.debug("    " + ", ".join([entity.name for entity in self.my_graveyard]))
        else:
            logger.debug(f"我的墓地为空")

    @property
    def my_remaining_mana(self):
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
        total_h_val = 0
        if self.oppo_hero:
            total_h_val += self.oppo_hero.heuristic_val
        if self.oppo_weapon:
            total_h_val += self.oppo_weapon.heuristic_val
        for minion in self.oppo_minions:
            total_h_val += minion.heuristic_val
        return total_h_val

    @property
    def my_heuristic_value(self):
        total_h_val = 0
        if self.my_hero:
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

    @property
    def touchable_oppo_minions(self) -> List[StrategyMinion]:
        ret = []

        for oppo_minion in self.oppo_minions:
            if oppo_minion.taunt and oppo_minion.can_be_pointed_by_minion:
                ret.append(oppo_minion)

        if len(ret) == 0:
            for oppo_minion in self.oppo_minions:
                if oppo_minion.can_be_pointed_by_minion:
                    ret.append(oppo_minion)

        return ret

    @property
    def oppo_has_taunt(self):
        for oppo_minion in self.oppo_minions:
            if oppo_minion.taunt and not oppo_minion.stealth:
                return True

        return False

    @property
    def my_total_attack(self):
        count = 0
        for my_minion in self.my_minions:
            if my_minion.can_beat_face:
                count += my_minion.attack

        if self.my_hero.can_attack:
            count += self.my_hero.attack

        return count

    # 场上有多少个虚触侍从，敌我双方都会生效，所以都算进去
    @property
    def voidtouched_attendant_on_board(self):
        count = 0
        for minion in self.my_minions + self.oppo_minions:
            if minion.card_id == "SW_446":
                count += 1

        return count

    # 我手牌里有几个空降歹徒，有的话就应该丢海盗
    @property
    def airborne_gangsters_in_hand(self):
        count = 0
        for hand_card in self.my_hand_cards:
            if hand_card.card_id == "DRG_056":
                count += 1

        return count

    @property
    # 给亡者复生用的
    def num_minions_in_my_graveyard(self):
        count = 0
        for entity in self.my_graveyard:
            if entity.cardtype == "MINION":
                count += 1

        return count

    def fetch_uni_entity(self, uni_index):
        if 0 <= uni_index < 7:
            return self.my_minions[uni_index]
        elif uni_index == 9:
            return self.my_hero
        elif 10 <= uni_index < 17:
            return self.oppo_minions[uni_index]
        elif uni_index == 19:
            return self.oppo_hero
        else:
            logger.error(f"Get invalid uni_index: {uni_index}")
            sys.exit(-1)

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
        touchable_oppo_minions = self.touchable_oppo_minions
        has_taunt = self.oppo_has_taunt
        beat_face_win = self.my_total_attack >= self.oppo_hero.health

        max_delta_h_val = 0
        max_my_index = -2
        max_oppo_index = -2
        min_attack = 0

        # 枚举每一个己方随从
        logger.debug("枚举随从")
        for my_index, my_minion in enumerate(self.my_minions):
            if not my_minion.can_attack_minion:
                continue

            # 如果没有墙,随从又能打脸,应该试一试
            if not has_taunt \
                    and my_minion.can_beat_face \
                    and self.oppo_hero.can_be_pointed_by_minion:
                if beat_face_win:
                    logger.debug(f"攻击决策: [{my_index}]({my_minion.name})->"
                                f"[-1]({self.oppo_hero.name}) "
                                f"斩杀了")
                    return my_index, -1

                tmp_delta_h = self.oppo_hero.delta_h_after_damage(my_minion.attack)

                logger.debug(f"攻击决策: [{my_index}]({my_minion.name})->"
                            f"[-1]({self.oppo_hero.name}) "
                            f"delta_h_val:{tmp_delta_h}")

                if tmp_delta_h > max_delta_h_val:
                    max_delta_h_val = tmp_delta_h
                    max_my_index = my_index
                    max_oppo_index = -1
                    min_attack = 999

            for oppo_minion in touchable_oppo_minions:
                oppo_index = oppo_minion.zone_pos - 1

                tmp_delta_h = 0
                tmp_delta_h -= my_minion.delta_h_after_damage(oppo_minion.attack)
                tmp_delta_h += oppo_minion.delta_h_after_damage(my_minion.attack)

                logger.debug(f"攻击尝试：[{my_index}]({my_minion.name})->"
                            f"[{oppo_index}]({oppo_minion.name}) "
                            f"delta_h_val: {tmp_delta_h}")

                if tmp_delta_h > max_delta_h_val or \
                        tmp_delta_h == max_delta_h_val and my_minion.attack < min_attack:
                    max_delta_h_val = tmp_delta_h
                    max_my_index = my_index
                    max_oppo_index = oppo_index
                    min_attack = my_minion.attack

        # 试一试英雄攻击
        if self.my_hero.can_attack:
            logger.debug("考虑英雄攻击")
            if not has_taunt and self.oppo_hero.can_be_pointed_by_minion:
                if beat_face_win:
                    logger.debug(f"攻击决策: [-1]({self.my_hero.name})->"
                                f"[-1]({self.oppo_hero.name}) "
                                f"斩杀了")
                    return -1, -1

            for oppo_minion in touchable_oppo_minions:
                oppo_index = oppo_minion.zone_pos - 1

                tmp_delta_h = 0
                tmp_delta_h += oppo_minion.delta_h_after_damage(self.my_hero.attack)
                tmp_delta_h -= self.my_hero.delta_h_after_damage(oppo_minion.attack)
                if self.my_weapon is not None:
                    tmp_delta_h -= self.my_weapon.attack

                logger.debug(f"攻击决策: [-1]({self.my_hero.name})->"
                            f"[{oppo_index}]({oppo_minion.name}) "
                            f"delta_h_val: {tmp_delta_h}")

                if tmp_delta_h >= max_delta_h_val:
                    max_delta_h_val = tmp_delta_h
                    max_my_index = -1
                    max_oppo_index = oppo_index

        logger.debug(f"最终决策: max_my_index: {max_my_index}, "
                    f"max_oppo_index: {max_oppo_index}")

        return max_my_index, max_oppo_index

    def my_entity_attack_oppo(self, my_index, oppo_index):
        if my_index == -1:
            if oppo_index == -1:
                click.hero_beat_hero()
            else:
                click.hero_beat_minion(oppo_index, self.oppo_minion_num)
        else:
            if oppo_index == -1:
                click.minion_beat_hero(my_index, self.my_minion_num)
            else:
                click.minion_beat_minion(my_index, self.my_minion_num,
                                         oppo_index, self.oppo_minion_num)

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
        logger.debug("------ 开始决策 ------")
        best_delta_h = 0
        best_index = -2
        best_args = []

        # 考虑使用手牌
        for hand_card_index, hand_card in enumerate(self.my_hand_cards):
            delta_h = 0
            args = []

            if hand_card.current_cost > self.my_remaining_mana:
                logger.debug(f"卡牌-[{hand_card_index}]({hand_card.name}) 跳过")
                continue

            detail_card = hand_card.detail_card
            if detail_card is None:
                if hand_card.cardtype == CARD_MINION and not hand_card.battlecry:
                    delta_h, *args = MinionNoPoint.best_h_and_arg(self, hand_card_index)
                    logger.debug(f"卡牌-[{hand_card_index}]({hand_card.name}) "
                                f"delta_h: {delta_h}, *args: {[]} (默认行为) ")
                else:
                    logger.debug(f"卡牌-[{hand_card_index}]({hand_card.name})无法评判")
            else:
                delta_h, *args = detail_card.best_h_and_arg(self, hand_card_index)
                logger.debug(f"卡牌-[{hand_card_index}]({hand_card.name}) "
                            f"delta_h: {delta_h}, *args: {args} (手写行为)")

            if delta_h > best_delta_h:
                best_delta_h = delta_h
                best_index = hand_card_index
                best_args = args

        # 考虑使用英雄技能
        if self.my_remaining_mana >= self.my_hero_power.current_cost and \
                self.my_detail_hero_power and \
                not self.my_hero_power.exhausted:
            hero_power = self.my_detail_hero_power

            delta_h, *args = hero_power.best_h_and_arg(self, -1)

            logger.debug(f"技能-[ ]({self.my_hero_power.name}) "
                        f"delta_h: {delta_h} "
                        f"*args: {args}")

            if delta_h > best_delta_h:
                best_index = -1
                best_args = args
        else:
            logger.debug(f"技能-[ ]({self.my_hero_power.name}) 跳过")

        logger.debug(f"决策结果: best_delta_h:{best_delta_h}, "
                    f"best_index:{best_index}, best_args:{best_args}")
        logger.debug("------ 结束决策 ------")
        return best_index, best_args

    def use_best_entity(self, index, args):
        if index == -1:
            logger.debug("将使用技能")
            hero_power = self.my_detail_hero_power
            hero_power.use_with_arg(self, -1, *args)
        else:
            self.use_card(index, *args)

    # 会返回这张卡的cost
    def use_card(self, index, *args):
        hand_card = self.my_hand_cards[index]
        detail_card = hand_card.detail_card
        logger.debug(f"将使用卡牌[{index}] {hand_card.name}")

        if detail_card is None:
            MinionNoPoint.use_with_arg(self, index, *args)
        else:
            detail_card.use_with_arg(self, index, *args)

        self.my_hand_cards.pop(index)
        return hand_card.current_cost


if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+q", sys.exit)

    log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)
    state = LogState()

    while True:
        log_container = next(log_iter)
        if log_container.length > 0:
            for x in log_container.message_list:
                update_state(state, x)
            strategy_state = StrategyState(state)
            strategy_state.debug_print_out()

            with open("game_state_snapshot.txt", "w", encoding="utf8") as f:
                f.write(str(state))

            mine_index, oppo_index = strategy_state.get_best_attack_target()
            logger.debug(f"我的决策是: mine_index: {mine_index}, oppo_index: {oppo_index}")

            if mine_index != -1:
                if oppo_index == -1:
                    click.minion_beat_hero(mine_index, strategy_state.my_minion_num)
                else:
                    click.minion_beat_minion(mine_index, strategy_state.my_minion_num,
                                             oppo_index, strategy_state.oppo_minion_num)
