from pynput.mouse import Button, Controller
import time

MOUSE_SLEEP_INTERVAL = 3  # 3 seconds

import ctypes

class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]

def get_screen_size():
    rect = RECT()
    ctypes.windll.user32.GetWindowRect(ctypes.windll.user32.GetDesktopWindow(), ctypes.byref(rect))
    width = rect.right - rect.left
    height = rect.bottom - rect.top
    return width, height

width, height = get_screen_size()
print("Width: %s, Height: %s" % (width, height))

def main():
    mouse = Controller()
    w,h = get_screen_size()
    # Read pointer position
    print("The current pointer position is {0}".format(mouse.position))
    print("Now please stare at your mouse, not the terminal :)")
    print("The mouse will move to the center of the screen\n")

    time.sleep(MOUSE_SLEEP_INTERVAL)
    # Set pointer position
    mouse.position = (w/2, h/2)
    print("Now we have moved it to {0}".format(mouse.position))
    print("A move based on absolute position")
    print("Then the mouse will move to the right\n")

    time.sleep(MOUSE_SLEEP_INTERVAL)
    # Move pointer relative to current position
    mouse.move(50, 0)
    print("Now we have moved it to {0}".format(mouse.position))
    print("A move based on relative position")
    print("Then we will click the right mouse button\n")

    time.sleep(MOUSE_SLEEP_INTERVAL)
    # Press and release
    mouse.press(Button.right)
    mouse.release(Button.right)

    print("Then we will move to the left and double click the left mouse button\n")
    time.sleep(MOUSE_SLEEP_INTERVAL)
    mouse.move(-50, 0)
    # Double click; this is different from pressing and releasing
    mouse.click(Button.left, 2)


if __name__ == "__main__":
     main()