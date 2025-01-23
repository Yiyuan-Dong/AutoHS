"""
主体代码引自 Demon_Hunter 的CSDN博客, 博客URL:https://blog.csdn.net/zhuisui_woxin/article/details/84345036
"""

import win32gui
import win32ui
import win32con
import win32com.client
import win32api
import win32process
import numpy
import cv2
import time
from autohs_logger import *
from constants.state_and_key import *
from constants.pixel_coordinate import *
from skimage.metrics import structural_similarity as ssim

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
figs_dir_path = os.path.join(current_dir_path, "figs")

choose_card_img = cv2.imread(os.path.join(figs_dir_path, "choose_card.png"))
choose_hero_img = cv2.imread(os.path.join(figs_dir_path, "choose_hero.png"))
print(os.path.join(figs_dir_path, "choose_hero.png"))
matching_img = cv2.imread(os.path.join(figs_dir_path, "matching.png"))
main_menu_img = cv2.imread(os.path.join(figs_dir_path, "main_menu.png"))

def get_HS_hwnd():
    hwnd = win32gui.FindWindow(None, "炉石传说")
    if hwnd != 0:
        return hwnd

    hwnd = win32gui.FindWindow(None, "《爐石戰記》")
    if hwnd != 0:
        return hwnd

    hwnd = win32gui.FindWindow(None, "Hearthstone")
    return hwnd


def get_battlenet_hwnd():
    hwnd = win32gui.FindWindow(None, "战网")
    if hwnd != 0:
        return hwnd

    hwnd = win32gui.FindWindow(None, "Battle.net")
    return hwnd


def test_hs_available():
    return get_HS_hwnd() != 0

def test_battlenet_available():
    return get_battlenet_hwnd() != 0

def move_window_foreground(hwnd, name=""):
    try:
        win32gui.BringWindowToTop(hwnd)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        if name != "":
            logger.warning(f"Open {name}: {e}")
        else:
            logger.warning(e)

    win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)


def max_diff(img, pixel_list):
    ans = 0
    for pair in pixel_list:
        diff = abs(int(img[pair[0]][pair[1]][1]) -
                   int(img[pair[0]][pair[1]][0]))
        ans = max(ans, diff)
        # print(img[pair[0]][pair[1]])

    return ans

# This function used to take the snapshot of a specific process,
# but I found it does not work well now. So now it just take the
# snapshot of the frontend window.
def take_snapshot():
    width = WIDTH
    height = HEIGHT

    # Get the snapshot of the desktop
    hwnd = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    signedIntsArray = saveBitMap.GetBitmapBits(True)

    # Release the resources
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    im_opencv = numpy.frombuffer(signedIntsArray, dtype='uint8')
    im_opencv.shape = (height, width, 4)

    # Create a writable copy of the array
    im_opencv = im_opencv.copy()

    return im_opencv


def wait_battlefield_stable(autohs_config, wait_count = 3, max_try = 40):
    last_battlefield_snapshot = None
    stable_count = 0
    start_time = 0
    end_time = 0

    for i in range(max_try):
        im_opencv = take_snapshot()
        if im_opencv.shape[2] == 4:
            im_opencv = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2BGR)

        start_x = autohs_config.click_coordinates[COORDINATE_BATTLEFILED_RANGE_X][0]
        end_x = autohs_config.click_coordinates[COORDINATE_BATTLEFILED_RANGE_X][1]
        start_y = autohs_config.click_coordinates[COORDINATE_BATTLEFILED_RANGE_Y][0]
        end_y = autohs_config.click_coordinates[COORDINATE_BATTLEFILED_RANGE_Y][1]
        curr_battlefield_snapshot = im_opencv[start_y:end_y, start_x:end_x]
        # simm计算比较慢，所以压缩一下
        curr_battlefield_snapshot = cv2.resize(curr_battlefield_snapshot, ((end_x - start_x) // 2, (end_y - start_y) // 2))

        if last_battlefield_snapshot is not None:
            start_time = time.time()
            simm = ssim(curr_battlefield_snapshot, last_battlefield_snapshot, multichannel=True, channel_axis = 2)
            end_time = time.time()
            logger.debug(f"Similarity: {simm}")
            if simm > 0.95:
                stable_count += 1
                if stable_count >= wait_count:
                    return
            else:
                stable_count = 0

        last_battlefield_snapshot = curr_battlefield_snapshot
        if end_time - start_time < 0.3:
            time.sleep(0.3 - (end_time - start_time))

    logger.warning("等待战场稳定超时")

def get_state():
    hwnd = get_HS_hwnd()
    if hwnd == 0:
        return FSM_LEAVE_HS

    im_opencv = take_snapshot()
    if im_opencv.shape[2] == 4:
        im_opencv = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2BGR)

    # if WIDTH == 2560:
    curr_main_menu_part = im_opencv[300:900,980:1580]
    curr_choose_hero_part = im_opencv[1040:1340, 1710:2010]
    curr_matching_part = im_opencv[400:1000, 980:1580]
    curr_choose_card_part = im_opencv[170:250, 1130:1430]

    simm_main_menu = ssim(curr_main_menu_part, main_menu_img, multichannel=True, channel_axis = 2)
    simm_choose_hero = ssim(curr_choose_hero_part, choose_hero_img, multichannel=True, channel_axis = 2)
    simm_matching = ssim(curr_matching_part, matching_img, multichannel=True, channel_axis = 2)
    simm_choose_card = ssim(curr_choose_card_part, choose_card_img, multichannel=True, channel_axis = 2)

    logger.debug(f"Similarity: main_menu: {simm_main_menu}, choose_hero: {simm_choose_hero}, matching: {simm_matching}, choose_card: {simm_choose_card}")

    if simm_main_menu > 0.83:
        return FSM_MAIN_MENU
    elif simm_choose_hero > 0.9:
        return FSM_CHOOSING_HERO
    elif simm_matching > 0.75:
        return FSM_MATCHING_OPPONENT
    elif simm_choose_card > 0.9:
        return FSM_CHOOSING_CARD
    else:
        return FSM_BATTLING

def terminate_HS():
    hwnd = get_HS_hwnd()
    if hwnd == 0:
        return
    _, process_id = win32process.GetWindowThreadProcessId(hwnd)
    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, process_id)
    win32api.TerminateProcess(handle, 0)
    win32api.CloseHandle(handle)
