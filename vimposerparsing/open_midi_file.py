from collections.abc import Callable
import os.path

def open_midi_file(filename: str, save_note: Callable[[int, int, int, int, int, int], None], save_tempo: Callable[[int], None], chars_per_quarter_note: int) -> int:
    from ctypes import CFUNCTYPE, c_int8, c_int32, cdll, CDLL, c_wchar_p
    from c.load_midi_file import load_midi_file 

    @CFUNCTYPE(None, c_int8, c_int32, c_int8, c_int8, c_int8, c_int8)
    def save_note_callback(p: int, x: int, l: int, track: int, velocity: int, instrument: int):
        save_note(p, x, l, track, velocity, instrument)

    @CFUNCTYPE(None, c_int32)
    def save_tempo_callback(new_tempo: int):
        save_tempo(new_tempo)

    library_name = f"{os.path.dirname(os.path.abspath(__file__))}/../c/libmidiloader.so"
    cdll.LoadLibrary(library_name)
    libmidiloader = CDLL(library_name)

    filename_wchar_p = c_wchar_p(filename)
    ticks_per_char = libmidiloader.export_midi_file(filename_wchar_p, save_note_callback, save_tempo_callback, chars_per_quarter_note)
    return ticks_per_char

