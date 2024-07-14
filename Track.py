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

    def calculate_closest_chord(self, old_x: int) -> int:
        """Return the occupied x-value closest to the given x-value on this track."""
        k = list(self.chords.keys())
        closest = 0
        closest_distance = abs(old_x - k[0])
        for i, x in enumerate(k):
            distance = abs(old_x - x)
            if distance < closest_distance:
                closest = i
                closest_distance = distance

        return k[closest] 

    def calculate_closest_pitch(self, old_p, x) -> int:
        return self.chords[x].calculate_closest_pitch(x)

    def calculate_closest_coordinates(self, old_p: int, old_x: int) -> tuple[int, int]:
        closest_x = self.calculate_closest_chord(old_x)
        closest_p = self.chords[closest_x].calculate_closest_pitch(old_p)
        return closest_p, closest_x

    def does_note_fit(self, p: int, x: int, l: int, current_x: int) -> bool:
        for chord_x, chord in self.chords.items():
            if chord.pitch_occupied(p):
                if chord_x == current_x and current_x != x:
                        continue # don't want the note itself to block itself from moving
                if chord_x <= x and chord_x + chord.get_note_length(p) > x:
                        return False
                if chord_x > x and chord_x < x + l:
                    return False
        if x < 0 or p < 0 or p > 127:
            return False

        return True
