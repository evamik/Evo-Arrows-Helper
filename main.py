from pygetwindow import getActiveWindow
from keyboard import add_hotkey
from threading import Thread
from fishing import toggle_fishing
from imp2_arrows import check_and_press_imp2, toggle_imp2
from overlay import run_overlay
import state

def is_warcraft_active():
    active_window = getActiveWindow()
    return active_window and "Warcraft III" in active_window.title

if __name__ == "__main__":    
    add_hotkey('ctrl+f1', toggle_fishing)
    add_hotkey('ctrl+f2', toggle_imp2)
    add_hotkey('ctrl+f3', state.set_fishes_caught_session, args=[-1])

    # Run the overlay in a separate thread
    overlay_thread = Thread(target=run_overlay, daemon=True)
    overlay_thread.start()
    
    while True:
        if is_warcraft_active():
            if state.get_imp2_enabled():
                check_and_press_imp2()