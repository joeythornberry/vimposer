from Pixel import Pixel
from PixelData import PixelData
from calculate_background_icon import calculate_background_icon

class PixelList:
    def __init__(self):
        self.pixels : dict[tuple[int,int],Pixel] = {}
    
    def set_data(self, p, x, track : int, pd : PixelData):
        if not (p,x) in self.pixels:
            self.pixels[(p,x)] = Pixel()
        self.pixels[(p,x)].set_data(track,pd)

    def get_data(self, p, x, current_track : int) -> tuple[PixelData,str]:
        if (p,x) not in self.pixels:
            pd = PixelData()
            pd.set_icon(calculate_background_icon(p,x))
            pd.set_track(-1)
            return pd, "background"
        pd, focused = self.pixels[(p,x)].get_data(current_track)
        t : str = "unfocused_track"
        if focused:
            t = "focused_track"
        return pd,t

    def remove_data(self, p, x, track : int):
        if (p,x) not in self.pixels:
            raise Exception(f"PixelList error: data at ({p,x}) on track {track} cannot be deleted because no pixel exists")
        self.pixels[(p,x)].remove_data(track)
        if len(self.pixels[(p,x)].data) == 0:
               del self.pixels[(p,x)]
