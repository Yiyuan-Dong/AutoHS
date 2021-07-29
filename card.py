import random
import time
from abc import ABC, abstractmethod

import click
from constants.constants import *
from print_info import *


class Card(ABC):
    value = 0

    # 返回两个东西,第一项是使用这张卡的\delta h,
    # 之后是是用这张卡的最佳参数,参数数目不定
    # 参数是什么呢,比如一张火球术,参数就是指示你
    # 是要打脸还是打怪
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        if not value:
            return cls.value,
        else:
            return value,

    @classmethod
    @abstractmethod
    def use_with_arg(cls, state, card_index, *args):
        pass

    @classmethod
    @abstractmethod
    def get_card_type(cls):
        pass


class SpellCard(Card):
    wait_time = 1.5

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
            warning_print(f"Spell {hand_card.name} should use with one arg!")
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
            warning_print(f"Spell {hand_card.name} should use with one arg!")
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


class MinionNoPoint(MinionCard):
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        # 格子满了
        if state.my_minion_num == 7:
            return -1, 0
        elif cls.value != 0:
            return cls.value, state.my_minion_num
        else:
            hand_card = state.my_hand_cards[hand_card_index]
            # 在什么都不知道的时候, 认为费用越高的卡应该越超模
            return hand_card.current_cost / 2 + 1, state.my_minion_num  # 默认放到最右边

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


class WeaponCard(Card):
    @classmethod
    def get_card_type(cls):
        return CARD_WEAPON

    # TODO: 还什么都没实现...


# 幸运币
class Coin(SpellNoPoint):
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        best_delta_h = 0

        for another_index, hand_card in enumerate(state.my_hand_cards):
            delta_h = 0

            if hand_card.current_cost != state.my_last_mana + 1:
                continue
            if hand_card.is_coin:
                continue

            detail_card = hand_card.detail_card
            debug_print(hand_card.name)
            if detail_card is None:
                if hand_card.cardtype == CARD_MINION and not hand_card.battlecry:
                    debug_print(hand_card.name)
                    delta_h = MinionNoPoint.best_h_and_arg(state, another_index)[0]
            else:
                delta_h = detail_card.best_h_and_arg(state, another_index)[0]

            delta_h -= 1  # 如果跳费之后能使用的卡显著强于不跳费的卡, 就跳币
            best_delta_h = max(best_delta_h, delta_h)

        return best_delta_h,


# 护甲商贩
class ArmorVendor(MinionNoPoint):
    value = 2


# 神圣惩击
class HolySmite(SpellPointOppo):
    wait_time = 2
    # 加个bias,一是包含了消耗的水晶的代价，二是包含了消耗了手牌的代价
    bias = -2

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        best_oppo_index = -1
        best_delta_h = 0

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            temp_delta_h = oppo_minion.delta_h_after_damage(3) + cls.bias
            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index


# 倦怠光波
class WaveOfApathy(SpellNoPoint):
    wait_time = 2
    bias = -4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        tmp = 0

        for minion in state.oppo_minions:
            tmp += minion.attack - 1

        return tmp + cls.bias,


# 噬骨殴斗者
class BonechewerBrawler(MinionNoPoint):
    value = 2


# 暗言术灭
class ShadowWordDeath(SpellPointOppo):
    wait_time = 1.5
    bias = -6

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        best_oppo_index = -1
        best_delta_h = 0

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if oppo_minion.attack < 5:
                continue

            tmp = oppo_minion.heuristic_val + cls.bias
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index


# 神圣化身
class Apotheosis(SpellPointMine):
    bias = -6

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        best_delta_h = 0
        best_mine_index = -1

        for my_index, my_minion in enumerate(state.my_minions):
            tmp = cls.bias + 3 + (my_minion.health + 2) / 4 + \
                  (my_minion.attack + 1) / 2
            if my_minion.can_attack_minion:
                tmp += my_minion.attack / 4
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_mine_index = my_index

        return best_delta_h, best_mine_index


# 亡首教徒
class DeathsHeadCultist(MinionNoPoint):
    value = 1


# 噬灵疫病
class DevouringPlague(SpellNoPoint):
    wait_time = 4
    bias = -4  # 把吸的血直接算进bias

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        curr_h = state.heuristic_value

        delta_h_sum = 0
        sample_times = 5

        for i in range(sample_times):
            tmp_state = state.copy_new_one()
            for j in range(4):
                tmp_state.random_distribute_damage(1, [i for i in range(tmp_state.oppo_minion_num)], [])

            delta_h_sum += tmp_state.heuristic_value - curr_h

        return delta_h_sum / sample_times + cls.bias,


# 狂傲的兽人
class OverconfidentOrc(MinionNoPoint):
    value = 3


# 神圣新星
class HolyNova(SpellNoPoint):
    bias = -8

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        return cls.bias + sum([minion.delta_h_after_damage(2)
                               for minion in state.oppo_minions]),


# 狂乱
class Hysteria(SpellPointOppo):
    wait_time = 5
    bias = -9  # 我觉得狂乱应该要能力挽狂澜

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        best_delta_h = 0
        best_arg = 0
        sample_times = 10

        if state.oppo_minion_num == 0 or state.oppo_minion_num + state.my_minion_num == 1:
            return 0, -1

        for chosen_index in range(state.oppo_minion_num):
            delta_h_count = 0

            for i in range(sample_times):
                tmp_state = state.copy_new_one()
                chosen_minion = tmp_state.oppo_minions[chosen_index]
                tmp_chosen_index = chosen_index

                while True:
                    another_index_list = [j for j in range(tmp_state.oppo_minion_num + tmp_state.my_minion_num)]
                    another_index_list.pop(tmp_chosen_index)
                    if len(another_index_list) == 0:
                        break
                    another_index = another_index_list[random.randint(0, len(another_index_list) - 1)]

                    # print("another index: ", another_index)
                    if another_index >= tmp_state.oppo_minion_num:
                        another_minion = tmp_state.my_minions[another_index - tmp_state.oppo_minion_num]
                        if another_minion.get_damaged(chosen_minion.attack):
                            tmp_state.my_minions.pop(another_index - tmp_state.oppo_minion_num)
                    else:
                        another_minion = tmp_state.oppo_minions[another_index]
                        if another_minion.get_damaged(chosen_minion.attack):
                            tmp_state.oppo_minions.pop(another_index)
                            if another_index < tmp_chosen_index:
                                tmp_chosen_index -= 1

                    if chosen_minion.get_damaged(another_minion.attack):
                        # print("h:", tmp_state.heuristic_value, state.heuristic_value)
                        tmp_state.oppo_minions.pop(tmp_chosen_index)
                        break

                    # print("h:", tmp_state.heuristic_value, state.heuristic_value)

                delta_h_count += tmp_state.heuristic_value - state.heuristic_value

            delta_h_count /= sample_times
            # print("average delta_h:", delta_h_count)
            if delta_h_count > best_delta_h:
                best_delta_h = delta_h_count
                best_arg = chosen_index

        return best_delta_h + cls.bias, best_arg


# 暗言术毁
class ShadowWordRuin(SpellNoPoint):
    bias = -8

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        return cls.bias + sum([minion.heuristic_val
                               for minion in state.oppo_minions
                               if minion.attack >= 5]),


# 除奇致胜
class AgainstAllOdds(SpellNoPoint):
    bias = -9

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        return cls.bias + \
               sum([minion.heuristic_val
                    for minion in state.oppo_minions
                    if minion.attack % 2 == 1]) - \
               sum([minion.heuristic_val
                    for minion in state.my_minions
                    if minion.attack % 2 == 1]),


# 锈骑劫匪
class RuststeedRaider(MinionNoPoint):
    value = 3
    # TODO: 也许我可以为突袭随从专门写一套价值评判?


# 泰兰佛丁
class TaelanFordring(MinionNoPoint):
    value = 3


# 凯恩血蹄
class CairneBloodhoof(MinionNoPoint):
    value = 6


# 吃手手鱼
class MutanusTheDevourer(MinionNoPoint):
    value = 5


# 灵魂之镜
class SoulMirror(SpellNoPoint):
    wait_time = 5
    bias = -16

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        copy_number = min(7 - state.my_minion_num, state.oppo_minion_num)
        h_sum = 0
        for i in range(copy_number):
            h_sum += state.oppo_minions[i].heuristic_val

        return h_sum + cls.bias,


# 戈霍恩之血
class BloodOfGhuun(MinionNoPoint):
    value = 8


# 闪电箭
class LightingBolt(SpellPointOppo):
    spell_type = SPELL_POINT_OPPO
    bias = -4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        best_delta_h = 0
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            delta_h = oppo_minion.delta_h_after_damage(3)
            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,


# 呱
class Hex(SpellPointOppo):
    bias = -8

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        best_delta_h = 0
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            delta_h = oppo_minion.heuristic_val - 1

            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,


# 闪电风暴
class LightningStorm(SpellNoPoint):
    bias = - 10

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        h_sum = 0
        for oppo_minion in state.oppo_minions:
            h_sum += (oppo_minion.delta_h_after_damage(2) +
                      oppo_minion.delta_h_after_damage(3)) / 2

        return h_sum + cls.bias,


# TC130
class MindControlTech(MinionNoPoint):
    value = 1

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        if state.oppo_minion_num < 4:
            return cls.value, state.my_minion_num
        else:
            h_sum = sum([minion.heuristic_val for minion in state.oppo_minions])
            h_sum /= state.oppo_minion_num
            return cls.value + h_sum * 2, state.my_minion_num


# 　野性狼魂
class FeralSpirit(SpellNoPoint):
    value = 4


# 碧蓝幼龙
class AzureDrake(MinionNoPoint):
    value = 4


# 奥妮克希亚
class Onyxia(MinionNoPoint):
    value = 10


# 火元素
class FireElemental(MinionPointOppo):
    def best_h_and_arg(cls, state, hand_card_index, value=0):
        best_h = 3 + state.oppo_hero.delta_h_after_damage(3)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            delta_h = 3 + oppo_minion.delta_h_after_damage(3)
            if delta_h > best_h:
                best_h = delta_h
                best_oppo_index = oppo_index

        return best_h, state.my_minion_num, best_oppo_index
