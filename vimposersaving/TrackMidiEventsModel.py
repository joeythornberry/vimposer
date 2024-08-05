from io import BufferedReader, BufferedWriter
from vimposermidi.Note import Note
from vimposermidi.TrackMidi import TrackMidi
from vimposersaving.BinaryWrites import *
import struct

class NoteOnEvent:
    p: int

    def __repr__(self) -> str:
        return f"{self.p}"

class NoteOffEvent:
    p: int

    def __repr__(self) -> str:
        return f"{self.p}"

class EventChord:
    """Represent a group of note_on and note_off events that occur at the same time."""
    note_ons: list[NoteOnEvent]
    note_offs: list[NoteOffEvent]

    def __init__(self):
        self.note_ons = []
        self.note_offs = []

    def __repr__(self) -> str:
        return f"offs: {[off for off in self.note_offs]} ons: {[on for on in self.note_ons]}"

class TrackMidiEventsModel:
    """Represent a track of MIDI notes as a stream of events, for saving in a MIDI file."""

    event_chords: dict[int, EventChord]
    track_length: int

    def __init__(self, track: TrackMidi):
        self.event_chords = {}
        self.track_length = 0
        for p, x, l in track.get_notes_list():
            self.record_note(p, x, l)

    def record_note(self, p: int, x: int, l: int):
        """Internally record a note as its On and Off event components."""


        if x not in self.event_chords:
            self.event_chords[x] = EventChord()

        note_on = NoteOnEvent()
        note_on.p = p
        self.event_chords[x].note_ons.append(note_on)

        if x + l not in self.event_chords:
            self.event_chords[x + l] = EventChord()

        note_off = NoteOffEvent()
        note_off.p = p
        self.event_chords[x + l].note_offs.append(note_off)

    def has_note(self, p: int, x: int, l: int) -> tuple[bool, str]:
        """Return True if the note_on and note_off events for the given note exist in this model."""
        if x not in self.event_chords or p not in [note_on.p for note_on in self.event_chords[x].note_ons]:
            return False, "Could not find note_on"

        if x + l not in self.event_chords or p not in [note_off.p for note_off in self.event_chords[x + l].note_offs]:
            return False, "Could not find note_off"

        return True, ""

    
    def write(self, file: BufferedWriter, ticks_per_char):

        write_counter = WriteCounter()

        for byte in "MTrk":
            write_8(file, ord(byte), write_counter)
        # remember where the track length is stored so we can go back and set it to the correct value
        length_position = file.tell()
        print("lenpos:",length_position)
        write_16(file, 0, write_counter) # put a placeholder length in for now

        write_counter.reset()

        for x, event_chord in self.event_chords.items():
            time = x * ticks_per_char
            write_variable_length_number(file, time, write_counter)

            for note_off in event_chord.note_offs:
                write_8(file, 0x90, write_counter) # note_off code i think
                write_8(file, note_off.p, write_counter) 
                write_8(file, 0, write_counter) # velocity

            for note_on in event_chord.note_ons:
                write_8(file, 0x80, write_counter) # note_on code i think
                write_8(file, note_on.p, write_counter) 
                write_8(file, 100, write_counter) # velocity

        # end-of-track meta event
        write_8(file, 0xff, write_counter)
        write_8(file, 0x2f, write_counter)
        write_8(file, 0x00, write_counter)

        # go back and set the track length to the correct value
        file.seek(length_position, 0) 
        write_16(file, write_counter.num_writes, write_counter)

        file.seek(0, 2) # return the cursor to the end of the file

