import socket

PROXY_ADDRESS = ("127.0.0.1", 8777)

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(PROXY_ADDRESS)

request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(PROXY_ADDRESS[0])
client_sock.send(request.encode())


response = b''
while True:
    resp_chunk = client_sock.recv(1024)
    if not resp_chunk:
        break

    response += resp_chunk

print(response.decode())

client_sock.close()
