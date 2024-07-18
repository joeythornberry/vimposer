from vimposerparsing.MidiFileParseResult import MidiFileParseResult
from vimposerparsing.parse_midi_file import parse_midi_file

midi_file_parse_result: MidiFileParseResult = parse_midi_file("MIDI/quantized_delta_times.mid", 100)
print(midi_file_parse_result.delta_times)
assert(480 in midi_file_parse_result.delta_times) # quarter note is picked up
assert(960 not in midi_file_parse_result.delta_times) # half note is avoided as multiple
assert(1920 not in midi_file_parse_result.delta_times) # whole note gap is avoided as multiple
