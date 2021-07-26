from constants.constants import *


def error_print(error_str):
    if ERROR_PRINT:
        print("[ERROR] " + error_str)


def warning_print(warning_str):
    if WARNING_PRINT:
        print("[WARNING] " + warning_str)


def debug_print(debug_str=""):
    if DEBUG_PRINT:
        print("[DEBUG] " + debug_str)


def sys_print(sys_str):
    if SYS_PRINT:
        print("[SYS] " + sys_str)


def info_print(info_str):
    if INFO_PRINT:
        print("[INFO] " + info_str)
