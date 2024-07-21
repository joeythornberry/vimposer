from vimposermidi.Frontend import Frontend
from vimposermidi.Drawable import Drawable

class MockFrontend(Frontend):
    def __init__(self):
        pass

    def load_colors(self) -> int:
        return super().load_colors()

    def paint_pixel(self, d: Drawable):
        return super().paint_pixel(d)

    def paint_ui_element(self, y: int, x: int, icon: str):
        return super().paint_ui_element(y, x, icon)

    def close(self):
        return super().close()

if __name__ == "__main__":
    mf = MockFrontend()
