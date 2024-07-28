import time
def is_measure_start(x: int, prev_x: int, prev_is_measure_start: bool) -> bool:
    """Return True if this pixel should be displayed as the start of a new measure."""
    if prev_x == x:
        return prev_is_measure_start
    return x % 24 == 23

def calculate_background_icon(p: int, x: int) -> str:
    """Returns the icon that the given location should display if it has no notes on it."""
    notes = "c#d#ef#g#a#b"
    i = notes[p % 12]
    return i
