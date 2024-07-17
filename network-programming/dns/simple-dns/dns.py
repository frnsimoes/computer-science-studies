import sys
import socket
import struct

if __name__ == '__main__':
    hostname = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    xid = 42 # made this random though
    flags = 0x0100

    query = struct.pack("!HHHHHH", xid, flags, 1, 0, 0, 0)
    qname = b''.join(
            len(p).to_bytes(1, 'big') + p.encode('ascii')
            for p in hostname.split('.')) + b'\x00'
    query += qname
    query += struct.pack("!HH", 1, 1)
    s.sendto(query, ("8.8.8.8", 53))
    res, sender = s.recvfrom(4096)

    print(res)
    print(sender)


    # Parsing the header. 
    # https://www.rfc-editor.org/rfc/rfc1035#section-4.1.1
    rxid, rflags, qdcount, ancount, _, _, = struct.unpack("!HHHHHH", res[:12])
    assert rxid == xid
    assert qdcount == 1
    print('ok')

    after_header_index = 12
    while True:
        x = res[after_header_index]
        if x == 0x00:
            after_header_index += 1
            break

        after_header_index += x + 1

    after_header_index += 4 # skip qtype and qclass

    print(res[after_header_index:after_header_index+10])



