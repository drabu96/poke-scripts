from datetime import datetime

import pyautogui
import time

from PIL import Image


def print_with_time(string):
    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + string)


def is_on_screen(pic: Image):
    try:
        pyautogui.locateOnScreen(pic, confidence=.99)
    except pyautogui.ImageNotFoundException:
        return False
    return True


def press_key(key):
    pyautogui.keyDown(key)
    time.sleep(0.1)
    pyautogui.keyUp(key)
