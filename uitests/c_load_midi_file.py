from ctypes import CFUNCTYPE, c_int8 # c_int8?

from config.DefaultFrontend import Frontend 
from vimposercore.VimposerAPI import VimposerAPI

from vimposermidi.MidiViewport import MidiViewport
from vimposerparsing.TicksPerCharCalculator import TicksPerCharCalculator
from c.load_midi_file import load_midi_file 
from config import config

from sys import argv

v = VimposerAPI(Frontend(), MidiViewport())

config.init(v)

@CFUNCTYPE(None, c_int8, c_int8, c_int8, c_int8)
def save_note_callback(p: int, x: int, l: int, track: int):
    print(f"saving note {p=} {x=} {l=} {track=}")
    if len(v.midi_manager.track_midi_manager.tracks) <= track:
        v.create_track(p, x, l)
    else:
        v.midi_manager.new_note(p, x, l, track, False)

load_midi_file(
        f"MIDI/{argv[1]}",
        save_note_callback,
        )

v.km.listen(v.midi_manager.midi_window.frontend.s.getkey)
v.midi_manager.midi_window.frontend.close()
