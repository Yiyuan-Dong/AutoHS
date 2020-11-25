import random
import click
import time
import get_screen

STRING_CHOOSINGHERO = "ChoosingHero"
STRING_MATCHING = "Matching"
STRING_CHOOSINGCARD = "ChoosingCard"
STRING_NOTMINE = "NotMine"
STRING_MYTURN = "MyTurn"
# STRING_UNCERTAIN = "Uncertain"

FRONT_ROPING_TIME = 2
BACK_ROPING_TIME = 2
STATE_CHECK_INTERVAL = 3
EMOJ_RATE = 0.2
IF_LOGOUT = 1

state = ""
turn_num = 0


def log_out():
    global state
    global turn_num
    if IF_LOGOUT:
        print("Entering " + state)
    if state == STRING_MYTURN:
        print("It is turn " + str(turn_num))
    if state == STRING_CHOOSINGCARD:
        print("Please wait 18 secs")
    return


def ChoosingHeroAction():
    log_out()
    click.math_opponent()
    time.sleep(1)
    return STRING_MATCHING


def MatchingAction():
    log_out()
    while get_screen.get_state() == STRING_MATCHING:
        time.sleep(STATE_CHECK_INTERVAL)
    return STRING_CHOOSINGCARD


def ChoosingCardAction():
    log_out()
    time.sleep(18)  # 18是一个经验数值...
    click.choose_card()
    time.sleep(STATE_CHECK_INTERVAL)
    return STRING_NOTMINE


def NotMineAction():
    log_out()
    global state
    while 1:
        click.flush_uncertain()
        time.sleep(STATE_CHECK_INTERVAL)
        state = get_screen.get_state()
        if state == STRING_NOTMINE:
            continue
        else:
            return state


def MyTurnAction():
    global turn_num
    turn_num += 1
    log_out()
    time.sleep(FRONT_ROPING_TIME)
    if_emoj = random.random()
    if if_emoj < EMOJ_RATE:
        click.emoj()
    if turn_num == 1:
        click.use_task()
        click.emoj()
        click.end_turn()
        return STRING_NOTMINE
    if turn_num >= 8:
        click.use_skill()
    click.use_card()
    # click.minion_attack()
    click.use_skill()
    click.hero_atrack()
    time.sleep(BACK_ROPING_TIME)
    click.end_turn()

    return STRING_NOTMINE


# def UncertainAction():
#     log_out()
#     time.sleep(STATE_CHECK_INTERVAL)
#     click.flush_uncertain()
#     return ""


def show_time(time_last):
    print("Now the time is " +
          time.strftime("%m-%d %H:%M:%S", time.localtime()))
    time_now = time.time()
    if time_last > 0:
        print("The last game last for : {} mins {} secs"
              .format((time_now - time_last) // 60,
                      int(time_now - time_last) % 60))
    return time.time()


def AutoHS_automata():
    global state
    global turn_num
    time_snap = 0.0
    game_count = 1
    while 1:
        if state == "":
            state = get_screen.get_state()

        if state == STRING_MATCHING:
            print("The " + str(game_count) + " game begins")
            turn_num = 0
            time_snap = show_time(time_snap)

        state = eval(state + "Action")()
