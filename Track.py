from Chord import Chord
from Note import Note

class Track:
    """Represent a track in a Midi file."""
    chords : dict[int, Chord]

    def __init__(self):
        """Init a Track with an empty chords dict."""
        self.chords: dict[int, Chord] = {}

    def __repr__(self):
        chordstring = ""
        for c in self.chords.items():
            chordstring += f"\t{c}\n"
        return f"\n\tTRACK\n\t{chordstring}\tEND TRACK\n"

    def add_note(self, p: int, x: int, l: int):
        """Add a note to this track at the given coords. Create a Chord if none exists at this x."""
        if x not in self.chords:
            self.chords[x] = Chord()
        self.chords[x].add_note(p,Note(l))

    def delete_note(self, p: int, x: int):
        """Delete the note at the given coords from this track. Raise exception if no Chord exists at x.

        Deletes the Chord if it is now empty.
        """
        if x not in self.chords:
            raise Exception(f"Track Error: chord {x} does not exist")
        self.chords[x].remove_note(p)
        if not self.chords[x].notes:
            del self.chords[x]

    def has_more_than_one_note(self) -> bool:
        """Return True if there is more than one note in this track."""
        more_than_one_chord = len(self.chords.keys()) > 1
        if more_than_one_chord:
            return True
        # If there's only one chord, see how many notes it has.
        lone_chord : int = list(self.chords.keys())[0]
        return self.chords[lone_chord].has_more_than_one_note()

    def get_notes_list(self):
        """Return a list of (p,x,l) tuples representing the Notes in this track."""
        notes = []
        for x,c in self.chords.items():
            for p,n in c.get_notes_list():
                notes.append((p,x,n.l))

        return notes
    
    def set_note_length(self, p: int, x: int, l: int):
        """Set the length of the note at the given coords to the given l."""
        self.chords[x].set_note_length(p, l)

    def get_note_length(self, p: int, x: int) -> int:
        """Return the length of the Note at the given coords in this track."""
        return self.chords[x].get_note_length(p)
