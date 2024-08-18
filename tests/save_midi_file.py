from io import BufferedReader
import sys
from vimposercore.VimposerAPI import VimposerAPI
from vimposerparsing.open_midi_file import open_midi_file
from testutils.VimposerTester import VimposerTester
from vimposersaving.BinaryWrites import read_variable_length_number, write_variable_length_number
from vimposersaving.TrackMidiEventsModel import TrackMidiEventsModel
from vimposersaving.save_midi_file import save_midi_file

tester = VimposerTester()
v = VimposerAPI(tester.mock_frontend, tester.mock_midi_viewport)
tester.observe_track_midi_manager(v)

def save_note_callback(p: int, x: int, l: int, track: int):
    if len(v.midi_manager.track_midi_manager.tracks) <= track:
        v.create_track(p, x, l)
    else:
        v.midi_manager.new_note(p, x, l, track, False)

ticks_per_char = open_midi_file(
        sys.argv[1],
        save_note_callback,
        12
        )

save_midi_file("test.mid", v.midi_manager.track_midi_manager)

