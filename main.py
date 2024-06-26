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
w.set_dimensions(0,20,0,60)

f = frontend.Frontend(w)

def send_keys(keys):
    pass
km = KeyboardManager.KeyboardManager(send_keys)

v = vapi.VimposerAPI(f,km)
v.add_track()
v.extend_to(60)

init.init(v)
v.create_note(2,4,4)
v.create_note(4,8,4)
v.create_note(5,12,4)
v.f.draw_window_border()
v.paint_entire_screen()
v.km.listen(stdscr.getkey)

v.f.close()
time.sleep(1)
print(v.tracks)

