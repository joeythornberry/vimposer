from PixelList import PixelList
from NoteData import NoteData
from Location import Location

class Screen:
    def get_locations(self,n : NoteData):
        for i in range(n.l):
            yield Location(n.p,n.x+i)

