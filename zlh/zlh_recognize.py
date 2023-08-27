import sys
sys.path.append(r"..")
import get_screen
import time
# from get_screen import *


def test_screen():
    MY_FSM_state = ""
    if get_screen.test_hs_available():
        hs_hwnd = get_screen.get_HS_hwnd()
        get_screen.move_window_foreground(hs_hwnd)
        time.sleep(0.5)
    # FSM_state = FSM_CHOOSING_CARD
    if MY_FSM_state == "":
        MY_FSM_state = get_screen.get_state()
        print(MY_FSM_state)

if __name__ == "__main__":
    test_screen()