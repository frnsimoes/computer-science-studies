É um identificador único, ou uma referência única, que o sistema operacional utiliza para acessar um arquivo ou um "stream of data". É um número que representa um arquivo aberto, ou um recurso de input/output dentro de um processo. 

**Standard file descriptors**:
- stdin: file descriptor 0, utilizado para input (por exemplo, ler algo do teclado).
- stdout: file descriptor 1, utilizado para output.
- stderr: file descriptor2, utilizado para mensagens de erro. 

O stderr, no entanto, serve para do que para armazenar mensagens de erro. `stderr` provides a standardized way for programs to output messages that are separate from normal output. 

Um exemplo disso é curl example.com 2>tmp/headers

Really cool explanation: https://crystallabs.io/unix-file-descriptors/
> In Unix, whenever a running program opens a file, the kernel stores a reference to it in the process’ memory. Those references to open files are integers starting from 0 for each process, and are called file descriptors or FDs. A process can only read and write files that it has opened, that is, for which it had obtained a file descriptor.



