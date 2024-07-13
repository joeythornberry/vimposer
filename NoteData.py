class NoteData:
    """Store the information a Screen needs to find the locations to refresh.

    Attributes:
    p -- The pitch of the note.
    x -- The starting x of the note.
    l -- The length of the note.
    """
    p: int
    x: int
    l: int

    def __init__(self, p: int, x: int, l: int):
        """Init a NoteData with the specified pitch, x, and l values"""
        self.p = p
        self.x = x
        self.l = l
