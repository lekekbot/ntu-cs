# Processes & Threads — Things to Take Note Of

The "before the exam" file for `Part2 (Process and Threads).pptx` (40 slides). It records what is
repeatedly stressed, what is easy to get wrong, and where the slides themselves are unreliable. It
contains **no new teaching material** — that is in [STUDY_GUIDE.md](STUDY_GUIDE.md).

There is **no audio** for this deck, so references are **slide numbers** (`S17`). `[NOTES]` are the
lecturer's speaker notes.

---

## 1. What is repeatedly stressed

| Point | Where | Why it matters |
|---|---|---|
| **"This figure is very important"** — the state transition diagram | S06 notes | It is the spine of the whole part: queues, schedulers, `wait()`, context switches and threads all reuse it |
| **Ready vs waiting — "waiting … although for different reasons"** | S05 notes | The single most common definitional error |
| **"The system does NO useful work while switching"** | S12 | Context switch is *overhead*, not work. Every performance question hinges on this |
| **PCBs are kept in a queue structure, in kernel space, and changed only in kernel mode** | S08, S09 notes | Explains protection, and why a state change is an OS action |
| **Degree of multiprogramming: long-term initially, medium-term thereafter** | S16 | A precise, quotable division of labour |
| **"A child process is not allowed to kill the parent" + cascaded termination** | S20 notes | Not on the slide text — notes only. Easy to miss |
| **"Only in this part do we refer to threads; all other parts mean single-threaded process"** | S29 notes | Sets the scope of the thread material to this deck only |
| **Threads share code/data/OS resources but not stack/PC/registers** | S30 | Everything about thread safety follows from this line |

---

## 2. Exam traps

1. **Process ≠ program.** Process is dynamic (an execution); program is static (a file). Clicking one
   executable three times makes three processes of one program.
2. **Ready ≠ waiting.** Ready waits for the **CPU**; waiting waits for **I/O or an event**. A
   process in the waiting state is *not* schedulable.
3. **The timer interrupt causes running → ready, not running → waiting.** Preemption never involves
   I/O.
4. **waiting → running is impossible.** The process must pass through ready and be dispatched.
5. **A context switch saves and restores the PCB, and costs time.** Never describe it as useful work;
   never claim it is free.
6. **The PCB is in kernel space.** Not in the process image, not on disk.
7. **Long-term scheduler ≠ the thing that runs every 100 ms.** Long-term is seconds/minutes and
   admits from disk; the ~100 ms one is short-term.
8. **Medium-term swapping does not change the long-term scheduler's decision** — it changes the
   *current* degree of multiprogramming.
9. **A device queue's length is a load indicator.** Empty device queue = idle device.
10. **`wait()` / `join()` put the parent in the *waiting* state**, and it returns to *ready* when the
    child terminates — not straight to running.
11. **Termination direction is one-way.** Parent may abort child; child may not kill parent. Killing
    the parent kills the descendants (cascaded termination).
12. **Message passing copies through the kernel; shared memory does not.** Therefore shared memory is
    faster and message passing works across machines.
13. **Direct MP names a process; indirect MP names a mailbox/port.** `send(mailbox, m)` is
    **indirect** — that is the answer to the question the S27 notes ask.
14. **In shared memory the OS supplies the memory, not the synchronisation.** That is the whole
    reason L5–6 exists.
15. **Bounded buffer: producer waits on *full*, consumer waits on *empty*.** Swapping the two is the
    classic blunder.
16. **A thread has its own stack, PC and registers — never its own code or data.**
17. **A thread switch in the same process does not change the address space**, which is why it is
    cheaper than a process switch.
18. **Many-to-one blocks the *group*, not just the thread.** Many-to-one also gives **no parallelism**
    even when threads never block.
19. **One-to-one's cost is kernel-thread creation**, not switch cost.
20. **There is no one-to-many model**, and the reason is *waste of OS resources*, not impossibility.
21. **Many-to-many is not "unlimited kernel threads"** — the OS picks *n*, and the difficulty is
    choosing the mapping.
22. **Threads are not on the S01 overview table.** Do not invent a lecture number for them.

---

## 3. Known slips in the slides

These are problems in the deck itself (or in the speaker notes), not extraction errors. Learn the
correct version, and if asked, follow the slide but say why it is loose.

| Where | What the slide/notes say | Correct version |
|---|---|---|
| **S13** | "**Job queue**: Set of all processes **with the same state** in the system" | Standard usage: the **job queue** is the set of **all** processes in the system, including those still on disk awaiting admission; a per-state list is just "a queue" (ready queue, device queue). The deck's own S15 says the long-term scheduler selects "processes from disk", which are in no in-memory state queue — consistent with the standard meaning, not with S13's. |
| **S03 notes** | "process is a formal term for operating system; and **a job is a larger concept**" | Muddled, and it contradicts the slide, which says **Job = Process**. In the exam, use the slide: job is the batch-system word for a process. |
| **S04** | Heap example `a=new int[10]`, while the notes talk about C/C++ | `new` is **C++** (and Java), not C — C would use `malloc`. Cosmetic, but do not write "C" beside it. |
| **S16** | Short-term scheduler "invoked frequently (e.g., **100 milliseconds**)" | 100 ms is the **quantum/timer period**, not the invocation rate of the scheduler — it is also invoked on every blocking call and every interrupt, i.e. far more often. Read "100 ms" as "at least every 100 ms". |
| **S37** | One-to-one examples: "**Windows 95/98**/NT/2000, OS/2" | Windows **95/98 used many-to-one** user-level threads; only **NT/2000** were genuinely one-to-one. The list is inherited from the textbook. |
| **S37 notes** | "**Both Windows and Linux support one-to-one**" | True today, but it **contradicts the slide's own list** (which omits Linux and includes 95/98). Do not quote both in one answer. |
| **S39** | Many-to-many examples: "**C++20 coroutines**, Golang goroutines" | Goroutines are a genuine M:N scheduler. **C++20 coroutines are language-level stackless coroutines**, not OS-scheduled threads — a loose mapping. Goroutines are the clean example. |
| **S36** | Many-to-one slide gives **no example** | The classic textbook example is Solaris **green threads** / early JVM user-level threads. Mentioning one is safe; asserting it is "on the slide" is not. |
| **S27** | `while(mailbox is full) wait;` with no blocking primitive and **no mutual exclusion** | As written this is a **busy wait**, and two producers can both pass the full-check and overflow a capacity-B mailbox. The slide shows *where* the conditions go, not how to enforce them — that is L5–6. |
| **S27** | Consumer's closing braces and the `//post-processing…` line are indented inconsistently | Layout artifact of the original slide and of the extraction. The brace structure is still balanced: function → `while(1)` → (unbraced) `while`. |
| **S31** | Slide has **no body text**; thread states and the **TCB** appear only in the [NOTES] | If you only read slide text you will miss the TCB. It is lecturer-stated, so treat it as examinable, but know it is notes-only. |
| **S38** | Text-free slide; the many-to-many definition is on **S39** | Read S38+S39 as one item. Same pattern: **S07, S14, S23, S31, S33, S38** are figure-only. |
| **S02 notes** | The review of the previous lecture is **cut off mid-sentence** ("Then, we spoke about operating system") | This is a **text-extraction truncation**, not a missing slide. The same happens in S04, S09, S11, S14, S18, S22–S24, S27, S32–S36. Do not read a truncated note as an omission in the deck. |

---

## 4. Numbering: slides vs lectures

Two different numbers exist, and mixing them up is easy.

**Slide numbers.** This deck is **S1–S40** in presentation order, and that is how this folder cites
everything. Note the structure:

| Slides | Role |
|---|---|
| S01 | course overview table |
| S02 | Part 2 outline + review of the previous lecture |
| S03–S09 | Process Concept |
| **S10** | divider (repeats the outline) |
| S11–S16 | Process Scheduling |
| **S17** | divider |
| S18–S20 | Operation on Processes |
| **S21** | divider |
| S22–S27 | Interprocess Communication |
| **S28** | divider |
| S29–S40 | Threads |

Four slides are **pure dividers** (S10, S17, S21, S28) repeating the same five-line outline; S02 is
the outline plus the review of the previous lecture. So "40 slides" contains only ~35 content
slides, and roughly a dozen of those are figures with little or no text.

**Lecture numbers.** S01 prints:

```
Processes (L2)      Scheduling (L3)        Synchronization (L5-6)
Deadlocks (L7)      Memory organization (L8)  Virtual memory (L9-10)
Filesystems (L11)   I/O & disk (L12)       Special: Real-time OS & virtualization
```

* **Threads are not printed on that slide at all.** They are part of this deck (S29–S40) but the
  course overview gives them no number. By **elimination** — L1 introduction, L2 processes,
  L3 scheduling, L5–6 synchronization — threads are **L4**. That is an inference; say so if you
  quote it.
* **Other decks print an older scheme**: `Synchronization (L4-5)` / `Deadlocks (L6)`. Under that
  scheme everything from synchronization onwards shifts by one. Always quote the topic with the
  number.
* Consequently: a lecture number tells you *which hour of the module* something is taught, and a
  slide number tells you *where in this deck* it is. They are unrelated.

---

## 5. Coverage map (which slide teaches what)

| Slide | Topic |
|---|---|
| S01 | Course overview; module map; lecture numbers |
| S02 | Part 2 outline; review of DMA, privileged instructions, protections |
| S03 | Process = program in execution; batch jobs vs time-sharing processes; job = process |
| S04 | Process in memory: text, data, heap, stack; base and base+limit |
| S05 | Five states defined |
| S06 | State transition diagram; timer interrupt and preemption |
| S07 | PCB layout (figure) |
| S08 | PCB fields and why each exists |
| S09 | PCBs in kernel space vs process images in user space; kernel-mode edits; the `new int[10]` question |
| S10 | Divider |
| S11 | Context switch timeline (P0/P1, timer every 100 ms) |
| S12 | Context switch definition and overhead |
| S13 | Job / ready / device queues; state change = queue migration |
| S14 | Queue headers, head/tail pointers, device queue length as load |
| S15 | Long-term, short-term, medium-term schedulers |
| S16 | Invocation frequencies; degree of multiprogramming |
| S17 | Divider |
| S18 | Process creation; fork; process tree (root, consoles, swap, flush, unzip, search) |
| S19 | Concurrent vs parent-waits; `wait()` / `join()`; browser tabs; background processes |
| S20 | Termination: exit, abort, the four abort reasons; cascaded termination (notes) |
| S21 | Divider |
| S22 | Independent vs cooperating processes; two IPC models |
| S23 | IPC figure: message passing via kernel mailbox vs shared memory in user space |
| S24 | Message passing: `send`/`receive`, fixed or variable size, establishing a link |
| S25 | Direct vs indirect (mailbox/port) message passing |
| S26 | Producer–consumer; unbounded vs bounded buffer |
| S27 | Bounded-buffer producer/consumer loops; direct-or-indirect quiz in the notes |
| S28 | Divider |
| S29 | Threads outline; scope restriction for the rest of the module |
| S30 | Thread anatomy (id, PC, registers, stack) and what it shares; lightweight vs heavyweight |
| S31 | Single-threaded vs multithreaded process figure; thread states and TCB (notes) |
| S32 | Benefits: overlap while blocked, throughput; the word-processor example |
| S33 | Multithreaded server: listen thread + one thread per request |
| S34 | The threading paradox; user threads vs kernel threads; the mapping |
| S35 | The three models; why no one-to-many |
| S36 | Many-to-one: a blocked thread blocks its peers on the same kernel thread |
| S37 | One-to-one: examples, more concurrency, kernel-thread cost |
| S38 | Many-to-many figure |
| S39 | Many-to-many definition, examples, disadvantage |
| S40 | Advanced readings (Beej IPC, pthreads, Win32) |

---

## 6. Memory hooks

* **"Process is running; program is resting."** Dynamic vs static in six words.
* **"Ready waits for the CPU; Waiting waits for the world."**
* **PCB = the process's passport** — it carries identity, destination (PC), and history (registers),
  and the border guard (kernel) is the only one who may stamp it.
* **Long-term hires, short-term dispatches, medium-term parks.** Hire once in a while, dispatch every
  quantum, park when the car park (memory) is full.
* **fork = family tree.** Careful: **when the parent dies, the children follow** (cascaded).
* **A mailbox is a queue with a name.** Naming the queue (not the person) = indirect.
* **Message passing = posting letters (the post office sees them); shared memory = a shared
  whiteboard (nobody supervises).**
* **Full → producer stops; empty → consumer stops.**
* **A thread = private stack, public everything else.**
* **Many-to-one = one checkout lane** (one person blocks the queue); **one-to-one = a lane each**
  (build more lanes, pay for them); **many-to-many = a car pool** (queue forms, cars are sized to the
  road).
* **No one-to-many** = many bosses for one worker: wages paid, work unchanged.

---

## 7. Quick self-check before the exam

- [ ] Can you draw the four-section process image and say which register pair bounds it?
- [ ] Can you draw the five states with **all six** transitions and the cause of each?
- [ ] Can you say in one line why ready ≠ waiting?
- [ ] Can you list eight PCB fields without looking?
- [ ] Can you explain where the PCB lives and why it must be edited in kernel mode?
- [ ] Can you compute context-switch overhead for a given quantum and switch cost?
- [ ] Can you name the three schedulers, what each selects, and how often each runs?
- [ ] Can you say who controls the degree of multiprogramming, and when?
- [ ] Can you draw the S18 process tree and count its processes, leaves and forks?
- [ ] Can you distinguish exit from abort, and state cascaded termination?
- [ ] Can you compare message passing vs shared memory on speed, location and distribution?
- [ ] Can you write `send(P,m)` vs `send(A,m)` and say which is direct?
- [ ] Can you reproduce the bounded-buffer loops from memory and explain both guards?
- [ ] Can you list what a thread owns privately and what it shares?
- [ ] Can you state why a thread switch is cheaper than a process switch?
- [ ] Can you explain the paradox and the two-layer solution?
- [ ] Can you draw all three multithreading models, name one disadvantage of each, and explain why
      one-to-many is absent?
