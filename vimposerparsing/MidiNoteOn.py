class MidiNoteOn:
    """Store note information while waiting for the note to end.

    Attributes: 
        start_time -- The raw time of the NoteOn event from the MIDI file.
    """
    start_time: int
    
    def __init__(self, start_time: int):
        """Init a MidiNoteOn with the given start time."""
        self.start_time = start_time

    def __repr__(self):
        return f"{self.start_time}"
