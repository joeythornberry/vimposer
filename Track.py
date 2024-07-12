from Chord import Chord
from Note import Note

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
        return f"\n\tTRACK (color: {self.color})\n\t{chordstring}\tEND TRACK\n"

    def add_note(self,p,x,l):
        if x not in self.chords:
            self.chords[x] = Chord()
        self.chords[x].add_note(p,Note(l))

    def delete_note(self,p,x):
        if x not in self.chords:
            raise Exception(f"Track Error: chord {x} does not exist")
        self.chords[x].remove_note(p)
        if not self.chords[x].notes:
            del self.chords[x]

    def has_more_than_one_note(self) -> bool:
        more_than_one_chord = len(self.chords.keys()) > 1
        if more_than_one_chord:
            return True
        lone_chord : int = list(self.chords.keys())[0]
        return self.chords[lone_chord].has_more_than_one_note()

