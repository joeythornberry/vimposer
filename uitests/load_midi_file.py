from config.DefaultFrontend import Frontend 
from vimposercore.VimposerAPI import VimposerAPI
from vimposercore.KeyboardManager import KeyboardManager

from vimposerparsing.TicksPerCharCalculator import TicksPerCharCalculator
from vimposerparsing.parse_midi_file import parse_midi_file

v = VimposerAPI(Frontend())

v.km.map("F",v.make_note_right)
v.km.map("A",v.make_note_left)
v.km.map("S",v.make_note_down)
v.km.map("D",v.make_note_up)

v.km.map("s",v.move_cursor_down)
v.km.map("d",v.move_cursor_up)
v.km.map("a",v.move_cursor_left)
v.km.map("f",v.move_cursor_right)

v.km.map("k",v.move_note_up)
v.km.map("j",v.move_note_down)
v.km.map("h",v.move_note_left)
v.km.map("l",v.move_note_right)

v.km.map("H", lambda : v.shift_window_horizontal(-1))
v.km.map("L", lambda : v.shift_window_horizontal(1))
v.km.map("J", lambda : v.shift_window_vertical(-1))
v.km.map("K", lambda : v.shift_window_vertical(1))

v.km.map("tn",v.create_track)
v.km.map("tk",v.change_track_up)
v.km.map("tj",v.change_track_down)
v.km.map("tx",v.delete_current_track)

v.km.map("x",v.delete_cursor_note)

v.km.map("i", lambda : v.shorten_cursor_note(1))
v.km.map("o", lambda : v.lengthen_cursor_note(1))

def save_note_callback(p: int, x: int, l: int, track: int) -> int:
    if len(v.s.track_midi_manager.tracks) <= track:
        v.create_track()
        return save_note_callback(p, x, l, track)
    else:
        v.s.new_note(p, x, l, track, False)
        return 0

parse_midi_file(
        "MIDI/bwv1052a.mid",
        save_note_callback,
        TicksPerCharCalculator(12)
        )

v.km.listen(v.s.midi_window.frontend.s.getkey)
v.s.midi_window.frontend.close()
