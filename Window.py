import curses
class Window:
    def __init__(self):
        self.across = 0
        self.up = 0

    def set_dimensions(self,top,bottom,left,right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right 
        self.height = self.bottom - self.top

    def shift_across(self,amount):
        if self.across == 0 and amount < 0:
            return
        self.across += amount

    def shift_up(self,amount):
        if (self.up == 0 and amount < 0) or (self.up == (129-self.height) and amount > 0):
            return
        self.up += amount

    def translate_coords(self,p,x):
        line = self.top + self.up + self.height - p - 1
        char = x + self.left - self.across + 1
        onscreen = not (line < self.top + 1 or line > self.bottom - 1 or char < self.left + 1 or char > self.right - 1)
        return line,char,onscreen

    def translate_coords_reverse(self,line,char):
        p = self.top + self.up + self.height - line - 1
        x = char - self.left + self.across - 1
        return p,x

    def locate_full_screen(self):
        for y in range(self.top,self.bottom):
            for x in range(self.left,self.right):
                yield self.translate_coords_reverse(y,x)

    def yield_border(self):

        # top
        for x in range(self.left+1, self.right):
            yield self.top,x,curses.ACS_HLINE

        # bottom
        for x in range(self.left+1, self.right):
            yield self.bottom,x,curses.ACS_HLINE

        # left
        for y in range(self.top+1, self.bottom):
            yield y, self.left, curses.ACS_VLINE

        # right 
        for y in range(self.top+1, self.bottom):
            yield y, self.right, curses.ACS_VLINE

        yield self.top,self.left,curses.ACS_ULCORNER
        yield self.top,self.right,curses.ACS_URCORNER
        yield self.bottom,self.left,curses.ACS_LLCORNER
        yield self.bottom,self.right,curses.ACS_LRCORNER
