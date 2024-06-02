"""
How to run: 
    `python http.server 8778` (upstream socket port)
    `python proxy.py`
    `curl 127.0.0.1:8777` (proxy port)

Notes:
    python http.server will run a socket server with the static files that exist in the directory.
"""
import socket
import sys


PROXY_ADDR = ("0.0.0.0", 8777)
UPSTREAM_ADDR = ("127.0.0.1", 8778)


def log(s):
    print(s, file=sys.stderr)

def close(s):
   # close will close the connection and 'unbind' the socket from the port, so the OS won't prevent (30 seconds?) the rebinding. 
   s.close() 
   s.detach()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(PROXY_ADDR)
s.listen(10)  # number of maxmium queued connections the socket should hold.
log(f"Accepting new connections on {PROXY_ADDR}")


while True:
    # This is a way to accept multiple connections without closing the connection after the first one is closed.
    client_sock, client_addr = s.accept()
    log(f"New connection from {client_addr}")

    # 4096 is the maximum message size.
    # We have a buffer which the OS can fill with data that it has received.
    # This is not saying that packet I receive can be as large as this
    # This is also not saying that the http message will have 4096 bytes.
    # This is an independente maximum buffer size that the OS will fill for us in calling recv.
    data = client_sock.recv(4096)
    log(f"-> *    {len(data)}B")

    upstream_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    upstream_sock.connect(UPSTREAM_ADDR)
    log(f"Connected to {UPSTREAM_ADDR}")
    upstream_sock.send(data)
    log(f"    * -> {len(data)}B")

    while True:
        res = upstream_sock.recv(4096)
        log(f"    * <- {len(res)}B")

        if not res:
            break

        client_sock.send(res)
        log(f"<- *    {len(res)}B")

    close(upstream_sock)
    close(client_sock)

close(s)


