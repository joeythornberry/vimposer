from config.DefaultFrontend import Frontend 
from config import config
from vimposercore.VimposerAPI import VimposerAPI
from vimposermidi.MidiViewport import MidiViewport
from vimposersaving.minimal import write_minimal_midi_file
from sys import argv
from os.path import exists

from vimposerparsing.open_midi_file import open_midi_file

if len(argv) < 2:
    print("Usage: pose <midi file>")
    quit()

filename = argv[1]

v = VimposerAPI(Frontend(), MidiViewport(), filename)

config.init(v)


if not exists(filename):
    write_minimal_midi_file(filename)

open_midi_file(f"{argv[1]}", v.save_note, v.save_tempo, v.get_chars_per_quarter_note())

v.midi_manager.write_console()
v.midi_manager.midi_window.frontend.s.refresh()
v.midi_player.connect_to_midi_port() # this can take a while so it should happen after the GUI appears

#v.after_action_hook()
v.km.listen(v.midi_manager.midi_window.frontend.s.getkey)
v.close()
