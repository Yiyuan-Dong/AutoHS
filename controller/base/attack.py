from controller.base.game import GameController
from controller.base.cards import CardsController
from controller.base.hero import HeroController
from controller.base.minion import MinionController
from constants.state_and_key import SkillType


class AttackController(CardsController, HeroController, MinionController, GameController):
    def minionAttackEnemyMinion(self, mine_index, mine_number, oppo_index, oppo_num):
        my_minion_pos = self.getMyMinionPosition(mine_index, mine_number)
        enemy_minion_pos = self.getEnemyMinionPosition(oppo_index, oppo_num)
        self.positionClickPosition(my_minion_pos, enemy_minion_pos)

    def minionAttackEnemyHero(self, mine_index, mine_number):
        my_minion_pos = self.getMyMinionPosition(mine_index, mine_number)
        enemy_hero_pos = self.getEnemyHeroPosition()
        self.positionClickPosition(my_minion_pos, enemy_hero_pos)

    def useSkillToTarget(self, index, num, skill_type : SkillType):
        self.useSkill()
        if skill_type == SkillType.POINT_TO_NONE:
            if index < 0:
                self.chooseMyHero()
            else:
                self.chooseMyMinion(index, num)
            self.cancelClick()

        elif skill_type in SkillType.POINT_TO_OPPONENT:
            if index < 0:
                self.chooseEnemyHero()
            else:
                self.chooseEnemyMinion(index, num)
            self.cancelClick()

    def myHeroAttackEnemyMinion(self, oppo_index, oppo_num):
        self.chooseMyHero()
        self.chooseEnemyMinion(oppo_index, oppo_num)