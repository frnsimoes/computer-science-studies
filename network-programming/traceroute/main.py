import socket

sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sender.setsockopt(socket.SOL_IP, socket.IP_TTL, 3)

receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

data = b'\x00' 
address = ('1.1.1.1', 1111)

sender.sendto(data, address)

print(receiver.recv(1024))
