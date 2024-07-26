#include <stdint.h>
#include <string.h>

#include "MidiFile.h"
#include "VariableLength.h"

typedef struct {
	int (*export_note) (int, int, int, int); // p, x, l, t
} ExportFunctions;

typedef struct {
	uint64_t start_time;
} NoteOn;

typedef struct {
	NoteOn note_on_map[127 * sizeof(NoteOn)];
} OngoingNotes;

int parse_event(
		MidiFile * midifile,
		uint8_t running_status,
		OngoingNotes * ongoing_notes,
		ExportFunctions * export_functions,
		uint64_t current_time
		) {
	uint32_t dt = readVariableLength(midifile);
	current_time += dt;

	uint8_t event_code = read8(midifile);

	if (event_code == 0xFF) {
		uint8_t meta_event_type = read8(midifile);
		uint32_t event_length = readVariableLength(midifile);
		for (int i = 0; i < event_length; i++) read8(midifile); // skip data
		if (meta_event_type == 0x2F) return 0; // end of track
		return parse_event(midifile, 0, ongoing_notes, export_functions, current_time);
	} 

	if (event_code == 0xF0) {
		uint32_t event_length = readVariableLength(midifile);
		for (int i = 0; i < event_length; i ++) read8(midifile); // skip data
		return parse_event(midifile, 0, ongoing_notes, export_functions, current_time);
	} 

	uint8_t first_data_byte;
	if (event_code < 0b10000000) {
		first_data_byte = event_code;
		event_code = running_status;
	} else {
		first_data_byte = read8(midifile);
	}

	switch (event_code & 0xF0) {
		case 0x90:
			uint8_t note_on_pitch = first_data_byte;
			uint8_t note_on_velocity = read8(midifile);
			NoteOn note_on;
			note_on.start_time = current_time;
			ongoing_notes->note_on_map[note_on_pitch] = note_on;
			break;
		case 0x80:
			uint8_t note_off_pitch = first_data_byte;
			uint8_t note_off_velocity = read8(midifile);
			NoteOn * corresponding_note_on = 
				&ongoing_notes->note_on_map[note_off_pitch];
			int note_length = current_time - corresponding_note_on->start_time;
			export_functions->export_note(note_off_pitch, corresponding_note_on->start_time, note_length, 12);
			break;
		case 0xB0: read8(midifile); break; // VoiceControlChange 2
		case 0xE0: read8(midifile); break; // VoicePitchBend 2
		case 0xA0: read8(midifile); break;// VoiceAftertouch 2
		case 0xC0: break;// VoiceProgramChange 1
		case 0xD0: break;// VoiceChannelPressure 1
	}
	return parse_event(midifile, event_code, ongoing_notes, export_functions, current_time);


}

int parse_track_chunk(
		MidiFile * midifile,
		uint16_t tracks_to_read,
		ExportFunctions * export_functions
		) {

	if (tracks_to_read == 0) return 0;

	uint64_t starting_bytes_read = midifile->bytes_read;

	char MTrk[4];
	for (uint8_t i = 0; i < 4; i++) MTrk[i] = read8(midifile);

	if (strcmp(MTrk, "MTrk") != 0) return 1;
	printf("this is a track\n");

	uint32_t track_length = read32(midifile);

	OngoingNotes ongoing_notes;

	parse_event(midifile, 0, &ongoing_notes, export_functions, 0);

	if (midifile->bytes_read - starting_bytes_read != track_length + 4 + 4) printf("UHOH: track lengths %ld and %d do not add up\n", midifile->bytes_read - starting_bytes_read, track_length + 4 + 4);

	return parse_track_chunk(midifile, tracks_to_read - 1, export_functions);
}

int parse_midi_file(MidiFile * midifile, ExportFunctions * export_functions) {

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

	return parse_track_chunk(midifile, ntrks, export_functions);
}