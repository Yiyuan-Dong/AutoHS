import random
import sys
import time

import keyboard

import FSM_action
import click
import get_screen

if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+q", sys.exit)
    FSM_action.AutoHS_automata()
