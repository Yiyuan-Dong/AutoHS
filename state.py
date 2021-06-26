import copy

import get_screen


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
        img = get_screen.catch_screen()
        self.oppo_num, self.mine_num = get_screen.count_minions(img)
        oppo_ah, mine_ah = get_screen.get_attack_health(img, self.oppo_num, self.mine_num)
        oppo_t, mine_t = get_screen.test_taunt(img, self.oppo_num, self.mine_num)
        oppo_ds, mine_ds = get_screen.test_divine_shield()

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

        self.card_num = get_screen.count_my_cards()
        self.cards = get_screen.identify_cards(self.card_num)

    def print_out(self):
        print(f"我有{self.card_num}张手牌,它们分别是")
        print("  " + ", ".join(self.cards))
        print(f"对手有{self.oppo_num}个随从")
        for minion in self.oppos:
            print("  " + str(minion))
        print(f"我有{self.mine_num}个随从")
        for minion in self.mines:
            print("  " + str(minion))

    # 用卡费体系来算启发值
    @property
    def oppo_heuristic_value(self):
        h_val = 0
        for minion in self.oppos:
            h_val += minion.attack + minion.health
            if minion.has_divine_shield:
                h_val += minion.health
        return h_val / 2

    @property
    def mine_heuristic_value(self):
        h_val = 0
        for minion in self.mines:
            h_val += minion.attack + minion.health
            if minion.has_divine_shield:
                h_val += minion.health
        return h_val / 2

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




if __name__ == "__main__":
    state = State()
    print(state.heuristic_value)
