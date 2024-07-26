#ifndef BINARYDEBUG_H
#define BINARYDEBUG_H

#include <stdio.h>
#include <stdint.h>

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

#endif
