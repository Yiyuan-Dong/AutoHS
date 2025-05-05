from config import autohs_config
from constants.state_and_key import *
from controller.base.mouse import MouseController

coors = autohs_config.click_coordinates

class MinionController(MouseController):
    def getMyMinionPosition(self, mine_index, mine_num):
        x = coors[COORDINATE_MID_X] + (mine_index * 2 - mine_num + 1) * coors[COORDINATE_HALF_MINION_GAP_X]
        y = coors[COORDINATE_MY_MINION_Y]
        return [x, y]

    def getEnemyMinionPosition(self, oppo_index, oppo_num):
        x = coors[COORDINATE_MID_X] + (oppo_index * 2 - oppo_num + 1) * coors[COORDINATE_HALF_MINION_GAP_X]
        y = coors[COORDINATE_OPPO_MINION_Y]
        return [x, y]

    def getPosition(self, position_index, mine_num, oppo_num):
        if position_index.is_my_minion():
            return self.getMyMinionPosition(position_index.index, mine_num)
        else:
            return self.getEnemyMinionPosition(position_index.index, oppo_num)

    def chooseMyMinion(self, mine_index, mine_num):
        x = coors[COORDINATE_MID_X] + (mine_index * 2 - mine_num + 1) * coors[COORDINATE_HALF_MINION_GAP_X]
        y = coors[COORDINATE_MY_MINION_Y]
        self.mouseClickPosition([x, y])

    def chooseEnemyMinion(self, oppo_index, oppo_num):
        x = coors[COORDINATE_MID_X] + (oppo_index * 2 - oppo_num + 1) * coors[COORDINATE_HALF_MINION_GAP_X]
        y = coors[COORDINATE_OPPO_MINION_Y]
        self.mouseClickPosition([x, y])

    def chooseMinion(self, position_index, mine_num, oppo_num):
        if position_index.is_my_minion():
            self.chooseMyMinion(position_index.index, mine_num)
        else:
            self.chooseEnemyMinion(position_index.index, oppo_num)