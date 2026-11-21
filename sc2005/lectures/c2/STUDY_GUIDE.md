# SC2005 — Processes & Threads: Study Guide

Companion to the deck `Part2 (Process and Threads).pptx` (40 slides) in this folder. There is no
audio for this deck, so citations are **slide numbers**: **`S17`** means slide 17 of this deck.
`[NOTES]` in the transcript are the lecturer's speaker notes and are quoted as content.
Verbatim text: [transcripts/01-processes-and-threads-slides.md](transcripts/01-processes-and-threads-slides.md).

---

## 0. The chapter in one picture

The whole deck answers four questions, in this order:

```
   1. WHAT is the unit of work?            -> a process: program in execution, own address space
   2. HOW does the OS manage many of them? -> states + PCB + queues + schedulers + fork/exit
   3. HOW do they cooperate?               -> IPC: message passing or shared memory
                                                    |
                                                    v
   4. WHAT if one address space needs      -> threads: many units of CPU utilisation
      several units of execution?            inside one process, mapped to kernel threads
```

```
 Part 2: Processes and Threads
 |
 +-- Process Concept .......................... S03 - S09
 |     process vs program, memory layout, states, PCB, kernel/user space
 |
 +-- Process Scheduling ....................... S10 - S16
 |     context switch, queues, long/short/medium-term schedulers
 |     (algorithms themselves: NOT here -> ../c3)
 |
 +-- Operation on Processes ................... S17 - S21
 |     creation (fork, tree), execution orders, termination (exit/abort)
 |
 +-- Interprocess Communication ............... S21 - S28
 |     cooperating processes, two IPC models, message passing, producer-consumer
 |     (mutual exclusion: NOT here -> ../c5)
 |
 +-- Threads .................................. S29 - S40
       thread anatomy, benefits, multithreaded server, user vs kernel threads,
       many-to-one / one-to-one / many-to-many
```

Sections §1–§6 of this guide follow that outline one-for-one, in slide order.

S10, S17, S21 and S28 are **section dividers** repeating the same five-line outline — bookmarks, no
new content. S02 is the outline *plus* the review of the previous lecture, which §1.2 uses.

---

## 1. Where Part 2 sits (S01–S02)

### 1.1 The course overview table (S01)

The first slide is a map of the whole module:

```
                       Operating Systems
                        /      |       \
              OS goals   CPU mgmt   Memory mgmt   Filesystem mgmt
                          |            |               |
                   Processes (L2)   Memory org (L8)  Filesystems (L11)
                   Scheduling (L3)  Virtual mem (L9-10)
                   Synchronization (L5-6)
                   Deadlocks (L7)
                   I/O & disk (L12)
                   Special: Real-time OS & virtualization
```

Two things to notice:

1. **Threads are not on this slide.** They belong to this deck (S29–S40) but the overview gives no
   lecture number for them. Counting the labels — L1 introduction, L2 processes, L3 scheduling,
   L5–6 synchronization — leaves **L4** for threads. That is an inference from the gap, not a
   quotation; the deck never prints "Threads (L4)". If you cite a lecture number for threads, say
   "L4 by elimination".
2. Other decks in the module still print an **older** numbering scheme,
   `Synchronization (L4-5)` and `Deadlocks (L6)`. Since synchronization in *this* deck's scheme is
   L5–6, everything after it shifts by one. Always give the **topic** as well as the number.

### 1.2 The outline of Part 2 (S02) and the review it opens with

S02 lists the five sections you will be examined on:

| # | Section | Slides |
|---|---|---|
| 1 | Process Concept | S03–S09 |
| 2 | Process Scheduling | S10–S16 |
| 3 | Operation on Processes | S17–S21 |
| 4 | Interprocess Communication | S21–S28 |
| 5 | Threads | S29–S40 |

The speaker notes open with a review of the previous lecture, and it is worth knowing what is being
assumed:

* The review assumes **interrupt-driven I/O vs DMA**, and **privileged instructions** as the
  mechanism behind **I/O and memory protection** (the base/limit registers of S04 and S09).
* "From this lecture on, we will start to introduce the system services and components one by one.
  We start with processes and threads." (S02 notes)

That sentence is the reason this part is the base of the rest of the module.

---

## 2. Process concept (S03–S09)

### 2.1 What a process is (S03)

> **Process: a program in execution; process execution must progress in a sequential fashion.** (S03)

Every word in that definition is load-bearing:

* **in execution** — a process exists only while something is running. It is a **dynamic** concept.
* **sequential** — the CPU executes the process's instructions one after another (the deck's
  abstraction; real CPUs pipeline, but the *logical* order is sequential).

The slide contrasts it with the other term the OS uses for the same thing:

| System type | What it executes | Called |
|---|---|---|
| **Batch system** | jobs | a **job** |
| **Time-sharing system** | user programs and commands | a **process** |

> **Textbook uses the terms job and process almost interchangeably (Job = Process).** (S03)

**Program vs process** — the distinction you must be able to state in one sentence:

| | **Program** | **Process** |
|---|---|---|
| Nature | **static** — an executable file on disk | **dynamic** — an execution of that file |
| Exists | before, during and after execution | only while running |
| Contents | instructions and static data | instructions + data + heap + stack + **state** + resources |
| Count | one file | many processes can run the same file |
| Stored in | disk | main memory (plus a PCB in kernel space) |

The notes' illustration: *"If you click the executable (that is the program) mul…"* — clicking the
same executable several times gives several **processes** of the same **program**. One program, many
processes.

The notes' aside that *"a job is a larger concept"* is loose — follow the slide (job = process); the
only useful distinction is historical, batch word vs time-sharing word.

### 2.2 The process in memory (S04)

The slide draws four sections inside a region delimited by the **base** and **limit** registers you
met in memory protection:

```
        Base                                              Base + Limit
          |                                                     |
          v                                                     v
          +----------------------+  <- low addresses
          |        text          |  (code section, program)
          +----------------------+
          |        data          |  (global parameters)
          +----------------------+
          |        heap          |  (all dynamically allocated variables,
          |          |           |   e.g. a = new int[10])
          |          v           |   grows toward the stack (higher addresses)
          +----------------------+
          |          ^           |
          |          |           |
          |        stack         |  (parameters and local variables in a function)
          |                      |   grows toward the heap (lower addresses)
          +----------------------+  <- high addresses
```

| Section | Holds | Lifetime | Grows |
|---|---|---|---|
| **text** | the code | fixed at load time | never |
| **data** | globals, static variables, constants | fixed at load time | never |
| **heap** | everything `malloc`/`new` returns | from allocation to `free`/`delete` | **upward** (toward the stack) |
| **stack** | function parameters, local variables, return addresses | from call to return | **downward** (toward the heap) |

Because heap and stack grow **towards each other**, the failure modes are symmetric:

* **Heap overflow / memory leak** — allocate and never free; the heap collides with the stack (or
  the allocator runs out) and the process is killed.
* **Stack overflow** — typically unbounded recursion; the stack collides with the heap and the
  process is killed (core dump).

The slide closes with a deliberate callback: *"Recall base and limit registers from memory
protection?"* Those two registers are what stop the process from writing outside this picture. The
process may only address `[base, base+limit)`; an address outside traps.

### 2.3 The five states (S05)

> As a process executes, it changes state. (S05)

| State | Definition on the slide | What it is waiting for |
|---|---|---|
| **New** | the process is being created | — (being built) |
| **Ready** | ready to run, but waiting to be assigned to the CPU | **the CPU** (the scheduler) |
| **Running** | instructions are being executed | nothing — it has the CPU |
| **Waiting** | waiting for I/O or an event | **an external event** (I/O completion, signal) |
| **Terminated** | the process has completed | — |

The notes make the one distinction that costs marks:

> "Note, in both ready and waiting, the process is waiting, although for different reasons. It is
> waiting in the **ready** state to be allocated to the CPU by the OS scheduler, whereas it is
> waiting in the **waiting** state for some operation to complete." (S05 notes)

Memory hook: **Ready waits for the CPU; Waiting waits for the world.**

### 2.4 State transitions (S06)

The transition diagram is flagged in the notes as *"This figure is very important."* Here it is with
every edge labelled by its cause:

```
  new --admit--> ready --dispatch--> running --exit--> terminated
                   ^   |                |
                   |   +--timer interrupt (preemption, running -> ready)
                   |                    |
                   +----event done--- waiting <--I/O or event wait--
```

As a table, because exam questions love to ask "which transition is caused by X":

| # | Transition | Cause | Notes |
|---|---|---|---|
| 1 | new → ready | **admitted** | only after initialisation: memory region and other resources allocated (S06 notes) |
| 2 | ready → running | **dispatch** | the scheduler selects it (details are L3, [`../c3`](../c3)) |
| 3 | running → ready | **timer interrupt** | preemption; the process did not ask for this |
| 4 | running → waiting | **I/O or event wait** | the process asked for something it must wait for |
| 5 | waiting → ready | **event completes** | the I/O finishes; the process is *ready*, not running |
| 6 | running → terminated | **exit** | normal completion |

Note what is **not** an edge: ready → waiting (you cannot wait for I/O without first running the
instruction that requests it), waiting → running (must go through ready), terminated → anywhere.

> "Timer interrupt is used in multiprogramming systems to switch between ready processes." (S06)

That sentence is the whole mechanism of preemption: without a timer, a process that never blocks
would keep the CPU forever. The timer forces transition 3, which puts a process back on the ready
queue and lets the scheduler perform transition 2 on somebody else.

### 2.5 The Process Control Block (S07–S08)

The OS cannot keep a process's information in the process's own memory (the process could corrupt
it, and it must survive while the process is not running). So each process gets a kernel data
structure: the **PCB**.

| Field (S08) | Why it is needed |
|---|---|
| **Pointer to other PCBs** | PCBs are maintained in **queues/lists** — the pointers are the links |
| **Process state** | one of the five states of §2.3 |
| **Process number (pid)** | identity; used by IPC, by `wait`, by the user |
| **Program counter** | address of the **next** instruction — this is what "resuming" means |
| **CPU registers** | accumulators, index registers, stack pointer, status word — the live machine state |
| **Process priority** | used in process scheduling (L3) |
| **Memory management information** | e.g. the **base and limit** register values of S04 |
| **Information regarding files** | e.g. the list of open files |

Two structural facts from the notes:

* *"In OS, PCBs of all processes are maintained in a queue structure."* (S08 notes) — a PCB is
  usually literally a node in a linked list; the "pointer to other PCBs" field is the `next`.
* *"Each process has its PCB stored in the main memory"* (S08 notes) — not on disk, not in the
  process's address space: in **kernel space** (see §2.6).

Mechanically, a context switch is *store the live registers into the old PCB, load them out of the
new one*; the PC is what makes resumption land on exactly the right instruction.

### 2.6 PCBs and the memory layout (S09)

Putting §2.2 and §2.5 together:

```
 +--------------------------------------------------+  low addresses
 |            memory area for OS (kernel space)      |
 |   PCB1   PCB2   PCB3   PCB4   ...  queues, tables |
 +--------------------------------------------------+
 |            user space                             |
 |   +------------+  +------------+                  |
 |   | process 1  |  | process 2  |   ...            |
 |   | base..limit|  | base..limit|                  |
 |   +------------+  +------------+                  |
 +--------------------------------------------------+  high addresses
```

Three consequences the notes spell out:

1. **PCBs live in kernel space** — "PCBs are stored in kernel space for protection."
2. **The process image lives in user space**, bounded by its base and limit.
3. **"Changes to PCB must happen in kernel mode."** A process cannot edit its own state; only the
   kernel can. That is why every state change in §2.4 is described as an OS action.

**Worked question (S09 notes).** *"Suppose PCB1 belongs to Process 1. What happens if Process 1
executes the code `a = new int[10]`?"*

Answer in three steps:

1. The allocation is a heap allocation, so the **heap of Process 1 grows by 10 × `sizeof(int)`**
   (40 bytes for a 4-byte `int`) toward the stack, inside `[base, base+limit)`.
2. Growing the heap may need more memory from the OS: that is a **system call** (`brk`/`sbrk`, or the
   language runtime's allocator calling it). A system call switches the CPU to **kernel mode**.
3. If the heap must extend beyond the current limit, the kernel must **update the memory-management
   fields of PCB1** (the limit, possibly the base if the region has to move) before returning.
   Otherwise the process would immediately fault on its own new memory.

That single question ties the whole of §2 together: user space grows, kernel space records, and the
boundary is crossed only in kernel mode.

---

## 3. Process scheduling (S10–S16)

**Scope warning.** This section is about the *machinery* around scheduling — switching, queues, and
which scheduler does what. The **algorithms** (FCFS, SJF, SRTF, priority, round robin, multilevel
feedback) and their metrics are **not in this deck**; they are L3, in [`../c3`](../c3). Do not
expand them here.

### 3.1 Context switch (S11–S12)

S11 is a timeline figure of two processes and the OS in the middle. The notes give the scenario:

> "In a time sharing system, every 100ms, there is a timer interrupt generated, and the running
> process gives up the CPU. Then, another process is picked to run on the CPU." (S11 notes)

So P0 goes running → ready, the OS saves P0, chooses P1 and loads P1, and P1 goes ready →
running — the two-way switch of §2.4.

The definition (S12):

> "When CPU switches to another process, the system must save the context (i.e., information) of the
> old process and load the saved context for the new process."

And the cost:

> "Context switch time is overhead: The system does NO useful work while switching between
> processes." (S12)

What "save the context" means concretely, using the PCB fields of §2.5: the interrupt transfers
control to the kernel, which **saves PC and registers into the old PCB**, updates the old state,
**runs the scheduler** ([`../c3`](../c3)), **reloads the memory-management registers** (base/limit,
page-table base) for the new process, **restores PC and registers from the new PCB**, and returns to
user mode at the restored PC.

**Worked arithmetic.** The timer fires every 100 ms; a switch takes 5 ms.

```
time slice           q = 100 ms
switch cost          s = 5 ms
cycle                q + s = 105 ms
overhead fraction    s / (q+s) = 5/105 = 0.0476  -> 4.8 %
useful fraction      100/105  = 0.952           -> 95.2 %
switches per second  1 / 0.105 = 9.5
```

Two exam-ready conclusions: (a) the overhead is a **fixed tax per quantum**, so a *shorter* quantum
raises the overhead fraction; (b) two processes do **not** each get 50 % of the CPU — they each get
about 47.6 %, and the rest is lost.

Note also that S12 says "switching between processes". Threads switch cheaper (§6) because steps 5
and much of 2–3 are unnecessary when the address space does not change.

### 3.2 The queues (S13–S14)

> **Job queue: Set of all processes with the same state in the system** — ready queue (processes in
> ready state), device queue (processes in waiting state and waiting for a specific I/O device), etc.
> (S13)

* All queues are stored in **main memory, in kernel space** (S13).
* A process **migrates between queues when its state changes** (S13) — exactly the transitions of
  §2.4: ready queue → running on dispatch; running → a device queue on an I/O wait; device queue →
  ready queue on I/O completion; running → ready queue on preemption; and out of all queues (PCB
  freed) on exit.

* There is **one device queue per device**. The notes give the operational reading: *"We can judge
  whether a device is busy or not from the length of the device queue. For example, mag unit 0 is
  idle, and disk unit 0 is relatively busy, with three processes waiting for I/O."* (S14 notes)
  An **empty** device queue means an **idle** device.
* Queue implementation (S14 notes): each queue has a **header** with a **head pointer** (first PCB)
  and a **tail pointer** (last PCB). Insertion at the tail, removal from the head — FIFO.
* Convention (S14 notes): *"We usually store the PCB of the running process as the first element of
  the ready queue."* A running process is therefore *conceptually* still the head of the ready
  queue; it has simply been chosen.

S13's definition of "job queue" is the one place in the deck where the terminology is loose — the
standard usage is that the *job queue* is the set of **all** processes in the system, including
those on disk, while a per-state list is just "a queue". See [NOTES.md](NOTES.md#3-known-slips-in-the-slides).

### 3.3 The three schedulers (S15)

> "We need multiple schedulers for different purposes." (S15)

| Scheduler | Other name | Selects | From → to | Invoked |
|---|---|---|---|---|
| **Long-term** | **job** scheduler | processes to admit | **disk → main memory** | infrequently — **seconds to minutes** (S16) |
| **Short-term** | **CPU** scheduler | which ready process runs next | **ready → running** | **frequently, ~100 ms** (S16) |
| **Medium-term** | (swapper) | a *partially executed* process to remove | **memory → disk, and back** | when load is heavy / light (S15) |

The medium-term scheduler is described by the situation, not by a rate:

> "When the system load is **heavy**, swaps out a partially executed process from memory to hard
> disk. When the system load is **light**, such processes can be swapped back into main memory."
> (S15)

Two design points from the notes:

* The **short-term** scheduler *"must be fast in making decision"* because it is invoked constantly
  (S16 notes). Any time it wastes is time the CPU is idle.
* The **long-term** scheduler can afford *"very advanced prediction on the memory usage"* because it
  runs rarely (S16 notes) — it can look at the whole job and decide whether admitting it is wise.

Why swap at all? See §3.4 — swapping is what the medium-term scheduler uses to change how many
processes are in memory, and memory is the scarce resource this whole module is about.

### 3.4 Degree of multiprogramming (S16)

> "Degree of multiprogramming is the number of processes in the main memory that can be supported by
> a multiprogrammed system." (S16 notes)

The division of labour between the two admission schedulers is the examinable sentence:

> "The degree of multiprogramming is **initially** controlled by the **long-term** scheduler, and
> **thereafter** by the **medium-term** scheduler." (S16)

```
   too few processes        good                 too many processes
   CPU idles    <---  degree of multiprogramming  --->  thrashing
        ^                     ^                            ^
        |                     |                            |
   long-term admits      (target)              medium-term swaps out
   from disk                                   (and back when light)
```

Why too many is bad: the notes' framing on S15 — *"each process needs some main memory and other
resources. Thus, a machine can only support a limited number"* — is the same argument that later
becomes thrashing in [`../c9`](../c9).

### 3.5 What this section deliberately omits

| Not on the slides | Where it is |
|---|---|
| FCFS / SJF / SRTF / priority / round robin / multilevel queues | [`../c3`](../c3) |
| Dispatch latency, CPU utilisation, turnaround, waiting time, response time | [`../c3`](../c3) |
| Dispatcher as a named component | [`../c3`](../c3) |
| Page-fault-driven swap decisions | [`../c9`](../c9) |

---

## 4. Operations on processes (S17–S21)

### 4.1 Process creation and the process tree (S18)

> "Parent process creates children processes, which, in turn create other processes, forming a tree
> of processes (**fork**)." (S18)

The slide's figure for a login session:

```
                        root process
        +-------------+------+------+-----------+
        |             |             |           |
     console1      console2       swap        flush
        |             |
      unzip         search
```

Reading the figure:

* **Root process** — the ancestor of everything (historically `init`/`systemd`); the notes say
  *"all the processes are the children of a root process."*
* **console1, console2** — one child per terminal/console the user opens.
* **Background processes created for the system itself** — the notes name two:
  * **`swap`** — *"used in the mid-term scheduler"*, i.e. the process/mechanism that performs the
    swapping of §3.3.
  * **`flush`** — *"for writing dirty pages"* back to disk (the write-back daemon).
* **unzip, search** — user commands run inside a console; each is a child of its console.

Count for this figure: **7 processes** (root, 4 children, 2 grandchildren), **6 fork edges**,
**4 leaves** (unzip, search, swap, flush), **depth 3**.

Why a *tree* matters: it defines who may terminate whom (§4.3), it defines inheritance of resources
(open files), and it is what makes *cascaded* termination necessary.

**Scope note.** The slide's parenthetical *"("fork")"* names the mechanism but the deck does not
teach the `fork()` API — no return values, no copy-on-write, no `exec`. Treat `fork` here as "the
system call that creates a child", and see [NOTES.md](NOTES.md) for the boundary.

### 4.2 Execution orders after creation (S19)

> "Two possible execution orders: parent and children execute **concurrently** (and independently);
> parent **waits** until all children terminate (`wait()`, `join()`)." (S19)

| Order | Parent behaviour | Parent's state | Typical use |
|---|---|---|---|
| **Concurrent** | keeps executing alongside the child | stays running/ready | a shell launching a background job; browser tab processes |
| **Parent waits** | calls `wait()` / `join()` | **running → waiting**, then **waiting → ready** when the child finishes | a shell running a foreground command; a build tool waiting for a compiler |

The notes connect `wait` to the state diagram of §2.4:

> "Remember in the process state transition, we have one event wait, causing a process transiting
> from running to waiting. The parent calls a system call `wait`, and its process state becomes
> waiting. Its state will change to ready when the child process finishes execution." (S19 notes)

The notes add the lab mapping: *"In Nachos, the API is `join`."* So `wait()` (Unix) and `join()`
(Nachos, and by analogy `pthread_join` for threads) are the same idea: **block until the other party
finishes**.

Examples on the slide:

* **Web browsers** — "many web browsers nowadays fork a new process when we access a new page in a
  'tab'". One process per tab gives **isolation**: a crashed renderer takes down one tab, not the
  browser.
* **Background processes** — "OS may create background processes for monitoring and maintenance
  tasks" (the `swap`/`flush` children of S18).

### 4.3 Process termination (S20)

> "Two possible ways to terminate a process." (S20)

| Way | Who initiates | What happens |
|---|---|---|
| **Exit** | the process itself, after its last statement | it asks the OS to delete it; **a child may output return data to its parent**; **the OS de-allocates its resources** |
| **Abort** | the **parent**, at any time | the child is killed before finishing |

Reasons a parent aborts a child (all four on the slide):

1. the child has **exceeded allocated resources**;
2. the **task assigned to the child is no longer required**;
3. the **parent is exiting**;
4. (implied by the notes) the child misbehaved.

Two rules from the notes that are not on the slide text and are very examinable:

> "Usually, a child process is **not allowed to kill the parent** process. OS typically kills a child
> process if its parent process terminates. This is called **cascaded termination**." (S20 notes)

* **Direction is one-way**: parent → child only. Authority flows down the tree of §4.1.
* **Cascaded termination**: killing a parent orphans its children, so the OS kills them too. This is
  why the tree structure is not just a picture — it is a lifetime hierarchy.

Put together, the lifecycle is:

```
   fork ──> child exists ──> child exits (return data to parent, resources freed)
                     │
                     └────> parent aborts child (resource abuse / not needed / parent exiting)
                                   │
                                   └── if parent dies first: cascaded termination
```

---

## 5. Interprocess communication (S21–S28)

### 5.1 Independent vs cooperating processes (S22)

| | **Independent process** | **Cooperating process** |
|---|---|---|
| Definition (S22) | "cannot affect or be affected by the execution of other processes" | "can affect or be affected by the execution of other processes" |
| Shares data? | no | **yes** — "such processes have to communicate with each other to share data" |
| Needs IPC? | no | **yes** |
| Example | a compiler and a text editor running side by side | producer and consumer; a web server and its worker processes |

The reason the course cares: once two processes **share data**, *ordering* and *mutual exclusion*
become problems — which is why the very next lecture series (L5–6, [`../c5`](../c5)) exists.

> "Two models of Inter-Process Communication (IPC): **Message passing**, **Shared memory**." (S22)

### 5.2 The two IPC models (S23)

The slide is one figure with two panels: **(a)** A puts a message into a **mailbox in kernel
space**, B takes it out; **(b)** A and B both map the **same buffer in user space** and exchange data
with ordinary loads and stores.

| | **Message passing** | **Shared memory** |
|---|---|---|
| Where the data lives | in the **kernel** ("mailbox" object) | in **user space**, a memory region mapped into both |
| How data moves | `send` **copies** from A into kernel; `receive` **copies** out to B | plain memory **read/write** — no copying, no system call per message |
| Primitives | `send(message)`, `receive(message)` | nothing special: load/store instructions |
| Who synchronises | the kernel can do it for you | **the processes must** — the OS only provided the memory |
| Requires shared address space? | **no** | **yes** |
| Works across machines? | **yes** — "message passing is more general, and can be used for distributed systems" (S24 notes) | **no** — "shared variables are usually for a single machine" (S24 notes) |
| Speed | slower (copy + kernel entry per message) | faster (no copies) |
| Typical sizing | small amounts of control data | large amounts of data |

The notes add that in (b) *"the address of the shared memory should be known to both the processes.
So, it is in user space"* — and that is the whole trade-off: shared memory is fast **because** it
bypasses the kernel, and dangerous **because** it bypasses the kernel.

### 5.3 Message passing mechanics (S24)

> "Processes communicate and synchronize their actions **without resorting to shared variables**."
> (S24)

Two operations, both system calls:

```
   send(message)        message size fixed or variable
   receive(message)
```

For two processes P and Q to communicate they must:

1. **establish a communication link** between them;
2. **exchange messages** via `send`/`receive`.

**Fixed** size makes the kernel's buffer allocation trivial (a pool of equal slots) but forces the
application to fragment large data; **variable** size is flexible but needs a heap-style allocator
in the kernel. Either way the receiver must know the convention.

### 5.4 Direct vs indirect message passing (S25)

> "There are many implementation details for message passing. I have condensed those details and
> focus on two key important methods: direct and indirect communication." (S25 notes)

| | **Direct** | **Indirect** |
|---|---|---|
| Names | the **process** | a **mailbox** (also called a **port**) |
| Send | `send(P, message)` — send to process P | `send(A, message)` — send to mailbox A |
| Receive | `receive(Q, message)` — receive from process Q | `receive(A, message)` — receive from mailbox A |
| Coupling | sender must know the receiver's identity | sender needs only the mailbox id |
| How many parties | one named pair | any number of senders/receivers can share a mailbox |
| Lifetime | tied to the processes | tied to the mailbox object |

> "Mailbox is an object into which messages are placed and removed (like a queue)." (S25)
> "Each mailbox has a unique id so that senders and receivers can identify the mailbox." (S25 notes)

So an indirect mailbox is precisely a **queue of messages with an identifier** — the same queue
structure you saw for PCBs (S14), holding messages instead of processes.

### 5.5 The producer–consumer paradigm (S26)

> "Classical paradigm for cooperating processes. Producer process produces information that is
> consumed by a consumer process. Shared buffer used for storing information." (S26)

Two variants, distinguished only by whether the buffer can fill up:

| Model | Buffer | What happens when the producer is faster |
|---|---|---|
| **Unbounded buffer** | "places no practical limit on the size of the buffer" | the producer never waits; the buffer grows |
| **Bounded buffer** | "assumes that there is a fixed buffer size" | the producer **must wait** when the buffer is full |

The notes' analogy: manufacturers produce, consumers buy, and a **warehouse** temporarily stores the
goods — that warehouse is the buffer. Its purpose is to **decouple rates**; the unbounded model is
the idealisation where decoupling is free, the bounded model is reality where space is finite.

### 5.6 The bounded buffer in code (S27)

Reproduced from the slide (only the brace indentation is normalised):

```c
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
```

**Line by line.**

| Line | Meaning |
|---|---|
| `mailbox` with capacity **B** | the shared buffer *is* a mailbox object with a bound — hence "bounded" |
| `while (1)` | both processes run forever; this is a long-lived pair |
| `//pre-processing` | the producer manufactures the message (its real work) |
| `while(mailbox is full) wait;` | **back-pressure**: no room, so do not send |
| `send(mailbox, m)` | put one message in the queue |
| `while(mailbox is empty) wait;` | **starvation guard**: nothing to take, so do not receive |
| `receive(mailbox, m)` | take one message out (queue order, FIFO) |
| `//post-processing` | the consumer uses the message (its real work) |

**The three observations the examiner wants.**

1. **It is indirect message passing.** The primitives name a **mailbox**, not a process
   (`send(mailbox, m)`, not `send(P, m)`). The notes ask this directly: *"Does this example use
   direct or indirect c…"* — the answer is **indirect**.
2. **The bound B is the only difference from the unbounded model.** Delete the "full" test and the
   producer can never block: that *is* an unbounded buffer in this notation.
3. **The two loops are mirror images.** Full/empty, send/receive, pre/post. If you can write one you
   can write the other, and the mirror symmetry is what makes the code memorable.

**What the code does *not* do — and it matters.**

* `while (…) wait;` is a **busy wait** as written; nothing in the slide says the process blocks or
  sleeps. The efficient version blocks on a condition.
* There is **no mutual exclusion**. With two producers, both can test "not full" and both `send`,
  overflowing a capacity-B mailbox. With two consumers, both can test "not empty" and both
  `receive`, taking a message that is not there. The *conditions* are checked atomically by the
  kernel's queue operations in a real implementation, but the composition of check-then-act is not
  safe in general.
* Nothing enforces **ordering beyond FIFO**, and nothing prevents the consumer from spinning while
  the producer is descheduled.

That gap is exactly the subject of L5–6: semaphores, mutexes, condition variables, and the classical
problems. See [`../c5`](../c5). In *this* deck, be able to write the two loops and say what the
two `while` guards protect against.

---

## 6. Threads (S29–S40)

**Scope note (S29).** *"In this course, we mainly talk about processes. Therefore, we will quickly go
through the basic concepts of threads in the remainder of this chapter."* And, decisively: *"Only in
this part, we refer to the concepts of threads. All other parts in this course, we refer to process
(single-threaded process)."* So threads are examined **only here**, and every later lecture silently
assumes one thread per process.

### 6.1 What a thread is (S30)

> "A thread (or **lightweight process**) is a basic unit of **CPU utilization**." (S30)

A thread **consists of** exactly four things:

| Private to the thread | Why |
|---|---|
| **Thread id** | identity inside the process |
| **Program counter** | where this thread is executing |
| **Register set** | its live machine state |
| **Stack space** | its own call frames, locals, parameters |

A thread **shares with its peer threads** in the same process:

* the **code and data sections** (the text/data of S04 — all threads see the same globals);
* **operating-system resources**: open files, sockets, signals, working directory.

And: *"A traditional or **heavyweight process** is an executing program with a **single thread of
control**."* (S30)

So: **process = resource container (+ at least one thread); thread = unit of execution inside it.**
Everything in §2 about `text/data/heap/stack` describes the *process*; the thread adds a stack **per
thread** on top.

The rule that follows and that exam questions test: **anything on the stack is private; anything
global is shared and must be protected.**

### 6.2 Single-threaded vs multithreaded process (S31)

```
   SINGLE-THREADED PROCESS                MULTITHREADED PROCESS
   +---------------------+                +---------------------+
   |  code    data       |                |  code    data       |  <- shared
   |  files   regs       |                |  files              |
   |  +------+           |                |  +------+ +------+ +------+
   |  |stack |  <- one   |                |  |stack | |stack | |stack |  <- one per thread
   |  +------+           |                |  | TCB  | | TCB  | | TCB  |
   |  | PC   |           |                |  +------+ +------+ +------+
   |  +------+           |                |   T1   T2   T3
   +---------------------+                +---------------------+
       one PCB, one PC                    one PCB, N PCs, N register sets, N stacks
```

From the notes:

* *"A thread has its state (new, ready, running, waiting). A data structure called **thread control
  block (TCB)** is also used to record the information of a thread. Thus, a thread has very similar
  state transitions as a process."* (S31)
* Therefore the §2.3 state machine and §3.2 queue discipline apply **per thread**, with TCBs in place
  of PCBs.

| | **Process switch** | **Thread switch (same process)** |
|---|---|---|
| Save/restore | PCB: registers, PC, **memory-management info** | TCB: registers, PC |
| Address-space change | yes — reload base/limit or page-table base | **no** |
| Caches/TLB | cold after the switch | still warm |
| Cost | high | low |

### 6.3 Why multithread (S32)

> "In a multithreaded process, **while one thread is blocked and waiting, a second thread can run**.
> Cooperation of multiple threads in the same process results in **higher throughput**." (S32)

The worked example on the slide's notes is a **word processor**, one process with (at least) three
threads:

| Thread | Job | Blocks on |
|---|---|---|
| keystroke/input | accept typing | the keyboard (I/O) |
| display/formatting | render the document | the screen |
| auto-save | write the document to disk | the disk (I/O) |

*"Even if a thread (say the one accepting the keyboard input) is blocked, other threads can [run]."*
(S32 notes) — so the window stays responsive while saving. That is the **responsiveness** argument;
the other classic arguments (same address space, cheap creation, cheap switch) follow from §6.1–6.2.

### 6.4 Worked example: the multithreaded server (S33)

> "This architecture is very common in web servers, FTP servers, etc." (S33 notes)

```
   clients                     server process (one address space)
   +-------+                  +------------------------------------------+
   | client| --request----->  |  listening thread                        |
   +-------+                  |      |  creates a thread per request     |
                              |      v                                   |
                              |  +---------+ +---------+ +---------+     |
                              |  | thread1 | | thread2 | | thread3 |     |
                              |  +---------+ +---------+ +---------+     |
                              |     serve     serve        serve        |
                              +------------------------------------------+
```

The sequence, in the notes' words: a client submits a request → **the server creates a new thread to
serve the request** → **the server resumes listening** for further requests → the worker thread
serves independently → when finished, **the thread is deallocated**.

Why threads and not processes here?

| | Process per request | Thread per request |
|---|---|---|
| Address space | new one per request | shared — the file cache, config, connection table are visible to all |
| Creation cost | high | low |
| Context switch | expensive | cheap |
| Isolation | one crash kills one request | one crash kills the whole server |

So the server trades isolation for throughput — the mirror image of the browser's choice in §4.2,
which trades throughput for isolation. Being able to name that trade-off is worth marks.

### 6.5 The threading paradox: user threads vs kernel threads (S34)

> **Paradox.** "Allow users to implement an arbitrary number of threads, BUT the OS kernel can
> support a limited number of threads due to resource constraints." (S34)

The **solution is two layers of abstraction**:

| | **User threads** (logical) | **Kernel threads** (physical) |
|---|---|---|
| Created in | **user space**, by a library | **kernel space**, by the OS |
| Number | "as many as they want" | limited by resources |
| Speed | fast to create and manage | "slower to create and manage than user threads" |
| Known to the kernel? | no — the kernel sees only the kernel threads | yes |
| What gets scheduled | — | kernel threads |
| Resources | "resources are eventually allocated in kernel threads" | hold the real resources |

> "OS maintains the **mapping** from user to kernel threads." (S34)

Consequence worth stating: if 100 user threads map to 1 kernel thread, the OS thinks one runnable
entity exists, so the 100 user threads **cannot run in parallel** — the library can only interleave
them.

### 6.6 The three multithreading models (S35)

> "Model that defines the **mapping** between user threads and kernel threads: Many-to-One,
> One-to-One, Many-to-Many." (S35)

```
  MANY-TO-ONE            ONE-TO-ONE             MANY-TO-MANY
  u1 u2 u3               u1  u2  u3             u1 u2 u3 u4 u5
   \ | /                 |   |   |              \  |  /  /
    \|/                  |   |   |               \ | /  /
     k1                  k1  k2  k3                k1  k2
   (1 kernel)          (one each)             (m user -> n kernel, m >= n)
```

> **"Why is there no One-to-Many mapping? Wastage of OS resources to map a single user thread to many
> kernel threads."** (S35)

That is a complete answer to a "why not" question: a single thread of control gains nothing from
being executed by several kernel threads; you would pay kernel-thread cost for no extra concurrency.

#### Many-to-one (S36)

> "Disadvantage: A blocked user thread will also block other user threads mapped to the same kernel
> thread." (S36)

The notes sharpen it: *"**For those threads mapped to the same kernel thread**, they are unable to
run in parallel due to the single kernel thread. That is, if a thread is stuck by a system call or
I/O, the other user threads mapped to the same kernel thread are also blocked."*

```
 user:  u1 (I/O -> blocked)   u2 (runnable)   u3 (runnable)
              \                   |               /
               +--------- k1 (blocked) ----------+
                              |
                        nothing runs
```

Two separate limitations: **no parallelism** (only one kernel thread, so at most one core busy) and
**head-of-line blocking** (one blocking call blocks the group). The upside is that thread management
is entirely in user space and therefore cheap. The slide names no example; the classic ones are
green threads and early user-level thread libraries.

#### One-to-one (S37)

> "Each user-level thread maps to a **unique** kernel thread." (S37)
> "**Examples: Windows 95/98/NT/2000, OS/2**" (S37)

| Advantages | Disadvantages |
|---|---|
| "Provides **more concurrency** than many-to-one" — a blocked thread does not block others | "Creating a user thread **requires creating the corresponding kernel thread**" |
| true parallelism on multiple cores | "May create **too many kernel threads**, which is a burden on the system" |

The notes add: *"Both Windows and Linux support one-to-one model."* Note that this **differs from the
slide's example list** — see [NOTES.md](NOTES.md#3-known-slips-in-the-slides) for why (the slide list
is inherited from the textbook and is historically imprecise; Windows 95/98 were never one-to-one).

The trade: pay one kernel object per thread, get real concurrency — which is why mainstream general
purpose OSes use it and optimise the cost (thread pools, cheaper kernel threads).

#### Many-to-many (S38–S39)

S38 is the figure; S39 is the text:

> "Allows many user level threads to be mapped to many kernel threads. **Examples: C++20 coroutines,
> Golang goroutines.** Allows the operating system to create a sufficient number of kernel threads.
> Does **not** have the disadvantages of one-to-one and many-to-one models. Disadvantage: **not easy
> to decide the mapping**." (S39)

The notes expand: *"the operating system can create more kernel threads on a multi-core machine…
the developer can create as many user threads as they wish, and the corresponding kernel threads are
run in parallel."*

So many-to-many buys both halves — cheap user threads *and* real parallelism — at the price of a
**scheduling policy problem**: how many kernel threads, and which user thread on which. Sizing
example: 1000 user threads on an 8-core machine mapped to 8–16 kernel threads.

Caveat on the slide's examples: **Go goroutines** genuinely are an M:N scheduler (G–M–P). **C++20
coroutines** are language-level stackless coroutines, not OS-scheduled threads at all — the mapping is
loose. Quote the slide, but know that goroutines are the clean example.

### 6.7 The three models side by side

| | **Many-to-One** | **One-to-One** | **Many-to-Many** |
|---|---|---|---|
| User : kernel | m : 1 | 1 : 1 | m : n (m ≥ n) |
| Parallelism | none | yes | yes |
| Blocking one thread | blocks the whole group | only that thread | only that thread |
| Creation cost | cheapest | one kernel thread each | moderate |
| Kernel thread count | 1 | = number of user threads (can explode) | chosen by the OS (bounded) |
| Main disadvantage | head-of-line blocking, no parallelism | kernel-thread overhead | mapping is hard to decide |
| Slide's examples | none | Windows 95/98/NT/2000, OS/2 | C++20 coroutines, Go goroutines |

### 6.8 Readings the slide recommends (S40)

Not examinable: **Beej's Guide to Unix IPC** (<http://beej.us/guide/bgipc/>), a **POSIX pthreads**
tutorial (<http://randu.org/tutorials/threads/>), and the Windows process/thread API on MSDN.

---

## 7. Putting it all together

### 7.1 The three-way comparison that recurs in exams

| | **Message passing** | **Shared memory** | **Threads** |
|---|---|---|---|
| Shares memory? | no | yes | yes (whole address space) |
| Kernel involved per transfer? | yes | no | no |
| Works across machines? | yes | no | no |
| Synchronisation provided? | partly (blocking send/receive) | none — you must add it | none — you must add it |
| Speed | slowest | fastest | fastest |

The pattern: **every step you take away from the kernel buys speed and costs safety.**

---

## 8. Quick facts sheet

```
process states                 5   new, ready, running, waiting, terminated
state transitions              6   admit, dispatch, preempt, wait, wake, exit
schedulers                     3   long-term (job), short-term (CPU), medium-term (swap)
IPC models                     2   message passing, shared memory
message-passing styles         2   direct (name the process), indirect (name the mailbox)
multithreading models          3   many-to-one, one-to-one, many-to-many  (never one-to-many)
thread private parts           4   id, PC, register set, stack
process sections               4   text, data, heap, stack

timer interrupt period       100 ms                       (S11 notes)
short-term scheduler rate    ~100 ms                       (S16)
long-term scheduler rate     seconds to minutes           (S16)
context-switch overhead      s / (q + s)                   q = quantum, s = switch
   q = 100 ms, s = 5 ms  ->  5/105 = 4.8 %
   q = 100 ms, s = 2 ms  ->  2/102 = 2.0 %
buffer occupancy             0 <= n <= B                    bounded buffer, capacity B
```

Rule of thumb to quote: **short quantum → responsiveness but high overhead; long quantum → low
overhead but sluggish interactive response.** That is the same trade-off L3 formalises.

---

## 9. Practice problems

**P1.** For each event, give the transition (old state → new state) and say whether it is a
preemption: (a) the timer interrupt fires; (b) the process issues a `read()`; (c) the disk interrupt
for that `read()` arrives; (d) the process calls `wait()` for a child; (e) the process
executes its last instruction.

**P2.** A process is created. List five PCB fields that must be filled in before it can be
dispatched, and say what each is used for.

**P3.** Time slice 40 ms, context switch 4 ms, 6 runnable processes. What fraction of CPU time is
lost to switching? What would it be with a 10 ms slice?

**P4.** Using the S18 tree (root; console1, console2, swap, flush; unzip under console1, search under
console2): (a) how many processes? (b) how many leaves? (c) if the root is killed, which processes
die?

**P5.** Classify each primitive or setup as **direct MP**, **indirect MP**, or **shared memory**:
(a) `send(A, msg)`; (b) `receive(Q, msg)`; (c) two processes both mapped to the same segment and
exchanging data with `x = 1;` / `y = x;`; (d) a FIFO of messages with an integer id; (e) a socket
connected to a named peer.

**P6.** Bounded buffer with B = 4. The producer sends m1…m6 as fast as it can while the consumer
takes one message after every two sends. Trace the occupancy, and say when (if ever) the producer
blocks.

**P7.** A process has 4 threads. How many PCs, stacks, register sets and PCBs does it have? Which of
these would change if the OS used a many-to-one model with 1 kernel thread?

**P8.** Choose a model (many-to-one / one-to-one / many-to-many) and justify: (a) an embedded sensor
with 10 000 tiny tasks and 1 core; (b) a database server on a 64-core machine where every connection
needs a thread; (c) a web crawler with 200 000 logical fetch tasks on 16 cores.

**P9.** Explain, in terms of §2.4, why a process cannot go straight from **waiting** to **running**.

### Solutions

**S1.** (a) running → ready, **preempted** (S06). (b) running → waiting, not preemption. (c) waiting →
ready, not preemption — it still needs the CPU. (d) running → waiting, then waiting → ready when the
child exits; not preemption. (e) running → terminated.

**S2.** State (schedulability), pid (identity), PC (entry/resume address), registers (initial machine
state), priority (scheduling), memory info (base and limit), PCB pointer (so it can be enqueued).

**S3.** `4/44 = **9.1 %**`; with a 10 ms slice `4/14 = **28.6 %**`. Shorter slices cost more but give
each of the 6 processes a turn sooner — that is what you are buying.

**S4.** (a) **7** processes. (b) **4** leaves — unzip, search, swap, flush; console1 and console2 are
internal nodes. (c) Under **cascaded termination** all 7 die: the root's death takes its whole
subtree.

**S5.** (a) indirect, (b) direct, (c) shared memory, (d) indirect, (e) indirect (a named endpoint, not
a process).

**S6.** Occupancy, B = 4:

```
 send m1 -> 1
 send m2 -> 2
 receive -> 1
 send m3 -> 2
 send m4 -> 3
 receive -> 2
 send m5 -> 3
 send m6 -> 4   <- mailbox now full
```

The producer never blocks during m1…m6 — the consumer keeps pace, and the peak (4) is reached only
on the last send. One more send would find the mailbox full and the producer would wait at
`while(mailbox is full) wait;`. If the consumer lagged instead, occupancy would hit 4 by m5 and the
producer would block there.

**S7.** **1 PCB**, **4 PCs**, **4 stacks**, **4 register sets** (per-thread, saved in the TCB). With
many-to-one the counts do not change; what changes is that only **one** can be running at a time, and
a blocking call in one blocks all four.

**S8.** (a) **many-to-one** — one core means no parallelism to lose, and 10 000 kernel threads would
be unaffordable. (b) **one-to-one** — 64 cores need real parallelism and each connection genuinely
blocks; the kernel-thread count is bounded by the connection count, which the admin controls.
(c) **many-to-many** — 200 000 tasks cannot each hold a kernel thread, but the 16 cores must stay
busy and one blocked fetch must not stall the rest.

**S9.** Because "running" means holding the CPU, and the CPU is granted by **dispatch** from the
**ready** queue. When the awaited event completes, the process becomes *eligible*, but eligibility is
not ownership — it must re-enter the ready queue and wait for the short-term scheduler. Only the
running → ready transition (preemption) and ready → running (dispatch) involve the CPU.

---

## 10. Self-test questions

1. State the difference between a program and a process, and give an example where one program
   corresponds to three processes.
2. Name the four sections of a process image and say which two grow and in which directions.
3. In a batch system, what is the unit called? In a time-sharing system?
4. Define the five process states in one line each.
5. Why is "ready" not the same as "waiting"?
6. Which transition does the timer interrupt cause, and why does multiprogramming need it?
7. List six fields of a PCB and say what each is for.
8. Where are PCBs stored, and why not in the process's own memory?
9. Define a context switch and explain why it is called overhead.
10. What is a job queue? A ready queue? A device queue?
11. Distinguish the long-term, short-term and medium-term schedulers by *what they select* and *how
    often they run*.
12. Who controls the degree of multiprogramming, and when?
13. Draw the process tree of a login session with two consoles, and say how many fork calls produced
    it.
14. What two execution orders can follow `fork`? Which system call makes the parent wait?
15. Give three reasons a parent may abort a child.
16. What is cascaded termination, and why can a child not kill its parent?
17. Distinguish independent from cooperating processes.
18. Compare message passing and shared memory on: where the data lives, speed, and cross-machine
    support.
19. Give the primitives for direct and for indirect message passing.
20. Write the bounded-buffer producer and consumer loops and say what each `while` guard prevents.
21. Is `send(mailbox, m)` direct or indirect? Why?
22. What four things does a thread own privately, and what does it share?
23. Why is a thread switch cheaper than a process switch?
24. Explain the threading paradox and the two-layer solution.
25. Describe the three multithreading models and one disadvantage of each.
26. Why is there no one-to-many model?
27. In a many-to-one model, one thread blocks on I/O. What happens to its peers?

### Answer sketches

1. Program = static executable file; process = dynamic execution of it. Three clicks → three processes.
2. text, data, heap (**up**), stack (**down**).
3. Job; process (program/command).
4. New = being created; ready = runnable, awaiting CPU; running = executing; waiting = blocked on I/O
   or an event; terminated = finished.
5. Ready waits for the **CPU**; waiting waits for an **event**. Both are "not running", only one is
   schedulable.
6. running → ready. Without it a CPU-bound process never yields and others starve.
7. State, pid, PC, registers, priority, memory info (base/limit), open files, PCB links.
8. **Kernel space**: the process cannot corrupt its own state, and the state must survive while it is
   not running; edits need kernel mode.
9. Save old context, load new context; no user work is done meanwhile.
10. Job queue = the queue for a given state (slide's usage); ready queue = all ready processes; device
    queue = processes waiting for one device.
11. Long-term: disk → memory, every seconds/minutes. Short-term: ready → running, ~100 ms. Medium-term:
    memory ↔ disk, on load changes.
12. Long-term **initially**, medium-term **thereafter**.
13. Root → console1, console2 (+ swap, flush); console1 → unzip; console2 → search: six forks, seven
    processes.
14. Concurrent, or parent waits (`wait()` / `join()`).
15. Exceeded allocated resources; task no longer required; parent is exiting.
16. Killing a parent kills its descendants; authority is one-way down the tree.
17. Independent: cannot affect or be affected. Cooperating: can affect and be affected, so they must
    communicate to share data.
18. Message passing: data in kernel mailboxes, slower, cross-machine. Shared memory: data in user
    space, fastest, single machine.
19. Direct: `send(P, msg)` / `receive(Q, msg)`. Indirect: `send(A, msg)` / `receive(A, msg)`.
20. §5.6. `full` prevents overflow; `empty` prevents consuming a non-existent message.
21. Indirect — the primitive names a **mailbox**, not a process.
22. Owns: thread id, PC, register set, stack. Shares: code, data, OS resources.
23. No address-space change, so memory-management registers stay put and TLB/caches stay warm.
24. Users want unlimited threads, the kernel can only afford a bounded number; so user threads map onto
    kernel threads, and the OS keeps the mapping.
25. Many-to-one: blocked thread blocks the group, no parallelism. One-to-one: one kernel thread each,
    overhead. Many-to-many: mapping is hard to decide.
26. One user thread gains nothing from several kernel threads — pure waste of OS resources.
27. Peers on that **same** kernel thread are also blocked; in a pure many-to-one that is all of them.

---

## 11. Glossary

| Term | Meaning |
|---|---|
| **Process** | a program in execution; execution progresses sequentially (S03) |
| **Process image** | the process's memory: text, data, heap, stack, inside `[base, base+limit)` (S04) |
| **Ready / waiting** | runnable but no CPU / blocked on I/O or an event (S05) |
| **PCB** | process control block: state, pid, PC, registers, priority, memory info, files, links (S08) |
| **TCB** | thread control block: the same bookkeeping for one thread (S31) |
| **Context switch** | save the old process's context, load the new one's; pure overhead (S12) |
| **Ready queue** | all processes in the ready state (S13) |
| **Device queue** | processes waiting for one particular I/O device (S13) |
| **Long-term / job scheduler** | admits processes from disk into memory (S15) |
| **Short-term / CPU scheduler** | picks which ready process runs next (S15) |
| **Medium-term scheduler** | swaps a partially executed process out and back (S15) |
| **Degree of multiprogramming** | number of processes that can be resident in memory (S16) |
| **fork** | the mechanism by which a parent creates a child; makes a process tree (S18) |
| **exit** | the process terminates itself and returns data to its parent (S20) |
| **abort** | the parent terminates a child (S20) |
| **Cascaded termination** | killing a parent kills its descendants (S20) |
| **Independent process** | cannot affect or be affected by others (S22) |
| **Cooperating process** | can affect and be affected; must communicate (S22) |
| **Message passing** | IPC through kernel-mediated `send`/`receive` (S24) |
| **Shared memory** | IPC through a region mapping into both address spaces (S23) |
| **Mailbox / port** | an object (queue) holding messages, with a unique id (S25) |
| **Direct / indirect MP** | naming the process / naming the mailbox (S25) |
| **Unbounded / bounded buffer** | no practical limit / fixed capacity B (S26) |
| **Thread** | basic unit of CPU utilisation: id, PC, registers, stack (S30) |
| **Lightweight process** | synonym for thread (S30) |
| **Heavyweight process** | a process with a single thread of control (S30) |
| **User thread** | created in user space, invisible to the kernel (S34) |
| **Kernel thread** | created in kernel space, the thing actually scheduled (S34) |
| **Multithreading model** | the user→kernel thread mapping (S35) |
