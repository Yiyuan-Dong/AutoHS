# 你的Power.log的路径, 应该在你的炉石安装目录下的`Logs/`文件夹中, 这里放的是我的路径
# ** 一定要修改成自己电脑上的路径 **
HEARTHSTONE_POWER_LOG_PATH = "C:\Program Files (x86)\Apps\Hearthstone\Logs\Hearthstone_2023_08_28_21_21_10\Power.log"

# 你的炉石用户名, 注意英文标点符号'#', 把后面的数字也带上
# 可以输入中文
YOUR_NAME = "ChangeThis#54321"

# 关于控制台信息打印的设置
DEBUG_PRINT = True
WARN_PRINT = True
SYS_PRINT = True
INFO_PRINT = True
ERROR_PRINT = True

# 关于文件信息输出的设置
DEBUG_FILE_WRITE = True
WARN_FILE_WRITE = True
SYS_FILE_WRITE = True
INFO_FILE_WRITE = True
ERROR_FILE_WRITE = True

# 每个回合开始发个表情的概率
EMOJ_RATIO = 0.15

# 随从相互攻击的启发值包括两个部分：敌方随从受伤的带来的收益；
# 以及我方随从受伤带来的损失。下面两个比例表示这两个启发值变化
# 数值应该以怎样权值比例相加。如果是控制卡组，可以略微调高
# OPPO_DELTA_H_FACTOR 来鼓励解场
OPPO_DELTA_H_FACTOR = 1.2
MY_DELTA_H_FACTOR = 1

# 对于没有单独建一个类去描述的卡牌, 如果它的法力值花费大于这个值,
# 就在流留牌阶段被换掉
REPLACE_COST_BAR = 3

OPERATE_INTERVAL = 0.2
STATE_CHECK_INTERVAL = 1
TINY_OPERATE_INTERVAL = 0.1
BASIC_MINION_PUT_INTERVAL = 0.8
BASIC_SPELL_WAIT_TIME = 1.5
BASIC_WEAPON_WAIT_TIME = 1

# 我觉得这行注释之后的内容应该不需要修改……
FSM_LEAVE_HS = "Leave Hearth Stone"
FSM_MAIN_MENU = "Main Menu"
FSM_CHOOSING_HERO = "Choosing Hero"
FSM_MATCHING = "Match Opponent"
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

CARD_BASE = "BASE"
CARD_SPELL = "SPELL"
CARD_MINION = "MINION"
CARD_WEAPON = "WEAPON"
CARD_HERO = "HERO"
CARD_HERO_POWER = "HERO_POWER"
CARD_ENCHANTMENT = "ENCHANTMENT"

SPELL_NO_POINT = 0
SPELL_POINT_OPPO = 1
SPELL_POINT_MINE = 2


CLICK_MAIN_START_GAME = "start game"
CLICK_MAIN_START_SINGLE_GAME = "start single game"
CLICK_MAIN_START_OPTION = "start option"
CLICK_MAIN_QUIT_GAME = "quit game"
CLICK_MAIN_START_MISSION = "start mission"
CLICK_MAIN_START_REWARD = "start reward"
CLICK_MAIN_NEXT_REWARD = "next reward"
CLICK_MAIN_PREV_REWARD = "prev reward"

CLICK_ANOTHER_MODE = "click another mode"
CLICK_PRITICE_MODE = "click pritice mode"
CLICK_PRITICE_MODE_NEXT = "click pritice mode next"
CLICK_PRITICE_MODE_NEXT_START_GAME = "lick pritice mode next start game"

SINGLE_GAME_CHOSE_HERO_PRE = "choose single game hero "
SINGLE_GAME_CHOSE_HERO_1 = "choose single game hero 1"
SINGLE_GAME_CHOSE_HERO_2 = "choose single game hero 2"
SINGLE_GAME_CHOSE_HERO_3 = "choose single game hero 3"
SINGLE_GAME_CHOSE_HERO_4 = "choose single game hero 4"
SINGLE_GAME_CHOSE_HERO_5 = "choose single game hero 5"
SINGLE_GAME_CHOSE_HERO_6 = "choose single game hero 6"
SINGLE_GAME_CHOSE_HERO_7 = "choose single game hero 7"
SINGLE_GAME_CHOSE_HERO_8 = "choose single game hero 8"
SINGLE_GAME_CHOSE_HERO_9 = "choose single game hero 9"

SINGLE_GAME_CHOSE_HERO_OPPO_PRE = "choose single game hero oppo "
SINGLE_GAME_CHOSE_HERO_OPPO_1 = "choose single game hero oppo 1"
SINGLE_GAME_CHOSE_HERO_OPPO_2 = "choose single game hero oppo 2"
SINGLE_GAME_CHOSE_HERO_OPPO_3 = "choose single game hero oppo 3"
SINGLE_GAME_CHOSE_HERO_OPPO_4 = "choose single game hero oppo 4"
SINGLE_GAME_CHOSE_HERO_OPPO_5 = "choose single game hero oppo 5"
SINGLE_GAME_CHOSE_HERO_OPPO_6 = "choose single game hero oppo 6"
SINGLE_GAME_CHOSE_HERO_OPPO_7 = "choose single game hero oppo 7"
SINGLE_GAME_CHOSE_HERO_OPPO_8 = "choose single game hero oppo 8"
SINGLE_GAME_CHOSE_HERO_OPPO_9 = "choose single game hero oppo 9"
SINGLE_GAME_CHOSE_HERO_OPPO_10 = "choose single game hero oppo 10"
SINGLE_GAME_START_GAME = "start single game"

CLICK_CHOSE_HERO_OPEN_GAME = "open game"
CLICK_CHOSE_HERO_CANCEL_GAME = "cancel game"
CLICK_CHOSE_HERO_1_CLICK = "chose hero 1"
CLICK_CHOSE_HERO_2_CLICK = "chose hero 2"
CLICK_CHOSE_HERO_3_CLICK = "chose hero 3"
CLICK_CHOSE_HERO_4_CLICK = "chose hero 4"
CLICK_CHOSE_HERO_5_CLICK = "chose hero 5"
CLICK_CHOSE_HERO_6_CLICK = "chose hero 6"
CLICK_CHOSE_HERO_7_CLICK = "chose hero 7"
CLICK_CHOSE_HERO_8_CLICK = "chose hero 8"
CLICK_CHOSE_HERO_9_CLICK = "chose hero 9"

CLICK_CHOSE_CARD_LATER_1 = "later chose card 1"
CLICK_CHOSE_CARD_LATER_2 = "later chose card 2"
CLICK_CHOSE_CARD_LATER_3 = "later chose card 3"
CLICK_CHOSE_CARD_LATER_4 = "later chose card 4"
CLICK_CHOSE_CARD_LATER_CONFIRM = "later chose card confirm"


CLICK_BATTLE_HERO_POWER_CLICK = "use hero power"
CLICK_BATTLE_END_TURN_CLICK = "end turn"
CLICK_BATTLE_OPTION_CLICK = "battle option"
CLICK_BATTLE_SURRENDER_CLICK = "battle surrender"
CLICK_BATTLE_QUITGAME_CLICK = "battle quit game"

CLICK_CHOSE_HAND_x_PRE = "chose hand "
CLICK_CHOSE_HAND_x_MID = "/"

CLICK_CHOSE_HAND_1_1 = "chose hand 1/1"

CLICK_CHOSE_HAND_1_2 = "chose hand 1/2"
CLICK_CHOSE_HAND_2_2 = "chose hand 2/2"

CLICK_CHOSE_HAND_1_3 = "chose hand 1/3"
CLICK_CHOSE_HAND_2_3 = "chose hand 2/3"
CLICK_CHOSE_HAND_3_3 = "chose hand 3/3"

CLICK_CHOSE_HAND_1_4 = "chose hand 1/4"
CLICK_CHOSE_HAND_2_4 = "chose hand 2/4"
CLICK_CHOSE_HAND_3_4 = "chose hand 3/4"
CLICK_CHOSE_HAND_4_4 = "chose hand 4/4"

CLICK_CHOSE_HAND_1_5 = "chose hand 1/5"
CLICK_CHOSE_HAND_2_5 = "chose hand 2/5"
CLICK_CHOSE_HAND_3_5 = "chose hand 3/5"
CLICK_CHOSE_HAND_4_5 = "chose hand 4/5"
CLICK_CHOSE_HAND_5_5 = "chose hand 5/5"

CLICK_CHOSE_HAND_1_6 = "chose hand 1/6"
CLICK_CHOSE_HAND_2_6 = "chose hand 2/6"
CLICK_CHOSE_HAND_3_6 = "chose hand 3/6"
CLICK_CHOSE_HAND_4_6 = "chose hand 4/6"
CLICK_CHOSE_HAND_5_6 = "chose hand 5/6"
CLICK_CHOSE_HAND_6_6 = "chose hand 6/6"

CLICK_CHOSE_HAND_1_7 = "chose hand 1/7"
CLICK_CHOSE_HAND_2_7 = "chose hand 2/7"
CLICK_CHOSE_HAND_3_7 = "chose hand 3/7"
CLICK_CHOSE_HAND_4_7 = "chose hand 4/7"
CLICK_CHOSE_HAND_5_7 = "chose hand 5/7"
CLICK_CHOSE_HAND_6_7 = "chose hand 6/7"
CLICK_CHOSE_HAND_7_7 = "chose hand 7/7"

CLICK_CHOSE_HAND_1_8 = "chose hand 1/8"
CLICK_CHOSE_HAND_2_8 = "chose hand 2/8"
CLICK_CHOSE_HAND_3_8 = "chose hand 3/8"
CLICK_CHOSE_HAND_4_8 = "chose hand 4/8"
CLICK_CHOSE_HAND_5_8 = "chose hand 5/8"
CLICK_CHOSE_HAND_6_8 = "chose hand 6/8"
CLICK_CHOSE_HAND_7_8 = "chose hand 7/8"
CLICK_CHOSE_HAND_8_8 = "chose hand 8/8"

CLICK_CHOSE_HAND_1_9 = "chose hand 1/9"
CLICK_CHOSE_HAND_2_9 = "chose hand 2/9"
CLICK_CHOSE_HAND_3_9 = "chose hand 3/9"
CLICK_CHOSE_HAND_4_9 = "chose hand 4/9"
CLICK_CHOSE_HAND_5_9 = "chose hand 5/9"
CLICK_CHOSE_HAND_6_9 = "chose hand 6/9"
CLICK_CHOSE_HAND_7_9 = "chose hand 7/9"
CLICK_CHOSE_HAND_8_9 = "chose hand 8/9"
CLICK_CHOSE_HAND_9_9 = "chose hand 9/9"

CLICK_CHOSE_HAND_1_10 = "chose hand 1/10"
CLICK_CHOSE_HAND_2_10 = "chose hand 2/10"
CLICK_CHOSE_HAND_3_10 = "chose hand 3/10"
CLICK_CHOSE_HAND_4_10 = "chose hand 4/10"
CLICK_CHOSE_HAND_5_10 = "chose hand 5/10"
CLICK_CHOSE_HAND_6_10 = "chose hand 6/10"
CLICK_CHOSE_HAND_7_10 = "chose hand 7/10"
CLICK_CHOSE_HAND_8_10 = "chose hand 8/10"
CLICK_CHOSE_HAND_9_10 = "chose hand 9/10"
CLICK_CHOSE_HAND_10_10 = "chose hand 10/10"


CLICK_CHOSE_OPPO_x_PRE = "chose oppo "
CLICK_CHOSE_OPPO_x_MID = "/"
CLICK_CHOSE_OPPO_BATLE_0_0 = "chose oppo 0/0"

CLICK_CHOSE_OPPO_BATLE_1_1 = "chose oppo 1/1"

CLICK_CHOSE_OPPO_BATLE_1_2 = "chose oppo 1/2"
CLICK_CHOSE_OPPO_BATLE_2_2 = "chose oppo 2/2"

CLICK_CHOSE_OPPO_BATLE_1_3 = "chose oppo 1/3"
CLICK_CHOSE_OPPO_BATLE_2_3 = "chose oppo 2/3"
CLICK_CHOSE_OPPO_BATLE_3_3 = "chose oppo 3/3"

CLICK_CHOSE_OPPO_BATLE_1_4 = "chose oppo 1/4"
CLICK_CHOSE_OPPO_BATLE_2_4 = "chose oppo 2/4"
CLICK_CHOSE_OPPO_BATLE_3_4 = "chose oppo 3/4"
CLICK_CHOSE_OPPO_BATLE_4_4 = "chose oppo 4/4"

CLICK_CHOSE_OPPO_BATLE_1_5 = "chose oppo 1/5"
CLICK_CHOSE_OPPO_BATLE_2_5 = "chose oppo 2/5"
CLICK_CHOSE_OPPO_BATLE_3_5 = "chose oppo 3/5"
CLICK_CHOSE_OPPO_BATLE_4_5 = "chose oppo 4/5"
CLICK_CHOSE_OPPO_BATLE_5_5 = "chose oppo 5/5"

CLICK_CHOSE_OPPO_BATLE_1_6 = "chose oppo 1/6"
CLICK_CHOSE_OPPO_BATLE_2_6 = "chose oppo 2/6"
CLICK_CHOSE_OPPO_BATLE_3_6 = "chose oppo 3/6"
CLICK_CHOSE_OPPO_BATLE_4_6 = "chose oppo 4/6"
CLICK_CHOSE_OPPO_BATLE_5_6 = "chose oppo 5/6"
CLICK_CHOSE_OPPO_BATLE_6_6 = "chose oppo 6/6"

CLICK_CHOSE_OPPO_BATLE_1_7 = "chose oppo 1/7"
CLICK_CHOSE_OPPO_BATLE_2_7 = "chose oppo 2/7"
CLICK_CHOSE_OPPO_BATLE_3_7 = "chose oppo 3/7"
CLICK_CHOSE_OPPO_BATLE_4_7 = "chose oppo 4/7"
CLICK_CHOSE_OPPO_BATLE_5_7 = "chose oppo 5/7"
CLICK_CHOSE_OPPO_BATLE_6_7 = "chose oppo 6/7"
CLICK_CHOSE_OPPO_BATLE_7_7 = "chose oppo 7/7"



CLICK_CHOSE_OWN_x_PRE = "chose own "
CLICK_CHOSE_OWN_x_MID = "/"
CLICK_CHOSE_OWN_BATLE_0_0 = "chose own 0/0"

CLICK_CHOSE_OWN_BATLE_1_1 = "chose own 1/1"

CLICK_CHOSE_OWN_BATLE_1_2 = "chose own 1/2"
CLICK_CHOSE_OWN_BATLE_2_2 = "chose own 2/2"

CLICK_CHOSE_OWN_BATLE_1_3 = "chose own 1/3"
CLICK_CHOSE_OWN_BATLE_2_3 = "chose own 2/3"
CLICK_CHOSE_OWN_BATLE_3_3 = "chose own 3/3"

CLICK_CHOSE_OWN_BATLE_1_4 = "chose own 1/4"
CLICK_CHOSE_OWN_BATLE_2_4 = "chose own 2/4"
CLICK_CHOSE_OWN_BATLE_3_4 = "chose own 3/4"
CLICK_CHOSE_OWN_BATLE_4_4 = "chose own 4/4"

CLICK_CHOSE_OWN_BATLE_1_5 = "chose own 1/5"
CLICK_CHOSE_OWN_BATLE_2_5 = "chose own 2/5"
CLICK_CHOSE_OWN_BATLE_3_5 = "chose own 3/5"
CLICK_CHOSE_OWN_BATLE_4_5 = "chose own 4/5"
CLICK_CHOSE_OWN_BATLE_5_5 = "chose own 5/5"

CLICK_CHOSE_OWN_BATLE_1_6 = "chose own 1/6"
CLICK_CHOSE_OWN_BATLE_2_6 = "chose own 2/6"
CLICK_CHOSE_OWN_BATLE_3_6 = "chose own 3/6"
CLICK_CHOSE_OWN_BATLE_4_6 = "chose own 4/6"
CLICK_CHOSE_OWN_BATLE_5_6 = "chose own 5/6"
CLICK_CHOSE_OWN_BATLE_6_6 = "chose own 6/6"

CLICK_CHOSE_OWN_BATLE_1_7 = "chose own 1/7"
CLICK_CHOSE_OWN_BATLE_2_7 = "chose own 2/7"
CLICK_CHOSE_OWN_BATLE_3_7 = "chose own 3/7"
CLICK_CHOSE_OWN_BATLE_4_7 = "chose own 4/7"
CLICK_CHOSE_OWN_BATLE_5_7 = "chose own 5/7"
CLICK_CHOSE_OWN_BATLE_6_7 = "chose own 6/7"
CLICK_CHOSE_OWN_BATLE_7_7 = "chose own 7/7"