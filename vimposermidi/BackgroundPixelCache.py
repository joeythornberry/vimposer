class BackgroundPixelCache:
    """Cache background pixel data."""
    prev_x: int
    prev_chars_from_measure_start: int

    def __init__(self):
        self.prev_x = -1
        self.prev_chars_from_measure_start = False

    def set_prev_data(self, new_prev_x: int, prev_chars_from_measure_start: int):
        self.prev_x = new_prev_x
        self.prev_chars_from_measure_start = prev_chars_from_measure_start

    def get_prev_data(self) -> tuple[int, int]:
        return self.prev_x, self.prev_chars_from_measure_start
