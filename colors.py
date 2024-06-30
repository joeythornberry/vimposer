import curses

class Color:
    def set_foreground(self, foreground : int):
        self.f = foreground

    def set_background(self, background : int):
        self.b = background

stdscr = curses.initscr()
curses.start_color()

cs = [
        (1000,1000,1000),
        (1000,0,0),
        (0,1000,0),
        (0,0,1000),
        ]

colors : list[Color] = []
background_color = curses.COLOR_BLACK
color_counter = 0
for i,c in enumerate(cs):

    color_id = i + 8 # don't overwrite the default colors
    curses.init_color(color_id,c[0],c[1],c[2])

    current_color = Color()
    color_counter += 1
    curses.init_pair(color_counter,color_id,background_color)
    current_color.set_foreground(color_counter)
    color_counter += 1
    curses.init_pair(color_counter,background_color,color_id)
    current_color.set_background(color_counter)

    colors.append(current_color)

for i in range(len(colors)):
    c = colors[i]
    stdscr.move(i,0)
    stdscr.attron(curses.color_pair(c.f))
    stdscr.addch("%")
    stdscr.move(i,1)
    stdscr.attron(curses.color_pair(c.b))
    stdscr.addch(" ")

stdscr.refresh()
stdscr.getch()

curses.echo()
curses.endwin()
