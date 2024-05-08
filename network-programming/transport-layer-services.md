What are the services that a transport layer protocol can offer to applications invoking it?

**Reliable Data Transfer**
It guarantees that the data sent by one end of the application is delivered correctly and completely to the other end of the application. When a protocol provices this service, the sending process can just pass its data into the socket and know with complete confidence that the data will arrive without errors at the receiving process. (ref. Kurose & Ross)

**Throughput**
Applications that are bandwidth-sensitive applications. For example, if an internet telephony application encodes voice at 32kbps, it needs to send data into the network and have data delivered to the receiving application at this rate. If the trannsport protocol cannot provide this throughput, the application would need to encode at a lower rate (and receive enough throughput to sustain this lower coding rate) or may have to give up, since receiving, say, half of the needed throughput is of little or no use to this internet telephony application. (ref. Kurose and Ross)

In contraposition, there are elastic applications. These applications can make use of as much, or as little, throughput as happens to be available. Eletronic mail, file transfer, and web transfers are all elastic applications. 

**Timing**
A transport-layer protocol can also provide timing guarantees. As with throughput guarantees, timing guarantees can come in many shapes and forms. An example guarantee might be that every bit that the sender puymps into the socket arrives at the receiver's socket no more than 100 msec later. Really important to low delay tolerant applications, such as telephony, streaming, only games, etc.

**Security**
Services like encrypting and decrypting data before sending / receiving.
