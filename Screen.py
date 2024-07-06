from Drawable import Drawable
from PixelList import PixelList
from PixelData import PixelData
from NoteData import NoteData
from Location import Location
from Window import Window
from Frontend import Frontend

class Screen:
    w : Window
    f : Frontend
    p : PixelList

    def __init__(self,w : Window, f : Frontend, p : PixelList, get_track_color) -> None:
        self.w = w
        self.f = f
        self.p = p
        self.get_track_color = get_track_color
        self.refresh_full_screen(0)
        self.draw_window_border()

    def get_locations(self,n : NoteData) -> list[Location]:
        return [Location(n.p,n.x+i) for i in range(n.l)]

    def refresh_location(self, l : Location, current_track: int):
        y,x,onscreen = self.w.translate_coords(l.p,l.x)
        if not onscreen:
            return

        pd,type = self.p.get_data(l.p,l.x,current_track)
        d = Drawable(pd)
        d.set_type(type)

        if type != "background":
            d.set_color(self.get_track_color(pd.track))

        d.set_y(y)
        d.set_x(x)

        self.f.paint_pixel(d)

    def refresh_note(self, n : NoteData, current_track : int):
        locs = self.get_locations(n)
        for l in locs:
            self.refresh_location(l,current_track)

    def refresh_full_screen(self, current_track : int):
        for p,x in self.w.locate_full_screen():
            l = Location(p,x)
            self.refresh_location(l, current_track)

    def draw_window_border(self):
        for y,x,icon in self.w.yield_border():
            self.f.paint_ui_element(y,x,icon)

    def set_location(self, l : Location, pd : PixelData):
        self.p.set_data(l.p,l.x,pd.track,pd)

    def remove_location(self, l : Location, t : int):
        self.p.remove_data(l.p,l.x,t)

    def set_note(self,n : NoteData, t : int, c : bool = False):
        locs = self.get_locations(n)
        start = PixelData("[",t,c)
        self.set_location(locs[0],start)

        for i in range(1,len(locs)-1):
            middle = PixelData("_",t,c)
            self.set_location(locs[i],middle)

        end = PixelData("]",t,c)
        self.set_location(locs[-1],end)

    def remove_note(self,n : NoteData, t : int):
        for l in self.get_locations(n):
            self.remove_location(l,t)
