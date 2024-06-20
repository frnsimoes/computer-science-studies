import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", 7777))

s.listen(1)

while True:
    conn, addr = s.accept()
    req = conn.recv(4096)
    headers, body = req.split(b"\r\n\r\n")
    d = {}
    for hline in headers.split(b"\r\n")[1:]:
        k, v = hline.split(b": ")
        d[k.decode("ascii")] = v.decode("ascii")

    conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
    print(headers)
    print(body)
    conn.send(json.dumps(d, indent=4).encode("ascii"))
    conn.close()
