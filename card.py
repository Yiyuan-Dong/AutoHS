import click
from state import State, Minion
from constants.constants import *


class Card:
    def __init__(self):
        self.name = ""
        self.cost = 0

    # 返回两个东西,第一项是使用这张卡的\delta h,
    # 之后是是用这张卡的最佳参数,参数数目不定
    # 参数是什么呢,比如一张火球术,参数就是指示你
    # 是要打脸还是打怪

    def best_arg(self, state: State):
        return -1

    def use_with_arg(self, state: State, card_index, *args):
        return None

    @property
    def card_type(self):
        return ""


class SpellCard(Card):
    def card_type(self):
        return CARD_SPELL


class MinionCard(Card):
    def card_type(self):
        return CARD_MINION


class WeaponCard(Card):
    def card_type(self):
        return CARD_WEAPON


class ArmorVendor(MinionCard):
    def __init__(self):
        super().__init__()
        self.name = "护甲商贩"
        self.cost = 1

    def best_arg(self, state: State):
        # 格子满了
        if state.mine_num == 7:
            return -1, 0
        else:
            return 2, state.mine_num

    def use_with_arg(self, state: State, card_index, *args):
        gap_index = args[0]
        click.choose_card(card_index, state.card_num)
        click.put_minion(gap_index, state.mine_num)


class HolySmite(SpellCard):
    def __init__(self):
        super().__init__()
        self.name = "神圣惩击"
        self.cost = 1

    def best_arg(self, state: State):
        best_oppo_index = -1
        best_delta_h = 0

        for oppo_index in range(len(state.oppos)):
            oppo_minion = state.oppos[oppo_index]
            # 加个bias让它省着点牌用
            bias = -4
            temp_delta_h = oppo_minion.delta_h_after_damage(3) + bias
            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index

    def use_with_arg(self, state: State, card_index, *args):
        oppo_index = args[0]
        click.choose_card(card_index, state.card_num)
        click.choose_opponent_minion(oppo_index, state.oppo_num)