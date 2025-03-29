from card.basic_card import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from strategy import StrategyState


# 闪电箭
class LightingBolt(SpellPointOppo):
    spell_type = SPELL_POINT_OPPO
    bias = -4

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        spell_power = state.my_total_spell_power
        damage = 3 + spell_power
        best_delta_h = state.oppo_hero.delta_h_after_damage(damage)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            delta_h = oppo_minion.delta_h_after_damage(damage)
            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,


# 呱
class Hex(SpellPointOppo):
    bias = -6
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        best_delta_h = 0
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue

            delta_h = oppo_minion.heuristic_val - 1

            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,


# 闪电风暴
class LightningStorm(SpellNoPoint):
    bias = -10

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
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
    def utilize_delta_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        if state.oppo_minion_num < 4:
            return cls.value, state.my_minion_num
        else:
            h_sum = sum([minion.heuristic_val for minion in state.oppo_minions])
            h_sum /= state.oppo_minion_num
            return cls.value + h_sum * 2,


# 野性狼魂
class FeralSpirit(SpellNoPoint):
    value = 2.4

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
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
    def utilize_delta_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        best_h = 3 + state.oppo_hero.delta_h_after_damage(3)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_minion:
                continue

            delta_h = 3 + oppo_minion.delta_h_after_damage(3)
            if delta_h > best_h:
                best_h = delta_h
                best_oppo_index = oppo_index

        return best_h, state.my_minion_num, best_oppo_index


# 精灵弓箭手
class ElvenArcher(MinionPointOppo):
    @classmethod
    def utilize_delta_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        # 不能让她下去点脸, 除非对面快死了
        best_h = -0.8 + state.oppo_hero.delta_h_after_damage(1)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_minion:
                continue

            delta_h = -0.5 + oppo_minion.delta_h_after_damage(1)
            if delta_h > best_h:
                best_h = delta_h
                best_oppo_index = oppo_index

        return best_h, state.my_minion_num, best_oppo_index


# 大地之环先知
class EarthenRingFarseer(MinionPointMine):
    @classmethod
    def utilize_delta_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        best_h = 0.2 + state.my_hero.delta_h_after_heal(3)
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
    keep_in_hand_bool = True

    @classmethod
    def utilize_delta_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        h_sum = 0
        for oppo_minion in state.oppo_minions:
            h_sum += oppo_minion.delta_h_after_damage(2)
        for my_minion in state.my_minions:
            h_sum -= my_minion.delta_h_after_damage(2)
        h_sum += state.oppo_hero.delta_h_after_damage(2)
        h_sum -= state.my_hero.delta_h_after_damage(2)

        return h_sum,


# 狂奔科多兽
class StampedingKodo(MinionNoPoint):
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        h_sum = 2
        temp_sum = 0
        temp_count = 0

        for oppo_minion in state.oppo_minions:
            if oppo_minion.attack <= 2:
                temp_sum += oppo_minion.heuristic_val
                temp_count += 1
        if temp_count > 0:
            h_sum += temp_sum / temp_count

        return h_sum,


# 血骑士
class BloodKnight(MinionNoPoint):
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        h_sum = 1

        for oppo_minion in state.oppo_minions:
            if oppo_minion.divine_shield:
                h_sum += oppo_minion.attack + 6
        for my_minion in state.my_minions:
            if my_minion.divine_shield:
                h_sum += -my_minion.attack + 6

        return h_sum,


# 末日
class DoomSayer(MinionNoPoint):
    keep_in_hand_bool = True

    @classmethod
    def utilize_delta_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        # 一费别跳末日
        if state.my_total_mana == 1:
            return 0,

        # 二三费压末日就完事了
        if state.my_total_mana <= 3:
            return 1000,

        # 优势不能上末日
        if state.my_heuristic_value >= state.oppo_heuristic_value:
            return 0,

        oppo_attack_sum = 0
        for oppo_minion in state.oppo_minions:
            oppo_attack_sum += oppo_minion.attack

        if oppo_attack_sum >= 7:
            # 当个嘲讽也好
            return 1,
        else:
            return state.oppo_heuristic_value - state.my_heuristic_value,


class StormforgedAxe(WeaponCard):
    keep_in_hand_bool = True
    value = 1.5

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        # 不要已经有刀了再顶刀
        if state.my_weapon is not None:
            return 0,
        if state.my_total_mana == 2:
            for oppo_minion in state.touchable_oppo_minions:
                # 如果能提起刀解了, 那太好了
                if oppo_minion.health <= 2 and \
                        not oppo_minion.divine_shield:
                    return 2000,

        return cls.value,

# 护甲商贩
class ArmorVendor(MinionNoPoint):
    value = 2
    keep_in_hand_bool = True


# 神圣惩击
class HolySmite(SpellPointOppo):
    wait_time = 2
    # 加个bias,一是包含了消耗的水晶的代价，二是包含了消耗了手牌的代价
    bias = -2

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        best_oppo_index = -1
        best_delta_h = 0

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            temp_delta_h = oppo_minion.delta_h_after_damage(3) + cls.bias
            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index


# 倦怠光波
class WaveOfApathy(SpellNoPoint):
    wait_time = 2
    bias = -4

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        tmp = 0

        for minion in state.oppo_minions:
            tmp += minion.attack - 1

        return tmp + cls.bias,


# 噬骨殴斗者
class BonechewerBrawler(MinionNoPoint):
    value = 2
    keep_in_hand_bool = True


# 暗言术灭
class ShadowWordDeath(SpellPointOppo):
    wait_time = 1.5
    bias = -6

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        best_oppo_index = -1
        best_delta_h = 0

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if oppo_minion.attack < 5:
                continue
            if not oppo_minion.can_be_pointed_by_spell:
                continue

            tmp = oppo_minion.heuristic_val + cls.bias
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index


# 神圣化身
class Apotheosis(SpellPointMine):
    bias = -6

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        best_delta_h = 0
        best_mine_index = -1

        for my_index, my_minion in enumerate(state.my_minions):
            if not my_minion.can_be_pointed_by_spell:
                continue

            tmp = cls.bias + 3 + (my_minion.health + 2) / 4 + \
                  (my_minion.attack + 1) / 2
            if my_minion.can_attack_minion:
                tmp += my_minion.attack / 4
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_mine_index = my_index

        return best_delta_h, best_mine_index


# 亡首教徒
class DeathsHeadCultist(MinionNoPoint):
    value = 1
    keep_in_hand_bool = True


# 噬灵疫病
class DevouringPlague(SpellNoPoint):
    wait_time = 4
    bias = -4  # 把吸的血直接算进bias

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        curr_h = state.heuristic_value

        delta_h_sum = 0
        sample_times = 5

        for i in range(sample_times):
            tmp_state = state.copy_new_one()
            for j in range(4):
                tmp_state.random_distribute_damage(1, [i for i in range(tmp_state.oppo_minion_num)], [])

            delta_h_sum += tmp_state.heuristic_value - curr_h

        return delta_h_sum / sample_times + cls.bias,


# 狂傲的兽人
class OverconfidentOrc(MinionNoPoint):
    value = 3
    keep_in_hand_bool = True


# 神圣新星
class HolyNova(SpellNoPoint):
    bias = -8

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        return cls.bias + sum([minion.delta_h_after_damage(2)
                               for minion in state.oppo_minions]),


# 狂乱
class Hysteria(SpellPointOppo):
    wait_time = 5
    bias = -9  # 我觉得狂乱应该要能力挽狂澜
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        best_delta_h = 0
        best_arg = 0
        sample_times = 10

        if state.oppo_minion_num == 0 or state.oppo_minion_num + state.my_minion_num == 1:
            return 0, -1

        for chosen_index, chosen_minion in enumerate(state.oppo_minions):
            if not chosen_minion.can_be_pointed_by_spell:
                continue

            delta_h_count = 0

            for i in range(sample_times):
                tmp_state = state.copy_new_one()
                tmp_chosen_index = chosen_index

                while True:
                    another_index_list = [j for j in range(tmp_state.oppo_minion_num + tmp_state.my_minion_num)]
                    another_index_list.pop(tmp_chosen_index)
                    if len(another_index_list) == 0:
                        break
                    another_index = another_index_list[random.randint(0, len(another_index_list) - 1)]

                    if another_index >= tmp_state.oppo_minion_num:
                        another_minion = tmp_state.my_minions[another_index - tmp_state.oppo_minion_num]
                        if another_minion.get_damaged(chosen_minion.attack):
                            tmp_state.my_minions.pop(another_index - tmp_state.oppo_minion_num)
                    else:
                        another_minion = tmp_state.oppo_minions[another_index]
                        if another_minion.get_damaged(chosen_minion.attack):
                            tmp_state.oppo_minions.pop(another_index)
                            if another_index < tmp_chosen_index:
                                tmp_chosen_index -= 1

                    if chosen_minion.get_damaged(another_minion.attack):
                        tmp_state.oppo_minions.pop(tmp_chosen_index)
                        break


                delta_h_count += tmp_state.heuristic_value - state.heuristic_value

            delta_h_count /= sample_times
            if delta_h_count > best_delta_h:
                best_delta_h = delta_h_count
                best_arg = chosen_index

        return best_delta_h + cls.bias, best_arg


# 暗言术毁
class ShadowWordRuin(SpellNoPoint):
    bias = -8
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        return cls.bias + sum([minion.heuristic_val
                               for minion in state.oppo_minions
                               if minion.attack >= 5]),


# 除奇致胜
class AgainstAllOdds(SpellNoPoint):
    bias = -9
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        return cls.bias + \
               sum([minion.heuristic_val
                    for minion in state.oppo_minions
                    if minion.attack % 2 == 1]) - \
               sum([minion.heuristic_val
                    for minion in state.my_minions
                    if minion.attack % 2 == 1]),


# 锈骑劫匪
class RuststeedRaider(MinionNoPoint):
    value = 3
    keep_in_hand_bool = False
    # TODO: 也许我可以为突袭随从专门写一套价值评判?


# 泰兰佛丁
class TaelanFordring(MinionNoPoint):
    value = 3
    keep_in_hand_bool = False


# 凯恩血蹄
class CairneBloodhoof(MinionNoPoint):
    value = 6
    keep_in_hand_bool = False


# 吃手手鱼
class MutanusTheDevourer(MinionNoPoint):
    value = 5
    keep_in_hand_bool = False


# 灵魂之镜
class SoulMirror(SpellNoPoint):
    wait_time = 5
    bias = -16
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        copy_number = min(7 - state.my_minion_num, state.oppo_minion_num)
        h_sum = 0
        for i in range(copy_number):
            h_sum += state.oppo_minions[i].heuristic_val

        return h_sum + cls.bias,


# 戈霍恩之血
class BloodOfGhuun(MinionNoPoint):
    value = 8
    keep_in_hand_bool = False


# ------ 下面是狂野暗牧的卡牌 ------
# 随从优先级：随船外科医生>宝藏经销商>心灵按摩师>肥婆>暗影投弹手>海盗帕奇斯
# 海盗帕奇斯
class PatchesThePirate(MinionNoPoint):
    value = 1
    keep_in_hand_bool = False


# 虚触侍从
class VoidtouchedAttendant(MinionNoPoint):
    live_value = 2
    value = 3
    keep_in_hand_bool = True


# 宝藏经销商
class TreasureMerchant(MinionNoPoint):
    live_value = 1
    value = 4
    keep_in_hand_bool = True


# 心灵按摩师
class MindrenderIllucia(MinionNoPoint):
    live_value = 1
    value = 3.5
    keep_in_hand_bool = True


# 随船外科医师
class ShipSurgeon(MinionNoPoint):
    live_value = 1
    value = 4.5
    keep_in_hand_bool = True


# 亡者复生
class RaiseDead(SpellNoPoint):
    wait_time = 5
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        if state.my_hero.health <= 3 + state.num_voidtouched_attendant_on_board:  # 用了就死
            return 0,
        elif any(card.card_id == "DED_513" for card in state.my_hand_cards) and state.my_remaining_mana > 3: #有麻风侏儒先战吼点击
            return 0
        elif state.num_minions_in_my_graveyard >= 2:
            return 100,
        else:
            return 0,


# 暗影投弹手
class ShadowBomber(MinionNoPoint):
    value = 1.8
    keep_in_hand_bool = True

    @classmethod
    def utilize_delta_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        # 如果剩余法力 >= 2 且手牌中存在虚触侍从（假设其卡牌ID为 "SW_446"），则降低投弹手的价值，
        # 使得系统优先下虚触侍从
        if state.my_remaining_mana >= 2:
            has_voidtouched = any(
                card.cardtype == CARD_MINION and card.card_id == "SW_446"
                for card in state.my_hand_cards
            )
            if has_voidtouched:
                # 返回一个非常低的价值，确保在决策时不选择投弹手
                return -100, 0

        # 否则，正常计算投弹手的收益
        return state.oppo_hero.delta_h_after_damage(3) + cls.value, 0

# 精神灼烧
# TODO: 理论上可以打死自己的随从实现斩杀...
class MindBlast(SpellPointOppo):
    wait_time = 2
    bias = -1
    keep_in_hand_bool = False   # 大数据显示起手留它正收益，但是很难用好这张牌

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        best_delta_h = -1
        best_oppo_index = -1

        for oppo_minion in state.oppo_minions:
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            # 我发现这个法术打不死随从的时候看着就很蠢
            if oppo_minion.health > 2:
                continue

            temp_delta_h = oppo_minion.delta_h_after_damage(2) + cls.bias
            if not oppo_minion.divine_shield and oppo_minion.health <= 3:
                temp_delta_h += state.oppo_hero.delta_h_after_damage(3)

            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = state.oppo_minions.index(oppo_minion)

        return best_delta_h, best_oppo_index


# 针灸
class Acupuncture(SpellNoPoint):
    wait_time = 2
    bias = -0.5
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        damage = 4 + state.my_total_spell_power + state.num_voidtouched_attendant_on_board
        if state.my_hero.health <= damage:
            return -1,

        damage = 4 + state.my_total_spell_power + state.num_voidtouched_attendant_on_board
        if state.my_hero.health <= damage:
            return -1,

        base_value = state.oppo_hero.delta_h_after_damage(damage) + cls.bias
        # 如果法力充沛，主动降低针灸的收益（或不加 bonus）
        if state.my_remaining_mana >= 2:
            adjustment = -1  # 例如减少1点价值，使其在决策排序中落后于英雄技能
        else:
            adjustment = 0
        bonus = 1 if any(minion.card_id == "SW_446" for minion in state.my_minions) else 0
        return base_value + adjustment+bonus,

        # 我的血不重要
        return state.oppo_hero.delta_h_after_damage(damage) + cls.bias,


# 心灵震爆
class MindShatter(SpellNoPoint):
    wait_time = 2
    bias = -1
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        # 同上，我们使得心灵震爆能够打出combo
        base_value = state.oppo_hero.delta_h_after_damage(5) + cls.bias
        if state.my_remaining_mana >= 2:
            adjustment = -1
        else:
            adjustment = 0
        bonus = 1 if any(minion.card_id == "SW_446" for minion in state.my_minions) else 0
        return base_value + adjustment + bonus,


# 暮光欺诈者
class TwilightDeceptor(MinionNoPoint):
    keep_in_hand_bool = True

    @classmethod
    def utilize_delta_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        hand_card = state.my_hand_cards[hand_card_index]

        if not hand_card.powered_up:
            return 0.1, state.my_minion_num
        else:
            return 4, state.my_minion_num


# 赎罪教堂
# 还没想好怎么写
class ChurchOfAtonement(MinionNoPoint):
    value = -100


# 空降歹徒
class CathedralOfAtonement(MinionNoPoint):
    value = 0.1  # 最好是从手牌里被拉出来
    keep_in_hand_bool = True


# 纸艺天使
class PaperCranes(MinionNoPoint):
    live_value = 3
    value = 4
    keep_in_hand_bool = True


# 暗影主教本尼迪塔斯
class DarkbishopBenedictus(MinionNoPoint):
    # 5费把直伤全用了很可能就赢了，不要下这个
    value = 0.1
    keep_in_hand_bool = False


# 狂暴邪翼蝠
class FrenziedFelwing(MinionNoPoint):
    keep_in_hand_bool = True

    @classmethod
    def utilize_delta_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        hand_card = state.my_hand_cards[hand_card_index]
        if hand_card.current_cost == 0:
            return 50, state.my_minion_num
        elif hand_card.current_cost == 1:
            return 1, state.my_minion_num
        else:
            return 0.1, state.my_minion_num


# 迪菲亚麻风侏儒
class DefiasCleaner(MinionPointOppo):
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state: 'StrategyState', hand_card_index: int):
        this_card = state.my_hand_cards[hand_card_index]

        if not this_card.powered_up:
            return 0.1, state.my_minion_num, -1   # 要是真的没事干，就算不打二也下去当白板打架

        best_delta_h = state.oppo_hero.delta_h_after_damage(2)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_minion:
                continue

            delta_h = oppo_minion.delta_h_after_damage(2)
            if delta_h > best_delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h, state.my_minion_num, best_oppo_index
