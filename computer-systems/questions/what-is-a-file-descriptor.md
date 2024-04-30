É um identificador único, ou uma referência única, que o sistema operacional utiliza para acessar um arquivo ou um "stream of data". É um número que representa um arquivo aberto, ou um recurso de input/output dentro de um processo. 

**Standard file descriptors**:
- stdin: file descriptor 0, utilizado para input (por exemplo, ler algo do teclado).
- stdout: file descriptor 1, utilizado para output.
- stderr: file descriptor2, utilizado para mensagens de erro. 

O stderr, no entanto, serve para do que para armazenar mensagens de erro. `stderr` provides a standardized way for programs to output messages that are separate from normal output. 

Um exemplo disso é curl example.com 2>tmp/headers
