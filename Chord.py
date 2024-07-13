from Note import Note

class Chord:
    def __init__(self):
        self.notes : dict[int,Note] = {}

    def __repr__(self):
        notestring = ""
        for key,n in self.notes.items():
            notestring += f" {key}: {n},"
        return f"[{notestring}]"

    def pitch_occupied(self, pitch):
        return pitch in self.notes

    def add_note(self, pitch, note):
        if(self.pitch_occupied(pitch)):
           raise Exception(f"Chord Error: pitch {pitch} is occupied already")
        self.notes[pitch] = note

    def remove_note(self, pitch):
        if(not self.pitch_occupied(pitch)):
            raise Exception(f"Chord Error: no note at {pitch} to delete")
        note = self.notes[pitch]
        del self.notes[pitch]
        return note

    def has_more_than_one_note(self):
        return len(self.notes.keys()) > 1

    def get_notes_list(self) -> list[tuple[int,Note]]:
        return list(self.notes.items())

    def set_note_length(self,p,l):
        self.notes[p].l = l

