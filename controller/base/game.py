# -*- coding: UTF-8 -*-

"""
__Author__ = "MakiNaruto"
__Mail__: "become006@gmail.com"
__Version__ = "1.0.1"
__Created__ = "2024/10/11"
__Description__ = ""
"""
import sys
import time
import random
from config import autohs_config, logger
from constants.state_and_key import *
from controller.base.mouse import MouseController
from utils.window_utils import get_HS_hwnd, get_battlenet_hwnd, get_window_pos, move_window_foreground, test_hs_available

coors = autohs_config.click_coordinates

class GameController(MouseController):
    def setting(self):
        self.mouseClickPosition([coors[COORDINATE_SETTING_X], coors[COORDINATE_SETTING_Y]])

    def surrender(self):
        self.mouseClickPosition([coors[COORDINATE_GIVE_UP_X], coors[COORDINATE_GIVE_UP_Y]])

    def matchOpponent(self):
        self.mouseClickPosition([coors[COORDINATE_MATCH_OPPONENT_X], coors[COORDINATE_MATCH_OPPONENT_Y]])

    def enterBattleMode(self):
        self.mouseClickPosition([coors[COORDINATE_MID_X], coors[COORDINATE_ENTER_BATTLE_Y]])

    def commitChooseCard(self):
        self.mouseClickPosition([coors[COORDINATE_MID_X], coors[COORDINATE_COMMIT_CHOOSE_START_CARD_Y]])

    def endTurn(self):
        self.mouseClickPosition([coors[COORDINATE_END_TURN_X], coors[COORDINATE_END_TURN_Y]])

    def useEmoj(self, target=None):
        emoj_list = coors[COORDINATE_EMOJ_LIST]
        self.mouseRightClickPosition([coors[COORDINATE_MID_X], coors[COORDINATE_MY_HERO_Y]])
        if target is None:
            x, y = emoj_list[random.randint(1, 4)]
        else:
            x, y = emoj_list[target]
        self.mouseClickPosition([x, y])

    def giveUpRoutine(self):
        self.useEmoj(1)
        self.setting()
        time.sleep(0.5)
        self.surrender()
        time.sleep(3)

    def cancelClick(self):
        self.mouseClickPosition([coors[COORDINATE_CANCEL_X], coors[COORDINATE_CANCEL_Y]])

    def chooseCardConfirm(self):
        choose_position = ''
        self.mouseClickPosition(choose_position)

    def commitErrorReport(self):
        # 一些奇怪的错误提示
        self.mouseClickPosition([coors[COORDINATE_ERROR_REPORT_X], coors[COORDINATE_ERROR_REPORT_Y]])
        # 如果已断线, 点这里时取消
        self.mouseClickPosition([coors[COORDINATE_DISCONNECTED_X], coors[COORDINATE_DISCONNECTED_Y]])

    def enterHS(self):
        if test_hs_available():
            move_window_foreground(get_HS_hwnd(), "炉石传说")
            return

        battlenet_hwnd = get_battlenet_hwnd()

        if battlenet_hwnd == 0:
            logger.error("未找到应用战网")
            sys.exit()

        move_window_foreground(battlenet_hwnd, "战网")

        left, top, right, bottom = get_window_pos(battlenet_hwnd)
        self.mouseClickPosition([left + 180, bottom - 110])

    def clickMiddle(self):
        self.mouseClickPosition([coors[COORDINATE_MID_X], coors[COORDINATE_NO_OP_Y]])

    def clickMainMenuMiddle(self):
        self.mouseClickPosition([coors[COORDINATE_MID_X], coors[COORDINATE_MAIN_MENU_NO_OP_Y]])