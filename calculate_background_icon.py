def calculate_background_icon(p: int, x: int) -> str:
    """Returns the icon that the given location should display if it has no notes on it."""
    notes = "c#d#ef#g#a#b"
    i = notes[p % 12]
    if x % 24 == 23:
        return "|"
    return i
