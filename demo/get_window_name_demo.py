import win32api
import win32gui
import win32con
import time

hwnd_title = {}
NAME = "战网"


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


if __name__ == "__main__":
    win32gui.EnumWindows(get_all_hwnd, 0)

    for h, t in hwnd_title.items():
        if t is not "":
            print(h, ":", t)

    hwnd = win32gui.FindWindow(None, NAME)
    print()
    title = win32gui.GetWindowText(hwnd)
    clsname = win32gui.GetClassName(hwnd)
    print(title, ":", clsname)

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    print("\n", left, top, right, bottom)
