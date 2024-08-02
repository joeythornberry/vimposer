from collections.abc import Callable

from config.DefaultFrontend import Frontend 
from vimposercore.VimposerAPI import VimposerAPI

from vimposermidi.MidiViewport import MidiViewport
from config import config

from vimposerparsing.open_midi_file import open_midi_file

from sys import argv
v = VimposerAPI(Frontend(), MidiViewport())

config.init(v)

def save_note(p: int, x: int, l: int, track: int):
    if len(v.midi_manager.track_midi_manager.tracks) <= track:
        v.create_track(p, x, l)
    else:
        v.midi_manager.new_note(p, x, l, track, False)

chars_per_quarter_note = 12
open_midi_file(f"MIDI/{argv[1]}", save_note, chars_per_quarter_note)

v.km.listen(v.midi_manager.midi_window.frontend.s.getkey)
v.midi_manager.midi_window.frontend.close()
