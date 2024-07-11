import sys
sys.path.append(".")
from VimposerAPI import VimposerAPI
import time

v = VimposerAPI()
t1 = v.s.trax.create_track()
t2 = v.s.trax.create_track()
try:

    for _ in range(10):
        v.move_note_right()

    v.km.map("F",v.make_note_right)
    v.km.map("A",v.make_note_left)
    v.km.map("S",v.make_note_down)
    v.km.map("D",v.make_note_up)

    v.km.map("s",v.move_cursor_down)
    v.km.map("d",v.move_cursor_up)
    v.km.map("a",v.move_cursor_left)
    v.km.map("f",v.move_cursor_right)

    v.km.map("k",v.move_note_up)
    v.km.map("j",v.move_note_down)
    v.km.map("h",v.move_note_left)
    v.km.map("l",v.move_note_right)

    v.km.listen(v.s.s.f.s.getkey)
finally:
    v.s.s.f.close()
    time.sleep(0.001)
    print(v.s.trax.tracks)
