import random
import time
from abc import ABC, abstractmethod
import click
from constants.constants import *
from print_info import *


class Card(ABC):
    # 用来指示是否在留牌阶段把它留下, 默认留下
    # 在 keep_in_hand 中返回
    keep_in_hand_bool = True

    @classmethod
    def keep_in_hand(cls, state, hand_card_index):
        return cls.keep_in_hand_bool

    # 用来指示这张卡的价值, 在 best_h_and_arg 中返回.
    # 如果为 0 则代表未设置, 会根据卡牌费用等信息区估算价值.
    # 一些功能卡不能用一个简单的数值去评判价值, 应针对其另写
    # 函数
    value = 0

    # 返回两个东西,第一项是使用这张卡的\delta h,
    # 之后是是用这张卡的最佳参数,参数数目不定
    # 参数是什么呢,比如一张火球术,参数就是指示你
    # 是要打脸还是打怪
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.value,

    @classmethod
    @abstractmethod
    def use_with_arg(cls, state, card_index, *args):
        pass

    @classmethod
    @abstractmethod
    def get_card_type(cls):
        pass


class SpellCard(Card):
    wait_time = BASIC_SPELL_WAIT_TIME

    @classmethod
    def get_card_type(cls):
        return CARD_SPELL


class SpellNoPoint(SpellCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        click.choose_and_use_spell(card_index, state.my_hand_card_num)
        click.cancel_click()
        time.sleep(cls.wait_time)


class SpellPointOppo(SpellCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        if len(args) == 0:
            hand_card = state.my_hand_cards[card_index]
            warn_print(f"Receive 0 args in using SpellPointOppo card {hand_card.name}")
            return

        oppo_index = args[0]
        click.choose_card(card_index, state.my_hand_card_num)
        if oppo_index >= 0:
            click.choose_opponent_minion(oppo_index, state.oppo_minion_num)
        else:
            click.choose_oppo_hero()
        click.cancel_click()
        time.sleep(cls.wait_time)


class SpellPointMine(SpellCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        if len(args) == 0:
            hand_card = state.my_hand_cards[card_index]
            warn_print(f"Receive 0 args in using SpellPointMine card {hand_card.name}")
            return

        mine_index = args[0]
        click.choose_card(card_index, state.my_hand_card_num)
        click.choose_my_minion(mine_index, state.oppo_minion_num)
        click.cancel_click()
        time.sleep(cls.wait_time)


class MinionCard(Card):
    @classmethod
    def get_card_type(cls):
        return CARD_MINION

    @classmethod
    def basic_delta_h(cls, state, hand_card_index):
        if state.my_minion_num >= 7:
            return -1000
        else:
            return 0

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        if cls.value != 0:
            return cls.value, state.my_minion_num
        else:
            # 费用越高的应该越厉害吧
            hand_card = state.my_hand_cards[hand_card_index]
            return hand_card.current_cost / 2 + 1, \
                   state.my_minion_num  # 默认放到最右边

    @classmethod
    def combo_delta_h(cls, state, hand_card_index):
        return 0

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        delta_h, *args = cls.utilize_delta_h_and_arg(state, hand_card_index)
        delta_h += cls.basic_delta_h(state, hand_card_index)
        delta_h += cls.combo_delta_h(state, hand_card_index)
        return (delta_h,) + tuple(args)


class MinionNoPoint(MinionCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        gap_index = args[0]
        click.choose_card(card_index, state.my_hand_card_num)
        click.put_minion(gap_index, state.my_minion_num)
        click.cancel_click()
        time.sleep(BASIC_MINION_PUT_INTERVAL)


class MinionPointOppo(MinionCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        gap_index = args[0]
        oppo_index = args[1]

        click.choose_card(card_index, state.my_hand_card_num)
        click.put_minion(gap_index, state.my_minion_num)
        if oppo_index >= 0:
            click.choose_opponent_minion(oppo_index, state.oppo_minion_num)
        else:
            click.choose_oppo_hero()
        click.cancel_click()
        time.sleep(BASIC_MINION_PUT_INTERVAL)


class MinionPointMine(MinionCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        gap_index = args[0]
        oppo_index = args[1]

        click.choose_card(card_index, state.my_hand_card_num)
        click.put_minion(gap_index, state.my_minion_num)
        if oppo_index >= 0:
            click.choose_my_minion(oppo_index, state.oppo_minion_num)
        else:
            click.choose_my_hero()
        click.cancel_click()
        time.sleep(BASIC_MINION_PUT_INTERVAL)


class WeaponCard(Card):
    @classmethod
    def get_card_type(cls):
        return CARD_WEAPON

    # TODO: 还什么都没实现...


class HeroPowerCard(Card):
    @classmethod
    def get_card_type(cls):
        return CARD_HERO_POWER


# 幸运币
class Coin(SpellNoPoint):
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0

        for another_index, hand_card in enumerate(state.my_hand_cards):
            delta_h = 0

            if hand_card.current_cost != state.my_last_mana + 1:
                continue
            if hand_card.is_coin:
                continue

            detail_card = hand_card.detail_card
            if detail_card is None:
                if hand_card.cardtype == CARD_MINION and not hand_card.battlecry:
                    delta_h = MinionNoPoint.best_h_and_arg(state, another_index)[0]
            else:
                delta_h = detail_card.best_h_and_arg(state, another_index)[0]

            delta_h -= 2  # 如果跳费之后能使用的卡显著强于不跳费的卡, 就跳币
            best_delta_h = max(best_delta_h, delta_h)

        return best_delta_h,
