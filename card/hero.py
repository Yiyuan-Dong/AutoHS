from card.basic import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from strategy.strategy import StrategyState


class TotemicCall(HeroPowerCard):
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        if not state.my_hero_power.exhausted \
                and state.my_minion_num < 7:
            return 0.1,
        else:
            return 0,

    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        controller.hero.useSkill()
        # click.use_skill_no_point()
        time.sleep(1)


class LesserHeal(HeroPowerCard):
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        if state.my_hero_power.exhausted:
            return 0,
        best_index = -1
        best_delta_h = state.my_hero.delta_h_after_heal(2)

        for my_index, my_minion in enumerate(state.my_minions):
            delta_h = my_minion.delta_h_after_heal(2)
            if delta_h > best_delta_h:
                best_delta_h = delta_h
                best_index = my_index

        return best_delta_h, best_index

    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        controller.attack.useSkillToTarget(args[0], state.my_minion_num, SkillType.POINT_TO_NONE)
        time.sleep(1)


class BallistaShot(HeroPowerCard):
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return 1,-1

    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        controller.hero.useSkill()
        # click.use_skill_no_point()
        time.sleep(1)


class MindSpike(HeroPowerCard):
    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index):
        if state.my_hero_power.exhausted:
            return 0,

        # 如果手牌中有纸艺天使，则直接返回0
        if state.if_card_in_hand("TOY_381"):
            return 0,

        best_index = -1
        best_delta_h = state.oppo_hero.delta_h_after_damage(2 + state.num_voidtouched_attendant_on_board)

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_hero_power:
                continue

            delta_h = oppo_minion.delta_h_after_damage(2)
            if delta_h > best_delta_h:
                best_delta_h = delta_h
                best_index = oppo_index

        # 二费打二不赚
        if state.my_hero_power.current_cost >= 2:
            best_delta_h /= state.my_hero_power.current_cost

        return best_delta_h, best_index

    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        controller.attack.useSkillToTarget(args[0], state.oppo_minion_num, SkillType.POINT_TO_OPPONENT)
        time.sleep(1)
