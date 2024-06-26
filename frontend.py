import window
from pixels import Drawable
import curses

class Frontend:
    def __init__(self,window):
        self.s = curses.initscr()
        self.w = window
        if not curses.has_colors():
            curses.endwin()
            curses.echo()
            print("Your terminal does not support color")
            quit()
        curses.start_color()
        curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_BLUE)

    def draw_window_border(self):
        for y,x,char in self.w.yield_border():
            self.s.move(y,x)
            self.s.addch(char)

    def paint_pixel(self, p, x, d: Drawable):
        line, char, onscreen = self.w.translate_coords(p,x)
        if onscreen:
            self.s.move(line, char)
            self.s.addch(d.icon,curses.color_pair(d.color))

    def draw_note(self, y, x, ds: list[Drawable]):
        for index,d in enumerate(ds):
            line, char, onscreen = self.w.translate_coords(y,x)
            if onscreen:
                self.s.move(line,char+index)
                self.s.addch(d.icon)

    def close(self):
        curses.endwin()
        curses.echo()
