import struct 

with open("synflood.pcap", "rb") as f:
    magic_number, major, minor, _, _, _, llh_type = struct.unpack('<IHHIIII', f.read(24))
    assert magic_number == 0xa1b2c3d4  # confirm that the file is little endian.

    print(f'pcap protocol version {major}.{minor}')

    assert llh_type == 0 # loopback

    count = 0
    while True:
        per_packet_header = f.read(16)
        if len(per_packet_header) == 0:
            break
        count += 1
        _, _, length, untruc_length = struct.unpack('<IIII', per_packet_header)
        assert length == untruc_length 

        packet = f.read(length)

        assert struct.unpack('<I', packet[:4])[0] == 2 # ipv4

    print(f'{count} packets parsed')
