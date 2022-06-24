from msvcrt import getch

#CP866 IS FOR RUSSIAN LANGUAGE!

SPECIAL_KEYS = {
    b'\x1b': 'escape',
    b'\t': 'tab',
    b' ': 'space',
    b'\r': 'enter',
    b'\x08': 'backspace'
}

ARROWS = {
    b'H': 'up_arrow',
    b'K': 'left_arrow',
    b'P': 'down_arrow',
    b'M': 'right_arrow'
}

CONSEQ_SYMB = {
    b'\x00',
    b'\xe0'
}


def get_special_key():
    ch = getch()
    if ch in SPECIAL_KEYS:
        return SPECIAL_KEYS[ch]
    elif ch not in CONSEQ_SYMB:
        return None
    ch2 = getch()
    if ch2 not in ARROWS:
        return None
    return ARROWS[ch2]