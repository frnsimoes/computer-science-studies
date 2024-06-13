"""
Objective: extend proxy to respect keep alive semantics.
Non-objective: maintain connection with origin.
Keep-alive semantics:
    HTTP/1.0: Close unless Connection: keep-alive
    HTTP/1.1: Keep open unless Connection: close


How to run:
    `python http.server 8778` (upstream socket port)
    `python proxy.py`
    `curl 127.0.0.1:8777` (proxy port)

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
    try:
        client_sock, client_addr = s.accept()
        log(f"New connection from {client_addr}")

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

    except ConnectionRefusedError:
        # If the upstream server is down, send a 502 to the client.
        with open("502.html", "r") as file:
            html_content = file.read()
        response = (
            "HTTP/1.1 502 Bad Gateway\r\nContent-Type: text/html\r\n\r\n" + html_content
        )
        client_sock.send(response.encode())
        log("<- *    BAD GATEWAY")

    except OSError as msg:
        log(msg)

    finally:
        close(upstream_sock)
        close(client_sock)

close(s)
