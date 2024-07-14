from vimposermidi.PixelData import PixelData

class Pixel:
    """Hold one PixelData for each track given, and return correct one for current track.

    Track information is stored both in the PixelData itself and in the Pixel's track-to-PixelData map.
    """

    def __init__(self):
        """Inits PixelData with empty data"""
        self.data : dict[int, PixelData] = {}

    def set_data(self, track: int, data_to_add: PixelData):
        """Give this Pixel a PixelData with the given track."""
        self.data[track] = data_to_add

    def remove_data(self, track: int):
        """Delete the PixelData in this Pixel with the given track."""
        del self.data[track]

    def get_data(self, track: int) -> PixelData:
        """Return a PixelData, preferentially one from the given track if present.

        If the given track is not represented in this Pixel, return a PixelData from a random track.
        """
        if track in self.data:
            return self.data[track]
        else:
            return next(iter(self.data.values()))
