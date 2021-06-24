import imagehash
from pynput.mouse import Button, Controller
import get_screen
import catch_screen_demo
import time
import cv2
from constants.constants import *
from constants.cards_info import *

if __name__ == "__main__":
    img = get_screen.catch_screen()
    img = cv2.GaussianBlur(img, (3, 3), 0)
    canny = cv2.Canny(img, 50, 150)
    cv2.imshow("canny", canny)
    cv2.waitKey()
    print(canny[300: 305, 300:302])
    cv2.destroyAllWindows()

    flag = 0
    for i in range(7, 0, -1):
        baseline = 960 - i * 70
        part_canny = canny[390:490, baseline:baseline + 40]
        if sum(sum(part_canny > 0)) > 100:
            flag = i
            break
    print(flag)

    flag = 0
    for i in range(7, 0, -1):
        baseline = 960 - i * 70
        part_canny = canny[510:610, baseline:baseline + 40]
        if sum(sum(part_canny > 0)) > 100:
            flag = i
            break
    print(flag)

    cv2.destroyAllWindows()
