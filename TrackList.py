from Track import Track
from Note import Note
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
        self.tracks[self.new_track_id] = Track(self.tcm.assign_track_color(self.new_track_id))
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
        t = self.tracks[note_track]
        if x not in t.chords:
            raise Exception(f"TRACKLIST ERROR: cannot get length of note ({p},{x}) because it does not exist in track {note_track}")
        c = t.chords[x]
        if p not in c.notes:
            raise Exception(f"TRACKLIST ERROR: cannot get length of note ({p},{x}) because it does not exist in chord {x} on track {note_track}")
        l =  self.tracks[note_track].chords[x].notes[p].l
        return l

    def calculate_closest_chord(self,old_x,track : int):
        t = self.tracks[track]
        if old_x in t.chords:
            return old_x
        k = list(t.chords.keys())
        closest = 500000000
        closest_distance = 500000000
        for i,x in enumerate(k):
            distance = abs(old_x - x)
            if distance < closest_distance:
                closest = i
                closest_distance = distance

        if closest_distance > 100000000:
            raise Exception(f"TRACK ERROR: looking for closest chord in track {self.current_track} but there are no chords in it (or your track is very long)")

        return k[closest] 
        
    def generate_new_cursor(self,old_p,old_x,track = -1):
        if track == -1:
            track = self.t
        if len(list(self.tracks[track].chords.keys())) == 0:
            raise Exception("TRACKLIST ERROR: cannot generate cursor for track {self.t} because it has no notes")
        new_x = self.calculate_closest_chord(old_x,track)
        new_p = self.calculate_closest_pitch(old_p,new_x,track)
        return new_p,new_x

    def find_cursor_up_target(self,p,x):
        c = self.tracks[self.t].chords[x]
        k = list(c.notes.keys())
        k.sort()
        i = k.index(p)
        if i < len(k) - 1:
            new_p = k[i+1]
            return new_p, x 
        return p,x

    def find_cursor_down_target(self,p,x):
        c = self.tracks[self.t].chords[x]
        k = list(c.notes.keys())
        k.sort()
        i = k.index(p)
        if i > 0 :
            new_p = k[i-1]
            return new_p, x 
        return p,x

    def calculate_closest_pitch(self,old_p,new_x,track):
        c = self.tracks[track].chords[new_x]
        closest = 500
        closest_distance = 500
        k = list(c.notes.keys())
        for i,p in enumerate(k):
            distance = abs(old_p - p)
            if distance < closest_distance:
                closest = i
                closest_distance = distance

        if closest_distance > 127:
            raise Exception(f"CHORD ERROR: looking for closest pitch in chord {new_x} but there are no notes in it")

        return k[closest] 

    def find_cursor_horizontal_target(self,p,x,move_left : bool):
        t = self.tracks[self.t]
        k = list(t.chords.keys())
        k.sort()
        i = k.index(x)

        can_move = (move_left and i > 0) or (not move_left and i < len(k) - 1)
        if can_move:
            if move_left:
                new_x = k[i-1]
            else:
                new_x = k[i+1]
            new_p = self.calculate_closest_pitch(p,new_x,self.t)
            return new_p, new_x
        return p,x

    def find_cursor_left_target(self,p,x):
        return self.find_cursor_horizontal_target(p,x,True)

    def find_cursor_right_target(self,p,x):
        return self.find_cursor_horizontal_target(p,x,False)

    def find_note_up_location(self,p,x):
        return p + 1,x

    def find_note_down_location(self,p,x):
        return p - 1,x

    def find_note_left_location(self,p,x):
        return p,x - 1

    def find_note_right_location(self,p,x):
        return p,x + 1

    def does_note_fit(self,p,x,l,cur_x,track : int) -> bool:
        tr = self.tracks[track]
        for chord_x,c in tr.chords.items():
            if c.pitch_occupied(p):
                if chord_x == cur_x:
                    if cur_x != x:
                        continue # don't want the note itself to block itself from moving
                if chord_x <= x:
                    if chord_x + c.notes[p].l > x:
                        return False
                if chord_x > x and chord_x < x + l:
                    return False
        if x < 0 or p < 0 or p > 127:
            return False

        return True

    def get_track_notes_list(self, track : int):
        return self.tracks[track].get_notes_list()

    def set_note_length(self,p,x,l,track : int):
        self.tracks[track].set_note_length(p,x,l)
