from Location import Location
from NoteData import NoteData
from PixelData import PixelData
from Window import Window
from PixelList import PixelList
from Frontend import Frontend
from Screen import Screen

def get_color(track : int):
    return track

f = Frontend()
w = Window()
w.set_dimensions(1,20,1,20)
f.load_colors()
s = Screen(w,f,PixelList(),get_color)
l = Location(10,10)
s.refresh_location(l,5)

pd = PixelData()
pd.set_track(2)
pd.set_icon("p")
l = Location(10,11)
s.set_location(l,pd)
s.refresh_location(l,1)

pd = PixelData()
pd.set_track(2)
pd.set_icon("p")
l = Location(10,12)
s.set_location(l,pd)
s.remove_location(l,2)
s.refresh_location(l,2)

pd = PixelData()
pd.set_track(2)
pd.set_icon("p")
l = Location(10,13)
s.set_location(l,pd)
s.refresh_location(l,2)

n = NoteData(6,5,4)
s.set_note(n,1)
s.refresh_note(n,2)

n = NoteData(5,5,4)
s.set_note(n,1)
s.refresh_note(n,1)

n = NoteData(4,5,4)
s.set_note(n,1,c = True)
s.refresh_note(n,1)

n = NoteData(3,5,4)
s.set_note(n,1)
s.remove_note(n,1)
s.refresh_note(n,1)

n = NoteData(2,5,4)
s.set_note(n,1)
s.set_note(n,2)
s.refresh_note(n,2)

s.f.s.getch()
f.close()
