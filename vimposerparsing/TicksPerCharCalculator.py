class TicksPerCharCalculator:
    """Callable that calculates ticks per char based on the given chars per quarter note."""
    chars_per_measure: int

    def __init__(self, chars_per_quarter_note: int):
        self.chars_per_quarter_note = chars_per_quarter_note

    def __call__(self,division: int) -> int:
        assert division < 32768
        if division < 32768:
            ticks_per_quarter_note = division
            ticks_per_char = int(ticks_per_quarter_note / self.chars_per_quarter_note)
            return ticks_per_char
        return 0
