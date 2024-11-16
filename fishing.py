from PIL import ImageOps, ImageEnhance
from pytesseract import image_to_string
from pyautogui import press, sleep, typewrite, screenshot as pyautogui_screenshot
from threading import Thread
from pygetwindow import getActiveWindow
from constants import coordinates, colors
import state
from pygetwindow import getActiveWindow
from re import findall

fishes_items_coordinates = {
    'fish_1': (1161, 938),
    'fish_2': (1161, 997),
}

fish_number_width = 22
fish_number_height = 14

fishing_rod_slot = 'num8'
fishing_loops = 0
perfect_loops_max = 2
save_on_fishes_count = 48
fishes_caught_postsave = 0
fishes_caught_presave = 0
max_possible_fishes = 0

def is_color_matching(screenshot, coord, color):
    return screenshot.getpixel(coord) == color

def check_fishing_arrow(screenshot, direction):
    if is_color_matching(screenshot, coordinates['white'], colors['white']):
        if is_color_matching(screenshot, coordinates[f'white_{direction}'], colors['white']):
            if is_color_matching(screenshot, coordinates[f'fishing_{direction}'], colors[f'fishing_{direction}']):   
                global fishing_loops
                if fishing_loops >= perfect_loops_max:
                    fishing_loops = -1
                    sleep(1.5)
                press_arrows_and_clear(direction)

def press_arrows_and_clear(direction, debug=False):
    press(direction)
    if debug: print(f"{direction.capitalize()} arrow pressed.")

def check_and_press_fishing():
    screenshot = pyautogui_screenshot()
    check_fishing_arrow(screenshot, 'down')
    check_fishing_arrow(screenshot, 'up')
    sleep(0.3)

def toggle_fishing():
    state.set_fishing_enabled(not state.get_fishing_enabled())
    toggle_fishing_loop()

def extract_text_from_roi(x, y, width, height, i):
    screenshot = pyautogui_screenshot(region=(x, y, width, height))
    processed_image = screenshot.point(lambda p: 255 if p > 160 else 0)
    gray_image = ImageOps.grayscale(processed_image)
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2)
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    text = image_to_string(enhanced_image, config=custom_config)
    return text

def parse_numbers_from_text(text):
    digits = findall(r'\d+', text)
    combined_number = ''.join(digits)
    number = int(combined_number) if combined_number else 0
    return 0 if number > 100 else number

def click_fishing_rod():
    if is_warcraft_active():
        press(fishing_rod_slot)

def is_hotbar_slot_black():
    screenshot = pyautogui_screenshot()
    hotbar_slot_coord = (1331, 896)
    black_color = (0, 0, 0)
    return is_color_matching(screenshot, hotbar_slot_coord, black_color)

def fishing_loop():
    global fishing_loops, fishes_caught_postsave, fishes_caught_presave, max_possible_fishes
    if state.get_fishes_caught_session() == -1:
        fishes_caught_postsave = 0
        fishes_caught_presave = 0
        max_possible_fishes = 0
        state.set_fishes_caught_session(0)

    while state.get_fishing_enabled():
        state.set_fishes_caught_session(fishes_caught_postsave + fishes_caught_presave)
        fishing = False
        get_fishes_count()
        if not is_warcraft_active():
            continue
        click_fishing_rod()
        sleep(2)
        while is_hotbar_slot_black():
            if not is_warcraft_active():
                break
            fishing = True
            check_and_press_fishing()
        if fishing:
            fishing_loops += 1
            max_possible_fishes += 3
            parsed_fishes_caught = get_fishes_count()
            fishes_caught_presave = parsed_fishes_caught if parsed_fishes_caught <= max_possible_fishes and parsed_fishes_caught >= fishes_caught_presave else fishes_caught_presave
        sleep(1)

def toggle_fishing_loop():
    if state.get_fishing_enabled():
        Thread(target=fishing_loop, daemon=True).start()

def is_warcraft_active():
    active_window = getActiveWindow()
    return active_window and "Warcraft III" in active_window.title

def get_fish_count(i):
    x, y = fishes_items_coordinates[i]
    text = extract_text_from_roi(x, y, fish_number_width, fish_number_height, i)
    return parse_numbers_from_text(text)

def get_fishes_count():
    global max_possible_fishes, fishes_caught_postsave, fishes_caught_presave
    fishes_count = 0
    for i in fishes_items_coordinates:
        fish_count = get_fish_count(i)
        if fish_count > fishes_count:
            fishes_count = fish_count
    if fishes_count >= save_on_fishes_count:
        max_possible_fishes = 0
        fishes_caught_postsave += save_on_fishes_count
        fishes_caught_presave = 0
        do_save()
    return fishes_count

def do_save():
    press('enter')
    typewrite('-s')
    press('enter')