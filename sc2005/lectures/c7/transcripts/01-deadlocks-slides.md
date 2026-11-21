# Part 5 — Deadlocks and Starvation (slide deck S1–S45)

Verbatim deck text of `Part5 (Deadlocks).pptx`, 45 slides; `[NOTES]` marks the speaker notes. Citations are slide numbers (`S17`), because there is no audio.


## S01

Comments are Welcome

Online feedback systems (SFTs) are open (Due soon)

Your comments are VERY important:
To have a self-assessment process
To improve teaching and course content/structure

Speak out:
If you like my lectures and the interactive deep dive sessions, I will treasure the positive feedback
If you think of any improvements that you can suggest, that would be great feedback as well

Operating Systems

[NOTES] Thank you and good luck.


## S02

Course Overview

Operating Systems

OS goals

CPU management

Memory management

Filesystem management

Synchronization (L4-5)
Deadlocks (L6)

I/O & disk (L12)

Processes (L2)
Scheduling (L3)

Filesystems (L11)

Memory organization (L8)
Virtual memory (L9-10)

Special: Real-time OS & virtualization (L7)


## S03

Operating Systems

Part 5:  Deadlocks and Starvation

Deadlock Problem
System Model
Deadlock Conditions
Deadlock Prevention
Deadlock Avoidance
Deadlock Detection – not examinable

[NOTES] This is the outline of deadlock and starvation. We first define what is a deadlock; We will show how to model the deadlock problem in a systematic way. We will then see the conditions for deadlock, and the methods to handle the deadlock. We have prevention; avoidance and detection. Due to the time constraint, we cannot cover all the details about deadlock detection. So, deadlock detection is not examinable.


## S04

Operating Systems

The Deadlock Problem

Deadlock: A set of blocked processes each holding a resource and waiting to acquire a resource held by another process in the set

Example 1: 
System has two different types of tape drives; both P1 and P2 need the two tapes to finish execution
P1 and P2 each hold one tape drive and need the other

Example 2: Semaphores A and B, initialized to 1
    P0		  	 P1
wait (A);		wait (B);
wait (B);		wait (A );

Context switch points

[NOTES] We have already seen deadlocks in the previous chapter. A set of blocked processes each holding a resource and waiting to acquire a resource held by another process in the set. 

Another example is incorrect usage of semaphores. Say, we have two semaphores A and B initialized to 1. The two processes P0 and P1 can deadlock. We have seen this example in the previous chapter.


## S05

Operating Systems

Bridge Crossing Example

Only one car is allowed on the bridge
The bridge can be viewed as a shared resource
If a deadlock occurs, it can be resolved if one car backs up (release resource, i.e., the bridge, and rollback)
Several cars may have to be backed up if a deadlock occurs

Deadlock

[NOTES] The bridge is a resource and the cars are processes.
 
Deadlock occurs if there are two cars on the bridge. When deadlock occurs, it can be resolved if one car backs up. Note, several cars may have to be backed up if a deadlock occurs. That means, deadlock recovery may affect other processes. Not only the process in the deadlock state are affected, but also other processes that have dependency on the deadlocked process.


## S06

Operating Systems

Part 5:  Deadlocks and Starvation

Deadlock Problem
System Model
Deadlock Conditions
Deadlock Prevention
Deadlock Avoidance
Deadlock Detection


## S07

Operating Systems

System Model

Resource types R1, R2, . . ., Rm
Memory space, I/O devices, semaphores, etc.

Each resource type Ri has Wi identical instances

Each process utilizes a resource as follows:
Request for a specific number of instances
Use 
Release all the instances

[NOTES] We now introduce the system model for deadlock. In this model, we have different resource types R1… Rm. The resource type can be memory space or I/O devices. Each resource type Ri has Wi identical instances. For example, we have two hard disks in the system. Ri is the hard disk and Wi=2. the instances are all identical. 
A process utilizes a resource as follows: first sends a request of a certain number of instances.
If the instances are available, then the request is granted. Otherwise, the process needs to wait.  If the request is granted, the process uses the resource, and after sometime, r


## S08

Operating Systems

Resource-Allocation Graph

V is partitioned into two types
P = {P1, P2, …, Pn}, the set consisting of all the processes in the system
R = {R1, R2, …, Rm}, the set consisting of all resource types in the system

E is partitioned into two types
Request Edge: Directed edge Pi  Rj
When the request is granted, this edge is removed
Assignment Edge: Directed edge Rj  Pi
When the resource is released, this edge is removed

Graph  A set of vertices V and a set of edges E

[NOTES] Consider the system has multiple processes and multiple resource types. How to model resource request, use and release?

We use a data structure called the resource-allocation graph to model the resource allocations in the system. The graph has a set of vertices V and a set of edges E. V is partitioned into two types: process vertex and resource type vertex. The process vertices represent all the processes, and resource vertices represent all the resource types in the system. 

When a process sends a request for Rj, we add a directed edge from Pi to Rj. When the request is granted, the request


## S09

Operating Systems

Resource-Allocation Graph (Cont.)

Process


Resource Type with 4 instances


Pi requests instance of Rj


Pi is holding an instance of Rj

[NOTES] The number of solid black dots within the rectangle represents the number of instances for the resource. 

When an instance of Rj is assigned to Pi, we draw an edge from one dot within the rectangle to Pi. Assignment of an instance of resources to the process: a certain dot within the resource vertex to the process vertex.


## S10

Operating Systems

Example of a Resource Allocation Graph

No deadlock

P3->P2->P1

Can you identify a sequence of process executions so that all requests are met?

Is there a deadlock?

[NOTES] We have four resource types. Three processes.

We can actually examine the structure of the resource allocation graph to see whether the system has deadlock or not. Ideally, if the system has deadlock, the resource allocation must have a cycle. why? By the definition of deadlock 

In this case there is no deadlock. Can you find a sequence of process execution that all the processes finish execution? If P3 finishes, P2 can finish, and then P1 can finish.


## S11

Operating Systems

Resource Allocation Graph With A Deadlock

Does this mean a cycle in the graph always indicates a deadlock?

[NOTES] How many cycles are there in this resource allocation graph?

Two cycles.  First cycle: P2 waits for P3 and P3 waits for P2. Second cycle: P1 waits for P2, P2 waits for P3, and P3 waits for both P1 and P2. In this case, no process can make any progress. Deadlock.


## S12

Operating Systems

Resource Allocation Graph With A Cycle But No Deadlock

Process execution order that avoids a deadlock
P2->P4->P3->P1

[NOTES] One cycle. But no deadlock. Because P2 can finish and release R1. Then P4 can finish. Then, P3  and P1 can finish.


## S13

Operating Systems

Basic Facts

If graph contains no cycles  no deadlock

If graph contains a cycle 

If only one instance per resource type, then deadlock

If several instances per resource type, possibility of deadlock

[NOTES] So, in summary, if a graph contains no cycle, no deadlock for sure. Because we do not have the problem of A waiting for B and B waiting for A. 
If the graph contains a cycle, we need to look at the resource types. If only one instance per resource type, then there is a deadlock. Because no process can make any progress. If several instances per resource type, deadlock is possible, but not 100% sure.

We will introduce banker’s algorithm to solve the problem with multiple instances later on.


## S14

Operating Systems

Part 5:  Deadlocks and Starvation

Deadlock Problem
System Model
Deadlock Conditions
Deadlock Prevention
Deadlock Avoidance
Deadlock Detection


## S15

Operating Systems

Deadlock Conditions

Mutual exclusion: Only one process at a time can use a resource instance

Hold and wait: A process holding at least one resource is waiting to acquire additional resources held by other processes

Deadlock may arise if the following four conditions hold simultaneously 
(necessary, but not sufficient)

[NOTES] When there are multiple instances per resource type, we are not sure whether the graph has deadlock even if the graph has cycles. To handle this case, we study the deadlock conditions, that is, conditions necessary for a deadlock to occur. Deadlock can arise if the four conditions hold simultaneously. If any of them is violated, there is no deadlock. Also, the four conditions are necessary, but not sufficient.
We will briefly talk about the definitions here, and then give more examples in the later slides.


## S16

Operating Systems

Deadlock Conditions (Cont.)

No preemption: A resource can be released only voluntarily by the process holding it, after that process has completed its task

Circular wait: There exists a set {P0, P1, …, Pn} of waiting processes such that P0 is waiting for a resource that is held by P1, P1 is waiting for P2, …, Pn–1 is waiting for Pn, and Pn is waiting for P0

[NOTES] No preemption means we cannot take the resource from the process by force. Circular wait corresponds to a cycle in the resource allocation graph.


## S17

Operating Systems

Part 5:  Deadlocks and Starvation

Deadlock Problem
System Model
Deadlock Conditions
Deadlock Prevention
Deadlock Avoidance
Deadlock Detection


## S18

Operating Systems

Methods for Handling Deadlocks

Ensure that the system will never enter a deadlock state

Allow the system to enter a deadlock state and then recover

Ignore the problem and pretend that deadlocks never occur in the system
Used by most operating systems, including UNIX

[NOTES] There are multiple approaches to handling deadlocks. 

First, we can ensure that the system will never enter a deadlock state. That is deadlock prevention and avoidance. 

Second, we can allow the system to enter a deadlock state and then recover. That is deadlock detection.

Third, we simply ignore the problem and pretend that deadlocks never occur in the system. That means, do nothing. That is so called Ostrich approach. Why do most systems use Ostrich approach? Efficiency. The overhead of deadlock detection and prevention is high. Why do we learn about deadlock detection and prevention then


## S19

Operating Systems

Deadlock Prevention

Recall dining-philosopher solution using semaphores
Each chopstick is a shared resource protected by a binary semaphore (chopstick [ 5 ];)
Initially, for all i, chopstick [ i ] = 1;
Code (Process Philosopher i)
					while (1) {
						    wait(chopstick [ i ]);
						    wait(chopstick [ (i+1)%5 ]);
							eat
						    signal(chopstick [ i ]);
				   		    signal(chopstick [ (i+1)%5 ]);
							think
		   			}

Prevent at least one of the four deadlock conditions We will illustrate using Dining-Philosophers Problem

[NOTES] For philosopher i ( 0<=i<5): He first picks up his left chopstick, and then the right chopstick. This is done by calling the wait operation on the corresponding semaphore. If both operations can succeed, the philosopher can eat. After eating, he releases the left chopstick and then the right one. After that, the philosopher will think, and then repeat the process. 

Does this solution have any problem? Each philosopher executes the first line and a context switch occurs.  deadlock.


## S20

Operating Systems

Deadlock Prevention (Cont.)

Mutual Exclusion
Chopsticks are not shareable (simultaneously), hence this condition cannot be eliminated

Hold and Wait: Must guarantee that whenever a process requests a resource, it does not hold any other resource
Allow a philosopher to pick up chopsticks only if both the required chopsticks are available

Prevent at least one of the four deadlock conditions We will illustrate using Dining-Philosophers Problem

[NOTES] We will talk about how to prevent the deadlock conditions one by one. Recall, the four conditions are necessary to hold simultaneously for a deadlock to occur. So, we can prevent any one of them to happen. We illustrate that with Dining-Philosophers as an example.
 
Hold and wait: In Dining-Philosophers, allow a philosopher to pick up his chopsticks only if both the chopsticks are available. That means, at the beginning, the philosopher hasn’t taken any chopstick. In that case, there is no hold and wait. So, no deadlock.


## S21

Operating Systems

Deadlock Prevention (Cont.)

No Preemption 
If a philosopher cannot get the second chopstick, then preempt and release the chopstick that is being held

Circular Wait
Allow at most four philosophers to be hungry simultaneously
Odd-Even solution (see previous lecture)
Chopsticks can only be acquired in order (next slide)

Prevent at least one of the four deadlock conditions We will illustrate using Dining-Philosophers Problem

[NOTES] No preemption. To prevent this condition, we need to allow preemption. That is, If a process that is holding some resources requests another resource that cannot be immediately allocated to it, then all resources currently being held are released. The process restarts later. In Dining-Philosophers, if a philosopher cannot get another chopstick for a long time, preempt. That means, the philosopher needs to put down the chopstick, and then restarts.

Circular wait: In Dining-Philosophers, allow at most four philosophers to be hungry simultaneously. This is because of pigeon hole theory.


## S22

Chopstick Ordering to Prevent Circular Wait

Operating Systems

1

2

3

4

0

1st request

2nd request

A

B

C

D

E

[NOTES] In the dining philosopher problem, each chopstick has an ID. Suppose each philosopher takes the chopstick with the small id first, and then takes the chopstick with the large id. 
First request in black.
Second request in yellow.
 No circular wait. 
 No deadlock.


## S23

Operating Systems

Part 5:  Deadlocks and Starvation

Deadlock Problem
System Model
Deadlock Conditions
Deadlock Prevention
Deadlock Avoidance
Deadlock Detection


## S24

Operating Systems

Deadlock Avoidance

The deadlock-avoidance algorithm dynamically examines the resource-allocation state to ensure that the system never goes into an unsafe state
When a process requests an available resource, system must decide if immediate allocation leaves the system in a safe state
If safe, the request is granted, and otherwise, the process must wait 

System is in a safe state if there exists a safe completion sequence of all processes without deadlock

[NOTES] The deadlock prevention breaks one of the deadlock conditions. We now consider a more general deadlock avoidance algorithm. The algorithm is run whenever a process requests resources. The algorithm examines the resource-allocation state, and ensures that the system never goes into unsafe state. That is, when a process requests an available resource, system must decide if immediate allocation leaves the system in a safe state. If safe, the request is granted. Otherwise, the process must wait. 

So what is safe state? System is in safe state if there exists a safe sequence of all processes. We d


## S25

Operating Systems

Safe State

A process completion sequence <P1, P2, …, Pn> is safe, if for each Pi, the resources that Pi requests can be satisfied by currently available resources + resources held by all the Pj, j< i
If Pi’s needs cannot be immediately met, then Pi can wait until all Pj, j<i have finished
When all Pj (j<i) are finished, Pi can obtain needed resources, execute, return allocated resources, and terminate 
When Pi terminates, Pi+1 can obtain its resources, and so on
All processes in the sequence can finish

[NOTES] Sequence <P1, P2, …, Pn> is safe if for each Pi, the resources that Pi requests can be satisfied by currently available resources + resources held by all the Pj, with j< i. That is the processes before Pi in the sequence.


## S26

Operating Systems

Example of Safe Process Sequence

Available: 1

[TABLE]

Processes | Hold | Request

P1 | 1 | 1

P2 | 1 | 2

P3 | 1 | 3

Q1: Is <P1, P2, P3> safe?
Yes 
P1.request<=Available
P2.request<=P1.Hold+Available
P3.request<=P1.Hold+P2.Hold+Available

Q2: <P3, P2, P1> safe?
No
P3.request>Available

Q3: Is the system safe?
Yes 
Exists one safe sequence     <P1, P2, P3>

[NOTES] Consider a system with a single resource type. The number of instances available is one. There are three processes. P1 holds one instance and requests for one more and so on.


## S27

Operating Systems

Safe, Unsafe and Deadlock States

If a system is in safe state  no deadlocks

If a system is in unsafe state  possibility of deadlock
If a process releases resources much before its completion, then deadlock may not occur
 
Deadlock Avoidance: Ensure that a system will never enter an unsafe state

[NOTES] By definition, if a system is in a safe state, no deadlock.

If the system is in unsafe state, that means, there is no safe sequence for the system. It only means possibility of a deadlock. Because we are considering the worst case in the safe sequence: the resources are released only when the process finishes (the worst case). If the process can release resources before termination. The later processes in the sequence can actually release the resources earlier. So the previous process have more resources to consume. The safe sequence does not consider this case. So, the unsafe state does not 


## S28

Operating Systems

Banker’s Algorithm

An algorithm to check whether satisfaction of a resource request would lead to an unsafe state
For multiple instances of each resource type

When a process requests a resource it may have to wait (if the allocation leads to unsafe state)

Assumptions
Each process must declare the maximum instances of each resource type that it needs
When a process gets all its resources it must return them in a finite amount of time

[NOTES] Now, let’s learn the banker’s algorithm for deadlock avoidance. The algorithm decides whether to meet a resource request, and to avoid the unsafe state. By its name: there are many bankers. They can borrow and lend money to each other. The banker’s algorithm is to make sure that the bankers will not have a deadlock problem. 

It can be used for multiple instances of each resource type. If all resource types have a single instance, what algorithm can we use? We can use resource-allocation graph, and see if the resource-allocation graph has a cycle.

We have some assumptions on the process execu


## S29

Operating Systems

Data Structures for Banker’s Algorithm

Available (vector of length m): If Available [ j ] == k, there are k instances of resource type Rj  available
Max (n x m matrix): If Max [ i, j ] == k, then process Pi may request at most k instances of resource type Rj
Allocation (n x m matrix): If Allocation [ i, j ] == k, then Pi is currently allocated k instances of Rj
Need (n x m matrix): If Need [ i, j ] == k, then Pi may need k more instances of Rj  to complete its task
Need = Max – Allocation

n = number of processes; m = number of resource types

[NOTES] Before we introduce the banker’s algorithm, we define the data structures it uses.


## S30

Operating Systems

Banker’s Algorithm Part 1: Safety Algorithm

Let Work and Finish be vectors of length m and n, respectively; initially
Work = Available
Finish [ i ] = false for i = 1,2, …, n

Find an i such that (a)Finish [i] == false and (b)Need [ i, * ]  Work
If no such i exists, go to step 4

Work = Work + Allocation [ i, * ]; Finish[i] = true 
Go to step 2

If Finish [i] == true for all i, then the system is in a safe state
Otherwise the system is in a unsafe state

Work= Available + resources held by all Pj (Finish [ j ] = true)

What if multiple answers?

[NOTES] Let’s first introduce safety algorithm. The algorithm determines whether the current system is in a safe state or not. If the system is in a safe state,  we will find a safe sequence for the system. 

In the first step, we define two vectors work and finish to denote the current system state. Work represents the available resources during the execution of the algorithm. We will update it in Step 3. Finish denotes whether a process can be finished. If Finish[i] is true, this means Pi can finish. It is also updated in Step 3.

What if multiple answers? Any one can be chosen. If we go to step 3 a


## S31

Operating Systems

Example of Safety Algorithm

5 processes: P0 through P4
3 resource types: A (10 instances), B (5 instances) and C (7 instances)
Snapshot at time T0:  Allocation	 Max	 Available
				                A B C     A B C     A B C
		       P0	                         0 1 0       7 5 3      3 3 2
	                   P1	                2 0 0 	 3 2 2  
		       P2	                3 0 2 	 9 0 2
		       P3	                2 1 1 	 2 2 2
		       P4	                0 0 2	        4 3 3

[NOTES] Now, let’ s look at one example. There are five processes, P0 to P4. There are 3 resource types: A with 10 instances, B with 5 instances, and C with 7 instances. 

The system state at time T0 is as follows. 
Allocation
Max
Available
For example: P0 is allocated with 1 instance of B, and P0 may request 7 instances of A, and 5 instances of B, and 3 instances of C at most.


## S32

Then the matrix Need is defined to be Max – Allocation

	       Allocation           Max	                Need              Available
            A B C	      A B C 	     A B C   	         A B C
P0         0 1 0	       7 5 3	      	                     3 3 2
P1         2 0 0 	       3 2 2
P2         3 0 2 	       9 0 2
P3         2 1 1 	       2 2 2
P4         0 0 2	       4 3 3

Operating Systems

Example of Safety Algorithm (Cont.)

7 4 3

1 2 2

6 0 0

0 1 1

4 3 1

[NOTES] So, now, let’s calculate Need. By definition, Need=Max- Allocation.


## S33

Operating Systems

Example of Safety Algorithm (Cont.)

The working is as follows:

Work

P0
P1
P2
P3
P4

The system is safe 
(sequence <P1, P3, P4, P2, P0>)

[NOTES] Is there any other completion sequence? As long as you can find a completion sequence for the process, we can say the system is safe.


## S34

Operating Systems

Banker’s Part 2: Resource-Request Algorithm

Requesti = Request vector for process Pi
If Requesti [ j ] == k then process Pi wants k instances of resource type Rj



If Requesti  Needi, go to step 2
Otherwise, raise error condition, since process has exceeded its maximum claim

If Requesti  Available, go to step 3
Otherwise Pi  must wait, since resources are not available

V1<=V2 ≣ V1[j]<=V2[j], for all j

The ith row of the matrix

[NOTES] We now describe the algorithm for resource-request algorithm for a process Pi. We decide whether to grant the resource to the process or let the process wait.
 
The resource request by the process Pi is represented in a vector Request. If Request [j] == k then process Pi wants k instances of resource type Rj.


## S35

Operating Systems

Resource-Request Algorithm (Cont.)

Pretend to allocate requested resources to Pi  by modifying the state as follows:
Available = Available – Requesti;
Allocationi = Allocationi + Requesti;
Needi = Needi – Requesti;

Run the safety algorithm
Safe  the resources are allocated to Pi
Unsafe  Pi must wait, and the old resource-allocation state is restored


## S36

Operating Systems

Example of Resource-Request Algorithm

Suppose P1 requests (1, 0, 2) resources

Step1: Check Request1  Need1, (1,0,2)  (1,2,2)  true
Step2: Check that Request1  Available, i.e. (1,0,2)  (3,3,2)  true
Steps 3 & 4: 
Allocation	Max	    Need   Available
	   A B C	A B C	   A B C	   A B C
P0  0 1 0	7 5 3 	   7 4 3	    3 3 2
P1  2 0 0 	3 2 2 	   1 2 2
P2  3 0 2 	9 0 2	    6 0 0
P3  2 1 1 	2 2 2 	   0 1 1
P4  0 0 2	4 3 3	    4 3 1

Step 3: Pretend to allocate requested resources

3 0 2

0 2 0

2 3 0

Step 4: Executing safety algorithm shows that sequence <P1, P3, P4, P0, P2> is safe

[NOTES] In step 3, we pretend to allocate the requested resources. 
What are the parameters  that we need to change?
Do we need to change Max? no.


## S37

Operating Systems

Example of Resource-Request Algorithm

Can a further request for (1,0,2) by P1 be granted?
Step 1: Check if Request1  Need1, (1,0,2)  (0,2,0)  false
Can a further request for (0,2,0) by P0 be granted?
Step 1: Check if Request0  Need0, (0,2,0)  (7,4,3)  true
Step 2: Check if Request0  Available, (0,2,0)  (2,3,0)  true
	Allocation	Need	   Available
	    A B C 	A B C   	A B C 
P0    0 1 0	7 4 3	     2 3 0
P1    3 0 2	0 2 0 	
P2    3 0 2	6 0 0 
P3    2 1 1	0 1 1
P4    0 0 2	4 3 1
How about a request for (2,3,0) by P4?

2 1 0

We cannot find Needi < Available 
 Restore the state

7 2 3

0 3 0

[NOTES] Consider another case: Can further request for (0,2,0) by P0 be granted?
We can actually find that step 1 and step 2 are true. Thus, we pretend to give the resource to P0. Thus, we update the system state by modifying Allocation0, Need0 and Available0. 
Then, in step 4, we run the safety algorithm. However, in step 2 of the safety algorithm, we cannot find any process with Needi<=Available. Thus, the system is unsafe.
What should we do? We should restore the old state.

How about a request for (2,3,0) by P4 ? 
This is for your homework.


## S38

Operating Systems

Part 5:  Deadlocks and Starvation

Deadlock Problem
System Model
Deadlock Conditions
Deadlock Prevention
Deadlock Avoidance
Deadlock Detection


## S39

Operating Systems

Deadlock Detection

Allow system to enter deadlock state

Then invoke detection algorithms
For single instance of each resource type (in textbook based on identifying cycle in resource-allocation graph)
For multiple instances of each resource type (next few slides)

Then invoke recovery algorithm (in textbook)

This slide and the later slides in this chapter are not examinable

[NOTES] The basic idea of deadlock detection is to allow system to enter deadlock state, then invoke detection algorithm periodically. If there is a deadlock, we invoke the recovery algorithm. 
The deadlock detection algorithm is actually similar to deadlock avoidance algorithm. If you are interested in them, you can refer to textbooks or just go through them in slides. They are not examinable.


## S40

Operating Systems

Multiple Instances of Each Resource Type

Available: A vector of length m indicates the number of available resource types
Allocation: An n x m matrix defines the number of resources of each type currently allocated to each process
Request: An n x m matrix indicates the current request  of each process.  If Request [ i, j ] = k, then process Pi  is requesting k more instances of resource type Rj


## S41

Operating Systems

Detection Algorithm

Let Work and Finish be vectors of length m and n, respectively; initially
Work = Available
For i = 1,2, …, n, if Allocationi != 0, then Finish[ i ] = false, else Finish[i] = true

Find an i such that (a)Finish [i] == false and (b)Request [ i, * ]  Work
If no such i exists, go to step 4

Work = Work + Allocation [ i, * ]; Finish[i] = true 
Go to step 2

If Finish [i] == false for some i, then system (process Pi) is deadlocked

[NOTES] Let’s first introduce safety algorithm. The algorithm determines whether the current system is in a safe state or not. If the system is in a safe state,  we will find a safe sequence for the system. 

In the first step, we define two vectors work and finish to denote the current system state. Work represents the available resources during the execution of the algorithm. We will update it in Step 3. Finish denotes whether a process can be finished. If Finish[i] is true, this means Pi can finish. It is also updated in Step 3.

What if multiple answers? Any one can be chosen. If we go to step 3 a


## S42

Operating Systems

Example of Detection Algorithm

Five processes: P0 through P4
Three resource types: A (7 instances), B (2 instances), and C (6 instances)
Snapshot at time T0:    Allocation	Request	  Available
				A B C 	A B C 	    A B C
		P0		0 1 0 	0 0 0 	     0 0 0
		P1		2 0 0 	2 0 2
		P2		3 0 3	0 0 0 
		P3		2 1 1 	1 0 0 
		P4		0 0 2 	0 0 2

Sequence <P0, P2, P3, P1, P4> results in Finish[i] = true for all i


## S43

Operating Systems

Example of Detection Algorithm (Cont.)

Suppose P2 requests an additional instance of type C

	Allocation   Request	Available
	 A B C        A B C 	A B C
P0 0 1 0         0 0 0 	0 0 0
P1 2 0 0         2 0 2
P2 3 0 3         0 0 1 
P3 2 1 1         1 0 0 
P4 0 0 2         0 0 2

Work

0 0 0

A B C

P0

0 1 0

+

0 1 0

Finished


## S44

Operating Systems

Example of Detection Algorithm (Cont.)

State of system?

Can reclaim resources held by process P0, but insufficient resources to fulfill other process requests

Deadlock exists, consisting of processes P1,  P2, P3, and P4


## S45

Operating Systems

Advanced Readings

“The Deadlock Problem:  An Overview”, By Sreekaanth S. Isloor, T. Anthony Marsland. (pdf in NTULearn)
 Other readings
Java Concurrency, http://docs.oracle.com/javase/tutorial/essential/concurrency/index.html
Deadlock, http://en.wikipedia.org/wiki/Deadlock

[NOTES] Those are advanced readings, if you want to know more beyond the text book.
