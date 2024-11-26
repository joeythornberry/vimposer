from vimposercore.VimposerAPI import VimposerAPI

def init(v: VimposerAPI):
    v.set_chars_per_quarter_note(12)

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

    v.km.map("H", lambda amount : v.shift_window_horizontal(-1 * amount))
    v.km.map("L", lambda amount : v.shift_window_horizontal(amount))
    v.km.map("J", lambda amount : v.shift_window_vertical(-1 * amount))
    v.km.map("K", lambda amount : v.shift_window_vertical(amount))

    v.km.map("tn",v.create_track)
    v.km.map("tk",v.change_track_up)
    v.km.map("tj",v.change_track_down)
    v.km.map("tx",v.delete_current_track)

    v.km.map("x",v.delete_cursor_note)

    v.km.map("i", v.shorten_cursor_note)
    v.km.map("o", v.lengthen_cursor_note)

    v.km.map("W", v.save)

    v.km.map("V", v.set_current_track_velocity)

    v.km.map("I", v.set_current_track_instrument)

    v.km.map("T", v.set_tempo)

