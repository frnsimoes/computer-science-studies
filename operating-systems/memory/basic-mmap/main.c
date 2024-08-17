#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <wait.h>

int n = 0;

int main() {
	int stat;
	srand(time(NULL));

	if (fork() == 0) {
		n = rand();
		printf("Child has written %d to the address %p\n", n, &n);
		exit(0);
	} else {
		wait(&stat);
		printf("Parent has read %d from the address %p\n", n, &n);
	}
}
