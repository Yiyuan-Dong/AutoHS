import add_parent_dir
import get_screen
import cv2

if __name__ == "__main__":
    img = get_screen.catch_screen()
    img = cv2.GaussianBlur(img, (3, 3), 0)
    canny = cv2.Canny(img, 50, 150)
    cv2.imshow("canny", canny)
    cv2.waitKey()
    cv2.destroyAllWindows()

    print(get_screen.count_minions(img))

    cv2.destroyAllWindows()
