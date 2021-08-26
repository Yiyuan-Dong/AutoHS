from FSM_action import system_exit, AutoHS_automata
import keyboard
from log_state import check_name
from print_info import print_info_init
from FSM_action import init

if __name__ == "__main__":
    check_name()
    print_info_init()
    init()
    keyboard.add_hotkey("ctrl+q", system_exit)
    AutoHS_automata()
