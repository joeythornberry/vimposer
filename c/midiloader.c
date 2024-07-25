#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <wchar.h>

char * wchar_t_to_const_char(wchar_t * wchar_t_string) {
	size_t len = wcslen(wchar_t_string);
	char * char_string = malloc(len + 1);
	for (uint8_t i = 0; i < len; i++) {
		char_string[i] = wchar_t_string[i];
	}
	char_string[len] = '\0';
	return char_string;
}

const char read_bit(uint8_t input, uint8_t bit_to_read) {
	uint8_t bit = input & (1 << bit_to_read);
	if (bit == 0) {
		return '0';
	} else {
		return '1';
	}
}

void binary_repr(char dest[8], uint8_t input) {
	for(uint8_t i = 0; i < 8; i++) {
		dest[i] = read_bit(input, i);
	}
}

uint32_t read32(FILE * file) {
	return (getc(file) << 24) | (getc(file) << 16) | (getc(file) << 8) | getc(file);
}

uint16_t read16(FILE * file) {
	return (getc(file) << 8) | getc(file);
}

typedef struct {
	uint16_t tracks_to_read;
} MidiParseContext;

int read_track_chunk(FILE * midifile, MidiParseContext midi_parse_context) {
	char MTrk[4];
	for (uint8_t i = 0; i < 4; i++) MTrk[i] = getc(midifile);

	if (strcmp(MTrk, "MTrk") != 0) return 1;
	printf("this is a track\n");

	uint32_t track_length = read32(midifile);
	for (uint32_t i = 0; i < track_length; i++) {
		getc(midifile);
	}

	uint16_t new_tracks_to_read = midi_parse_context.tracks_to_read - 1;
	if (new_tracks_to_read == 0) return 0;

	MidiParseContext new_midi_parse_context;
	new_midi_parse_context.tracks_to_read = new_tracks_to_read;
	return read_track_chunk(midifile, new_midi_parse_context);
}

int read_header_chunk(FILE * midifile) {

	char MThd[4];
	for (uint8_t i = 0; i < 4; i++) MThd[i] = getc(midifile);

	if (strcmp(MThd, "MThd") != 0) return 1;

	uint32_t header_length = read32(midifile);

	uint16_t format = read16(midifile);
	uint16_t ntrks = read16(midifile);
	uint16_t division = read16(midifile);

	int is_ticks_mode = (division & (1 << 15)) != 0;

	// we only know how to read 6-byte headers, so toss any extra bytes
	for (uint32_t i = header_length; i > 6; i--) getc(midifile);

	if (ntrks == 0) return 0;

	MidiParseContext midi_parse_context;
	midi_parse_context.tracks_to_read = ntrks;

	return read_track_chunk(midifile, midi_parse_context);
}

const char * parse_midi_file(wchar_t * filename_wchar_p, int (*save_note)(int, int, int, int)) {

	char * filename = wchar_t_to_const_char(filename_wchar_p);
	printf("Parsing MIDI File: %s\n", filename);

	FILE * midifile;
	midifile = fopen(filename, "rb");
	if (midifile == NULL) {
		return "Failed to open file.";
	}

	read_header_chunk(midifile);

	fclose(midifile);

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
