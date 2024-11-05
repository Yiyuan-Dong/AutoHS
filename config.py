import json
from autohs_logger import *

class AutoHSConfig:
    def __init__(self):
        self.is_running = 0
        self.width = 0
        self.height = 0
        self.max_play_time = 0
        self.max_win_count = 0
        self.hearthstone_install_path = ""
        self.player_name = ""

    def save_config(self, path="configs.json"):
        try:
            with open(path, "w") as f:
                json.dump(self.__dict__, f)
                logger.info("配置文件保存成功")
        except (IOError, OSError) as e:
            logger.error(f"保存配置文件时出错: {e}")

    def load_config(self, path="configs.json"):
        try:
            with open(path, "r") as f:
                self.__dict__.update(json.load(f))
                logger.info(f"配置文件加载成功，配置：{self.__dict__}")
        except FileNotFoundError:
            logger.error("配置文件 configs.json 未找到")