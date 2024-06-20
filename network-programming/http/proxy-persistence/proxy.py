"""
Objective: extend proxy to respect keep alive semantics.
Non-objective: maintain connection with origin.
Keep-alive semantics:
    HTTP/1.0: Close unless Connection: keep-alive
    HTTP/1.1: Keep open unless Connection: close


How to run:
    `python -m http.server 8778` (upstream socket port)
    `python proxy.py`
    `curl 127.0.0.1:8777` (proxy port)


Tests using netcat:
    nc localhost 8777 # stablishes connection
    
    # Test a simple get
    GET / HTTP/1.1

    -- 1) should return GET / content; 2) should keep alive.

    # Test /styles
    GET / HTTP/1.1

    -- 1) should return /styles content; 2) should keep alive.

    # Test 404
    GET /foo HTTP/1.1

    -- 1) should return 404 content; 2) should keep alive -- current failing, returning Connection: close in resp headers.


    # Test keepalive on HTTP/1.0:
    GET / HTTP/1.0

    -- 1) should return GET / content; 2) should close the connection;

    GET / HTTP/1.0
    Connection: Keep-alive

    -- 1) should return GET / content; 2) should keepalive.


"""

import socket
import sys
import parser


PROXY_ADDR = ("0.0.0.0", 8777)
UPSTREAM_ADDR = ("127.0.0.1", 8778)


def log(s):
    print(s, file=sys.stderr)


def close(s):
    # close will close the connection and 'unbind' the socket from the port, so the OS won't prevent (30 seconds?) the rebinding.
    s.close()
    s.detach()

def should_keepalive(req):
    if req.version == b'HTTP/1.0':
        return req.headers.get(b'connection', "").lower() == b'keep-alive'
    if req.version == b'HTTP/1.1':
        close_connection = req.headers.get(b'connection', '').lower() == b'close'
        return not close_connection

    return False
        

def handle_client_connection(client_sock):
    while True: # one per req from client
        upstream_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        upstream_sock.connect(UPSTREAM_ADDR)
        log(f"Connected to {UPSTREAM_ADDR}")

        req = parser.HttpRequest()
        close = False
        while req.state is not parser.HttpState.END:
            data = client_sock.recv(4096)
            log(f"-> *    {len(data)}B")
            
            if not data:
                close = True
                break

            req.parse(data)
            upstream_sock.send(data)
            log(f"    * -> {len(data)}B")

        if close:
            upstream_sock.send(data)
            return

        while True:
            res = upstream_sock.recv(4096)
            log(f"    * <- {len(res)}B")

            if not res:
                break

            client_sock.send(res)
            log(f"<- *    {len(res)}B")

        upstream_sock.close()
        upstream_sock.detach()

        if not should_keepalive(req):
            return

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(PROXY_ADDR)
s.listen(10)  # number of maxmium queued connections the socket should hold.
log(f"Accepting new connections on {PROXY_ADDR}")


# This is a way to accept multiple connections without closing the connection after the first one is closed.
while True: # one per client connection
    try:
        client_sock, client_addr = s.accept()
        log(f"New connection from {client_addr}")
        handle_client_connection(client_sock)


    except ConnectionRefusedError:
        # If the upstream server is down, send a 502 to the client.
        with open("502.html", "r") as file:
            html_content = file.read()
        response = (
            "HTTP/1.1 502 Bad Gateway\r\nContent-Type: text/html\r\n\r\n" + html_content
        )
        client_sock.send(response.encode())
        log("<- *    BAD GATEWAY")

    except Exception as msg:
        log(msg)
        client.sock.send(b'HTTP/1.1 500 Internal Server Error\r\n\r\n')
        log("<- *    INTERNAL SERVER ERROR")

    finally:
        close(client_sock)

close(s)
