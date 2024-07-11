def calculate_background_icon(p,x):
    notes = "c#d#ef#g#a#b"
    try:
        i = notes[p % 12]
        return i
    except:
        return "X"
