from vimposerparsing.MidiFileParseResult import MidiFileParseResult
from vimposerparsing.parse_midi_file import parse_midi_file

midi_file_parse_result: MidiFileParseResult = parse_midi_file("MIDI/quantized_delta_times.mid", 100)
assert(480 in midi_file_parse_result.delta_times) # quarter note is picked up
assert(960 in midi_file_parse_result.delta_times) # half note is picked up
assert(1920 in midi_file_parse_result.delta_times) # whole note gap is picked up

midi_file_parse_result: MidiFileParseResult = parse_midi_file("MIDI/unquantized_delta_times.mid", 100)
assert(480 in midi_file_parse_result.delta_times) # quarter note is picked up
assert(960 in midi_file_parse_result.delta_times) # half note is picked up
assert(1920 in midi_file_parse_result.delta_times) # whole note gap is picked up
print(midi_file_parse_result.delta_times)
