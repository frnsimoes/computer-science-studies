import sys
import struct
import socket

MAX_PAYLOAD_SIZE = 4 # 4 bytes


def pack_segment(seq, ack, payload):
    return struct.pack('!HH', seq, ack) + payload

def unpack_segment(data):
    seq, ack = struct.unpack('!HH', data[:4])
    return seq, ack, data[4:]


class ReliableDelivery:
    def __init__(self, target_addr=None):
        self.target_addr = target_addr
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.seq = 0
        self.ack = 0
        
    def bind(self, own_addr):
        self._sock.bind(own_addr)

    def send(self, data):
        i = 0
        while i < len(data):
            payload = data[i:i+MAX_PAYLOAD_SIZE]
            # send
            segment = pack_segment(self.seq, self.ack, payload)
            self._sock.sendto(segment, self.target_addr)
            self.seq += 1
            i += len(payload)

    def recv(self):
        while True:
            data, sender = self._sock.recvfrom(4096)
            if not self.target_addr:
                self.target_addr = sender

            if self.target_addr != sender:
                # let's wait for another packet
                continue

            seq, ack, payload = unpack_segment(data)
            print(f'Recvd seq: {seq}, ack: {ack}')

            return payload


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # we act as client, and send data to given port
        rd = ReliableDelivery(('127.0.0.1', int(sys.argv[1])))
        rd.send(b'0123456789')
        print(rd.recv())
        print(rd.recv())
    else:
        # no port, we act as server, binding to a port 
        rd = ReliableDelivery()
        rd.bind(('0.0.0.0', 8000))
        recvd = 0

        while recvd < 3:
            print(rd.recv())
            recvd += 1

        rd.send(b'abcde')
