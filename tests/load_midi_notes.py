from vimposercore.VimposerAPI import VimposerAPI
from tests.MockFrontend import MockFrontend
from vimposerparsing.parse_midi_file import parse_midi_file
from vimposerparsing.TicksPerCharCalculator import TicksPerCharCalculator

frontend = MockFrontend()
v = VimposerAPI(frontend)

def save_note_callback(p: int, x: int, l: int, track: int) -> int:
    if len(v.s.track_midi_manager.tracks) <= track:
        v.create_track()
        return save_note_callback(p, x, l, track)
    else:
        v.s.new_note(p, x, l, track, False)
        return 0

parse_midi_file(
        "MIDI/bwv1052a.mid",
        save_note_callback,
        TicksPerCharCalculator(12)
        )
