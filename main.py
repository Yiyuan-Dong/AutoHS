from FSM_action import system_exit, AutoHS_automata
import keyboard
from log_state import check_name
from print_info import print_info_init
from FSM_action import init

if __name__ == "__main__":
    # check_name()
    print_info_init()
    init()
    keyboard.add_hotkey("ctrl+q", system_exit)
    args = {
        "MERC_NAME": ["拉格纳罗斯", "迦顿男爵", "安东尼达斯"],
        "MERC_SKILL": [1, 1, 0],
        "MERC_TARGET": [-1, -1, 1]
    }
    AutoHS_automata(args)
