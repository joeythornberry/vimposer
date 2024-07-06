class PixelData:
    cursor : bool = False
    icon : str
    track : int

    def __init__(self,icon : str = " ", track : int = -1, cursor : bool = False):
        self.icon = icon
        self.track = track
        self.cursor = cursor

    def set_icon(self, i : str):
        self.icon = i

    def set_cursor(self, c : bool):
        self.cursor = c

    def set_track(self, t : int):
        self.track = t
