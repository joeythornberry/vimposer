import curses
import pixels
from KeyboardManager import KeyboardManager
from frontend import Frontend
import track

def get_note_chars(duration):
    #return [curses.ACS_BLOCK for _ in range(duration)]
    return [" " for _ in range(duration)]

def get_erase_chars(duration):
    return [" " for _ in range(duration)]

class VimposerAPI:
    def __init__(self,f : Frontend,km : KeyboardManager):
        self.f = f
        self.km = km
        self.tracks : list[track.Track] = []
        self.current_track = 0
        self.pix = pixels.PixelList()
    
    def extend_to(self,length):
        for t in self.tracks:
            t.extend_to(length)

    def add_track(self):
        self.tracks.append(track.Track())

    def get_background_drawable(self,p,x):
        #notes = "c#d#efg#a#b"
        notes = "-----------"
        return pixels.Drawable(notes[p % 11])

    def get_pixel(self, p, x) -> pixels.Drawable:    
        icon, exists = self.pix.get_drawable(p,x,self.current_track)
        if exists:
            return icon
        else:
            return self.get_background_drawable(p,x)

    def paint_entire_screen(self):
        width = len(self.tracks[0].chords)
        for x in range(width):
            for p in range(128):
                d = self.get_pixel(p,x)
                self.f.paint_pixel(p,x,d)

    def create_note(self,p,x,d):
        self.tracks[self.current_track].add_note(p,x,d)
        for i,icon in enumerate(get_note_chars(d)):
            draw = pixels.Drawable(icon,2)
            self.pix.set_drawable(p,x+i,self.current_track,draw)
            self.f.paint_pixel(p,x+i,draw)

    def move_note(self,p,x,np,nx,d):
        #self.f.draw_note(p,x,get_erase_chars(d))
        #self.f.draw_note(np,nx,get_note_chars(d))
        pass
