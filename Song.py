from Frontend import Frontend
from NoteData import NoteData
from PixelList import PixelList
from Screen import Screen
from TrackList import TrackList
from Window import Window
from Cursor import Cursor
import curses

class Song:
    s : Screen
    trax : TrackList
    t : int
    new_track_id : int
    cur : Cursor

    def __init__(self):
        f = Frontend()
        self.colors = f.load_colors()
        w = Window()
        w.set_dimensions(0,curses.LINES-1,0,curses.COLS-2)
        p = PixelList()
        self.trax = TrackList()
        self.s = Screen(w,f,p,self.trax.tcm.get_track_color)
        self.trax.create_track()
        self.s.w.shift_down(40)
        self.new_note(60,1,4,0,True)
        self.cur = Cursor(60,1)

    def curL(self):
        return self.trax.get_length(self.cur.p, self.cur.x, self.trax.t)

    def curP(self):
        return self.cur.p

    def curX(self):
        return self.cur.x

    def curT(self):
        return self.trax.current()
        
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

    def move_note(self,p,x,l,np,nx,nl,note_track : int,move_cursor : bool):
        self.delete_note(p,x,l,note_track)
        self.new_note(np,nx,nl,note_track,False)
        if move_cursor:
            self.move_cursor(np,nx,note_track,note_track,old_note_exists=False)

    def move_note_in_direction(self,get_location):
        p,x = get_location(self.curP(),self.curX())
        l = self.trax.get_length(self.curP(),self.curX(),self.curT())
        if self.trax.does_note_fit(p,x,l,self.curX(),self.curT()):
            self.move_note(self.curP(),self.curX(),l,p,x,l,self.curT(),move_cursor=True)

    def move_note_up(self):
        self.move_note_in_direction(self.trax.find_note_up_location)
            
    def move_note_down(self):
        self.move_note_in_direction(self.trax.find_note_down_location)

    def move_note_left(self):
        self.move_note_in_direction(self.trax.find_note_left_location)

    def move_note_right(self):
        self.move_note_in_direction(self.trax.find_note_right_location)

    def set_note_cursor(self,p,x,l,track : int, c : bool):
        n = NoteData(p,x,l)
        self.s.set_note(n,track,c)

    def move_cursor(self,p,x,old_track : int, new_track : int, old_note_exists : bool = True):
        if old_note_exists:
            l = self.trax.get_length(self.curP(),self.curX(),old_track)
            self.set_note_cursor(self.curP(),self.curX(),l,old_track,False)
            n = NoteData(self.curP(),self.curX(),l)
            self.s.refresh_note(n,new_track)
        self.cur.set(p,x)
        new_l = self.trax.get_length(self.curP(),self.curX(),new_track)
        self.set_note_cursor(self.curP(),self.curX(),new_l,new_track,True)
        n = NoteData(self.curP(),self.curX(),new_l)
        self.s.refresh_note(n,new_track)


    def change_track(self,calculate_track):
        old_track = self.curT()
        self.trax.change_track_to(calculate_track)
        p,x = self.trax.generate_new_cursor(self.cur.p,self.cur.x)
        self.move_cursor(p,x,old_track,self.curT())
        self.s.refresh_full_screen(self.curT())

    def change_track_up(self):
        self.change_track(self.trax.get_up_track())

    def change_track_down(self):
        self.change_track(self.trax.get_down_track())

    def move_cursor_down(self):
        p,x = self.trax.find_cursor_down_target(self.curP(), self.curX())
        self.move_cursor(p,x,self.curT(),self.curT())

    def move_cursor_up(self):
        p,x = self.trax.find_cursor_up_target(self.curP(), self.curX())
        self.move_cursor(p,x,self.curT(),self.curT())

    def move_cursor_left(self):
        p,x = self.trax.find_cursor_left_target(self.curP(), self.curX())
        self.move_cursor(p,x,self.curT(),self.curT())

    def move_cursor_right(self):
        p,x = self.trax.find_cursor_right_target(self.curP(), self.curX())
        self.move_cursor(p,x,self.curT(),self.curT())
