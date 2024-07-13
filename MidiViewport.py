class MidiViewport:
    """Define area of screen dedicated to midi, and translate (p,x) to (line,char) coords.

    Attributes:
    across -- How far right the viewport has been shifted (never negative)
    up -- how far up the viewport has been shifted (never negative)
    top, bottom -- The lines the top and bottom borders are drawn on
    left, right -- the chars the left and right borders are drawn on
    height -- the height of the viewport
    """

    across: int
    up: int
    top: int
    bottom: int
    left: int
    right: int 
    height: int

    def __init__(self):
        """Init a MidiViewport with across and up offsets set to 0"""
        self.across = 0
        self.up = 0

    def set_dimensions(self, top: int, bottom: int, left: int, right: int):
        """Set viewport borders to given values, and calculate viewport height"""
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right 
        self.height = self.bottom - self.top

    def shift_across(self, amount: int):
        """Shift viewport across the screen.

        Can shift in negative direction, but will not set across to a negative value.
        """
        if self.across == 0 and amount < 0:
            return
        self.across += amount

    def shift_up(self, amount: int):
        """Shift viewport up and down the screen.

        Can shift in negative direction, but will not set up to a negative value, or to a value that would 
        draw a pitch location above 127 on the screen.
        """
        if (self.up == 0 and amount < 0) or (self.up == (129-self.height) and amount > 0):
            return
        self.up += amount

    def translate_coords(self, p: int, x: int) -> tuple[int, int, bool]:
        """Translate (p, x) coords to (line, char) coords for display on screen, and report if coords will be in viewport or not.

        Returns line, char, onscreen, where onscreen is True if the coordinates will be in the viewport and should be drawn.
        """
        line = self.top + self.up + self.height - p - 1
        char = x + self.left - self.across + 1
        onscreen = not (line < self.top + 1 or line > self.bottom - 1 or char < self.left + 1 or char > self.right - 1)
        return line, char, onscreen

    def translate_coords_reverse(self,line,char) -> tuple[int, int]:
        """Translate (line, char) coords to (p, x) coords."""
        p = self.top + self.up + self.height - line - 1
        x = char - self.left + self.across - 1
        return p, x

    def locate_full_screen(self):
        """Yield all (p, x) coordinate pairs that are currently visible on the screen"""
        for y in range(self.top,self.bottom):
            for x in range(self.left,self.right):
                yield self.translate_coords_reverse(y,x)

    def yield_border(self):
        """Yield (line, char) coords and ui icon types for the viewport's border on the screen.

        Yields line, char, icon.
        """
        # top
        for char in range(self.left+1, self.right):
            yield self.top, char, "top_border"

        # bottom
        for char in range(self.left+1, self.right):
            yield self.bottom, char, "bottom_border"

        # left
        for line in range(self.top+1, self.bottom):
            yield line, self.left, "left_border"

        # right 
        for line in range(self.top+1, self.bottom):
            yield line, self.right, "right_border"

        yield self.top,self.left,"top_left_corner"
        yield self.top,self.right,"top_right_corner"
        yield self.bottom,self.left,"bottom_left_corner"
        yield self.bottom,self.right,"bottom_right_corner"
