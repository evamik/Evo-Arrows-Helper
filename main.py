from imp2_arrows import check_and_press_imp2
from controls import get_current_menu, set_hotkeys
from overlay import run_overlay
import state
from threading import Thread

if __name__ == "__main__":
    set_hotkeys(get_current_menu())

    overlay_thread = Thread(target=run_overlay, daemon=True)
    overlay_thread.start()

    print("Evo Arrows Helper started!")
    
    while True:
        if state.is_warcraft_active():
            if state.get_imp2_enabled():
                check_and_press_imp2()