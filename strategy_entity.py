from json_op import *
from abc import abstractmethod
from card.id2card import ID2CARD_DICT
import copy


class StrategyEntity:
    def __init__(self, card_id, zone, zone_pos,
                 current_cost, overload, is_mine):
        self.card_id = card_id
        self.zone = zone
        self.zone_pos = zone_pos
        self.current_cost = current_cost
        self.overload = overload
        self.is_mine = is_mine

    @property
    def name(self):
        return query_json_dict(self.card_id)

    @property
    def heuristic_val(self):
        return 0

    @property
    @abstractmethod
    def cardtype(self):
        pass

    @property
    def is_coin(self):
        return self.name == "幸运币"

    @property
    def detail_card(self):
        if self.is_coin:
            return ID2CARD_DICT["COIN"]
        else:
            return ID2CARD_DICT.get(self.card_id, None)

    # uni_index是对场上可能要被鼠标指到的对象的统一编号.
    # 包括敌我随从和敌我英雄, 具体编号为:
    # 0-6: 我方随从
    # 9: 我方英雄
    # 10-16: 敌方随从
    # 19: 敌方英雄　
    @property
    def uni_index(self):
        return -1


CRITICAL_MINION = {
    "VAN_NEW1_019": 1.5,  # 飞刀杂耍者
    "VAN_EX1_162": 1.5,  # 恐狼前锋
    "VAN_CS2_235": 1.5,  # 北郡牧师
    "VAN_CS2_237": 2,  # 饥饿的秃鹫
    "VAN_EX1_004": 1.5,  # 年轻的女祭司
    "VAN_EX1_095": 1.5,  # 加基森拍卖师
    "VAN_EX1_044": 1.5,  # 任务达人
}


class StrategyMinion(StrategyEntity):
    def __init__(self, card_id, zone, zone_pos,
                 current_cost, overload, is_mine,
                 attack, max_health, damage=0,
                 taunt=0, divine_shield=0, stealth=0,
                 windfury=0, poisonous=0, life_steal=0,
                 spell_power=0, freeze=0, battlecry=0,
                 not_targeted_by_spell=0, not_targeted_by_power=0,
                 charge=0, rush=0,
                 attackable_by_rush=0, frozen=0,
                 dormant=0, untouchable=0, immune=0,
                 cant_attack=0, exhausted=1, num_turns_in_play=1):
        super().__init__(card_id, zone, zone_pos,
                         current_cost, overload, is_mine)
        self.attack = attack
        self.max_health = max_health
        self.damage = damage
        self.taunt = taunt
        self.divine_shield = divine_shield
        self.stealth = stealth
        self.windfury = windfury
        self.poisonous = poisonous
        self.life_steal = life_steal
        self.spell_power = spell_power
        self.freeze = freeze
        self.battlecry = battlecry
        self.not_targeted_by_spell = not_targeted_by_spell
        self.not_targeted_by_power = not_targeted_by_power
        self.charge = charge
        self.rush = rush
        # 当一个随从具有毛刺绿边（就是突袭随从刚出来时的绿边）的时候就会有这个属性
        self.attackable_by_rush = attackable_by_rush
        self.frozen = frozen
        self.dormant = dormant
        # UNTOUCHABLE作用不明, 不过休眠的随从会在休眠时具有UNTOUCHABLE属性
        # self.untouchable = untouchable
        self.immune = immune
        self.cant_attack = cant_attack
        self.num_turns_in_play = num_turns_in_play
        # exhausted == 1: 随从没有绿边, 不能动
        # 普通随从一入场便具有 exhausted == 1,
        # 但是突袭随从和冲锋随从一开始不具有这个标签,
        # 所以还要另作判断(尤其是突袭随从一开始不能打脸)
        self.exhausted = exhausted

        # 对于突袭随从, 第一回合应不能打脸, 而能攻击随从由
        # attackable_by_rush体现
        if self.rush and not self.charge \
                and self.num_turns_in_play < 2:
            self.exhausted = 1

    def __str__(self):
        temp = f"[{self.zone_pos}] {self.name} " \
               f"{self.attack}-{self.health}({self.max_health})"

        if self.can_beat_face:
            temp += " [能打脸]"
        elif self.can_attack_minion:
            temp += " [能打怪]"
        else:
            temp += " [不能动]"

        if self.dormant:
            temp += " 休眠"
        if self.immune:
            temp += " 免疫"
        if self.frozen:
            temp += " 被冻结"
        if self.taunt:
            temp += " 嘲讽"
        if self.divine_shield:
            temp += " 圣盾"
        if self.stealth:
            temp += " 潜行"
        if self.charge:
            temp += " 冲锋"
        if self.rush:
            temp += " 突袭"
        if self.windfury:
            temp += " 风怒"
        if self.poisonous:
            temp += " 剧毒"
        if self.life_steal:
            temp += " 吸血"
        if self.freeze:
            temp += " 冻结敌人"
        if self.not_targeted_by_spell and self.not_targeted_by_power:
            temp += " 魔免"
        if self.spell_power:
            temp += f" 法术伤害+{self.spell_power}"
        if self.cant_attack:
            temp += " 不能攻击"

        temp += f" h_val:{self.heuristic_val}"

        return temp

    @property
    def cardtype(self):
        return CARD_MINION

    @property
    def uni_index(self):
        if self.is_mine:
            return self.zone_pos
        else:
            return self.zone_pos + 10

    @property
    def health(self):
        return self.max_health - self.damage

    @property
    def can_beat_face(self):
        return self.attack > 0 \
               and not self.dormant \
               and not self.frozen \
               and not self.cant_attack \
               and self.exhausted == 0

    @property
    def can_attack_minion(self):
        return self.attack > 0 \
               and not self.dormant \
               and not self.frozen\
               and not self.cant_attack \
               and (self.exhausted == 0
                    or self.attackable_by_rush)

    @property
    def can_be_pointed_by_spell(self):
        return not self.stealth \
               and not self.not_targeted_by_spell \
               and not self.dormant \
               and not self.immune

    @property
    def can_be_pointed_by_hero_power(self):
        return not self.stealth \
               and not self.not_targeted_by_power \
               and not self.dormant \
               and not self.immune

    @property
    def can_be_pointed_by_minion(self):
        return not self.stealth \
               and not self.dormant \
               and not self.immune

    @property
    def can_be_attacked(self):
        return not self.stealth \
               and not self.immune \
               and not self.dormant

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

        if self.zone == "HAND":
            if self.rush or self.attack:
                h_val += self.attack / 4

        h_val *= CRITICAL_MINION.get(self.card_id, 1)

        return h_val

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

    def get_heal(self, heal):
        if heal > self.damage:
            self.damage = 0
        else:
            self.damage -= heal

    def delta_h_after_damage(self, damage):
        temp_minion = copy.copy(self)
        temp_minion.get_damaged(damage)
        return self.heuristic_val - temp_minion.heuristic_val

    def delta_h_after_heal(self, heal):
        temp_minion = copy.copy(self)
        temp_minion.get_heal(heal)
        return temp_minion.heuristic_val - self.heuristic_val


class StrategyWeapon(StrategyEntity):
    def __init__(self, card_id, zone, zone_pos,
                 current_cost, overload, is_mine,
                 attack, durability, damage=0, windfury=0):
        super().__init__(card_id, zone, zone_pos,
                         current_cost, overload, is_mine)
        self.attack = attack
        self.durability = durability
        self.damage = damage
        self.windfury = windfury

    def __str__(self):
        temp = f"{self.name} {self.attack}-{self.health}" \
               f"({self.durability}) h_val:{self.heuristic_val}"
        if self.windfury:
            temp += " 风怒"
        return temp

    @property
    def cardtype(self):
        return CARD_WEAPON

    @property
    def health(self):
        return self.durability - self.damage

    @property
    def heuristic_val(self):
        return self.attack * self.health


class StrategyHero(StrategyEntity):
    def __init__(self, card_id, zone, zone_pos,
                 current_cost, overload, is_mine,
                 max_health, damage=0,
                 stealth=0, immune=0,
                 not_targeted_by_spell=0, not_targeted_by_power=0,
                 armor=0, attack=0, exhausted=1):
        super().__init__(card_id, zone, zone_pos,
                         current_cost, overload, is_mine)
        self.max_health = max_health
        self.damage = damage
        self.stealth = stealth
        self.immune = immune
        self.not_targeted_by_spell = not_targeted_by_spell
        self.not_targeted_by_power = not_targeted_by_power
        self.armor = armor
        self.attack = attack
        self.exhausted = exhausted

    def __str__(self):
        temp = f"{self.name} {self.attack}-{self.health}" \
               f"({self.max_health - self.damage}+{self.armor})"

        if self.can_attack:
            temp += " [能动]"
        else:
            temp += " [不能动]"

        if self.stealth:
            temp += " 潜行"
        if self.immune:
            temp += " 免疫"

        temp += f" h_val:{self.heuristic_val}"
        return temp

    @property
    def cardtype(self):
        return CARD_HERO

    @property
    def uni_index(self):
        if self.is_mine:
            return 10
        else:
            return 20

    @property
    def health(self):
        return self.max_health + self.armor - self.damage

    @property
    def heuristic_val(self):
        if self.health <= 0:
            return -10000
        if self.health <= 5:
            return self.health
        if self.health <= 10:
            return 5 + (self.health - 5) * 0.6
        if self.health <= 20:
            return 8 + (self.health - 10) * 0.4
        else:
            return 12 + (self.health - 20) * 0.3

    @property
    def can_attack(self):
        return self.attack > 0 and not self.exhausted

    @property
    def can_be_pointed_by_spell(self):
        return not self.stealth \
               and not self.not_targeted_by_spell \
               and not self.immune

    @property
    def can_be_pointed_by_hero_power(self):
        return not self.stealth \
               and not self.not_targeted_by_power \
               and not self.immune

    @property
    def can_be_pointed_by_minion(self):
        return not self.stealth \
               and not self.immune

    @property
    def can_be_attacked(self):
        return not self.stealth and not self.immune

    def get_damaged(self, damage):
        if damage <= self.armor:
            self.armor -= damage
        else:
            last_damage = damage - self.armor
            self.armor = 0
            self.damage += last_damage

    def get_heal(self, heal):
        if heal >= self.damage:
            self.damage = 0
        else:
            self.damage -= heal

    def delta_h_after_damage(self, damage):
        temp_hero = copy.copy(self)
        temp_hero.get_damaged(damage)
        return self.heuristic_val - temp_hero.heuristic_val

    def delta_h_after_heal(self, heal):
        temp_hero = copy.copy(self)
        temp_hero.get_heal(heal)
        return temp_hero.heuristic_val - self.heuristic_val


class StrategySpell(StrategyEntity):
    @property
    def cardtype(self):
        return CARD_SPELL


class StrategyHeroPower(StrategyEntity):
    def __init__(self, card_id, zone, zone_pos,
                 current_cost, overload, is_mine,
                 exhausted):
        super().__init__(card_id, zone, zone_pos,
                         current_cost, overload, is_mine)
        self.exhausted = exhausted

    @property
    def cardtype(self):
        return CARD_HERO_POWER

    @property
    def detail_hero_power(self):
        if self.name == "次级治疗术":
            return ID2CARD_DICT["LESSER_HEAL"]
        if self.name == "图腾召唤":
            return ID2CARD_DICT["TOTEMIC_CALL"]
        if self.name == "稳固射击":
            return ID2CARD_DICT["BALLISTA_SHOT"]
        return None
