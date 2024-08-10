Back to scheduler and policies.

The goal is to study the multi-level feedback queue, used in Unix systems.

But how? Maybe we could use the past to predict the future? What can we know about the program to be runned?

**Multi-level feedback queue**: policy with many queues. A job is on one queue at any give time (and this might change over time). Each queue has a priority.

Rules: 
1) if priority (A) > Priority (B): A runs (and B doesn't).
2) If priority (A) == Priority (B): round robin between them.
3) where to start: with the highest priority.
4) if processes uses time slice @ given priority, then at the end of the time slice, move down one level in the queue.

Let's suppose a scenario where we have a job A with a long runtime and smaller jobs C1, C2, C3 with short runtimes. Three queues: Q0, Q1, Q2. Q0 has the highest priority.

-> A begins at Q0. -> Runs a little bit -> Goes to Q1 -> runs a little bit -> Goes to Q2 -> C1 appears -> A stops -> C1 runs at Q0. C1 finishes. ->  A runs at Q2 -> C2 appers -> A stops...

This has a big problem. If an infinite number of short jobs that will only run at the highest priority queue (in this case, Q0), A will never be resumed. Starvation for A.

So, how to to ensure long-running jobs make progress? How to avoid starvation?

General idea: once in a while, long-running jobs need to move up in priority

Rule: every T seconds, move all jobs to the highest priority. Beneficial side effects of this rule: the nature of the job might change. This allows the scheduler to relearn something about the job periodically.


About IO: naive rule: if the job runs for < time slice, stay at the same level. This arises the problem of "gaming the scheduler", though, that a job is always running < time slice.

Solution: better accounting: if a job uses up quantum, it moves down.

### Virtual memory

Goals: provide a large memory to each process; provide a privated (protected) memory to each process; efficient memory to each process. It's a good thing that the processes have an address space of 32-bit or 64-bit, this allows easy of use. Imagina if a process only had, like, 100k of AS, what would happen? Somehow, if the program needed to use too much space (think of a big linked list), it would have to carve some new space in, say, disk, or whatever. So giving the illusion of a big address space allows ease of use. One thing that is left to be discovered is: address space != real memory space, so what happens when physical memory space is "full", even though the program has the illusion it's not?

Protection allows isolation of memory spaces, so process A cannot have access to process B in memory data.

Mechanisms: hardware + os support

Memory access: instruction fetch; explicit loads, stores.

Address translation: how to place these address spaces (or pieces of it) in physical memory? On every memory reference, we are going to translate the virutal memory address from the process into a physical memory address where that data resides.

But how does the OS translate the illusion of multiple memory spaces into physical memory addresses? One possibility is the MMU (Memory management unity). The MMU has two registers: the base and the bounds. The base represents the address in physical memory where the address space of the currently running process starts. 

What goes inside the MMU is the virtual address that the program generates. (Every address we see in a program is the virtual address). But how? The MMU takes the base value (the start) and adds the virtual address (length?). So: base + virt address.

The bounds gives us protection. Check we are within address space. If the memory is not "in bounds", if it's not OK to access that memory space, the hardware raises an exception. (Illegal memory access). 

The bads of base and bounds: hard to allocate memory because you have to always find large chunks of memory (to allocate contiguous memory); hard to expand. Hard to share memory

