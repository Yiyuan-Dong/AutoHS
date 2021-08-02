import sys

import requests
import json
import os
from print_info import *


# 来源于互联网的炉石JSON数据下载API, 更多信息可以访问 https://hearthstonejson.com/
def download_json(json_path):
    json_url = "https://api.hearthstonejson.com/v1/latest/zhCN/cards.json"
    file = requests.get(json_url)

    with open(json_path, "wb") as f:
        f.write(file.content)


def read_json(re_download=False):
    dir_path = os.path.dirname(__file__)
    if dir_path == "":
        dir_path = "."
    json_path = dir_path + "/cards.json"

    if not os.path.exists(json_path):
        sys_print("未找到cards.json,试图通过网络下载文件")
        download_json(json_path)
    elif re_download:
        sys_print("疑似有新版本炉石数据，正在重新下载最新文件")
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


def query_json_dict(key):
    global JSON_DICT

    if key == "":
        return "Unknown"

    if key in JSON_DICT:
        return JSON_DICT[key]["name"]
    # 认为是炉石更新了，出现了新卡，需要重新下载。
    else:
        JSON_DICT = read_json(True)
        if key not in JSON_DICT:
            error_print("出现未识别卡牌，程序无法继续")
            sys.exit(-1)
        return JSON_DICT[key]["name"]


JSON_DICT = read_json()

if __name__ == "__main__":
    with open("id-name.txt", "w", encoding="utf8") as f:
        for key, val in JSON_DICT.items():
            f.write(key + " " + val["name"] + "\n")

    query_json_dict("SW_085t")
