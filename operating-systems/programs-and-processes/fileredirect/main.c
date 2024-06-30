/*from OSTEP p4.c: https://github.com/remzi-arpacidusseau/ostep-code/blob/master/cpu-api/p4.c, with my comments*/


#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <assert.h>
#include <sys/wait.h>

	int
main(int argc, char *argv[])
{
	int rc = fork();
	if (rc < 0) {
		// fork failed; exit
		fprintf(stderr, "fork failed\n");
		exit(1);
	} else if (rc == 0) {
		// child: redirect standard output to a file
		close(STDOUT_FILENO); 
		open("./p4.output", O_CREAT|O_WRONLY|O_TRUNC, S_IRWXU);

		// now exec "wc"...
		char *myargs[3];

		// man strdup:
		// The strdup() function allocates sufficient memory for a copy of the
		// string s1, does the copy, and returns a pointer to it.  The pointer may
		// subsequently be used as an argument to the function free(3).
		myargs[0] = strdup("wc");   // program: "wc" (word count)
					    //
		myargs[1] = strdup("p4.c"); // argument: file to count
		myargs[2] = NULL;           // marks end of array
		
		// man execvp:
		// The exec family of functions replace the currenct process *image* with a new process image
		// Meaning: if there was a "printf" after the execvp, for example, the printf would not be executed.
		// What's image in this context?
		// It's the complete state of a process as it exists in memory. Including:
		// executable code, data, stack, heap, and other resources.
		//
		// When a process calls exec, its current process image is replaced
		// with a new process image from the executable file specified in the exec call.
		execvp(myargs[0], myargs);  // runs word count
	} else {
		// parent goes down this path (original process)
		int wc = wait(NULL);
		assert(wc >= 0);
	}
	return 0;
}
