Overview of CPU virtualization.

When the OS boots, it loads traps. So when a program needs something from the kernel (privileged space), it needs to make a system call. The system call interacts with the Kernel and runs the procedure there. One interesting thing is that the trap instruction (that is interacting with the kernel) doesn´t expose the memory of the privileged instruction. The kernel understands what the system call need to do and executes that system call that was initialized when the OS booted. This is like this for security reasons: the user space (or unprivileged space) shouldn´t know anything about the memory space of the kernel. So when the kernel finishes executing the call, it `returns from trap` to the user space. But how? For this to happen, the OS must save in the register information about the program running in user space, so it can continue to run the program when it returns from trap.

User "A" Prog. -> "A" wnats OS service (system call) -> issues special intruction (trap / interrupt in x86 specifically) -> jumps into OS -> target: trap handlers (OS booted) -> save register state (to enable resume) -> OS sys call handler: runs call -> return from trap 

--

the OS must have a "process list". Must track different user processes. Per-process info: state (like READY, RUNNING, etc). The OS must track "slow operations" (IO).

Example of tracking slow operations:
prog "A" -> trap (sys call to open) -> OS issues IO to disk -> a slow thing happens... -- In this case, the OS should knwo that this is a slow operation, and, for example, have mechanisms to now run prog "B" while IO happens for prog "A".

The OS tracks these state to achieve efficiency.

OS: from Mechanisms to Policies. 

What should the OS runs?

Highly complicated topic. 

**Runtime to completion**: the OS could simple run each task/process until it completes. It would be insanely inefficient, though. Imagine we have process A, B and C, and it's a FIFO (first in, first out). A runs until completion; then B, then C. Suppose that each one of team takes 100ms to complete. All of them would be completed in 300ms. But what if A runs for 1 minute? Process B and C would be waiting until A completes. So there must be an alternative to this.

**Shortest job first**: Instead, it would be interesting if the OS knew, somehow, the runtime of each job, and had the opportunity to run the shortest job first (SJF). Until now, though, we are assuming that all jobs arrive at the same time. But what if only A is running, and suddenly, like a wild pikachu, B appears? Suppose that B has the shortest run time of the two. What should the OS do? 

**Shortest time to completion first**, in this policy, the OS will, in some cases, stop existing jobs and start a new one. 

New metric: response time. It's the time until a process generates a response; or the time the process first run - time it arrives.

If we take into account the response time metric, the shortest time to completion turns out to be not that good. 

**Round robin**: In this policy, the OS runs a little slice of A, and then slice of B, and C, and then A again... The time that the OS runs the slices are called "quantum" or "time slice". This can work with a timer interrupt period. Example: every 10ms a slice runs. But we have a trade off: if we have short time slices, we have better response times, but tigh context switch overhead. Longer time slices have worse response time, but more efficient (fewer context switches).

Ideas: We like the SJF (STCF) policy, but the OS doesn´t know job lengths. And we would like to take response time into consideration in our policy. 

So how to build a real scheduler that deals with all of these?




