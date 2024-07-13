from Frontend import Frontend
from NoteData import NoteData
from PixelList import PixelList
from Screen import Screen
from TrackList import TrackList
from MidiViewport import MidiViewport
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
        midi_viewport = MidiViewport()
        midi_viewport.set_dimensions(0,curses.LINES-1,0,curses.COLS-2)
        midi_viewport.shift_up(40)
        p = PixelList()
        self.trax = TrackList()
        self.s = Screen(midi_viewport,f,p,self.trax.tcm.get_track_color)
        self.cur = Cursor(-1,-1)
        self.create_track()

    def curL(self):
        return self.trax.get_length(self.cur.p, self.cur.x, self.trax.t)

    def curP(self):
        return self.cur.p

    def curX(self):
        return self.cur.x

    def curT(self):
        return self.trax.current()
        
    def new_note_from_cursor(self,p,x):
        successful = self.new_note(p,x,self.curL(),self.curT(),False)
        if successful:
            self.move_cursor(p,x,self.curT(),self.curT())

    def new_note(self,p,x,l,note_track : int, c) -> bool:
        if not self.trax.does_note_fit(p,x,l,self.curX(),note_track):
            return False
        n = NoteData(p,x,l)
        self.trax.add_note(p,x,l,note_track)
        self.s.set_note(n,note_track,c)
        self.s.refresh_note(n,self.trax.current())
        return True

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

    def move_note_in_direction(self,p,x):
        l = self.trax.get_length(self.curP(),self.curX(),self.curT())
        if self.trax.does_note_fit(p,x,l,self.curX(),self.curT()):
            self.move_note(self.curP(),self.curX(),l,p,x,l,self.curT(),move_cursor=True)

    def change_cursor_note_length(self,amount):
        self.change_note_length(self.curP(),self.curX(),self.curT(),amount,True)

    def change_note_length(self,p,x,track : int,amount : int,is_cursor : bool):
        old_l = self.trax.get_length(p,x,track)
        new_l = old_l + amount
        if new_l <= 0:
            return
        if amount > 0 and not self.trax.does_note_fit(p,x+old_l,amount,x,track):
            return
        self.trax.set_note_length(p,x,new_l,track)
        n = NoteData(p,x,new_l)
        if amount < 0:
            old_n = NoteData(p,x,old_l)
            self.s.remove_note(old_n,track)
            self.s.refresh_note(old_n,track)
        self.s.set_note(n,track,is_cursor)
        self.s.refresh_note(n,track)

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

    def delete_cursor_note(self):
        if not self.trax.track_has_more_than_one_note(self.curT()):
            return
        self.delete_note(self.curP(),self.curX(),self.trax.get_length(self.curP(),self.curX(),self.curT()),self.curT())
        p,x = self.trax.generate_new_cursor(self.curP(),self.curX())
        self.move_cursor(p,x,self.curT(),self.curT(),old_note_exists=False)

    def change_track(self,calculate_track):
        old_note_exists = self.curX() != -1 and self.curP() != -1
        old_track = self.curT()
        self.trax.change_track_to(calculate_track)
        p,x = self.trax.generate_new_cursor(self.cur.p,self.cur.x)
        self.move_cursor(p,x,old_track,self.curT(),old_note_exists)
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

    def shift_up(self,amount):
        self.s.shift_up(amount, self.curT())

    def shift_across(self,amount):
        self.s.shift_across(amount, self.curT())

    def create_track(self):
        t = self.trax.create_track()
        self.trax.add_note(60,0,4,t)
        #p,x = self.trax.generate_new_cursor(0,0,t)
        #self.cur.set(p,x)
        #self.move_cursor(p,x,self.curT(),t,old_note_exists=False)
        self.change_track(t)

    def delete_current_track(self):
        track_to_delete = self.curT()
        if self.trax.only_one_track_exists():
            self.create_track()
        else:
            self.change_track_up()
        for p,x,l in self.trax.get_track_notes_list(track_to_delete):
            self.delete_note(p,x,l,track_to_delete)
        self.trax.delete_track(track_to_delete)
