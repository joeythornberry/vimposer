import KeyboardManager
from vapi import VimposerAPI

def init(v: VimposerAPI):
    map = v.km.map

    map("u",lambda : v.change_track(1))
    map("d",lambda : v.change_track(0))
