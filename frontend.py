import window
import curses

class Frontend:
    def __init__(self,window):
        self.s = curses.initscr()
        self.w = window

    def draw_window_border(self):
        for y,x,char in self.w.yield_border():
            self.s.move(y,x)
            self.s.addch(char)

    def paint_pixel(self, p, x, icon):
        line, char, onscreen = self.w.translate_coords(p,x)
        if onscreen:
            self.s.move(line, char)
            self.s.addch(icon)

    def draw_note(self, y, x, icons):
        for index,i in enumerate(icons):
            line, char, onscreen = self.w.translate_coords(y,x)
            if onscreen:
                self.s.move(line,char+index)
                self.s.addch(i)

    def close(self):
        curses.endwin()
        curses.echo()
