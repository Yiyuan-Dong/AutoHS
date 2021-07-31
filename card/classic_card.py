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
    bias = - 10

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
    value = 1

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        if state.my_minion_num >= 7:
            return 0, -1
        elif state.oppo_minion_num < 4:
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
    value = 4


# 奥妮克希亚
class Onyxia(MinionNoPoint):
    value = 10


# 火元素
class FireElemental(MinionPointOppo):
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        if state.my_minion_num >= 7:
            return -1, 0
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
