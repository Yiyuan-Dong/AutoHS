from enum import Enum

FSM_LEAVE_HS = "Leave Hearth Stone"
FSM_MAIN_MENU = "Main Menu"
FSM_CHOOSING_HERO = "Choosing Hero"
FSM_MATCHING_OPPONENT = "Match Opponent"
FSM_CHOOSING_CARD = "Choosing Card"
# FSM_NOT_MY_TURN = "Not My Turn"
# FSM_MY_TURN = "My Turn"
FSM_BATTLING = "Battling"
FSM_ERROR = "ERROR"
FSM_QUITTING_BATTLE = "Quitting Battle"
FSM_WAIT_MAIN_MENU = "Wait main menu"

LOG_CONTAINER_ERROR = 0
LOG_CONTAINER_INFO = 1

LOG_LINE_CREATE_GAME = "Create Game"
LOG_LINE_GAME_ENTITY = "Create Game Entity"
LOG_LINE_PLAYER_ENTITY = "Create Player Entity"
LOG_LINE_FULL_ENTITY = "Full Entity"
LOG_LINE_SHOW_ENTITY = "Show Entity"
LOG_LINE_CHANGE_ENTITY = "Change Entity"
LOG_LINE_BLOCK_START = "Block Start"
LOG_LINE_BLOCK_END = "Block End"
LOG_LINE_PLAYER_ID = "Player ID"
LOG_LINE_TAG_CHANGE = "Tag Change"
LOG_LINE_TAG = "Tag"
LOG_LINE_MODE_CHANGE = "Mode Change"

CARD_BASE = "BASE"
CARD_SPELL = "SPELL"
CARD_MINION = "MINION"
CARD_WEAPON = "WEAPON"
CARD_HERO = "HERO"
CARD_HERO_POWER = "HERO_POWER"
CARD_ENCHANTMENT = "ENCHANTMENT"
CARD_LOCATION = "LOCATION"

SPELL_NO_POINT = 0
SPELL_POINT_OPPO = 1
SPELL_POINT_MINE = 2

COORDINATE_MID_X = "mid_x"
COORDINATE_MID_Y = "mid_y"
COORDINATE_HALF_MINION_GAP_X = "half_minion_gap_x"
COORDINATE_MY_MINION_Y = "my_minion_y"
COORDINATE_OPPO_MINION_Y = "oppo_minion_y"
COORDINATE_MY_HERO_Y = "my_hero_tuple_y"
COORDINATE_OPPO_HERO_Y = "oppo_hero_tuple_y"
COORDINATE_CANCEL_X = "cancel_x"
COORDINATE_CANCEL_Y = "cancel_y"
COORDINATE_MY_HAND_X = "my_hand_x"
COORDINATE_MY_HAND_Y = "my_hand_y"
COORDINATE_START_CARD_X = "start_card_x"
COORDINATE_START_CARD_Y = "start_card_y"
COORDINATE_NO_OP_Y = "no_op_y"
COORDINATE_MAIN_MENU_NO_OP_Y = "main_menu_no_op_y"
COORDINATE_SETTING_X = "setting_x"
COORDINATE_SETTING_Y = "setting_y"
COORDINATE_MATCH_OPPONENT_X = "match_opponent_x"
COORDINATE_MATCH_OPPONENT_Y = "match_opponent_y"
COORDINATE_ENTER_BATTLE_Y = "enter_battle_y"
COORDINATE_COMMIT_CHOOSE_START_CARD_Y = "commit_choose_start_card_y"
COORDINATE_END_TURN_X = "end_turn_x"
COORDINATE_END_TURN_Y = "end_turn_y"
COORDINATE_ERROR_REPORT_X = "error_report_x"
COORDINATE_ERROR_REPORT_Y = "error_report_y"
COORDINATE_DISCONNECTED_X = "disconnected_x"
COORDINATE_DISCONNECTED_Y = "disconnected_y"
COORDINATE_EMOJ_LIST = "emoj_list"
COORDINATE_SKILL_X = "skill_x"
COORDINATE_SKILL_Y = "skill_y"
COORDINATE_BATTLEFILED_RANGE_X = "battlefield_range_x"
COORDINATE_BATTLEFILED_RANGE_Y = "battlefield_range_y"
COORDINATE_GIVE_UP_X = "give_up_x"
COORDINATE_GIVE_UP_Y = "give_up_y"

SCREEN_MODE_STARTUP = "STARTUP"                           # 启动炉石
SCREEN_MODE_LOGIN = "LOGIN"                               # 点击进入游戏
SCREEN_MODE_HUB = "HUB"                                   # 可以选择传统对战/酒馆战旗/乱斗的地方
SCREEN_MODE_TOURNAMENT = "TOURNAMENT"                     # 选卡组
SCREEN_MODE_COLLECTIONMANAGER = "COLLECTIONMANAGER"       # 我的收藏
SCREEN_MODE_GAMEPLAY = "GAMEPLAY"                         # 对战中
SCREEN_MODE_TRAVEN_BRAWL = "TRAVENBRAWL"                  # 乱斗
SCREEN_MODE_BACON = "BACON"                               # 酒馆战旗

class SkillType(Enum):
    POINT_TO_NONE = 0
    POINT_TO_MINE = 1
    POINT_TO_OPPONENT = 2