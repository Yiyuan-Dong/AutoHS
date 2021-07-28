import re

from card import *
from constants.card_name import *

NAME2CARD = {
    "护甲商贩": ArmorVendor(),
    "神圣惩击": HolySmite(),
    "倦怠光波": WaveOfApathy(),
    "噬骨殴斗者": BonechewerBrawler(),
    "暗言术：灭": ShadowWordDeath(),
    "神圣化身": Apotheosis(),
    "亡首教徒": DeathsHeadCultist(),
    "噬灵疫病": DevouringPlague(),
    "狂傲的兽人": OverconfidentOrc(),
    "神圣新星": HolyNova(),
    "狂乱": Hysteria(),
    "暗言术：毁": ShadowWordRuin(),
    "除奇致胜": AgainstAllOdds(),
    "锈骑劫匪": RuststeedRaider(),
    "泰兰·弗丁": TaelanFordring(),
    "凯恩·血蹄": CairneBloodhoof(),
    "吞噬者穆坦努斯": MutanusTheDevourer(),
    "灵魂之镜": SoulMirror(),
    "戈霍恩之血": BloodOfGhuun(),
    NAME_THE_COIN: Coin(),
}

BASE_COIN_PATTERN = re.compile(r".*_COIN\d$")


def is_coin_id(card_id):
    if card_id in ["GAME_005", "GAME_005e"]:
        return True
    return BASE_COIN_PATTERN.match(card_id) is not None
