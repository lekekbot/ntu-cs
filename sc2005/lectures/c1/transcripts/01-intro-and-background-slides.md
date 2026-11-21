# Part 1 — Intro and Background (slide deck S1–S46)

Verbatim deck text of `Part1 (Intro and Background)(1).pptx`, 46 slides; `[NOTES]` = the lecturer’s speaker notes.


## S01

Operating Systems

Part 1:   Introduction

What is an Operating System (OS)?
Types of Computing Systems
Computer System Architecture (Review)
Operating System Services

[NOTES] After introducing the outline of the entire course, we now start the first chapter. In this chapter, we will introduce “what is an operating system” and some representative types of operating systems in computing history, from mainframe systems in the old days to multiprocessor systems in recent years. We will also discuss some special-purpose systems such as real-time systems, handheld systems and embedded/cyber-physical systems. We will also briefly review computer system architecture. 

We will then introduce lots of basic concepts in operating systems. if you are puzzled, fine, you can kee


## S02

Why Learn Operating Systems?

Operating systems (OS-s) are the core of computer systems
Key goal: Hide the system complexity from developers
Why: Simplicity of programming
How: Abstractions, policies, and mechanisms
OS is a foundation to understand advanced systems (e.g., cloud, databases, AI-as-a-Service, Internet-of-Things)
Focus on abstractions and principles not implementation
Why do we need to learn Operating Systems?
System architects require in-depth OS understanding
App. developers at a high level to optimize their software

SC2005 Operating Systems


## S03

Operating Systems

What is an Operating System?

A program that acts as an intermediary between a user and the computer hardware
Two major goals: user convenience and efficient hardware utilization
Hide hardware complexity 
Use hardware in an efficient manner
Smart resource (e.g., Central Processing Unit (CPU), I/O devices, memory) allocation
These two goals can be contradictory
Smart resource allocation may require lot of information about user programs

[NOTES] So, what is the definition of an operating system? It is defined to be a program that acts as an intermediary between a user and the computer hardware. 

In the definition, we need to pay attention to two points. First, operating system is a program. That means, operating system is a piece of software. Not hardware. Second, operating system is an intermediate software between user and computer hardware. That means, when users want to run their jobs, their jobs need to go through operating system, and are then executed on the hardware. On the other hand, when computer hardware needs to return t


## S04

Operating Systems

Computer System Components

CPU, memory, I/O devices

Control and coordinate 
apps & hardware

[NOTES] In this figure, we have the illustration of an abstract view of system components. From bottom up, we have hardware, operating system, application programs, and users. The operating system is in the middle layer of the abstract view.


## S05

Operating Systems

Computer System Components

Hardware: Provides basic computing resources (CPU, memory, I/O devices)
Operating System(OS): Controls and coordinates the use of the hardware among various application programs for various users
Application programs: Defines the ways in which system resources are used to solve computing problems for users (compilers, database systems, video games, business programs)
Users: People, machines, other computers

[NOTES] Let’s look at the position of an operating system in a computer system. A computer system can be roughly divided into four components: the hardware, the operating system, the application programs and the users. 

The hardware provides the basic computing resources such as CPU, memory, and I/O devices. Computers can have quite different hardware, as we will see in the computing history.
The application programs define the ways how the system resources are used to solve the problems. Example application programs include word processors, spreadsheets, video games, etc.
The users can be people, or


## S06

Operating Systems

Operating System Definitions

Resource allocator: Manages and allocates hardware resources

Control program: Controls the execution of user programs and operations of I/O devices

Kernel: The one “core” program that is always ready to accept new commands from the users as well as hardware (all else being application programs)

[NOTES] Based on the abstract view, we can see what an operating system does. 

The operating system is a resource allocator. It allocates resources to different application programs.
The operating system is a control program. It controls the execution of user programs and operations on devices.
We also call operating system Kernel. It is the one “core” program that is always ready to accept new requests from users as well as the hardware.


## S07

Operating Systems

Part 1:   Introduction

What is an Operating System (OS)?
Types of Computing Systems
Computer System Architecture (Review)
Operating System Services


## S08

Operating Systems

Types of Computing Systems

Batch systems

Multiprogrammed and Time-sharing systems
Desktop systems

Embedded and Cyber-physical systems
Real-Time systems
Handheld systems

[NOTES] Now, we give some examples on different types of operating systems. We will introduce them one by one.


## S09

Operating Systems

A Short Review on Computers

In this video, we will briefly review the history of computers

[NOTES] We will have a short review on computers with a video.


## S10

Operating Systems

Simple Batch Systems

Reduce setup time by batching similar jobs
Automatic job sequencing – automatically transfers control from one job to another
Simple memory layout
Only one user job in
   memory at any time point
Not very efficient
When job waits for I/O,
   CPU idles

[NOTES] In the first generation of computing systems, each job has a setup cost, for example, loading the data into the main memory and figure out the memory layout. To reduce the setup cost, the operator often batch the jobs with similar needs. We set up once and runs multiple jobs in a batch. 

The batch system needs to figure out which job to run in the batch. It has a functionality called automatic job sequencing, order the jobs from one job to another automatically. 

Finally, the batch system initially has very simple memory layout (or the data layout in the main memory). Only allow one user pro


## S11

Operating Systems

Multiprogrammed (Time-Sharing) Systems

Several jobs are kept in main memory at the same time, and the CPU is multiplexed among them
A job is swapped in and out of                   memory to the hard disk
System is highly interactive;                              t  supports multiple online users
Examples: desktops, servers

[NOTES] The CPU is multiplexed among the jobs. When a job is waiting for I/O, we will give the CPU to other jobs. For example, we can allow job 1 to run some time and then switch to job 2. Job 2 takes the CPU for some time. later Job 3  and so on.

The memory layout is different from the simple batch system. As you can see, the program data of multiple jobs are stored in the main memory at the same time, instead of a single job in simple batch system.

One question: why are  multiprogrammed systems more advanced than simple batch systems? Efficiency. In multiprogrammed systems, the CPU utilization is 


## S12

Operating Systems

OS Features Needed for Multiprogramming

Memory management: To allocate memory to several jobs

CPU scheduling: To choose among several jobs ready to run

I/O device scheduling: Allocation of I/O devices to jobs

[NOTES] In order to support multiprogramming, what features should the operating system provide? The key point is on scheduling the usage of shared resources: memory, CPU and devices. 

First, memory management. The operating system should have the capability of allocating memory to multiple jobs. We need to allocate the memory for new jobs, and deallocate the memory when a job ends.
The second feature is to decide which job to run. There are many criteria for scheduling. We discuss the topic of CPU scheduling in a later lecture. 
Third, the operating system should know how to allocate the devices to 


## S13

Operating Systems

Time-Sharing Systems

The CPU is multiplexed among several jobs that are in memory
A job is swapped in and out of memory to the disk
On-line communication between the user and the system is provided; when the operating system finishes the execution of one command, it seeks the next command from the user


## S14

Operating Systems

Desktop Systems

Personal computers – computer system dedicated to a single user

Several I/O devices – keyboard, mouse, display screens, printers, etc.

User convenience and responsiveness is the main focus

May run several different types of operating systems (Windows, MacOS, UNIX, Linux)

[NOTES] The batch and time sharing systems are already far away from us. We are already familiar with Windows, MacOS, Unix, Linux etc.  Every day, we are using them. I want to highlight two points here:
First, each PC has many I/O devices: keyboards, mouse, small printer etc. this is different from the traditional/old systems. What is the impact? Hardware driver can be a huge part in the code base.
Second, user convenience and responsiveness is the top goal. Remember that we have two goals for operating system: efficiency and user convenience. Here, desktop systems favor user convenience, for example,


## S15

Embedded and Cyber-physical Systems

What are they? Physical systems whose operations are monitored and controlled by a reliable computing and communication core
Resource constrained: Low power, small memory, low bandwidth, etc.
Domain-specific OSes: Real-time, Handheld, Automotive, Avionics, Industrial Controls, Sensor networks, etc.

Operating Systems

[NOTES] In the next three slides, we will briefly introduce some special purpose systems, real-time systems, cyber-physical systems and handheld systems. 

Cyber-physical systems are typically embedded in another physical system that they monitor and control. Examples include automotive, avionics, medical devices, industrial controls, Internet-of-Things (IoT), smart home devices, future mobility devices, etc. 

These systems are highly resource constrained, and hence the operating system is required to be very efficient. In some cases, user responsiveness is also important, for example in the case of 


## S16

Operating Systems

Real-Time Systems

Used as a control device in a dedicated application such as industrial controls, automotive, avionics, medical devices, etc.
Well-defined fixed-time constraints
Job must be completed within a deadline
Example: Airbag control in cars
Example real-time OSes

[NOTES] Real-time systems have well defined fixed-time constraints on the job execution. Operations must be finished within the defined time constraints, otherwise the system will fail. Widely used as a control device in special applications. For example, some scientific experiments, automotive, avionics, industrial control and display systems.

Real-time systems are generally a subset of embedded and cyber-physical systems; those embedded systems that have stringent timing requirements. 

Some popular Oses are given here. you may not be familiar with those names.  The e-learning lecture (week 7) is a


## S17

Operating Systems

Handheld Systems

Mobile phones, tablets
Issues:
Limited memory
Slow processors
Small display screens
Popular OSes: iOS, Android, HarmonyOS

[NOTES] They are widely used in mobile phones and pads. They can be regarded as a subset of embedded and cyber-physical systems. The popular handheld operating systems include iOS and Android. Compared with the desktop operating systems, the handheld devices have some special issues: 

Memory: Unlike the PC with several GB of main memory, the handheld devices have limited memory. 
The second issue is that the processor speed is slow.
Finally, the display screens are small. The system needs to do some clipping in order to fit the content to the display. 

One of the few systems in which both user respo


## S18

Operating Systems

A Dual-Core CPU Design

[NOTES] Operating system development can be also driven by computer hardware. Recently, we have witnessed that the CPUs can have multiple cores. For example, in this figure, we have a CPU with two cores. The two cores share the main memory. Each core has its local registers and caches.

As the CPU has multiple cores, how the operating system is adapted to the multi-core design?


## S19

Operating Systems

Multiprocessor Systems

Systems with more than one CPU, or CPU with multiple cores (also called multi-core systems)

Tightly coupled systems: Communication usually takes place through shared memory

Advantages of such parallel systems
Increased system throughput
Economical due to sharing of memory and I/O devices (as compared to multiple single CPU systems)
Increased reliability due to redundancy

[NOTES] Multiprocessor systems are targeted towards hardware with more than one CPU, or CPU with multiple cores.

Multiprocessor systems are also known as tightly coupled systems: communication is performed through shared memory. In comparison, loosely coupled systems are OSes running on distributed computers. You will learn them in other courses at higher level. 

Multi-programming: the system can run multiple programs.
Multi-processing: the system can run on multiple CPUs or CPU with multiple cores.

There are multiple advantages of using such parallel systems:
First, of course, it can increase the 


## S20

Operating Systems

Part 1:   Introduction

What is an Operating System (OS)?
Types of Computing Systems
Computer System Architecture (Review)
Operating System Services


## S21

Operating Systems

Computer System Architecture

Computer System Operation

Storage Hierarchy

Hardware Protection

[NOTES] Now, we will start to introduce the computer system architecture, which is essentially a brief review of what you learnt in CE/CZ1006. In computer system architecture, we will introduce computer system operation, then storage hierarchy and then hardware protection.


## S22

Operating Systems

Computer-System Operation

Buffer

Buffer

Buffer

Interrupt

Bus

[NOTES] A modern computer system consists of a CPU and a number of devices , for example, disks, printer etc. these devices are usually connected with a common system bus. 

A device controller is in charge of the operations of a specific type of device.  The CPU and the device controllers can execute concurrently, and compete for the bus cycles.  The device controller usually has a local buffer. The buffer is used to store the data temporarily. 

After the CPU issues an I/O instruction, how does the CPU know the operation is done or not? in operating system, this event is called interrupt. The device


## S23

Operating Systems

Computer-System Operation

I/O devices and the CPU can execute concurrently
Each device controller is in charge of a particular device type
Each device controller has a local buffer
Device controller moves data between local buffer and memory
Device controller informs CPU that it has finished its operation by causing an interrupt

[NOTES] The following concepts are important in computer system operation. We will explain them one by one using a figure.


## S24

Operating Systems

Common Functions of Interrupts

An interrupt transfers control to the interrupt service routine generally through the interrupt vector, which contains the addresses of all the service routines

Incoming interrupts are disabled while another interrupt is being processed to prevent any loss of interrupts

A trap is a CPU generated interrupt caused either by a software error or request
Unhandled exceptions in user program

An operating system is typically interrupt driven
If the OS is not interrupt driven, it would be required to poll for task/event completions

[NOTES] Interrupt is a very important concept in OS. Different operating systems have different interrupt handling mechanisms. But there are multiple common functions for interrupt handling. First, all the interrupt handling routines are fixed, and their addresses are stored in an array called interrupt vector. 

Second, to prevent a lost interrupt, the incoming interrupts are disabled while another interrupt is being handled. That means, we process the interrupt one by one.

Third, the interrupt can be generated from hardware or software. A software generated interrupt is called a trap. Usually, the 


## S25

Operating Systems

Interrupt Handling

The operating system preserves the state of the CPU by storing registers and the program counter
Also called a context switch

It then determines which type of interrupt has occurred
Separate segments of code determine what action should be taken for each type of interrupt

Based on the interrupt type, it identifies the appropriate interrupt service routine to execute
Obtained from the interrupt vector table

[NOTES] There are multiple steps for handling an interrupt. 

First, the operating system must save the state of the current execution: the address of the next instruction (the program counter), the state of the CPU including the registers. You will know more details when we talk about the concept of processes and context switches. 

Second, we determine which type of interrupt has occurred. The system needs to read the CPU register to see the interrupt type. 

Third, the interrupt service routine is executed according to the type of interrupt. How can we find the target interrupt service routine? Int


## S26

Interrupt-Driven I/O Timeline

Job 1

Job 2

OS

Operating Systems

[NOTES] Let’s see one example for interrupt handling. In this figure, we have the timeline of interrupt handling. 
We consider two states for CPU: executing the user process or handling I/O interrupt
Two states for I/O device: idle (nothing to do) or transferring data.

Initially, the I/O device is idle and the CPU is executing the user process, say Job 1. Now, an I/O request is issued, and the CPU continues the execution for another job, say Job 2 (recall multiprogrammed system). After some time, the I/O completes, and an interrupt is issued to the CPU. The disk becomes idle. Then, CPU starts the I/O


## S27

Operating Systems

Direct Memory Access (DMA)

Used for high-speed I/O devices that are able to transmit information at close to memory speeds

OS sets up the memory blocks, counters, etc.

Device controller transfers data blocks from buffer to main memory without CPU intervention

Only one interrupt is generated per block, rather than one interrupt per byte

[NOTES] Interrupt driven I/O may cause too many interrupts. Consider that you want to copy 1 TB of data, and each byte causes an interrupt in the worst case. On the other hand, interrupt has considerable overhead in saving the state and resuming execution. The overhead can be larger for high-speed I/O devices such as solid state drives. There must be some mechanism to reduce the number of interrupts. Direct memory access, DMA, is a common technique. 

In DMA, the operating system sets up the buffer, pointers, and counters once. And then, the device controller transfers blocks of data from the buffer d


## S28

Operating Systems

How a Modern Computer Works

[NOTES] With the concept of interrupt, let’s see how a modern computer works. We have three parties: CPU, memory, and device. The memory stores the instructions and data. A job execution fetches instructions from the memory, and read/write data from/to the memory. After the CPU issues an I/O request to the device, the device will notify the CPU when the data is ready. Depending on whether interrupt driven I/O or DMA is used, the data buffer location is different. If DMA is used, the data is stored in the memory. Otherwise, the CPU can get the data directly from the device buffer.


## S29

Operating Systems

Storage Hierarchy

Memory Hierarchy: CPU registers, CPU caches, main memory, hard disk …
Storage system organization based on 
speed
cost
volatility
size
Caching: Copying information into faster storage system; main memory can be viewed as the last cache before secondary storage

This slide is not examinable.

[NOTES] In our last lecture, we stopped here. First of all, let’s review our previous lecture. We started with multiprogramming systems. Multiprogramming means that the system can run multiple jobs at the same time. We then talk about multi-processing systems. Multiprocessing means the system can run on multiple CPUs or CPU with multiple cores. Then, we learnt one important concept: interrupt. About the interrupt, you should know about the steps on how OS handles an interrupt. Also, the difference between interrupt driven I/O and DMA.

We now have a quick introduction on memory hierarchy. The modern c


## S30

Operating Systems

Storage/Memory Hierarchy

This slide is not examinable.

[NOTES] This figure shows the storage device hierarchy in modern computers. From top down, we have registers, cache, memory, disk, tapes etc. From top down, the cost decreases, the speed also decreases, the size increases. The levels above main memory (including main memory itself) are volatile; the layer below is non-volatile.


## S31

Operating Systems

Hardware Protection

Dual-Mode Operation

I/O Protection

Memory Protection

[NOTES] Hardware resources need to be protected. Recall that OS must control and coordinate the access to hardware. However, in practice, a malfunctioning program may issue illegal I/O instructions, accessing memory locations of the operating system. The operating system should provide protections in hardware to avoid such scenarios. So, we will first introduce the concept of dual-mode operation, and then, see how the concept of dual-mode operation can be used to implement I/O and memory protection.


## S32

Operating Systems

Dual-Mode Operation

Provides hardware protection by differentiating between at least two modes of operations

User mode: Execution of user processes

Monitor mode (supervisor mode or system mode or kernel mode): Execution of operating system processes

[NOTES] Because there can be illegal accesses, for example, virus from applications, we should distinguish the execution whether it is simple normal execution from user process, or whether the execution will access the hardware or other important data structures in OS. In the latter case, we must make sure the execution does not issue illegal operations to hardware and data structures of OS.

In the user mode, we execute user processes; in the monitor mode, we execute the operating system processes (or kernel). Interrupt handling is an example of operating system process.


## S33

Operating Systems

Dual-Mode Operation (Cont.)

Mode bit added to computer hardware to indicate the current mode:  monitor (0) or user (1)
When an interrupt or trap occurs hardware switches to monitor mode

Privileged instructions can be used only in monitor mode

[NOTES] Modern hardware supports a bit named mode bit to indicate the two modes of operations. A bit value of zero means monitor mode; a bit value of one means user mode. 

Let’s see how the system transitions between these two modes. Suppose we are in the user mode, executing the user process. When a trap or interrupt occurs, the system will switch to the monitor mode automatically (controlled by hardware and not OS). This is because the CPU will execute the interrupt service routine, which is the code in operating system and access the data structures in OS. After handling the trap or the interrupt,


## S34

Kernel mode vs. root/admin.

Are they the same?
No, they are not the same

Kernel or user mode is a hardware operation mode

Root/Administrator is a user account in an OS
Jobs still execute in user mode, even when executed by a root/admin. user
This user may execute code in kernel mode indirectly  e.g., by loading a kernel module

Operating Systems


## S35

Operating Systems

I/O Protection

A user program may issue illegal I/O operation; hence I/O must be protected
Case 1: read a file that does not exist
Case 2: unauthorized access to a device

All I/O instructions are privileged instructions 

All I/O operations must go through the OS to ensure its correctness and legality
CPU generates a trap for I/O operations that try to bypass the OS

[NOTES] Suppose we have a user program with computation and I/O. The normal computations are in the user mode. After some time, the process issues an I/O request and the process waits for I/O to complete. After the I/O is done, the interrupt service routine is executed. That is the OS code, and thus, it is in monitor mode. After the interrupt service routine is done, we resume the computation in the user process.


## S36

Operating Systems

Memory Protection

Must provide memory protection, at least for the interrupt vector and the interrupt service routines

Two CPU registers determine the range of legal addresses a program may access:
Base register: Holds the first legal physical memory address
Limit register: Contains the size of legal range

Memory outside the defined range is protected and cannot be accessed

[NOTES] We need to protect the memory in many ways. For example, we must protect the interrupt vector and the interrupt service routines in OS.  If those data and instructions are changed, the operating system will go wrong. For example, a virus can intentionally change those data structures to do the wrong things. 

The functionality of memory protection is to protect the memory space of a process from being modified by other processes.  

The basic idea is to define the memory area for each program. In particular, add two special registers that determine the range of the memory addesses that a progr


## S37

Operating Systems

Memory Protection (Cont.)

[NOTES] Let’s look at one example of memory protection. We consider this memory layout. Btw, is it a simple batch system? No. it is multiprogrammed system.
Here, the base is 300040, the limit is 120900. therefore, the memory range for job 2 is from 300040 to 420940.


## S38

Operating Systems

Memory Protection (Cont.)

The load instructions for the base and limit registers are privileged instructions (only in monitor mode)

CPU issues a trap to the OS if above checks fail

e.g., Load/Store
(address)

[NOTES] let’s see how the memory protection is performed. Given a memory address to access, we first check whether it is larger than the base register. If failed, a trap is issued to the operating system. This addressing error is a segmentation fault in Linux. Then check whether the address is smaller than the sum of (base and limit) registers. Again, if failed, a trap is generated. If both tests are passed, the memory access is issued to the main memory.

Why the loading instructions for base and limit are privileged instructions? loading means loading the values from main memory to CPU registers. OS


## S39

Operating Systems

Part 1:   Introduction

What is an Operating System (OS)?
Types of Computing Systems
Computer System Architecture (Review)
Operating System Services


## S40

Operating Systems

A View of Operating System Services

[NOTES] We will have a quick introduction on operating system services. In this figure, we look into the internals of an operating system. Operating system has multiple layers: user interfaces, system calls, and services. To allow users to access the operating system services, a set of API is offered. Those APIs are called system calls. The services include program execution, file system etc. Again, if you are puzzled about some terms, don’t worry, we will introduce them in later lectures. 

One set of operating-system services provides functions that are helpful to the user:
User interface - Almost a


## S41

Operating Systems

System Calls

System calls provide the interface between a user program and the operating system
Generally available as assembly-language instructions
Possible to replace assembly language for systems programming to allow system calls to be made directly (e.g., in C/C++)

The execution of a system call requires the switch from the user to the kernel mode

[NOTES] We now focus on the system calls.

They are generally available as assembly language instructions, and now system calls in high level languages such as C is also available. For example, those system calls in UNIX and Windows can be directly invoked in C and C++.

The execution of a system call requires the switch from the user to the kernel mode.


## S42

Operating Systems

API – System Call – OS Relationship

#include <stdio.h>
main() 
{
FILE *fp;
…
fp = fopen(…);
…
}

FILE *fopen(…)
{
Int fd;
…
fd = open(…);
…
}

API
(standard C library)

System Call

[NOTES] Let’s see one example on the details of executing a system call. This is a C program, which opens a file. It uses fopen(). It is similar to opening a file in java. The implementation actually consists of a system call, open. Now, before the system call is executed, we change the mode from user to kernel. Why? All the I/O instructions are privileged instructions, and they must be executed in the kernel mode. Then, we allocate the instructions of open() and execute the open() system call. When it is done, we need to get back to user mode and continue the execution of user process. In summary, ho


## S43

System Call Processing (CPU to Device)

CE2005/CZ2005 Operating Systems

User code

OS code

❶Program’s code executing

❷Invoke system call

❸Execute system call

❹Continue executing program’s code

User program

Device

Trap!


## S44

Interrupt Processing (Device to CPU)

CE2005/CZ2005 Operating Systems

❶Program’s code executing

❷Process the interrupt

Interrupt!

❸ Continue executing program’s code

User program

Device

User code

OS code


## S45

Operating Systems

Advanced Readings

Mobile operating systems
Apple iOS, http://en.wikipedia.org/wiki/IOS
Google Android, http://en.wikipedia.org/wiki/Android_(operating_system)

“History of Operating Systems”, by Ayman Moumina (pdf in NTULearn)

[NOTES] Those are advanced readings, if you want to know more beyond the text book.


## S46

Operating Systems

Future Operating Systems

Operating systems are not limited to Windows/Linux/MacOS etc.

Operating system development never stops
Changes in hardware
Changes in user requirements

Examples:
Unikernel, https://en.wikipedia.org/wiki/Unikernel
Formally verified OS kernel, https://sel4.systems/

[NOTES] Those are advanced readings, if you want to know more beyond the text book.
