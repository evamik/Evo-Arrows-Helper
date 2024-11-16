from tkinter import Tk, Label
from ctypes import windll
import state
from pygetwindow import getActiveWindow

overlay_params = {
    'x': 100,
    'y': 50,
    'width': 450,
    'height': 150,
}

fish_cost = 185800
shard_cost = 40000

def is_warcraft_active():
    active_window = getActiveWindow()
    return active_window and "Warcraft III" in active_window.title

def update_overlay(label, root):
    if is_warcraft_active():
        root.deiconify()
        status = f"Fishing: {'Enabled' if state.get_fishing_enabled() else 'Disabled'} (Ctrl+F1)\n"
        status += f"Imp2 Arrows: {'Enabled' if state.get_imp2_enabled() else 'Disabled'} (Ctrl+F2)\n"
        status += f"Fishes caught: {state.get_fishes_caught_session()} (~{calculate_estimated_profit()} shards) (Reset: Ctrl+F3)\n"
        label.config(text=status)
    else:
        root.withdraw()
    label.after(500, update_overlay, label, root)

def create_overlay():
    root = Tk()
    root.title("Overlay")
    root.geometry(f"{overlay_params['width']}x{overlay_params['height']}+{overlay_params['x']}+{overlay_params['y']}")
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.7)
    root.configure(bg='black')

    label = Label(root, text="", font=("Helvetica", 16), bg='black', fg='white', anchor='w', justify='left')
    label.pack(pady=20, fill='both', expand=True)

    root.wm_attributes("-transparentcolor", 'black')
    root.overrideredirect(True)

    hwnd = windll.user32.GetParent(root.winfo_id())
    styles = windll.user32.GetWindowLongPtrW(hwnd, -20)
    windll.user32.SetWindowLongPtrW(hwnd, -20, styles | 0x80000 | 0x20)
    windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0020)

    return root, label

def run_overlay():
    root, label = create_overlay()
    update_overlay(label, root)
    root.mainloop()

def calculate_estimated_profit():
    return int(state.get_fishes_caught_session() * fish_cost / shard_cost)