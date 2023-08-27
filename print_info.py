from constants.constants import *
import os
import time

error_file_handle = None
warn_file_handle = None
debug_file_handle = None
sys_file_handle = None
info_file_handle = None


def print_info_init():
    global error_file_handle
    global warn_file_handle
    global debug_file_handle
    global sys_file_handle
    global info_file_handle

    if not os.path.exists("./log/"):
        os.mkdir("./log/")

    error_file_handle = open("./log/error_log.txt", "w", encoding="utf8")
    warn_file_handle = open("./log/warn_log.txt", "w", encoding="utf8")
    debug_file_handle = open("./log/debug_log.txt", "w", encoding="utf8")
    sys_file_handle = open("./log/sys_log.txt", "w", encoding="utf8")
    info_file_handle = open("./log/info_log.txt", "w", encoding="utf8")


def print_info_close():
    global error_file_handle
    global warn_file_handle
    global debug_file_handle
    global sys_file_handle
    global info_file_handle

    error_file_handle.close()
    error_file_handle = None
    warn_file_handle.close()
    warn_file_handle = None
    debug_file_handle.close()
    debug_file_handle = None
    sys_file_handle.close()
    sys_file_handle = None
    info_file_handle.close()
    info_file_handle = None

def current_time():
    return time.strftime("%H:%M:%S", time.localtime())

def error_print(error_str):
    error_str = f"[{current_time()} ERROR] {error_str}"

    if ERROR_PRINT:
        print(error_str)
    if ERROR_FILE_WRITE and error_file_handle:
        error_file_handle.write(error_str + "\n")


def warn_print(warn_str):
    warn_str = f"[{current_time()} WARN] {warn_str}"

    if WARN_PRINT:
        print(warn_str)
    if WARN_FILE_WRITE and warn_file_handle:
        warn_file_handle.write(warn_str+ "\n")


def debug_print(debug_str=""):
    debug_str = f"[{current_time()} DEBUG] {debug_str}"

    if DEBUG_PRINT:
        print(debug_str)
    if DEBUG_FILE_WRITE and debug_file_handle:
        debug_file_handle.write(debug_str + "\n")
        debug_file_handle.flush()


def sys_print(sys_str):
    sys_str = f"[{current_time()} SYS] {sys_str}"

    if SYS_PRINT:
        print(sys_str)
    if SYS_FILE_WRITE and sys_file_handle:
        sys_file_handle.write(sys_str + "\n")


def info_print(info_str):
    info_str = f"[{current_time()} INFO] {info_str}"

    if INFO_PRINT:
        print(info_str)
    if INFO_FILE_WRITE and info_file_handle:
        info_file_handle.write(info_str + "\n")
