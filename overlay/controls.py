from fishing.fishing import toggle_fishing, set_respawn_point, get_respawn_point
from imp2.imp2_arrows import toggle_imp2
from utils import state
from fishing.fishing_modes import set_fishing_mode, get_fishing_mode, set_save_on_fishes_count, get_save_on_fishes_count
from keyboard import unhook_all_hotkeys, add_hotkey

# Define the main menu and submenus
controls = {
    'main_menu': {
        'ctrl+f1': 'fishing_menu',
        'ctrl+f2': 'imp2_menu',
    },
    'fishing_menu': {
        'ctrl+f1': toggle_fishing,
        'ctrl+f2': 'main_menu',  # Go back to main menu
        'ctrl+f3': state.set_fishes_caught_session,
        'ctrl+f4': set_fishing_mode,  # Toggle fishing mode
        'ctrl+f5': set_save_on_fishes_count,  # Toggle save on fishes count
        'ctrl+f6': set_respawn_point,  # Set respawn point
    },
    'imp2_menu': {
        'ctrl+f1': toggle_imp2,
        'ctrl+f2': 'main_menu',  # Go back to main menu
    }
}

# Custom names for actions
custom_names = {
    'toggle_fishing': lambda: f"Toggle Fishing (Enabled)" if state.get_fishing_enabled() else "Toggle Fishing (Disabled)",
    'toggle_imp2': lambda: f"Toggle Imp2 (Enabled)" if state.get_imp2_enabled() else "Toggle Imp2 (Disabled)",
    'set_fishes_caught_session': lambda: "Reset Fishes Caught Session",
    'set_fishing_mode': lambda: f"Set Fishing Mode: {get_fishing_mode()}",
    'set_save_on_fishes_count': lambda: f"Set Save on Fishes Count: {get_save_on_fishes_count() if get_save_on_fishes_count() is not None else 'Disabled'}",
    'set_respawn_point': lambda: f"Set Respawn Point ({get_respawn_point()})" if get_respawn_point() else "Set Respawn Point",
    'fishing_menu': lambda: "Fishing Menu",
    'imp2_menu': lambda: "Imp2 Menu",
    'main_menu': lambda: "Main Menu"
}

# Current menu state
_current_menu = 'main_menu'

def get_current_menu():
    return _current_menu

def set_current_menu(menu):
    global _current_menu
    _current_menu = menu

def set_hotkeys(menu):
    try:
        unhook_all_hotkeys()
    except AttributeError:
        pass
    if menu in controls:
        for hotkey, action in controls[menu].items():
            if isinstance(action, str):
                add_hotkey(hotkey, lambda action=action: navigate_to(action))
            else:
                add_hotkey(hotkey, action)

def navigate_to(menu):
    set_current_menu(menu)
    set_hotkeys(menu)