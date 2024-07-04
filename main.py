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
w.set_dimensions(0,curses.LINES-2,0,curses.COLS-1)
f = frontend.Frontend(w)

def send_keys(keys):
    pass
km = KeyboardManager.KeyboardManager(send_keys)

v = vapi.VimposerAPI(f,km)
v.extend_to(200)
v.add_track()

init.init(v)
v.create_note(12,4,4)
v.create_note(10,4,4)
v.create_note(8,4,4)
v.create_note(4,4,4)
v.create_note(13,10,4)
v.create_note(11,10,4)
v.create_note(9,10,4)
v.create_note(5,10,4)
v.add_track()
v.change_track_up()
v.create_note(20,4,4)
v.create_note(22,8,4)
v.create_note(20,12,4)
v.create_note(23,12,4)
v.change_track_up()
v.change_track_up()
v.f.draw_window_border()
v.paint_entire_screen()
v.km.listen(stdscr.getkey)

v.f.close()
time.sleep(1)
print(v.tracks)
print(v.full_log)

