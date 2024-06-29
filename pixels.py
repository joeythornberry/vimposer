class Drawable:
    """contains everything you need to 
    fill in a pixel for a note"""
    def __init__(self, icon, color=1):
        self.icon = icon
        self.color = color

class Pixel:
    def __init__(self):
        self.tracks = {}

    def set_drawable(self, track, d : Drawable):
        self.tracks[track] = d

    def remove_drawable(self,track):
        del self.tracks[track]

    def get_drawable(self, track) -> tuple[Drawable,bool]:
        if track in self.tracks:
            return self.tracks[track], True
        else:
            return Drawable('x'), False

class PixelList:
    def __init__(self):
        self.pixels : dict[tuple[int,int],Pixel] = {}
    
    def set_drawable(self, p, x, track : int, d : Drawable):
        if not (p,x) in self.pixels:
            self.pixels[(p,x)] = Pixel()
        self.pixels[(p,x)].set_drawable(track,d)

    def get_drawable(self, p, x, track : int) -> tuple[Drawable,bool]:
        if (p,x) not in self.pixels:
            return Drawable('X'), False
        return self.pixels[(p,x)].get_drawable(track)

    def remove_drawable(self, p, x, track : int):
        if (p,x) not in self.pixels:
            raise Exception(f"PixelList error: drawable at ({p,x}) on track {track} cannot be deleted because no pixel exists")
        self.pixels[(p,x)].remove_drawable(track)
