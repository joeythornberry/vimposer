from vimposermidi.Pixel import Pixel
from vimposermidi.PixelData import PixelData
from config.Background import is_measure_start, calculate_background_icon
from vimposermidi.BackgroundPixelManager import BackgroundPixelManager

class PixelList:
    """Store the Pixels that represent each (p,x) location

    Attributes:
    pixels -- a map of (p,x) pairs to Pixel objects
    """
    pixels: dict[tuple[int, int], Pixel]
    background_pixel_manager: BackgroundPixelManager;

    def __init__(self):
        """Init a PixelList with an empty pixels map"""
        self.pixels: dict[tuple[int, int], Pixel] = {}
        self.background_pixel_manager = BackgroundPixelManager()
    
    def set_data(self, p: int, x: int, track : int, data_to_set: PixelData):
        """Give data_to_set and track to the Pixel at (p,x)

        If there is no Pixel at (p,x), create one.
        """
        if not (p,x) in self.pixels:
            self.pixels[(p,x)] = Pixel()

        self.pixels[(p,x)].set_data(track,data_to_set)

    def get_data(self, p: int, x: int, current_track: int) -> tuple[PixelData, str]:
        """Get the PixelData and icon_type at (p,x) for the given track.

        Returns (fetched_data, icon_type). If there is no Pixel at (p,x), create and return 
        a background PixelData.
        """
        if (p,x) not in self.pixels:
            background_data = PixelData()
            background_data.set_icon(calculate_background_icon(p,x))
            background_data.set_track(-1)
            prev_x, prev_is_measure_start = self.background_pixel_manager.get_prev_data()
            pixel_is_measure_start = is_measure_start(x, prev_x, prev_is_measure_start)
            self.background_pixel_manager.set_prev_data(x, pixel_is_measure_start)
            icon_type: str = "measure_start" if pixel_is_measure_start else "background"
            return background_data, icon_type

        fetched_data: PixelData = self.pixels[(p,x)].get_data(current_track)

        icon_type: str = "unfocused_track"
        if fetched_data.track == current_track:
            icon_type = "focused_track"

        return fetched_data, icon_type

    def remove_data(self, p: int, x: int, track_to_delete_from: int):
        """Remove the PixelData at (p,x) for the given track.

        Throw an error if there is no Pixel at (p,x).
        If this action empties the Pixel at (p,x), delete it.
        """
        if (p,x) not in self.pixels:
            raise Exception(f"PixelList error: data at ({p,x}) cannot be deleted because no pixel exists")

        self.pixels[(p,x)].remove_data(track_to_delete_from)

        if len(self.pixels[(p,x)].data) == 0:
               del self.pixels[(p,x)]
