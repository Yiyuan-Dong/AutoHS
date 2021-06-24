import cv2
from pynput.mouse import Button, Controller
import get_screen
import time
import numpy
import imagehash
from PIL import Image

if __name__ == "__main__":
    print(get_screen.count_my_cards())

    exit(0)
    # 之后这段代码分步展示了如何数出手牌数量

    mouse = Controller()
    last_part = numpy.zeros((200, 200, 3))
    last_part = last_part.astype(numpy.uint8)
    count = 0

    for x in range(500, 1301, 40):
        mouse.position = (x, 1030)
        time.sleep(0.1)

        img = get_screen.catch_screen()

        left_part, right_part = get_screen.get_card_with_x(img, x, 40, True)

        last_image = Image.fromarray(last_part)
        last_hash = imagehash.phash(last_image)
        curr_image = Image.fromarray(left_part)
        curr_hash = imagehash.phash(curr_image)
        if last_hash - curr_hash > 10:
            count += 1

        last_part = right_part
        cv2.waitKey()

    cv2.destroyAllWindows()
    print(count)
    exit(0)
