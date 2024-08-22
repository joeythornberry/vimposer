from vimposermidi.TrackMidiManager import TrackMidiManager
from vimposersaving.TrackMidiEventsModel import TrackMidiEventsModel
from vimposersaving.BinaryWrites import *

def save_midi_file(filename: str, track_midi_manager: TrackMidiManager, tempo: int):

    TICKS_PER_CHAR = 40
    CHARS_PER_QUARTER_NOTE = 12

    write_counter = WriteCounter()

    tracks = track_midi_manager.get_tracks_list()

    with open(filename, "wb") as midifile:

        for byte in "MThd":
            write_8(midifile, ord(byte), write_counter)

        write_16(midifile, 0, write_counter)
        write_16(midifile, 6, write_counter) # header length

        write_16(midifile, 1, write_counter) # format

        write_16(midifile, len(tracks), write_counter) # ntrks

        write_16(midifile, TICKS_PER_CHAR * CHARS_PER_QUARTER_NOTE, write_counter) # division
        
        assert write_counter.num_writes == 14, f"wrote incorrect number of bytes ({write_counter.num_writes}) to MIDI header.\nLog:{write_counter.log}"

        for (trackid, track) in enumerate(tracks):
            track_midi_events_model = TrackMidiEventsModel(track, trackid)

            if trackid == 0:
                track_midi_events_model.set_tempo(tempo)

            track_midi_events_model.write(midifile, TICKS_PER_CHAR, write_counter)
