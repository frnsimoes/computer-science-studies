import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('142.250.66.238', 80))

# Google responds to no protocol version (implicitly HTTP 0.9)
s.send(b'GET /\n')

print(s.recv(1000))
