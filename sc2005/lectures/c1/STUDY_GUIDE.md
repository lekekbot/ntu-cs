# SC2005 — Introduction & Background: Study Guide

Companion to `Part1 (Intro and Background)(1).pptx`, 46 slides. Citations are slide numbers:
**`S17`** = slide 17 of the deck. There is no recording, so there are no timestamps in this folder.

Transcript: [01 — slide deck S1–S46](transcripts/01-intro-and-background-slides.md)

**S29 and S30 are printed with "This slide is not examinable."** They are covered in §5 for
completeness only — see [NOTES.md](NOTES.md) §3.

---

## 0. The chapter in one picture

Four jobs: say **what an OS is**, survey **what kinds exist**, **revise the hardware** it controls,
and show **how a program reaches it**.

```
                              users                                    S04, S05
                                |
                    application programs          "defines the ways resources are used"
                                |  API -> system call                   S41, S42
        +-----------------------------------------------+
        |            OPERATING SYSTEM (kernel)          |  resource allocator  \
        |   hides hardware, allocates CPU/memory/I/O    |  control program      > S06
        +-----------------------------------------------+  kernel              /
                |                          ^
   privileged instructions          traps / interrupts switch
   only in monitor mode (S33,S35)   the mode for you (S33, S43, S44)
                |                          |
        +-----------------------------------------------+
        |      HARDWARE:  CPU | memory | I/O devices    |                 S04
        +-----------------------------------------------+
          bus, device controllers, local buffers, DMA                 S22-S27
```

| # | Question | Slides | Section |
|---|---|---|---|
| 1 | What *is* an operating system? | S01–S06 | §1, §2 |
| 2 | What *types* of computing system exist? | S08–S19 | §3 |
| 3 | What must the OS control, and how? | S21–S38 | §4, §5, §6 |
| 4 | How does a program reach the OS? | S39–S44 | §7, §8 |

### The deck's own outline

The same four-item outline slide appears four times — **S01, S07, S20, S39** — and those are the act
dividers:

```
S01  Part 1: Introduction      What is an Operating System (OS)?
                               Types of Computing Systems
                               Computer System Architecture (Review)
                               Operating System Services
S07  ---- divider before "Types of Computing Systems"
S20  ---- divider before "Computer System Architecture (Review)"
S39  ---- divider before "Operating System Services"
```

| Slides | Topic | Weight |
|---|---|---|
| S01–S06 | What an OS is: motivation, definition, goals, components, three definitions | definitional |
| S08–S19 | Types of computing systems | definitional + one comparison |
| S21–S28 | Computer-system operation: bus, **interrupts**, **DMA** | *core* — mechanism questions |
| S29–S30 | Storage hierarchy, caching | **not examinable** |
| S31–S38 | Hardware protection: **dual mode**, **I/O**, **base/limit** | *core* — expect the arithmetic |
| S40–S44 | Services, **system calls**, the trap/interrupt pair | *core* — expect the four-step diagrams |
| S45–S46 | Readings, future OSes | trivia |

---

## 1. Why learn operating systems (S02)

| Claim on the slide | What it buys |
|---|---|
| "Operating systems are the core of computer systems" | nothing above it can be explained without it |
| **Goal: hide the system complexity from developers** | the one-sentence purpose |
| **Why:** simplicity of programming | the benefit |
| **How: abstractions, policies, and mechanisms** | the technique |
| "Foundation to understand advanced systems (cloud, databases, AI-as-a-Service, Internet-of-Things)" | why it still matters |
| "Focus on abstractions and principles not implementation" | what is examined |
| System architects need depth; app developers need enough to optimise | two audiences, two depths |

The three words in the fourth line are three different things, and later chapters use each:

| Word | Question | Later example |
|---|---|---|
| **Abstraction** | what does the developer see? | a process, a file, an address space |
| **Mechanism** | how is it done? | a page table, an interrupt vector, a context switch |
| **Policy** | which alternative is chosen? | CPU scheduling, page replacement |

Keeping mechanism and policy apart is what lets the *same* mechanism serve a different policy — most
exam questions that look like "which algorithm?" are really "which is the policy?".

---

## 2. What an operating system is (S01, S03–S06)

### 2.1 The definition (S03)

> A program that acts as an **intermediary between a user and the computer hardware**.

| Element | Why the notes stress it |
|---|---|
| "a **program**" | the OS is **software**, not hardware |
| "an **intermediary**" | a user's job passes *through* the OS to the hardware, and results pass back |
| "**user** … **hardware**" | it is the only layer that knows both sides |

### 2.2 The two goals, and the conflict (S03)

| Goal | Meaning |
|---|---|
| **User convenience** | hide hardware complexity (`fopen` instead of sectors) |
| **Efficient hardware utilisation** | smart allocation of CPU, I/O devices, memory |

> "These two goals **can be contradictory**."
> "Smart resource allocation may require **lot of information about user programs**."

That is the trade-off in two lines: a *better* policy needs *more* information, gathering
information is overhead, and the abstraction that made programming simple is precisely what hides
that information. Every system in §3 is a different point on this one axis:

| System | Goal that wins | Evidence |
|---|---|---|
| Batch | efficiency | batching, automatic job sequencing (S10) |
| Time-sharing | convenience **and** efficiency | "highly interactive", but still multiplexed (S11, S13) |
| Desktop | **convenience** | "user convenience and responsiveness is the main focus" (S14) |
| Embedded / CPS | **efficiency** | "resource constrained… required to be very efficient" (S15) |
| Handheld | **both** | notes: one of the few systems where both matter (S17) |

### 2.3 The four components (S04, S05)

```
+---------------------------+
| users                     |  "People, machines, other computers"
+---------------------------+
| application programs      |  compilers, database systems, video games, business programs
+---------------------------+
| operating system          |  controls and coordinates the use of the hardware
+---------------------------+
| hardware                  |  CPU, memory, I/O devices
+---------------------------+
```

Note that **users include machines and other computers** — a program can be a user of an OS. And the
layers are strict: application programs do not touch hardware. The only deliberate blurring is the
**system call** (§8) and the **kernel module** (§6.3).

### 2.4 Three definitions (S06)

| Definition | Slide text | Implies |
|---|---|---|
| **Resource allocator** | "Manages and allocates hardware resources" | bookkeeping for CPU, memory, devices |
| **Control program** | "Controls the execution of user programs and operations of I/O devices" | it must be able to stop a program and start another — i.e. interrupts (§4) |
| **Kernel** | "The one 'core' program that is always ready to accept new commands from the users as well as hardware (all else being application programs)" | it is always resident and always listening |

The kernel line is the one that gets misread. Keep three things apart:

| Word | What it names |
|---|---|
| **kernel** | the always-resident core *code* |
| **kernel mode** | a *hardware* mode of the CPU (§6.2) |
| **root / administrator** | a *user account* (§6.3) |

---

## 3. Types of computing systems (S08–S19)

S08 lists seven, and the order is **historical**: each exists because the previous one wasted
something.

| Type | What it fixes or is | Slides |
|---|---|---|
| Simple batch | the **setup cost** of running a job | S10 |
| Multiprogramming | the **idle CPU** while a job waits for I/O | S11, S12 |
| Time-sharing | the **user waiting** for a whole batch | S13 |
| Desktop | one user, many devices | S14 |
| Embedded / cyber-physical | resource constraints, physical control | S15 |
| Real-time | a missed deadline is a **failure** | S16 |
| Handheld | small memory, slow CPU, small screen | S17 |
| Multiprocessor (hardware, not usage) | one CPU is not enough | S18, S19 |

### 3.1 Simple batch systems (S10)

| Property | Slide text |
|---|---|
| Purpose | "Reduce setup time by batching similar jobs" |
| Mechanism | "Automatic job sequencing – automatically transfers control from one job to another" |
| Memory | "Simple memory layout"; "Only one user job in memory at any time point" |
| Weakness | "Not very efficient: when job waits for I/O, CPU idles" |

```
setup is expensive -> batch similar jobs, set up once
                   -> someone must start job 2: automatic job sequencing (the ancestor of scheduling)
                   -> memory holds ONE job, so while it blocks on I/O the CPU has nothing to run
```

**The number.** A job needing 20 ms CPU and 80 ms I/O gives `20 / 100 = 20 %` utilisation. That 20%
is the reason multiprogramming exists. (Derived from "CPU idles"; S10 does not print it.)

Two traps: **batch is not OS-less** — the batch monitor *is* the OS, and job sequencing is its
scheduler. And **"not efficient" means idle, not slow**: the hardware is fully used while computing.

### 3.2 Multiprogrammed systems (S11) and the features they force (S12)

S11: **"Several jobs are kept in main memory at the same time, and the CPU is multiplexed among
them."**

| Property | Slide text |
|---|---|
| Memory | "The program data of multiple jobs are stored in the main memory at the same time, instead of a single job" (notes) |
| Swapping | "A job is swapped in and out of memory to the hard disk" |
| Interaction | "System is highly interactive; supports multiple online users" |
| Examples | "desktops, servers" |
| Why better | **efficiency** — CPU utilisation (notes) |

With four or five such jobs resident there is always something runnable, so utilisation climbs from
20% toward 100%. The gain comes from **overlap**, not from a faster CPU.

**S12 names three features — and with them, three later chapters.** The notes state the principle:
*"scheduling the usage of shared resources: memory, CPU and devices."*

| Resource | Feature | Slide text | Taught in |
|---|---|---|---|
| Memory | **Memory management** | "To allocate memory to several jobs" (allocate for new jobs, deallocate when one ends) | `c8`, `c9` |
| CPU | **CPU scheduling** | "To choose among several jobs ready to run" | `c3` |
| Devices | **I/O device scheduling** | "Allocation of I/O devices to jobs" | `c12` |

Each item is a *shared resource* plus a *decision*. Note what is **absent**: synchronisation and
deadlock, which multiprogramming also creates — those are `c5` and `c7`.

### 3.3 Time-sharing systems (S13)

| Property | Slide text |
|---|---|
| Concurrency | "The CPU is multiplexed among several jobs that are in memory" |
| Swapping | "A job is swapped in and out of memory to the disk" |
| Interaction | "On-line communication between the user and the system is provided" |
| **Defining sentence** | "when the operating system finishes the execution of one command, it seeks the next command from the user" |

S13's body is almost identical to S11's; only the last sentence is new, and it is the definition:
**multiprogramming is a scheduling property, time-sharing is an interaction property built on it.**

| | Multiprogramming | Time-sharing |
|---|---|---|
| Goal | keep the **CPU** busy | keep the **user** responsive |
| Needs | memory management + scheduling | that **plus** a time quantum and terminal I/O |
| Slide | S11 (whose title pairs the two) | S13 |

### 3.4 Desktop systems (S14)

"Personal computers – computer system dedicated to a single user"; "several I/O devices – keyboard,
mouse, display screens, printers"; "**user convenience and responsiveness is the main focus**";
"Windows, MacOS, UNIX, Linux".

Two examinable consequences from the notes:

1. **Many devices ⇒ device drivers are a large part of the code base** (compare `c12`'s four kernel
   I/O layers). This is why a desktop kernel dwarfs its scheduler.
2. **Responsiveness is traded against efficiency** — a desktop OS will waste CPU to keep the UI
   smooth. That is S03's left-hand goal, deliberately chosen.

### 3.5 Embedded and cyber-physical systems (S15)

"Physical systems whose operations are **monitored and controlled** by a **reliable** computing and
communication core." Constraints: "low power, small memory, low bandwidth, etc." Domains:
"Real-time, Handheld, Automotive, Avionics, Industrial Controls, Sensor networks".

The nesting is stated on the slide itself, and confirmed in the S16/S17 notes:

```
cyber-physical / embedded            S15
   +-- real-time      (with hard timing constraints)    S16
   +-- handheld       (phones, tablets)                 S17
   +-- automotive, avionics, medical, industrial, sensor networks
```

"**Reliable**" is not decoration: for a CPS a failure is not a reboot, it is a crash in the physical
world.

### 3.6 Real-time systems (S16)

| Property | Slide text |
|---|---|
| Role | "A control device in a dedicated application such as industrial controls, automotive, avionics, medical devices" |
| **Defining property** | **"Well-defined fixed-time constraints"** |
| **Rule** | **"Job must be completed within a deadline"** |
| Example | "Airbag control in cars" |

Notes: *"Operations must be finished within the defined time constraints, **otherwise the system will
fail**"*; real-time systems are "a **subset of embedded and cyber-physical systems** — those with
stringent timing requirements".

**Fast ≠ real-time.** Real-time means *correctness depends on when the answer arrives*. An airbag
trigger 10 ms late is not slow, it is wrong. The slide's "Example real-time OSes" list is not in the
text extraction; the notes point to the week-7 e-learning lecture, and the course has
[`../c6a`](../c6a) for real-time OS.

### 3.7 Handheld systems (S17)

| Issue | Slide | What the OS does (notes) |
|---|---|---|
| "Limited memory" | yes | PCs have "several GB"; handheld memory is the scarce resource |
| "Slow processors" | yes | power and thermal limits |
| "Small display screens" | yes | "the system needs to do some **clipping** in order to fit the content" |

OSes: "iOS, Android, HarmonyOS". Handhelds are "a **subset of embedded and cyber-physical
systems**", and they are "**one of the few systems in which both** user responsiveness *and*
efficiency" matter — they cannot pick a side of S03's trade-off.

### 3.8 Multiprocessor systems (S18, S19)

S18 is a figure only: **a dual-core CPU** — two cores sharing main memory, each with its **own
registers and caches**. S19 generalises it.

| Property | Slide text |
|---|---|
| Definition | "More than one CPU, or CPU with multiple cores (also called multi-core systems)" |
| Coupling | "**Tightly coupled**: communication usually takes place through **shared memory**" |
| Advantage 1 | "Increased system **throughput**" |
| Advantage 2 | "**Economical** due to sharing of memory and I/O devices (compared to multiple single CPU systems)" |
| Advantage 3 | "Increased **reliability** due to **redundancy**" |

| Advantage | Mechanism | One-line justification |
|---|---|---|
| Throughput | more execution units | n cores retire more work — *if* the work divides |
| Economical | shared memory, shared I/O, one chassis | n single-CPU machines need n of everything |
| Reliability | redundancy | one CPU fails, the rest continue |

**The pair most often confused**, both defined in the S19 notes:

| Term | Notes definition |
|---|---|
| **Multi-programming** | "the system can run multiple **programs**" |
| **Multi-processing** | "the system can run on multiple **CPUs** or CPU with multiple cores" |

```
multi-PROGRAMMING -> many programs, 1 CPU
multi-PROCESSING  -> many CPUs,    any number of programs
```

They are independent: S11 is multiprogramming on one core; a parallel program on 4 cores is
multiprocessing with one program. **Loosely coupled** = "OSes running on distributed computers" —
a different course.

---

## 4. Computer-system operation (S21–S28)

S21 opens the architecture act with three sub-topics, and calls the whole act "essentially a brief
review of what you learnt in CE/CZ1006": **Computer System Operation** (S22–S28), **Storage
Hierarchy** (S29–S30, not examinable), **Hardware Protection** (S31–S38).

### 4.1 The machine (S22, S23)

S22 is a figure: CPU, controllers, buffers, a shared **bus**, and an arrow labelled **Interrupt**.
S23 gives the five facts it draws:

1. "I/O devices and the CPU can execute **concurrently**" — the basis of all of §3.2.
2. "Each **device controller** is in charge of a particular device type" — one per kind, not per device.
3. "Each device controller has a **local buffer**."
4. "Device controller moves data between **local buffer and memory**."
5. "Device controller informs CPU that it has finished by causing an **interrupt**."

The notes add what the figure cannot show: CPU and controllers "**compete for the bus cycles**" —
which is why DMA (§4.5) is not free.

```
        +---------+        +---------+        +---------+
        |   CPU   |        | memory  |        |  disk   |
        +----+----+        +----+----+        | contr.  |--[buffer]-- disk
             |                  |             +----+----+
        =====+==================+==================+=====  system bus
             |                  |
        +----+----+        +----+----+
        |  ...    |        | printer |
        +---------+        | contr.  |
                           +---------+
```

### 4.2 Interrupts (S24)

| Clause | Meaning |
|---|---|
| "An interrupt transfers control to the **interrupt service routine** generally through the **interrupt vector**, which contains the addresses of all the service routines" | the vector is an **array of ISR addresses**, indexed by type |
| "Incoming interrupts are **disabled** while another interrupt is being processed **to prevent any loss of interrupts**" | handling is serialised, and the slide gives the reason |
| "A **trap** is a **CPU generated** interrupt caused either by a software error or request" | traps come from the program, not a device |
| "Unhandled exceptions in user program" | the "software error" case |
| "An operating system is typically **interrupt driven**" | the OS is reactive |
| "If the OS is not interrupt driven, it would be required to **poll** for task/event completions" | the alternative |

| | Interrupt-driven | Polled |
|---|---|---|
| Who initiates | the device | the CPU, repeatedly |
| Cost when idle | ~zero | the whole polling loop, forever |
| Latency | immediate | up to one poll interval |

(Real hardware adds priorities so that higher-priority interrupts *can* preempt a handler; the slide
states the simple version — answer with the slide's version.)

### 4.3 Interrupt handling (S25)

| Step | Slide text | Needs |
|---|---|---|
| **1 save** | "preserves the state of the CPU by storing **registers** and the **program counter**" — "Also called a **context switch**" | somewhere to save it (stack / PCB) |
| **2 identify** | "determines which type of interrupt has occurred. Separate segments of code determine what action should be taken for each type" | the interrupt number, from a CPU register (notes) |
| **3 dispatch** | "identifies the appropriate **interrupt service routine**… Obtained from the **interrupt vector table**" | the vector |

```
device raises interrupt
   [1] hardware saves PC + registers      <- the context switch
   [2] software reads the interrupt type
   [3] ISR = vector[type]
   [4] run the ISR (in monitor mode, S33)
   [5] restore state, resume the interrupted program
```

> **Trap.** "Context switch" here covers both the interrupt save/restore *and* the switch between
> processes. Same mechanism; the difference is whether the state returns to the same process.

### 4.4 The interrupt-driven I/O timeline (S26)

S26 has three rows — **Job 1, Job 2, OS** — and four states (notes: "two states for CPU … two states
for I/O device").

```
time  ------------------------------------------------------------------>
CPU   | Job 1 | Job 1 | Job 2 | Job 2 | Job 2 | OS  | Job 2 | Job 1 | ...
device| idle  |<------ transferring ------>| idle |<--- transferring --->|
                        ^                   ^
                   I/O request        I/O completes -> INTERRUPT
```

1. Device **idle**, CPU runs **Job 1**.
2. An I/O request is issued.
3. The CPU **does not wait**; it continues with **Job 2** ("recall multiprogrammed system").
4. I/O completes; an **interrupt** is issued; the device becomes **idle**.
5. The CPU runs the **OS** (the ISR), then resumes a job.

Three observations: the **OS row is a sliver** (handling must be fast — the argument for DMA); the
**CPU never idles** because a second job is ready; the **device is idle most of the time**, which is
what a request queue is for (`c12`).

### 4.5 Direct Memory Access (S27)

The notes give the motivation as an extreme: *"you want to copy **1 TB** of data, and each byte
causes an interrupt in the worst case … interrupt has considerable overhead in saving the state and
resuming execution."*

```
1 TB = 2^40 B = 1 099 511 627 776 B  ->  ~1.1 x 10^12 interrupts at one per byte
```

| # | Slide text | What it changes |
|---|---|---|
| 1 | "Used for **high-speed I/O devices** … close to memory speeds" | DMA is for devices where the CPU would be the bottleneck |
| 2 | "**OS sets up the memory blocks, counters**, etc." | the CPU does setup, once |
| 3 | "Device controller transfers data blocks from buffer to main memory **without CPU intervention**" | the controller becomes a bus master |
| 4 | **"Only one interrupt is generated per block, rather than one interrupt per byte"** | the whole point |

The improvement factor is exactly the block size (derived; the slide gives the rule):

```
per byte    : 2^40 interrupts
per 4 KB    : 2^40 / 2^12 = 2^28 = 268 435 456     -> 4096x fewer
per 64 KB   : 2^40 / 2^16 = 2^24 =  16 777 216
```

| | Interrupt-driven I/O | DMA |
|---|---|---|
| Who moves data | the CPU | the **controller** |
| Interrupts | one per **byte** (worst case) | one per **block** |
| Data lands in | the device buffer (S28 notes) | **main memory** (S28 notes) |
| Cost | save/restore per byte | setup once; competes for bus cycles |
| Suits | slow character devices | high-speed block devices |

### 4.6 How a modern computer works (S28)

No body text; the notes are the content: *"three parties: **CPU, memory, and device** … a job
execution **fetches instructions from the memory**, and **read/write data** from/to it. After the CPU
issues an I/O request … the device will **notify the CPU** when the data is ready. Depending on
whether interrupt driven I/O or DMA is used, **the data buffer location is different**: if DMA is
used, the data is stored in the **memory**; otherwise the CPU can get the data directly from the
**device buffer**."*

---

## 5. Storage hierarchy and caching (S29, S30) — *not examinable*

**Both slides print "This slide is not examinable."** Do not revise them; keep only the vocabulary.

| Slide | Content |
|---|---|
| **S29** | "CPU registers, CPU caches, main memory, hard disk …"; organisation based on "**speed, cost, volatility, size**"; "**Caching**: copying information into faster storage system; main memory can be viewed as the **last cache before secondary storage**" |
| **S30** | the diagram only. Notes: "From top down … registers, cache, memory, disk, tapes … the **cost decreases**, the **speed also decreases**, the **size increases**. The levels **above main memory** (including main memory itself) are **volatile**; the layer **below** is **non-volatile**." |

```
registers   fastest  smallest  dearest/byte  volatile
cache
main memory                                   <- volatility boundary
disk        slowest  largest   cheapest/byte non-volatile
tape
```

Three carry-overs: **volatility changes at the memory/disk boundary** (why files have long-term
existence, `c11`); **caching = a copy in a faster level** (`c12` separates a *buffer* — data in
transit — from a *cache* — a copy kept for reuse, using this definition); and the hierarchy is the
premise of virtual memory (`c9`).

> If a question mentions it, one sentence suffices: *"cost per byte falls and capacity rises going
> down, speed falls too, and everything above main memory is volatile."* Then answer the real
> question.

---

## 6. Hardware protection (S31–S38)

### 6.1 Why it exists (S31)

> "OS must control and coordinate the access to hardware. However … a **malfunctioning program may
> issue illegal I/O instructions, accessing memory locations of the operating system**. The operating
> system should provide protections **in hardware**."

| Phrase | Why it matters |
|---|---|
| "a **malfunctioning** program" | a bug is enough; malice is not required |
| "illegal **I/O** instructions" | §6.4 |
| "memory locations of **the operating system**" | §6.5 |
| protection **in hardware** | **software cannot police itself** — a subroutine check can be skipped |

The thesis: **the enforcer must be the CPU, not the kernel.**

```
Hardware Protection
    Dual-Mode Operation   S32, S33   <- the primitive
    I/O Protection        S35        <- dual mode applied to instructions
    Memory Protection     S36-S38    <- dual mode applied to addresses
```

### 6.2 Dual-mode operation (S32, S33)

| Mode | Slide text | Runs |
|---|---|---|
| **User mode** | "Execution of **user processes**" | your program |
| **Monitor mode** | "**supervisor mode** or **system mode** or **kernel mode**: execution of **operating system processes**" | the kernel, including interrupt handling |

Four names for one thing — *monitor, supervisor, system, kernel* — used interchangeably. The notes
add that "**interrupt handling is an example of operating system process**", which is why the
hardware switches mode on an interrupt.

| Mode | Mode bit |
|---|---|
| **monitor / kernel** | **0** |
| **user** | **1** |

**Memorise the polarity: 0 = monitor, 1 = user.**

```
                 interrupt or trap  (hardware switches it, S33)
    +----------+ -------------------> +----------+
    |   user   |                      | monitor  |
    |  mode=1  | <------------------- |  mode=0  |
    +----------+  privileged return-  +----------+
                 from-interrupt
```

| Clause (S33) | Consequence |
|---|---|
| "Mode bit **added to computer hardware**" | the bit is hardware, so user code cannot lie about it |
| "When an interrupt or trap occurs **hardware switches to monitor mode**" | the transition *in* is not an OS decision ("controlled by hardware and not OS") |
| "**Privileged instructions** can be used only in monitor mode" | the CPU itself refuses — the enforcement primitive |

**Why the switch must be hardware-controlled:** if the OS decided when to enter monitor mode, it
would have to run code — in user mode — to make that decision, and a misbehaving program could
simply not call it. That hardware transition is the only non-bypassable door into the kernel.

**Why privileged instructions are needed:** they are the short list of operations that change the
machine's *configuration* rather than its *data* — set the mode bit, load base/limit (§6.5), do I/O
(§6.4), disable interrupts, halt.

### 6.3 Kernel mode vs root/admin (S34)

| Question on the slide | Answer |
|---|---|
| "Are they the same?" | **"No, they are not the same"** |
| What is kernel/user mode? | "a **hardware** operation mode" |
| What is root/Administrator? | "a **user account** in an OS" |
| Does root run in kernel mode? | "Jobs still execute in **user mode**, even when executed by a root/admin user" |
| Can root reach kernel mode? | "**indirectly** → e.g., by **loading a kernel module**" |

| | Kernel mode | Root |
|---|---|---|
| Kind of thing | a mode of the **CPU** | an **account** |
| Granted by | the hardware (mode bit) | the OS (authentication) |
| Who "is in" it | a **process**, transiently | a **user**, until logout |
| Gets you there | interrupt, trap, system call | `su` / `sudo`, login |
| Bypasses protection? | it *is* the protection | **no** — root's instructions still run in user mode |

One line: **root is about *who* you are; kernel mode is about *where the CPU is*.**

### 6.4 I/O protection (S35)

| Clause | Meaning |
|---|---|
| "A user program may issue **illegal I/O**; hence I/O must be protected" | the threat |
| "**Case 1:** read a file that does not exist" | legal in form, illegal in content |
| "**Case 2:** unauthorised access to a device" | illegal per se |
| "**All I/O instructions are privileged instructions**" | the mechanism |
| "All I/O operations must **go through the OS** to ensure its correctness and legality" | the policy |
| "CPU generates a **trap** for I/O operations that try to bypass the OS" | the penalty |

Case 1 is the interesting one: a nonexistent file is not a hardware error at all. Only the OS holds
the metadata that can answer "does this exist?", so I/O must be *mediated*, not merely restricted.

The notes give the mode timeline: normal computation in **user mode** → I/O request → the process
waits → the **ISR runs in monitor mode** ("that is the OS code") → resume in **user mode**.

### 6.5 Memory protection (S36–S38)

**The requirement (S36):** "Must provide memory protection, **at least for the interrupt vector and
the interrupt service routines**." The "at least" matters: if a user program can write the vector it
can redirect every interrupt to itself and the machine is owned. The notes generalise it to
"protect the memory space of a process from being modified by other processes".

| Register | Slide definition |
|---|---|
| **Base register** | "Holds the **first legal physical memory address**" — the start |
| **Limit register** | "Contains the **size of the legal range**" — the **length, not the end address** |

```
        base                        base + limit
          |<---------- limit ---------->|
   -------+=============================+-------->  physical addresses
          ^ legal                       ^ illegal from here

   legal  <=>  base <= address < base + limit
```

Two traps in one line: **limit is a size** (not an end address, so the range is `limit` bytes wide),
and the **upper bound is exclusive** (`address == base + limit` is already outside).

**The worked example (S37).** The figure shows a multiprogrammed layout with job 2 in the middle
("Btw, is it a simple batch system? No. it is multiprogrammed system."), and the notes read the
registers off it:

```
base  = 300 040
limit = 120 900
base + limit = 300 040 + 120 900 = 420 940
legal range  = [300 040 , 420 940)     i.e. bytes 300 040 .. 420 939
```

| Address | `>= base`? | `< base+limit`? | Verdict |
|---|---|---|---|
| 300 039 | no | — | **trap** |
| 300 040 | yes | yes | legal — **first** legal byte |
| 420 939 | yes | yes | legal — **last** legal byte |
| 420 940 | yes | **no** | **trap** |
| 0 | no | — | **trap** |

**The check (S38):**

| Clause | Meaning |
|---|---|
| "The **load instructions** for the base and limit registers are **privileged**" | otherwise a process widens its own window |
| "CPU issues a **trap** to the OS if above checks fail" | the fault path |
| "e.g., **Load/Store (address)**" | the check is on every memory reference |

```
   Load/Store(address)               <- every access
        addr >= base ?        -- no --> TRAP
        addr <  base + limit ? -- no --> TRAP
        otherwise: issue the access
```

The notes name the visible consequence: *"This addressing error is a **segmentation fault** in
Linux."* And note that base/limit is **contiguous** protection — one interval only. Once memory is
scattered (paging, `c8`), the check must become per-page.

### 6.6 Privilege, in one table

| Operation | Privileged? | Because |
|---|---|---|
| ordinary instruction | no | — |
| **I/O instruction** | **yes** | must be mediated and validated (S35) |
| **load base / limit** | **yes** | otherwise the window is self-service (S38) |
| **change the mode bit** | **yes** | otherwise user code enters monitor mode (S33) |
| return from interrupt | **yes** | it restores the mode bit (S33) |
| handle an interrupt | (runs in monitor mode) | the ISR is OS code (S32) |

---

## 7. Operating system services (S40)

S40 is a section-opening figure. The notes describe it: *"multiple layers: **user interfaces, system
calls, and services**. To allow users to access the operating system services, a set of **API** is
offered. Those APIs are called **system calls**. The services include **program execution, file
system** etc."*

```
+-------------------------------------------------------+
|  user interfaces     (GUI / command line / batch)     |
+-------------------------------------------------------+
|  system calls / API                                   |  <- the only legal door in
+-------------------------------------------------------+
|  services: program execution, file system, ...        |
+-------------------------------------------------------+
```

The notes' own advice — *"if you are puzzled about some terms, don't worry, we will introduce them
in later lectures"* — says plainly that S40 is a map. The one sentence to keep: **the user interface
is built on system calls, and system calls are built on services.**

---

## 8. System calls, and the trap/interrupt pair (S41–S44)

### 8.1 What a system call is (S41)

| Clause | Meaning |
|---|---|
| "provide the **interface between a user program and the operating system**" | the narrow waist of the system |
| "Generally available as **assembly-language instructions**" | historically a dedicated instruction |
| "possible to replace assembly language … to allow system calls to be made directly (e.g., in **C/C++**)" | the library wrapper |
| **"requires the switch from the user to the kernel mode"** | the defining cost |

That last line is why a system call is expensive: the mode switch *is* a context switch (S25), paid
before any work is done.

### 8.2 API → system call → OS (S42)

```c
#include <stdio.h>
main()
{
    FILE *fp;
    ...
    fp = fopen(...);        /* API: standard C library */
    ...
}

FILE *fopen(...)            /* API: standard C library */
{
    Int fd;                 /* (sic) */
    ...
    fd = open(...);         /* system call */
    ...
}
```

```
   your program  --fopen()-->  libc  --open()-->  | mode switch |  -> kernel
                   API, user mode    system call
```

| Layer | Written by | Runs in | Replaceable? |
|---|---|---|---|
| **API** (`fopen`) | library author | user mode | yes — that is why Windows and Unix can both offer C streams |
| **System call** (`open`) | kernel author | kernel mode | no — it *is* the contract |

Why the switch: *"**All the I/O instructions are privileged instructions, and they must be executed
in the kernel mode.** Then … execute the open() system call. When it is done, we need to get back to
user mode"* (notes). Why an API layer exists at all: **portability and convenience** — `fopen` gives
a portable, buffered, checked interface over a minimal primitive.

### 8.3 System call processing (S43) — CPU to device

```
  user code |  ❶ program's code executing
            |  ❷ invoke system call   --- TRAP! --->
  OS code   |  ❸ execute system call
  user code |  ❹ continue executing program's code
```

| Step | Mode | What happens |
|---|---|---|
| ❶ | user | the program runs normally |
| ❷ | user → **kernel** | the trap instruction switches the mode |
| ❸ | **kernel** | the privileged work is done |
| ❹ | kernel → user | the program resumes after the trap |

### 8.4 Interrupt processing (S44) — device to CPU

```
  user code |  ❶ program's code executing
            |        <--- INTERRUPT! ---
  OS code   |  ❷ process the interrupt
  user code |  ❸ continue executing program's code
```

### 8.5 The pair — the highest-value table in the chapter

| | **System call** (S43) | **Interrupt** (S44) |
|---|---|---|
| Direction | **CPU → device** (the program asks) | **device → CPU** (the device reports) |
| Origin | the running program | the hardware |
| Is it a trap? | **yes** — S43 labels it `Trap!` | no — traps are CPU-generated (S24) |
| Timing | **synchronous** | **asynchronous** |
| Mode switch caused by | the trap instruction | the interrupt line |
| Example | `open()`, `read()`, `write()` | disk transfer complete, key pressed |

One sentence: **both mean "something needs the kernel now" — a trap is the program asking, an
interrupt is the hardware telling.**

---

## 9. Readings and the future (S45, S46)

| Slide | Content |
|---|---|
| **S45** | Readings: Apple iOS, Google Android (Wikipedia); *"History of Operating Systems", by Ayman Moumina* (PDF in NTULearn) |
| **S46** | "Operating systems are **not** limited to Windows/Linux/MacOS"; "development **never stops**" — **changes in hardware**, **changes in user requirements**; examples: **Unikernel**, **formally verified OS kernel** (seL4) |

| Example | What it is | Why it exists |
|---|---|---|
| **Unikernel** | one application linked with only the OS code it needs, on a hypervisor — no user/kernel split | removes the mode switches of §8 and the generality it does not need ⇒ smaller, faster |
| **seL4** | a microkernel with a **machine-checked proof** of correctness | for systems where a bug is a catastrophe — the "**reliable** computing core" of S15 |

---

## 10. Putting it all together

One program run, touching every act of the deck:

```
 1. the user double-clicks an icon                       user interface (S40)
 2. the OS creates a process and places it in memory     memory management (S12)
 3. the program calls fopen("notes.txt")                 API (S42)
 4. libc executes open()                                 system call (S41)
       TRAP -> hardware switches 1 -> 0                  mode bit (S33, S43)
 5. the kernel checks the path and permissions           I/O protection (S35)
 6. the kernel programs the controller and returns       back to user mode (S43 step 4)
 7. the process keeps computing while the disk works     interrupt-driven I/O, multiplexed CPU (S26)
 8. the controller DMAs the block into memory            one interrupt per block (S27)
 9. the controller raises an interrupt                   (S24)
       hardware switches 1 -> 0                          (S44)
10. the ISR saves state, reads the type, dispatches      context switch (S25)
11. the process resumes                                  (S44 step 3)
```

Every line is one slide. That is the point: **this chapter is the map of the rest of the course.**

---

## 11. Definitions and numbers worth memorising

```
OS            = the program between the user and the hardware            (S03)
2 goals       = user convenience + efficient hardware utilisation       (S03)
3 definitions = resource allocator, control program, kernel             (S06)
4 components  = hardware, OS, application programs, users               (S05)
3 features for multiprogramming = memory mgmt, CPU sched, I/O sched     (S12)
3 MP advantages = throughput, economy, reliability                      (S19)
3 protection mechanisms = dual mode, I/O protection, memory protection  (S31)
3 interrupt-handling steps = save state, identify type, dispatch ISR    (S25)
```

```
mode bit = 0  ->  monitor / supervisor / system / kernel mode
mode bit = 1  ->  user mode
entering monitor mode is done by the HARDWARE on a trap or interrupt   (S33)
privileged instructions execute ONLY in monitor mode                   (S33)
```

```
legal  <=>  base <= address < base + limit                    (S36, S38)
limit = SIZE of the range, not the last address
example (S37): base 300 040, limit 120 900
               legal = [300 040 , 420 940)     300 040 + 120 900 = 420 940
failure -> trap to the OS -> (Linux) segmentation fault
```

```
interrupt vector = array of ISR addresses, indexed by type      (S24)
trap             = CPU-generated interrupt (software error/request)  (S24)
one interrupt per byte  ->  N bytes => N interrupts
one interrupt per block ->  N bytes => N / block_size interrupts     (S27)

1 TB = 2^40 B = 1 099 511 627 776 B
   per byte    : 2^40  ~= 1.1 x 10^12 interrupts
   per 4 KB    : 2^28  =    268 435 456 interrupts   (4096x fewer)
```

```
cyber-physical / embedded            (S15)
   +-- real-time   deadline, e.g. airbag control   (S16)
   +-- handheld    iOS / Android / HarmonyOS       (S17)
tightly coupled   = multiprocessor, shared memory  (S19)
loosely coupled   = distributed systems            (S19 notes)
multi-PROGRAMMING = many programs in memory, 1 CPU  (S11, S19 notes)
multi-PROCESSING  = many CPUs / cores               (S19, S19 notes)
```

---

## 12. Practice problems

**P1.** A job needs 20 ms of CPU then 80 ms of I/O, once, and exits. (a) CPU utilisation under
simple batch with one resident job? (b) With five such jobs resident under multiprogramming,
assuming instant switching?

**P2.** For each of S12's three features, name the shared resource and the decision.

**P3.** Classify as multi-programming, multi-processing, both, or neither: (a) a single-core laptop
with a browser and an editor open; (b) a quad-core phone running one game; (c) two computers running
a distributed database; (d) a dual-core PC with ten processes.

**P4.** Base 300 040, limit 120 900. Legal or trap: 300 039, 300 040, 420 939, 420 940, 0? How wide
is the legal region, and how wide if you wrongly treat the limit as an end address?

**P5.** A process gets base 8192, limit 4096. (a) Last legal address? (b) The program computes a
pointer to 12 288 — what happens, and what is it called on Linux? (c) Why can the program not just
load 0 into the limit register?

**P6.** A device transfers 512 MB. Compare interrupt counts for one interrupt per byte vs one per
4 KB block, and give the ratio.

**P7.** Trap or interrupt, and synchronous or asynchronous: (a) `read()` is called; (b) the disk
finishes; (c) division by zero; (d) an invalid address is dereferenced; (e) a keyboard scancode.

**P8.** Give the five steps from "the device finishes" to "the interrupted program resumes", and say
which is the context switch.

**P9.** Mode bit value, and what causes the transition: (a) executing `printf`; (b) calling `open()`;
(c) running the disk ISR; (d) the ISR returning.

**P10.** A root user runs `rm -rf /`. Does that command execute in kernel mode? Justify in one
sentence and name the one legitimate way root gets code into kernel mode.

**P11.** Explain with S10, S11 and S12 why simple batch is called "not very efficient" even though
its CPU is fully used whenever the single job computes.

### Solutions

**S1.** (a) `20 / (20 + 80) = 20 %`. (b) Each job needs the CPU 20% of its life; five resident jobs
guarantee a runnable job, so `5 × 20 % = 100 %`. The real condition is *jobs resident × per-job CPU
fraction ≥ 1* — four jobs would already give 80%. (Derived from "CPU idles"; not printed.)

**S2.**

| Feature | Resource | Decision |
|---|---|---|
| Memory management | **memory** | which region a new job gets; how to reclaim it |
| CPU scheduling | **the CPU** | which ready job runs next, and for how long |
| I/O device scheduling | **devices** | which job gets the device, and in what order |

**S3.** (a) **multi-programming** (one core). (b) **multi-processing** — and multi-programming too,
since the OS runs other processes. (c) **neither** in the S19 sense: loosely coupled, a distributed
system. (d) **both**.

**S4.**

| Address | Verdict |
|---|---|
| 300 039 | **trap** (< base) |
| 300 040 | **legal** (first) |
| 420 939 | **legal** (last) |
| 420 940 | **trap** (= base+limit, exclusive) |
| 0 | **trap** |

The region is **120 900 bytes** (the limit). Treating 120 900 as an end address would give the range
`300 040 … 120 900`, which is empty — the fastest way to see that "limit" is a size.

**S5.** (a) `8192 + 4096 − 1 = 12 287`. (b) 12 288 fails the upper-bound test, the CPU traps, and
Linux reports a **segmentation fault**. (c) Loading the base/limit registers are **privileged
instructions** (S38): the attempt traps and is treated as a protection violation.

**S6.** `512 MB = 2^29 B`. Per byte: `2^29 = 536 870 912` interrupts. Per 4 KB:
`2^29 / 2^12 = 2^17 = 131 072`. Ratio `2^12 = 4096×` — exactly the block size, which is S27's
fourth bullet.

**S7.**

| | Type | Timing |
|---|---|---|
| (a) `read()` | **trap** (S43 calls it so) | **synchronous** |
| (b) disk finishes | **interrupt** | **asynchronous** |
| (c) divide by zero | **trap** ("software error", S24) | **synchronous** |
| (d) invalid address | **trap** (S38) | **synchronous** |
| (e) keyboard | **interrupt** | **asynchronous** |

**S8.** `1` save registers and PC → `2` determine the interrupt type → `3` fetch the ISR address from
the vector table → `4` run the ISR → `5` restore and resume. **Step 1** is the context switch (S25
names it there; the notes apply the word to the whole save/resume pair).

**S9.**

| State | Mode bit | Caused by |
|---|---|---|
| (a) `printf` | **1** | — |
| (b) `open()` | 1 → **0** | the **trap** instruction, executed by hardware (S33, S43) |
| (c) ISR | **0** | — |
| (d) return | 0 → **1** | the privileged return-from-interrupt |

The asymmetry is the answer: entering the kernel cannot be an ordinary instruction (§6.2), but
leaving it must be privileged.

**S10.** **No.** `rm` is an ordinary user program; root changes its *permissions*, not the CPU's
*mode*. Each `unlink()` is a system call that traps in, and the kernel's checks then succeed because
the user is root. The one legitimate route into kernel mode is **loading a kernel module** (S34).

**S11.** Because "efficiency" here means **utilisation of the machine**, not speed of the job. Batch
uses 100% of the CPU *while computing*, but with one resident job the CPU has nothing to do during
that job's 80 ms of I/O — 20% utilisation in S1's example. S11 keeps several jobs in memory so there
is always something runnable, and S12 lists the three mechanisms that make that possible. So "not
efficient" is a statement about **idleness caused by lack of concurrency**.

---

## 13. Self-test questions

1. State S03's definition and the two goals inside it. Why can they contradict?
2. What does "smart allocation may require lot of information about user programs" imply about the
   cost of a good policy?
3. Name the four components of a computer system and one responsibility of each.
4. Give S06's three definitions. Which says the kernel is "always ready to accept new commands"?
5. Distinguish **kernel**, **kernel mode** and **root**. Which is a hardware concept?
6. What is simple batch's central problem, and what is the fix in each of the next two types?
7. What is **automatic job sequencing**, and what is it the ancestor of?
8. List the three features multiprogramming needs, with the resource each manages.
9. Give S13's one sentence that distinguishes time-sharing from plain multiprogramming.
10. Why does a desktop OS prioritise responsiveness, and what does it cost?
11. Define a cyber-physical system in the slide's words; name three domains.
12. What makes a system real-time — speed or something else? Give the slide's example.
13. How do real-time and handheld systems relate to embedded/cyber-physical systems?
14. Name the three handheld issues and what the OS does about the third.
15. Distinguish multi-programming from multi-processing in one line each.
16. Give the three advantages of multiprocessors and the mechanism behind each.
17. Tightly coupled vs loosely coupled?
18. Give S23's five facts of computer-system operation in order.
19. Why is the interrupt vector needed, and what does it contain?
20. Why are incoming interrupts disabled while one is processed?
21. Define a trap and give two causes.
22. What must an OS do if it is not interrupt driven?
23. List the three interrupt-handling steps; which needs the vector?
24. In S26, what is the CPU doing during the transfer, and why may it?
25. What problem does DMA solve, and how large is the improvement?
26. Where does data land under interrupt-driven I/O, and where under DMA?
27. Which two slides are "not examinable", and what do they cover?
28. Define caching in the slide's words; why is main memory the last cache?
29. Give the four names for the privileged mode.
30. Which bit value means monitor mode, and what switches the bit on an interrupt?
31. Why must the mode switch itself be hardware-controlled?
32. Can root run code in kernel mode? Name the indirect route.
33. Why must *all* I/O go through the OS? Use S35's "file does not exist" case.
34. Define base and limit. Which is a size?
35. With base 300 040 and limit 120 900, give the legal interval and test 420 940.
36. Why are the base/limit loads privileged, and what does a failed check produce?
37. Name the three layers of the OS-services figure, and say which is the API.
38. What must happen, in mode terms, for a system call to execute?
39. Trace `fopen` → `open` → kernel, naming each layer.
40. Give the four system-call steps and the three interrupt steps. What single label distinguishes
    them on the diagrams?

---

## 14. Glossary

| Term | Meaning |
|---|---|
| **Operating system** | the program acting as intermediary between the user and the hardware (S03) |
| **Kernel** | the one core program always ready to accept new commands; all else is application programs (S06) |
| **Resource allocator / control program** | the OS seen as manager of resources / as supervisor of execution (S06) |
| **Abstraction / mechanism / policy** | what is seen / how it is done / which alternative is chosen (S02) |
| **Batch system** | one job in memory at a time, jobs grouped to amortise setup (S10) |
| **Automatic job sequencing** | automatic transfer of control from one job to the next (S10) |
| **Multiprogramming** | several jobs resident so the CPU is never idle while one waits for I/O (S11) |
| **Time-sharing** | multiprogramming plus on-line interaction: the OS returns for the next command (S13) |
| **Swapping** | moving a job between memory and disk (S11, S13) |
| **Throughput** | work completed per unit time (S19) |
| **Tightly / loosely coupled** | shared-memory multiprocessor / distributed computers (S19) |
| **Multi-processing** | the system runs on multiple CPUs or cores (S19 notes) |
| **Cyber-physical system** | physical system monitored and controlled by a reliable computing and communication core (S15) |
| **Real-time system** | system with well-defined fixed-time constraints; jobs must meet deadlines (S16) |
| **Device controller** | hardware for one device type; has a local buffer; moves data to/from memory (S23) |
| **Interrupt** | signal that a device has finished, transferring control to an ISR (S23, S24) |
| **Trap** | a CPU-generated interrupt caused by a software error or request (S24) |
| **Interrupt vector** | table of the addresses of all interrupt service routines (S24) |
| **ISR** | interrupt service routine: the handler for one interrupt type (S24, S25) |
| **Context switch** | saving registers and the program counter so execution can resume (S25) |
| **Polling** | repeatedly checking for completion instead of being interrupted (S24) |
| **DMA** | direct memory access; the controller moves blocks with one interrupt per block (S27) |
| **Dual-mode operation** | hardware distinction between user mode and monitor/kernel mode (S32) |
| **Mode bit** | hardware bit: **0 = monitor, 1 = user** (S33) |
| **Privileged instruction** | instruction that executes only in monitor mode (S33) |
| **Base register** | holds the first legal physical address (S36) |
| **Limit register** | holds the **size** of the legal range (S36) |
| **Segmentation fault** | Linux's name for the addressing error the base/limit check reports (S38) |
| **System call** | interface between a user program and the OS; requires a switch to kernel mode (S41) |
| **API** | library interface wrapping system calls, e.g. `fopen` around `open` (S42) |
| **Unikernel / seL4** | one application plus a minimal kernel / a formally verified kernel (S46) |
