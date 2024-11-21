from imp2.imp2_arrows import check_and_press_imp2
from overlay.controls import get_current_menu, set_hotkeys
from overlay.overlay import run_overlay
from utils import state
from threading import Thread
from fishing.fishing import handle_respawn, is_character_alive
import pyautogui

pyautogui.FAILSAFE = False

if __name__ == "__main__":
    set_hotkeys(get_current_menu())

    overlay_thread = Thread(target=run_overlay, daemon=True)
    overlay_thread.start()

    print("Evo Arrows Helper started!")
    print("**Keep this window open and enjoy overlay in Warcraft III**")
    
    while True:
        if state.is_warcraft_active():
            if state.get_imp2_enabled():
                check_and_press_imp2()
            if state.get_fishing_enabled() and not is_character_alive():
                handle_respawn()