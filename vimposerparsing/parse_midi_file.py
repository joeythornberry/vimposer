import MIDI
from _collections_abc import Callable
from vimposerparsing.MidiNoteOn import MidiNoteOn
from vimposerparsing.MidiNoteCollector import MidiNoteCollector
from vimposerparsing.MidiTrackAssigner import MidiTrackAssigner

def parse_midi_file(filename: str, save_note_callback: Callable[[int, int, int, int], int]):
    """Parse the given .mid file and pump the notes into save_note_callback."""

    midi_track_assigner = MidiTrackAssigner()
    midi_note_collector = MidiNoteCollector()

    midi_file = MIDI.MIDIFile(filename)
    midi_file.parse()

    for current_track_id, midi_track in enumerate(midi_file):
        midi_track.parse()
        for midi_event in midi_track:
            match midi_event.header & 240: # first 4 bits of header define event type
                case 0x90: # Note On
                    pitch = (int.from_bytes(midi_event.data, byteorder="big") & 0xff00) >> 8
                    #velocity = int.from_bytes(midi_event.data, byteorder="big") & 0xff
                    time = midi_event.time
                    midi_note_collector.push_note_on(pitch, MidiNoteOn(time))

                case 0x80: # Note Off
                    pitch = (int.from_bytes(midi_event.data, byteorder="big") & 0xff00) >> 8
                    note_on = midi_note_collector.pop_note_on(pitch)
                    start_time = note_on.start_time
                    end_time = midi_event.time
                    duration = end_time - start_time
                    channel = midi_event.channel
                    track = midi_track_assigner.get_track_id(current_track_id, channel)
                    save_note_callback(pitch, int(start_time/80), int(duration/80), track)
