Process: instance of a running program.

If we have two processes, their have their own address space, and these addresses are going to be mapped by the OS to their own physical addresses independently of one another. They can both be scheduled on the CPU independently of one another. 

The goal is to share memory between processes, independently of the scheduler. 

A process has two schedulable units. So we have a process that has two threads, and the process has only one address space in memory. So the two threads share the same address space.

Thread is something that shares certain memory areas, but is independently scheduled. 

The linux approach: Let's not talk about these as processes and threads. Let's just make every one of these a task. And a task can be scheduled, a task can be run, a task has state (running, waiting, sleeping, zombie, etc). Tasks could share memory mappings. 

https://github.com/torvalds/linux/blob/master/include/linux/sched.h

A task has a pointer to `mm`, which is the memory mappings. If you create a child by using pthread_create, it will be a new task with the same memory mappings, because it is a thread. If you create a child with forks, it will be a child with new memory mappings (with a copy of the parent's memory mappings). 

The stack is separated from memory mappings, though. Why?  Two tasks always need they own stacks. If they can be scheduled separately. Until now, we are talking about OS threads / POSIX threads. 

Nodejs: the nodejs runtime is only one process. The async is operating in only one thread. All those async functions are shceduled on the CPU. The OS sees only one nodejs thread. The nodejs runtime decides what pieces are going to run at each time.

Asyncio Python library: the same thing happens.

Goroutines: One go program, running as a process, has actual posix threads. However, it's the Go runtime that maps the goroutines in threads.
