from Track import Track
from TrackColorManager import TrackColorManager
class TrackList:
    tracks : dict[int,Track]
    t : int
    tcm : TrackColorManager
    new_track_id : int

    def __init__(self):
        self.tracks = {}
        self.t = 0
        self.new_track_id = -1
        self.tcm = TrackColorManager()

    def __repr__(self):
        return str(self.tracks)

    def current(self) -> int:
        return self.t

    def change_track_to(self,new_t : int):
        if new_t in self.tracks:
            self.t = new_t
        else: 
            raise Exception(f"TRACKLIST ERROR: cannot change to track {new_t} because it does not exist")

    def create_track(self):
        self.new_track_id += 1
        self.tracks[self.new_track_id] = Track(self.tcm.assign_track_color(self.new_track_id))
        return self.new_track_id

    def add_note(self,p,x,l,note_track : int):
        self.tracks[note_track].add_note(p,x,l)

    def delete_note(self,p,x,note_track : int):
        self.tracks[note_track].delete_note(p,x)
