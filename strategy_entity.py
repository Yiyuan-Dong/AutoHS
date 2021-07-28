from print_info import *
import copy


class Minion:
    def __init__(self, attack, max_health, damage=0, taunt=0, divine_shield=0,
                 stealth=0, poisonous=0, life_steal=0, spell_power=0, freeze=0,
                 not_targeted_by_spell=0, not_targeted_by_power=0, charge=0, rush=0,
                 attackable_by_rush=0, frozen=0, exhausted=1, zone_pos=0, name=""):
        self.attack = attack
        self.max_health = max_health
        self.damage = damage
        self.taunt = taunt
        self.divine_shield = divine_shield
        self.stealth = stealth
        self.poisonous = poisonous
        self.life_steal = life_steal
        self.spell_power = spell_power
        self.freeze = freeze
        self.not_targeted_by_spell = not_targeted_by_spell
        self.not_targeted_by_power = not_targeted_by_power
        self.charge = charge
        self.rush = rush
        self.attackable_by_rush = attackable_by_rush
        self.frozen = frozen
        self.exhausted = exhausted
        self.zone_pos = zone_pos
        self.name = name

    @property
    def health(self):
        return self.max_health - self.damage

    @property
    def can_beat_face(self):
        return self.exhausted == 0 and not self.frozen

    @property
    def can_attack_minion(self):
        return not self.frozen and \
               self.exhausted == 0 or self.attackable_by_rush

    def __str__(self):
        temp = f"[{self.zone_pos - 1}]{self.name} " \
               f"{self.attack}-{self.health}({self.max_health})"

        if self.can_beat_face:
            temp += " [能打脸]"
        elif self.can_attack_minion:
            temp += " [能打怪]"
        else:
            temp += " [不能动]"

        if self.frozen:
            temp += " 被冻结"
        if self.taunt:
            temp += " 嘲讽"
        if self.divine_shield:
            temp += " 圣盾"
        if self.stealth:
            temp += " 潜行"
        # if self.charge:
        #     temp += " 冲锋"
        # if self.rush:
        #     temp += " 突袭"
        if self.poisonous:
            temp += " 剧毒"
        if self.life_steal:
            temp += " 吸血"
        if self.freeze:
            temp += "冻结敌人"
        if self.not_targeted_by_spell and self.not_targeted_by_power:
            temp += " 魔免"
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
        if self.taunt:  # 嘲讽不值钱
            h_val += self.health / 4
        if self.poisonous:
            h_val += self.health
            if self.divine_shield:
                h_val += 3
        if self.life_steal:
            h_val += self.attack / 2 + self.health / 4
        h_val += self.poisonous

        return h_val

    def delta_h_after_damage(self, damage):
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
        return f"{self.name} {self.attack}-{self.health}" \
               f"({self.durability}) h_val:{self.heuristic_val}"

    @property
    def health(self):
        return self.durability - self.damage

    @property
    def heuristic_val(self):
        return self.attack * self.health


class Hero:
    def __init__(self, max_health, damage=0, armor=0,
                 attack=0, exhausted=1, name=""):
        self.max_health = max_health
        self.damage = damage
        self.armor = armor
        self.attack = attack
        self.exhausted = exhausted
        self.name = name

    def __str__(self):
        res = f"{self.name} {self.attack}-{self.health}" \
              f"({self.max_health - self.damage}+{self.armor})"
        if self.exhausted == 1:
            res += " [不能动]"
        else:
            res += " [能动]"
        res += f" h_val:{self.heuristic_val}"
        return res

    @property
    def health(self):
        return self.max_health + self.armor - self.damage

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

    def get_damaged(self, damage):
        if damage <= self.armor:
            self.armor -= damage
        else:
            last_damage = damage - self.armor
            self.armor = 0
            self.damage += last_damage

    def delta_h_after_damage(self, damage):
        temp_hero = copy.copy(self)
        temp_hero.get_damaged(damage)
        return self.heuristic_val - temp_hero.heuristic_val


class HandCard:
    def __init__(self, card_type, cost, zone_pos, name):
        self.card_type = card_type
        self.cost = cost
        self.name = name
        self.zone_pos = zone_pos

    def __str__(self):
        return f"[{self.zone_pos - 1}]{self.name} " \
               f"cost:{self.cost} type:{self.card_type}"
