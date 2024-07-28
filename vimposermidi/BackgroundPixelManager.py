class BackgroundPixelManager:
    """Cache background pixel data."""
    prev_x: int
    prev_is_measure_start: int

    def __init__(self):
        self.prev_x = -1
        self.prev_is_measure_start = False

    def set_prev_data(self, new_prev_x: int, new_prev_is_measure_start: bool):
        self.prev_x = new_prev_x
        self.prev_is_measure_start = new_prev_is_measure_start

    def get_prev_data(self) -> tuple[int, int]:
        return self.prev_x, self.prev_is_measure_start
