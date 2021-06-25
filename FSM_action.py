import random
import click
import time
import get_screen
import sys
import cv2

STRING_CHOOSINGHERO = "ChoosingHero"
STRING_MATCHING = "Matching"
STRING_CHOOSINGCARD = "ChoosingCard"
STRING_NOTMYTURN = "NotMyTurn"
STRING_MYTURN = "MyTurn"
# STRING_UNCERTAIN = "Uncertain"
STRING_LEAVEHS = "LeaveHS"

FRONT_ROPING_TIME = 3
BACK_ROPING_TIME = 2
STATE_CHECK_INTERVAL = 3
EMOJ_RATE = 0.2
IF_LOGOUT = 1

state = ""
turn_num = 0
time_snap = 0.0
game_count = 1


def log_out():
    global state
    global turn_num
    global time_snap
    global game_count

    if IF_LOGOUT:
        print("  Entering " + state)
        if state == STRING_MYTURN:
            print("    It is turn " + str(turn_num))

    if state == STRING_LEAVEHS:
        print("Wow, What happened?")
        show_time(0.0)
        print("Try to go back to HS")
        print()

    if state == STRING_MATCHING:
        print("The " + str(game_count) + " game begins")
        game_count += 1
        turn_num = 0
        time_snap = show_time(time_snap)
        print()

    return


def ChoosingHeroAction():
    log_out()
    click.match_opponent()
    time.sleep(1)
    return STRING_MATCHING


def MatchingAction():
    log_out()
    local_state = STRING_MATCHING
    while local_state == STRING_MATCHING:
        time.sleep(STATE_CHECK_INTERVAL)
        local_state = get_screen.get_state()
    time.sleep(18)  # 18是一个经验数值...
    return STRING_CHOOSINGCARD


def ChoosingCardAction():
    log_out()
    click.choose_card()
    time.sleep(STATE_CHECK_INTERVAL)
    return STRING_NOTMYTURN


def NotMineAction():
    log_out()
    global state
    while 1:
        click.flush_uncertain()
        time.sleep(STATE_CHECK_INTERVAL)
        state = get_screen.get_state()
        if state == STRING_NOTMYTURN:
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
        return STRING_NOTMYTURN
    if turn_num >= 10:
        click.use_skill()
    click.use_card()
    click.minion_attack()
    click.use_skill()
    click.hero_atrack()
    time.sleep(BACK_ROPING_TIME)
    click.end_turn()
    time.sleep(STATE_CHECK_INTERVAL)

    return STRING_NOTMYTURN


# def UncertainAction():
#     log_out()
#     time.sleep(STATE_CHECK_INTERVAL)
#     click.flush_uncertain()
#     return ""

def LeaveHSAction():
    log_out()
    global state
    while state == STRING_LEAVEHS:
        click.enter_HS()
        time.sleep(15)
        state = get_screen.get_state()
    while state != STRING_CHOOSINGHERO:
        click.enter_battle_mode()
        time.sleep(10)
        state = get_screen.get_state()
    return state


def show_time(time_last):
    print("Now the time is " +
          time.strftime("%m-%d %H:%M:%S", time.localtime()))
    time_now = time.time()
    if time_last > 0:
        print("The last game last for : {} mins {} secs"
              .format(int((time_now - time_last) // 60),
                      int(time_now - time_last) % 60))
    return time.time()


def AutoHS_automata():
    global state
    global turn_num

    def increase():
        i = 0
        while True:
            yield i
            i += 1

    i = increase()

    while 1:
        if state == "":
            state = get_screen.get_state()
        cv2.imwrite("./img/" + state + "/" +
                    time.strftime("%m_%d_%H_%M_%S", time.localtime()) + ".jpg"
                    , get_screen.catch_screen())
        state = eval(state + "Action")()
