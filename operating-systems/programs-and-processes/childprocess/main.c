#include <signal.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/resource.h>

int main() {
    struct rlimit rl;
    
    getrlimit(RLIMIT_NPROC, &rl);
    
    rl.rlim_cur = 1;
    setrlimit(RLIMIT_NPROC, &rl);

    pid_t pid = fork();

    printf("PID: %d\n", pid);

    if (pid == 0) {
        printf("Child\n");
    } else {
        wait(NULL);
	kill(pid, SIGKILL);
	printf("Parent\n");
    }

    return 0;
}
