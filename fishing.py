from pyautogui import press, sleep, typewrite, screenshot as pyautogui_screenshot
from threading import Thread
from constants import coordinates, colors, sizes
import state
from re import findall
import logging
from ocr_utils import extract_text_from_roi
from fishing_modes import get_fishing_mode_params, get_save_on_fishes_count

logging.getLogger('easyocr').setLevel(logging.ERROR)

fishing_rod_slot = 'num8'
fishing_loops = 0
fishes_caught_postsave = 0
fishes_caught_presave = 0
max_possible_fishes = 0

def is_color_matching(screenshot, coord, color):
    return screenshot.getpixel(coord) == color

def check_fishing_arrow(screenshot, direction):
    try:
        resolution, _, _, _, _ = state.get_resolution()
        if is_color_matching(screenshot, coordinates[resolution]['white'], colors['white']):
            if is_color_matching(screenshot, coordinates[resolution][f'white_{direction}'], colors['white']):
                if is_color_matching(screenshot, coordinates[resolution][f'fishing_{direction}'], colors[f'fishing_{direction}']):   
                    global fishing_loops
                    if fishing_loops >= get_fishing_mode_params()['perfect_loops_max']:
                        fishing_loops = -1
                        sleep(1.5)
                    press_arrows_and_clear(direction)
                    return True
    except KeyError:
        return False

def press_arrows_and_clear(direction, debug=False):
    press(direction)
    if debug: print(f"{direction.capitalize()} arrow pressed.")

def check_and_press_fishing():
    _, x, y, width, height = state.get_resolution()
    screenshot = pyautogui_screenshot(region=(x, y, width, height))
    pressed = check_fishing_arrow(screenshot, 'down') or check_fishing_arrow(screenshot, 'up')    
    sleep(0.3)
    return pressed

def toggle_fishing():
    state.set_fishing_enabled(not state.get_fishing_enabled())
    toggle_fishing_loop()

def parse_numbers_from_text(text):
    digits = findall(r'\d+', text)
    combined_number = ''.join(digits)
    number = int(combined_number) if combined_number else 0
    return 0 if number > 100 else number

def click_fishing_rod():
    if state.is_warcraft_active():
        press(fishing_rod_slot)

def is_hotbar_slot_black():
    _, x, y, width, height = state.get_resolution()
    screenshot = pyautogui_screenshot(region=(x, y, width, height))
    try:
        resolution, _, _, _, _ = state.get_resolution()
        hotbar_slot_coord = coordinates[resolution]['hotbar_slot_1']
    except KeyError:
        return False
    black_color = (0, 0, 0)
    return is_color_matching(screenshot, hotbar_slot_coord, black_color)

def initialize_fishing_session():
    global fishes_caught_postsave, fishes_caught_presave, max_possible_fishes
    if state.get_fishes_caught_session() == -1:
        fishes_caught_postsave = 0
        fishes_caught_presave = 0
        max_possible_fishes = 0
        state.set_fishes_caught_session(0)

def handle_fishing_rod_click():
    click_fishing_rod()
    sleep(2)

def handle_fishing_score():
    global fishing_loops, max_possible_fishes, fishes_caught_presave
    score = 0
    while is_hotbar_slot_black():
        if score >= get_fishing_mode_params()['score_limit']:
            break
        if not state.is_warcraft_active():
            break
        pressed = check_and_press_fishing()
        if pressed:
            score += 500
    if score > 0:
        fishing_loops += 1
        max_possible_fishes += 3
        parsed_fishes_caught = get_fishes_count()
        fishes_caught_presave = parsed_fishes_caught if parsed_fishes_caught <= max_possible_fishes and parsed_fishes_caught >= fishes_caught_presave else fishes_caught_presave

def update_fishing_session_state():
    state.set_fishes_caught_session(fishes_caught_postsave + fishes_caught_presave)

def fishing_loop():
    initialize_fishing_session()
    while state.get_fishing_enabled():
        update_fishing_session_state()
        get_fishes_count()
        if not state.is_warcraft_active():
            continue
        handle_fishing_rod_click()
        handle_fishing_score()
        update_fishing_session_state()  # Update fishing count after finishing the loop
        sleep(1)

def toggle_fishing_loop():
    if state.get_fishing_enabled():
        Thread(target=fishing_loop, daemon=True).start()

def get_fish_count(i):
    try:
        resolution, _, _, _, _ = state.get_resolution()
        fish_x, fish_y = coordinates[resolution][i]
        fish_number_width = sizes[resolution]['fish_number_width']
        fish_number_height = sizes[resolution]['fish_number_height']
    except KeyError:
        return 0
    text = extract_text_from_roi(fish_x, fish_y, fish_number_width, fish_number_height, state.get_resolution())
    return parse_numbers_from_text(text)

def get_fishes_count():
    global max_possible_fishes, fishes_caught_postsave, fishes_caught_presave
    fishes_count = 0
    for i in ['fish_1', 'fish_2']:
        fish_count = get_fish_count(i)
        if fish_count > fishes_count:
            fishes_count = fish_count
    save_on_fishes_count = get_save_on_fishes_count()
    if save_on_fishes_count is not None and fishes_count >= save_on_fishes_count:
        max_possible_fishes = 0
        fishes_caught_postsave += save_on_fishes_count
        fishes_caught_presave = 0
        do_save()
    return fishes_count

def do_save():
    press('enter')
    typewrite('-s')
    press('enter')