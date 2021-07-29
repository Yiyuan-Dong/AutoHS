import random
import time

import click
from constants.constants import *
from print_info import *


class Card:
    name = "Unknown"
    cost = 0

    # 返回两个东西,第一项是使用这张卡的\delta h,
    # 之后是是用这张卡的最佳参数,参数数目不定
    # 参数是什么呢,比如一张火球术,参数就是指示你
    # 是要打脸还是打怪
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return -1

    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        return None

    @classmethod
    def get_card_type(cls):
        return CARD_BASE


class SpellCard(Card):
    spell_type = ""
    wait_time = 2

    @classmethod
    def get_card_type(cls):
        return CARD_SPELL

    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        if cls.spell_type == "":
            warning_print(f"Spell card {cls.name} does not been assigned spell type!")
            return

        if cls.spell_type == SPELL_NO_POINT:
            click.choose_and_use_spell(card_index, state.my_hand_card_num)
            click.cancel_click()
            time.sleep(cls.wait_time)
            return

        if cls.spell_type == SPELL_POINT_OPPO:
            if len(args) == 0:
                warning_print(f"Spell {cls.name} should use with one arg!")
                return

            oppo_index = args[0]
            click.choose_card(card_index, state.my_hand_card_num)
            click.choose_opponent_minion(oppo_index, state.oppo_minion_num)
            click.cancel_click()
            time.sleep(cls.wait_time)
            return

        if cls.spell_type == SPELL_POINT_MINE:
            if len(args) == 0:
                warning_print(f"Spell {cls.name} should use with one arg!")
                return

            mine_index = args[0]
            click.choose_card(card_index, state.my_hand_card_num)
            click.choose_my_minion(mine_index, state.oppo_minion_num)
            click.cancel_click()
            time.sleep(cls.wait_time)
            return

        warning_print(f"{cls.name} has unknown spell type: {cls.spell_type}")


class Coin(SpellCard):
    spell_type = SPELL_NO_POINT

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0

        for another_index in range(state.my_hand_card_num):
            delta_h = 0
            hand_card = state.my_hand_cards[another_index]

            if hand_card.current_cost != state.my_last_mana + 1:
                continue
            if hand_card.is_coin:
                continue

            detail_card = hand_card.detail_card
            debug_print(hand_card.name)
            if detail_card is None:
                if hand_card.cardtype == CARD_MINION and not hand_card.battlecry:
                    debug_print(hand_card.name)
                    delta_h = BasicMinionCard.best_h_and_arg(state, another_index)[0]
            else:
                delta_h = detail_card.best_h_and_arg(state, another_index)[0]

            delta_h -= 1  # 如果跳费之后能使用的卡显著强于不跳费的卡, 就跳币
            best_delta_h = max(best_delta_h, delta_h)

        return best_delta_h,


class MinionCard(Card):
    @classmethod
    def get_card_type(cls):
        return CARD_MINION


class BasicMinionCard(MinionCard):
    value = -1  # -1代表默认值, 此时具体价值视手牌而定

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        # 格子满了
        if state.my_minion_num == 7:
            return -1, 0
        elif cls.value != -1:
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


class WeaponCard(Card):
    @classmethod
    def get_card_type(cls):
        return CARD_WEAPON

    # TODO: 还什么都没实现...


class ArmorVendor(BasicMinionCard):
    name = "护甲商贩"
    cost = 1
    value = 2


class HolySmite(SpellCard):
    name = "神圣惩击"
    cost = 1
    spell_type = SPELL_POINT_OPPO
    wait_time = 2
    # 加个bias,一是包含了消耗的水晶的代价，二是包含了消耗了手牌的代价
    bias = -2

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0

        for oppo_index in range(state.oppo_minion_num):
            oppo_minion = state.oppo_minions[oppo_index]
            temp_delta_h = oppo_minion.delta_h_after_damage(3) + cls.bias
            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index


class WaveOfApathy(SpellCard):
    name = "倦怠光波"
    cost = 1
    spell_type = SPELL_NO_POINT
    wait_time = 2
    bias = -4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        tmp = 0

        for minion in state.oppo_minions:
            tmp += minion.attack - 1

        return tmp + cls.bias,


class BonechewerBrawler(BasicMinionCard):
    name = "噬骨斗殴者"
    cost = 2
    value = 2


class ShadowWordDeath(SpellCard):
    name = "暗言术灭"
    cost = 2
    spell_type = SPELL_POINT_OPPO
    wait_time = 1.5
    bias = -6

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0

        for i in range(state.oppo_minion_num):

            minion = state.oppo_minions[i]
            if minion.attack < 5:
                continue

            tmp = minion.attack + minion.health + cls.bias
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_oppo_index = i

        return best_delta_h, best_oppo_index


class Apotheosis(SpellCard):
    name = "神圣化身"
    cost = 3
    spell_type = SPELL_POINT_MINE
    bias = -6

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0
        best_mine_index = -1

        for i in range(state.my_minion_num):
            minion = state.my_minions[i]
            tmp = cls.bias + 3 + (minion.health + 2) / 4 + \
                  (minion.attack + 1) / 2
            if minion.can_attack_minion:
                tmp += minion.attack / 4
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_mine_index = i

        return best_delta_h, best_mine_index


class DeathsHeadCultist(BasicMinionCard):
    name = "亡首教徒"
    cost = 3
    value = 1


class DevouringPlague(SpellCard):
    name = "噬灵疫病"
    cost = 3
    spell_type = SPELL_NO_POINT
    wait_time = 4
    bias = -4  # 把吸的血直接算进bias

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        h = state.heuristic_value

        sum = 0
        sample_times = 5

        for i in range(sample_times):
            tmp_state = state.copy_new_one()
            for j in range(4):
                tmp_state.random_distribute_damage(1, [i for i in range(tmp_state.oppo_minion_num)], [])

            sum += tmp_state.heuristic_value - h

        return sum / sample_times + cls.bias,


class OverconfidentOrc(BasicMinionCard):
    name = "狂傲的兽人"
    cost = 3
    value = 3


class HolyNova(SpellCard):
    name = "神圣新星"
    cost = 4
    spell_type = SPELL_NO_POINT
    bias = -8

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.bias + sum([minion.delta_h_after_damage(2)
                               for minion in state.oppo_minions]),


class Hysteria(SpellCard):
    name = "狂乱"
    cost = 4
    wait_time = 5
    spell_type = SPELL_POINT_OPPO
    bias = -9  # 我觉得狂乱应该要能力挽狂澜

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
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


class ShadowWordRuin(SpellCard):
    name = "暗言术毁"
    cost = 4
    spell_type = SPELL_NO_POINT
    bias = -8

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.bias + sum([minion.attack + minion.health
                               for minion in state.oppo_minions
                               if minion.attack >= 5]),


class AgainstAllOdds(SpellCard):
    name = "除奇致胜"
    cost = 5
    spell_type = SPELL_NO_POINT
    bias = -9

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.bias + \
               sum([minion.attack + minion.health
                    for minion in state.oppo_minions
                    if minion.attack % 2 == 1]) - \
               sum([minion.attack + minion.health
                    for minion in state.my_minions
                    if minion.attack % 2 == 1]),


class RuststeedRaider(BasicMinionCard):
    name = "锈骑劫匪"
    cost = 5
    value = 3
    # TODO: 也许我可以为突袭随从专门写一套价值评判?


class TaelanFordring(BasicMinionCard):
    name = "泰兰佛丁"
    cost = 5
    value = 3


class CairneBloodhoof(BasicMinionCard):
    name = "凯恩血蹄"
    cost = 6
    value = 6


class MutanusTheDevourer(BasicMinionCard):
    name = "吃手手鱼"
    cost = 7
    value = 5


class SoulMirror(SpellCard):
    name = "灵魂之镜"
    cost = 7
    spell_type = SPELL_NO_POINT
    wait_time = 5
    bias = -16

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        copy_number = min(7 - state.my_minion_num, state.oppo_minion_num)
        h_sum = 0
        for i in range(copy_number):
            h_sum += state.oppo_minions[i].attack + state.oppo_minions[i].health

        return h_sum + cls.bias,


class BloodOfGhuun(BasicMinionCard):
    name = "戈霍恩之血"
    cost = 9
    value = 8
