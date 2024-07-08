from Frontend import Frontend
from NoteData import NoteData
from PixelList import PixelList
from Screen import Screen
from TrackList import TrackList
from Window import Window

class Song:
    s : Screen
    trax : TrackList
    t : int
    new_track_id : int

    def __init__(self):
        f = Frontend()
        self.colors = f.load_colors()
        w = Window()
        w.set_dimensions(1,30,1,30)
        p = PixelList()
        self.trax = TrackList()
        self.s = Screen(w,f,p,self.trax.tcm.get_track_color)
        
    def new_note(self,p,x,l,note_track : int, c):
        n = NoteData(p,x,l)
        self.trax.add_note(p,x,l,note_track)
        self.s.set_note(n,note_track,c)
        self.s.refresh_note(n,self.trax.current())

    def delete_note(self,p,x,l,note_track : int):
        n = NoteData(p,x,l)
        self.trax.delete_note(p,x,note_track)
        self.s.remove_note(n,note_track)
        self.s.refresh_note(n,self.trax.current())

    def move_note(self,p,x,l,np,nx,nl,note_track : int,c):
        self.delete_note(p,x,l,note_track)
        self.new_note(np,nx,nl,note_track,c)
