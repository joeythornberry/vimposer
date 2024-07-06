from Song import Song

s = Song()

t1 = s.create_track()
t2 = s.create_track()
s.new_note(3,5,7,0,False)
s.new_note(5,5,7,t1,False)
s.new_note(7,5,7,t2,False)
s.s.f.s.getch()
s.s.f.close()
