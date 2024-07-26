#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <wchar.h>

#include "MidiFile.h"
#include "BinaryDebug.h"
#include "Conversions.h"
#include "VariableLength.h"

int read_event(MidiFile * midifile, uint8_t running_status) {
	uint32_t dt = readVariableLength(midifile);
	printf("delta time: %d\n", dt);

	uint8_t event_code = read8(midifile);

	if (event_code == 0xFF) {
		uint8_t meta_event_type = read8(midifile);
		printf("meta-event type: %d\n", meta_event_type);
		uint32_t event_length = readVariableLength(midifile);
		for (int i = 0; i < event_length; i++) read8(midifile);

		if (meta_event_type == 0x2F) return 0; // end of track
		
		return read_event(midifile, 0);
						       
	} 

	if (event_code == 0xF0) {
		uint32_t event_length = readVariableLength(midifile);
		printf("sysex event length: %d", event_length);
		for (int i = 0; i < event_length; i ++) read8(midifile);

		return read_event(midifile, 0);
	} 

	uint8_t first_data_byte;
	if (event_code < 0b10000000) {
		first_data_byte = event_code;
		event_code = running_status;
	} else {
		first_data_byte = read8(midifile);
	}

	switch (event_code & 0xF0) {
		case 0x80:
			printf("voice note off\n");
			uint8_t second_data_byte = read8(midifile);
			break;
		case 0x90:
			printf("voice note on\n");
			uint8_t second_data_byte2 = read8(midifile);
			break;
		case 0xB0: read8(midifile); break; // VoiceControlChange 2
		case 0xE0: read8(midifile); break; // VoicePitchBend 2
		case 0xA0: read8(midifile); break;// VoiceAftertouch 2
		case 0xC0: break;// VoiceProgramChange 1
		case 0xD0: break;// VoiceChannelPressure 1
	}
	return read_event(midifile, event_code);


}

int read_track_chunk(MidiFile * midifile, uint16_t tracks_to_read) {

	if (tracks_to_read == 0) return 0;

	uint64_t starting_bytes_read = midifile->bytes_read;

	char MTrk[4];
	for (uint8_t i = 0; i < 4; i++) MTrk[i] = read8(midifile);

	if (strcmp(MTrk, "MTrk") != 0) return 1;
	printf("this is a track\n");

	uint32_t track_length = read32(midifile);

	read_event(midifile, 0);

	if (midifile->bytes_read - starting_bytes_read != track_length + 4 + 4) printf("UHOH: track lengths %ld and %d do not add up\n", midifile->bytes_read - starting_bytes_read, track_length + 4 + 4);

	return read_track_chunk(midifile, tracks_to_read - 1);
}

int read_header_chunk(MidiFile * midifile) {

	char MThd[4];
	for (uint8_t i = 0; i < 4; i++) MThd[i] = read8(midifile);

	if (strcmp(MThd, "MThd") != 0) return 1;

	uint32_t header_length = read32(midifile);

	uint16_t format = read16(midifile);
	uint16_t ntrks = read16(midifile);
	uint16_t division = read16(midifile);

	int is_ticks_mode = (division & (1 << 15)) != 0;

	// we only know how to read 6-byte headers, so toss any extra bytes
	for (uint32_t i = header_length; i > 6; i--) read8(midifile);

	if (ntrks == 0) return 0;

	return read_track_chunk(midifile, ntrks);
}

const char * parse_midi_file(wchar_t * filename_wchar_p, int (*save_note)(int, int, int, int)) {

	char * filename = wchar_t_to_const_char(filename_wchar_p);
	printf("Parsing MIDI File: %s\n", filename);

	MidiFile midifile;
	midifile.bytes_read = 0;
	midifile.fp = fopen(filename, "rb");
	if (midifile.fp == NULL) return "Failed to open file.";

	read_header_chunk(&midifile);

	fclose(midifile.fp);

	free(filename);
	return "Midi parse successful.";
}

int dummy_save_note(int a, int b, int c, int d) {
	printf("saving note");
	return 0;
}

int main() {
	wchar_t * filename = L"../MIDI/d_minor_scale.mid";
	parse_midi_file(filename, *dummy_save_note);
}
