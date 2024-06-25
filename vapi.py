import curses
from KeyboardManager import KeyboardManager
from frontend import Frontend
import track

def get_note_chars(duration):
    return [curses.ACS_BLOCK for _ in range(duration)]

def get_erase_chars(duration):
    return [" " for _ in range(duration)]

class VimposerAPI:
    def __init__(self,f : Frontend,km : KeyboardManager):
        self.f = f
        self.km = km
        self.tracks : list[track.Track] = []
        self.current_track = 0
    
    def extend_to(self,length):
        for t in self.tracks:
            t.extend_to(length)

    def add_track(self):
        self.tracks.append(track.Track())

    def get_pixel(self, p, x):    
        chord : track.Chord = self.tracks[self.current_track].chords[x]
        if p in chord.notes:
            return 'n'
        else:
            return 'i'

    def paint_entire_screen(self):
        width = len(self.tracks[0].chords)
        for x in range(width):
            for p in range(128):
                char = self.get_pixel(p,x)
                self.f.paint_pixel(p,x,char)

    def create_note(self,p,x,d):
        self.tracks[self.current_track].add_note(p,x,d)
        self.f.draw_note(p,x,get_note_chars(d))

    def move_note(self,p,x,np,nx,d):
        self.f.draw_note(p,x,get_erase_chars(d))
        self.f.draw_note(np,nx,get_note_chars(d))
