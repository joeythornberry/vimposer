from vimposermidi.Drawable import Drawable
from vimposermidi.PixelList import PixelList
from vimposermidi.PixelData import PixelData
from vimposermidi.NoteData import NoteData
from vimposermidi.Location import Location
from vimposermidi.MidiViewport import MidiViewport
from vimposermidi.VimposerFrontend import VimposerFrontend

class MidiWindow:
    """Control the display of Midi elements to the screen.

    Attributes:
    midi_viewport -- The MidiViewport that tells the MidiWindow how to write to the screen.
    frontend -- The Frontend that writes to the screen.
    pixel_list -- The PixelList that stores screen data.
    """
    midi_viewport: MidiViewport
    frontend: VimposerFrontend
    pixel_list: PixelList

    def __init__(self, midi_viewport: MidiViewport, frontend : VimposerFrontend, pixel_list : PixelList, get_track_color) -> None:
        """Init a MidiWindow, and then refresh the screen."""
        self.midi_viewport = midi_viewport
        self.frontend = frontend
        self.pixel_list = pixel_list
        self.get_track_color = get_track_color
        self.refresh_full_screen(0)
        self.draw_window_border()

    def get_locations(self, note_data: NoteData) -> list[Location]:
        """Translate a NoteData object into the Locations it contains."""
        return [Location(note_data.p, note_data.x+i) for i in range(note_data.l)]

    def refresh_location(self, location: Location, current_track: int):
        """Refresh a Location on the screen with the data stored in pixel_data."""
        y,x,onscreen = self.midi_viewport.translate_coords(location.p, location.x)
        if not onscreen:
            return

        pixel_data, icon_type = self.pixel_list.get_data(location.p, location.x, current_track)
        drawable = Drawable(pixel_data)
        drawable.set_type(icon_type)

        if icon_type != "background":
            drawable.set_color(self.get_track_color(pixel_data.track))

        drawable.set_line(y)
        drawable.set_char(x)

        self.frontend.paint_pixel(drawable)

    def refresh_note(self, note_data: NoteData, current_track: int):
        """Refresh a note on the screen with the data stored in pixel_data."""
        locs = self.get_locations(note_data)
        for location in locs:
            self.refresh_location(location, current_track)

    def refresh_full_screen(self, current_track : int):
        """Refresh all visible screen locations with the data stored in pixel_data."""
        for p,x in self.midi_viewport.locate_full_screen():
            self.refresh_location(Location(p,x), current_track)

    def draw_window_border(self):
        """Paint the MidiWindow border to the screen."""
        for y,x,icon in self.midi_viewport.yield_border():
            self.frontend.paint_ui_element(y,x,icon)

    def set_location(self, location: Location, pixel_data: PixelData):
        """Store the given PixelData to the given Location in pixel_list."""
        self.pixel_list.set_data(location.p, location.x, pixel_data.track, pixel_data)

    def remove_location(self, location: Location, track: int):
        """Remove the PixelData at location in track."""
        self.pixel_list.remove_data(location.p, location.x, track)

    def set_note(self, note_data: NoteData, track: int, is_cursor: bool = False):
        """Store the given note in pixel_list. Length must not be 0."""
        if note_data.l == 0:
            raise Exception(f"SCREEN ERROR: cannot set note of length 0 at position ({note_data.p},{note_data.x})")
        locations_to_set = self.get_locations(note_data)

        start = PixelData("note_start", track, is_cursor)
        self.set_location(locations_to_set[0],start)

        for i in range(1,len(locations_to_set)-1):
            middle = PixelData("note_middle", track, is_cursor)
            self.set_location(locations_to_set[i], middle)

        end = PixelData("note_end", track, is_cursor)
        self.set_location(locations_to_set[-1], end)

    def remove_note(self, note_data: NoteData, track: int):
        """Remove the given note from pixel_list."""
        for location in self.get_locations(note_data):
            self.remove_location(location,track)

    def shift_up(self, amount: int, track: int):
        """Shift the viewport up the given amount, and then refresh the screen.

        A negative amount will shift the viewport down.
        """
        self.midi_viewport.shift_up(amount)
        self.refresh_full_screen(track)

    def shift_across(self,amount : int, track: int):
        """Shift the viewport right the given amount, and then refresh the screen.

        A negative amount will shift the viewport left.
        """
        self.midi_viewport.shift_across(amount)
        self.refresh_full_screen(track)
