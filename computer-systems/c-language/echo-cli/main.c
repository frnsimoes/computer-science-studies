#include <stdio.h>


int main(int argc, char *argv[]) {
	int i;
	for (i = 1; i < argc; i++) {
		char *last_char = (i < argc -1) ? " " : "";
		printf("%s%s", argv[i], last_char);
	}
	printf("\n");
	return 0;
}



