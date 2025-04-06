import json
from autohs_logger import *
from constants.number import OPPO_MINION_DELTA_H_FACTOR, OPPO_HERO_DELTA_H_FACTOR

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
        self.oppo_minion_delta_h_factor = OPPO_MINION_DELTA_H_FACTOR
        self.oppo_hero_delta_h_factor = OPPO_HERO_DELTA_H_FACTOR

    def save_config(self, path="configs.json"):
        try:
            with open(path, "w") as f:
                temp = self.click_coordinates
                temp2 = self.exit_func
                self.click_coordinates = None
                self.exit_func = None
                json.dump(self.__dict__, f)
                logger.info(f"配置文件成功保存至{path}")
                self.click_coordinates = temp
                self.exit_func = temp2
        except (IOError, OSError) as e:
            logger.error(f"保存配置文件时出错: {e}")

    def update_oppo_minion_delta_h_factor(self):
        global OPPO_MINION_DELTA_H_FACTOR
        OPPO_MINION_DELTA_H_FACTOR = self.oppo_minion_delta_h_factor
        logger.info(f"解场权重设置为：{OPPO_MINION_DELTA_H_FACTOR}")

    def update_oppo_hero_delta_h_factor(self):
        global OPPO_HERO_DELTA_H_FACTOR
        OPPO_HERO_DELTA_H_FACTOR = self.oppo_hero_delta_h_factor
        logger.info(f"打脸权重设置为：{OPPO_HERO_DELTA_H_FACTOR}")

    def load_config(self, path="configs.json"):
        logger.info(f"加载配置文件: {path}")
        try:
            with open(path, "r") as f:
                self.__dict__.update(json.load(f))
                logger.info(f"配置文件加载成功，配置：{self.__dict__}")
                self.update_oppo_minion_delta_h_factor()
                self.update_oppo_hero_delta_h_factor()
        except FileNotFoundError:
            logger.error("配置文件 configs.json 未找到")

autohs_config = AutoHSConfig()