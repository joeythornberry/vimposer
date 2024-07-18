from vimposerparsing.RawMidiSong import RawMidiSong
from vimposerparsing.SongMetadata import SongMetadata

class MidiFileParseResult:
    raw_midi_song: RawMidiSong
    song_metadata: SongMetadata
    delta_times: list[int]
