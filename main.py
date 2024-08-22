from config.DefaultFrontend import Frontend 
from config import config
from vimposercore.VimposerAPI import VimposerAPI
from vimposermidi.MidiViewport import MidiViewport
from sys import argv

from vimposerparsing.open_midi_file import open_midi_file

if len(argv) < 2:
    print("Usage: pose <midi file>")
    quit()

v = VimposerAPI(Frontend(), MidiViewport(), argv[1])

config.init(v)

open_midi_file(f"{argv[1]}", v.save_note, v.save_tempo, v.get_chars_per_quarter_note())

v.after_action_hook()
v.km.listen(v.midi_manager.midi_window.frontend.s.getkey)
v.midi_manager.midi_window.frontend.close()
