midiloader: midiloader.o
	gcc -shared midiloader.o -o libmidiloader.so

test: midiloader.o
	gcc midiloader.o -o test.exe
