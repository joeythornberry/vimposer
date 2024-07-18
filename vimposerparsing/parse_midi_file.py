from vimposerparsing.RawMidiSong import RawMidiSong
from vimposerparsing.SongMetadata import SongMetadata
from vimposerparsing.MidiFileParseResult import MidiFileParseResult
from vimposerparsing.assign_delta_time import assign_delta_time
import MIDI

def parse_midi_file(filename: str, tolerance: int) -> MidiFileParseResult:
    """Parse the given .mid file and return the raw Midi and metadata."""

    delta_times: list[int] = []

    midi_file = MIDI.MIDIFile(filename)
    midi_file.parse()

    for midi_track in midi_file:
        midi_track.parse()
        last_timestamp = 0
        for midi_event in midi_track:
            new_delta_time = midi_event.time - last_timestamp
            processed_new_delta_time, record_new_delta_time = assign_delta_time(delta_times, new_delta_time, tolerance)
            if record_new_delta_time:
                delta_times.append(processed_new_delta_time)
            last_timestamp = midi_event.time
            
    midi_file_parse_result = MidiFileParseResult()
    midi_file_parse_result.delta_times = delta_times

    return midi_file_parse_result

