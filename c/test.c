#include <stdio.h>

void message() {
	printf("A monad is a monoid in the category of endofunctors.");
}

void run_py_func(void (*fun)()) {
	fun();
}
