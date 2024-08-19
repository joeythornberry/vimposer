from io import BufferedReader
from vimposercore.VimposerAPI import VimposerAPI
from vimposerparsing.open_midi_file import open_midi_file
from testutils.VimposerTester import VimposerTester
from vimposersaving.BinaryWrites import WriteCounter, read_variable_length_number, write_variable_length_number
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
    model.write(midifile, ticks_per_char, WriteCounter())

def read_8(file: BufferedReader):
    return int.from_bytes(file.read(1))

def read_16(file: BufferedReader):
    return int.from_bytes(file.read(2))

with open("test.txt", "rb") as midifile:
    for byte in "MTrk":
        c = read_8(midifile)
        assert c == ord(byte)
            
    length = read_16(midifile)
    print("len:",length)

    varlen_num = read_variable_length_number(midifile)
    read_8(midifile)
    read_8(midifile)
    read_8(midifile)
    for i in range(1,7):
        varlen_num = read_variable_length_number(midifile)
        print(varlen_num)
        read_8(midifile)
        read_8(midifile)
        read_8(midifile)
        read_8(midifile)
        read_8(midifile)
        read_8(midifile)

#tester.assert_note_exists(60, 0, 6, 0)
tester.assert_note_exists(50, 0, 12, 0)
