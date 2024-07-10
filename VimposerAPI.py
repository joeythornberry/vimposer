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

    def make_note(self):
        self.s.new_note(self.s.curP(),self.s.curX()+self.s.curL(),self.s.curL(),self.s.curT(),True)

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
