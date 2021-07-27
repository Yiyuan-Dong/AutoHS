import json
import os

import requests

from print_info import *


def download_json(json_path):
    json_url = "https://api.hearthstonejson.com/v1/latest/zhCN/cards.json"
    file = requests.get(json_url)

    with open(json_path, "wb") as f:
        f.write(file.content)


def read_json():
    dir_path = os.path.dirname(__file__)
    if dir_path == "":
        dir_path = "."
    json_path = dir_path + "/cards.json"

    if not os.path.exists(json_path):
        sys_print("未找到cards.json,试图通过网络下载文件")
        download_json(json_path)
    else:
        sys_print("cards.json已存在")

    with open(json_path, "r", encoding="utf8") as f:
        json_string = f.read()
        json_list = json.loads(json_string)
        json_dict = {}
        for item in json_list:
            json_dict[item["id"]] = item
        return json_dict


if __name__ == "__main__":
    json_dict = read_json()
    print(json_dict["VAN_EX1_048"])
