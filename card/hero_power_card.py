import click
from card.basic_card import *


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
        click.use_skill_no_point()
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
        click.use_skill_point_mine(args[0], state.my_minion_num)
        time.sleep(1)

class BallistaShot(HeroPowerCard):
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return 1,-1

    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        click.use_skill_no_point()
        time.sleep(1)

class MindSpike(HeroPowerCard):
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        if state.my_hero_power.exhausted:
            return 0,

        # 如果手牌中有纸艺天使，则直接返回0
        if any(card.card_id == "TOY_381" for card in state.my_hand_cards):
            return 0,
            
        best_index = -1
        best_delta_h = state.oppo_hero.delta_h_after_damage(2)

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_minion:
                continue

            delta_h = oppo_minion.delta_h_after_damage(2)
            if delta_h > best_delta_h:
                best_delta_h = delta_h
                best_index = oppo_index

        # 二费打二不赚
        if state.my_hero_power.current_cost >= 2:
            best_delta_h /= state.my_hero_power.current_cost

        # 统计手牌中可用的随从数量
        available_minion_count = sum(
            1 for card in state.my_hand_cards
            if card.cardtype == CARD_MINION and card.current_cost <= state.my_remaining_mana and card.card_id != "YOD_032"
        )

        # 如果剩余法力 >= 2 且手牌中没有可用随从，则增加 bonus
        if state.my_remaining_mana >= 2 and available_minion_count == 0:
            bonus = 5  # 此数值可根据实际调优需要修改
        else:
            bonus = 0

        # 如果敌方英雄的生命值低于15，则增加 bonus，默认敌方英雄
        if state.oppo_hero.health < 15:
            bonus = 5  # 此数值可根据实际调优需要修改
            return best_delta_h + bonus, -1


        return best_delta_h, best_index

    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        click.use_skill_point_oppo(args[0], state.oppo_minion_num)
        time.sleep(1)
