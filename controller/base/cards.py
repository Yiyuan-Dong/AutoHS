# -*- coding: UTF-8 -*-

"""
__Author__ = "MakiNaruto"
__Mail__: "become006@gmail.com"
__Version__ = "1.0.1"
__Created__ = "2025/04/26"
__Description__ = ""
"""

from constants.state_and_key import *
from controller.base.mouse import MouseController
from config import coors


class CardsController(MouseController):
    def chooseHandCard(self, card_index, card_num, click=True):
        """ 选择手牌 """
        hand_card_x = coors[COORDINATE_MY_HAND_X]

        # TODO: 其实最多可以有12张手牌
        assert 0 <= card_index < card_num <= 10
        # 选中手牌的坐标
        x = hand_card_x[card_num][card_index]
        y = coors[COORDINATE_MY_HAND_Y]
        if click:
            self.mouseClickPosition([x, y])
        else:
            self.mouseMoveToPosition([x, y])

    def useHandCard(self, card_index, card_num, place_position=None):
        """ 通用出牌, 不需考虑额外的战吼, 抉择等额外操作 """
        self.chooseHandCard(card_index, card_num, click=False)
        if place_position:
            self.mouseDragToPosition(place_position)
        else:
            self.mouseDragToPosition([coors[COORDINATE_MID_X], coors[COORDINATE_NO_OP_Y]])

    def replaceStartingCard(self, card_index, hand_card_num):
        start_card_x = coors[COORDINATE_START_CARD_X]

        self.mouseClickPosition([start_card_x[hand_card_num][card_index], coors[COORDINATE_START_CARD_Y]])

    def chooseScreenCard(self, card_index, hand_card_num):
        # TODO
        # 抉择, 泰坦
        self.mouseClickPosition([coors[COORDINATE_START_CARD_X], coors[COORDINATE_START_CARD_Y]])

    def useBattlecryCard(self, card_index, card_num, gap_index, minion_num, choose_card_indx=None, target_pos=None):
        """ 使用具有战吼的卡片, 若需要选择目标, 则传入目标坐标参 """
        self.putMinionOnBattleGround(card_index, card_num, gap_index, minion_num)
        if choose_card_indx:
            self.chooseScreenCard(card_index, card_num)
            # TODO
            # 某些条件下添加点击的target_pos
        if target_pos:
            self.mouseClickPosition(target_pos)

    def putMinionOnBattleGround(self, card_index, card_num, gap_index, minion_num):
        x = coors[COORDINATE_MID_X] + (2 * gap_index - minion_num) * coors[COORDINATE_HALF_MINION_GAP_X]
        y = coors[COORDINATE_MY_MINION_Y]
        self.useHandCard(card_index, card_num, [x, y])