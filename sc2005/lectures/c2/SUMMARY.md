# Processes & Threads — Summary (one page)

40 slides, two halves, one question: **what is the unit of work the OS schedules, what does it
remember about it, and how do two of them talk?**

---

## The 60-second version

1. A **process** is a *program in execution* — dynamic; a **program** is an executable file —
   static. The textbook uses **job** = **process** (S03).
2. It owns a region between **base** and **base + limit** holding four sections: **text, data,
   heap, stack**. Heap grows up, stack grows down (S04).
3. Five states: **new → ready → running → waiting → terminated** (S05). Both ready and waiting are
   "not running", but ready waits for the **CPU** and waiting waits for **I/O or an event**.
4. The OS records everything in a **PCB** — state, pid, PC, registers, priority, memory info, open
   files, links to other PCBs — stored in **kernel space**, editable only in kernel mode (S07–S09).
5. A **context switch** saves the old PCB and loads the new one; it is **pure overhead** — no useful
   work is done (S12). Timer interrupts every ~100 ms drive it (S11 notes).
6. Processes live in **queues** (ready queue; one device queue per device), all in kernel memory
   (S13–S14). **Long-term** admits from disk, **short-term** picks the next to run, **medium-term**
   swaps a partially executed process out and back (S15).
7. Processes form a **tree** made by `fork`; the parent either runs **concurrently** with the child
   or **waits** (`wait()` / `join()`) (S18–S19). A process ends by **exit** (itself) or **abort**
   (parent kills it); killing a parent kills its children — **cascaded termination** (S20).
8. Cooperating processes need **IPC**: **message passing** (kernel mailbox) or **shared memory**
   (user space) (S22–S23). Message passing is **direct** (name the process) or **indirect** (name a
   mailbox) (S25).
9. The classical workload is **producer–consumer** with an **unbounded** or **bounded** buffer; the
   bounded version waits when the mailbox is full / empty (S26–S27).
10. A **thread** is a *lightweight process*: it owns an id, PC, register set and stack, and **shares**
    code, data and OS resources with its peers (S30). Threads overlap blocked work and let a server
    serve many clients from one process (S32–S33).
11. Threads come in two layers: **user threads** (cheap, unlimited) and **kernel threads** (limited,
    scheduled by the OS). The mapping is the **multithreading model**: **many-to-one**,
    **one-to-one**, **many-to-many** — never one-to-many (S34–S39).

---

## The table you must be able to reproduce

| | **Process** | **Thread** |
|---|---|---|
| Also called | heavyweight process | **lightweight process** — the unit of **CPU utilisation** |
| Private | address space, PCB, open-file table | thread id, PC, register set, stack |
| Shared with peers | nothing (isolated) | code section, data section, OS resources (open files) |
| Creation / switch cost | high (new address space, memory maps) | low (new stack + registers, same maps) |
| Isolation | one crash does not kill another process | one thread's bad pointer kills the process |
| Bookkeeping | PCB | TCB |

## The three multithreading models (S35–S39)

| Model | Mapping | Pro | Con | Named examples |
|---|---|---|---|---|
| **Many-to-one** | many user threads → **one** kernel thread | cheapest; user-space scheduling; any number of threads | **one blocked thread blocks all** threads on that kernel thread; no parallelism | not on the slide |
| **One-to-One** | each user thread → its **own** kernel thread | real concurrency; a blocked thread does not block others | creating a user thread **requires** a kernel thread → overhead, too many kernel threads | Windows 95/98/NT/2000, OS/2 (slide); Windows and Linux (notes) |
| **Many-to-Many** | m user threads → n kernel threads, m ≥ n | keeps the good halves of both; OS sizes n to the machine | **hard to decide the mapping** | C++20 coroutines, Go goroutines (slide) |

**One-to-many does not exist**: one user thread mapped to many kernel threads only wastes OS
resources (S35).

---

## Definitions worth memorising verbatim

* **Process** — a program in execution; execution must progress in a sequential fashion (S03).
* **Job** — synonym for process in this textbook (S03).
* **PCB** — the data structure holding all information associated with a process: pointers to other
  PCBs, state, pid, PC, CPU registers, priority, memory-management info, open files (S08).
* **Context switch** — saving the context of the old process and loading the saved context of the
  new one (S12).
* **Degree of multiprogramming** — the number of processes that can be supported in main memory at
  once (S16 notes); set initially by the long-term scheduler, thereafter by the medium-term one.
* **Independent process** — cannot affect, and is not affected by, other processes (S22).
* **Cooperating process** — can affect, and be affected by, other processes; must communicate to
  share data (S22).
* **Thread** — a basic unit of CPU utilisation consisting of thread id, program counter, register
  set and stack space (S30). **User thread** — created in user space; **kernel thread** — the thing
  actually scheduled (S34).

---

## Worked numbers worth remembering

**The bounded buffer (S27).** A mailbox of capacity **B** messages. Producer: pre-process → *while
mailbox full, wait* → `send(mailbox, m)`. Consumer: *while mailbox empty, wait* →
`receive(mailbox, m)` → post-process. Three things to say about it:

1. `send(mailbox, m)` / `receive(mailbox, m)` name a **mailbox**, not a process → this is **indirect**
   message passing. The speaker notes ask exactly this question.
2. The mailbox **is** the buffer: capacity B ⇒ a **bounded buffer**. Remove the capacity check and
   "full" can never happen ⇒ unbounded.
3. `while (…) wait;` as written is a **busy wait with no mutual exclusion**: two producers can both
   see "not full" and both send. The code shows *where* the conditions are, not how to enforce them —
   that is [`../c5`](../c5).

**The process tree (S18).** Root process forks `console1`, `console2`, `swap`, `flush`;
`console1` forks `unzip`; `console2` forks `search`. That is **7 processes** — 1 root + 4 direct
children + 2 grandchildren — and one tree edge per fork.

**Context-switch overhead (S11, S12).** Timer fires every **100 ms**; if a switch costs **5 ms**,
overhead is `5 / (100 + 5) ≈ **4.8 %**`. Short-term scheduler is invoked at that kind of rate
(~100 ms, S16); long-term every **seconds to minutes**.

**States and transitions (S06).** Five states, six transitions: new→ready (admitted), ready→running
(dispatch), running→ready (timer interrupt), running→waiting (I/O or event wait), waiting→ready
(event completes), running→terminated (exit).

---

## Ten things that decide exam marks

1. **Process is dynamic, program is static.** Never write "a process is a file".
2. **Ready ≠ waiting.** Ready waits for the **CPU**; waiting waits for **I/O/event**. Confusing them
   loses the state-diagram marks.
3. **Preemption comes from the timer interrupt** — the running process is moved to ready, not to
   waiting.
4. **The PCB is in kernel space**, and every state change is a PCB field update; only kernel mode may
   do it (S09 notes).
5. **Context switch = overhead.** "The system does NO useful work while switching" (S12).
6. **Long-term = admission from disk; short-term = CPU dispatch; medium-term = swap out/in.**
   Degree of multiprogramming is long-term first, medium-term after (S16).
7. **`wait()` / `join()` put the parent in the waiting state** until the child terminates.
8. **A parent dying takes its children with it** — cascaded termination; children may not kill the
   parent (S20 notes).
9. **Message passing needs no shared address space** (so it works across machines); **shared memory
   is faster** but lives in user space and needs the address known to both (S23 notes).
10. **Threads share code/data/files, not registers/stack.** In many-to-one, a blocked thread blocks
    every thread mapped to the same kernel thread (S36).

---

## What is *not* in this series

* **Scheduling algorithms** — FCFS, SJF, priority, round robin, multilevel queues. S15/S16 name the
  *schedulers*, never an algorithm; they are taught in [`../c3`](../c3).
* **Synchronization** — semaphores, monitors, mutex, critical sections, and the classic problems.
  S27 shows the conditions but no mechanism: see [`../c5`](../c5).
* **Deadlocks** — appear only as a line in the S01 overview; see [`../c7`](../c7).
* **The real `fork()` API and its return values**, copy-on-write, `exec`, zombies and orphans. The
  deck gives a *tree diagram* for fork (S18), not code.
* **Thread library APIs** — pthreads, Win32, C++ `std::thread`. S40 only points at readings.
