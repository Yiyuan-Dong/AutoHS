import imagehash
from pynput.mouse import Button, Controller
import get_screen
import catch_screen_demo
import time
import cv2
from constants.constants import *
from constants.cards_info import *

# AREA_LIST_4 = [((622, 600), (822, 800), (722, 1000)),
#                ((753, 600), (953, 800), (853, 1000)),
#                ((884, 600), (1084, 800), (980, 1000)),
#                ((1015, 600), (1215, 800), (1115, 1000)),
#                ((1495, 465), (1620, 522)),
#                ]
#
# step_5 = 105
# AREA_list_5 = [((608 + step_5 * i, 600),
#                 (608 + 200 + step_5 * i, 800),
#                 (608 + 100 + step_5 * i, 1000)
#                 ) for i in range(5)
#                ]


step = STEP
start = START

if __name__ == "__main__":
    card_num = get_screen.count_my_cards()
    print(f"I have cards {card_num}")

    area_list = [((start[card_num] + step[card_num] * i, 600),
                  (start[card_num] + 200 + step[card_num] * i, 800),
                  (start[card_num] + 65 + step[card_num] * i, 1000)
                  ) for i in range(card_num)
                 ]

    im_opencv = get_screen.catch_screen()

    mouse = Controller()

    for i in range(len(area_list)):
        area = area_list[i]
        if len(area) < 2 or len(area) > 3:
            print("[Usage]: ((left-top), (botton-right), [mouse-position])")
        if len(area) == 2:
            top_left, bottom_right = area
        else:
            top_left, bottom_right, mouse_pos = area
            mouse.position = mouse_pos
            time.sleep(0.1)
            im_opencv = get_screen.catch_screen()
        # catch_screen_demo.show_area(im_opencv, top_left, bottom_right, 4)

        hash = get_screen.get_card_hash(card_num, i)
        min_diff = 64
        name = "?"
        for k, v in CARD_HASH_INFO.items():
            temp_diff = bin(int(k, 16) ^ int(str(hash), 16))[2:].count("1")
            if temp_diff < min_diff:
                min_diff = temp_diff
                name = v
        print(f"The name of the card at [{i}] is {name}")

    cv2.destroyAllWindows()
