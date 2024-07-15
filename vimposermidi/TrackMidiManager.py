from vimposermidi.TrackMidi import TrackMidi
from vimposermidi.TrackColorManager import TrackColorManager

class TrackMidiManager:
    tracks : dict[int,TrackMidi]
    t : int
    tcm : TrackColorManager
    new_track_id : int

    def __init__(self, num_colors: int):
        self.tracks = {}
        self.t = 0
        self.new_track_id = -1
        self.tcm = TrackColorManager(num_colors)

    def __repr__(self):
        return str(self.tracks)

    def current(self) -> int:
        return self.t

    def track_has_more_than_one_note(self,track : int) -> bool:
        return self.tracks[track].has_more_than_one_note()

    def change_track_to(self,new_t : int):
        if new_t in self.tracks:
            self.t = new_t
        else: 
            raise Exception(f"TRACKLIST ERROR: cannot change to track {new_t} because it does not exist")

    def get_up_track(self):
        ts = list(self.tracks.keys())
        i = ts.index(self.t) + 1 
        if i == len(ts):
            return ts[0]
        return ts[i]

    def get_down_track(self):
        ts = list(self.tracks.keys())
        i = ts.index(self.t) - 1 
        if i == -1:
            return ts[len(ts) - 1]
        return ts[i]

    def create_track(self):
        self.new_track_id += 1
        self.tcm.assign_track_color(self.new_track_id)
        self.tracks[self.new_track_id] = TrackMidi()
        return self.new_track_id

    def delete_track(self, track : int):
        del self.tracks[track]

    def only_one_track_exists(self) -> bool:
        return len(self.tracks.keys()) == 1

    def add_note(self,p,x,l,note_track : int):
        self.tracks[note_track].add_note(p,x,l)

    def delete_note(self,p,x,note_track : int):
        self.tracks[note_track].delete_note(p,x)

    def get_length(self,p,x,note_track : int) -> int:
        return self.tracks[note_track].get_note_length(p, x)

    def calculate_closest_chord(self,old_x,track : int):
        return self.tracks[track].calculate_closest_chord(old_x)
        
    def generate_new_cursor(self,old_p,old_x,track):
        new_x = self.calculate_closest_chord(old_x,track)
        new_p = self.tracks[track].calculate_closest_pitch(old_p,new_x)
        return new_p,new_x

    def find_cursor_up_target(self, current_p: int, current_x: int):
        return self.tracks[self.t].find_cursor_up_target(current_p, current_x)

    def find_cursor_down_target(self,current_p: int, current_x: int):
        return self.tracks[self.t].find_cursor_down_target(current_p, current_x)

    def find_cursor_left_target(self,p,x):
        return self.tracks[self.t].find_cursor_left_target(p, x)

    def find_cursor_right_target(self,p,x):
        return self.tracks[self.t].find_cursor_right_target(p, x)

    def find_note_up_location(self,p,x):
        return p + 1,x

    def find_note_down_location(self,p,x):
        return p - 1,x

    def find_note_left_location(self,p,x):
        return p,x - 1

    def find_note_right_location(self,p,x):
        return p,x + 1

    def get_track_notes_list(self, track : int):
        return self.tracks[track].get_notes_list()

    def set_note_length(self,p,x,l,track : int):
        self.tracks[track].set_note_length(p,x,l)

    def does_note_fit(self, p: int, x: int, l:int, current_x: int, track: int) -> bool:
        return self.tracks[track].does_note_fit(p, x, l, current_x)