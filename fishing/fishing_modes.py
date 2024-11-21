fishing_modes = [
    'Only Perfect',
    'Perfect+No Flying Wish Fish',
    'Great',
    'Standard'
]

fishing_mode_params = {
    'Only Perfect': {'score_limit': 99999, 'perfect_loops_max': 2000},
    'Perfect+No Flying Wish Fish': {'score_limit': 99999, 'perfect_loops_max': 2},
    'Great': {'score_limit': 8000, 'perfect_loops_max': 2000},
    'Standard': {'score_limit': 5000, 'perfect_loops_max': 2000},
}

save_on_fishes_count_options = [48, 5, 10, 20, 30, None]

_current_fishing_mode_index = fishing_modes.index('Perfect+No Flying Wish Fish')
_current_save_on_fishes_count_index = 0

def get_fishing_mode():
    return fishing_modes[_current_fishing_mode_index]

def set_fishing_mode():
    global _current_fishing_mode_index
    _current_fishing_mode_index = (_current_fishing_mode_index + 1) % len(fishing_modes)

def get_fishing_mode_params():
    return fishing_mode_params[get_fishing_mode()]

def get_save_on_fishes_count():
    return save_on_fishes_count_options[_current_save_on_fishes_count_index]

def set_save_on_fishes_count():
    global _current_save_on_fishes_count_index
    _current_save_on_fishes_count_index = (_current_save_on_fishes_count_index + 1) % len(save_on_fishes_count_options)