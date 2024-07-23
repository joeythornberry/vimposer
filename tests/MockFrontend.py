from vimposermidi.Drawable import Drawable
from vimposermidi.VimposerFrontend import VimposerFrontend

class MockFrontend(VimposerFrontend):
    num_colors: int
    pixels: dict[tuple[int, int], Drawable]

    def __init__(self):
        self.num_colors = 100
        self.pixels = {}

    def set_num_colors(self, new_num_colors: int):
        self.num_colors = new_num_colors

    def load_colors(self) -> int:
        return self.num_colors

    def paint_pixel(self, d: Drawable):
        if d.color == -1:
            return
        self.pixels[d.line, d.char] = d

    def has_note(self, line: int, char: int, l: int) -> tuple[bool, str]:
        if not (line, char) in self.pixels:
            return False, f"no pixel at {line}, {char}"
        note_start_drawable = self.pixels[line, char]
        if not note_start_drawable.icon == "note_start":
            return False, "could not find note_start"

        for i_char in range(char + 1,char + l - 2):
            if not (line, char) in self.pixels:
                return False, f"no pixel at {line}, {char}"
            note_middle_drawable = self.pixels[line, i_char]
            if not note_middle_drawable.icon == "note_middle":
                return False, "could not find note_middle"

        if not (line, char) in self.pixels:
            return False, f"no pixel at {line}, {char}"
        note_end_drawable = self.pixels[line, char + l - 1]
        if not note_end_drawable.icon == "note_end":
            return False, "could not find note_end"

        return True, "note exists"

    def paint_ui_element(self, y: int, x: int, icon: str):
        return super().paint_ui_element(y, x, icon)

    def close(self):
        return super().close()

if __name__ == "__main__":
    mf = MockFrontend()
