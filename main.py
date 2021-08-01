import FSM_action
import keyboard
from game_state import check_name


if __name__ == "__main__":
    check_name()
    keyboard.add_hotkey("ctrl+q", FSM_action.system_exit)
    FSM_action.AutoHS_automata()
