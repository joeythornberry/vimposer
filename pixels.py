class Drawable:
    def __init__(self, icon):
        self.icon = icon
        self.cursor = False

    def set_cursor(self,c : bool):
        self.cursor = c

    def set_color(self,c : int):
        self.color = c

    def set_track(self,t : int):
        self.track = t

class Pixel:
    def __init__(self):
        self.tracks = {}

    def set_drawable(self, track, d : Drawable):
        d.set_track(track)
        self.tracks[track] = d

    def remove_drawable(self,track):
        del self.tracks[track]

    def get_drawable(self, track) -> Drawable:
        if track in self.tracks:
            d = self.tracks[track]
        else:
            d = next(iter(self.tracks.values()))
        return d

class PixelList:
    def __init__(self):
        self.pixels : dict[tuple[int,int],Pixel] = {}
    
    def set_drawable(self, p, x, track : int, d : Drawable):
        if not (p,x) in self.pixels:
            self.pixels[(p,x)] = Pixel()
        self.pixels[(p,x)].set_drawable(track,d)

    def get_drawable(self, p, x, current_track : int):
        if (p,x) not in self.pixels:
            return False
        d = self.pixels[(p,x)].get_drawable(current_track)
        return d

    def remove_drawable(self, p, x, track : int):
        if (p,x) not in self.pixels:
            raise Exception(f"PixelList error: drawable at ({p,x}) on track {track} cannot be deleted because no pixel exists")
        self.pixels[(p,x)].remove_drawable(track)
