from vimposermidi.Chord import Chord
from vimposermidi.Note import Note

class TrackMidi:
    """Represent a track in a Midi file."""
    chords : dict[int, Chord]
    velocity: int
    instrument: int

    def __init__(self, velocity: int, instrument: int):
        """Init a Track with an empty chords dict."""
        self.chords: dict[int, Chord] = {}
        self.velocity = velocity
        self.instrument = instrument

    def __repr__(self):
        chordstring = ""
        for c in self.chords.items():
            chordstring += f"\t{c}\n"
        return f"\n\tTRACK\n\t{chordstring}\tEND TRACK\n"

    def has_note(self, p: int, x: int, l: int) -> bool:
        """Return True if the given chord has a note of the given pitch and length."""
        if x not in self.chords:
            return False
        return self.chords[x].has_note(p, l)

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

    def calculate_closest_pitch(self, old_p: int, x: int) -> int:
        """Return the closest occupied pitch to the given pitch in the chord at the given x-value."""
        return self.chords[x].calculate_closest_pitch(old_p)

    def calculate_closest_coordinates(self, old_p: int, old_x: int) -> tuple[int, int]:
        """Return the closest (p, x) coords to the given coords."""
        closest_x = self.calculate_closest_chord(old_x)
        closest_p = self.chords[closest_x].calculate_closest_pitch(old_p)
        return closest_p, closest_x

    def does_note_fit(self, p: int, x: int, l: int, current_x: int) -> bool:
        """Return True if a note with the given coords and length can fit on the screen."""
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

    def find_cursor_up_target(self, current_p: int, x: int) -> tuple[int, int]:
        """Return the note above the given note on the same chord, or the given note if none exists."""
        return self.chords[x].find_cursor_up_target(current_p), x

    def find_cursor_down_target(self, current_p: int, x: int) -> tuple[int, int]:
        """Return the note below the given note on the same chord, of the given note if none exists."""
        return self.chords[x].find_cursor_down_target(current_p), x

    def find_cursor_horizontal_target(self, current_p: int, current_x: int, left: bool):
        """Find the best note to the left or right of the given location, as determined by the left flag.

        If left is True, find the note to the left. If False, find the note to the right.
        """
        x_values = list(self.chords.keys())
        x_values.sort()
        index_of_current_x = x_values.index(current_x)

        can_move = (left and index_of_current_x > 0) or (not left and index_of_current_x < len(x_values) - 1)
        if can_move:
            if left:
                new_x = x_values[index_of_current_x - 1]
            else:
                new_x = x_values[index_of_current_x + 1]
            new_p = self.calculate_closest_pitch(current_p, new_x)
            return new_p, new_x
        return current_p, current_x

    def find_cursor_left_target(self, current_p: int, current_x: int):
        """Return the best note to the left of the given location."""
        return self.find_cursor_horizontal_target(current_p, current_x, True)

    def find_cursor_right_target(self, current_p: int, current_x: int):
        """Return the best note to the right of the given location."""
        return self.find_cursor_horizontal_target(current_p, current_x, False)
