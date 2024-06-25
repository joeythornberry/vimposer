import KeyboardManager
import time
import init
import curses
import window
import frontend
import vapi

stdscr = curses.initscr()
curses.noecho()

w = window.Window()
w.set_dimensions(3,13,5,35)

f = frontend.Frontend(w)

def send_keys(keys):
    pass
km = KeyboardManager.KeyboardManager(send_keys)

v = vapi.VimposerAPI(f,km)
v.add_track()
v.extend_to(10)

init.init(v)
v.create_note(5,5,5)
v.f.draw_window_border()
v.paint_entire_screen()
v.km.listen(stdscr.getkey)

v.f.close()
time.sleep(1)
print(v.tracks)

