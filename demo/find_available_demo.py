import sys
import add_parent_dir
import get_screen
from constants.constants import *
from constants.hash_vals import *
import cv2


# 不能动:0, 突袭:1, 冲锋:2
if __name__ == "__main__":
    img = get_screen.catch_screen()
    _, mine_num = get_screen.count_minions(img)
    res = get_screen.test_available(img, mine_num)
    print(res)
