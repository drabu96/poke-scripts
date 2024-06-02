import getopt
import sys
from datetime import datetime

from PIL import Image

from common import print_with_time, is_on_screen, press_key
from nds_scripts.nds_common import restart_game

import json
import time


def main(argv):
    config_file_path = ''
    keymap_file_path = ''
    keymap = None

    try:
        opts, args = getopt.getopt(argv, "hc:k:", ["config=", 'keymap='])
    except getopt.GetoptError:
        print('static_encounters_shiny.py -c <configfile> -k <keymapfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('static_encounters_shiny.py -c <configfile> -k <keymapfile>')
            sys.exit()
        elif opt in ("-c", "--config"):
            config_file_path = arg
        elif opt in ("-k", "--keymap"):
            keymap_file_path = arg
    print('Config file path is "', config_file_path)

    config = json.load(open(config_file_path))
    if keymap_file_path == '':
        keymap = json.load(open('default_keymap.json'))
    else:
        keymap = json.load(open(keymap_file_path))
    pokemon_name = config['pokemonName']
    regular_sprite = Image.open(config['regularSpritePath'])
    shiny_sprite = Image.open(config['shinySpritePath'])
    proof_battle_started = Image.open(config['proofBattleStartedPath'])

    def start_battle():
        print_with_time('Starting battle')
        press_key(keymap['BTN_A'])
        time.sleep(1)
        press_key(keymap['BTN_A'])
        time.sleep(.7)
        press_key(keymap['BTN_A'])
        time.sleep(.7)
        press_key(keymap['BTN_A'])

    def check_battle_started():
        for x in range(0, 10):
            if is_on_screen(proof_battle_started):
                return True
            time.sleep(.3)
        raise Exception('Error in battle starting')

    def check_shiny():
        regular = is_on_screen(regular_sprite)
        shiny = is_on_screen(shiny_sprite)
        if regular and not shiny:
            print_with_time('Found regular ' + pokemon_name)
            return False
        if shiny and not regular:
            print_with_time('Found shiny ' + pokemon_name + '!!! Congratulations!')
            return True
        raise Exception('Couldn\'t recognise pokemon')

    tries = 0
    begin_time = datetime.now()

    time.sleep(5)
    while True:
        tries += 1
        total_time = datetime.now() - begin_time
        print_with_time('Attempt count: ' + str(tries) + ', Total time: ' + str(total_time))
        restart_game(keymap)
        time.sleep(2)
        start_battle()
        time.sleep(3)
        check_battle_started()
        if check_shiny():
            print_with_time('Found shiny ' + pokemon_name + ' after ' + str(tries) + ' tries')
            break


if __name__ == "__main__":
    main(sys.argv[1:])
