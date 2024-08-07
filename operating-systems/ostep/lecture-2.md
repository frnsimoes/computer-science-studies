Overview of CPU virtualization.

When the OS boots, it loads traps. So when a program needs something from the kernel (privileged space), it needs to make a system call. The system call interacts with the Kernel and runs the procedure there. One interesting thing is that the trap instruction (that is interacting with the kernel) doesn´t expose the memory of the privileged instruction. The kernel understands what the system call need to do and executes that system call that was initialized when the OS booted. This is like this for security reasons: the user space (or unprivileged space) shouldn´t know anything about the memory space of the kernel. So when the kernel finishes executing the call, it `returns from trap` to the user space. But how? For this to happen, the OS must save in the register information about the program running in user space, so it can continue to run the program when it returns from trap.

User "A" Prog. -> "A" wnats OS service (system call) -> issues special intruction (trap / interrupt in x86 specifically) -> jumps into OS -> target: trap handlers (OS booted) -> save register state (to enable resume) -> OS sys call handler: runs call -> return from trap 

--

the OS must have a "process list". Must track different user processes. Per-process info: state (like READY, RUNNING, etc). The OS must track "slow operations" (IO).

Example of tracking slow operations:
prog "A" -> trap (sys call to open) -> OS issues IO to disk -> a slow thing happens... -- In this case, the OS should knwo that this is a slow operation, and, for example, have mechanisms to now run prog "B" while IO happens for prog "A".

The OS tracks these state to achieve efficiency.

OS: from Mechanisms to Policies. What should the OS runs?
