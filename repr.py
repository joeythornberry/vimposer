import track

t = track.Track()
t.extend_to(10)
t.add_note(5,5,track.Note(5))
print(t)
