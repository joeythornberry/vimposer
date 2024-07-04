import KeyboardManager
from vapi import VimposerAPI

def init(v: VimposerAPI):
    map = v.km.map

    map("u",lambda : v.change_track_up())
    map("d",lambda : v.change_track_down())
    map("k",lambda : v.move_cursor_up())
    map("j",lambda : v.move_cursor_down())
    map("h",lambda : v.move_cursor_left())
    map("l",lambda : v.move_cursor_right())
