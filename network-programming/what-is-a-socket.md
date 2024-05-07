A socket is a communication endpoint that allows processes to communicate over a network. It can be thought of as a virtual bidirectional communication channel between two processes running on different devices, typically connected over a network.

Socket file descriptor:
when a process creates or interacts with a socket, the operating system assigns a file descriptor to that socket. This file descriptor serves as a reference or handle that the process uses to perform operations related to the socket, such as sending or receiving data.

Socket file descriptors (numbers) are integer values returned by system calls when creating or interacting with sockets. 
