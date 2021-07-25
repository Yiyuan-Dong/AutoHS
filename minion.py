import copy


class Minion:
    def __init__(self, attack, health, taunt=0,
                 divine_shield=0, stealth=0, poisonous=0,
                 spellpower=0, charge=0, exhausted=0):
        self.attack = attack
        self.health = health
        self.taunt = taunt
        self.divine_shield = divine_shield
        self.stealth = stealth
        self.poisonous = poisonous
        self.charge = charge
        self.spellpower = spellpower
        self.exhausted = exhausted

    def __str__(self):
        temp = str(self.attack) + "-" + str(self.health)
        if self.exhausted:
            temp += " [不能动]"
        else:
            temp += " [能动]"

        if self.taunt:
            temp += " 嘲讽"
        if self.divine_shield:
            temp += " 圣盾"
        if self.stealth:
            temp += " 潜行"
        if self.charge:
            temp += " 冲锋"
        if self.poisonous:
            temp += " 剧毒"
        if self.spellpower:
            temp += f" 法术伤害+{self.spellpower}"
        return temp

    def get_damaged(self, damage):
        if damage <= 0:
            return False
        if self.divine_shield:
            self.divine_shield = False
        else:
            self.health -= damage
            if self.health <= 0:
                return True
        return False

    # 简单介绍一下卡费理论
    # 一点法力水晶 = 抽0.5张卡 = 造成1点伤害
    # = 2点攻击力 = 2点生命值 = 回复2点血
    # 一张卡自带一点水晶
    # 可以类比一下月火术, 奥术射击, 小精灵, 战斗法师等卡
    @property
    def heuristic_val(self):
        if self.health <= 0:
            return 0

        h_val = self.attack + self.health
        if self.divine_shield:
            h_val += self.attack
        if self.stealth:
            h_val += self.attack / 2
        if self.taunt:
            h_val += self.health / 2
        if self.poisonous:
            h_val += self.health
        h_val += self.poisonous

        return h_val

    def delta_h_after_damage(self, damage):
        # if damage == 0:
        #     return 0
        # if self.divine_shield:
        #     return self.attack
        # else:
        #     if damage >= self.health:
        #         return self.heuristic_val
        #     else:
        #         delta_h = damage
        #         if self.taunt:
        #             delta_h += damage / 2
        #         if self.poisonous:
        #             delta_h += damage
        #     return delta_h

        temp_minion = copy.copy(self)
        temp_minion.get_damaged(damage)
        return self.heuristic_val - temp_minion.heuristic_val
