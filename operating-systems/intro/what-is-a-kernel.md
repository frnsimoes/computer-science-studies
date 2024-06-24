It's the core set of functionality in the operating system. It's the code is loaded when the machine is in the boot load process. Deals with: memory virtualization, process scheduling, etc. It's the portion of the operating systems that is loaded into memory at the begining of the boot process.

More formally, the kernel is what's behind the system call interface.

From Shichao notes:
> The interface to the kernel is a layer of software called the system calls.
> Libraries of common function are built on top of the system call interface, but applications are free to use both.
> The shell is a special application that provides an interface for running other applications.

Kernel responsabilities:
- Mediation of I/O devices + driver code
    - Disk I/O
    - Networking
    - Keyboard
    ...
- Process management
    - Origination/launching
    - Lifecycle management
    - Signaling/IPC (What happens when processing ends?)
    - Scheduling
        - Fairness
        - Interactive processes prioritized
        - Multicore

The most simple example of IO:

```c
int main() {
    printf("%s", "hello")
}
```

Curious info by Oz:
> It doesn't feel IO to us, but in the past we have a physical screen situated in a console. The console was a something with a CTR screen, it had wires, like a phone wire, which was connected to a mainframe. And hit is how you would use an operating system with a console. Then it really feel like IO, because the mainframe, the thing that's running the operating system, does I/O. It writes to the terminal interface, goes over the phone line, goes to your terminal in another room or building and displays it.


In this example, the system call that the OS uses to display "hello" in stdout is `write(2)`

When we run `strace <./binary>`, it shows the system calls made to execute the program, including `write(1, "hello", 5hello)

