import json
import platform
from utils.autohs_logger import *
from constants.pixel_coordinate import COORDINATES_1920_1080, COORDINATES_2560_1440, get_screen_resolution
# 每个回合开始发个表情的概率
EMOJ_RATIO = 0.05

# 随从相互攻击的启发值包括两个部分：敌方随从受伤的带来的收益；
# 以及我方随从受伤带来的损失。下面两个比例表示这两个启发值变化
# 数值应该以怎样权值比例相加。如果是控制卡组，可以略微调高
# OPPO_MINION_DELTA_H_FACTOR 来鼓励解场；如果是快攻卡组则反之
OPPO_MINION_DELTA_H_FACTOR = 1
MY_MINION_DELTA_H_FACTOR = 1
# OPPO_HERO_DELTA_H_FACTOR 越高就越喜欢打脸
OPPO_HERO_DELTA_H_FACTOR = 2

# 对于没有单独建一个类去描述的卡牌, 如果它的法力值花费大于这个值,
# 就在留牌阶段被换掉
REPLACE_COST_BAR = 3

# 鼠标点击相关
OPERATE_INTERVAL = 0.2
STATE_CHECK_INTERVAL = 1
TINY_OPERATE_INTERVAL = 0.1
BASIC_MINION_PUT_INTERVAL = 0.8
BASIC_SPELL_WAIT_TIME = 1.5
BASIC_WEAPON_WAIT_TIME = 1
PLATFORM = platform.system()


class AutoHSConfig:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.max_play_time = 0
        self.max_win_count = 0
        self.hearthstone_install_path = ""
        self.user_name = ""
        self.give_up_with_dignity = False
        self.click_coordinates = None
        self.exit_func = None
        self.debug_log_start = False
        self.has_loading_screen = False

        self.emoj_ratio = EMOJ_RATIO
        self.oppo_minion_delta_h_factor = OPPO_MINION_DELTA_H_FACTOR
        self.my_minion_delta_h_factor = MY_MINION_DELTA_H_FACTOR
        self.oppo_hero_delta_h_factor = OPPO_HERO_DELTA_H_FACTOR
        self.replace_cost_bar = REPLACE_COST_BAR
        self.operate_interval = OPERATE_INTERVAL
        self.state_check_interval = STATE_CHECK_INTERVAL
        self.tiny_operate_interval = TINY_OPERATE_INTERVAL
        self.basic_minion_put_interval = BASIC_MINION_PUT_INTERVAL
        self.basic_spell_wait_time = BASIC_SPELL_WAIT_TIME
        self.basic_weapon_wait_time = BASIC_WEAPON_WAIT_TIME

    def save_config(self, path="configs.json"):
        try:
            with open(path, "w") as f:
                export_dict = {k: v for k, v in self.__dict__.items() if k not in ["click_coordinates", "exit_func", "has_loading_screen"]}
                json.dump(export_dict, f)
                logger.info(f"配置文件成功保存至{path}")
        except (IOError, OSError) as e:
            logger.error(f"保存配置文件时出错: {e}")

    def load_config(self, path="configs.json"):
        logger.info(f"加载配置文件: {path}")
        try:
            with open(path, "r") as f:
                self.__dict__.update(json.load(f))
                logger.info(f"配置文件加载成功，配置：{self.__dict__}")
        except FileNotFoundError:
            logger.error("配置文件 configs.json 未找到")


autohs_config = AutoHSConfig()
WIDTH, HEIGHT = get_screen_resolution()
if WIDTH == 1920 and HEIGHT == 1080:
    coors = COORDINATES_1920_1080
elif WIDTH == 2560 and HEIGHT == 1440:
    coors = COORDINATES_2560_1440
else:
    logger.error(f"未找到对应分辨率的点击坐标，当前分辨率为{WIDTH}X{HEIGHT}")
autohs_config.click_coordinates = COORDINATES_2560_1440
