from ctypes import CFUNCTYPE, c_int8, c_int32

from c.load_midi_file import load_midi_file 

from sys import argv

@CFUNCTYPE(None, c_int8, c_int32, c_int32, c_int8)
def save_note_callback(p: int, x: int, l: int, track: int):
    print(f"saving note {p=} {x=} {l=} {track=}")

load_midi_file(
        f"MIDI/{argv[1]}",
        save_note_callback
        )
