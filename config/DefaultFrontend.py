from vimposermidi.Drawable import Drawable
from vimposermidi.VimposerFrontend import VimposerFrontend
import curses

class Color:
    def set_foreground(self, foreground : int):
        self.f = foreground

    def set_background(self, background : int):
        self.b = background

class Frontend(VimposerFrontend):
    def __init__(self):
        self.s = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        if not curses.has_colors():
            curses.endwin()
            curses.echo()
            print("Your terminal does not support color")
            quit()
        curses.start_color()
        curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_BLUE)
        # thanks to ChatGPT for the color choices lolol
        self.rgb_codes = [
                (1000, 0, 0),     # Red
                (0, 1000, 0),     # Green
                (0, 0, 1000),     # Blue
                (1000, 1000, 0),  # Yellow
                (1000, 0, 1000),  # Magenta
                (0, 1000, 1000),  # Cyan
                (1000, 500, 0),   # Orange
                (500, 1000, 0),   # Lime
                (0, 1000, 500),   # Aqua
                (1000, 0, 500),   # Fuchsia
                (500, 0, 1000),   # Purple
                (500, 500, 1000), # Periwinkle
                (1000, 500, 500), # Salmon
                (500, 1000, 500)  # Spring Green
                ]

    def paint_ui_element(self,y,x,icon):
        self.s.move(y,x)
        char = "X"
        match icon:
            case "left_border":
                char = curses.ACS_VLINE
            case "right_border":
                char = curses.ACS_VLINE
            case "top_border":
                char = curses.ACS_HLINE
            case "bottom_border":
                char = curses.ACS_HLINE
            case "top_left_corner":
                char = curses.ACS_ULCORNER
            case "top_right_corner":
                char = curses.ACS_URCORNER
            case "bottom_left_corner":
                char = curses.ACS_LLCORNER
            case "bottom_right_corner":
                char = curses.ACS_LRCORNER
        self.s.addch(char)

    def load_colors(self) -> int:
        self.colors : list[Color] = []
        background_color = curses.COLOR_BLACK
        curses.init_color(2,300,300,300)
        curses.init_pair(2,2,background_color)
        self.weak_ui_color = 2
        color_counter = 5 # leave room for ui colors
        for i,c in enumerate(self.rgb_codes):

            color_id = i + 8 # don't overwrite the default colors
            curses.init_color(color_id,c[0],c[1],c[2])

            current_color = Color()
            color_counter += 1
            curses.init_pair(color_counter,color_id,background_color)
            current_color.set_foreground(color_counter)
            color_counter += 1
            curses.init_pair(color_counter,background_color,color_id)
            current_color.set_background(color_counter)

            self.colors.append(current_color)

        return len(self.colors)

    def paint_pixel(self, d: Drawable):
        self.s.move(d.line,d.char)

        icon = "X"
        match d.icon:
            case "note_start":
                if d.cursor:
                    icon = curses.ACS_BULLET
                else:
                    icon = "["
            case "note_middle":
                if d.cursor:
                    icon = curses.ACS_BULLET
                else:
                    icon = " "
            case "note_end":
                if d.cursor:
                    icon = curses.ACS_BULLET
                else:
                    icon = "]"

        match d.type:
            case "background":
                self.s.attron(curses.color_pair(self.weak_ui_color))
                icon = d.icon
            case "measure_start":
                self.s.attron(curses.color_pair(self.weak_ui_color))
                icon = "|"
            case "focused_track":
                self.s.attron(curses.color_pair(self.colors[d.color].b))
            case "unfocused_track":
                self.s.attron(curses.color_pair(self.colors[d.color].f))
            case _:
                raise Exception("PAINT ERROR: drawable has no type")

        self.s.addch(icon)

    def close(self):
        curses.endwin()
        curses.echo()

    def write_console(self, lines: list[str], screen_width: int):
        for (y,line) in enumerate(lines):
            self.s.attron(curses.color_pair(self.colors[2].f))
            self.s.move(y, 0)
            self.s.addstr(str.join("",[" " for _ in range(screen_width)]))
            self.s.move(y, 1)
            self.s.addstr(line)
        self.s.refresh()
