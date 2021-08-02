from card.basic_card import *


# 闪电箭
class LightingBolt(SpellPointOppo):
    spell_type = SPELL_POINT_OPPO
    bias = -4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        spell_power = state.my_total_spell_power
        damage = 3 + spell_power
        best_delta_h = state.oppo_hero.delta_h_after_damage(damage)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_point_by_spell:
                continue
            delta_h = oppo_minion.delta_h_after_damage(damage)
            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,


# 呱
class Hex(SpellPointOppo):
    bias = -8
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_point_by_spell:
                continue

            delta_h = oppo_minion.heuristic_val - 1

            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,


# 闪电风暴
class LightningStorm(SpellNoPoint):
    bias = -8

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        h_sum = 0
        spell_power = state.my_total_spell_power

        for oppo_minion in state.oppo_minions:
            h_sum += (oppo_minion.delta_h_after_damage(2 + spell_power) +
                      oppo_minion.delta_h_after_damage(3 + spell_power)) / 2

        return h_sum + cls.bias,


# TC130
class MindControlTech(MinionNoPoint):
    value = 0.2
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        if state.oppo_minion_num < 4:
            return cls.value, state.my_minion_num
        else:
            h_sum = sum([minion.heuristic_val for minion in state.oppo_minions])
            h_sum /= state.oppo_minion_num
            return cls.value + h_sum * 2, state.my_minion_num


# 　野性狼魂
class FeralSpirit(SpellNoPoint):
    value = 2.4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        if state.my_minion_num >= 7:
            return -1, 0
        else:
            return cls.value, 0


# 碧蓝幼龙
class AzureDrake(MinionNoPoint):
    value = 3.5
    keep_in_hand_bool = False


# 奥妮克希亚
class Onyxia(MinionNoPoint):
    value = 10
    keep_in_hand_bool = False


# 火元素
class FireElemental(MinionPointOppo):
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        best_h = 3 + state.oppo_hero.delta_h_after_damage(3)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_point_by_minion:
                continue

            delta_h = 3 + oppo_minion.delta_h_after_damage(3)
            if delta_h > best_h:
                best_h = delta_h
                best_oppo_index = oppo_index

        return best_h, state.my_minion_num, best_oppo_index


# 精灵弓箭手
class ElvenArcher(MinionPointOppo):
    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        # 不能让她下去点脸, 除非对面快死了
        best_h = -0.8 + state.oppo_hero.delta_h_after_damage(1)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_point_by_minion:
                continue

            delta_h = -0.5 + oppo_minion.delta_h_after_damage(1)
            if delta_h > best_h:
                best_h = delta_h
                best_oppo_index = oppo_index

        return best_h, state.my_minion_num, best_oppo_index


# 大地之环先知
class EarthenRingFarseer(MinionPointMine):
    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        best_h = 0.1 + state.my_hero.delta_h_after_heal(3)
        if state.my_hero.health <= 5:
            best_h += 4
        best_my_index = -1

        for my_index, my_minion in enumerate(state.my_minions):
            delta_h = -0.5 + my_minion.delta_h_after_heal(3)
            if delta_h > best_h:
                best_h = delta_h
                best_my_index = my_index

        return best_h, state.my_minion_num, best_my_index


# 憎恶
class Abomination(MinionNoPoint):
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        h_sum = 0
        for oppo_minion in state.oppo_minions:
            h_sum += oppo_minion.delta_h_after_damage(2)
        for my_minion in state.my_minions:
            h_sum -= my_minion.delta_h_after_damage(2)
        h_sum += state.oppo_hero.delta_h_after_damage(2)
        h_sum -= state.my_hero.delta_h_after_damage(2)

        return h_sum, state.my_minion_num
