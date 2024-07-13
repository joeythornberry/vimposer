def calculate_background_icon(p,x):
    notes = "c#d#ef#g#a#b"
    i = notes[p % 12]
    if x % 24 == 23:
        return "|"
    return i
