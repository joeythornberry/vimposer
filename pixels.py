class Drawable:
    """contains everything you need to 
    fill in a pixel for a note"""
    def __init__(self, char):
        self.char = char

class Pixel:
    def __init__(self):
        self.tracks = {}

    def set_drawable(self, track, d):
        self.tracks[track] = d

    def get_drawable(self, track):
        return self.tracks[track]
