import random
import click
import time
import get_screen

FRONT_ROPING_TIME = 3
BACK_ROPING_TIME = 5
EMOJ_RATE = 0.2
game_count = 0


def ChoosingHeroAction():
    print("Entering Choosing Hero")
    click.math_opponent()
    time.sleep(1)
    MatchingAction()


def MatchingAction():
    print("Entering matching")
    while get_screen.get_state() == "Matching":
        time.sleep(5)
    ChoosingCardAction()


def ChoosingCardAction():
    time.sleep(18)
    print("Entering choosing card")
    click.choose_card()
    time.sleep(5)
    NotMineAction()


def NotMineAction():
    print("Entering not mine")
    state = ""
    while 1:
        time.sleep(3)
        state = get_screen.get_state()
        if state == "NotMine":
            continue
        if state == "MyTurn":
            MyTurnAction()
            break
        else:
            UncertainAction()
            break


def MyTurnAction():
    print("Entering my turn")
    time.sleep(FRONT_ROPING_TIME)
    state = ""
    if_emoj = random.random()
    if if_emoj < EMOJ_RATE:
        click.emoj()

    click.use_skill()
    click.use_card()
    click.minion_attack()
    click.use_skill()
    click.hero_atrack()
    click.end_turn()
    # time.sleep(BACK_ROPING_TIME)
    NotMineAction()


def UncertainAction():
    print("Entering uncertain")
    time.sleep(3)
    click.flush_uncertain()
