# -*- coding: UTF-8 -*-

"""
__Author__ = "MakiNaruto"
__Mail__: "become006@gmail.com"
__Version__ = "1.0.1"
__Created__ = "2024/10/11"
__Description__ = ""
"""

from controller.base.cards import CardsController
from controller.base.game import GameController
from controller.base.hero import HeroController
from controller.base.minion import MinionController
from controller.base.attack import AttackController


class Controller:
    def __init__(self) -> None:
        self.cards = CardsController()
        self.game = GameController()
        self.hero = HeroController()
        self.minion = MinionController()
        self.attack = AttackController()


controller = Controller()
