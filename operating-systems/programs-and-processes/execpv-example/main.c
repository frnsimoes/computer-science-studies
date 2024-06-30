#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    char *args[] = {"ls", "-l", NULL};

    int pid_c = fork();
    if (pid_c < 0) {
	    // fork failed; exit
	    fprintf(stderr, "fork failed\n");
    } else if (pid_c == 0) {
	    printf("Before execvp\n");

	    if (execvp("ls", args) == -1) {
		    perror("execvp failed");
	    };

	    // Won't run if execvp executes
	    printf("After execvp\n");
    } else {
	    int wc = wait(NULL);
	    printf("end");
    }
	
    return 0;
}
