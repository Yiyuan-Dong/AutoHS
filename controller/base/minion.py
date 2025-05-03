from config import coors
from constants.state_and_key import *
from controller.base.mouse import MouseController


class MinionController(MouseController):
    def getMyMinionPosition(self, mine_index, mine_num):
        x = coors[COORDINATE_MID_X] + (mine_index * 2 - mine_num + 1) * coors[COORDINATE_HALF_MINION_GAP_X]
        y = coors[COORDINATE_MY_MINION_Y]
        return [x, y]

    def getEnemyMinionPosition(self, oppo_index, oppo_num):
        x = coors[COORDINATE_MID_X] + (oppo_index * 2 - oppo_num + 1) * coors[COORDINATE_HALF_MINION_GAP_X]
        y = coors[COORDINATE_OPPO_MINION_Y]
        return [x, y]

    def chooseMyMinion(self, mine_index, mine_num):
        x = coors[COORDINATE_MID_X] + (mine_index * 2 - mine_num + 1) * coors[COORDINATE_HALF_MINION_GAP_X]
        y = coors[COORDINATE_MY_MINION_Y]
        self.mouseClickPosition([x, y])

    def chooseEnemyMinion(self, oppo_index, oppo_num):
        x = coors[COORDINATE_MID_X] + (oppo_index * 2 - oppo_num + 1) * coors[COORDINATE_HALF_MINION_GAP_X]
        y = coors[COORDINATE_OPPO_MINION_Y]
        self.mouseClickPosition([x, y])

    def useMinionSkill(self, mine_index, mine_number, oppo_index, oppo_num):
        my_minion_pos = self.getMyMinionPosition(mine_index, mine_number)
        self.mouseClickPosition(my_minion_pos)
        # 选择
        self.chooseCard()
        # TODO 如果有指定目标
        target_pos = []
        self.mouseClickPosition(target_pos)