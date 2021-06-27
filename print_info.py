from constants.constants import *


def warning_print(info_str):
    if WARNING:
        print("[WARNING] " + info_str)


def debug_print(info_str):
    if DEBUG:
        print("[DEBUG] " + info_str)


def sys_print(sys_str):
    if SYS:
        print("[SYS] " + sys_str)


def info_print(info_str):
    if INFO:
        print("[INFO] " + info_str)
