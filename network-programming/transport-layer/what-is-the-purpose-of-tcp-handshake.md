With UDP, the kernels don´t need to remember anything about, because there's no functionality in UDP that requires the mantainence of state. But TCP is different. There are certain parameters that needs to be remembered. For example, how long is it typically taking to receive a response (to implemente retransmission).

So, when there is the first SYN, it has a sequence number, say, 1. In the server's response ACK, the sequence will be n+1. 

The handshake then prevents DDOS attacks, for example, the handshake also stablishes the round-trip time.
