_fishing_enabled = False
_imp2_enabled = False
_fishes_caught_session = 0

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