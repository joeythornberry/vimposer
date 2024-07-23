from vimposercore.VimposerAPI import VimposerAPI
from vimposerparsing.parse_midi_file import parse_midi_file
from vimposerparsing.TicksPerCharCalculator import TicksPerCharCalculator
from tests.VimposerTester import VimposerTester

tester = VimposerTester()
v = VimposerAPI(tester.mock_frontend, tester.mock_midi_viewport)
tester.observe_track_midi_manager(v)

def save_note_callback(p: int, x: int, l: int, track: int) -> int:
    if len(v.midi_manager.track_midi_manager.tracks) <= track:
        v.create_track(p, x, l)
        return 0
    else:
        v.midi_manager.new_note(p, x, l, track, False)
        return 0

parse_midi_file(
        "MIDI/d_minor_scale.mid",
        save_note_callback,
        TicksPerCharCalculator(12)
        )

#tester.assert_note_exists(60, 0, 6, 0)
tester.assert_note_exists(50, 0, 12, 0)
