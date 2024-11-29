#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <sys/wait.h>

int main() {
    size_t mem_size = 4096; // Size of the shared memory
    char *shared_mem = mmap(NULL, mem_size, PROT_READ | PROT_WRITE,
                            MAP_ANONYMOUS | MAP_SHARED, -1, 0);

    if (shared_mem == MAP_FAILED) {
        perror("mmap failed");
        return 1;
    }

    // Process 1 writes and depends on data integrity
    if (fork() == 0) {
        strcpy(shared_mem, "Data from Process 1");
        printf("Process 1 wrote: %s\n", shared_mem);

        sleep(2); // Simulate work depending on valid data

        if (strcmp(shared_mem, "Data from Process 1") != 0) {
            fprintf(stderr, "Process 1 detected corruption: %s\n", shared_mem);
            raise(SIGSEGV); // Simulate a crash
        }

        printf("Process 1 finished successfully!\n");
        exit(0);
    }

    // Process 2 disrupts the memory
    sleep(1); // Wait for Process 1 to start
    strcpy(shared_mem, "Corrupted by Process 2");
    printf("Process 2 wrote: %s\n", shared_mem);

    wait(NULL); // Wait for Process 1
    munmap(shared_mem, mem_size);
    return 0;
}
