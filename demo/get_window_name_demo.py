import sys

import win32gui

hwnd_title = {}
NAME = "炉石传说"
# NAME = "战网"


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


if __name__ == "__main__":
    win32gui.EnumWindows(get_all_hwnd, 0)

    print(f"HWND : NAME")
    for h, t in hwnd_title.items():
        if t != "":
            print(h, ":", t)

    hwnd = win32gui.FindWindow(None, NAME)
    if hwnd == 0:
        print("未找到应用")
        sys.exit(-1)

    title = win32gui.GetWindowText(hwnd)
    clsname = win32gui.GetClassName(hwnd)
    print(title, ":", clsname)

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    print("位置:", left, top, right, bottom)