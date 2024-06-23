#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <limits.h>
#include <stdlib.h>

#define ONE_MEG 1024 * 1024

char* file_path() {
    static char filepath[PATH_MAX];
    char cwd[PATH_MAX];
    if (getcwd(cwd, sizeof(cwd)) == NULL) {
        perror("getcwd() error");
        return NULL;
    }

    snprintf(filepath, sizeof(filepath), "%s/%s", cwd, "tmp/foo");
    return filepath;
}

int main() {
	int f = open(file_path(), O_WRONLY | O_TRUNC);

	blkcnt_t prior_blocks = -1;
	struct stat st;

	for (int i = 0; i < ONE_MEG; i++) {
		write(f, ".", 1);
		fstat(f, &st);

		if (st.st_blocks != prior_blocks) {
			printf("Size: %lld, blocks: %lld, on disk: %lld\n", st.st_size, st.st_blocks, st.st_blocks * 512);
			prior_blocks = st.st_blocks;
		}
	}

	close(f);
	return 0;
}

