#ifndef MIDIFILE_H
#define MIDIFILE_H

#include <stdio.h>
#include <stdint.h>

typedef struct {
	uint64_t bytes_read;
	FILE * fp;
} MidiFile;

uint32_t read32(MidiFile * file) {
	file->bytes_read += 4;
	return (getc(file->fp) << 24) | (getc(file->fp) << 16) | (getc(file->fp) << 8) | getc(file->fp);
}

uint16_t read16(MidiFile * file) {
	file->bytes_read += 2;
	return (getc(file->fp) << 8) | getc(file->fp);
}

uint8_t read8(MidiFile * file) {
	file->bytes_read += 1;
	return getc(file->fp);
}

#endif
