#include <stdio.h>
#include <wchar.h>

int parse_midi_file(const wchar_t * filename_wchar_p, int (*save_note)(int, int, int, int)) {
	char filename[100];
	sprintf(filename, "%ls", filename_wchar_p);
	printf("Opening %s\n",filename);

	FILE * midifile;
	midifile = fopen(filename, "rb");
	if (midifile == NULL) {
		printf("failed to open file %s\n", filename);
		return 1;
	}

	int note_save_result = save_note(-1,-1,-1,-1);

	fclose(midifile);
	return 0;
}
