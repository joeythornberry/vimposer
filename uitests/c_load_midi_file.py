from config.DefaultFrontend import Frontend 
from config import config
from vimposercore.VimposerAPI import VimposerAPI
from vimposermidi.MidiViewport import MidiViewport
from sys import argv

from vimposerparsing.open_midi_file import open_midi_file

v = VimposerAPI(Frontend(), MidiViewport())

config.init(v)

chars_per_quarter_note = 12
open_midi_file(f"{argv[1]}", v.save_note, chars_per_quarter_note)

v.km.listen(v.midi_manager.midi_window.frontend.s.getkey)
v.midi_manager.midi_window.frontend.close()
