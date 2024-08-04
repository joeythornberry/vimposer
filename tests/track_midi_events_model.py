from vimposercore.VimposerAPI import VimposerAPI
from vimposerparsing.open_midi_file import open_midi_file
from testutils.VimposerTester import VimposerTester
from vimposersaving.BinaryWrites import read_variable_length_number, write_variable_length_number
from vimposersaving.TrackMidiEventsModel import TrackMidiEventsModel

tester = VimposerTester()
v = VimposerAPI(tester.mock_frontend, tester.mock_midi_viewport)
tester.observe_track_midi_manager(v)

def save_note_callback(p: int, x: int, l: int, track: int):
    if len(v.midi_manager.track_midi_manager.tracks) <= track:
        v.create_track(p, x, l)
    else:
        v.midi_manager.new_note(p, x, l, track, False)

ticks_per_char = open_midi_file(
        "MIDI/d_minor_scale.mid",
        save_note_callback,
        12
        )

model = TrackMidiEventsModel(v.midi_manager.track_midi_manager.tracks[0])
exists, msg = model.has_note(50, 0, 12)
assert exists, msg

for p, x, l in v.midi_manager.track_midi_manager.get_track_notes_list(0):
    exists, msg = model.has_note(p, x, l)
    assert exists, msg

with open("test.txt", "wb") as midifile:
    model.write(midifile, ticks_per_char)

with open("test.txt", "rb") as midifile:
    for i in range(7):
        varlen_num = read_variable_length_number(midifile)
        print(f"delta {i}: {varlen_num}")

#tester.assert_note_exists(60, 0, 6, 0)
tester.assert_note_exists(50, 0, 12, 0)
