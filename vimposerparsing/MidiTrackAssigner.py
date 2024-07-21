class MidiTrackAssigner:
    raw_track_and_channel_to_track_map: dict[tuple[int,int], int]
    next_track_id: int

    def __init__(self):
        self.raw_track_and_channel_to_track_map = {}
        self.next_track_id = 0

    def get_track_id(self, raw_track: int, channel: int):
        """Return the parsed track that notes on this raw track and channel should go to.

        Creates a new track id if none exists.
        """
        existing_track_id = self.raw_track_and_channel_to_track_map.get((raw_track, channel), None)
        if existing_track_id != None:
            return existing_track_id
        else:
            new_id = self.next_track_id
            self.raw_track_and_channel_to_track_map[(raw_track, channel)] = new_id
            self.next_track_id += 1
            return new_id
