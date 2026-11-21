# Part 3 — CPU Scheduling (slide deck S1–S30)
Verbatim slide text of `Part3 (CPU Scheduling).pptx`, extracted with tables and speaker notes. Lines starting `[NOTES]` are the lecturer's speaker notes, not slide body text.

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

Part 3:  Process Scheduling

Basic Concepts

Scheduling Criteria 

Scheduling Algorithms
Uniprocessor (single-core) scheduling
Multiprocessor (multi-core) scheduling

[NOTES] After introducing the concepts in the previous two weeks, we now study some advanced topics. We will study process scheduling algorithms in this chapter. We will have some calculations. We first introduce the basic concepts, scheduling criteria and then we will introduce the scheduling algorithms one by one.

@in our last lecture, we stopped here. let’s review what we have learnt in our last lecture. We start with talking about single processs operations, including process creation and termination. You can use some system calls to create/terminate a process. Then, we talk about IPC, inter-proc


## S03

Operating Systems

Basic Concepts

CPU–I/O Bursts: Process execution alternates between CPU executions and I/O operations
CPU burst: Duration of one CPU execution cycle
I/O burst: Duration of one I/O operation (wait time)

CPU scheduling objective: Keep the CPU busy as much as possible (i.e., using multiprogramming)

For simplicity, we focus on the concepts of short-term (ready queue) scheduler for both uni- and multi- processor CPUs

[NOTES] When a process has to wait for I/O or other events, the operating system performs a context switch, and gives the CPU core to another process. That means, a normal process execution has CPU execution, then I/O and then CPU execution, and so on. CPU execution and I/O wait form a cycle.

Why do we need to learn about CPU-I/O burst cycle? Single process cannot fully utilize the CPU. When a process is in an I/O burst, we need to seek another process to execute on the CPU. That is multiprogramming. 

Maximum CPU utilization is obtained with multiprogramming. Multiprogramming means that there are mu


## S04

Operating Systems

Alternating Sequence of CPU And I/O Bursts

[NOTES] Let’s look at one example of alternativing sequence of CPU and IO bursts. As you can see from this figure, the process execution usually starts with a CPU burst, and then followed by an IO burst by reading from file. Then, CPU and IO bursts appear alternatively, and they form a cycle.


## S05

Operating Systems

CPU Scheduler (Short-Term)

Goal: Select one or more of the processes in the ready queue, and allocate it to the CPU (one process per core)

Scheduler may run whenever a process changes state

In which case(s) does CPU scheduling have to occur in order to keep the CPU cores busy?

Answer:
Only 1 and 5

[NOTES] When one or more of the CPU cores become idle, the CPU scheduler is responsible for selecting processes from the ready queue and allocating them to the cores (one per core).

CPU scheduling decisions can take place when a process changes the state. Let’s see the process state transitions. There are five transitions when a scheduling decision may be made.  Scheduler dispatch is the decision made by the CPU scheduler. 

For which cases does scheduling have to occur, in order to keep the CPU busy? When I say “have to occur”, I mean: if scheduling does not take place, one or more CPU cores will be


## S06

Operating Systems

Types of CPU Schedulers

Nonpreemptive means that once the CPU has been allocated to a process, the process keeps the CPU until it voluntarily releases the CPU either by terminating or requesting I/O/event wait
Scheduling is nonpreemptive if it happens only for transitions 1 and 5 (also 4, when a CPU core is idle)

Preemptive means that the CPU can be taken away from a running process at any time by the scheduler
Scheduling is preemptive if it also happens for transitions 2, 3, 4 or at any other time instant

[NOTES] Based on when a scheduler chooses a new process, we can categorize the scheduler to be nonpreemptive or preemptive. 

A scheduler is nonpreemptive, if once the CPU has been allocated to a process, the process keeps the CPU until it voluntarily releases it either by terminating or requesting I/O/event wait. That means, scheduling is nonpreemptive if it happens only for transitions 1 and 5 (also 4, when a CPU core is idle).

A scheduler is preemptive if the CPU can be taken away from the running process at any time by the OS. Scheduling is preemptive if it also happens for transitions 2, 3, 4 or


## S07

Operating Systems

Scheduling Objectives

System-wide Objectives:				
Max. CPU Utilization: Keep the CPU as busy as possible
Percentage of time during which the CPU cores are busy executing processes.
(Sum of execution time on each core) divided by (total time multiplied by number of cores)
Max. Throughput: Number of processes that complete their execution per unit of time
Number of “exit” transitions per unit of time

[NOTES] In operating system, there are multiple scheduling criteria. In this lecture, we introduce five of them. Two are system-wide criteria, whereas three are process specific criteria.  

The first system-wide criteria is CPU utilization. The goal is to keep the CPU as busy as possible. It is the ratio of CPU core execution time over total time (can also be denoted as a percentage of total time) divided by the number of CPU cores.

Throughput refers to the number of processes that complete their execution per time unit. For example, the number of processes per second.


## S08

Operating Systems

Scheduling: Concepts and Terms

Individual Process Objectives to minimize: Turnaround time, Waiting time, Response time

Process ready to execute (Admitted -> Ready)

Time

Process scheduled (Running)

Process scheduled again (Running)

Turnaround time

Waiting time

Response time

Process preempted (Ready)

Waiting time

Process exited (Terminated)

CPU burst

CPU burst

[NOTES] The third criteria is turnaround time, which is a process specific criteria. It denotes the amount of time to execute a particular process, from the time of creation to the time of termination.


## S09

Operating Systems

Scheduling Objectives (Cont.)

Individual Process Objectives:
Min. Turnaround Time (Admitted -> Terminated)
Includes: CPU burst (Running), I/O burst or event wait (Waiting),waiting time (Ready)
Min. Waiting Time
waiting time = turnaround time - CPU bursts - I/O bursts - event wait

Min. Response Time (Admitted -> 1st time in Running)

System-wide: Average turnaround/waiting/response time
Average across all processes

[NOTES] The third criteria is turnaround time, which is a process specific criteria. It denotes the amount of time to execute a particular process, from the time of creation to the time of termination.


## S10

Operating Systems

Scheduling Algorithms: Uniprocessor System

First-Come, First-Served (FCFS) 
Shortest Job First (SJF)
Priority-based Scheduling
Round Robin (RR)
Multilevel Queue Scheduling

We assume a single CPU burst for each process, a single CPU core and focus on the average waiting time


## S11

Operating Systems

First-Come, First-Served (FCFS) Scheduling

Example:	Process	    CPU Burst Length
		P1	24
		 P2 	 3
		 P3	 3 
Suppose that processes arrive in the order P1,  P2, P3, all at time 0

The Gantt Chart for the schedule is:
Waiting time for P1  = 0; P2  = 24; P3 = 27
Average waiting time: (0 + 24 + 27)/3 = 17

P1

P2

P3

30

0

[NOTES] The simplest algorithm is first come first served, FCFS algorithm. The process that comes first is scheduled on the CPU core first. This algorithm can be implemented using a FIFO queue. 

Here is one example. Suppose these three processes arrive at time 0. We use a Gantt chart to represent the schedule. *In the exam, I encourage you to draw the Gantt chart to help your calculation.*

Note, once the CPU has been allocated to a process, that process keeps the CPU until it releases the CPU, either by terminating or by requesting I/O. So is FCFS preemptive or nonpreemptive? Nonpreemptive.


## S12

Operating Systems

FCFS Scheduling (Cont.)

Suppose that the processes arrive in the order P2, P3, P1, again all at time 0

The Gantt chart for the schedule is:


Waiting time for P1 = 6; P2 = 0; P3 = 3
Average waiting time: (6 + 0 + 3)/3 = 3 
Much better than the previous case

[NOTES] The average waiting time of FCFS algorithm is affected by the arrival order. Let’s consider another arrival order for the same example.

The average waiting time is much better than the previous case.


## S13

Operating Systems

FCFS Scheduling: Properties

Is FCFS preemptive or nonpreemptive?
Nonpreemptive, because processes have to voluntarily release the CPU once allocated

Main problem with FCFS is the convoy effect
Short processes suffer increased waiting times due to an earlier arrived long process
We saw this effect in the previous example - P1 increased the waiting times of P2 and P3

[NOTES] Different arrival order causes different waiting times. This reveals the problem of FCFS. It is called the convoy effect. In FCFS, the job arrival order matters!


## S14

Operating Systems

Shortest-Job-First (SJF) Scheduling

Prioritize processes based on their CPU burst lengths
Shorter burst implies higher priority
Intuitive way to handle the convoy effect of FCFS

Two schemes: 
Nonpreemptive: Once core is given to a process, it cannot be preempted until it completes its CPU burst
Preemptive (also known as Shortest Remaining-Time First or SRTF): If a newly created process has CPU burst length less than the remaining CPU burst of currently running process, then preemption will occur

SJF/SRTF is optimal for minimizing average waiting time

[NOTES] The convoy effect of FCFS problem shows that the short job should have a higher priority. Thus, we have the shortest job first scheduling. Priority is given to the job with the shortest time.
 
Depending on whether the scheduling is preemptive or not, we have two variants of SJF algorithm:
Nonpreemptive: Once the CPU is given to the process, it cannot be preempted until the CPU burst is completed. 
Preemptive: If a new process arrives with CPU burst length less than the remaining time of the current executing process, then preempt. That means, the CPU should be given to the new process.

SJF i


## S15

Operating Systems

Process	Arrival Time	Burst Time
		P1	0.0	7
		 P2	2.0	4
		 P3	4.0	1
		 P4	5.0	4

SJF (Nonpreemptive) Gantt Chart:




Average waiting time = (0 + 6 + 3 + 7)/4 = 4

Example of Nonpreemptive SJF

P1

P3

P2

7

3

16

0

P4

8

12

[NOTES] P2 and P4 have the same CPU burst time. How to break the tie? We choose the one with the earliest arrival time when two processes have the same CPU burst length. However, note tie can broken using any strategy. The optimality of SJF w.r.t average waiting time will still hold, irrespective of the tie breaking strategy.


## S16

Operating Systems

Example of Preemptive SJF (SRTF)

Process	Arrival Time	Burst Time
		P1	0.0	7
		 P2	2.0	4
		 P3	4.0	1
		 P4	5.0	4

SJF (Preemptive) Gantt Chart:





Average waiting time = (9 + 1 + 0 +2)/4 = 3

P1

P3

P2

4

2

11

0

P4

5

7

P2

P1

16

P1

P2

P3

P4

5

2

0

0

0

0

[NOTES] We need to consider scheduling when a new process comes, or when a process terminates.


## S17

Operating Systems

Priority-based Scheduling

A priority number (integer) is associated with each process

CPU is allocated to the process with the highest priority
Usually, smallest integer implies highest priority
Two schemes: Preemptive and nonpreemptive
FCFS: Priority based on arrival order
SJF: Priority based on CPU burst length

Problem of Starvation: Lower priority processes may never execute in a heavily loaded system
Solution is Aging: As time progresses, slowly increase the priority of processes that are not able to execute

[NOTES] In FCFS, a higher priority is given to a process that arrives earlier. In SJF, a higher prirority is given to a process with shorter CPU burst length. In general, we can assign an arbitrary priority to each process and schedule based on that priority. This is what happens in priority-based scheduling. 

The priority number can be an integer. For example, in Linux, the priority number can be [-20, 20]. -20 means the highest priority; 20 means the lowest priority. Similar to SJF, priority scheduling can be preemptive or nonpreemptive. 

One of the problems with priority-based scheduling is that 


## S18

Operating Systems

Round Robin (RR) Scheduling

Fixed time quantum for scheduling (q): A Process is allocated CPU for q time units, preempted thereafter and inserted at the end of the ready queue
Processes are scheduled cyclically based on q
Usually q is small, around 10-100 milliseconds

Performance:
n processes in ready queue implies waiting time is no more than (n-1)q time units
Large q: Degenerates to FCFS
Small q: Many context switches; high overhead

[NOTES] Now we look at a fair scheduling algorithm. This algorithm is called round robin. In RR, each process gets a small unit of CPU time (called time quantum). The time quantum is usually 10-100 ms. After this time has elapsed, the process is preempted and added to the tail of the ready queue. We give the CPU to the process that is at the head of the ready queue. This is the timer interrupt in the process state transition diagram.
 
Question: is RR preemptive or nonpreemptive? Preemptive. The CPU is forcibly taken away from the process when the time quantum is finished. We actually use RR to implem


## S19

Operating Systems

Example:  RR with Time Quantum = 20

Process	Burst Time
		P1	53
		 P2	 17
		 P3	68
		 P4	 24
All processes come at time 0 in the order of P1, P2, P3, P4

RR scheduling Gantt Chart: 			
Typically, higher average waiting/turnaround time than SJF, but better response time

P1

P2

P3

P4

0

20

37

57

77

0

33

48

4

[NOTES] RR has a higher average turnaround time than SJF, but better response time. 

What is the response time for P1? 0 P2? 20….


## S20

Operating Systems

Smaller Time Quantum Increases Context Switches

[NOTES] So, now let’s see the effect of the time quantum size on the number of context switches.
 
A process with a CPU burst of ten units of time. If the quantum is 12 units of time, the number of context switches *during* the process execution is zero. If the quantum is 6, the number of context switches during the process execution is 1. If the quantum becomes 1, the number of context switches is 9. So you can see, a small time quantum will dramatically increase the context switch overhead.  There is a similar question in the tutorial.


## S21

Operating Systems

Turnaround Time Varies With Time Quantum

No well-defined relationship between average turnaround time and quantum size

Average turnaround time remains fixed once quantum size is larger than maximum CPU burst length

Assume arrival order is P1, P2, P3, P4 all at time 0

[NOTES] FCFS = (6+9+10+17)/4=10.5, assuming arrival order of P1, P2, P3 and P4.

In this example we see how the time quantum size affects the turnaround time. We can make two observations. First, there is no clear relationship between the average turnaround time and the time quantum size. As the time quantum size increases, the average turnaround time may not always increase. Second, if the time quantum is larger than the largest CPU burst length, the average turnaround time becomes stable. Why? Because RR becomes FCFS.


## S22

Operating Systems

Multilevel Queue Scheduling

Different processes have different requirements
Foreground processes like those handling I/O need to be interactive (RR is preferred)
Background processes need NOT be interactive; scheduling overhead can be low (FCFS)

Solution: Multi-level Queue Scheduling
Ready queue is partitioned into several queues
Each queue has its own scheduling algorithm
How to schedule among the queues?

[NOTES] So far, we focused on a single ready queue. In practice, different processes have different requirements on performance, and thus they may require different scheduling algorithms. For example, foreground processes are more interactive like the key stroke, mouse or when you are playing a game. We prefer RR for such processes. Background processes are more about batch processing such as virus scanning. We prefer FCFS for such processes. Moreover, foreground processes may have a higher priority than background processes.
  
Multi-level queue scheduling can be used to handle such varying requireme


## S23

Operating Systems

Multilevel Queue Scheduling (Cont.)

Two schemes for inter-queue scheduling

Fixed priority scheduling
Queues served in priority order (e.g., foreground before background)
Starvation for lower priority queues

Time-slice based scheduling
Each queue gets a fixed time quantum on the CPU (e.g., 80ms for foreground, 20ms for background, and then repeat)

[NOTES] We call it multi-level queue, because the scheduling is not only performed within each queue, but also among the queues. 

There are basically two ways of inter-queue scheduling. 

The first one is fixed priority scheduling: we first serve all the processes in the foreground queue. After serving all the processes in the foreground queue, we consider the background queue. That may cause starvation for the background process. So, how to solve this problem? Aging.

The other method is time slice. Each queue gets a certain amount of CPU time which it can use to schedule among the processes. For ex


## S24

Operating Systems

Scheduling Algorithms: Multiprocessor System

Partitioned Scheduling (Asymmetric Multiprocessing - AMP) 
Global Scheduling (Symmetric Multiprocessing - SMP)

We assume a multi-core CPU and that each process may only execute on one CPU core at any time instant

[NOTES] We now look at the multiprocessor scheduling problem in which processes need to be allocated to two or more CPU cores. We will look at two types of scheduling strategies, partitioned and global scheduling.

For this section, we assume that a single process cannot execute in parallel on two CPU cores at the same time. However, it is possible that it executes on different CPU cores at different times. For example, it may start executing on core 1 and at a later time be context switched to execute on core 2.


## S25

Partitioned Scheduling (AMP)

Operating Systems

Processes are partitioned apriori (at process creation time) among CPU cores
Each process is mapped to one core
Separate uniprocessor CPU scheduling for each core (asymmetric scheduling)

Advantages
Core-specific scheduling strategy is feasible (FCFS, SJF, RR, multi-level, etc.)
Easy and simple extension of uniprocessor CPU scheduling to multiprocessor CPU scheduling

[NOTES] This is the simplest mechanism to extend single-core CPU scheduling to multi-core systems.

There are one or more dedicated ready queues per CPU core (queues are specific to cores), and different uniprocessor scheduling algorithms can be used for different cores. Mapping of processes to cores is done at process creation time.

What would be the main challenge in such a simple extension of uniprocessor scheduling to multiprocessors?


## S26

Partitioned Scheduling: Issues

Operating Systems

How to map cores to processes?
Poor mapping can lead to unequal loads: a core is idling while another is overloaded
May reduce system/process performance
NP-Hard problem: Similar to the well-known knapsack problem!
Heuristics such as best-fit could be used if CPU burst lengths are known

[NOTES] Allocating processes to cores is a challenging problem. Ideally, some sort of load balancing strategy must be employed so that all cores are equally utilized. This will improve overall system and process performance (turnaround time, throughput, etc.). An unbalanced distribution may lead to scenarios in which one core is idling while the other core is overloaded with several processes waiting/ready to execute. This can worsen the performance metrics on the overloaded core.

However, optimal allocation of processes to core is not feasible, unless P=NP. This is a NP-Hard problem very similar to 


## S27

Global Scheduling (SMP)

Operating Systems

One or more ready queues for the entire system (no mapping of queues to CPU cores)
When any core becomes idle, CPU scheduler runs and allocates the next process to execute
Process selection based on strategy applied globally or symmetrically across all cores (FCFS, SJF, etc.)
It is possible that the same process may execute on different cores at different times

No core-process mapping problem!

[NOTES] A global set of ready queues are maintained. Queues are not assigned to specific CPU cores. When a core becomes idle, a process is selected from one of the queues and allocated to the core. The selection strategy is applied globally across all the cores.

For example, if we use FCFS on a dual-core system, then there will be a single global ready queue. At any point in time, the two earliest arrived processes that are ready to execute will be executing on the two CPU cores.

Since processes could have multiple CPU bursts or they could be preempted, it is possible that the same process is execut


## S28

Process	Arrival Time	Burst Time
		P1	0.0	7
		 P2	2.0	4
		 P3	4.0	1
		 P4	5.0	4
SJF (Preemptive) on dual-core Gantt Chart:

Operating Systems

Example of SRTF (dual-core)

P3

P2

4

2

10

0

P4

5

8

P1

P1

P2

P3

P4

3

0

0

0

0

Core 1

Core 2

P1

6

Average waiting time = (1 + 0 + 0 + 1)/4 = 0.5

[NOTES] Preemptive shortest job first applied to the case when we have two CPU cores. The example is the same as the one used for uniprocessor scheduling. 

Compare the waiting times obtained here with the ones for the uniprocessor system.


## S29

Operating Systems

Example of RR with q = 20 (dual-core)

Process	Burst Time
		P1	53
		 P2	 17
		 P3	68
		 P4	 24
All processes come at time 0 in the order of P1, P2, P3, P4

RR scheduling dual-core Gantt Chart:

P1

0

20

17

37

57

60

61

73

89

0

33

48

4

Core 1

Core 2

P3

P2

P4

40

P1

P3

P4

P1

P3

0

13

0

28

0

0

[NOTES] Round robin scheduling applied to the case when we have two CPU cores. The example is the same as the one used for uniprocessor scheduling. 

Compare the waiting times obtained here with the ones for the uniprocessor system.


## S30

Global Scheduling: Issues

Operating Systems

Implementation complexity is high when compared to partitioned scheduling
Need to synchronize clocks across cores
Global strategy for process selection combining all the cores
Implementation overhead is high when compared to partitioned scheduling
Process could context switch from one core and be scheduled on another (private core-specific cache data needs to be migrated)

[NOTES] The scheduler must use a single clock so that the cores can be synchronized. Notion of time is global across all cores.

Selection of next process to run may involve going through several processes in the ready queue, particularly when there are more than one idle cores.

When a process context switches from one core to another, it loses access to the core’s private cache. This means that data must now be migrated to the other core’s private cache, which can be time consuming. Or the process has to start with a cold private cache in the other core, which can significantly increase its executio
