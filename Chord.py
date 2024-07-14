from Note import Note

class Chord:
    """Store all of the Notes for a given x-value."""

    def __init__(self):
        """Init Chord with empty notes dict."""
        self.notes : dict[int,Note] = {}

    def __repr__(self):
        notestring = ""
        for key,n in self.notes.items():
            notestring += f" {key}: {n},"
        return f"[{notestring}]"

    def pitch_occupied(self, p: int) -> bool:
        """Return True if this chord contains a note at the given pitch"""
        return p in self.notes

    def add_note(self, p: int, note: Note):
        """Add note to this chord at the given pitch. Throw error if pitch is already occupied."""
        if(self.pitch_occupied(p)):
           raise Exception(f"Chord Error: pitch {p} is occupied already")
        self.notes[p] = note

    def remove_note(self, p: int):
        """Remove the Note at the given pitch from this chord. Throw error if there is no Note at the given pitch."""
        if(not self.pitch_occupied(p)):
            raise Exception(f"Chord Error: no note at {p} to delete")
        del self.notes[p]

    def has_more_than_one_note(self):
        """Return True if there is more than one Note in this chord.""" 
        return len(self.notes.keys()) > 1

    def get_notes_list(self) -> list[tuple[int, Note]]:
        """Return this chord's pitch-Note combinations as a list of (p, Note) tuples."""
        return list(self.notes.items())

    def set_note_length(self, p: int, l: int):
        """Set the length of the note at pitch p in this chord to l."""
        self.notes[p].l = l

    def get_note_length(self, p: int) -> int:
        """Return the length of the Note at the given pitch in this chord."""
        return self.notes[p].l

    def calculate_closest_pitch(self, old_p) -> int:
        """Return the occupied pitch in this chord that is closest to the given pitch."""
        k = list(self.notes.keys())
        closest = 0
        closest_distance = abs(old_p - k[0])
        for i,p in enumerate(k):
            distance = abs(old_p - p)
            if distance < closest_distance:
                closest = i
                closest_distance = distance

        return k[closest] 

    def find_cursor_vertical_target(self, current_p: int, up: bool) -> int:
        """Returns higher/lower pitch, if one exists. Direction is determined by the up flag.

        If up is true, attempt to return a higher pitch. If false, attempt to return a lower pitch."""
        pitches = list(self.notes.keys())
        pitches.sort()
        index_of_current_pitch = pitches.index(current_p)
        if up and index_of_current_pitch < len(pitches) - 1:
            new_p = pitches[index_of_current_pitch + 1]
            return new_p
        if not up and index_of_current_pitch > 0 :
            new_p = pitches[index_of_current_pitch - 1]
            return new_p
        return current_p

    def find_cursor_down_target(self, current_p) -> int:
        """If this chord has a note at a lower pitch than the given pitch, return it. Otherwise, return the given pitch."""
        return self.find_cursor_vertical_target(current_p, False)

    def find_cursor_up_target(self, current_p) -> int:
        """If this chord has a note at a higher pitch than the given pitch, return it. Otherwise, return the given pitch."""
        return self.find_cursor_vertical_target(current_p, True)
