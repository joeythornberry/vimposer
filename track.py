class Note:
    def __init__(self, d):
        self.d = d

    def __repr__(self):
        return f"<duration: {self.d}>"

class Chord:
    def __init__(self):
        self.notes = {}

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


class Track:
    def __init__(self, color : int):
        self.chords = {}
        self.color = color

    def __repr__(self):
        chordstring = ""
        for c in self.chords.items():
            chordstring += f"\t{c}\n"
        return f"TRACK\n{chordstring}END TRACK"

    def add_note(self,x,p,note):
        if x not in self.chords:
            self.chords[x] = Chord()
        self.chords[x].add_note(p,note)

    def remove_note(self,x,p):
        if x not in self.chords:
            raise Exception(f"Track Error: chord {x} does not exist")
        self.chords[x].remove_note(p)
        if not self.chords[x].notes:
            del self.chords[x]

