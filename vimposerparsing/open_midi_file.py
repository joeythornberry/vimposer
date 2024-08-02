from collections.abc import Callable

def open_midi_file(filename: str, save_note: Callable[[int, int, int, int], None], chars_per_quarter_note: int):
    from ctypes import CFUNCTYPE, c_int8, c_int32, cdll, CDLL, c_wchar_p
    from c.load_midi_file import load_midi_file 

    @CFUNCTYPE(None, c_int8, c_int32, c_int8, c_int8)
    def save_note_callback(p: int, x: int, l: int, track: int):
        save_note(p, x, l, track)

    load_midi_file(filename, save_note_callback, chars_per_quarter_note)
    library_name = "./c/libmidiloader.so"
    cdll.LoadLibrary(library_name)
    libmidiloader = CDLL(library_name)

    filename_wchar_p = c_wchar_p(filename)
    libmidiloader.export_midi_file(filename_wchar_p, save_note_callback, chars_per_quarter_note)

