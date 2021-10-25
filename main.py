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
        # 这三个list内元素的相对顺序需要一致
        "MERC_NAME": ["拉格纳罗斯", "迦顿男爵", "安东尼达斯"],  # 上场打伤害的随从的名字
        "MERC_SKILL": [1, 1, 0],  # 要使用哪个技能, 0是第一个, 1是第二个. 这里是死吧虫子, 地狱火, 火球术
        "MERC_TARGET": [-1, -1, 1]  # 指向敌方那个随从, -1是不指向, 0是左数第一个, 1是左数第二个
    }
    AutoHS_automata(args)
