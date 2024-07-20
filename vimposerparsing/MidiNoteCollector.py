from vimposerparsing.MidiNoteOn import MidiNoteOn

class MidiNoteCollector:
    """Store the currently playing notes while we parse through the MIDI file. 

    Attributes:
        pitch_to_note_map -- a map of pitches to the notes that are currently playing on them. Only one note is allowed per pitch."""
    pitch_to_note_map: dict[int, MidiNoteOn]

    def __init__(self):
        """Init a MidiNoteCollector."""
        self.pitch_to_note_map = {}

    def push_note_on(self, pitch: int, note_on: MidiNoteOn):
        """Mark the given pitch as occupied by the given note."""
        self.pitch_to_note_map[pitch] = note_on

    def pop_note_on(self, pitch: int) -> MidiNoteOn:
        """Return the MidiNoteOn occupying the given pitch, and then free the pitch."""
        assert(pitch in self.pitch_to_note_map)
        note_on = self.pitch_to_note_map[pitch]
        del self.pitch_to_note_map[pitch]
        return note_on

    def __repr__(self):
        return str(self.pitch_to_note_map)
