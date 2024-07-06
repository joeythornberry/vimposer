from Chord import Chord

class Track:
    color : int
    chords : dict[int,Chord]

    def __init__(self, color : int):
        self.chords = {}
        self.color = color

    def __repr__(self):
        chordstring = ""
        for c in self.chords.items():
            chordstring += f"\t{c}\n"
        return f"TRACK\n{chordstring}END TRACK\n"

    def add_note(self,p,x,note):
        if x not in self.chords:
            self.chords[x] = Chord()
        self.chords[x].add_note(p,note)

    def remove_note(self,x,p):
        if x not in self.chords:
            raise Exception(f"Track Error: chord {x} does not exist")
        self.chords[x].remove_note(p)
        if not self.chords[x].notes:
            del self.chords[x]

