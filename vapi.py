import curses
import pixels
from KeyboardManager import KeyboardManager
from frontend import Frontend
import track

def get_note_chars(duration):
    #return [curses.ACS_BLOCK for _ in range(duration)]
    return ["%" for _ in range(duration)]

def get_erase_chars(duration):
    return [" " for _ in range(duration)]

class VimposerAPI:
    def __init__(self,f : Frontend,km : KeyboardManager):
        self.f = f
        self.num_colors = self.f.load_colors()
        self.km = km
        self.tracks : list[track.Track] = []
        self.current_track = 0
        self.pix = pixels.PixelList()
        self.length = 0

    def color_is_taken(self,color : int):
        for track in self.tracks:
            if track.color == color:
                return True
        return False

    def assign_new_color(self) -> int:
        color_to_try = 0
        while self.color_is_taken(color_to_try):
            color_to_try += 1
            if color_to_try >= self.num_colors:
                return 0

        return color_to_try
    
    def extend_to(self,length):
        self.length = length

    def add_track(self):
        self.tracks.append(track.Track(self.assign_new_color()))

    def change_track(self,t : int):
        self.current_track = t
        self.paint_entire_screen()

    def get_background_drawable(self,p,x):
        notes = "c#d#efg#a#b"
        d = pixels.Drawable(notes[p % 11])
        d.set_color(-1)
        d.set_track(-1)
        return d

    def get_pixel(self, p, x) -> pixels.Drawable:    
        d = self.pix.get_drawable(p,x,self.current_track)
        if d == False:
            return self.get_background_drawable(p,x)
        else:
            d.set_color(self.tracks[d.track].color)
            return d 

    def set_length(self, length):
        self.length = length
        
    def paint_entire_screen(self):
        for x in range(self.length):
            for p in range(128):
                d = self.get_pixel(p,x)
                is_current_track = d.track == self.current_track
                self.f.paint_pixel(p,x,d,is_current_track)

    def create_note(self,p,x,d):
        self.tracks[self.current_track].add_note(p,x,d)
        for i,icon in enumerate(get_note_chars(d)):
            draw = pixels.Drawable(icon)
            self.pix.set_drawable(p,x+i,self.current_track,draw)
            draw.set_color(2)
            self.f.paint_pixel(p,x+i,draw,True)

    def move_note(self,p,x,np,nx,d):
        #self.f.draw_note(p,x,get_erase_chars(d))
        #self.f.draw_note(np,nx,get_note_chars(d))
        pass
