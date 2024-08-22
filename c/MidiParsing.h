#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "MidiFile.h"
#include "VariableLength.h"

typedef struct {
	void (*export_note) (uint8_t, uint32_t, uint32_t, uint8_t, uint8_t, uint8_t); // p, x, l, t, v, instrument
										
	void (*export_tempo) (uint32_t);
} ExportFunctions;

typedef struct {
	uint64_t start_time;
	uint8_t velocity;
} NoteOn;

typedef struct {
	NoteOn note_on_map[127 * sizeof(NoteOn)];
} OngoingNotes;

uint32_t quantize(uint64_t time, uint16_t base_unit_of_time) {
	return time / base_unit_of_time;
}

int parse_event(
		MidiFile * midifile,
		uint8_t running_status,
		uint16_t base_unit_of_time,
		OngoingNotes * ongoing_notes,
		ExportFunctions * export_functions,
		uint64_t current_time, 
		uint16_t track_id,
		uint8_t track_has_notes, 
		uint8_t instrument
		) {

	uint8_t new_instrument = instrument;
	uint32_t dt = readVariableLength(midifile);
	current_time += dt;

	uint8_t event_code = read8(midifile);
	printf("%x\n", event_code);

	if (event_code == 0xFF) {
		uint8_t meta_event_type = read8(midifile);
		uint32_t event_length = readVariableLength(midifile);

		uint8_t SET_TEMPO = 0x51;
		if (meta_event_type == SET_TEMPO && event_length == 3) {
			uint32_t new_tempo = (read8(midifile) << 16) | (read8(midifile) << 8) | read8(midifile);
			printf("new tempo: %d\n", new_tempo);
			export_functions->export_tempo(new_tempo);
		} else {
			for (int i = 0; i < event_length; i++) read8(midifile); // skip data
			if (meta_event_type == 0x2F) return track_has_notes; // end of track
		}
		return parse_event(midifile, 0, base_unit_of_time, ongoing_notes, export_functions, current_time, track_id, track_has_notes, instrument);
	} 

	if (event_code == 0xF0) {
		uint32_t event_length = readVariableLength(midifile);
		for (int i = 0; i < event_length; i++) read8(midifile); // skip data
		return parse_event(midifile, 0, base_unit_of_time, ongoing_notes, export_functions, current_time, track_id, track_has_notes, instrument);
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
			NoteOn note_on;
			note_on.start_time = quantize(current_time, base_unit_of_time);
			note_on.velocity = read8(midifile);
			ongoing_notes->note_on_map[note_on_pitch] = note_on;
			track_has_notes = 1;
			NoteOn * responding_note_on = 
				&ongoing_notes->note_on_map[note_on_pitch];
			break;
		case 0x80:
			uint8_t note_off_pitch = first_data_byte;
			uint8_t note_off_velocity = read8(midifile);
			NoteOn * corresponding_note_on = 
				&ongoing_notes->note_on_map[note_off_pitch];
			int note_length = quantize(current_time, base_unit_of_time) - corresponding_note_on->start_time;
			export_functions->export_note(note_off_pitch, corresponding_note_on->start_time, note_length, track_id, corresponding_note_on->velocity, instrument);
			break;
		case 0xB0: read8(midifile); break; // VoiceControlChange 2
		case 0xE0: read8(midifile); break; // VoicePitchBend 2
		case 0xA0: read8(midifile); break; // VoiceAftertouch 2
		case 0xC0: 
			   new_instrument = first_data_byte; 
			   break; // VoiceProgramChange 1
		case 0xD0: break; // VoiceChannelPressure 1
	}

	return parse_event(midifile, event_code, base_unit_of_time, ongoing_notes, export_functions, current_time, track_id, track_has_notes, new_instrument);
}

int parse_track_chunk(
		MidiFile * midifile,
		uint16_t tracks_remaining,
		uint16_t track_id,
		uint16_t base_unit_of_time,
		ExportFunctions * export_functions
		) {

	if (tracks_remaining == 0) return 0;

	uint64_t starting_bytes_read = midifile->bytes_read;

	char MTrk[4];
	for (uint8_t i = 0; i < 4; i++) MTrk[i] = read8(midifile);

	if (strcmp(MTrk, "MTrk") != 0) return 1;
	//printf("this is a track\n");

	uint32_t track_length = read32(midifile);

	OngoingNotes ongoing_notes;

	uint8_t instrument = 0;

	uint8_t track_has_notes = parse_event(midifile, 0, base_unit_of_time, &ongoing_notes, export_functions, 0, track_id, 0, instrument);

	if (midifile->bytes_read - starting_bytes_read != track_length + 4 + 4) printf("UHOH: track lengths %ld and %d do not add up\n", midifile->bytes_read - starting_bytes_read, track_length + 4 + 4);

	return parse_track_chunk(midifile, tracks_remaining - 1, track_id + track_has_notes, base_unit_of_time, export_functions);
}

int parse_midi_file(MidiFile * midifile, ExportFunctions * export_functions, uint8_t chars_per_quarter_note) {

	char MThd[4];
	for (uint8_t i = 0; i < 4; i++) MThd[i] = read8(midifile);

	if (strcmp(MThd, "MThd") != 0) return 1;

	uint32_t header_length = read32(midifile);

	uint16_t format = read16(midifile);
	uint16_t ntrks = read16(midifile);
	uint16_t division = read16(midifile);
	printf("division: %d\n", division);

	int is_ticks_mode = (division & (1 << 15)) == 0;

	uint16_t base_unit_of_time = 1;

	if (is_ticks_mode) base_unit_of_time = division / chars_per_quarter_note; // 32nd note
	printf("base time unit: %d\n", base_unit_of_time);

	// we only know how to read 6-byte headers, so toss any extra bytes
	for (uint32_t i = header_length; i > 6; i--) read8(midifile);

	if (ntrks == 0) return -1;

	parse_track_chunk(midifile, ntrks, 0, base_unit_of_time, export_functions);

	return base_unit_of_time;
}
