class TrackColorManager:
    """Handle a map of track ids to color ids, so we know what color each track should be."""
    track_to_color_map: dict[int, int]

    def __init__(self):
        """Init a TrackColorManager with an empty track-to-color dict."""
        self.track_to_color_map: dict[int, int] = {}

    def assign_track_color(self, track: int):
        """Generate a new color id and assign it to the given track."""
        taken_colors = list(self.track_to_color_map.values())
        color = 0 # just need to find a color id that isn't taken already
        while color in taken_colors:
            color += 1

        self.track_to_color_map[track] = color

    def free_track_color(self, track: int):
        """Delete a track-color mapping from the record."""
        del self.track_to_color_map[track]

    def get_track_color(self, track: int) -> int:
        """Return the color id that the given track is associated with."""
        return self.track_to_color_map[track]
