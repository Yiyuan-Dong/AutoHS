#TODO: 这个文件不应存在，要么是常量，要么用GUI配置


# 每个回合开始发个表情的概率
EMOJ_RATIO = 0.05

# 随从相互攻击的启发值包括两个部分：敌方随从受伤的带来的收益；
# 以及我方随从受伤带来的损失。下面两个比例表示这两个启发值变化
# 数值应该以怎样权值比例相加。如果是控制卡组，可以略微调高
# OPPO_DELTA_H_FACTOR 来鼓励解场
OPPO_DELTA_H_FACTOR = 1.2
MY_DELTA_H_FACTOR = 1

# 对于没有单独建一个类去描述的卡牌, 如果它的法力值花费大于这个值,
# 就在留牌阶段被换掉
REPLACE_COST_BAR = 3

OPERATE_INTERVAL = 0.2
STATE_CHECK_INTERVAL = 1
TINY_OPERATE_INTERVAL = 0.1
BASIC_MINION_PUT_INTERVAL = 0.8
BASIC_SPELL_WAIT_TIME = 1.5
BASIC_WEAPON_WAIT_TIME = 1