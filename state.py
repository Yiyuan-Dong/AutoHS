import copy
import time

import click
import get_screen
import keyboard
import sys


class Minion:
    def __init__(self, attack, health, is_taunt, is_divine_shield):
        self.attack = attack
        self.health = health
        self.is_taunt = is_taunt
        self.has_divine_shield = is_divine_shield

    def __str__(self):
        temp = str(self.attack) + "-" + str(self.health)
        if self.is_taunt:
            temp += " 嘲讽"
        if self.has_divine_shield:
            temp += " 圣盾"
        return temp


class State:
    def __init__(self):
        self.oppo_num = 0
        self.mine_num = 0
        self.available = []
        self.oppos = []
        self.mines = []

        self.update_minions()

        self.card_num = get_screen.count_my_cards()
        self.cards = get_screen.identify_cards(self.card_num)

    def update_minions(self):
        img = get_screen.catch_screen()
        self.oppo_num, self.mine_num = get_screen.count_minions(img)
        oppo_ah, mine_ah = get_screen.get_attack_health(img, self.oppo_num, self.mine_num)
        oppo_t, mine_t = get_screen.test_taunt(img, self.oppo_num, self.mine_num)
        oppo_ds, mine_ds = get_screen.test_divine_shield()
        self.available = get_screen.test_available(img, self.mine_num)

        self.oppos = []
        for i in range(self.oppo_num):
            self.oppos.append(
                Minion(
                    oppo_ah[i][0],
                    oppo_ah[i][1],
                    oppo_t[i],
                    oppo_ds[i]
                )
            )

        self.mines = []
        for i in range(self.mine_num):
            self.mines.append(
                Minion(
                    mine_ah[i][0],
                    mine_ah[i][1],
                    mine_t[i],
                    mine_ds[i]
                )
            )

    def print_out(self):
        print(f"我有{self.card_num}张手牌,它们分别是")
        print("  " + ", ".join(self.cards))
        print(f"对手有{self.oppo_num}个随从")
        for minion in self.oppos:
            print("  " + str(minion))
        print(f"我有{self.mine_num}个随从")
        for i in range(len(self.mines)):
            minion = self.mines[i]
            print("  " + str(minion), end=" ")
            if self.available[i] == 2:
                print("能打脸")
            elif self.available[i] == 1:
                print("是突袭")
            else:
                print("不能动")

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

                if my_minion.has_divine_shield:
                    tmp_delta_h_val -= my_minion.attack
                else:
                    if my_minion.health <= oppo_minion.attack:
                        tmp_delta_h_val -= my_minion.attack + my_minion.health
                    else:
                        tmp_delta_h_val -= oppo_minion.attack

                if oppo_minion.has_divine_shield:
                    tmp_delta_h_val += oppo_minion.attack
                else:
                    if oppo_minion.health <= my_minion.attack:
                        tmp_delta_h_val += oppo_minion.attack + oppo_minion.health
                    else:
                        tmp_delta_h_val += my_minion.attack

                # 想给过墙行为加一点补正
                if oppo_minion.is_taunt:
                    tmp_delta_h_val += min(oppo_minion.health, my_minion.attack) * 0.5

                if tmp_delta_h_val > max_delta_h_val:
                    max_delta_h_val = tmp_delta_h_val
                    max_my_index = my_index
                    max_oppo_index = oppo_index

            # 如果没有墙,自己又能打脸,应该试一试
            if not has_taunt:
                if self.available[my_index] == 2 and \
                        my_minion.attack * 0.75 > max_delta_h_val:
                    # *0.75 因为场面更重要
                    max_delta_h_val = my_minion.attack * 0.75
                    max_my_index = my_index
                    max_oppo_index = -1

        return max_my_index, max_oppo_index


if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+q", sys.exit)

    state = State()
    while True:
        state.print_out()
        print(state.mine_heuristic_value, state.oppo_heuristic_value, state.heuristic_value)
        mine_index, oppo_index = state.get_best_action()
        print(mine_index, oppo_index)

        time.sleep(2)

        if mine_index == -1:
            break
        if oppo_index == -1:
            click.minion_beat_hero(mine_index, state.mine_num)
        else:
            click.minion_beat_minion(mine_index, state.mine_num, oppo_index, state.oppo_num)

        time.sleep(2)
        state.update_minions()
