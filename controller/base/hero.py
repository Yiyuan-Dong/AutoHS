from config import coors
from constants.state_and_key import *
from controller.base.mouse import MouseController


class HeroController(MouseController):
    def getMyHeroSkillPosition(self):
        return [coors[COORDINATE_SKILL_X], coors[COORDINATE_SKILL_Y]]

    def getMyHeroPosition(self):
        return [coors[COORDINATE_MID_X], coors[COORDINATE_MY_HERO_Y]]

    def getEnemyHeroPosition(self):
        return [coors[COORDINATE_MID_X], coors[COORDINATE_OPPO_HERO_Y]]

    def useSkill(self):
        skill_pos = self.getMyHeroSkillPosition()
        self.mouseClickPosition(skill_pos)

    def chooseMyHero(self):
        my_hero_pos = self.getMyHeroPosition()
        self.mouseClickPosition(my_hero_pos)

    def chooseEnemyHero(self):
        enemy_hero_pos = self.getEnemyHeroPosition()
        self.mouseClickPosition(enemy_hero_pos)

    def myHeroAttackEnemyHero(self):
        self.chooseMyHero()
        self.chooseEnemyHero()