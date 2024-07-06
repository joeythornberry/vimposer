from PixelData import PixelData

class Pixel:
    def __init__(self):
        self.data : dict[int,PixelData] = {}

    def set_data(self, track, pd : PixelData):
        self.data[track] = pd

    def remove_data(self,track):
        del self.data[track]

    def get_data(self, track) -> tuple[PixelData,bool]:
        """Returns a PixelData and whether it is focused or not"""
        if track in self.data:
            return self.data[track], True
        else:
            return next(iter(self.data.values())), False
