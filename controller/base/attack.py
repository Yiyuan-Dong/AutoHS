

from controller.base.game import GameController
from controller.base.cards import CardsController
from controller.base.hero import HeroController
from controller.base.minion import MinionController


class AttackController(CardsController, HeroController, MinionController, GameController):
    def minionAttackEnemyMinion(self, mine_index, mine_number, oppo_index, oppo_num):
        my_minion_pos = self.getMyMinionPosition(mine_index, mine_number)
        enemy_minion_pos = self.getEnemyMinionPosition(oppo_index, oppo_num)
        self.positionClickPosition(my_minion_pos, enemy_minion_pos)
    
    def minionAttackEnemyHero(self, mine_index, mine_number):
        my_minion_pos = self.getMyMinionPosition(mine_index, mine_number)
        enemy_hero_pos = self.getEnemyHeroPosition()
        self.positionClickPosition(my_minion_pos, enemy_hero_pos)

    def magicCardAttackEnemy(self, hand_card_index, enemy_pos, target='minion'):
        if target == 'hero':
            enemy_pos = self.getEnemyHeroPosition()

        self.useMagicCard(hand_card_index, enemy_pos)

    def useSkillToTarget(self, index, num, skill_type='次级治疗术'):
        self.useSkill()
        if skill_type in ['治疗术']:
            if index < 0:
                self.chooseMyHero()
            else:
                self.chooseMyMinion(index, num)

        elif skill_type in ['火焰冲击', '次级治疗术']:
            if index < 0:
                self.chooseEnemyHero()
            else:
                self.chooseEnemyMinion(index, num)

            self.cancelClick()

        # TODO
        # elif skill_type in ['恶魔之爪', '变形', '匕首精通']:
        #     self.myHeroAttackEnemyHero()
        # else:
        #     ...

    def myHeroAttackEnemyMinion(self, oppo_index, oppo_num):
        self.chooseMyHero()
        self.chooseEnemyMinion(oppo_index, oppo_num)