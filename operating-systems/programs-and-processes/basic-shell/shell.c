// execute a program by name (search path)
// support a few builtins (eg. quit, help)
// do this in a loop
// no support for strings for now (tokenize on space and tabs)
// handle EOF and SIGINT correctly (EOF should terminate shell; SIGINT should terminal child)
//
// 1. implement a basic REPL, but echo instead of evaluating. (fgets/printf, not readline)
// 2. tokenize cmd, print argc/argv (strtok)
// 3. actually execute (fork/exec)
// 4. refactor/details, check success criteria incl signal handling

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <signal.h>

#define MAX_CMD 4096
#define MAX_ARGV 256
#define SEP " \t\n"
#define PROMPT "> "

volatile pid_t childpid = 0;


bool check_cmd(char* user_cmd, char *argv[]) {
    return (0 == strcmp(argv[0], user_cmd));
}

void sigint_handler(int sig) {
	if (!childpid) return;
	if (kill(childpid, SIGINT) < 0) {
		perror("Error sending SIGINT to child");
	}
}

int main () {
	char cmd[MAX_CMD];
	int argc;
	char *argv[MAX_ARGV];

	signal(SIGINT, sigint_handler);

	while (1) {
		printf(PROMPT);
		
		// If `fgets` returns `NULL` but `ferror(stdin)` is not true, it means that the end of the file (`EOF`) has been reached. 
		if (NULL == fgets(cmd, MAX_CMD, stdin) && ferror(stdin)) {
			perror("fgets error");
			exit(1);
		};
		// Check if reached EOF.
		// There is no signaling here.
		if (feof(stdin)) 
			exit(0);

		//  The strtok() function is used to isolate sequential tokens in a null-terminated string, str.  These tokens are separated in the string by at least one of the characters in sep.  The first time that strtok() is called, str should be specified; subsequent calls, wishing to obtain further tokens from the same
		// string, should pass a null pointer instead.  The separator string, sep, must be supplied each time, and may change between calls.
		
		// tokenize
		argc = 0;
		argv[argc] = strtok(cmd, SEP);

		while (argv[argc] != NULL) {
			argv[++argc] = strtok(NULL, SEP);
		};

		//eval
		if (argc == 0) continue;

		if (check_cmd("quit", &argv[0])) {
			exit(0);
		};

		if (check_cmd("help", &argv[0])) {
			printf("Welcome to my shell, builtins are quit and help \n");
			continue;
		};

		if ((childpid = fork()) < 0) {
			perror("fork error");
			exit(1);
		};	

		if (childpid == 0) { //child
			// example: `ls .`
			// excevp first argument "is the pathname of the file which is to be executed".
			//
			// nothing returns from execvp if it succeeds, for the current process is replaced by the new one.
			// if an error occurred, execvp returns `-1`
			printf("%s", *argv);
			if (execvp(argv[0], argv)) {
				perror("excepv error");
				exit(1);
			};
			exit(1);
		} 
		
	
		int status;
		waitpid(childpid, &status, 0);
		childpid = 0;

	};
}

