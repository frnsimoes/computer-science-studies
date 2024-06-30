#include <signal.h>
#include <stdio.h>
#include <sys/ioctl.h>

volatile sig_atomic_t resized = 0;

void handler(int sig) {resized = 1;}

int main () {
	struct winsize ws;
	struct sigaction sa;
	sa.sa_handler = handler;
	sigaction(SIGWINCH, &sa, NULL);

	printf("Waiting for signal\n");
	for(;;)
		if (resized) {
			resized = 0;
		};
	;

}
