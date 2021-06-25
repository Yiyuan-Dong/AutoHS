import pickle

import imagehash
from pynput.mouse import Button, Controller
import get_screen
import catch_screen_demo
import time
import cv2
from constants.constants import *
from constants.hash_vals import *
import sklearn
import numpy

steps_oppos = [0, 140, 140, 139, 139, 139, 139, 139]
steps_mine = [0, 140, 140, 140, 140, 140, 140, 140]


def find_closest(img_hash, hash_dict):
    min_diff = 64
    flag = -1
    for k, v in hash_dict.items():
        if get_screen.hash_diff(k, str(img_hash)) < min_diff:
            min_diff = get_screen.hash_diff(k, str(img_hash))
            flag = v

    return flag, min_diff


if __name__ == "__main__":
    oppos, mine = get_screen.count_minions()
    print(oppos, mine)

    img = get_screen.catch_screen()

    mine_baseline = 960 - int((mine - 1) * steps_mine[mine] / 2)
    oppos_baseline = 960 - int((oppos - 1) * steps_oppos[oppos] / 2)

    with open("SVC_poly", "rb") as f:
        svc = pickle.load(f)

    for i in range(mine + oppos):
        if i < mine:
            print(f"Mine[{i}]:")
            baseline = mine_baseline + i * steps_mine[mine]
            attack_img = img[626:652, baseline - 47:baseline - 28]
            health_img = img[626:652, baseline + 29:baseline + 48]

        else:
            print(f"Oppos[{i - mine}]:")
            baseline = oppos_baseline + (i - mine) * steps_oppos[oppos]
            print(baseline)
            attack_img = img[438:464, baseline - 47:baseline - 28]
            health_img = img[438:464, baseline + 29:baseline + 48]

        grey_health_img = get_screen.health_attack_number_in_img(health_img)
        grey_attack_img = get_screen.health_attack_number_in_img(attack_img)

        attack_hash = get_screen.image_hash(grey_attack_img)
        print(f"attack: {attack_hash}, {find_closest(attack_hash, ATTACK_NUMBER_HASH)}")
        health_hash = get_screen.image_hash(grey_health_img)
        print(f"health: {health_hash}, {find_closest(health_hash, ATTACK_NUMBER_HASH)}")

        cv2.imshow("attack", attack_img)
        cv2.imshow("health", health_img)

        grey_attack_img = cv2.resize(grey_attack_img, (grey_attack_img.shape[1] * 5, grey_attack_img.shape[0] * 5))
        grey_health_img = cv2.resize(grey_health_img, (grey_health_img.shape[1] * 5, grey_health_img.shape[0] * 5))
        cv2.imshow("attack_grey", grey_attack_img)
        cv2.imshow("health_grey", grey_health_img)
        cv2.waitKey()

    cv2.destroyAllWindows()
