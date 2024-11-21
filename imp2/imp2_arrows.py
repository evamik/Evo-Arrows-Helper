from pyautogui import press, screenshot, sleep
from utils.constants import coordinates, colors, sizes, opposite_directions
from utils.state import set_imp2_enabled, get_imp2_enabled, get_resolution

def is_color_matching(screenshot_img, coord, color):
    return screenshot_img.getpixel(coord) == color

def check_arrow(screenshot_img, direction):
    resolution, _, _, _, _ = get_resolution()
    imp2_arrows_height = sizes[resolution]['imp2_arrows_height']
    
    def check_line(y_offset):
        return all(is_color_matching(screenshot_img, (coordinates[resolution][f'{direction}_yellow_{i}'][0], coordinates[resolution][f'{direction}_yellow_{i}'][1] + y_offset), colors['yellow']) for i in range(1, 5))
    
    if is_color_matching(screenshot_img, coordinates[resolution]['red'], colors['red']):
        if check_line(0) or check_line(imp2_arrows_height) or check_line(2 * imp2_arrows_height):
            press_arrows_and_clear(direction)

def press_arrows_and_clear(direction, clear=True):
    press(direction)
    
    opposite_direction = opposite_directions[direction]
    sleep(0.1)
    press(opposite_direction)
    
    if clear:
        sleep(0.1)
        press('esc')

def check_and_press_imp2():
    screenshot_img = screenshot()
    check_arrow(screenshot_img, 'down')
    check_arrow(screenshot_img, 'up')
    check_arrow(screenshot_img, 'left')
    check_arrow(screenshot_img, 'right')
    sleep(0.5)

def toggle_imp2():
    set_imp2_enabled(not get_imp2_enabled())