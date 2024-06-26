class Drawable:
    """contains everything you need to 
    fill in a pixel for a note"""
    def __init__(self, icon, color=1):
        self.icon = icon
        self.color = color

class Pixel:
    def __init__(self):
        self.tracks = {}

    def set_drawable(self, track, d):
        self.tracks[track] = d

    def get_drawable(self, track) -> tuple[Drawable,bool]:
        if track in self.tracks:
            return self.tracks[track], True
        else:
            return Drawable('x'), False

class PixelList:
    def __init__(self):
        self.pixels = {}
    
    def set_drawable(self, p, x, track : int, d : Drawable):
        if not (p,x) in self.pixels:
            self.pixels[(p,x)] = Pixel()
        self.pixels[(p,x)].set_drawable(track,d)

    def get_drawable(self, p, x, track : int) -> tuple[Drawable,bool]:
        if (p,x) not in self.pixels:
            return Drawable('X'), False
        return self.pixels[(p,x)].get_drawable(track)
