AIMD (additive increae, multiplicative decrease)
Approach
- senders can increase sending rate until packet loss (congestion) occurs, then decrease sending rate on loss event.
- additive increase: increase rate by 1 maximum segment size every rtt until loss detected.
- multiplicative decrease: cut sending rate in half at each loss event

Slow start:
- when a tcp connection is established, the congestion window (cwnd) is set to a small value, typically the size of one MSS (maximum segment size). 
- the cwnd controls the amount of data tha can be sent before waitinf for an ACK

When should the exponential increase switch to linear?
- when xend gets to 1/2 of its value before timout.
