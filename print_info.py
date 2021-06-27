from constants.constants import *


def warning_print(info_str):
    if WARNING:
        print("[WARNING] " + info_str)


def debug_print(info_str):
    if DEBUG:
        print("[DEBUG] " + info_str)
