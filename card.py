import random
import time

import click
from constants.constants import *
from print_info import *
from constants.card_name import *


class Card:
    def __init__(self):
        self.name = ""
        self.cost = 0

    # 返回两个东西,第一项是使用这张卡的\delta h,
    # 之后是是用这张卡的最佳参数,参数数目不定
    # 参数是什么呢,比如一张火球术,参数就是指示你
    # 是要打脸还是打怪
    def best_h_and_arg(self, state):
        return -1

    def use_with_arg(self, state, card_index, *args):
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

    def use_with_arg(self, state, card_index, *args):
        if self.spell_type == "":
            warning_print(f"Spell card {self.name} does not been assigned spell type!")
            return

        if self.spell_type == SPELL_NO_POINT:
            click.choose_and_use_spell(card_index, state.my_hand_card_num)
            click.cancel_click()
            time.sleep(self.wait_time)
            return

        if self.spell_type == SPELL_POINT_OPPO:
            if len(args) == 0:
                warning_print(f"Spell {self.name} should use with one arg!")
                return

            oppo_index = args[0]
            click.choose_card(card_index, state.my_hand_card_num)
            click.choose_opponent_minion(oppo_index, state.oppo_minion_num)
            click.cancel_click()
            time.sleep(self.wait_time)
            return

        if self.spell_type == SPELL_POINT_MINE:
            if len(args) == 0:
                warning_print(f"Spell {self.name} should use with one arg!")
                return

            mine_index = args[0]
            click.choose_card(card_index, state.my_hand_card_num)
            click.choose_my_minion(mine_index, state.oppo_minion_num)
            click.cancel_click()
            time.sleep(self.wait_time)
            return

        warning_print(f"{self.name} has unknown spell type: {self.spell_type}")


class Coin(SpellCard):
    def __init__(self):
        super(Coin, self).__init__()
        self.spell_type = SPELL_NO_POINT


class MinionCard(Card):
    def card_type(self):
        return CARD_MINION


class BasicMinionCard(MinionCard):
    def __init__(self):
        super(BasicMinionCard, self).__init__()
        self.value = 0

    def best_h_and_arg(self, state):
        # 格子满了
        if state.my_minion_num == 7:
            return -1, 0
        else:
            # 默认放到最右边
            return self.value, state.my_minion_num

    def use_with_arg(self, state, card_index, *args):
        gap_index = args[0]
        click.choose_card(card_index, state.my_hand_card_num)
        click.put_minion(gap_index, state.my_minion_num)
        click.cancel_click()
        time.sleep(BASIC_MINION_PUT_INTERVAL)


class WeaponCard(Card):
    def card_type(self):
        return CARD_WEAPON

    # TODO: 还什么都没实现...


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
        # 加个bias,一是包含了消耗的水晶的代价，二是包含了消耗了手牌的代价
        self.bias = -2

    def best_h_and_arg(self, state):
        best_oppo_index = -1
        best_delta_h = 0

        for oppo_index in range(state.oppo_minion_num):
            oppo_minion = state.oppo_minions[oppo_index]
            temp_delta_h = oppo_minion.delta_h_after_damage(3) + self.bias
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
        self.bias = -4

    def best_h_and_arg(self, state):
        tmp = 0

        for minion in state.oppo_minions:
            tmp += minion.attack - 1

        return tmp + self.bias,


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
        self.bias = -6

    def best_h_and_arg(self, state):
        best_oppo_index = -1
        best_delta_h = 0

        for i in range(state.oppo_minion_num):

            minion = state.oppo_minions[i]
            if minion.attack < 5:
                continue

            tmp = minion.attack + minion.health + self.bias
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_oppo_index = i

        return best_delta_h, best_oppo_index


class Apotheosis(SpellCard):
    def __init__(self):
        super().__init__()
        self.name = "神圣化身"
        self.cost = 3
        self.spell_type = SPELL_POINT_MINE
        self.bias = -6

    def best_h_and_arg(self, state):
        best_delta_h = 0
        best_mine_index = -1

        for i in range(state.my_minion_num):
            minion = state.my_minions[i]
            tmp = self.bias + 3 + (minion.health + 2) / 4 + \
                  (minion.attack + 1) / 2
            if minion.can_attack_minion:
                tmp += minion.attack / 4
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_mine_index = i

        return best_delta_h, best_mine_index


class DeathsHeadCultist(BasicMinionCard):
    def __init__(self):
        super().__init__()
        self.name = "亡首教徒"
        self.cost = 3
        self.value = 1


class DevouringPlague(SpellCard):
    def __init__(self):
        super().__init__()
        self.name = "噬灵疫病"
        self.cost = 3
        self.spell_type = SPELL_NO_POINT
        self.wait_time = 4
        self.bias = -4  # 把吸的血直接算进bias

    def best_h_and_arg(self, state):
        h = state.heuristic_value

        sum = 0
        sample_times = 5

        for i in range(sample_times):
            tmp_state = state.copy_new_one()
            for j in range(4):
                tmp_state.random_distribute_damage(1, [i for i in range(tmp_state.oppo_minion_num)], [])

            sum += tmp_state.heuristic_value - h

        return sum / sample_times + self.bias,


class OverconfidentOrc(BasicMinionCard):
    def __init__(self):
        super().__init__()
        self.name = "狂傲的兽人"
        self.cost = 3
        self.value = 3


class HolyNova(SpellCard):
    def __init__(self):
        super().__init__()
        self.name = "神圣新星"
        self.cost = 4
        self.spell_type = SPELL_NO_POINT
        self.bias = -8

    def best_h_and_arg(self, state):
        return self.bias + sum([minion.delta_h_after_damage(2)
                                for minion in state.oppo_minions]),


class Hysteria(SpellCard):
    def __init__(self):
        super(Hysteria, self).__init__()
        self.name = "狂乱"
        self.cost = 4
        self.wait_time = 5
        self.spell_type = SPELL_POINT_OPPO
        self.bias = -9  # 我觉得狂乱应该要能力挽狂澜

    def best_h_and_arg(self, state):
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

        return best_delta_h + self.bias, best_arg


class ShadowWordRuin(SpellCard):
    def __init__(self):
        super(ShadowWordRuin, self).__init__()
        self.name = "暗言术毁"
        self.cost = 4
        self.spell_type = SPELL_NO_POINT
        self.bias = -8

    def best_h_and_arg(self, state):
        return self.bias + sum([minion.attack + minion.health
                                for minion in state.oppo_minions
                                if minion.attack >= 5]),


class AgainstAllOdds(SpellCard):
    def __init__(self):
        super(AgainstAllOdds, self).__init__()
        self.name = "除奇致胜"
        self.cost = 5
        self.spell_type = SPELL_NO_POINT
        self.bias = -9

    def best_h_and_arg(self, state):
        return self.bias + \
               sum([minion.attack + minion.health
                    for minion in state.oppo_minions
                    if minion.attack % 2 == 1]) - \
               sum([minion.attack + minion.health
                    for minion in state.my_minions
                    if minion.attack % 2 == 1]),


class RuststeedRaider(BasicMinionCard):
    def __init__(self):
        super(RuststeedRaider, self).__init__()
        self.name = "锈骑劫匪"
        self.cost = 5
        self.value = 3
        # TODO: 也许我可以为突袭随从专门写一套价值评判?


class TaelanFordring(BasicMinionCard):
    def __init__(self):
        super(TaelanFordring, self).__init__()
        self.name = "泰兰佛丁"
        self.cost = 5
        self.value = 3


class CairneBloodhoof(BasicMinionCard):
    def __init__(self):
        super(CairneBloodhoof, self).__init__()
        self.name = "凯恩血蹄"
        self.cost = 6
        self.value = 6


class MutanusTheDevourer(BasicMinionCard):
    def __init__(self):
        super(MutanusTheDevourer, self).__init__()
        self.name = "吃手手鱼"
        self.cost = 7
        self.value = 5


class SoulMirror(SpellCard):
    def __init__(self):
        super(SoulMirror, self).__init__()
        self.name = "灵魂之镜"
        self.cost = 7
        self.spell_type = SPELL_NO_POINT
        self.wait_time = 5
        self.bias = -16

    def best_h_and_arg(self, state):
        copy_number = min(7 - state.my_minion_num, state.oppo_minion_num)
        sum = 0
        for i in range(copy_number):
            sum += state.oppo_minions[i].attack + state.oppo_minions[i].health

        return sum + self.bias,


class BloodOfGhuun(BasicMinionCard):
    def __init__(self):
        super(BloodOfGhuun, self).__init__()
        self.name = "戈霍恩之血"
        self.cost = 9
        self.value = 8
