from vimposermidi.MidiViewport import MidiViewport

class MockMidiViewport(MidiViewport):
    def __init__(self):
        super().__init__()
        self.set_dimensions(0,100,0,100)

    def translate_coords(self, p: int, x: int) -> tuple[int, int, bool]:
        return p, x, True

    def translate_coords_reverse(self, line, char) -> tuple[int, int]:
        return line, char

