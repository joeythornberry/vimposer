from vimposermidi.TrackMidi import TrackMidi
from vimposermidi.TrackColorManager import TrackColorManager

class TrackMidiManager:
    """Coordinate TrackMidis and keep track of which one is focused."""
    tracks : dict[int,TrackMidi]
    current_track : int
    track_color_manager : TrackColorManager
    new_track_id : int

    def __init__(self, num_colors: int):
        """Init a TrackMidiManager with no tracks in it."""
        self.tracks = {}
        self.current_track = 0
        self.new_track_id = -1
        self.track_color_manager = TrackColorManager(num_colors)

    def __repr__(self):
        return str(self.tracks)

    def has_note(self, p: int, x: int, l: int, track: int) -> bool:
        """Return True if the given track contains a note of the given p, x, and l."""
        if track not in self.tracks:
            return False
        return self.tracks[track].has_note(p, x, l)

    def current(self) -> int:
        """Return the currently focused track."""
        return self.current_track

    def track_has_more_than_one_note(self, track: int) -> bool:
        """Return True if the given track has more than one note in it."""
        return self.tracks[track].has_more_than_one_note()

    def change_track_to(self, new_t: int):
        """Make the given track the current track."""
        if new_t in self.tracks:
            self.current_track = new_t
        else: 
            raise Exception(f"TRACKLIST ERROR: cannot change to track {new_t} because it does not exist")

    def get_up_track(self) -> int:
        """Return the track id of the track with the next highest track id (wrap around to 0 if current track has the highest id)."""
        all_track_ids = list(self.tracks.keys())
        next_current_track = all_track_ids.index(self.current_track) + 1 
        if next_current_track == len(all_track_ids):
            return all_track_ids[0]
        return all_track_ids[next_current_track]

    def get_down_track(self) -> int:
        """Return the track id of the track with the next lowest track id (wrap around to len(tracks)-1 if current track has the lowest id)."""
        all_track_ids = list(self.tracks.keys())
        next_current_track = all_track_ids.index(self.current_track) - 1 
        if next_current_track == -1:
            return all_track_ids[len(all_track_ids) - 1]
        return all_track_ids[next_current_track]

    def create_track(self) -> int:
        """Create a new track with a unique id. Returns id of created track, if you need it."""
        self.new_track_id += 1
        self.track_color_manager.assign_track_color(self.new_track_id)
        self.tracks[self.new_track_id] = TrackMidi()
        return self.new_track_id

    def delete_track(self, track: int):
        """Delete the track with the current track id."""
        del self.tracks[track]

    def only_one_track_exists(self) -> bool:
        """Return True if only one track exists in this TrackMidiManager."""
        return len(self.tracks.keys()) == 1

    def add_note(self, p: int, x: int, l: int, note_track: int):
        """Add a note with the given attributes to the given track."""
        self.tracks[note_track].add_note(p, x, l)

    def delete_note(self, p: int, x: int, note_track: int):
        """Delete the note with the given coords from the given track."""
        self.tracks[note_track].delete_note(p, x)

    def get_length(self, p: int, x: int, note_track: int) -> int:
        """Get the length of the note at the given coords on the given track."""
        return self.tracks[note_track].get_note_length(p, x)

    def calculate_closest_chord(self, x: int, track: int) -> int:
        """Return the closest occupied x-value to the given x-value."""
        return self.tracks[track].calculate_closest_chord(x)
        
    def generate_new_cursor(self, old_p: int, old_x: int, track: int) -> tuple[int, int]:
        """Return the coords of the best candidate for the new cursor note based on the given coords and track."""
        new_x = self.calculate_closest_chord(old_x,track)
        new_p = self.tracks[track].calculate_closest_pitch(old_p,new_x)
        return new_p, new_x

    def find_cursor_up_target(self, current_p: int, current_x: int):
        """Return the note that the cursor should go to if it moves up (if there is none, return the given coords)."""
        return self.tracks[self.current_track].find_cursor_up_target(current_p, current_x)

    def find_cursor_down_target(self,current_p: int, current_x: int):
        """Return the note that the cursor should go to if it moves down (if there is none, return the given coords)."""
        return self.tracks[self.current_track].find_cursor_down_target(current_p, current_x)

    def find_cursor_left_target(self, current_p: int, current_x: int):
        """Return the note that the cursor should go to if it moves left (if there is none, return the given coords)."""
        return self.tracks[self.current_track].find_cursor_left_target(current_p, current_x)

    def find_cursor_right_target(self, current_p: int, current_x: int):
        """Return the note that the cursor should go to if it moves right (if there is none, return the given coords)."""
        return self.tracks[self.current_track].find_cursor_right_target(current_p, current_x)

    def get_track_notes_list(self, track: int):
        """Return a list in (p,x) tuple form of all the notes in the current track."""
        return self.tracks[track].get_notes_list()

    def set_note_length(self, p: int, x: int, l: int, track: int):
        """Set the length of the note at the given coords on the given track to the given value."""
        self.tracks[track].set_note_length(p, x, l)

    def does_note_fit(self, p: int, x: int, l: int, current_x: int, track: int) -> bool:
        """Return True if a note with the given attributes could fit on the current track. Ignore the note at (p, current_x)."""
        return self.tracks[track].does_note_fit(p, x, l, current_x)

    def get_track_color(self, track: int) -> int:
        """Return the color id that the given track should have."""
        return self.track_color_manager.get_track_color(track)
