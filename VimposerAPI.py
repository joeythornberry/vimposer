from KeyboardManager import KeyboardManager
from Song import Song

class VimposerAPI:
    km : KeyboardManager
    s : Song

    def send_keys(self,msg):
        pass

    def __init__(self):
        self.km = KeyboardManager(self.send_keys)
        self.s = Song()

    def sound(self):
        print("we are here")

    def make_note_right(self):
        self.s.new_note_from_cursor(self.s.curP(),self.s.curX() + self.s.curL())

    def make_note_left(self):
        self.s.new_note_from_cursor(self.s.curP(),self.s.curX() - self.s.curL())

    def make_note_up(self):
        self.s.new_note_from_cursor(self.s.curP() + 1,self.s.curX())

    def make_note_down(self):
        self.s.new_note_from_cursor(self.s.curP() - 1,self.s.curX())

    def delete_cursor_note(self):
        self.s.delete_cursor_note()

    def change_track_up(self):
        self.s.change_track_up()

    def change_track_down(self):
        self.s.change_track_down()

    def move_cursor_down(self):
        self.s.move_cursor_down()

    def move_cursor_up(self):
        self.s.move_cursor_up()

    def move_cursor_left(self):
        self.s.move_cursor_left()

    def move_cursor_right(self):
        self.s.move_cursor_right()

    def move_note_right(self):
        self.s.move_note_in_direction(self.s.curP(),self.s.curX() + 1)
            
    def move_note_left(self):
        self.s.move_note_in_direction(self.s.curP(),self.s.curX() - 1)

    def move_note_down(self):
        self.s.move_note_in_direction(self.s.curP() - 1,self.s.curX())

    def move_note_up(self):
        self.s.move_note_in_direction(self.s.curP() + 1,self.s.curX())

    def shift_window_vertical(self,amount : int):
        self.s.shift_up(amount)

    def shift_window_horizontal(self,amount : int):
        self.s.shift_across(amount)

    def create_track(self):
        self.s.create_track()

    def delete_current_track(self):
        self.s.delete_current_track()
