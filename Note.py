class Note:
    """Represent a MIDI note. 

    l -- The length of the note.
    """
    l : int
    def __init__(self, l : int):
        """Init a Note with the given length."""
        self.l = l

    def __repr__(self):
        return f"<duration: {self.l}>"

