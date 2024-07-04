import curses
import pixels
from KeyboardManager import KeyboardManager
from frontend import Frontend
import track

class Cursor:
    def __init__(self):
        self.p = 0
        self.x = 0
        self.exists = False

    def set(self,newp:int,newx:int):
        self.p = newp
        self.x = newx

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
        self.cur = Cursor()

#    def resize_window(self):
#        self.f.w.set_dimensions(0,curses.LINES-2,0,curses.COLS-1)

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

    def generate_new_cursor(self,old_p,old_x):
        return 0,0

    def change_track_to(self,t : int):
        old_p,old_x = self.remove_cursor()
        self.current_track = t
        new_p,new_x = self.generate_new_cursor(old_p,old_x)
        self.cur.set(new_p, new_x)
        self.paint_entire_screen()
    
    def change_track_up(self):
        new_track = self.current_track + 1
        if new_track == len(self.tracks):
            new_track = 0
        self.change_track_to(new_track)

    def change_track_down(self):
        new_track = self.current_track - 1
        if new_track == -1:
            new_track = len(self.tracks) - 1
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

    def create_note(self,p,x,d,change_cursor=True):
        self.tracks[self.current_track].add_note(p,x,track.Note(d))
        for i,icon in enumerate(get_note_chars(d)):
            draw = pixels.Drawable(icon)
            self.pix.set_drawable(p,x+i,self.current_track,draw)
            draw.set_color(2)
            self.f.paint_pixel(p,x+i,draw,True)
        if change_cursor:
            self.change_cursor(p,x)

    def move_note(self,p,x,np,nx,d):
        #self.f.draw_note(p,x,get_erase_chars(d))
        #self.f.draw_note(np,nx,get_note_chars(d))
        pass

    def get_note_duration(self,p,x):
        return self.tracks[self.current_track].chords[p].notes[x].d

    def remove_cursor(self):
        if not self.cur.exists:
            return self.cur.p, self.cur.x
        self.set_note_cursor(self.cur.p,self.cur.x,self.get_note_duration(self.cur.p,self.cur.x),False)
        self.cur.exists = False
        return self.cur.p, self.cur.x

    def set_note_cursor(self,p,x,d,c:bool):
        for i in range(d):
            self.pix.pixels[(p,x+i)].tracks[self.current_track].set_cursor(c)

    def change_cursor(self, p, x, refresh=True):
        pass
        if self.cur.exists:
            l = self.get_note_duration(self.cur.p,self.cur.x)
            self.set_note_cursor(self.cur.p,self.cur.x,l,False)
        l = self.get_note_duration(p,x)
        self.set_note_cursor(p,x,l,True)
        self.cur.set(p,x)
        self.cur.exists = True
        if refresh:
            self.paint_entire_screen()
