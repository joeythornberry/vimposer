from vimposerparsing.TicksPerCharCalculator import TicksPerCharCalculator
from vimposerparsing.parse_midi_file import parse_midi_file

class MockNote:
    p: int
    x: int
    l: int
    track: int

    def __init__(self, p: int, x: int, l: int, track: int):
        assert x >= 0
        assert p >= 0
        assert p <= 127
        assert l > 0
        self.p = p
        self.x = x
        self.l = l
        self.track = track

class MockSaveNote:

    num_calls: int
    mock_notes: list[MockNote]
    
    def __init__(self):
        self.num_calls = 0
        self.mock_notes = []

    def __call__(self, p: int, x: int, l: int, track: int) -> int:
        self.num_calls += 1
        mock_note = MockNote(p, x, l, track)
        self.mock_notes.append(mock_note)
        return 0

calculate_ticks_per_char = TicksPerCharCalculator(6)

mock_save_note = MockSaveNote()
parse_midi_file(
        "MIDI/quantized_triplets.mid",
        mock_save_note,
        calculate_ticks_per_char
        )

assert mock_save_note.num_calls == 9
assert len(mock_save_note.mock_notes) == 9
assert mock_save_note.mock_notes[0].x == 0
assert mock_save_note.mock_notes[1].x == 0
assert mock_save_note.mock_notes[0].p == 60
assert mock_save_note.mock_notes[1].p == 48
assert mock_save_note.mock_notes[0].track == 0
assert mock_save_note.mock_notes[0].l == 6
assert mock_save_note.mock_notes[1].l == 8
print("all tests passed")
