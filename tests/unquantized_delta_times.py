from vimposerparsing.MidiFileParseResult import MidiFileParseResult
from vimposerparsing.parse_midi_file import parse_midi_file

midi_file_parse_result: MidiFileParseResult = parse_midi_file("MIDI/unquantized_delta_times.mid", 200)
print(midi_file_parse_result.delta_times)
assert(480 in midi_file_parse_result.delta_times) # quarter note is picked up
assert(1790 not in midi_file_parse_result.delta_times) # short whole note gap is ignored as multiple
