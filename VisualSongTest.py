from Song import Song
import time

s = Song()

t1 = s.trax.create_track()
t2 = s.trax.create_track()
t3 = s.trax.create_track()
s.trax.change_track_to(t3)
s.new_note(3,5,7,t3,False)
s.new_note(5,5,7,t1,False)
s.new_note(7,5,7,t2,False)
s.s.f.s.getch()
s.move_note(7,5,7,9,6,8,t2,False)
s.s.f.s.getch()
s.trax.change_track_to(t2)
s.s.refresh_full_screen(t2)
s.s.f.s.getch()
s.s.f.close()
time.sleep(0.001)
print(s.trax)
