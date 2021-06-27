import time

import click
from state import State, Minion
from constants.constants import *
from print_info import *


class Card:
    def __init__(self):
        self.name = ""
        self.cost = 0

    # 返回两个东西,第一项是使用这张卡的\delta h,
    # 之后是是用这张卡的最佳参数,参数数目不定
    # 参数是什么呢,比如一张火球术,参数就是指示你
    # 是要打脸还是打怪
    def h_and_best_arg(self, state: State):
        return -1

    def use_with_arg(self, state: State, card_index, *args):
        return None

    @property
    def card_type(self):
        return ""


class SpellCard(Card):
    def __init__(self):
        super(SpellCard, self).__init__()
        self.spell_type = ""
        self.wait_time = 2

    def card_type(self):
        return CARD_SPELL

    def use_with_arg(self, state: State, card_index, *args):
        if self.spell_type == "":
            warning_print(f"Spell card {self.name} does not been assigned spell type!")
            return

        if self.spell_type == SPELL_NO_POINT:
            click.choose_and_use_spell(card_index, state.card_num)
            time.sleep(self.wait_time)
            return

        if self.spell_type == SPELL_POINT_OPPO:
            oppo_index = args[0]
            click.choose_card(card_index, state.card_num)
            click.choose_opponent_minion(oppo_index, state.oppo_num)
            time.sleep(self.wait_time)
            return

        if self.spell_type == SPELL_POINT_MINE:
            mine_index = args[0]
            click.choose_card(card_index, state.card_num)
            click.choose_my_minion(mine_index, state.oppo_num)
            time.sleep(self.wait_time)
            return

        warning_print(f"{self.name} has unknown spell type: {self.spell_type}")

class MinionCard(Card):
    def card_type(self):
        return CARD_MINION


class BasicMinionCard(MinionCard):
    def __init__(self):
        super(BasicMinionCard, self).__init__()
        self.value = 0

    def h_and_best_arg(self, state: State):
        # 格子满了
        if state.mine_num == 7:
            return -1, 0
        else:
            # 默认放到最右边
            return self.value, state.mine_num

    def use_with_arg(self, state: State, card_index, *args):
        gap_index = args[0]
        click.choose_card(card_index, state.card_num)
        click.put_minion(gap_index, state.mine_num)


class WeaponCard(Card):
    def card_type(self):
        return CARD_WEAPON


class ArmorVendor(BasicMinionCard):
    def __init__(self):
        super().__init__()
        self.name = "护甲商贩"
        self.cost = 1
        self.value = 2


class HolySmite(SpellCard):
    def __init__(self):
        super().__init__()
        self.name = "神圣惩击"
        self.cost = 1
        self.spell_type = SPELL_POINT_OPPO
        self.wait_time = 2

    def h_and_best_arg(self, state: State):
        best_oppo_index = -1
        best_delta_h = 0

        for oppo_index in range(state.oppo_num):
            oppo_minion = state.oppos[oppo_index]
            # 加个bias,一是包含了消耗的水晶的代价，二是包含了消耗了手牌的代价
            bias = -4
            temp_delta_h = oppo_minion.delta_h_after_damage(3) + bias
            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index


class WaveOfApathy(SpellCard):
    def __init__(self):
        super().__init__()
        self.name = "倦怠光波"
        self.cost = 1
        self.spell_type = SPELL_NO_POINT
        self.wait_time = 2

    def h_and_best_arg(self, state: State):
        bias = -4
        tmp = 0

        for minion in state.oppos:
            tmp += minion - 1

        return tmp + bias,


class BonechewerBrawler(BasicMinionCard):
    def __init__(self):
        super().__init__()
        self.name = "噬骨斗殴者"
        self.cost = 2
        self.value = 2


class ShadowWordDeath(SpellCard):
    def __init__(self):
        super(ShadowWordDeath, self).__init__()
        self.name = "暗言术灭"
        self.cost = 2
        self.spell_type = SPELL_POINT_OPPO
        self.wait_time = 1.5

    def h_and_best_arg(self, state: State):
        best_oppo_index = -1
        best_delta_h = 0

        for i in range(state.oppo_num):
            bias = -6

            minion = state.oppos[i]
            if minion.attack < 5:
                continue

            tmp = minion.attack + minion.health + bias
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_oppo_index = i

        return best_delta_h, best_oppo_index


