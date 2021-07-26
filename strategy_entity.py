from print_info import *
import copy


class Minion:
    def __init__(self, attack, max_health, damage=0, taunt=0,
                 divine_shield=0, stealth=0, poisonous=0, life_steal=0,
                 spell_power=0, charge=0, exhausted=1, name=""):
        self.attack = attack
        self.max_health = max_health
        self.damage = damage
        self.taunt = taunt
        self.divine_shield = divine_shield
        self.stealth = stealth
        self.poisonous = poisonous
        self.life_steal = life_steal
        self.spell_power = spell_power
        self.charge = charge
        self.exhausted = exhausted
        self.name = name

    @property
    def health(self):
        return self.max_health - self.damage

    def __str__(self):
        temp = f"{self.name} {self.attack}-{self.health}({self.max_health})"
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
        if self.life_steal:
            temp += " 吸血"
        if self.spell_power:
            temp += f" 法术伤害+{self.spell_power}"

        temp += f" h_val:{self.heuristic_val}"

        return temp

    def get_damaged(self, damage):
        if damage <= 0:
            return False
        if self.divine_shield:
            self.divine_shield = False
        else:
            self.damage += damage
            if self.health <= 0:
                return True
        return False

    def get_restore(self, restore):
        if restore > self.damage:
            self.damage = 0
        else:
            self.damage -= restore

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
            if self.divine_shield:
                h_val += 3
        if self.life_steal:
            h_val += self.attack / 2 + self.health / 2
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


class Weapon:
    def __init__(self, attack, durability, damage=0, name=""):
        self.attack = attack
        self.durability = durability
        self.damage = damage
        self.name = name

    def __str__(self):
        return f"{self.name} {self.attack}-{self.health}({self.durability}) h_val:{self.heuristic_val}"

    @property
    def health(self):
        return self.durability - self.damage

    @property
    def heuristic_val(self):
        return self.attack * self.health


class Hero:
    def __init__(self, max_health, damage=0, attack=0, exhausted=1, name=""):
        self.max_health = max_health
        self.damage = damage
        self.attack = attack
        self.exhausted = exhausted
        self.name = name

    def __str__(self):
        res = f"{self.name} {self.attack}-{self.health}({self.max_health})"
        if self.exhausted == 1:
            res += " [不能动]"
        else:
            res += " [能动]"
        res += f" h_val:{self.heuristic_val}"
        return res

    @property
    def health(self):
        return self.max_health - self.damage

    @property
    def heuristic_val(self):
        if self.health <= 0:
            return -10000
        if self.health <= 10:
            return self.health * 0.6
        if self.health <= 20:
            return 6 + (self.health - 10) * 0.4
        else:
            return 10 + (self.health - 20) * 0.3


class HandCard:
    pass
