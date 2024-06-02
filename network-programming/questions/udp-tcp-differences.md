Differences:
- TCP is connection-oriented, it establishes a connection between the sender and receiver before transmitting data. UDP is connectionless, data packets are sent without establishing a connection.
- TCP ensures reliable delivery of data by using acknowledgements, retransmissions, and sequencing. UDP does not guarantee delivery or sequencing of packets. 
- TCP implements flow control and congestion control mechanisms to manage the rate of data transmission and avoid network congestion. UDP does not have this functionallity builtin.
- TCP headers are larger then UDP headers.
- TCP is commonly used for applications that require reliable and ordered delivery of data, such as web browsing, file transfer (FTP) and remote login (SSH). USP is used for realtime applications like streaming, VoIP, gaming, DNS.

Similarities:
- Both are packet-based protocols, where data is transmitted in discrete units called packets or datagrams.
- They both operate at the transport layer of the OSI model and provide communication services to higher-layer protocols and applications.
- Both use a 16-bit checksum field in the header to detect errors in the packet during transmission
- Borth use port numbers to identify different applications or services running on devices, allowing multiple applications to use network resources simultaneously.

Check this out: https://deepplum.com/post-b/
> UDP was actually “designed” in 30 minutes on a blackboard when we decided pull the original TCP protocol apart into TCP and IP, and created UDP on top of IP as an alternative for multiplexing and demultiplexing IP datagrams inside a host among the various host processes or tasks. But it was a placeholder that enabled all the non-virtual-circuit protocols since then to be invented, including encapsulation, RTP, DNS, …,  without having to negotiate for permission either to define a new protocol or to extend TCP by adding “features”.



Looking in retrospect, though, UDP is kinda of genius, since this skinless protocol is the bases of QUIC, which is the base of HTTP/3
