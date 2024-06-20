"""
Goal: concurrent web server that returns 200 ojk to everything
Test: should be able to make two connections, and achieve req/res on either.
"""

import select
import socket


listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# In non-blocking mode, if a `recv()` call doesn't find any data, or if a `send()` call can't immediately dispose of the data, a `socket.error` exception is raised. 
# This means the system will not wait for these operations to complete and will continue with the rest of the code.
listener.setblocking(False)

listener.bind(('0.0.0.0', 10000))
listener.listen(10)

inputs = [listener]
outputs = []

to_send = set()

while True:
    # select.select() stops the execution of the program.
    # it waits until something happens to the monitored file descriptors.

    # Without the select, I would have needed each individual socket to check if it was ready for reading or writing.
    # With select, though, the program can simply wait until one of the sockets is ready. 
    # When select returns, it informs which sockets are ready, and the program can read and write to these sockets immediately, without
    # the need to verify every other socket.

    # Select allows the program to handle multiple sockets with only one thread, without the need of multithreading or multiprocessing.
    readable, writable, excepcional = select.select(inputs, outputs, inputs)
    print('readables')
    print(readable)

    print('writables')
    print(writable)

    for s in readable:
        # when s is the listener itself. 
        if s is listener:
            # listener can accept connection immediately 
            client_sock, client_addr = s.accept()
            client_sock.setblocking(False)
            inputs.append(client_sock)

        else:
            # socket is a client connection 
            data = s.recv(4096)
            if data:
                print(data)
                outputs.append(s)
                to_send.add(s)
            else:
                s.close()
            inputs.remove(s)

    for s in writable:
        if s in to_send:
            to_send.remove(s)
            outputs.remove(s)
            s.send(b'HTTP/1.0 200 ok \r\n\r\nbody text')
            s.close()

