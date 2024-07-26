#ifndef VARIABLELENGTH_H
#define VARIABLELENGTH_H

#include "BinaryDebug.h"
#include "MidiFile.h"

#include <stdint.h>
#include <stdio.h>

uint32_t readVariableLength(MidiFile * midifile) {
	uint8_t current_byte = getc(midifile->fp);
	char current_byte_repr[8];
	binary_repr(current_byte_repr, current_byte);
	midifile->bytes_read += 1;
	if (current_byte < 0b10000000) return current_byte;

	current_byte = current_byte & 0b01111111;

	uint64_t bytes_read = midifile->bytes_read;
	uint32_t next_bytes = readVariableLength(midifile);
	uint8_t num_next_bytes = midifile->bytes_read - bytes_read;

	return (current_byte << (7 * num_next_bytes)) | next_bytes;
}

#endif
