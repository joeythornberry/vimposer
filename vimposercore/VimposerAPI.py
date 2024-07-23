from vimposercore.KeyboardManager import KeyboardManager
from vimposermidi.MidiViewport import MidiViewport
from vimposermidi.VimposerFrontend import VimposerFrontend
from vimposermidi.MidiManager import MidiManager

class VimposerAPI:
    km : KeyboardManager
    midi_manager : MidiManager

    def send_keys(self,msg):
        pass

    def __init__(self, frontend: VimposerFrontend, midi_viewport: MidiViewport):
        self.km = KeyboardManager(self.send_keys)
        self.midi_manager = MidiManager(frontend, midi_viewport)

    def sound(self):
        print("we are here")

    def make_note_right(self):
        self.midi_manager.new_note_from_cursor(self.midi_manager.curP(),self.midi_manager.curX() + self.midi_manager.curL())

    def make_note_left(self):
        self.midi_manager.new_note_from_cursor(self.midi_manager.curP(),self.midi_manager.curX() - self.midi_manager.curL())

    def make_note_up(self):
        self.midi_manager.new_note_from_cursor(self.midi_manager.curP() + 1,self.midi_manager.curX())

    def make_note_down(self):
        self.midi_manager.new_note_from_cursor(self.midi_manager.curP() - 1,self.midi_manager.curX())

    def delete_cursor_note(self):
        self.midi_manager.delete_cursor_note()

    def change_track_up(self):
        self.midi_manager.change_track_up()

    def change_track_down(self):
        self.midi_manager.change_track_down()

    def move_cursor_down(self):
        self.midi_manager.move_cursor_down()

    def move_cursor_up(self):
        self.midi_manager.move_cursor_up()

    def move_cursor_left(self):
        self.midi_manager.move_cursor_left()

    def move_cursor_right(self):
        self.midi_manager.move_cursor_right()

    def move_note_right(self):
        self.midi_manager.move_cursor_note(self.midi_manager.curP(),self.midi_manager.curX() + 1)
            
    def move_note_left(self):
        self.midi_manager.move_cursor_note(self.midi_manager.curP(),self.midi_manager.curX() - 1)

    def move_note_down(self):
        self.midi_manager.move_cursor_note(self.midi_manager.curP() - 1,self.midi_manager.curX())

    def move_note_up(self):
        self.midi_manager.move_cursor_note(self.midi_manager.curP() + 1,self.midi_manager.curX())

    def shift_window_vertical(self,amount : int):
        self.midi_manager.shift_up(amount)

    def shift_window_horizontal(self,amount : int):
        self.midi_manager.shift_across(amount)

    def create_track(self, starting_note_p: int = 60, starting_note_x: int = 0, starting_note_l: int = 6):
        self.midi_manager.create_track(starting_note_p, starting_note_x, starting_note_l)

    def delete_current_track(self):
        self.midi_manager.delete_current_track()

    def lengthen_cursor_note(self,amount):
        self.midi_manager.change_cursor_note_length(amount)

    def shorten_cursor_note(self,amount):
        self.midi_manager.change_cursor_note_length(-amount)
