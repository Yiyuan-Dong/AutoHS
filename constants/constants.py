# 你的Power.log的路径, 应该在你的炉石安装目录下的`Logs/`文件夹中, 这里放的是我的路径
# ** 一定要修改成自己电脑上的路径 **
HEARTHSTONE_POWER_LOG_PATH = "D:/战网/Hearthstone/Logs/Power.log"

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
FSM_QUITTING_BATTLE = "QUITTING BATTLE"

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
