import sys
sys.path.append(".")
from VimposerAPI import VimposerAPI
import time

v = VimposerAPI()
t1 = v.s.trax.create_track()
t2 = v.s.trax.create_track()
try:
    v.s.new_note(65,1,4,0,False)
    v.s.new_note(67,1,9,0,False)
    v.s.new_note(69,1,13,0,False)

    v.s.new_note(68,9,4,t2,False)
    v.s.new_note(66,9,4,t2,False)

    v.s.new_note(66,9,4,t1,False)
    v.s.new_note(68,13,4,t1,False)

    v.km.map("t",v.change_track_up)
    v.km.map("T",v.change_track_down)
    v.km.map("j",v.move_cursor_down)
    v.km.map("k",v.move_cursor_up)
    v.km.map("h",v.move_cursor_left)
    v.km.map("l",v.move_cursor_right)
    v.km.listen(v.s.s.f.s.getkey)
finally:
    v.s.s.f.close()
    time.sleep(0.001)
    print(v.s.trax.tracks)

