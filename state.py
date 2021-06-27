import copy
import time
from minion import Minion
import click
import get_screen
import keyboard
import sys
import random
from name2card import NAME2CARD
from constants.card_name import *
from print_info import *


class State:
    def __init__(self):
        self.available = []
        self.oppos = []
        self.mines = []

        self.update_minions()

        tmp_card_num = get_screen.count_my_cards()
        self.cards = get_screen.identify_cards(tmp_card_num)

        self.debug_print_out()

    def update_minions(self):
        img = get_screen.catch_screen()
        tmp_oppo_num, tmp_mine_num = get_screen.count_minions(img)
        oppo_ah, mine_ah = get_screen.get_attack_health(img, tmp_oppo_num, tmp_mine_num)
        oppo_t, mine_t = get_screen.test_taunt(img, tmp_oppo_num, tmp_mine_num)

        oppo_ds, mine_ds = get_screen.test_divine_shield()
        if len(oppo_ds) != tmp_oppo_num:
            oppo_ds = [False for i in range(tmp_oppo_num)]
        if len(mine_ds) != tmp_mine_num:
            mine_ds = [False for i in range(tmp_mine_num)]

        self.available = get_screen.test_available(img, tmp_mine_num)

        self.oppos = []
        for i in range(tmp_oppo_num):
            self.oppos.append(
                Minion(
                    oppo_ah[i][0],
                    oppo_ah[i][1],
                    oppo_t[i],
                    oppo_ds[i]
                )
            )

        self.mines = []
        for i in range(tmp_mine_num):
            self.mines.append(
                Minion(
                    mine_ah[i][0],
                    mine_ah[i][1],
                    mine_t[i],
                    mine_ds[i]
                )
            )

    def debug_print_out(self):
        if not DEBUG:
            return
        debug_print(f"我有{self.card_num}张手牌,它们分别是")
        debug_print("    " + ", ".join(self.cards))
        debug_print(f"对手有{self.oppo_num}个随从")
        for minion in self.oppos:
            debug_print("    " + str(minion))
        debug_print(f"我有{self.mine_num}个随从")
        for i in range(len(self.mines)):
            minion = self.mines[i]
            tmp_str = "    " + str(minion)
            if self.available[i] == 2:
                tmp_str += " 能打脸"
            elif self.available[i] == 1:
                tmp_str += " 是突袭"
            else:
                tmp_str += " 不能动"
            debug_print(tmp_str)

    @property
    def oppo_num(self):
        return len(self.oppos)

    @property
    def mine_num(self):
        return len(self.mines)

    @property
    def card_num(self):
        return len(self.cards)

    # 用攻血点数之和算启发值(方卡费体系里就是卡费乘2)
    @property
    def oppo_heuristic_value(self):
        h_val = 0
        for minion in self.oppos:
            h_val += minion.attack + minion.health
            if minion.has_divine_shield:
                h_val += minion.attack
        return h_val

    @property
    def mine_heuristic_value(self):
        h_val = 0
        for minion in self.mines:
            h_val += minion.attack + minion.health
            if minion.has_divine_shield:
                h_val += minion.attack
        return h_val

    @property
    def heuristic_value(self):
        return self.mine_heuristic_value - self.oppo_heuristic_value

    @property
    def min_cost(self):
        minium = 100
        for card_name in self.cards:
            if card_name != NAME_THE_COIN and card_name in NAME2CARD:
                minium = min(NAME2CARD[card_name].cost, minium)
        return minium


    def fight_between(self, oppo_index, mine_index):
        oppo_minion = self.oppos[oppo_index]
        mine_minion = self.mines[mine_index]

        if oppo_minion.has_divine_shield:
            oppo_minion.has_divine_shield = False
        else:
            oppo_minion.health -= mine_minion.attack
            if oppo_minion.health <= 0:
                self.oppos.pop(oppo_index)

        if mine_minion.has_divine_shield:
            mine_minion.has_divine_shield = False
        else:
            mine_minion.health -= oppo_minion.attack
            if mine_minion.health <= 0:
                self.mines.pop(mine_index)

    def random_distribute_damage(self, damage, oppo_index_list, mine_index_list):
        if len(oppo_index_list) == len(mine_index_list) == 0:
            return

        random_x = random.randint(0, len(oppo_index_list) + len(mine_index_list) - 1)

        if random_x < len(oppo_index_list):
            oppo_index = oppo_index_list[random_x]
            minion = self.oppos[oppo_index]
            if minion.get_damaged(damage):
                self.oppos.pop(oppo_index)
        else:
            mine_index = mine_index_list[random_x - len(oppo_index_list)]
            minion = self.mines[mine_index]
            if minion.get_damaged(damage):
                self.mines.pop(mine_index)

    def get_best_action(self):
        could_attack_oppos = []
        has_taunt = False

        for i in range(len(self.oppos)):
            if self.oppos[i].is_taunt:
                could_attack_oppos.append(i)
                has_taunt = True

        if not has_taunt:
            could_attack_oppos = [i for i in range(len(self.oppos))]

        max_delta_h_val = 0
        max_my_index = -1
        max_oppo_index = -1

        for my_index in range(len(self.mines)):
            if self.available[my_index] == 0:
                continue
            my_minion = self.mines[my_index]

            for oppo_index in could_attack_oppos:
                oppo_minion = self.oppos[oppo_index]
                tmp_delta_h_val = 0

                tmp_delta_h_val -= my_minion.delta_h_after_damage(oppo_minion.attack)
                tmp_delta_h_val += oppo_minion.delta_h_after_damage(my_minion.attack)

                # 想给过墙行为加一点补正
                if oppo_minion.is_taunt:
                    tmp_delta_h_val += min(oppo_minion.health, my_minion.attack) * 0.5

                if tmp_delta_h_val > max_delta_h_val:
                    max_delta_h_val = tmp_delta_h_val
                    max_my_index = my_index
                    max_oppo_index = oppo_index

                print(my_index, oppo_index, tmp_delta_h_val)
            # 如果没有墙,自己又能打脸,应该试一试
            if not has_taunt:
                if self.available[my_index] == 2 and \
                        my_minion.attack * 0.75 > max_delta_h_val:
                    # *0.75 因为场面更重要
                    max_delta_h_val = my_minion.attack * 0.75
                    max_my_index = my_index
                    max_oppo_index = -1

        return max_my_index, max_oppo_index

    def copy_new_one(self):
        tmp = copy.deepcopy(self)
        for i in range(self.oppo_num):
            tmp.oppos[i] = copy.deepcopy(self.oppos[i])
        for i in range(self.mine_num):
            tmp.mines[i] = copy.deepcopy(self.mines[i])
        return tmp

    def best_h_and_arg_within_mana(self, mana_limit, full_use=False):
        best_delta_h = 0
        best_index = 0
        best_args = []

        for card_index in range(self.card_num):
            card_name = self.cards[card_index]

            if card_name != NAME_THE_COIN and card_name in NAME2CARD:
                card = NAME2CARD[card_name]

                if full_use and card.cost != mana_limit:
                    continue
                if card.cost > mana_limit:
                    continue

                delta_h, *args = card.best_h_and_arg(self)
                debug_print(f"card[{card_index}]({card_name}) delta_h: {delta_h}, *args: {args}")

                if delta_h > best_delta_h:
                    best_delta_h = delta_h
                    best_index = card_index
                    best_args = args

        return best_delta_h, best_index, best_args

    def test_use_coin(self, curr_mana):
        if NAME_THE_COIN not in self.cards:
            return False
        if curr_mana == 10:
            res = False
        else:
            res = self.best_h_and_arg_within_mana(curr_mana + 1, full_use=True)[0] \
                  - self.best_h_and_arg_within_mana(curr_mana)[0] > 3
        if res:
            debug_print("Should use the coin")
        else:
            debug_print("Should not use the coin")

        return res

    def use_coin(self):
        for index in range(self.card_num):
            if self.cards[index] == NAME_THE_COIN:
                debug_print(f"Will use the coin at [{index}]")
                NAME2CARD[NAME_THE_COIN].use_with_arg(self, index)

    # 会返回这张卡的cost
    def use_card(self, index, *args):
        card_name = self.cards[index]
        card = NAME2CARD[card_name]
        debug_print(f"Will use card[{index}] {card.name}")
        card.use_with_arg(self, index, *args)
        self.cards.pop(index)
        return card.cost


if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+q", sys.exit)

    current_mana = 7
    while True:
        time.sleep(0.5)
        state = State()
        if state.test_use_coin(current_mana):
            state.use_coin()
            continue

        delta_h, index, args = state.best_h_and_arg_within_mana(current_mana)
        if delta_h == 0:
            debug_print("Do not want ot use card")
            break
        current_mana -= state.use_card(index, *args)

    while True:
        state.debug_print_out()
        mine_index, oppo_index = state.get_best_action()
        print(f"mine_index: {mine_index}, oppo_index: {oppo_index}")

        time.sleep(2)

        if mine_index == -1:
            break
        if oppo_index == -1:
            click.minion_beat_hero(mine_index, state.mine_num)
        else:
            click.minion_beat_minion(mine_index, state.mine_num, oppo_index, state.oppo_num)

        time.sleep(2)
        state.update_minions()
