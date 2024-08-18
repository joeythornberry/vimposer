import sys
import MIDI

midifile = MIDI.MIDIFile(sys.argv[1])
midifile.parse()
print(midifile)
