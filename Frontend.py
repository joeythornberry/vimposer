from Drawable import Drawable
import curses

class Color:
    def set_foreground(self, foreground : int):
        self.f = foreground

    def set_background(self, background : int):
        self.b = background

class Frontend:
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
        self.rgb_codes = [
            (1000,1000,1000),
            (1000,0,0),
            (0,1000,0),
            (0,0,1000),
            ]

    def paint_ui_element(self,y,x,icon):
        self.s.move(y,x)
        self.s.addch(icon)

    def load_colors(self) -> int:
        self.colors : list[Color] = []
        background_color = curses.COLOR_BLACK
        curses.init_color(20,300,300,300)
        curses.init_pair(2,20,background_color)
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
        self.s.move(d.y,d.x)

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
