import KeyboardManager
from vapi import VimposerAPI

def init(v: VimposerAPI):
    map = v.km.map

    map("r",lambda : v.resize_window())
    map("u",lambda : v.change_track_up())
    map("d",lambda : v.change_track_down())
