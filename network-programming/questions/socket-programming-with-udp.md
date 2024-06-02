From the Kurose book:
> Before the sendin process can push a packet of data out the socket door, when using UDP, it first attach a destination address to the packet. After the packet passes through the sender's socket, the Internet will use this destination address to route the packet through the internet to the socket in the receiving process. When the packet arrives at the receiving socket, the receiving process will retrive the packet through the socket, and then inspect the packet's contents and take appropriate action.

Three steps:
- before pushing the data out the socket door, attach a destination adress to the packet.
- after the packet is released from the sender's socket, the internet uses the destination adress to route the packet.
- the reciving socket receives and handles the packet.

What goes in the address of the first step?
- the destination IP.
- Because the destination machine might be busy with other processes, using one or more sockets, also a port.
- the sender's source address and port also goes in the address.
