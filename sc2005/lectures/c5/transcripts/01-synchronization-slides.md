# Part 4 — Process Synchronization (slide deck S1–S54)

> Verbatim text of `Part4 (Synchronization).pptx` (54 slides): every bullet, table cell and code line,
> in slide order. Lines beginning `[NOTES]` are the speaker notes from the deck, reproduced as-is.

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

Part 4:  Process Synchronization

Race Condition & Critical-Section
User-level Solutions
OS-level Solutions
Synchronization Hardware
Semaphores
Classical Problems of Synchronization

* Important but difficult 

[NOTES] In this chapter, we will talk about process synchronization. I have two points to highlight. Firstly, this is one of the most difficult but also the most important parts in an operating system. That is why we will spend two weeks’ time on process synchronization. We will learn the concepts with concrete examples, animations and also the scripts in the comment of the ppt. An extra slide stack has been uploaded to NTULearn. I hope those additional animations can help you to better understand the concepts.

We first talk about critical-section problem. Next we will talk about the operating system


## S03

Operating Systems

Background

Access to shared data from concurrent processes may result in data inconsistency
Inconsistent Data: Data value depends on the order of instruction executions from concurrent processes
That is, data value depends on when context switches occur between the concurrent processes

Maintaining data consistency requires mechanisms to ensure the orderly execution of concurrent processes
Causal ordering (sequencing) of reads and writes to the shared data from concurrent processes

[NOTES] Why we need process synchronization? Remember that cooperating/concurrent processes usually share some data. Concurrent access to shared data may result in data inconsistency. We should consider context switches in any place of process execution in order to consider all the possible interleaving orders.
 
We need some mechanisms to ensure the orderly execution of cooperating processes.


## S04

Operating Systems

Example: Producer-Consumer (with bounded buffer)

Both producer and consumer work concurrently
Producer fills the shared memory buffer with items
Consumer takes items from that buffer

[NOTES] Let’s look at one example. Suppose we have two processes in the producer and consumer example: producer and consumer. They share a variable counter to keep track of the number of items in the shared buffer. 

Buffer is the shared buffer with BUFFER_SIZE size.
in and out are pointers.
in: the current empty slot in the buffer that the producer wants to put in.
out: the item in the buffer that the consumer wants to take from. 
counter is the number of items in the buffer.
in and out are initialized with zero, and counter is also equal to zero.


## S05

Operating Systems

Example: Producer-Consumer (with bounded buffer)

#define BUFFER_SIZE 10
typedef struct {. . .} item;
int in=0; //the next-to-fill empty slot (producer variable)
int out=0; //the next-to-process item (consumer variable)

Shared Data 	
item buffer[BUFFER_SIZE];
int counter = 0; // Number of items in buffer

[NOTES] Let’s look at one example. Suppose we have two processes in the producer and consumer example: producer and consumer. They share a variable counter to keep track of the number of items in the shared buffer. 

Buffer is the shared buffer with BUFFER_SIZE size.
in and out are pointers.
in: the current empty slot in the buffer that the producer wants to put in.
out: the item in the buffer that the consumer wants to take from. 
counter is the number of items in the buffer.
in and out are initialized with zero, and counter is also equal to zero.


## S06

Operating Systems

Bounded-Buffer (Cont.)

Producer process
  item nextProduced;  while (1) {
		while (counter == BUFFER_SIZE); // wait for space 
		buffer[in] = nextProduced; // produce item
		in = (in + 1) % BUFFER_SIZE; // prepare for next item
		counter++;
	}

Example: Producer-Consumer (with bounded buffer)

[NOTES] If the buffer is full, wait (pay attention to the semicolon).  Otherwise, we put the item into the buffer and increase the counter by one.
We use (in+1) mod BUFFER_SIZE, meaning that the buffer is a circular buffer. When the in value reaches the end of the buffer, it goes back to zero.


## S07

Operating Systems

Bounded-Buffer (Cont.)

Consumer process
  item nextConsumed;  while (1) {
		while (counter == 0); // wait for buffer to receive an item
		nextConsumed = buffer[out]; // Consume the item
		out = (out + 1) % BUFFER_SIZE; // Prepare for next item
		counter--;
	}

Example: Producer-Consumer (with bounded buffer)

[NOTES] Consumer: we check whether the buffer is empty. If it is empty, the consumer waits.

So, now, let’s see what are the shared variables in those two processes?
Between producer and consumer:
Counter is the shared variable.
Buffer is the address shared by both processes. However, it is read-only.


## S08

Operating Systems

Bounded-Buffer (Cont.)

Lets take a close look at these instructions
Producer process: counter++; 
Consumer process: counter--;

They may create inconsistent value for variable counter due to race condition
The actual value depends on when the producer or consumer process context switches

Example: Producer-Consumer (with bounded buffer)

[NOTES] The two statements counter++ and counter– may create inconsistent value due to race condition. Race condition means that the actual value depends on the order of process executions. Let’s see the details with an example.


## S09

Operating Systems

Race Condition

With “counter = 5” initially, suppose we execute producer and consumer once using the following interleaving
Producer executes register1 = counter {register1 = 5}
Producer executes register1 = register1 + 1 {register1 = 6}
Context switch occurs from Producer to Consumer
Consumer executes register2 = counter {register2 = 5} 
Consumer executes register2 = register2 – 1 {register2 = 4} 
Context switch occurs from Consumer to Producer
Producer executes counter = register1 {counter = 6 } 
Context switch occurs from Producer to Consumer
Consumer executes counter = register2 {counter = 4}

Counter value is 4 instead of 5!

In Consumer counter-- implemented as:     register2 = counter     register2 = register2 - 1     counter = register2

In Producer counter++ implemented as:     register1 = counter     register1 = register1 + 1     counter = register1

[NOTES] @one animation in the additional slide.

This example shows that different execution orders of multiple processes may result in data inconsistency. The actual value of the shared variable depends on the order of process executions. We need to consider all possible context switch places to check whether inconsistency is possible.


## S10

Operating Systems

The Critical-Section Problem

n processes all competing to use some shared data

Each process has a code segment, called critical section, in which the shared data is accessed
Process may be changing shared variables, updating a shared table, writing a shared file, etc.
At least one process modifies (writes to) the shared data

Problem: Design protocol to ensure that when one process is executing in its critical section, no other process is allowed to execute in its critical section

[NOTES] Now we define the critical section problem. In this problem, we have multiple processes all competing to use some shared data. Each process has a code segment called critical section, where the shared data is accessed. At least one of the processes is updating the data.

So, the critical section problem is to design a protocol to ensure that when a process is executing in its critical section, no other process is allowed to execute in its critical section. That means, at any time, there is at most one process in the critical section.

In the previous example, counter++ and counter-- are critic


## S11

Operating Systems

Generic Solution Structure for the Critical-Section Problem

Entry section: Ask permission to enter critical section
Exit section: Exit critical section (notify other processes)

Generic Process Structure
				while (1) { 
			   	    entry section
			          		critical section
			    	    exit section
			           	remainder section
				 }

Non critical section executions

What should the logic inside here be?

[NOTES] We model each process with a program structure. Each process must ask permission to enter the critical section in entry section, then enter the critical section to access the shared variables, and exit it in the exit section. In the exit section it indicates that the other processes can go into the critical section. Remainder sections are for other (non critical section) logic.
 
The loop is to allow you to explore all possible orders of executions (different places to perform context switches). Our implementation of the entry section/exit section should be correct for all the possible orders 


## S12

Operating Systems

Desired Properties of Solutions to the Critical-Section Problem

Assumptions of critical and remainder sections
Each process is guaranteed to make progress over time in these sections
No assumption about relative execution speed of different processes in these sections (may execute at different speeds)

Desired Properties of entry and exit sections

Mutual Exclusion: If a process is executing in its critical section, then no other process can be executing in its critical section at the same time

[NOTES] Mutual exclusion means the solution must guarantee that, at any time, there is at most one process in the critical section.


## S13

Operating Systems

Solution to Critical-Section Problem (Cont.)

Progress: If no process is executing in its critical section and there exist processes that wish to enter their critical section, then the selection of the next process to enter the critical section cannot be postponed indefinitely

Bounded Waiting:	After a process has requested to enter its critical section and before that request is granted, other processes are allowed to enter their critical section only a bounded number of times

These two properties together ensure that a process is not stuck in the entry section forever

Desired Properties of Solutions to the Critical-Section Problem (Cont.)

[NOTES] Progress: If there is no process in the critical section, a process requesting to enter the critical section will eventually enter it. Progress means that a process that is not in the critical section cannot block other processes from entering the critical section. Bounded waiting means a process can eventually get the chance to enter the critical section. 

A correct solution to a critical section problem should satisfy all the three requirements. If any of the three requirements is violated, the solution is wrong. 

There is a circumstance called live-lock (corresponding to deadlock), in whi


## S14

Operating Systems

Part 4:  Process Synchronization

Race Condition & Critical-Section
User-level Solutions
OS-level Solutions
Synchronization Hardware
Semaphores
Classical Problems of Synchronization


## S15

Operating Systems

Initial Attempts to Solve the Problem

Generic structure of process
		while (1){
			entry section
				critical sections
			exit section
			remainder section
		}
We start with only 2  processes P0 and P1
Although P0 and P1 have the same generic structure, they may have different implementations for the four sections

We look at user-level software approaches w/o OS support

[NOTES] Before we talk about operating system support for the critical section problem, we look at software solutions without operating system support. 
Two points:
1. We learn how to analyze whether a solution can satisfy the three requirements.
2. These solutions are implemented by users, without any special support from OS. 

Here, we want to use these examples to show you: these software approaches are difficult to write, even for two processes. Thus, it is necessary for OS to provide support.


## S16

Operating Systems

Algorithm 1

Variable shared between processes: int turn; // initially turn=0
turn = i  Pi can enter critical section

Process Pi :  while (1){
			while (turn != i );
				critical section
			turn = k;
				remainder section
		}

Process P0

0);

1;

Process P1

1)

0;

Entry Section

Exit Section

[NOTES] First try: Algorithm 1. We define one shared variable: turn. If turn=0, P0 can enter its critical section, otherwise P1 can enter its critical section.


## S17

Operating Systems

Algorithm 1: Property Analysis

Mutual Exclusion?  
Suppose turn = 0 and P0 enters critical section
turn is only updated in exit section, when P0 exits critical section
Process P1 therefore cannot enter its critical section

Progress? 
turn = 0 and P0 is in a long remainder section (think while(1) loop or blocked I/O), and P1 wants to enter critical section

Bounded Waiting? 
Assuming turn is updated in a fair (e.g., round-robin) manner among the two concurrent processes

[NOTES] **Best practices for analyzing BMP (Bounded Waiting, Mutual Exclusion, Progress)***

- Mutual exclusion: we assume that one process is in the critical session, and then see if the other process can enter the critical section. If yes, mutual exclusion is violated. Otherwise, mutual exclusion is satisfied in this scenario. we can check the other way around. 

- Progress: we consider the scenario if no process is in the critical section. Let’s consider if a process is in the entry/exit section, will it stop other processes to go into the critical section? If yes, progress is violated.

- Bounded 


## S18

Operating Systems

Algorithm 2

Variables shared: boolean flag[2]; 
Initially flag [0] = flag [1] = false
flag [ i ] = true  Pi ready to enter its critical section

Process Pi :   while (1) {
		flag [ i ] = true;	while (flag [ k ]);
		  critical section
		flag [ i ] = false;
		  remainder section
	                       }

Entry Section

Exit Section

Algorithm 1 had an issue that it did not know if a process wants to enter its critical section
Issue solved in Algorithm 2 by using one flag for each process to express interest

[NOTES] Shortcoming of Algorithm 1: The single shared variable is not sufficient to remember the state of each process. It only records the process that is allowed to enter its critical section. To address this problem, we use two shared variables. Flag[0] and flag[1].

In the entry section, we set our flag to be true. Then, we wait for flag[k] to be false, that means pk has left the critical section.

In the exit section, we set flag[i] to be false, meaning that Pi has left the critical section.


## S19

Operating Systems

Algorithm 2: Property Analysis

Consider the following execution sequence:
	T0 : P0 sets flag[0] = true
	T1 : P1 sets flag[1] = true
	Now P0  and P1 are looping forever in their respective while statements.

Mutual Exclusion?  
Suppose P0 enters critical section, then flag [ 1 ] = false and      flag [ 0 ] = true
flag [ 0 ] is only updated to false in the exit section of P0
Process P1 therefore cannot enter its critical section

Progress?  Consider the following interleaving:
P0 executes flag [ 0 ] = true;
Context switch to P1
P1 executes flag [ 1 ] = true; 

Bounded Waiting? 
Once P0 sets flag [ 0 ] = true, process P1 cannot enter its critical section

Both P0 and P1 are stuck in an infinite while loop now!


## S20

Variables are a combination of Algorithms 1 and 2
flag [ i ] = true  Pi ready to enter its critical section
turn = i  Pi can enter critical section

Proc. Pi: while(1){
			flag [ i ] = true;	    turn = k;	    while (flag [ k ] and turn = k);
				critical section
		    flag [ i ] = false;
				remainder section
		}

Operating Systems

Algorithm 3

Entry Section

Exit Section

Algorithm 2 could not choose between two processes that wanted to enter their critical section at the same time
Issue solved in Algorithm 3 by using turn variable to denote whose turn it is

[NOTES] This algorithm combines the ideas of algorithms 1 and 2. 

This algorithm satisfies the three requirements of a solution to the critical section problem. Let’s see how it solves the problem of algorithms 1 and 2.
In the entry section: we indicate the intension of entering the critical section by setting flag[i]=true, and also set turn to be k. If flag[k]=true and turn=k, that means process Pk has expressed intent to enter the critical section and it is its turn. If either condition is false, we can enter the critical section.


## S21

Operating Systems

Algorithm 3: Property Analysis

Mutual Exclusion?  
If P0 enters critical section, then flag [ 0 ] = true
If P1 now wants to enter critical section, then it will first set turn = 0
P1 then cannot enter because turn = 0 and flag [ 0 ] = true

Progress?  Suppose P0 wants to enter critical section
If P1 is in remainder section then flag [ 1 ] = false and P0 can enter
If P1 is in entry section, then access is granted either to P0 or P1 depending on the latest value of turn

Bounded Waiting?  Assuming turn is updated fairly

How to extend Algorithm 3 for say three processes?

[NOTES] Algorithm 3 meets all the three requirements. It solves the critical section problem for two processes. Please refer the textbook for the proof. The proof is just for your reference.

The algorithm is developed by a famous Microsoft researcher named Leslie Lamport.  I have shown you how difficult it is to implement a solution with software approaches (via shared variable).

In summary, we have learnt different implementations for the critical section problem. Here, the important point is to show you how to analyze whether an implementation can solve the problem. You are not required to remembe


## S22

Operating Systems

Part 4:  Process Synchronization

Race Condition & Critical-Section
User-level Solutions
OS-level Solutions
Synchronization Hardware
Semaphores
Classical Problems of Synchronization


## S23

Operating Systems

OS Support for Synchronization

Previous software approaches are difficult to implement for more than two processes
Solution: Operating system support

OS has the following three kinds of support for the critical section problem (low level to high level)
Synchronization hardware
Semaphore
Monitor

[NOTES] @let’s review what we have learnt in our last lecture. We started with talking about the critical section problem. there are three requirements: mutual exclusion, progress and bounded waiting. You can refer to the previous slides for the detailed definition of each requirement. Then, we talk about software approaches to solve this problem, and those approaches are without operating system support. There are three algorithms for solving the critical section problem of two processes. Algorithm 1, 2, and 3. Algorithms 1 and 2 have progress violations, and Algorithm 3 satisfies all the three requi


## S24

Operating Systems

Synchronization Hardware

Modern processors provide special atomic hardware instructions 
Atomic = non-interruptible (no context switches)

TestAndSet: Test and modify the content of a main memory word atomically
	           boolean TestAndSet (boolean *target) {
				       boolean rv = *target;
			          *target = true;
				       return rv;
              }

No context switches allowed during this execution

Interrupt is disabled

Interrupt is enabled

Get current value

Store true

Return old value

[NOTES] Modern hardware usually offer some atomic operations or instructions. An atomic operation means that the operation is executed in order without preemption. The execution of an atomic operation is non-interruptible, meaning that there is no context switch from the first line till the last line.
 
TestAndSet is a common one. It reads a value and changes the value of the target word atomically. The return value is the old value of the target word. Note * denotes a pointer in c/c++.

Interrupt is disabled -> OS will disable the context switch before the first line is executed. OS will enable the c


## S25

Variable shared: boolean lock; 
Initially lock = false
If TestAndSet on lock returns false, then process can enter critical section (because it set lock to true)

Process Pi : while (1) { 
				  while(TestAndSet(&lock));
					critical section
				  lock = false;
					remainder section
			   }

Operating Systems

Critical-Section with Test-and-Set

Acquire lock

Release lock

Entry Section

Exit Section

[NOTES] We can use TestAndSet to implement mutual exclusion. We define a lock boolean variable. Initially, it is false. & is the address of the variable in c/c++.


## S26

Operating Systems

TestAndSet: Property Analysis

Mutual Exclusion?  
A process enters critical section  lock = false immediately before it executes TestAndSet(&lock) and lock = true thereafter
lock is reset to false only in the exit section of the process
No process can thereafter enter critical section since lock = true

Progress? 
If lock = false, then the first process that executes TestAndSet(&lock) will immediately enter critical section

Bounded Waiting?  See next slide
More complex solution with TestAndSet that satisfies bounded waiting is in the textbook – not examinable


## S27

Operating Systems

Bounded Waiting fails with TestAndSet

Process P0
   1. Initialization code
   2. while (1) { 
	3.   while(TestAndSet(&lock));
	4.      critical section
	5.   lock = false;
   6. }

Process P1
  1. while (1) { 
  2.    while(TestAndSet(&lock));
  3.       critical section
  4.    lock = false;
  5. }

Suppose for P0 lines 1-3 take 10ms and 2-6 also take 10ms
Suppose we use round-robin scheduling with quantum 10ms
Whenever P0 context switches out, it holds the lock (is in critical section)
									 . . .

P0 (1,2,3)

P1 (1,2)

P0 (4,5,6,2,3)

P1 (2)

P0 (4,5,6,2,3)

Context switch points


## S28

Operating Systems

Semaphore

Semaphore S: Integer shared variable

Only accessible by two atomic system calls: Wait and Signal
Wait (S): if S>0, S--; else, wait();
Signal (S): S++;

Two types of semaphores
Counting semaphore: Integer value can range over an unrestricted domain
Binary semaphore: Integer value can never be greater than 1

[NOTES] The hardware solutions are too low level, and are complicated to use. So, operating system provides a higher level synchronization mechanism called semaphore. Semaphore is very important, not only because we have questions on this part in every past exam paper, but also because semaphore is a widely used process synchronization mechanism. 

Semaphore is an integer shared variable. Operating system offers two atomic operations to manipulate this shared variable: Wait and Signal. We will talk about the details of implementation in later slides.

When we execute Wait, if S value is one, we can fi


## S29

Operating Systems

Semaphore Solution for the Critical Section Problem

Variable shared: semaphore mutex; // initially mutex=1
If mutex=1 and process executes Wait(mutex), then it can enter critical section

Process Pi :   while(1) {
		Wait(mutex);
			critical section
		Signal(mutex);
			remainder section
	                       }

Acquire Semaphore

Release Semaphore

Entry Section

Exit Section

[NOTES] With the semaphore, we can easily develop a solution to the critical section problem. The mutex value is initialized with 1, a binary semaphore. You can see, this implementation is simpler than the previous solution using atomic instructions. There is no while-loop, because it is already implemented in wait. We will see more details later.


## S30

Operating Systems

Classical Semaphore Implementation (Busy Waiting)

Wait (S):  
	while (S <= 0)	   ; // busy wait
	S--;
Signal (S): 
	S++;

Pros: No context switch overhead (busy waiting)

Cons: Inefficient if critical sections are long
Busy waiting wastes CPU cycles

Assembly for Wait(S):
loop1: ldr ax, [S]
           cmp ax, 0
           jle loop1
           sub ax, 1
           str [S], ax

Assembly for Signal(S):
           ldr ax, [S]	
           add ax, 1
           str [S], ax

[NOTES] Now let’s see how semaphore is implemented in OS. The classical implementation for Wait and Signal uses busy waiting. 

Why the implementation is called busy waiting? Because if S<=0, the process needs to busy wait in a while loop, and keeps polling the value of S. Busy waiting has the advantage that no context switches occur. That is particularly good for a short waiting time. However, the constraint is that busy waiting is inefficient if the critical section is long, because the while loop will consume too many CPU cycles. 

Note, if Wait(S) is not implemented in an atomic manner, mutual exc


## S31

Operating Systems

Busy Waiting Semaphore(Property Analysis)

To avoid race condition, S++ and S-- must be atomic
Wait(S) must be atomic to ensure mutual exclusion
Consider the following with S>0 initially
Process P0 executes while (S <= 0); and exits busy wait
Context switch from P0 to P1
Process P1 executes while (S <= 0); and S--;
Context switch from P1 to P0
Process P0 executes S--;
Mutual Exclusion? 

Assembly for Wait(S):
loop1: ldr ax, [S]
           cmp ax, 0
           jle loop1
           sub ax, 1
           str [S], ax

Assembly for Signal(S):
           ldr ax, [S]	
           add ax, 1
           str [S], ax

while (S <= 0);

S--;

S++;


## S32

Operating Systems

Current Semaphore Implementation (Blocking)

Define a semaphore as a record
		typedef struct {
		     int value; 
		     struct process *L; 
		} semaphore;

Need two simple operations
block( ): blocks the current process
wakeup( ): resumes the execution of a blocked process in list L

[NOTES] Because the busy waiting implementation is not feasible on a single processor system, current operating systems have another implementation: blocking. The basic idea is that when a process enters its critical section, other processes that want to enter their critical section will be blocked. A process is blocked, meaning it will be put into the waiting state. So, the process waiting to enter the critical section does not consume CPU cycles. 

Before we go into the implementation details, we define the relevant data structure and two operations.


## S33

Operating Systems

Blocking Semaphore Implementationblock() and wakeup()

block( ):
Dequeue current process from ready queue
Enqueue the process to list L
Change state of the process to waiting

wakeup( ):
Dequeue a process from list L
Enqueue the process to the ready queue
Change state of the process to ready

[NOTES] Let’s take a closer look at those two operations. 

Block: first dequeue current process from ready queue (we suppose that the PCB of the running process is also stored in the head of the ready queue), and then enqueue current process to list L.  The process state changes from running to waiting.
Wakeup: dequeue a process P from list L. We can have different policies here, just like process scheduling. Then enqueue P to the ready queue. The process state changes from waiting to ready.


## S34

Operating Systems

Blocking Semaphore Implementation Wait(S) and Signal(S)

Wait(S):	
		S.value--;
		if (S.value < 0) 
		{ 
		   block( );
         }

If S.value = -2, how many processes are waiting in list L?

Signal(S): 
		S.value++;
		if (S.value <= 0) 
		{ 
		   wakeup(P);
		}

2

[NOTES] Wait(S): We first decrease the value by one. If S.value<0, then it means we need to block because the value before we decreased it was already <=0. Hence we block the process.

Signal(S): We first increase the value by one. If S.value is smaller than or equal to zero, we wakeup a process from list L. Why we need to check if(s.value<=0) and not if(s.value<0)? Consider s.value=-1 (only one process waiting in list L), before executing signal. After S.value++, what is the value? S.value=0. That is why we need to consider s.value==0 as well for waking up processes.


## S35

Operating Systems

Blocking Semaphore Implementation Wait and Signal must still be atomic?

Wait(S): S.value--;
		if (S.value < 0) 
		{ block( ); }

Initially, S.value = 1
Process P0 executes S.value--;
Context switch from P0 to P1
Process P1 executes S.value--; and blocks since S.value = -1
Context switch from P1 to P0
Process P0 also blocks
Progress for P0 and P1? 

Signal(S): S.value++;
		      if (S.value <= 0) 
		      { wakeup(P); }

Initially, S.value = -1 (P2 blocked for S)
Process P0 executes S.value++;
Context switch from P0 to P1
Process P1 executes S.value++; and exits. No wakeup(P); since S.value = 1
Context switch from P1 to P0
Process P0 also exits without wakeup(P);
Progress for P2? 

Also lead to mutual exclusion violation due to -- and ++

All updates and checks for S must be atomic

[NOTES] Both Wait() and Signal() must be executed atomically (at least all updates and checks for semaphore S), even if the blocking semaphore implementation is used. If these updates and checks are not atomic, then progress can be violated as shown in the slide. It can also lead to violation of mutual exclusion because of the update to S (same issue as with the counter variable in the producer-consumer problem in Slide 4.7).

There is some possibility to allow limited context switches inside Wait() and Signal(). More details about this are in the tutorial.


## S36

Operating Systems

Blocking Semaphore Implementation S.value-- at the end of Wait(S)?

Wait(S):	
		if (S.value <= 0) { 
		   block( );
	          }
		S.value--;

Problems:

This would require a context switch between block( ); and S.value--; if the process blocks
If this context switch is allowed, mutual exclusion will be violated
Say S.value = 0 and P0 executes block( );
P1 uses Signal(S) to increment S.value to 1 and executes wakeup(P0);
P2 executes Wait(S), locks S, enters critical section
P0 executes S.value--; and enters critical section

Signal(S):	
		S.value++;
		if (S.value <= 1) { 
		   wakeup(P);
	          }

[NOTES] Why should we update the value of S before blocking? If we update the value after blocking, then this means we need to allow for a context switch inside Wait(). The process that is blocked cannot execute, because it is in the Waiting state. This means another process must be allowed to execute, otherwise the process that is currently holding the semaphore cannot release it.

If we allow context switch between block() and S.value-- inside Wait(), this can lead to violation of mutual exclusion. Suppose a process P0 executes block() and moves to the Waiting state (semaphore value currently is 0).


## S37

Operating Systems

Part 4:  Process Synchronization

The Critical-Section Problem
User-level Solutions
OS-level Solutions
Synchronization Hardware
Semaphores
Classical Problems of Synchronization


## S38

Operating Systems

Best Practices for Semaphores

Step 1: Understand the application scenario and identify the following:
Shared variables/data
Shared resources  

Step 2: Protect the shared variables
Identify the critical section
Use binary semaphore, and add entry section (Wait) and exit section (Signal)

Step 3: Protect the shared resources
Identity each kind of resource; one semaphore for one kind
Initial value: number of resource instances
When the resource is requested/consumed: Wait
When the resource is released: Signal

[NOTES] Step 1, 2, 3 for semaphores. Those are the three typical steps for solving process synchronization problems with semaphores.  

Shared variables is logical: counter in producer/consumer.
Shared resources are physical: Number of printers.

If you remove all the Wait/Signal, the *logic* of the code is still correct in sequential executions. However, it is not correct in concurrent executions.

The semaphore value represents the number of instances for that kind of resource (>0). Otherwise, represents the number of processes waiting in the waiting queue (list L).


## S39

Operating Systems

Semaphore as General Synchronization Tool

We wish to execute code segment B in process Pk only after code segment A in process Pi
Use a semaphore flag initialized to 0
Code:   Pi		        Pk

		  	 	
		A		    Wait(flag)
		    Signal(flag)			B

[NOTES] @Let’s review what we have learnt so far. We start with talking about atomic operations. There is no context switches from the first line to the last line of the execution of an atomic operation. We give one example of showing how to implement process synchronization with atomic operation TestAndSet. Semaphore is implemented as a shared integer variable. It supports two atomic operations: Wait and Signal. With the semaphore, it is easy to implement the process synchronization among multiple processes. Then, we have talked about two implementations of semaphores in operating systems. Busy waiti


## S40

Operating Systems

Deadlocks (Incorrect Semaphore Use)

Deadlock: Two or more processes are waiting indefinitely for an event that can be caused by only one of the waiting processes
Let S and Q be two semaphores initialized to 1

	       P0	                   P1
      Wait(S);	         Wait(Q);
	   Wait(Q);	         Wait(S);
	       	                     
	   Signal(S);      Signal(Q);
	   Signal(Q);      Signal(S);

Consider the following interleaving:

P0 executes Wait(S);
Context switch from P0 to P1
P1 executes Wait(Q); and Wait(S);
Context switch from P1 to P0
P0 executes Wait(Q);

[NOTES] However, incorrect usage of semaphore can cause problems. We will talk about two problems: deadlocks and starvation.

Deadlock means two or more processes are waiting indefinitely for an event that can be caused by only one of the waiting processes. Simply speaking, for two processes, A and B, a deadlock occurs if A waits for B, and B waits for A. That means, none of them can make any progress.


## S41

Operating Systems

Starvation (Incorrect Semaphore Use)

Starvation: Indefinite postponement (no progress)

A process may never have a chance to be removed from the semaphore queue (list L) due to queue discipline

Examples of queue disciplines that can cause starvation

Priority-based: Low priority process may starve if higher priority processes keep joining the queue

Last-In-First-Out policy

[NOTES] Starvation– a process may never have a chance to be removed from the semaphore queue (list L). For example, if the dequeue method is priority based, or LIFO (Last in first out).

What is the solution? Aging.


## S42

Operating Systems

Classical Problems of Synchronization

Bounded-Buffer (Producer-Consumer) Problem
Dining-Philosophers Problem
Readers and Writers Problem

[NOTES] We now talk about three classical problems of synchronization. We see how developers can use semaphore to implement the process synchronization in those three problems. 
Bounded buffer problem, dining philosopher problem, and readers and writer problems.
After learning those examples, we should learn two things: firstly we should know how to write a process synchronization with semaphore; Secondly, we should be able to analyze the correctness of the program with semaphore.


## S43

Consider multiple producers/consumers
We used counter, in and out variables for a producer-consumer pair
in/out are also shared variables now (in - producers, out - consumers)

Shared data and resources (Step 1)
item buffer[n];
buffer is a shared data structure
Slots in buffer are shared resources

Semaphores to be used
	       semaphore full, empty, mutex;
	       full =0; empty = n; mutex =1;

Operating Systems

Producer-Consumer with Bounded-Buffer

Counting semaphore for consumers to identify full buffer to consume

Binary semaphore for mutual exclusion to update buffer

Counting semaphore for producers to identify empty buffer to fill

in replaced with empty
out replaced with full
counter not used (why?)
mutex introduced to control access to buffer

[NOTES] In general, we use counting semaphore to represent shared resources that requires process synchronization, and use binary semaphore to protect shared variable for mutual exclusions.

Mutex for mutual exclusion on the buffer (semaphore mutex). Any access to the buffer must be protected by this semaphore.

What are the shared resources that we need to protect?  What are the counting semaphores that we need to define? Consider if the system has multiple producers and consumers.
The number of items in the buffer (semaphore full). They are the same resource among multiple consumers. We must make su


## S44

Operating Systems

Bounded-Buffer Problem (Cont.)

Producer process (Step 2)
                         Protect Shared Data:

		 item nextProduced;
		 while (1) {
			   	…
		   produce nextProduced;
				 …
			Wait(mutex);
			 	 …
 		    add nextProduced to buffer;
                                   …
			 Signal(mutex);
    	 }

Without synchronization:

[NOTES] Original code: no synchronization.

First, we protect the critical section, i.e., buffer update with the binary semaphore mutex. Say, we need to increment the number of items in the buffer, and manipulate the buffer. “add nextProduced to buffer;” is a critical section.


## S45

Operating Systems

Bounded-Buffer Problem (Cont.)

Producer process (Step 3)
		Manage Shared Resources:

		item nextProduced;
		while (1) {
				…
			produce nextProduced;
				 …
			Wait(empty);
			Wait(mutex);
				…
 		   add nextProduced to buffer;
                                 …
			Signal(mutex);
			Signal(full);
		}

Consume one empty slot

Signal consumers

Protect Shared Data:

[NOTES] Step 3: protect the shared resources.


## S46

Operating Systems

Bounded-Buffer Problem (Cont.)

Consumer process

      Protect Shared Data and Manage Shared Resources:

	         item nextConsumed;
	         while (1) {
	            Wait(full);
	            Wait(mutex);
		 …
	            nextConsumed = item from buffer;
		 …
               Signal(mutex);
               Signal(empty);
		 …
	             consume the item nextConsumed;
	          }

Consume one full slot

Signal producers

What if we swap as below?

Wait(mutex);
Wait(full);

DEADLOCK if buffer is empty!

[NOTES] You can think of different scenarios to see that they are correctly synchornized. For example, when the buffer is full. consumer can go in; but producer cannot. You can consider other cases as well.
Now, let’s consider one question: the order of Wait(full) and Wait(mutex) cannot be swapped. Why?


## S47

Operating Systems

Dining-Philosophers Problem

Five philosophers seated in a round table alternating between eating and thinking

Five plates (one for each philosopher) and only five chopsticks (one between each plate)

Problem: Devise a strategy to enable the philosophers to eat peacefully!

[NOTES] What is the five philosopher problem?
Each philosopher is either eating or thinking. They share a circular table with five chairs. A philosopher sits on a chair. There are only five chopsticks. When a philosopher becomes hungry, he will try to pick up the two chopsticks (on his left and right hand side). A philosopher can only pick the chopstick one at a time. He cannot take the chopsticks from others. He can eat only when he picks both chopsticks.  When he finishes eating, he puts down the chopsticks.

What are the shared data here? Five chopsticks. So, we can define five semaphores, one sema


## S48

Operating Systems

Dining-Philosophers Problem (Cont.)

Initial Solution
Each philosopher is a process
Each chopstick is a shared resource protected by a binary semaphore (chopstick [ 5 ];)
Initially, for all i, chopstick [ i ] = 1;

Code (Philosopher i)
		while (1) {
					Wait(chopstick [ i ]);
					Wait(chopstick [ (i+1)%5 ]);
					eat
					Signal(chopstick [ i ]);
				   Signal(chopstick [ (i+1)%5 ]);
					think
		   }

[NOTES] For philosopher i ( 0<=i<5): He first picks up his left chopstick, and then the right chopstick. This is done by calling the Wait operation on the corresponding semaphore. If both operations can succeed, the philosopher can eat. After eating, he releases the left chopstick and then the right one. After that, the philosopher will think, and then repeat the process. 

Does this solution have any problem? Each philosopher executes the first line and a context switch occurs.  deadlock.


## S49

Operating Systems

Dining-Philosophers Problem (Cont.)

Does the above solution have a problem?

Consider the following interleaving (Pi=Philosopher i):
P0 executes Wait(0); and then context switch to P1
P1 executes Wait(1); and then context switch to P2
P2 executes Wait(2); and then context switch to P3
P3 executes Wait(3); and then context switch to P4
P4 executes Wait(4);

Each philosopher has 1 chopstick and needs another to eat Deadlock!

[NOTES] The problem occurs when all five philosophers become hungry simultaneously, and each grabs his left chopstick. Now all the semaphores of chopstick will be equal to 0. When each philosopher tries to grab his right chopstick, he will be delayed forever. That is called deadlock. You can consider there is a context switch after the philosopher process executes the first line. You can see, incorrect use of semaphores can easily lead to the deadlock problem.


## S50

Operating Systems

Dining-Philosophers Problem (Cont.)

There are several possible remedies to avoid the above deadlock problem

Allow at most four philosophers to be hungry simultaneously

Allow a philosopher to pick up his chopsticks only if both chopsticks are available

Use an asymmetric solution
An odd philosopher picks up first his left chopstick and then his right chopstick
An even philosopher picks up first his right chopstick and then his left chopstick

[NOTES] Can you think of a solution for this problem? There are many possible solutions. We give some examples here. We will talk more in our next chapter. Here, you just need to know that, those solutions will make sure: even when all the five philosophers are hungry at the same time, at least one philosopher can eat.

First, we allow at most four philosophers to be hungry at the same time. In this case, at least one philosopher can pick up both chopsticks. 
Second, we allow a philosopher to pick up his chopsticks only if both are available. There is no deadlock, because one philosopher can take both


## S51

Operating Systems

Readers-Writers Problem

Problem: Scenario in a database or file
A writer requires exclusive access
Multiple readers can concurrently access
The first reader: Before reading, it must block the writers
The last reader: After reading, it can allow writers
Readers given preference (writer preference also possible)


Shared data
int readcount =0;  // Tracks #readers in the database
Database itself

Semaphores to be used
mutex=1;
wrt=1;

Binary semaphore protects access to readcount

Binary semaphore for mutual exclusion to database

If a reader is in database, more readers can access it

[NOTES] In database system, or file systems, we need to synchronize the reads and writes to shared data. The difference here is that we allow two readers to concurrently read the data. But if there is a writer, the access is exclusive and we require that writer has exclusive access to the shared data.

For system throughput, we try to maximize the probability of concurrent accesses from readers. Suppose a reader is accessing the database. During this period, if another reader comes to the database, we allow multiple readers to access and block the writers. Only after the last reader has exited the dat


## S52

Operating Systems

Readers-Writers Problem

Writer process

				Wait(wrt);
					 …
				writing is performed
					 …
				Signal(wrt);


## S53

Operating Systems

Readers-Writers Problem (Cont.)

Reader process

		Wait(mutex);
		readcount ++;
		if (readcount == 1) Wait(wrt);
		Signal(mutex);
				 …
			reading is performed
				 …
		Wait(mutex);
		readcount --;
		if (readcount == 0) Signal(wrt);
		Signal(mutex);

When a reader 
comes

When a reader 
leaves

The first reader?
Request access to database

The last reader?
Release database

[NOTES] The first reader holds the wrt semaphore, and blocks the writer. The last reader signals on this semaphore.
 
Readcount is the shared variable. So we need to use a mutex for synchronization.


## S54

Operating Systems

High-level synchronization construct that allows the sharing of variables among concurrent processes

Monitor is a collection of procedures and data

Processes may call procedures within monitor to access and update the data

Only one process can be active in the monitor at any one time (i.e., only one process can be executing a monitor procedure at any one time)

Data within monitor can only be accessed by procedures within it

Monitor

This slide is not examinable

[NOTES] We have already seen that semaphore can solve the process synchronization problem, but also induce other problems such as deadlock. OS actually introduces a higher level construct for developers named monitor. With monitor, it is even easier to implement a solution for process synchronization.

Monitor is a higher level abstraction that allows the sharing of variable among concurrent processes. In its definition, it is a collection of procedures and data. You can consider it as a java class. Processes call the procedures within monitor to access the shared data. The operating system ensures th
