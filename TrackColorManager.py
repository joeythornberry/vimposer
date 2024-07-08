class TrackColorManager:
    track_to_color_map : dict[int,int]

    def __init__(self):
        self.track_to_color_map = {}

    def assign_track_color(self, t : int):
        if not self.track_to_color_map:
            self.track_to_color_map[t] = 0
            return 0
        taken_colors = list(self.track_to_color_map.values())

        color = 0
        while color in taken_colors:
            color += 1

        self.track_to_color_map[t] = color
        return color

    def free_track_color(self, t : int):
        del self.track_to_color_map[t]

    def get_track_color(self, t : int) -> int:
        return self.track_to_color_map[t]
