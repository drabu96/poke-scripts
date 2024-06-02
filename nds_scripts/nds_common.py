import pyautogui

from common import print_with_time


def restart_game(keymap):
    print_with_time('Restarting game')
    keys = [keymap['BTN_L'], keymap['BTN_R'], keymap['BTN_SELECT'], keymap['BTN_START']]
    for key in keys:
        pyautogui.keyDown(key)
    for key in keys:
        pyautogui.keyUp(key)
