from tkinter import Tk, Label, font as tkFont
from ctypes import windll
import state
from controls import controls, get_current_menu, custom_names

overlay_params = {
    'x': 100,
    'y': 50,
    'width': 450,
    'height': 200,
}

fish_cost = 185800
shard_cost = 40000

def calculate_estimated_profit():
    return int(state.get_fishes_caught_session() * fish_cost / shard_cost)

def update_overlay(label, root):
    if state.is_warcraft_active():
        root.deiconify()
        
        status = f"Current Menu: {custom_names[get_current_menu()]()}\n"
        for hotkey, action in controls[get_current_menu()].items():
            if isinstance(action, str):
                status += f"{hotkey}: Navigate to {custom_names[action]()}\n"
            else:
                action_name = action.__name__
                status += f"{hotkey}: {custom_names.get(action_name, lambda: action_name)()}\n"
        if get_current_menu() == 'fishing_menu':
            status += f"Fishes caught: {state.get_fishes_caught_session()} (~{calculate_estimated_profit()} shards)\n"
        label.config(text=status)
        
        # Calculate the required size for the overlay
        text_font = tkFont.Font(font=label.cget("font"))
        text_width = text_font.measure(status)
        text_height = text_font.metrics("linespace") * (status.count('\n') + 1)
        
        # Add padding to the calculated height
        padding = 60
        root.geometry(f"{max(text_width + 20, overlay_params['width'])}x{max(text_height + padding, overlay_params['height'])}+{overlay_params['x']}+{overlay_params['y']}")
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