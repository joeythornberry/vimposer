#include <wchar.h>
#include <stdlib.h>
#include <stdint.h>

char * wchar_t_to_const_char(wchar_t * wchar_t_string) {
	size_t len = wcslen(wchar_t_string);
	char * char_string = (char *) malloc(len + 1);
	for (uint8_t i = 0; i < len; i++) {
		char_string[i] = wchar_t_string[i];
	}
	char_string[len] = '\0';
	return char_string;
}

