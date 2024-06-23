#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

int main(int argc, char *argv[]) {
	// mallic(sizeof(int)) function call allocated anough memory to store one integer
	// in most modern systems, the size of an integer is 4 bytes.
	// the malloc function returns a p[ointer to the first byte of the allocated memory, and this pointer is stored in `p`.
	// so `p` is storing the memory address of the allocated memory. 
	// the allocated memory is where an integer value can be stored
	// at this point, however the memory has been allocated but not initialized.
	int *p = malloc(sizeof(int)); 
	assert(p != NULL);
	printf("(%d) address pointed to by p: %p\n", getpid(), p); 
	*p = 0;
	while (*p < 3) {
		sleep(1);
		*p = *p + 1;
		printf("(%d) p: %d\n", getpid(), *p); // a4
	}
	return 0;
}
