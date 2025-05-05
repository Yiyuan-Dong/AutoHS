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
from enum import Enum

class Controller:
    def __init__(self) -> None:
        self.cards = CardsController()
        self.game = GameController()
        self.hero = HeroController()
        self.minion = MinionController()
        self.attack = AttackController()

class PositionIndexType(Enum):
    INVALID = 0,
    MY_HERO = 1,
    OPPO_HERO = 2,
    MY_MINION = 3,
    OPPO_MINION = 4,

class PositionIndex:
    def __init__(self, position_type: PositionIndexType, index: int):
        self.position_type = position_type
        self.index = index

    def __str__(self):
        return f"PositionIndex(type={self.position_type}, index={self.index})"

    def is_valid(self):
        return self.position_type != PositionIndexType.INVALID

    def is_my_minion(self):
        return self.position_type == PositionIndexType.MY_MINION

controller = Controller()
