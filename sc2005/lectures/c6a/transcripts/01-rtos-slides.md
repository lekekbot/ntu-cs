# Part 6a — Real-Time OS (slide deck S1–S19)

Verbatim text of `Part6a (RTOS).pptx` (19 slides), slide by slide; lines starting `[NOTES]` are the
lecturer's speaker notes. There is no audio recording for this deck, so citations are slide numbers
(`S17`), not timestamps.


## S01

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


## S02

Operating Systems

Part 6a: Real-Time OS

What is a Real-Time OS (RTOS)?
Real-Time Process Specification
Real-Time CPU Scheduling

[NOTES] In this part, we take a closer look at Real-Time Operating Systems (RTOS). We understand the applications and their requirements for which a RTOS is appropriate. We then look at some of the key features and functions of a RTOS, over and above the services in a standard OS.

We then look at some examples of CPU scheduling algorithms that are specific to RTOS and provide the appropriate functions essential to meet application requirements.

Finally, we take a look at some of the techniques for hardware virtualization, understand what virtualization means, as well as list some popular examples.


## S03

Operating Systems

Cyber-Physical Systems

Physical/Engineered systems whose operations are monitored, coordinated and controlled by a reliable computing and communication core
Automotive Systems (Autonomous driving, Parking assist, Airbag controls)
Avionics (Flight navigation & control)
Manufacturing Systems (Robotics, Process controls)
Medical Systems (Robotic surgery, devices)
…

[NOTES] Trend 1: Proliferation of sensor devices. As these devices include embedded processors that are increasingly becoming smaller and also more powerful and plentiful; that is, they are everywhere and can support complex functionalities. They range from simple environmental monitoring, to medical devices, to cargo ships, to factories, to smart spaces that are for assisted living for elderly or disabled.

Trend 2: The second trend is that these systems are increasingly being integrated as system of systems. These integrations can range from simple interconnection to exchange sensor data, to inter-o


## S04

Operating Systems

Relevance of Real-Time

Common to many application examples we saw in the previous slide:
Collect data from various sensing devices
Execute control law(s) to determine response
Send actuator commands in a reasonable amount of time

Collision avoidance and braking

Pacemaker timing diagram

[NOTES] Common requirements among several of the CPS applications is that of real-time. Meaning the applications are required to process inputs and generate outputs within a pre-defined amount of time. We can call this time the application deadline. Not only does the application have to produce a functionally correct output, but it must do so within this deadline. So, for such applications, both functional/logical correctness as well as temporal correctness or timeliness are equally important.

Couple of examples of such real-time CPS applications are given here. One is that of a pace-maker, which is 


## S05

Operating Systems

What is a Reasonable Time?

What is the functionality?
Collision avoidance in automotive (milliseconds)
Pacemaker (up to a second)
Robotic surgery (varies greatly depending on the target)
What are the environment constraints?
Available computing and communication resources
Timing characteristics of sensors/actuators/operations
Failure-mitigation strategies?
Time to detect and recover from failures
Example: execution replication for redundancy

[NOTES] Although several CPS applications have hard real-time requirements (deadlines), the notion of these requirements are dependent on various factors. 

It depends on the type of functionality. The notion of real-time could range from a few milliseconds to potentially even few minutes. Longer time durations would usually then not be considered as real-time requirements, but instead would be regarded as design-time planning.

It also depends on the constraints imposed by the surrounding environment, such as available computing and communication resources, the timing characteristics of the mechanica


## S06

Operating Systems

Common Misconception

Real-Time ≠ Fast
Real-Time = Predictable even in the worst-case





“Man drowned in a river with average depth 20 cms”

[NOTES] A common misconception is that real-time requirements imply fast execution on an average or simply fast response times. This is not true at all.
Real-time requirements imply guarantees on the worst-case response times, AND NOT average case response times. So, in the worst-case, the execution of the application must be completed within the pre-specified deadline.


## S07

Real-Time CPS / Real-Time OS

Operating Systems

Definition: System whose correctness depends not only on the logical/functional aspects, but also on the temporal aspects
Application has deadlines that must be met
A real-time OS (RTOS) provides OS services to such systems (e.g., FreeRTOS, MicriumOS, …)
Key performance measure for RTOS
Timeliness/Predictability on timing constraints (deadlines)
Significance of worst-case over average-case
Deadlines are a function of application requirements

[NOTES] In summary, the key focus of real-time CPS, and hence real-time OS, is that of ensuring predictability over the timing constraints. In the worst-case, the timing requirements of the application must be met. This worst-case must take into account the impact from mechanical devices, computation (both software and hardware), communication, etc.


## S08

Operating Systems

Part 5: Real-Time OS & Virtualization

What is a Real-Time OS (RTOS)?
Real-Time Process Specification
Real-Time CPU Scheduling


## S09

RTOS (Real-Time) Process

Operating Systems

Definition: A real-time process is specified as <R,C,D>, where R is process release time, C is execution requirement and D is relative deadline
Requires C time units of CPU in the interval [R, R+D)
How does one determine these parameters?
Example: P1<0,5,10>, P2<5,10,35>, P3<20,10,30>




In this lecture, we assume processes only have a single CPU burst; C is the duration of this burst

[NOTES] We now consider how to model a real-time RTOS process. We need to know when the process is released for execution in the system. We need to know how much CPU cycles it needs in the worst-case. We also need to know by when it requires these CPU cycles. Only with these parameters can the RTOS manage the processes to ensure that their real-time requirements (deadlines) can be met.

It is an interesting question to understand how one could determine these process parameters. R and D are straightforward. Usually they are derived depending on the application requirements. How often or when the appli


## S10

Recurrent Real-Time Process

Operating Systems

Nature of real-time processes
Collect data from sensing devices, execute control laws to determine responses, and send actuator commands in reasonable time
Repeat the above steps regularly
Examples: airbag control, flight control, collision avoidance, pacemaker, etc. 
A recurrent real-time process
Executes some function repeatedly over time
Each instance of execution is a real-time process <R,C,D>

[NOTES] In many real-time applications, the nature of a real-time process is repetitive. Meaning it needs to execute the real-time function repeatedly over time. Each instance of such a recurrent real-time process is a real-time process with parameters <R,C,D>.

Depending on the nature of repetition, there are two broad types of recurrent real-time processes. We will look at these in the next couple of slides.


## S11

Periodic Real-Time Process

Operating Systems

Definition: A process that repeats periodically
Processes generated by a time-triggered phenomena (sensor sending data periodically)
Example: Perception function for collision detection
A periodic process is specified as <T,C,D>, where T is process period, C & D are as defined earlier
Real-time processes are released at R=0, T, 2T, …
Example: Periodic process P<10, 5, 7>

[NOTES] One type of recurrence is the periodic recurrence, in which real-time processes are released in the system periodically at fixed time intervals. Several time-triggered functions fall in this category.


## S12

Operating Systems

Part 6a: Real-Time OS

What is a Real-Time OS (RTOS)?
Real-Time Process Specification
Real-Time CPU Scheduling (short-term scheduler)
Fixed-priority scheduling
Dynamic-priority scheduling

[NOTES] In this section we focus on the problem of CPU scheduling, that is the short-term scheduler from Week 3. We see how the algorithms we studied in Week 3 perform for real-time processes and what new algorithms we can consider for this specific application domain.


## S13

Why Classic Algorithms Fail?

Operating Systems

Consider real-time processes (non-recurring): P1<0,20,30>, P2<0,5,10>, P3<5,10,35>, P4<20,10,30>, P5<25,5,10>










  They don’t prioritize deadlines and hence perform poorly

FCFS schedule

SJF schedule

RR(q=5) schedule

P1

P2

P5

P3

P4

P2

P3

P1

P5

P4

P1

P1

P1

P1

P2

P5

P4

P4

P3

P3

[NOTES] Lets take a closer look at how the classic CPU scheduling algorithms that we learned in Week 3 fair for the real-time process scheduling problem. Are they effective in meeting process deadlines?

None of them do well in terms of the performance measure for real-time processes, that is meeting deadlines. This is expected, because none of them focus/prioritize on deadlines.


## S14

Real-Time CPU Scheduling Problem

Operating Systems

Given a set of periodic/sporadic real-time processes, find a uni-processor CPU scheduling algorithm that can meet process deadlines
We will use a running example (periodic real-time process set): P1<10,6,10>, P2<19,4,19>, P3<20,2,20>

0		10	          19 20		30	        38

P1<10,6,10>

P2<19,4,19>

P3<20,2,20>

P1

P2

P3

P1

P1

P2

[NOTES] In this section we will focus on the short-term CPU scheduler (ready queue scheduler) for a set of periodic real-time processes scheduled on a uni-processor CPU. Although example focuses on periodic processes, the same techniques can be applied to sporadic processes as well.


## S15

Fixed-Priority CPU Scheduling

Operating Systems

Priorities are fixed for each recurrent process
Priorities are fixed across instances of recurrent processes
Suppose instance of P1(R=0) has higher priority than instance of P2(R=0). Then,
P1(R=10) has higher priority than P2(R=0)
P1(R=10) has higher priority than P2(R=19)
P1(R=20) has higher priority than P2(R=19) …

[NOTES] Fixed-priority CPU scheduling is a class of schedulers in which priorities are fixed at the level of each periodic/sporadic process. So priorities don’t change across process instances.

We will look at two examples of this class of schedulers.


## S16

Rate Monotonic (RM) Scheduler

Operating Systems

Assign priorities based on process periods / minimum release-separation time (T)
Shorter T implies higher priority
Ties are broken arbitrarily






RM is a very popular short-term CPU scheduler in the real-time CPS industry. Why?

0	    6 	10	   16   19 20	    26 	30	         38

P1<10,6,10>

P2<19,4,19>

P3<20,2,20>

P1

P2

P3

P2

P1

P1

[NOTES] Under RM scheduling, priorities are assigned based on the process periods or minimum release-separation times. Smaller this value, higher is the priority. Ties are broken arbitrarily.

RM is a popular choice in the real-time CPS industry. For high-priority periodic/sporadic processes it gives a very predictable schedule. So important processes can be given high priority under RM.


## S17

RM and Process Deadlines

Operating Systems

RM is good, but still does not always prioritize urgent processes
Suppose we modify the process set as follows: P1<10,6,10>, P2<19,4,19>, P3<20,2,14>

0	    6 	10         14 16   19 20	    26 	30	         38

P1<10,6,10>

P2<19,4,19>

P3<20,2,14>

P1

P2

P3

P2

P1

P1

Deadline Miss

[NOTES] Since RM ignores the relative deadline parameter D, it can potentially miss deadlines for some process sets as shown in this slide.


## S18

Earliest Deadline First (EDF) Scheduler

Operating Systems

Dynamic-priority scheduler that assigns priorities based on process instance deadlines
Instances with shorter deadline are given higher priority
NOT the same as parameter D
Ties are broken arbitrarily





EDF is a dynamic-priority scheduler, hence more powerful than RM

0	    6    8  10  12    14  17 19 20              26  28 30        34  36 38

P1<10,6,10>

P2<19,4,17>

P3<20,2,14>

P1

P3

P1

P2

P2

P1

P3

[NOTES] EDF is a dynamic-priority scheduler that changes priorities across process instances based on their actual deadlines. This allows a lot of flexibility to EDF and hence it is able to perform really well in terms of meeting deadlines.

Then, why is RM more popular in the real-time CPS industry? Lets take a closer look at the advantages and dis-advantages of these two classes of schedulers.


## S19

RM versus EDF

Operating Systems

Simpler implementation (separate queue for each recurrent process)

Predictability for high priority processes, even under high load

Harder implementation (online sorting of queue based on instance deadlines)

Can be unpredictable under high load

RM

EDF

[NOTES] RM are easy to implement. A simple priority-based queue data structure would suffice. There can be one queue per recurrent process. In fact, efficient O(1) time complexity implementations are available for RM using bitmaps.

EDF implementation requires an online sorting strategy, because process instance deadlines are only known once the processes are released in the system (true for sporadic processes). Further it is not possible to separate the instances into separate queues offline, like in RM/DM. The best known time complexity for implementation of EDF is O(log n), where n is the number of
