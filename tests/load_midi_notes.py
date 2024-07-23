import os
from tests.MockMidiViewport import MockMidiViewport
from vimposercore.VimposerAPI import VimposerAPI
from tests.MockFrontend import MockFrontend
from vimposerparsing.parse_midi_file import parse_midi_file
from vimposerparsing.TicksPerCharCalculator import TicksPerCharCalculator

frontend = MockFrontend()
midi_viewport = MockMidiViewport()
v = VimposerAPI(frontend, midi_viewport)
v.midi_manager.midi_window.midi_viewport = MockMidiViewport()

def save_note_callback(p: int, x: int, l: int, track: int) -> int:
    if len(v.midi_manager.track_midi_manager.tracks) <= track:
        v.create_track()
        return save_note_callback(p, x, l, track)
    else:
        v.midi_manager.new_note(p, x, l, track, False)
        return 0

parse_midi_file(
        "MIDI/d_minor_scale.mid",
        save_note_callback,
        TicksPerCharCalculator(12)
        )

print(frontend.pixels)
default_note_exists, msg = frontend.has_note(60, 0, 4)
assert default_note_exists, msg

first_d_exists, msg = frontend.has_note(50,0,12)
assert first_d_exists, msg

# method 2, faster
print("\033[2J\033[H", end="", flush=True) # clears, ensures no new line
                                           # and ensures immediate print
# the ansi code here is interpreted as clearing the screen with `\033[2J` but it
# doesn't move the cursor back to the beginning which is why `\033[H`
