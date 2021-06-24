from pynput.mouse import Button, Controller
import get_screen
import catch_screen_demo
import time
import cv2

AREA_LIST_4 = [((622, 600), (822, 800), (722, 1000)),
               ((753, 600), (953, 800), (853, 1000)),
               ((884, 600), (1084, 800), (980, 1000)),
               ((1015, 600), (1215, 800), (1115, 1000)),
               ((1495, 465), (1620, 522)),
               ]

step_5 = 105
AREA_list_5 = [((608 + step_5 * i, 600),
                (608 + 200 + step_5 * i, 800),
                (608 + 100 + step_5 * i, 1000)
                ) for i in range(5)
               ]

step = [0, 0, 140, 139, 131, 105, 88, 75, 66, 58, 52]
start = [0, 819, 749, 679, 622, 608, 599, 593, 588, 585, 582]
card_num = 1
AREA_LIST = [((start[card_num] + step[card_num] * i, 600),
              (start[card_num] + 200 + step[card_num] * i, 800),
              (start[card_num] + 65 + step[card_num] * i, 1000)
              ) for i in range(card_num)
             ]

if __name__ == "__main__":
    im_opencv = get_screen.catch_screen()

    mouse = Controller()
    for area in AREA_LIST:
        if len(area) < 2 or len(area) > 3:
            print("[Usage]: ((left-top), (botton-right), [mouse-position])")
        if len(area) == 2:
            top_left, right_bottom = area
        else:
            top_left, right_bottom, mouse_pos = area
            mouse.position = mouse_pos
            time.sleep(0.1)
            im_opencv = get_screen.catch_screen()
        catch_screen_demo.show_area(im_opencv, top_left, right_bottom, 4)

    cv2.destroyAllWindows()
