class PixelData:
    """Represent a single (p,x) coordinate in a track.

    Attributes:
    cursor -- Should this pixel be drawn as a cursor pixel for this track?
    icon -- What kind of character should be drawn in this pixel for this track?
    track -- What track does this PixelData belong to? Background pixels have a track of -1.
    """
    cursor : bool = False
    icon : str
    track : int

    def __init__(self, icon: str = " ", track: int = -1, cursor: bool = False):
        """Init a PixelData with the given attributes."""

        self.icon = icon
        self.track = track
        self.cursor = cursor

    def set_icon(self, new_icon: str):
        """Set this PixelData's icon attribute to this string value"""
        self.icon = new_icon

    def set_cursor(self, new_cursor_value: bool):
        """Set this PixelData's cursor attribute to this bool value"""
        self.cursor = new_cursor_value

    def set_track(self, new_track: int):
        """Set this PixelData's track attribute to this int value"""
        self.track = new_track
