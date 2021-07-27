import cv2

import get_screen

if __name__ == "__main__":
    img = get_screen.catch_screen()

    # 这个canny边缘图让你有更直观的理解
    img = cv2.GaussianBlur(img, (3, 3), 0)
    canny = cv2.Canny(img, 50, 150)
    cv2.imshow("canny", canny)
    cv2.waitKey()
    cv2.destroyAllWindows()

    print(get_screen.count_minions(img))

    cv2.destroyAllWindows()
