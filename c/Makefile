midiloader: midiloader.o
	rm midiloader.o
	gcc -c midiloader.c -fPIC
	gcc -shared midiloader.o -o libmidiloader.so

test: midiloader.o
	gcc midiloader.o -o test.exe
