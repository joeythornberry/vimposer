import KeyboardManager
from VimposerAPI import VimposerAPI

def init(v: VimposerAPI):
    map = v.km.map

    map("p",v.sound)
    map("n",v.make_note)
