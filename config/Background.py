from math import floor

def get_chars_from_measure_start(x: int, prev_x: int, prev_is_measure_start: int) -> int:
    """Return how many chars after the last measure-start char this pixel will be displayed."""
    if prev_x == x:
        return prev_is_measure_start
    chars_per_measure = 24
    return x - (chars_per_measure * floor(x / chars_per_measure))

def calculate_background_icon(p: int, chars_from_measure_start: int) -> str:
    """Returns the icon that the given location should display if it has no notes on it."""
    if chars_from_measure_start == 0:
        return "1"
    elif chars_from_measure_start == 5:
        return "5"
    notes = "c#d#ef#g#a#b"
    i = notes[p % 12]
    return i
