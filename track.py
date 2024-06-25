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
    def __init__(self):
        self.chords = []

    def __repr__(self):
        chordstring = ""
        for c in self.chords:
            chordstring += f"\t{c}\n"
        return f"TRACK\n{chordstring}END TRACK"

    def extend_to(self, to):
        needed_chords = to - len(self.chords)
        if to > 0:
            for _ in range(needed_chords):
                self.chords.append(Chord())

    def add_note(self,x,p,note):
        if x >= len(self.chords):
            raise Exception(f"Track Error: chord {x} is out of range")
        self.chords[x].add_note(p,note)

    def remove_note(self,x,p):
        if x >= len(self.chords):
            raise Exception(f"Track Error: chord {x} is out of range")
        self.chords[x].remove_note(p)

