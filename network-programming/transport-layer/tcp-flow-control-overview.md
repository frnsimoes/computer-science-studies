- point-to-point: one sender, one receiver
- reliable, in-order byte stream abstraction: no message boundaries
- full duplex data:
    - bi-directional data flow in same connection
    - mss: maximum segment size

- cumulative ACKS
- pipelining: TCP congestion and flow control set window size
- connection-oriented: handshaking (exchange of control messages) initializes sender, receiver state before data exchanger.
- flow controlled: sender will not overwhelm receiver

TCP segment structure, the interesting parts:
- sequence number: byte stream number of first byte in segment's data
    - counting butes of data into bytestream (not segments).
- ACK: sequence number of next byte expected from other side
- internet checksum: error detection
- RST, SYN, FIN: connection setup, teardown
- window size: flow control. The receiver can tell the sender the number of bytes its willing to accept
- congestion control: sender limits transmission rate based on network congestion

TCP sequence numbers and ACKs:
- sequence numbers: byte stream "number" of first byte in segment's data
- ACK: sequence number of next byte expected from other side
- ACK generation:
    - delayed ACK: wait up to foo ms for next segment
    - ACK every other received segment
    - ACK immediately if segment has FIN
    - ACK immediately if segment has no data

Simple flow:
- sender: SEQ=42, data='C', ACK=79
- receiver: ACK=79, data='C', SEQ=43
- sender: SEQ=79, ACK=80

How should the timeout be set?
- too short: premature timeout, unnecessary retransmissions
- too long: slow reaction to segment loss

How to estimate RTT?
- sample RTT: measured time from segment transmission until ACK receipt
- RTT will vary. Avarage several recent measurements, not just the last RTT measurement
- Exponential weighted moving average:
    - EstimatedRTT = (1-a) * EstimatedRTT + a * SampleRTT
    - a=0.125

TCP sender (simplified):
- event: data received from application layer
    - create segment with sequence number
        - sequence number is byte-stream number of first data byte in segment

    - start timer if not already running
        
- event: timeout
    - retransmit segment that caused timeout
    - restart timer

- event: ACK received
    - if ACK acknowledges new data
        - update what is known to be ACKed
        - start timer if there is unACKed data

