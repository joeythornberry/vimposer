#include <stdint.h>
#include <stdlib.h>

#include <stdio.h>
#include <string.h>
#include <time.h>
#include <wchar.h>

#include "MidiFile.h"
#include "BinaryDebug.h"
#include "Conversions.h"
#include "VariableLength.h"
#include "MidiParsing.h"

int export_midi_file(wchar_t * filename_wchar_p, void (*export_note)(uint8_t, uint32_t, uint32_t, uint8_t), uint8_t chars_per_quarter_note) {

	char * filename = wchar_t_to_const_char(filename_wchar_p);
	printf("Parsing MIDI File: %s\n", filename);

	MidiFile midifile;
	midifile.bytes_read = 0;
	midifile.fp = fopen(filename, "rb");
	if (midifile.fp == NULL) return -1;

	ExportFunctions export_functions;
	export_functions.export_note = export_note;

	int ticks_per_char = parse_midi_file(&midifile, &export_functions, chars_per_quarter_note);

	fclose(midifile.fp);

	free(filename);

	return ticks_per_char;
}

void dummy_save_note(uint8_t p, uint8_t x, uint8_t l, uint8_t t) {
	printf("saving note: p=%d x=%d l=%d t=%d\n", p, x, l, t);
}


int main() {
	wchar_t * filename = L"../MIDI/d_minor_scale.mid";
	//export_midi_file(filename, *dummy_save_note);
}
