# Part 2 — Processes and Threads (slide deck S1–S40)

Verbatim text of `Part2 (Process and Threads).pptx`, 40 slides; lines beginning `[NOTES]` are the speaker notes.

## S01

Course Overview

Operating Systems

OS goals

CPU management

Memory management

Filesystem management

Synchronization (L5-6)
Deadlocks (L7)

I/O & disk (L12)

Processes (L2)
Scheduling (L3)

Filesystems (L11)

Memory organization (L8)
Virtual memory (L9-10)

Special: Real-time OS & virtualization


## S02

Operating Systems

Part 2:  Processes and Threads

Process Concept
Process Scheduling
Operation on Processes
Interprocess Communication
Threads

[NOTES] From this lecture on, we will start to introduce the system services and components one by one. We start with processes and threads. 

In our last lecture, we stopped here. Before starting today’s lecture, let’s review what we have learnt. We start with DMA and then hardware protection. You should be able to tell the difference between interrupt driven I/O and DMA. We next spoke about how we use privileged instructions to implement hardware protections. You should be able to tell how privileged instructions are used to implement I/O and memory protections. Then, we spoke about operating system


## S03

Operating Systems

Process Concept

Process: A program in execution; process execution must progress in a sequential fashion

An operating system executes a variety of processes
Batch system – jobs
Time-sharing system – user programs & commands

Textbook uses the terms job and process almost interchangeably (Job = Process)

[NOTES] So what is a process? There are many similar terms in operating system. An operating system executes many kinds of programs: a batch system executes jobs. A time sharing system executes user programs and commands. 

The textbook uses job and process interchangeably. Here, Job=process. Formally speaking, process is a formal term for operating system; and a job is a larger concept.

A process is defined to be a program in execution. It is a dynamic concept. Process is different from program. The program is an executable file (static concept). If you click the executable (that is the program) mul


## S04

Operating Systems

Process in Memory

Base

Base + Limit

(code section, program)

(global parameters)

(all dynamically allocated variables, 
e.g., a=new int[10])

(parameters and local variables 
in a function)

Recall base and limit registers from memory protection?

[NOTES] This figure shows the memory layout of a process. It has four sections: text, data, heap and stack. The memory region is defined from Base to Base+limit. Remember those two registers from memory protection slides? 

The text and data sections are usually at the bottom, because they are fixed during runtime. Text is for the code and data is for global variables. In C/C++ and java, you can declare global variables. They are allocated in the data section.
Stack and heap are two dynamically growing sections. Stack grows from top down, for parameters and local variables in a function call. Consider


## S05

Operating Systems

Process State

As a process executes, it changes state

New: The process is being created

Running: Instructions are being executed

Waiting: The process is waiting for I/O or event

Ready: The process is ready to run, but is waiting to be assigned to the CPU

Terminated: The process has completed

[NOTES] As a process executes, it changes state. A process can have five states: new, running, waiting, ready and terminated. Let’s use a figure to illustrate the process state transitions. Note, in both ready and waiting, the process is waiting, although for different reasons. It is waiting in the ready state to be allocated to the CPU by the OS scheduler, whereas it is waiting in the waiting state for some operation to complete.


## S06

Operating Systems

Diagram of Process State Transitions

Timer interrupt is used in multiprogramming systems to switch between ready processes

[NOTES] This figure is very important. When a process is being created, its state is new. Then, it is admitted into the system, when the initialization is done (for example, the memory region and other resources are allocated). And it becomes ready for scheduling. The state is ready. In practice, there can be multiple processes that are ready to execute on the CPU. Then, OS chooses a ready process to execute, that is scheduler dispatch. The selected process changes its state from ready to running. We will talk about the details on process scheduling, that is, which process to select next week. 

The t


## S07

Operating Systems

Process Control Block (PCB)

[NOTES] In the main memory, PCB is laid out in this manner. If we need to change the process state, we need to change the corresponding field.


## S08

Operating Systems

Process Control Block (PCB)

Keeps information associated with each process

Pointer to other PCBs (PCBs are maintained in a queue/list structure)
Process state
Process number (process id)
Program counter (pointer to the next instruction)
CPU registers
Process priority (used in process scheduling)
Memory management information (e.g., base and limit register values)
Information regarding files (e.g., list of open files)

[NOTES] The processes take turn to use the CPU, according to the timer interrupt or I/O/event wait. How does OS support this switch?

We need to use some data structure to maintain the state of the process. The data structure is called PCB, process control block. PCB includes
Pointer to other PCB, because in OS, PCBs of all processes are maintained in a queue structure.
Process state
Process id,
Programmer counter: the address of the next instruction to be executed.
A series of CPU registers.
CPU scheduling information like priority.

Where is PCB stored? Each process has its PCB stored in the main me


## S09

Operating Systems

PCB and Processes in Main Memory

Base

Base+ Limit

PCB1

PCB2

PCB3

PCB4

Memory area for OS (kernel space)

Memory regions for user processes 
(user space)

[NOTES] Let’s put the concepts together. Let’s first look at PCB and memory layout. The entire main memory is divided into two parts: memory area for OS (kernel space) and memory regions for user processes (user space). PCBs are stored in kernel space for protection. The base and limit defines the memory region for a process. The process memory is stored in user space. 

Changes to PCB must happen in kernel mode.

Here let me give you one question: suppose PCB1 belongs to Process 1. What happens if Process 1 executes the code “a=new int[10]”, that is to allocate one new array? The heap of Process 1 gr


## S10

Operating Systems

Part 2:  Processes and Threads

Process Concept
Process Scheduling
Operation on Processes
Interprocess Communication
Threads


## S11

Operating Systems

Context Switch Between Processes

timer

timer

[NOTES] First, let’s talk about CPU switch, also called context switch. In a time sharing system, every 100ms, there is a timer interrupt generated, and the running process gives up the CPU. Then, another process is picked to run on the CPU. 

This is one example of context switch.  We have two processes P0 and P1. The operations of OS is shown in the middle. At the beginning, P0 is executing. Then, an interrupt occurs (for example, the timer interrupt occurs). P0 will transit from running to ready, and OS should schedule another process for execution. The operating system takes control at this point.


## S12

Operating Systems

Context Switch

When CPU switches to another process, the system must save the context (i.e., information) of the old process and load the saved context for the new process

Context switch time is overhead: The system does NO useful work while switching between processes


## S13

Operating Systems

Process Scheduling Queues

Job queue: Set of all processes with the same state in the system
Ready queue (processes in ready state), device queue (processes in waiting state and waiting for a specific I/O device), etc.

All the queues are stored in main memory (kernel memory space)

Process migrates between queues when its state changes

[NOTES] Now, let’s talk about process scheduling. But before that, let’s see how OS organizes processes. 

The operating system uses the queue structure to maintain all the processes with the same state in the operating system. These queues are called job queues. Therefore, a single job queue contains all the processes with the same state in the system. 
The ready queue is a set of all processes in the ready state. That is, the processes in the memory, ready and waiting for CPU execution. Note: it is not waiting state. It is just waiting for CPU, not I/O or other events.
There is a device queue for ea


## S14

Operating Systems

Ready Queue And Various I/O Device Queues

[NOTES] This is an illustration about the ready queue and device queues.

Each queue structure is located at the queue header. In the queue header, there is a head pointer to the first PCB in the queue, and a tail pointer to the last PCB in the queue.

You can also see that there is a device queue for each device. We can judge whether a device is busy or not from the length of the device queue. For example, mag unit 0 is idle, and disk unit 0 is relatively busy, with three processes waiting for I/O. 

PCB7 is running. We usually store the PCB of the running process as the first element of the ready qu


## S15

Operating Systems

Process Schedulers

We need multiple schedulers for different purposes 
Long-term scheduler (or job scheduler): Selects processes from disk and loads them into main memory for execution
Short-term scheduler (or CPU scheduler): Selects from among the processes that are ready to execute, and allocates the CPU to one of them
Medium-term scheduler:
When the system load is heavy, swaps out a partially executed process from memory to hard disk 
When the system load is light, such processes can be swapped back into main memory

[NOTES] Summary of last lecture: A process is a program in execution. You should be able to tell the difference between program and process. Then, we spoke about process state transition. You should be able to understand each state transition in the transition diagram. Then, we have spoke about process control block or PCB. Then, we studied how PCB and process state changes during a context switch. 

Consider a user clicking an executable many times. Ideally, one click will create one process. However, each process needs some main memory and other resources. Thus, a machine can only support a limited 


## S16

Operating Systems

Process Schedulers (Cont.)

Short-term scheduler is invoked frequently (e.g., 100 milliseconds) in a multiprogrammed system for responsiveness and efficiency purposes

Long-term scheduler is invoked infrequently (e.g., seconds or minutes)

The degree of multiprogramming is initially controlled by the long-term scheduler, and thereafter by the medium-term scheduler

[NOTES] As the name suggests, short-term scheduler is invoked very frequently. It must be fast in making decision.

In contrast, the long-term scheduler is very infrequent. We can do very advanced prediction on the memory usage. See the second half of the course.

The long-term scheduler controls the degree of multiprogramming initially. Then medium-term scheduler does a similar job after that, by swapping in/out processes. 

Degree of multiprogramming is the number of processes in the main memory that can be supported by a multiprogrammed system.


## S17

Operating Systems

Part 2:  Processes and Threads

Process Concept
Process Scheduling
Operation on Processes
Interprocess Communication
Threads


## S18

Operating Systems

Process Creation

Parent process creates children processes, which, in turn create other processes, forming a tree of processes (fork)

Root process

Console 1

Console 2

swap

flush

Unzip

Search

[NOTES] Now, we talk about process creation and process termination. 

Operating system provides system calls to create a child process. So, the parent process can create a child process, and the child process can create its own child process. The relationship forms a tree. Thus, all the processes are the children of a root process. Then, users may open different consoles and create more processes for their command. There may also be some background processes that are automatically created by the root when the system starts, such as swap (used in the mid-term scheduler) and flush (for writing dirty pa


## S19

Operating Systems

Process Creation (Cont.)

Two possible execution orders
Parent and children execute concurrently     (and independently)
Parent waits until all children terminate (wait(),join())

Examples
Many web browsers nowadays fork a new process when we access a new page in a “tab”
OS may create background processes for monitoring and maintenance tasks

[NOTES] There are two execution orders for parent and child processes. One is to execute concurrently (independently). The other is that parent waits until children terminate. Remember in the process state transition, we have one event wait, causing a process transiting from running to waiting. The parent calls a system call wait, and its process state becomes waiting. Its state will change to ready when the child process finishes execution. In Nachos, the API is join . You can check out the lab briefing slides and video.


## S20

Operating Systems

Process Termination

Two possible ways to terminate a process

Exit: Process executes last statement and asks the OS to delete it
A child may output return data to its parent
Process resources are de-allocated by the OS

Abort: Parent may terminate execution of children processes at any time
Child has exceeded allocated resources
Task assigned to child is no longer required
Parent is exiting

[NOTES] Usually, a child process is not allowed to kill the parent process. OS typically kills a child process if its parent process terminates. This is called cascaded termination.


## S21

Operating Systems

Part 2:  Processes and Threads

Process Concept
Process Scheduling
Operation on Processes
Interprocess Communication
Threads


## S22

Operating Systems

Cooperating Processes

An independent process cannot affect or be affected by the execution of other processes

A cooperating process on the other hand can affect or be affected by the execution of other processes
Such processes have to communicate with each other to share data
Two models of Inter-Process Communication (IPC)
Message passing
Shared memory

[NOTES] So far, we have talked about the operations for a single processes. Now, we talk about two or more processes working together. Two processes can be independent or cooperating. Two cooperating processes usually have shared data, and they communicate with each other.


## S23

Operating Systems

IPC Models

Message Passing

Shared Memory

User space

Kernel 
space

[NOTES] Let’s use one figure to illustrate the communication models. Figure (a) is message passing and (b) is shared memory. 

In figure (b), Process A updates the data in the memory buffer, and process B reads the data from this shared buffer (shared variables). The communication is done by using memory read/write operations. The address of the shared memory should be known to both the processes. So, it is in user space.

In figure (a), Process A puts a message in a storage named “mailbox” in the kernel space (that is, copy a message from A to kernel space). Process B can take the message from the ke


## S24

Operating Systems

IPC – Message Passing

Processes communicate and synchronize their actions without resorting to shared variables

Two operations (system calls) are required
send(message) – message size fixed or variable 
receive(message)

If two processes wish to communicate, they need to
Establish a communication link between them
Exchange messages via send/receive

[NOTES] Message passing is a mechanism for processes to communicate and to synchronize their actions without shared variables. Message passing is more flexible. Shared variables are usually for a single machine. Message passing is more general, and can be used for distributed systems.
 
If two processes P and Q wish to communicate, they need to (a) establish a communication link between them, and (b) send and receive messages with the send/receive APIs.


## S25

Operating Systems

Direct vs. Indirect Message Passing

Direct: Processes must name each other explicitly
send (P,message): Send a message to process P
receive(Q,message): Receive a message from process Q

Indirect: Messages are sent to or received from mailboxes (also referred to as ports)
Mailbox is an object into which messages are placed and removed (like a queue)
Primitives are:
send(A,message): Send a message to mailbox A
receive(A,message): Receive a message from mailbox A

[NOTES] There are many implementation details for message passing. I have condensed those details and focus on two key important methods: direct and indirect communication for message passing. 

Direct communication means to send and receive with the explicit name of processes, and indirect communication does not have this requirement. In indirect communication, a mailbox is used. The mailbox is an object where messages are placed and removed. The mailbox can be implemented as a queue structure. Each mailbox has a unique id so that senders and receivers can identify the mailbox. Processes can communic


## S26

Operating Systems

Producer-Consumer Process Paradigm

Classical paradigm for cooperating processes
Producer process produces information that is consumed by a consumer process
Shared buffer used for storing information

Two models for shared buffer
unbounded-buffer places no practical limit on the size of the buffer
bounded-buffer assumes that there is a fixed buffer size

[NOTES] Let’s see one example of the classical producer-consumer problem. It is a basic paradigm for cooperating processes. There are many producer-consumer examples in our daily life. For example, the manufacturers produce products and consumers buy the products. Thus, the manufacturers and consumers are one kind of producers and consumers. Also, usually, there can be a warehouse for manufacturers to temporarily store the products, it is like a buffer in this case.

Producer generates messages that is consumed by the consumer. There is a buffer shared by the producer and the consumer. The buffer can 


## S27

Operating Systems

Producer-Consumer: Bounded Buffer

//declare a mailbox with capacity of B messages (buffer size B)


void producer(void)
{
	message m;
	while (1) {
		//pre-processing…
		while(mailbox is full) wait;
		send(mailbox, m);
	}
}

void consumer(void)
{
	message m;
	while (1) {	
		while(mailbox is empty) wait;	
		receive(mailbox, m); 	
    	//post-processing…		
		}
	}

[NOTES] We first declare a mailbox with capacity of B messages. This is a bounded buffer.

Let’s first look at the producer process. It is a while loop. That means, it keeps doing the same thing. It first performs some pre-processing, and then checks whether the mailbox is full or not. if it is full, the producer has to wait. Then, it sends a message to the consumer. 
In consumer, it first checks whether the mailbox is empty or not. if so, it has to wait. Then the consumer receives a message from the mailbox and performs some post-processing on the message. 

Does this example use direct or indirect c


## S28

Operating Systems

Part 2:  Processes and Threads

Process Concept
Process Scheduling
Operation on Processes
Interprocess Communication
Threads


## S29

Operating Systems

Threads

Overview
Single vs Multithreading Process
Benefits of threads
Types of threads
Multithreading models

[NOTES] In this course, we mainly talk about processes. Therefore, we will quickly go through the basic concepts of threads in the remainder of this chapter.

Note: Only in this part, we refer to the concepts of threads. All other parts in this course, we refer to process (single-threaded process).


## S30

Overview

Operating Systems

A thread (or lightweight process) is a basic unit of CPU utilization; it consists of:
Thread id
Program counter
Register set 
Stack space

A thread shares with its peer threads in the same process:
Code and data sections
Operating system resources (open files, etc.) 

A traditional or heavyweight process is an executing program with a single thread of control


## S31

Operating Systems

Single vs Multithreaded Processes

[NOTES] This figure illustrates the difference between a single-threaded process and a multi-threaded process. 

On the left we have the single-threaded process, and on the right we have the multi-threaded process. The single-threaded process is just the same as a conventional process that we introduced earlier. Also, a thread has its state (new, ready, running, waiting). A data structure called thread control block (TCB) is also used to record the information of a thread. Thus, a thread has very similar state transitions as a process. 

In the multi-threaded process, we can see that all the threads s


## S32

Operating Systems

Advantage of Multithreaded Processes

In a multithreaded process, while one thread is blocked and waiting, a second thread can run
Cooperation of multiple threads in the same process results in higher throughput

WORD

[NOTES] Most operating systems support multithreaded processes. In a multithread process, when one thread is blocked or waiting for an event, the other thread can run. Therefore, cooperation of multiple threads in the same process can deliver better performance. 
 For example, a word processor is only one process in the windows system. It has multiple threads: one thread for displaying the inputs, the other thread for accepting the keystrokes from users, one thread for auto-saving the document into the hard disk. Even if a thread (say the one accepting the keyboard input) is blocked, other threads can


## S33

Example: Multithreaded Server

Operating Systems

[NOTES] This example is a multithreaded server. This architecture is very common in web servers, FTP servers, etc. There can be multiple clients sharing the same server. A client is a process in the client machine, and the server is a process in the server machine. Let’s see how the server handles a request from the client. First, a client submits a request to the server. Next, the server create a new thread to serve the request. And then, the server resume listening for additional client requests. The thread will serve the request independently. When finished, the thread is deallocated. Since creatin


## S34

Operating Systems

Thread Implementation Models

Paradox
Allow users to implement an arbitrary number of threads, BUT
OS kernel can support a limited number of threads due to resource constraints

Solution: Two layers of abstraction

User threads (logical): Created in user space
Allows users to create as many threads as they want

Kernel threads (physical): Created in kernel space
Slower to create and manage than user threads
Resources are eventually allocated in kernel threads

OS maintains the mapping from user to kernel threads

[NOTES] On one hand, we want to allow users to implement an arbitrary number of threads. This is for the convenience and simplicity of multithreading programming. On the other hand, the OS kernel can only support a limited number of threads due to resource constraints. 
The solution is to have two layers of abstraction. There are two types of threads, user threads and kernel threads. User threads are created and managed by users/developers, and kernel threads are created and managed by OS. Then, OS maintains the mapping from user threads to kernel threads.
 
Let’s look at more details about user threa


## S35

Operating Systems

Multithreading Models

Model that defines the mapping between user threads and kernel threads
Many-to-One
One-to-One
Many-to-Many

Why is there no One-to-Many mapping?
Wastage of OS resources to map a single user thread to many kernel threads

[NOTES] From the user space to the kernel space, there is a mapping from the user threads to the kernel threads. We have three multithreading models: many-to-one, one-to-one, and many-to-many. 

Note that we do not have one to many. Why? Because it does not make sense to have one user thread mapping to multiple kernel threads. It is a waste of OS resources.


## S36

Operating Systems

Many-to-One Mapping

Disadvantage: A blocked user thread, will also block other user threads mapped to the same kernel thread

I/O or System call









Blocked

[NOTES] In the many-to-one model, many user-levels threads are mapped to a single kernel thread. *For those threads mapped to the same kernel thread*, they are unable to run in parallel due to the single kernel thread. That is, if a thread is stuck by a system call or I/O, the other user threads mapped to the same kernel thread are also blocked.


## S37

Operating Systems

One-to-One Mapping

Each user-level thread maps to a unique kernel thread
Examples: Windows 95/98/NT/2000, OS/2

Provides more concurrency than many-to-one model

Disadvantages: 
Creating a user thread requires creating the corresponding kernel thread
May create too many kernel threads which is a burden on the system

[NOTES] The second model is one-to-one: each user level thread maps to a kernel thread. Both Windows and Linux support one-to-one model.
This model has the advantage of providing more concurrency than the many-to-one model. If a thread is blocked by a system call, the other threads can run.
The disadvantage is mainly on the thread creation overhead.  
Creating a user thread requires the creation of a kernel thread.
If too many kernel threads are created, the system can be overloaded.


## S38

Operating Systems

Many-to-Many Mapping


## S39

Operating Systems

Many-to-Many Mapping

Allows many user level threads to be mapped to many kernel threads (see next slide)
Examples: C++20 coroutines, Golang goroutines

Allows the operating system to create a sufficient number of kernel threads

Does not have the disadvantages of one-to-one and many-to-one models

Disadvantage: Not easy to decide the mapping

[NOTES] The last model is many-to-many. This model allows a more flexibile mapping: multiple user level threads can be mapped to multiple kernel threads.
It allows the operating system to create a sufficient number of kernel threads to utilize the processor resources. For example, the operating system can create more kernel threads on a multi-core machine. 
Finally, due to the flexible mapping, the many-to-many model does not have the disadvantages of one-to-one and many-to-one models. The developer can create as many user threads as they wish, and the corresponding kernel threads are run in parallel.


## S40

Operating Systems

Advanced Readings

Beej's Guide to Unix Interprocess Communication
http://beej.us/guide/bgipc/
Very good introduction on the IPC implementation inside Unix


Tutorials on how to use thread libraries:
POSIX pthreads, http://randu.org/tutorials/threads/  
Windows Process and Thread Functions http://msdn.microsoft.com/en-us/library/windows/desktop/ms684847(v=vs.85).aspx

[NOTES] Those are advanced readings, if you want to know more beyond the text book.
