import sys

import get_screen

if __name__ == "__main__":
    print(get_screen.count_my_cards())
    sys.exit(0)

    # 之后这段代码分步展示了如何数出手牌数量
    # mouse = Controller()
    # last_part = numpy.zeros((200, 200, 3))
    # last_part = last_part.astype(numpy.uint8)
    # count = 0
    #
    # step = 30
    # for x in range(590, 1281, step):
    #     mouse.position = (x, 1030)
    #     time.sleep(0.1)
    #
    #     img = get_screen.catch_screen()
    #
    #     left_part, right_part = get_screen.test_card_with_x(img, x, step, True)
    #
    #     last_image = Image.fromarray(last_part)
    #     last_hash = imagehash.phash(last_image)
    #     curr_image = Image.fromarray(left_part)
    #     curr_hash = imagehash.phash(curr_image)
    #
    #     print(last_hash)
    #     print(curr_hash)
    #
    #     print(last_hash - curr_hash)
    #     if last_hash - curr_hash > 18:
    #         count += 1
    #
    #
    #     last_part = right_part
    #     cv2.waitKey()
    #
    # cv2.destroyAllWindows()
    # print(count)
    # exit(0)
