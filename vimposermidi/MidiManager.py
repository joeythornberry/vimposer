from config.Frontend import Frontend
from vimposermidi.NoteData import NoteData
from vimposermidi.PixelList import PixelList
from vimposermidi.MidiWindow import MidiWindow
from vimposermidi.TrackMidiManager import TrackMidiManager
from vimposermidi.MidiViewport import MidiViewport
from vimposermidi.Cursor import Cursor
import curses

class MidiManager:
    """Edit and paint to screen MIDI notes.

    Attributes:
    midi_window -- The MidiWindow that controls the display of MIDI notes.
    tracklist -- The TrackList that stores note data.
    """
    s : MidiWindow 
    trax : TrackMidiManager
    t : int
    new_track_id : int
    cur : Cursor

    def __init__(self):
        """Init a MidiManager with default track."""
        f = Frontend()
        self.num_colors = f.load_colors()
        midi_viewport = MidiViewport()
        midi_viewport.set_dimensions(0, curses.LINES-1, 0, curses.COLS-2)
        midi_viewport.shift_up(40)
        p = PixelList()
        self.trax = TrackMidiManager(self.num_colors)
        self.s = MidiWindow(midi_viewport, f, p, self.trax.tcm.get_track_color)
        self.cur = Cursor(-1,-1)
        self.create_track()

    def curP(self) -> int:
        """Return the pitch of the cursored note."""
        return self.cur.p

    def curX(self) -> int:
        """Return the x-value of the cursored note."""
        return self.cur.x

    def curT(self) -> int:
        """Return the ID of the current track."""
        return self.trax.current()

    def curL(self) -> int:
        """Return the length of the cursored note."""
        return self.trax.get_length(self.curP(), self.curX(), self.curT())
        
    def new_note_from_cursor(self, p: int, x: int):
        """Create a note with the length of the cursored note at the given coords, and move the cursor to it."""
        successful = self.new_note(p,x,self.curL(),self.curT(),False)
        if successful:
            self.move_cursor(p,x,self.curT(),self.curT())

    def new_note(self, p: int, x: int, l: int, note_track: int, is_cursor: bool) -> bool:
        """If a note can fit in the given location on the given track, create it. Return True if the note was successfully created."""
        if not self.trax.does_note_fit(p, x, l, self.curX(), note_track):
            return False
        note_to_create = NoteData(p, x, l)
        self.trax.add_note(p, x, l, note_track)
        self.s.set_note(note_to_create, note_track, is_cursor)
        self.s.refresh_note(note_to_create, self.trax.current())
        return True

    def delete_note(self, p: int, x: int, l: int, note_track : int):
        """Delete the note at the given location and track."""
        n = NoteData(p, x, l)
        self.trax.delete_note(p, x, note_track)
        self.s.remove_note(n, note_track)
        self.s.refresh_note(n, self.trax.current())

    def move_note(self, p: int, x: int, l: int, new_p: int, new_x: int, new_l: int, note_track: int, move_cursor: bool):
        """Move the note at the first set of coords to the second set of coords (on the given track)."""
        self.delete_note(p, x, l, note_track)
        self.new_note(new_p, new_x, new_l, note_track, False)
        if move_cursor:
            self.move_cursor(new_p, new_x, note_track, note_track, old_note_exists=False)

    def move_cursor_note(self, p: int, x: int):
        """Move the cursored note to the given coords, if it will fit there."""
        l = self.trax.get_length(self.curP(), self.curX(), self.curT())
        if self.trax.does_note_fit(p, x, l, self.curX(), self.curT()):
            self.move_note(self.curP(), self.curX(), l, p, x, l, self.curT(), move_cursor=True)

    def change_cursor_note_length(self, amount: int):
        """Change the length of the cursored note by the given value (negative amount will shrink the note)."""
        self.change_note_length(self.curP(), self.curX(), self.curT(), amount, True)

    def change_note_length(self, p: int, x: int, track: int, amount: int, is_cursor: bool):
        """Change the length of the note at the given location by the specified amount (negative amount will shrink the note)."""
        old_l = self.trax.get_length(p, x, track)
        new_l = old_l + amount
        if new_l <= 0: # don't make a note with zero or negative length 
            return
        if amount > 0 and not self.trax.does_note_fit(p,x+old_l,amount,x,track): # don't extend a note into another note
            return
        self.trax.set_note_length(p, x, new_l, track)
        n = NoteData(p, x, new_l)
        if amount < 0: # have to clean up the old note bc the new smaller note won't overwrite all of it
            old_n = NoteData(p, x, old_l)
            self.s.remove_note(old_n, track)
            self.s.refresh_note(old_n, track)
        self.s.set_note(n, track, is_cursor)
        self.s.refresh_note(n, track)

    def set_note_cursor(self, p: int, x: int, l: int, track: int, is_cursor: bool):
        """Draw the note at the given location with the given cursor value."""
        note_to_give_cursor = NoteData(p, x, l)
        self.s.set_note(note_to_give_cursor, track, is_cursor)

    def move_cursor(self, p: int, x: int, old_track: int, new_track: int, old_note_exists: bool = True):
        """Move the cursor from the current cursored note to the note at the given location."""
        if old_note_exists:
            l = self.trax.get_length(self.curP(), self.curX(), old_track)
            self.set_note_cursor(self.curP(), self.curX(), l, old_track, False)
            note_to_uncursor = NoteData(self.curP(), self.curX(), l)
            self.s.refresh_note(note_to_uncursor, new_track)
        self.cur.set(p, x)
        new_l = self.trax.get_length(self.curP(), self.curX(), new_track)
        self.set_note_cursor(self.curP(), self.curX(), new_l, new_track, True)
        note_to_cursor = NoteData(self.curP(), self.curX(), new_l)
        self.s.refresh_note(note_to_cursor, new_track)

    def delete_cursor_note(self):
        """Delete the currently cursored note, and move the cursor to the nearest note. If only one note on current track, does not delete it."""
        if not self.trax.track_has_more_than_one_note(self.curT()):
            return
        self.delete_note(self.curP(), self.curX(), self.trax.get_length(self.curP(), self.curX(), self.curT()), self.curT())
        p, x = self.trax.generate_new_cursor(self.curP(), self.curX(), self.curT())
        self.move_cursor(p, x, self.curT(), self.curT(), old_note_exists=False)

    def change_track(self, calculate_track_function):
        """Change the current track to the track given by the supplied function."""
        old_note_exists = self.curX() != -1 and self.curP() != -1
        old_track = self.curT()
        self.trax.change_track_to(calculate_track_function)
        p, x = self.trax.generate_new_cursor(self.cur.p, self.cur.x, self.curT())
        self.move_cursor(p, x, old_track, self.curT(),old_note_exists)
        self.s.refresh_full_screen(self.curT())

    def change_track_up(self):
        """Change the current track to the track with the next highest id."""
        self.change_track(self.trax.get_up_track())

    def change_track_down(self):
        """Change the current track to the track with the next lowest id."""
        self.change_track(self.trax.get_down_track())

    def move_cursor_down(self):
        """Move the cursor to the next lowest note on the current chord, if one exists."""
        p, x = self.trax.find_cursor_down_target(self.curP(),  self.curX())
        self.move_cursor(p, x, self.curT(), self.curT())

    def move_cursor_up(self):
        """Move the cursor to the next highest note on the current chord, if one exists."""
        p, x = self.trax.find_cursor_up_target(self.curP(),  self.curX())
        self.move_cursor(p, x, self.curT(), self.curT())

    def move_cursor_left(self):
        """Move the cursor to the closest note to the left, as calculated by the track midi manager."""
        p, x = self.trax.find_cursor_left_target(self.curP(),  self.curX())
        self.move_cursor(p, x, self.curT(), self.curT())

    def move_cursor_right(self):
        """Move the cursor to the closest note to the right, as calculated by the track midi manager."""
        p,x = self.trax.find_cursor_right_target(self.curP(), self.curX())
        self.move_cursor(p,x,self.curT(),self.curT())

    def shift_up(self,amount):
        """Shift the Midi viewport up by the specified amount. A negative amount will lower the viewport."""
        self.s.shift_up(amount, self.curT())

    def shift_across(self,amount):
        """Shift the Midi viewport to the right by the specified amount. A negative amount will shift the viewport to the left."""
        self.s.shift_across(amount, self.curT())

    def create_track(self):
        """Create a new track, and make it the current track."""
        t = self.trax.create_track()
        self.trax.add_note(60, 0, 4, t)
        self.change_track(t)

    def delete_current_track(self):
        """Delete the current track, and switch to the track with the next highest track id. If there is no other track, create one."""
        track_to_delete = self.curT()
        if self.trax.only_one_track_exists():
            self.create_track()
        else:
            self.change_track_up()
        for p, x, l in self.trax.get_track_notes_list(track_to_delete):
            self.delete_note(p, x, l, track_to_delete)
        self.trax.delete_track(track_to_delete)
