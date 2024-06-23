It's the core set of functionality in the operating system. It's the code is loaded when the machine is in the boot load process. Deals with: memory virtualization, process scheduling, etc. It's the portion of the operating systems that is loaded into memory at the begining of the boot process.

More formally, the kernel is what's behind the system call interface.

From Shichao notes:
> The interface to the kernel is a layer of software called the system calls.
> Libraries of common function are built on top of the system call interface, but applications are free to use both.
> The shell is a special application that provides an interface for running other applications.
