from ctypes import *

@CFUNCTYPE(c_int, c_int, c_int, c_int, c_int)
def save_note(p: int, x: int, l: int, track: int):
    print(f"saving note {p=} {x=} {l=} {track=}")
    return 0

def load_midi_file(filename: str, save_note):
    library_name = "./libmidiloader.so"
    cdll.LoadLibrary(library_name)
    libmidiloader = CDLL(library_name)

    filename_wchar_p = c_wchar_p(filename)
    result = libmidiloader.parse_midi_file(filename_wchar_p, save_note)

if __name__ == "__main__":
    load_midi_file("../MIDI/d_minor_scale.mid", save_note)
