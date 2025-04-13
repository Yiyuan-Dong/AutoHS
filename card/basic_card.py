import random
import time
from abc import ABC, abstractmethod
import click
from constants.state_and_key import *
from config import autohs_config
from autohs_logger import *

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
    wait_time = autohs_config.basic_spell_wait_time

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
            logger.warning(f"Receive 0 args in using SpellPointOppo card {hand_card.name}")
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
            logger.warning(f"Receive 0 args in using SpellPointMine card {hand_card.name}")
            return

        mine_index = args[0]
        click.choose_card(card_index, state.my_hand_card_num)
        click.choose_my_minion(mine_index, state.my_minion_num)
        click.cancel_click()
        time.sleep(cls.wait_time)


class MinionCard(Card):
    # 有的随从带有光环，其价值不仅仅由身材决定，所以加上一个偏移量
    live_value = 0

    @classmethod
    def get_card_type(cls):
        return CARD_MINION

    @classmethod
    def basic_delta_h(cls, state, hand_card_index):
        if state.my_minion_num >= 7:
            return -20000
        else:
            return 0

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        if cls.value != 0:
            return cls.value, state.my_minion_num
        else:
            # 费用越高的应该越厉害吧
            hand_card = state.my_hand_cards[hand_card_index]
            delta_h = hand_card.current_cost / 2 + 1

            if state.my_hero.health <= 10 and hand_card.taunt:
                delta_h *= 1.5

            return delta_h, state.my_minion_num  # 默认放到最右边

    @classmethod
    def combo_delta_h(cls, state, hand_card_index):
        h_sum = 0
        hand_card = state.my_hand_cards[hand_card_index]

        for my_minion in state.my_minions:
            # 有末日就别下怪了
            if my_minion.card_id in ["VAN_NEW1_021", "CORE_NEW1_021", "NEW1_021"]:
                h_sum += -1000

            # 有飞刀可以多下怪
            if my_minion.card_id == ["VAN_NEW1_019", "NEW1_019"]:
                h_sum += 0.5

        # 海盗可以把空降歹徒拉下来
        for my_hand_card_id, my_hand_card in enumerate(state.my_hand_cards):
            if hand_card.is_pirate and my_hand_card.card_id == "DRG_056" and my_hand_card_id != hand_card_index:
                logger.debug(f"{my_hand_card.name} 可以配合 {hand_card.name}")
                h_sum += 2

        return h_sum

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        delta_h, *args = cls.utilize_delta_h_and_arg(state, hand_card_index)
        if len(args) == 0:
            args = [state.my_minion_num]

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
        time.sleep(autohs_config.basic_minion_put_interval)


class MinionPointOppo(MinionCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        if len(args) <= 1:
            logger.warning(f"Receive {len(args)} args in using MinionPointOppo card {state.my_hand_cards[card_index].name}")

        gap_index = args[0] if len(args) > 0 else state.my_minion_num
        oppo_index = args[1] if len(args) > 1 else -1


        click.choose_card(card_index, state.my_hand_card_num)
        click.put_minion(gap_index, state.my_minion_num)
        if oppo_index >= 0:
            click.choose_opponent_minion(oppo_index, state.oppo_minion_num)
        else:
            click.choose_oppo_hero()
        click.cancel_click()
        time.sleep(autohs_config.basic_minion_put_interval)


class MinionPointMine(MinionCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        gap_index = args[0]
        my_index = args[1]

        click.choose_card(card_index, state.my_hand_card_num)
        click.put_minion(gap_index, state.my_minion_num)
        if my_index >= 0:
            # 这时这个随从已经在场上了, 其他随从已经移位了
            click.choose_my_minion(my_index, state.my_minion_num + 1)
        else:
            click.choose_my_hero()
        click.cancel_click()
        time.sleep(autohs_config.basic_minion_put_interval)


class WeaponCard(Card):
    @classmethod
    def get_card_type(cls):
        return CARD_WEAPON

    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        click.choose_and_use_spell(card_index, state.my_hand_card_num)
        click.cancel_click()
        time.sleep(autohs_config.basic_weapon_wait_time)

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        if state.my_weapon:
            return 0,
        else:
            return cls.value,
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

            if hand_card.current_cost != state.my_remaining_mana + 1:
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
