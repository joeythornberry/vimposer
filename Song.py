from Frontend import Frontend
from NoteData import NoteData
from PixelList import PixelList
from Screen import Screen
from Track import Track
from Window import Window

class Song:
    s : Screen
    tracks : dict[int,Track]
    t : int
    new_track_id : int

    def __init__(self):
        f = Frontend()
        self.colors = f.load_colors()
        w = Window()
        w.set_dimensions(1,30,1,30)
        p = PixelList()
        self.s = Screen(w,f,p,self.get_track_color)
        self.tracks = {}
        self.t = 0
        self.new_track_id = -1
        
    def assign_track_color(self) -> int:
        if not self.tracks:
            return 0
        taken_colors = [track.color for track in self.tracks.values()]
        color = 0
        while color in taken_colors:
            color += 1
        return color
            
    def create_track(self):
        self.new_track_id += 1
        self.tracks[self.new_track_id] = Track(self.assign_track_color())
        return self.new_track_id

    def get_track_color(self, t : int):
        return self.tracks[t].color

    def new_note(self,p,x,l,note_track : int, c):
        n = NoteData(p,x,l)
        self.s.set_note(n,note_track,c)
        self.s.refresh_note(n,self.t)
