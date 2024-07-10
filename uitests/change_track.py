import sys
sys.path.append(".")
from VimposerAPI import VimposerAPI
import time

v = VimposerAPI()
t2 = v.s.trax.create_track()
try:
    v.s.new_note(60,5,4,0,False)
    v.s.new_note(65,13,4,t2,False)
    v.s.new_note(67,5,4,t2,False)
    v.s.new_note(68,9,4,t2,False)
    v.km.map("t",v.change_track_up)
    v.km.map("T",v.change_track_down)
    v.km.listen(v.s.s.f.s.getkey)
finally:
    v.s.s.f.close()
    time.sleep(0.001)
    print(v.s.trax.tracks)

