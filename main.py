import get_screen
import click
import time
import random
import FSM_action
import keyboard
import sys

if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+alt+q", sys.exit)
    while 1:
        eval("FSM_action." + get_screen.get_state() + "Action")()
