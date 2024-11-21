from pygetwindow import getActiveWindow
import win32.win32gui as win32gui

_fishing_enabled = False
_imp2_enabled = False
_fishes_caught_session = 0
_resolution = ""
_x = 0
_y = 0
_width = 0
_height = 0

def get_fishing_enabled():
    return _fishing_enabled

def set_fishing_enabled(value):
    global _fishing_enabled
    _fishing_enabled = value

def get_imp2_enabled():
    return _imp2_enabled

def set_imp2_enabled(value):
    global _imp2_enabled
    _imp2_enabled = value

def get_fishes_caught_session():
    return _fishes_caught_session

def set_fishes_caught_session(value):
    global _fishes_caught_session
    _fishes_caught_session = value

def is_warcraft_active():
    active_window = getActiveWindow()
    is_active = active_window and "Warcraft III" in active_window.title
    if is_active:
        global _resolution, _x, _y, _width, _height
        _resolution, _x, _y, _width, _height = get_resolution()
    else:
        _width = 0
    return is_active

def get_resolution():
    global _resolution, _x, _y, _width, _height
    if _width != 0:
        return _resolution, _x, _y, _width, _height
    active_window = getActiveWindow()
    hwnd = active_window._hWnd
    rect = win32gui.GetClientRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    x, y = win32gui.ClientToScreen(hwnd, (0, 0))
    _x, _y, _width, _height = x, y, width, height
    _resolution = f"{width}x{height}"
    return _resolution, x, y, width, height