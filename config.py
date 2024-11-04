import json

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
        except (IOError, OSError) as e:
            print(f"保存配置文件时出错: {e}")

    def load_config(self, path="configs.json"):
        try:
            with open(path, "r") as f:
                self.__dict__.update(json.load(f))
        except FileNotFoundError:
            print("配置文件 configs.json 未找到")