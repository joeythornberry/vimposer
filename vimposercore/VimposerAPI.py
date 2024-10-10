from vimposercore.KeyboardManager import KeyboardManager
from vimposercore.LinuxMidiPlayer import LinuxMidiPlayer
from vimposermidi.MidiViewport import MidiViewport
from vimposermidi.VimposerFrontend import VimposerFrontend
from vimposermidi.MidiManager import MidiManager
from vimposermidi.tempo_conversions import mpq_to_bpm

class VimposerAPI:
    km : KeyboardManager
    midi_manager : MidiManager
    chars_per_quarter_note: int

    def set_chars_per_quarter_note(self, new: int):
        self.chars_per_quarter_note = new

    def get_chars_per_quarter_note(self):
        return self.chars_per_quarter_note

    def send_keys(self,msg):
        self.midi_manager.in_progress_keys = msg
        self.midi_manager.write_console()

    def save_note(self, p: int, x: int, l: int, track: int, velocity: int, instrument: int):
        if len(self.midi_manager.track_midi_manager.tracks) <= track:
            self.create_track(p, x, l, velocity, instrument)
        else:
            self.midi_manager.new_note(p, x, l, track, False)

    def save_tempo(self, new_tempo: int):
        self.midi_manager.tempo = mpq_to_bpm(new_tempo)

    def after_action_hook(self):
        # self.play_cursor_note()
        self.midi_manager.write_console()

    def log(self, msg):
        self.midi_manager.console.log(msg)

    def __init__(self, frontend: VimposerFrontend, midi_viewport: MidiViewport, filename: str):
        self.km = KeyboardManager(self.after_action_hook, self.send_keys)
        self.midi_manager = MidiManager(frontend, midi_viewport, 2, filename)
        self.midi_player = LinuxMidiPlayer()
        self.midi_player.initialize_player()
        self.log("Welcome to Vimposer.")
        self.log("Happy Composing!")

    def play_cursor_note(self):
        t = self.midi_manager.track_midi_manager.tracks[self.midi_manager.curT()]
        self.midi_player.play_note(t.instrument, self.midi_manager.curP(), t.velocity)

    def set_tempo(self, new_tempo: int):
        if new_tempo > 0:
            self.midi_manager.tempo = new_tempo
        else:
            self.log("New tempo must be greater than zero.")

    def set_current_track_velocity(self, new_velocity: int):
        if new_velocity >= 0 and new_velocity < 128:
            self.midi_manager.track_midi_manager.set_current_track_velocity(new_velocity)
        else: 
            self.log("New velocity must be between 0 and 127")

    def set_current_track_instrument(self, new_instrument: int):
        if new_instrument >= 0 and new_instrument < 128:
            self.midi_manager.track_midi_manager.set_current_track_instrument(new_instrument)
        else: 
            self.log("New instrument must be between 0 and 127")

    def sound(self):
        print("we are here")

    def save(self, _):
        self.log("Saving...")
        self.midi_manager.write_console()
        self.midi_manager.save()
        self.log("Saved!")

    def make_note_right(self, times: int):
        for _ in range(times):
            self.midi_manager.new_note_from_cursor(self.midi_manager.curP(),self.midi_manager.curX() + self.midi_manager.curL())

    def make_note_left(self, times: int):
        for _ in range(times):
            self.midi_manager.new_note_from_cursor(self.midi_manager.curP(),self.midi_manager.curX() - self.midi_manager.curL())

    def make_note_up(self, offset: int):
        self.midi_manager.new_note_from_cursor(self.midi_manager.curP() + offset, self.midi_manager.curX())

    def make_note_down(self, offset: int):
        self.midi_manager.new_note_from_cursor(self.midi_manager.curP() - offset,self.midi_manager.curX())

    def delete_cursor_note(self, _):
        self.midi_manager.delete_cursor_note()

    def change_track_up(self, _):
        self.midi_manager.change_track_up()

    def change_track_down(self, _):
        self.midi_manager.change_track_down()

    def move_cursor_down(self, _):
        self.midi_manager.move_cursor_down()

    def move_cursor_up(self, _):
        self.midi_manager.move_cursor_up()

    def move_cursor_left(self, _):
        self.midi_manager.move_cursor_left()

    def move_cursor_right(self, _):
        self.midi_manager.move_cursor_right()

    def move_note_right(self, amount: int):
        self.midi_manager.move_cursor_note(self.midi_manager.curP(),self.midi_manager.curX() + amount)
            
    def move_note_left(self, amount: int):
        self.midi_manager.move_cursor_note(self.midi_manager.curP(),self.midi_manager.curX() - amount)

    def move_note_down(self, amount: int):
        self.midi_manager.move_cursor_note(self.midi_manager.curP() - amount,self.midi_manager.curX())

    def move_note_up(self, amount: int):
        self.midi_manager.move_cursor_note(self.midi_manager.curP() + amount,self.midi_manager.curX())

    def shift_window_vertical(self, amount: int):
        self.midi_manager.shift_up(amount)

    def shift_window_horizontal(self,amount: int):
        self.midi_manager.shift_across(amount)

    def create_track(self, starting_note_p: int = 60, starting_note_x: int = 0, starting_note_l: int = 6, track_velocity: int = 100, track_instrument: int = 0):
        self.midi_manager.create_track(starting_note_p, starting_note_x, starting_note_l, track_velocity, track_instrument)

    def delete_current_track(self, _):
        self.midi_manager.delete_current_track()

    def lengthen_cursor_note(self, amount: int):
        self.midi_manager.change_cursor_note_length(amount)

    def shorten_cursor_note(self, amount: int):
        self.midi_manager.change_cursor_note_length(-amount)

    def close(self):
        self.midi_manager.midi_window.frontend.close()
        self.midi_player.close_player()

    def toggle_playing(self, _: int):
        self.midi_player.toggle_playing(self.midi_manager.filename)
        self.log(str(self.midi_player.play_file_process))
