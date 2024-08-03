from vimposercore.VimposerAPI import VimposerAPI
from vimposerparsing.open_midi_file import open_midi_file
from testutils.VimposerTester import VimposerTester
from vimposermidi.TrackMidiEventsModel import TrackMidiEventsModel

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

open_midi_file(
        "MIDI/d_minor_scale.mid",
        save_note_callback,
        12
        )

model = TrackMidiEventsModel(v.midi_manager.track_midi_manager.tracks[0])
print(model.event_chords)
exists, msg = model.has_note(50, 0, 12)
assert exists, msg

for p, x, l in v.midi_manager.track_midi_manager.get_track_notes_list(0):
    exists, msg = model.has_note(p, x, l)
    assert exists, msg

#tester.assert_note_exists(60, 0, 6, 0)
tester.assert_note_exists(50, 0, 12, 0)
