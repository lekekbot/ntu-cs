# SC2005 — CPU Scheduling: Study Guide

Companion to the slide deck `Part3 (CPU Scheduling).pptx` (**30 slides, no audio**). Citations are
slide numbers: **`S14`** means slide 14. Verbatim slide text, including the lecturer's speaker notes,
is in [`transcripts/01-cpu-scheduling-slides.md`](transcripts/01-cpu-scheduling-slides.md); notes are
marked `[NOTES]` there.

One structural warning before you start. The `.pptx` keeps its Gantt charts as a pile of separate
text boxes, so the extracted text shows process names and numbers **in no meaningful order**
(`P1 P3 P2 4 2 11 0 P4 5 7 …`). Every chart below was therefore **rebuilt from the arrival/burst
table** and then **checked against the average printed on the slide**. A reconstruction is only
trusted when it reproduces that printed average exactly; each one is shown with the check. If you
already know the deck, this is why the numbers in the transcript look scrambled — the deck is fine,
the extraction is not.

---

## 0. The chapter in one picture

L2 gave you the **process state diagram**: `new → ready → running → waiting → ready → … → terminated`.
The ready queue is the set of processes that *could* run. L3 answers the only question left:

> **More than one process is ready; the core is free. Which one do we run, and for how long?**

Everything in the thirty slides hangs off that sentence.

```
                     +---------------------------+
                     |   READY QUEUE (L2)        |   n processes waiting
                     +---------------------------+
                                  |
                    (1) WHO?  ------+------ (2) HOW LONG?
                        |                       |
        +---------------+--------+     +--------+---------+
        |  FCFS      S11-S13     |     | nonpreemptive    |
        |  SJF/SRTF  S14-S16     |     | preemptive (RR)  |
        |  Priority  S17         |     | quantum q S18-S21|
        |  RR        S18-S21     |     +------------------+
        |  Multilevel S22-S23    |
        +------------------------+
                        |
        +---------------+-------------------+
        |  ONE CORE  S10-S23                |
        |  MANY CORES S24-S30               |
        |     partitioned (AMP) S25-S26     |
        |     global (SMP)      S27-S30     |
        +-----------------------------------+
                        |
              (3) WHAT DID IT COST?
                  turnaround | waiting | response      S07-S09
                  averaged over all processes
```

Three layers of the chapter, in the deck's own order (S02):

| Layer | Slides | Question |
|---|---|---|
| **Basic concepts** | S03–S09 | what a burst is, when scheduling happens, what we are optimising |
| **Criteria** | S07–S09 | the five numbers we measure and average |
| **Algorithms** | S10–S30 | uniprocessor first (S10–S23), then multiprocessor (S24–S30) |

### 0.1 Two scheduling problems that share a name

"FCFS" and "scheduling" appear twice in SC2005. Do not let them bleed into each other:

| | **CPU scheduling** (this chapter, L3) | **Disk scheduling** (L12, [`../c12`](../c12)) |
|---|---|---|
| Queue contents | **processes** waiting for a **CPU core** | **block requests** waiting for the **disk head** |
| "Job length" | CPU burst, given in the question | cylinder distance, computed from the request list |
| Algorithms | FCFS, SJF/SRTF, priority, RR, multilevel queue | FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK |
| Cost measured | **time** (ms) per process | **head movement** (cylinders) |
| Preemption | yes — RR, SRTF | no meaning — the head cannot teleport |

Only FCFS appears in both. **Cylinders, seek time, tracks, head movement ⇒ L12.** Bursts, quantum,
turnaround ⇒ here.

---

## 1. Basic concepts (S03–S09)

### 1.1 The CPU–I/O burst cycle (S03, S04)

> **CPU burst**: the duration of one CPU execution cycle.
> **I/O burst**: the duration of one I/O operation (the wait time).

A process does not compute from start to finish. It computes for a while (**CPU burst**), then asks
for something from the outside world and waits (**I/O burst**), then computes again. S04 draws the
alternating sequence: the process starts with a CPU burst, then reads a file (I/O burst), then
computes, and so on in a cycle (S04 notes).

```
   CPU burst      I/O burst      CPU burst      I/O burst      CPU burst
  |=========|                  |=========|                  |===|
              |############|                |########|
              ^ waiting for I/O: the core is IDLE if nobody else is ready
```

That last line is the whole motivation for scheduling. A single process leaves the core idle during
every I/O burst. **Multiprogramming** — keeping several processes in memory at once so the ready
queue is never empty — is what turns those idle gaps into someone else's CPU time. The deck states
the objective bluntly (S03):

> **CPU scheduling objective: keep the CPU busy as much as possible (i.e., using multiprogramming).**

Two facts worth carrying into the calculations:

* A process's **turnaround time** therefore contains *three* different kinds of time: its own CPU
  bursts, its own I/O waits, and the time it spends sitting in the ready queue. Only the last one is
  under the scheduler's control.
* The scheduler never changes how much CPU time a process needs. It only changes **when** it gets it.
  So every algorithm here produces the same total busy time; only the *distribution of waiting*
  differs.

### 1.2 The CPU scheduler (S05)

> **Goal: select one or more processes from the ready queue and allocate it to the CPU (one process
> per core).**

This is the **short-term scheduler** (the dispatcher's decision-maker). The deck deliberately limits
scope (S03): *"For simplicity, we focus on the concepts of short-term (ready queue) scheduler for
both uni- and multi-processor CPUs."* Long-term (job) and medium-term (swapping) scheduling are not
part of the calculation.

The scheduler gets to run **whenever a process changes state**. S05 lists five transitions from the
L2 state diagram and asks: for which of them is a scheduling decision **mandatory** — i.e. if
scheduling did *not* happen, one or more cores would be idle while work is waiting?

| # | Transition | Core becomes | Is a decision **required**? |
|---|---|---|---|
| 1 | running → terminated (**exit**) | free, and the queue may be non-empty | **yes** — the slide's answer |
| 2 | running → waiting (I/O or event wait) | free | no (but the core would idle if we don't) |
| 3 | running → ready (interrupt / preemption) | still busy with the preemptor | only by a *preemptive* scheduler |
| 4 | waiting → ready (event completes) | unchanged | only when a core happens to be idle |
| 5 | ready → running (**dispatch**) | taken | **yes** — the slide's answer |

The slide's printed answer is **"Only 1 and 5"**: the two transitions where the CPU *cannot* be kept
busy without a decision — a process leaving the CPU for good, and a queued process entering it.
Transitions 2, 3 and 4 create *opportunities*, not obligations.

> The arrow numbers come from the L2 process-state diagram. If your copy of the diagram numbers the
> arrows differently, the substance is unchanged: **exit and dispatch are mandatory; the others are
> optional and are what distinguish a preemptive scheduler from a nonpreemptive one.**

### 1.3 Preemptive vs nonpreemptive (S06)

| | **Nonpreemptive** | **Preemptive** |
|---|---|---|
| Definition | once the CPU is allocated, the process keeps it until it **voluntarily** releases it: **terminates** or **requests I/O / waits for an event** | the scheduler may take the CPU away **at any time** |
| Transitions that trigger it | 1 and 5 (and 4, when a core is idle) | 1, 5 **and also 2, 3, 4** — or any other instant |
| Analogy | the process owns the core | the OS owns the core and lends it |
| Examples | FCFS, nonpreemptive SJF, nonpreemptive priority | RR, SRTF, preemptive priority |
| Cost | none extra | context switches, timer interrupts, shared-data hazards |

Two consequences that exams like:

* **"Voluntary" is the test.** Requesting I/O is voluntary even though the process did not finish —
  it chose to block. Being interrupted by a timer is not voluntary.
* **A preemptive scheduler must be able to stop a process mid-burst**, which means it needs a
  hardware **timer interrupt**. Without one, the OS only regains control when the process calls into
  it (S18 notes call this "the timer interrupt in the process state transition diagram").

### 1.4 The five scheduling criteria (S07–S09)

Two are **system-wide** (about the machine), three are **per-process** (about one job). All five are
things we want to **maximise** (the first two) or **minimise** (the last three), and the last three
are reported as **averages across all processes** (S09).

| Criterion | Scope | Definition (slide wording) | Direction |
|---|---|---|---|
| **CPU utilisation** | system | percentage of time the cores are busy: (sum of execution time on each core) ÷ (total time × number of cores) | maximise |
| **Throughput** | system | number of processes completing per unit time — the number of "exit" transitions per unit time | maximise |
| **Turnaround time** | process | admitted → terminated: the whole lifetime | minimise |
| **Waiting time** | process | time spent in the **ready** state only | minimise |
| **Response time** | process | admitted → **first** time in the running state | minimise |

The single most useful line on S09 is the waiting-time decomposition:

> **waiting time = turnaround time − CPU bursts − I/O bursts − event wait**

Read it as: *turnaround is everything; subtract everything the process did on its own behalf; what is
left is the time it spent queued.* This is why `W = T − burst` works in all the deck's examples —
every one of them assumes a **single CPU burst and no I/O** (S10), so the two subtrahends collapse
into one.

```
  admitted                                                          terminated
     |                                                                   |
     v                                                                   v
     +--ready--+--RUNNING--+----WAITING (I/O)--+--ready--+--RUNNING--+---+
     |         |  burst 1  |    I/O burst      |         |  burst 2  |   |
     |<------->|<--------->|<----------------->|<------->|<--------->|   |
     |  W part1 |           |                   |  W part2 |           |   |
     |<--------------------- turnaround ------------------------------>|
     |<-->| response time (to the FIRST dispatch)

     W = T - burst1 - burst2 - (I/O burst)
```

**A numeric illustration** (not from the deck — constructed to exercise S09's formula):

| Event | Time |
|---|---|
| admitted (new → ready) | 0 |
| dispatched (ready → running), 1st time | 1 |
| 1st CPU burst ends, requests I/O | 5 |
| I/O completes (waiting → ready) | 10 |
| dispatched again, 2nd time | 12 |
| 2nd CPU burst ends, terminates | 16 |

* Turnaround = 16 − 0 = **16**
* CPU bursts = 4 + 4 = **8**; I/O = **5**
* Waiting = 16 − 8 − 5 = **3** — and by hand: 0–1 (1) plus 10–12 (2) = 3 ✓
* Response = 1 − 0 = **1** (only the *first* dispatch counts)

**CPU utilisation, worked.** Two cores, a 10 ms window; core 1 busy 8 ms, core 2 busy 6 ms.
Utilisation = (8 + 6) ÷ (10 × 2) = 14/20 = **70 %**. Note the denominator carries the core count —
forgetting it gives a nonsensical 140 %.

### 1.5 The assumptions used from S10 onwards

Every algorithm from S10 to S29 is evaluated under one deliberately narrow model (S10):

> *"We assume a single CPU burst for each process, a single CPU core and focus on the average waiting
> time."*

| Assumption | Consequence |
|---|---|
| **One CPU burst per process** | no I/O in the middle ⇒ `waiting = turnaround − burst`, and response time is just "first start − arrival" |
| **All burst lengths known in advance** | SJF is implementable in the exercise, even though reality needs prediction |
| **One core** (until S24) | one process runs at a time; the Gantt chart is a single row |
| **Metric = average waiting time** | unless the question names another one |
| **Processes arrive at known times** | needed for S15/S16, where arrival times are staggered |
| **Context-switch cost ignored** | switching is instantaneous; S20 is where the cost is discussed |

Burst lengths are **given**, not measured. That is the standard fiction of this chapter: it lets us
compute the optimum and compare real algorithms against it (S14: SJF is optimal).

---

## 2. First-Come, First-Served (S11–S13)

### 2.1 The rule

The ready queue is a **FIFO queue** (S11 notes). The process that arrived earliest runs next, and it
runs **to completion of its burst**. FCFS is **nonpreemptive** — the slide asks the question
directly and answers it: *"So is FCFS preemptive or nonpreemptive? Nonpreemptive."*

Mechanically, FCFS is a Gantt chart of back-to-back blocks in arrival order. The only subtlety is
that a process that arrives **while the CPU is busy** joins the tail of the queue, so its start time
is *not* its arrival time.

### 2.2 Worked example A — order P1, P2, P3 (S11)

| Process | CPU burst |
|---|---|
| P1 | 24 |
| P2 | 3 |
| P3 | 3 |

All three arrive at **t = 0**, in the order P1, P2, P3.

```
       0                24        27        30
       |                 |         |         |
       +--------P1-------+---P2----+---P3----+
       |      24         |    3    |    3    |
```

| Process | Arrival | Burst | Start | Completion | Turnaround `T` | Waiting `W = T − burst` |
|---|---|---|---|---|---|---|
| P1 | 0 | 24 | 0 | 24 | 24 | **0** |
| P2 | 0 | 3 | 24 | 27 | 27 | **24** |
| P3 | 0 | 3 | 27 | 30 | 30 | **27** |

Average waiting time = (0 + 24 + 27) / 3 = 51/3 = **17**  ← printed on S11 ✓
(Turnaround average = (24 + 27 + 30)/3 = **27**; response average = (0 + 24 + 27)/3 = **17**,
because in a nonpreemptive algorithm response = waiting.)

Look at the shape of the answer: P1 needed 24 units of CPU and waited 0; P2 and P3 needed 3 units
each and waited 24 and 27. **The short jobs paid for the long job.**

### 2.3 Worked example B — order P2, P3, P1 (S12)

Identical processes, identical arrival time (t = 0); only the **queue order** changes.

```
       0         3         6                          30
       |         |         |                           |
       +---P2----+---P3----+-----------P1--------------+
       |    3    |    3    |           24              |
```

| Process | Arrival | Burst | Start | Completion | `T` | `W` |
|---|---|---|---|---|---|---|
| P1 | 0 | 24 | 6 | 30 | 30 | **6** |
| P2 | 0 | 3 | 0 | 3 | 3 | **0** |
| P3 | 0 | 3 | 3 | 6 | 6 | **3** |

Average waiting = (6 + 0 + 3)/3 = 9/3 = **3**  ← printed on S12 ✓

The slide's comment: *"Much better than the previous case."* Same three processes, same total time
(30 units), average waiting time **17 → 3**. Nothing about the jobs changed; only their order in the
FIFO queue did.

> **Confidence check.** Both examples reproduce the printed averages exactly (17 and 3), and the
> turnaround sums match the end of the chart (30 in both cases). The Gantt blocks are therefore
> `P1|P2|P3` and `P2|P3|P1` — the only two orders that could produce those numbers.

### 2.4 The convoy effect (S13)

> **Main problem with FCFS is the convoy effect: short processes suffer increased waiting times due
> to an earlier-arrived long process.**

The metaphor is a convoy of vehicles stuck behind one slow truck: nobody can pass, so everybody's
journey time is the truck's journey time. In S11, P2 and P3 are the cars and P1 is the truck.

Three things to say in an answer: it is **caused by nonpreemption** (P1's 24 units are indivisible);
it **hurts short jobs disproportionately**, because waiting in FCFS is the sum of the bursts ahead of
you; and it **interacts with the CPU–I/O cycle** — a CPU-bound job holds the core while I/O-bound jobs
queue, then they all issue I/O at once and the CPU idles again. Hence the fix (§3): prioritise the
short burst.

**How to avoid it:** allow preemption (RR, SRTF), or reorder the queue by burst length (SJF).

---

## 3. Shortest-Job-First (S14–S16)

### 3.1 The rule

> **Prioritise processes based on their CPU burst lengths. Shorter burst implies higher priority.**

SJF is the direct answer to the convoy effect: if short jobs go first, they cannot be stuck behind a
long one (S14 notes: *"the short job should have a higher priority"*). The algorithm exists in two
variants, and the difference is the whole examinable content of the section:

| Variant | Rule | Preemptive? |
|---|---|---|
| **SJF (nonpreemptive)** | once the core is given to a process, it cannot be preempted until its CPU burst **completes** | no |
| **SRTF — Shortest Remaining-Time First** (preemptive SJF) | if a newly created process has a CPU burst **shorter than the remaining** burst of the running process, preempt and run the newcomer | yes |

Note the wording of the preemptive rule carefully (S14): the comparison is against the **remaining**
time of the runner, **not** against the runner's original burst. That single word is where most
marks are lost.

And the headline result:

> **SJF/SRTF is optimal for minimizing average waiting time.**

### 3.2 Worked example — nonpreemptive SJF (S15)

The deck reuses one arrival pattern for both variants:

| Process | Arrival time | Burst time |
|---|---|---|
| P1 | 0.0 | 7 |
| P2 | 2.0 | 4 |
| P3 | 4.0 | 1 |
| P4 | 5.0 | 4 |

Nonpreemptive means: **decisions happen only when a process finishes** (plus the initial choice).
Arrivals at t = 2, 4, 5 do not disturb the runner.

**Decision log**

| Event | Ready queue at that instant | Choice | Why |
|---|---|---|---|
| t = 0 | P1 | **P1** | only process in the system |
| t = 7 (P1 ends) | P2(4), P3(1), P4(4) | **P3** | shortest burst (1) |
| t = 8 (P3 ends) | P2(4), P4(4) | **P2** | tie on burst → **earlier arrival** wins (S15 notes) |
| t = 12 (P2 ends) | P4(4) | **P4** | last one left |

**Gantt chart**

```
       0       7  8        12        16
       |       |  |         |         |
       +--P1---+--+---P2----+---P4----+
       |   7   |P3|    4    |    4    |
       |       |1 |         |         |
```

**Metrics**

| Process | Arrival | Burst | Start | Completion | `T` | `W = T − burst` |
|---|---|---|---|---|---|---|
| P1 | 0 | 7 | 0 | 7 | 7 | **0** |
| P2 | 2 | 4 | 8 | 12 | 10 | **6** |
| P3 | 4 | 1 | 7 | 8 | 4 | **3** |
| P4 | 5 | 4 | 12 | 16 | 11 | **7** |

Average waiting time = (0 + 6 + 3 + 7)/4 = 16/4 = **4**  ← printed on S15 ✓
(Average turnaround = (7 + 10 + 4 + 11)/4 = 32/4 = **8.5**.)

> **Confidence check.** The printed average is 4 and my four waiting times sum to 16. The Gantt labels
> visible in the extracted text are `7`, `3`, `16`, `0`, `8`, `12` — which is exactly this chart read
> as (P1@0, P3@7, P2@8, P4@12, end@16) and the waiting times 0/6/3/7. Reconstruction confirmed.

**Notice what nonpreemption cost.** P3 has a burst of 1 and arrives at t = 4, but waits until t = 7
because P1 cannot be stopped: 3 units of pure waste. The preemptive variant fixes exactly this.

### 3.3 Worked example — preemptive SJF / SRTF (S16)

Same four processes, same arrivals. Now a decision is made at **every event**: an arrival or a
completion.

**Remaining-time table.** This is the bookkeeping that makes SRTF safe; build it before drawing.

| Time | Event | P1 rem | P2 rem | P3 rem | P4 rem | Runs next |
|---|---|---|---|---|---|---|
| 0 | P1 arrives, starts | 7 | – | – | – | **P1** |
| 2 | P2 arrives, burst 4 < P1's rem 5 → **preempt** | 5 | 4 | – | – | **P2** |
| 4 | P3 arrives, burst 1 < P2's rem 2 → **preempt** | 5 | 2 | 1 | – | **P3** |
| 5 | P3 ends; P4 arrives | 5 | 2 | 0 | 4 | **P2** (rem 2 < 4 < 5) |
| 7 | P2 ends | 5 | 0 | 0 | 4 | **P4** (4 < 5) |
| 11 | P4 ends | 5 | 0 | 0 | 0 | **P1** (only one left) |
| 16 | P1 ends | 0 | 0 | 0 | 0 | — |

**Gantt chart**

```
       0    2    4 5    7         11              16
       |    |    | |    |         |               |
       +-P1-+-P2-+-+P2-+---P4-----+------P1-------+
       | 2  | 2  |P3| 2 |    4    |      5        |
                  |1 |
```

**Metrics**

| Process | Arrival | Burst | Runs | Completion | `T` | `W` |
|---|---|---|---|---|---|---|
| P1 | 0 | 7 | 0–2, 11–16 | 16 | 16 | 16 − 7 = **9** |
| P2 | 2 | 4 | 2–4, 5–7 | 7 | 5 | 5 − 4 = **1** |
| P3 | 4 | 1 | 4–5 | 5 | 1 | 1 − 1 = **0** |
| P4 | 5 | 4 | 7–11 | 11 | 6 | 6 − 4 = **2** |

Average waiting time = (9 + 1 + 0 + 2)/4 = 12/4 = **3**  ← printed on S16 ✓
(Average turnaround = (16 + 5 + 1 + 6)/4 = 28/4 = **7**.)

> **Confidence check.** The printed average is 3 and the sum is 12. Cross-check P1 by hand: it runs
> 2 units, waits 2→11 = **9**, runs 5 more → 7 total burst ✓. The extracted labels `4`, `5`, `7`,
> `11`, `16`, `2` are exactly this chart's boundaries.

**What the preemption bought.** P3 now runs the moment it arrives (wait 0 instead of 3) and P2 is
split, but **P1's** waiting time explodes from 0 to 9 — it is preempted twice and pays for
everything. Average waiting falls 4 → 3, so the total is better, but the *distribution* is worse for
the longest job. That is the recurring theme of the whole chapter: minimising the average
deliberately sacrifices the unlucky.

### 3.4 Why SJF is optimal (the exchange argument)

You may be asked to justify the claim, not just quote it.

Take any schedule for a set of jobs that are *all available at the same time* and that runs with no
idle time. Suppose that somewhere a job **J** with burst `b_J` runs immediately before a job **S**
with burst `b_S`, where `b_S < b_J`. Swap those two blocks:

* **S** now starts `b_J` earlier → its waiting time drops by `b_J`.
* **J** now starts `b_S` earlier → its waiting time drops by `b_S` … but S moved *earlier*, so J
  actually moves **later** by `b_S` relative to its old position → its waiting time rises by `b_S`.
* Every other job is untouched.
* Net change in the **sum** of waiting times = `b_S − b_J < 0` — strictly better.

So no schedule containing a long-before-short inversion can be optimal, and the only schedule with no
such inversion is the one sorted by burst length: **SJF**. Two hooks:

* The argument is about the **sum** (= the average, since `n` is fixed), never about any single
  process. SJF minimises the average and can be terrible for one long job (§3.6).
* It assumes jobs are **available**; with future arrivals the greedy choice at each decision point
  gives **SRTF**, optimal among *preemptive* algorithms for the same exchange reason applied to
  remaining times.

Also note the corollary used in practice: the gain comes from putting the **shortest** job first, so
SJF is only as good as your **burst-length knowledge**. In the exercises bursts are given; in a real
system they must be predicted from history (exponential averaging), and a wrong prediction degrades
the schedule — sometimes below FCFS.

### 3.5 Tie-breaking (S15 notes — this is a real mark)

> *"P2 and P4 have the same CPU burst time. How to break the tie? We choose the one with the earliest
> arrival time when two processes have the same CPU burst length. **However, note tie can be broken
> using any strategy. The optimality of SJF w.r.t average waiting time will still hold, irrespective
> of the tie breaking strategy.**"*

| Situation | What to do | Why |
|---|---|---|
| Equal bursts, nonpreemptive | earlier **arrival** first (deck's rule) — or any rule, **announced** | the exchange argument never needed a strict `<` |
| Equal **remaining** times in SRTF | any rule; state it | same argument |
| New arrival exactly equal to the runner's remaining time | **no** preemption (`shorter than`, not `shorter than or equal`) | S14 wording: "less than the remaining CPU burst" |

In an exam, one line — *"ties broken by arrival order; the average is unaffected"* — protects the
whole calculation.

### 3.6 The cost side of SJF

| Problem | Explanation |
|---|---|
| **Burst length is not knowable** | the OS knows a process's future only by predicting it; every prediction is a guess |
| **Starvation of long jobs** | if short jobs keep arriving, a long job is never the shortest → it may never run. Nonpreemptive SJF starves it too, just more slowly |
| **Unfair in the tail** | by construction it optimises the *sum*, so it is indifferent to one job waiting forever |

Starvation is not unique to SJF; §4 gives it its name and its cure (**aging**).

**SJF properties**

| Property | Value |
|---|---|
| Preemptive? | nonpreemptive by default; **SRTF** is the preemptive form |
| Average waiting | **optimal** (both variants) |
| Starvation? | **yes** — long jobs |
| Needs | burst lengths in advance |
| Used in | long-term / batch scheduling, where bursts can be estimated; not in interactive systems as-is |

---

## 4. Priority-based Scheduling (S17)

### 4.1 The rule

> A **priority number** (integer) is associated with each process. The CPU is allocated to the process
> with the **highest priority**. Usually, **smallest integer = highest priority**.

The deck's framing is worth copying: **FCFS and SJF are both priority scheduling in disguise.**

| Algorithm | What plays the role of "priority" |
|---|---|
| **FCFS** | **arrival order** — earlier arrival = higher priority |
| **SJF** | **CPU burst length** — shorter burst = higher priority |
| **Priority scheduling** | an **arbitrary number** attached to the process |

That is why priority scheduling inherits both variants: it can be **preemptive** or
**nonpreemptive**, according to whether a newly arriving higher-priority process takes the CPU away
from a running lower-priority one.

The speaker notes add the concrete range used in Linux: **`[-20, +20]`**, where `-20` is the highest
priority and `+20` the lowest. (Note the trap: the *numerically smaller* value is the *more* urgent
one.)

### 4.2 Worked example

Three processes, all at t = 0, **smaller integer = higher priority**, nonpreemptive:

| Process | Priority | Burst |
|---|---|---|
| P1 | 3 | 4 |
| P2 | 1 | 6 |
| P3 | 4 | 2 |

**Decision log:** at t = 0 all three are ready → highest priority (smallest number) is P2 (1), then
P1 (3), then P3 (4). Nonpreemptive, so the order is fixed once chosen, and no later arrival can
interrupt.

```
       0              6          10     12
       |              |          |      |
       +------P2------+---P1-----+--P3--+
       |      6       |    4     |  2   |
```

| Process | Priority | Burst | Start | Completion | `T` | `W` |
|---|---|---|---|---|---|---|
| P1 | 3 | 4 | 6 | 10 | 10 | **6** |
| P2 | 1 | 6 | 0 | 6 | 6 | **0** |
| P3 | 4 | 2 | 10 | 12 | 12 | **10** |

Average waiting = (6 + 0 + 10)/3 = 16/3 ≈ **5.33**. Average turnaround = (10 + 6 + 12)/3 ≈ **9.33**.

Compare with SJF on the same data (order by burst: P3 2, P1 4, P2 6):
waits = 0 (P3), 2 (P1: starts 2), 6 (P2: starts 6) → average **8/3 ≈ 2.67**. Priority scheduling is
*worse* than SJF here because priority and burst length point in opposite directions — and that is
the honest comparison to make when a question asks "why not just use priorities?".

### 4.3 Starvation and aging

> **Problem — starvation:** lower-priority processes may never execute in a heavily loaded system.
> **Solution — aging:** as time progresses, slowly **increase the priority** of processes that are not
> able to execute.

Starvation is not randomness, and it is not a bug — it is the algorithm working as specified. If a
priority-1 process arrives every 2 ms while a priority-4 process needs 5 ms, the queue is never
empty of priority-1 work, so the priority-4 process waits forever. **Aging** fixes it by making
waiting itself improve your priority: after enough time at the back, a low-priority process becomes
the highest-priority one and finally runs.

Two details that earn marks:

* Aging **destroys the strict priority ordering**. That is the point: you trade a little
  "importance" for bounded waiting. An exam answer should say so rather than pretend pure priority
  survives.
* Aging is the standard cure for **every** starvation-prone scheduler in this chapter: priority
  scheduling (§4), multilevel queue with fixed priority (§6), and (in principle) SJF.

---

## 5. Round Robin (S18–S21)

### 5.1 The rule

> **Fixed time quantum `q`:** a process is allocated the CPU for `q` time units, **preempted
> thereafter and inserted at the end of the ready queue**. Processes are scheduled cyclically.

RR is the first algorithm in the deck designed for **fairness** rather than for the average
(S18 notes: *"Now we look at a fair scheduling algorithm"*). Mechanism:

1. Take the process at the **head** of the ready queue.
2. Run it for at most `q` units (or until it blocks/terminates).
3. If it is not finished, put it at the **tail**.
4. Repeat.

| Parameter / property | Value (S18) |
|---|---|
| Quantum `q` | "usually small, around **10–100 ms**" |
| Preemptive? | **yes** — the CPU is forcibly taken at the end of the quantum (needs a timer interrupt) |
| Waiting-time bound | with `n` processes in the ready queue, waiting is **no more than `(n − 1)q`** |
| Large `q` | degenerates to **FCFS** |
| Small `q` | many **context switches**, high overhead |
| Starvation? | **no** — every process returns to the head within one round |

The `(n − 1)q` bound is easy to see: in the worst case you just missed your turn, and you must wait
for each of the other `n − 1` processes to consume one quantum before you run again. It is a **safe
upper bound for waiting**, not a formula for the actual waiting time and **not** a turnaround bound —
a distinction worth stating explicitly (see §13 traps).

### 5.2 Worked example — RR with q = 20 (S19)

| Process | Burst |
|---|---|
| P1 | 53 |
| P2 | 17 |
| P3 | 68 |
| P4 | 24 |

All processes arrive at **t = 0**, in the order P1, P2, P3, P4.

The whole example is bookkeeping. Track the queue and the **remaining burst** after every slice:

| Slice | Runs | Interval | Remaining after the slice | Queue after the slice |
|---|---|---|---|---|
| 1 | P1 | 0–20 | P1 = 33 | P2, P3, P4, P1 |
| 2 | P2 | 20–37 | P2 = **0** (finished early, 17 < q) | P3, P4, P1 |
| 3 | P3 | 37–57 | P3 = 48 | P4, P1, P3 |
| 4 | P4 | 57–77 | P4 = 4 | P1, P3, P4 |
| 5 | P1 | 77–97 | P1 = 13 | P3, P4, P1 |
| 6 | P3 | 97–117 | P3 = 28 | P4, P1, P3 |
| 7 | P4 | 117–121 | P4 = **0** (only 4 left) | P1, P3 |
| 8 | P1 | 121–134 | P1 = **0** (13 left) | P3 |
| 9 | P3 | 134–154 | P3 = 8 | P3 |
| 10 | P3 | 154–162 | P3 = **0** | — |

**Gantt chart**

```
       0        20    37       57       77       97      117 121   134   154  162
       |         |     |        |        |        |        |   |     |     |    |
       +---P1----+--P2-+---P3---+---P4---+---P1---+---P3---+P4-+-P1--+--P3-+--P3+
       |   20    | 17  |   20   |   20   |   20   |   20   | 4 | 13  | 20  | 8  |
```

Two quirks of RR are visible in that chart and both are examinable:

* **Slice 2 is short.** P2 needs only 17 of its 20 units. The core does not idle for the remaining 3;
  P3 starts immediately at 37.
* **P3 runs last twice in a row** (slices 9 and 10): at 134 the queue contains only P3, so it simply
  keeps going in a fresh quantum.

**Metrics**

| Process | Arrival | Burst | Completion | `T = comp − arr` | `W = T − burst` | Response (first start) |
|---|---|---|---|---|---|---|
| P1 | 0 | 53 | 134 | 134 | **81** | 0 |
| P2 | 0 | 17 | 37 | 37 | **20** | 20 |
| P3 | 0 | 68 | 162 | 162 | **94** | 37 |
| P4 | 0 | 24 | 121 | 121 | **97** | 57 |

Average waiting = (81 + 20 + 94 + 97)/4 = 292/4 = **73**
Average turnaround = (134 + 37 + 162 + 121)/4 = 454/4 = **113.5**
Average response = (0 + 20 + 37 + 57)/4 = 114/4 = **28.5**

Cross-check P3's waiting by hand, because it is the one people get wrong: it waits 0→37 (37), then
57→97 after its first preemption (40), then 117→134 (17). Total 37 + 40 + 17 = **94** ✓.

> **Confidence check.** The reconstruction produces `P1 0–20, P2 20–37, P3 37–57, P4 57–77, P1 77–97,
> P3 97–117, P4 117–121, P1 121–134, P3 134–154, P3 154–162`. Every number visible in the extracted
> slide text (0, 20, 37, 57, 77, 117, 121, 134, 154, 162 and the remainders 33, 48, 4, 13, 28) appears
> in that list, and the total run time 162 equals the sum of the bursts (53 + 17 + 68 + 24 = 162) ✓.

### 5.3 What S19's notes ask you to do

> *"[NOTES] What is the response time for P1? 0. P2? 20 …"*

Read response times straight off the **first** occurrence of each process in the chart:
**P1 = 0, P2 = 20, P3 = 37, P4 = 57.** Average **28.5**. Do not confuse this with waiting time: P2's
response is 20 and its waiting is also 20 (it was never preempted), while P3's response is 37 but its
waiting is 94 (it was preempted twice more).

And the summary line on S19:

> **"Typically, higher average waiting/turnaround time than SJF, but better response time."**

That is the trade RR makes: it deliberately interrupts jobs so that nobody waits long *for a first
turn*. SJF gives the best average but can make the last job wait a very long time before it ever
starts.

### 5.4 Quantum size and context-switch overhead (S20)

> **Smaller time quantum increases context switches.**

S20 uses one process with a **CPU burst of 10 units**:

| Quantum `q` | Slices needed | Context switches **during** the burst | Arithmetic |
|---|---|---|---|
| 12 | 1 | **0** | the burst fits inside one quantum |
| 6 | 2 | **1** | 6 + 6 (2nd slice is 4 units) → one preemption in the middle |
| 1 | 10 | **9** | 1 × 10 → nine preemptions before it finishes |

The general formula for one process running alone:

```
context switches during a burst B = ceil(B / q) − 1
```

Why `− 1`: the final slice ends because the process **finished**, not because the timer fired. There
is no preemption after the last unit of work. (If the same process has more work, then the count is
`ceil(B/q) − 1` plus whatever the rest of its execution needs.)

**Costing it out.** With `q = 10 ms` and a switch cost of `0.5 ms`, each round costs `10.5 ms` of
wall time for 10 ms of work → overhead `0.5/10.5 ≈ 4.8 %`. At `q = 5 ms` it is `0.5/5.5 ≈ 9.1 %`; at
`q = 1 ms` it is `0.5/1.5 ≈ 33 %` — a third of the machine spent switching. That is the argument for
"not too small". The opposing pressure is that a **very large** quantum makes RR behave like FCFS
again, so a short interactive job waits behind everything. The quantum is the dial between
**responsiveness** and **overhead**; no single value is optimal in general.

### 5.5 Turnaround time vs quantum size (S21)

> **"No well-defined relationship between average turnaround time and quantum size."**
> **"Average turnaround time remains fixed once quantum size is larger than maximum CPU burst length."**

Two claims, and the second explains the first's limit case:

1. **No monotone relationship.** It is tempting to think "smaller quantum = fairer = better
   turnaround". It is false. As `q` grows, average turnaround can go **up or down** at different
   steps; the curve is jagged. The only thing you may state with confidence is the limiting
   behaviour.
2. **Plateau.** Once `q ≥ max burst`, no process is ever preempted, so every process runs exactly once
   — that is precisely **FCFS**. Hence the average turnaround becomes constant and equals the FCFS
   average.

The speaker notes give the plateau value for the deck's figure:

> `FCFS = (6 + 9 + 10 + 17)/4 = 10.5`, assuming arrival order P1, P2, P3, P4.

Those four numbers are **turnaround times**, and in FCFS with all processes arriving at t = 0 the
turnaround times are the running totals of the bursts: 6, 6 + 3 = 9, 9 + 1 = 10, 10 + 7 = 17. So the
process set behind the figure is **bursts 6, 3, 1, 7** for P1…P4. (The figure itself is an image and
is not captured by the text extraction; the arithmetic above is what pins the data down.)

**Reconstruction of the figure's curve** — average turnaround of that set as `q` varies, simulated
with the same RR rules as §5.2:

| `q` | Turnaround P1/P2/P3/P4 | Average |
|---|---|---|
| 1 | 15 / 9 / 3 / 17 | 11.00 |
| 2 | 14 / 10 / 5 / 17 | 11.50 |
| 3 | 13 / 6 / 7 / 17 | 10.75 |
| 4 | 14 / 7 / 8 / 17 | 11.50 |
| 5 | 15 / 8 / 9 / 17 | 12.25 |
| 6 | 6 / 9 / 10 / 17 | **10.50** |
| ≥ 7 | 6 / 9 / 10 / 17 | **10.50** |

Read the middle of that table: going from `q = 1` to `q = 2` makes the average **worse** (11.00 →
11.50), then better, then worse and much worse (12.25 at `q = 5`, worse than FCFS), and finally it
**snaps to the FCFS value** 10.50 and stays there. That non-monotone wander is exactly the "no
well-defined relationship" claim, and the snap is the plateau. In this data set the plateau starts at
`q = 6` simply because the arrival order already equals the FCFS order; the *guarantee* is only from
`q ≥ max burst = 7`.

**Exam-safe statements about quantum size:**

* Smaller `q` → better **response**, worse **overhead** (pathological once `q` approaches the switch
  cost); `q ≥ max burst` → identical to **FCFS**.
* Average **turnaround** does **not** decrease monotonically with `q`.
* Typical choice **10–100 ms** (S18): comfortably above a switch, small enough to feel interactive.

---

## 6. Multilevel Queue Scheduling (S22–S23)

### 6.1 The problem

Every algorithm so far assumes **one** ready queue and **one** policy — but different processes want
different things (S22):

| Process class | Example | Wants | Preferred algorithm |
|---|---|---|---|
| **Foreground** (interactive) | keystrokes, mouse, a game | low **response** time | **RR** |
| **Background** (batch) | virus scan, compilation, backups | throughput, not interactivity | **FCFS** (less overhead) |

Running RR over everything wastes switches on batch jobs; running FCFS over everything ruins
interactivity. The deck's answer (S22):

> **The ready queue is partitioned into several queues; each queue has its own scheduling algorithm.**
> Then you must answer: **how do you schedule *among* the queues?**

```
   queue 1  system processes          highest priority
   queue 2  interactive / foreground   RR, small q     <- S22: I/O-bound
   queue 3  interactive / background   RR, large q
   queue 4  batch / background         FCFS            <- S22: CPU-bound
   queue 5  student jobs               lowest priority

   scheduling WITHIN a queue = that queue's own algorithm
   scheduling AMONG queues   = the inter-queue policy (S23)
```

The deck draws the minimal two-queue version: **foreground (RR)** and **background (FCFS)**, with
foreground possibly having higher priority as well.

### 6.2 The two inter-queue policies (S23)

**(a) Fixed priority scheduling**

> Queues are served in priority order (e.g. foreground before background).

Serve every process in the foreground queue first; only when the foreground queue is *empty* does the
background queue get the CPU.

* **Advantage:** simple, and gives foreground work the machine immediately.
* **Fatal flaw:** **starvation for lower-priority queues.** A steady trickle of interactive work
  keeps the background queue empty of service forever.
* **Cure (S23 notes):** **aging** — as in §4, gradually raise the priority of starved processes until
  they migrate in effect to a servable queue.

**(b) Time-slice based scheduling**

> Each queue gets a **fixed time quantum on the CPU** — e.g. **80 ms for foreground, 20 ms for
> background, and then repeat**.

CPU time is divided **between queues by percentage**: foreground 80 %, background 20 %, and within
each share the queue's own algorithm decides who runs.

* **Advantage:** **no starvation** — every queue is guaranteed its share by construction.
* **Cost:** the split is **static**; an idle queue wastes its share, and 20 % is a *ceiling*.

### 6.3 Comparing the two policies

| | Fixed priority | Time slice |
|---|---|---|
| Allocation | winner takes all, in priority order | fixed percentage per queue |
| Starvation | **yes** (low queues) | no |
| Needs aging? | yes | no |
| Responsiveness of the top queue | best possible | good, but capped at its share |
| Throughput of low queues | zero in the worst case | guaranteed minimum |
| Complexity | trivial | slightly more (needs per-queue accounting) |

### 6.4 What is *not* here

The queues in S22–S23 are **static**: a process is assigned to a queue when it is created and stays
there. The variant where processes **migrate** between queues (multilevel **feedback** queue) is not
on these slides — do not import it into an answer about this deck, though you may mention it as an
extension if the question invites it.

---

## 7. Multiprocessor Scheduling (S24–S30)

### 7.1 The model (S24)

> **Assumption: a multi-core CPU, and each process may only execute on one CPU core at any time
> instant.**

That single line is important. There is **no parallelism inside a process** in this chapter — a
process is a single sequential instruction stream.

| Consequence | Meaning |
|---|---|
| One process on at most one core **at a time** | two cores run two *different* processes |
| One process on different cores **at different times** | migration is allowed (and is what makes SMP expensive, S30) |
| Total work unchanged | `Σ burst_i` is the same; only the overlap is new |

The deck then names the two families (S24):

| Family | Also called | Core idea |
|---|---|---|
| **Partitioned scheduling** | **AMP** — *Asymmetric Multiprocessing* | processes are **pinned** to cores in advance; each core runs its own uniprocessor algorithm |
| **Global scheduling** | **SMP** — *Symmetric Multiprocessing* | **one** set of ready queues for the whole system; any idle core takes the next process |

### 7.2 Partitioned scheduling (AMP) — S25

> Processes are partitioned **a priori** (at process creation time) among CPU cores; each process is
> mapped to one core; **separate uniprocessor CPU scheduling for each core**.

**Advantages** (S25):

* **Core-specific strategy is feasible** — core 1 can run RR for interactive work while core 2 runs
  FCFS for batch work.
* **Easy and simple extension** of uniprocessor scheduling: nothing new to design, the algorithms of
  §2–§6 are reused verbatim, once per core.
* No shared ready-queue data structure → no contention on the scheduler itself.

**The problem it inherits** — mapping is fixed, so a bad map is permanent (S26):

| Issue | Detail |
|---|---|
| **How to map processes to cores?** | done once, at creation; nothing rebalances later |
| **Poor mapping ⇒ unequal loads** | one core idles while another is overloaded; the overloaded core's queue only grows |
| **Performance impact** | worse turnaround, worse throughput, idle cores — a system-wide loss for a local decision |
| **Complexity** | optimal assignment is **NP-hard**, *"similar to the well-known knapsack problem"* (S26) |
| **Practical fix** | **heuristics** such as **best-fit**, *if* CPU burst lengths are known |

Why it is like a knapsack: you are distributing items (processes) of given sizes (bursts) into a
fixed number of bins (cores) so that the heaviest bin is as light as possible — bin-packing, whose
optimisation version contains knapsack. The deck's honest conclusion is that **optimality is
unattainable in general** and load balancing must be heuristic.

### 7.3 Global scheduling (SMP) — S27

> **One or more ready queues for the entire system** (no mapping of queues to CPU cores). When **any**
> core becomes idle, the CPU scheduler runs and allocates the next process to execute. Process
> selection uses the strategy applied **globally / symmetrically** across all cores.

Properties to quote:

* **No core–process mapping problem.** Any core can take any process, so idle cores always find work
  if work exists.
* **A process may run on different cores at different times** (S27) — after a preemption it can be
  dispatched elsewhere.
* **FCFS on a dual-core system** (S27 notes) = one global queue; *"at any point in time, the two
  earliest arrived processes that are ready to execute will be executing on the two CPU cores."* That
  sentence is the whole trick to the dual-core examples: **the k shortest/earliest ready processes
  run simultaneously, where k = number of cores.**

### 7.4 Worked example — SRTF on two cores (S28)

Same four processes as §3.2/§3.3:

| Process | Arrival | Burst |
|---|---|---|
| P1 | 0.0 | 7 |
| P2 | 2.0 | 4 |
| P3 | 4.0 | 1 |
| P4 | 5.0 | 4 |

Two cores, SRTF applied **globally**: at every event, the ready processes with the **shortest
remaining times** occupy the cores, up to two of them.

**Event log**

| Time | Event | Ready / running (remaining) | Action |
|---|---|---|---|
| 0 | P1 arrives | P1(7) | core 1 takes P1; **core 2 idles** (nothing else exists) |
| 2 | P2 arrives | P1(5) running, P2(4) | core 2 takes **P2** — no need to preempt, a core was free |
| 4 | P3 arrives | P1(3), P2(2), P3(1) | the two smallest are P3(1) and P2(2) → **P3 preempts P1** (the longest remaining) |
| 5 | P3 ends; P4 arrives | P1(3), P2(2), P4(4) | core 1 takes **P1** (3 is smallest), core 2 keeps P2 |
| 6 | P2 ends | P1(2), P4(4) | core 2 takes **P4** |
| 8 | P1 ends | P4(2) | core 1 idle |
| 10 | P4 ends | — | done |

**Gantt chart (two rows)**

| Core | 0–2 | 2–4 | 4–5 | 5–6 | 6–8 | 8–10 |
|---|---|---|---|---|---|---|
| **Core 1** | **P1** | P1 | **P3** | **P1** | **P1** | idle |
| **Core 2** | idle | **P2** | **P2** | **P2** | **P4** | **P4** |

**Metrics**

| Process | Arrival | Burst | Completion | `T` | `W = T − burst` | Response |
|---|---|---|---|---|---|---|
| P1 | 0 | 7 | 8 | 8 | **1** | 0 |
| P2 | 2 | 4 | 6 | 4 | **0** | 0 |
| P3 | 4 | 1 | 5 | 1 | **0** | 0 |
| P4 | 5 | 4 | 10 | 5 | **1** | 1 |

Average waiting = (1 + 0 + 0 + 1)/4 = **0.5**  ← printed on S28 ✓
(Average turnaround = (8 + 4 + 1 + 5)/4 = 4.5; average response = (0 + 0 + 0 + 1)/4 = 0.25.)

> **Confidence check.** The printed average is 0.5 and the sum of my four waiting times is exactly 2.
> The labels visible in the extracted text — `0`, `2`, `4`, `5`, `6`, `8`, `10` and the remainder `3`
> — are all boundaries of this chart (the `3` is P1's remaining time at t = 4, which is *why* it was
> the one preempted).
>
> **Why P1 was preempted at t = 4, not P2.** Both were runnable (P1 rem 3, P2 rem 2) and only one
> core was needed for the newcomer P3(1). Global SRTF keeps the two smallest remaining times, so
> P2(2) and P3(1) stay and **P1(3) — the largest — goes back to the queue**. Preempting P2 instead
> would produce a different, worse schedule; check any answer against "the two smallest run".

### 7.5 Worked example — RR with q = 20 on two cores (S29)

Same four processes as §5.2: P1 = 53, P2 = 17, P3 = 68, P4 = 24, all at t = 0, arrival order
P1, P2, P3, P4. One global queue, two cores.

**Slice log** (each core takes the head of the queue when it frees up; a finished slice goes to the
**tail**)

| # | Core 1 | Core 2 | Queue after |
|---|---|---|---|
| 1 | **P1 0–20** (rem 33) | **P2 0–17** (done) | P3, P4, P1 |
| 2 | **P4 20–40** (rem 4) | **P3 17–37** (rem 48) | P1, P3, P4 |
| 3 | **P3 40–60** (rem 28) | **P1 37–57** (rem 13) | P4, P1, P3 |
| 4 | **P1 60–73** (done) | **P4 57–61** (done) | P3 |
| 5 | idle 73–81 | **P3 61–81** (rem 8) | P3 |
| 6 | **P3 81–89** (done) | idle | — |

**Gantt chart (two rows)**

| Core | 0–20 | 20–40 | 40–60 | 60–73 | 73–81 | 81–89 |
|---|---|---|---|---|---|---|
| **Core 1** | **P1** | **P4** | **P3** | **P1** | idle | **P3** |
| **Core 2** | **P2** (0–17) | **P3** (17–37) | **P1** (37–57) | **P4** (57–61) | **P3** (61–81) | — |

**Metrics**

| Process | Burst | Completion | `T` | `W = T − burst` | Response |
|---|---|---|---|---|---|
| P1 | 53 | 73 | 73 | **20** | 0 |
| P2 | 17 | 17 | 17 | **0** | 0 |
| P3 | 68 | 89 | 89 | **21** | 17 |
| P4 | 24 | 61 | 61 | **37** | 20 |

Average waiting = (20 + 0 + 21 + 37)/4 = 78/4 = **19.5**
Average turnaround = (73 + 17 + 89 + 61)/4 = 240/4 = **60**
Average response = (0 + 0 + 17 + 20)/4 = 37/4 = **9.25**

> **Confidence check.** Total work is 162 units over 2 cores → the schedule cannot finish before 81;
> it finishes at 89, i.e. the cores are busy `162/178 ≈ 91 %` of the wall time (the gap is core 1
> idling 73–81). The extracted labels `17`, `37`, `40`, `57`, `60`, `61`, `73`, `89` and the
> remainders `33`, `48`, `4`, `13`, `28` all appear in the slice log ✓.
>
> **Why P3 runs on core 1 at 81–89.** At t = 81 its quantum on core 2 expires with 8 units left; the
> queue has only P3, so it is re-queued and immediately re-dispatched — on the core that happens to be
> free. This is the SMP property "the same process may execute on different cores at different times"
> (S27/S30) happening for real.

### 7.6 One core vs two cores — the numbers side by side

| Example | One core | Two cores | What improved |
|---|---|---|---|
| **SRTF**, S16 vs S28 | avg waiting **3** | avg waiting **0.5** | both metrics, because two processes run truly in parallel |
| **RR q = 20**, S19 vs S29 | avg waiting **73**, avg turnaround **113.5**, avg response **28.5** | avg waiting **19.5**, avg turnaround **60**, avg response **9.25** | all three, roughly 3–4× |

Two lessons: **do not divide by the number of cores** (concurrency changes *which* processes overlap,
so the chart must be rebuilt), and **cores help only when the queue is long** — S28's core 2 idled
0–2 because only P1 existed, so speed-up is bounded by available parallelism.

### 7.7 The price of global scheduling (S30)

> Implementation complexity is high compared to partitioned scheduling.

| Cost | Why (S30 notes) |
|---|---|
| **Clock synchronisation** | *"The scheduler must use a single clock so that the cores can be synchronized. Notion of time is global across all cores."* Two cores with drifting timers would disagree about whose quantum expired first |
| **Global selection overhead** | when several cores go idle at once, one scheduler pass must scan the queue repeatedly — *"going through several processes in the ready queue"* — and the cores may contend on the same queue |
| **Cache migration** | a process that moves cores loses its **private cache**; its data must be migrated, or it starts with a **cold cache**, which *"can significantly increase its execution time"* — so the scheduler's "no mapping problem" is paid for in memory behaviour |
| **Implicit cost of preemption** | every quantum boundary can now move a process to a different core, making the cache issue frequent |

**AMP vs SMP summary**

| | **Partitioned (AMP)** | **Global (SMP)** |
|---|---|---|
| Ready queues | one per core | one (or a few) system-wide |
| Mapping | fixed at creation | none — dynamic |
| Load balance | poor unless mapped well | naturally good |
| Per-core algorithm | **yes**, different per core | one global policy |
| Migration | never | possible at every dispatch |
| Implementation | simple | complex (clocks, contention, caches) |
| Mapping problem | **NP-hard** (knapsack-like), best-fit heuristic | does not exist |

---

## 8. Putting it all together

### 8.1 The comparison matrix (memorise the columns)

| Algorithm | Preemptive | Starvation | Avg waiting | Response | Overhead | Needs |
|---|---|---|---|---|---|---|
| **FCFS** | no | convoy effect | order-dependent | poor | minimal | nothing |
| **SJF** | no | yes (long jobs) | **optimal** | poor | low | burst lengths |
| **SRTF** | **yes** | yes (long jobs) | **optimal** | good | switches | burst lengths |
| **Priority** | either | **yes** → aging | priority-dependent | depends | low | priorities |
| **RR** | **yes** | no | higher than SJF | **best** | `q` switches | a timer, `q` |
| **Multilevel queue** | either | yes (fixed priority) | depends | good for foreground | moderate | classification + inter-queue policy |

### 8.2 Which algorithm is this? (the giveaway phrases)

| If the question says… | It is |
|---|---|
| "arrive in the order", "FIFO queue" | **FCFS** |
| "shortest burst", "once allocated it runs to completion" | **SJF** (nonpreemptive) |
| "newly arrived process has a shorter remaining time", "preempt" | **SRTF** |
| "higher priority number", "smallest integer = highest" | **priority** |
| "aging", "raise priority over time" | **priority** (or multilevel, fixed priority) |
| "time quantum", "inserted at the end of the ready queue" | **RR** |
| "foreground / background", "queue per class" | **multilevel queue** |
| "pinned to a core", "partitioned", "asymmetric" | **AMP** |
| "one global ready queue", "any idle core", "symmetric" | **SMP** |

---

## 9. Formula sheet

```
turnaround          T_i = completion_i − arrival_i
waiting             W_i = T_i − Σ CPU bursts − Σ I/O waits
                        = T_i − burst_i           (single burst, no I/O — the deck's assumption)
response            R_i = first_dispatch_i − arrival_i

average metric      = (Σ value_i) / n              n = number of processes
CPU utilisation     = Σ(exec time per core) / (total time × number of cores)
throughput          = number of exits / unit time

FCFS waiting        W_i = Σ bursts of all processes ahead of i  (for arrivals at t = 0)
SJF/SRTF            picks min burst / min remaining → optimal average waiting
SRTF preemption     when new_burst < remaining_of_runner
Priority             smallest integer = highest priority; aging raises starved priorities
RR                  slice = min(q, remaining); unfinished → tail; finished → out
RR waiting bound    W ≤ (n − 1) × q                (n processes in the ready queue)
RR context switches ceil(B / q) − 1                (one process, burst B, alone)
RR plateau          q ≥ max burst  ⇒  RR ≡ FCFS  ⇒  average turnaround constant
```

---

## 10. Practice problems

Attempt these on paper before reading §10.1. Every one is doable in the deck's model (single burst,
no I/O, bursts known).

**P1.** Processes arrive as below. Compute the average waiting time under **FCFS**.

| Process | Arrival | Burst |
|---|---|---|
| P1 | 0 | 8 |
| P2 | 1 | 4 |
| P3 | 2 | 9 |
| P4 | 3 | 5 |

**P2.** Same four processes. Compute the average waiting time under **(a) nonpreemptive SJF** and
**(b) SRTF**. Which is better, and by how much?

**P3.** P1 = 5, P2 = 4, P3 = 2, all arriving at t = 0. Run **RR with q = 2**. Give the Gantt chart,
the average waiting time, the response time of each process, and the number of context switches
during execution.

**P4.** **Preemptive** priority scheduling, smallest integer = highest priority:

| Process | Arrival | Burst | Priority |
|---|---|---|---|
| P1 | 0 | 5 | 2 |
| P2 | 1 | 3 | 1 |
| P3 | 2 | 2 | 3 |

Draw the chart and compute the average waiting time.

**P5.** The S15/S16 process set (P1 0/7, P2 2/4, P3 4/1, P4 5/4) on **two cores** with
**nonpreemptive SJF**. Compute the average waiting time and compare it with the one-core answer.

**P6.** P1 arrives at 0 with burst 5; P2 and P3 both arrive at 5 with burst 5 each. Nonpreemptive
SJF is used. Show that the two tie-break choices give the **same** average waiting time.

**P7.** A process has a CPU burst of **30** units. The quantum is **4** and a context switch costs
**1** unit. How many switches occur during the burst, and what fraction of wall-clock time is spent
switching?

**P8.** Answer briefly:
(a) For which of the five process-state transitions is a scheduling decision mandatory, and why?
(b) Which algorithm minimises average waiting time, and which minimises average response time?
(c) "Average turnaround time decreases as the quantum decreases." True or false?

### 10.1 Solutions

**S1 — FCFS.** Chart `P1 0–8 · P2 8–12 · P3 12–21 · P4 21–26`.
Waits: P1 = 0; P2 = 8 − 1 = **7**; P3 = 12 − 2 = **10**; P4 = 21 − 3 = **18**.
Average = 35/4 = **8.75**. (Shortcut: waiting = bursts ahead − arrival offset, so
P4 = (8 + 4 + 9) − 3 = 18 ✓.)

**S2 — (a) nonpreemptive SJF.** Only P1 exists at t = 0 → 0–8. Then shortest first from {P2 4, P3 9,
P4 5}: `P2 8–12 · P4 12–17 · P3 17–26`. Waits 0 / 7 / **9** / **15** → average 31/4 = **7.75**.

**(b) SRTF.** Events: t = 1 P2(4) preempts P1(7 rem); t = 2 P3(9) no; t = 3 P4(5) no (P2 has 2 left);
t = 5 P2 done → P4; t = 10 → P1; t = 17 → P3. Chart
`P1 0–1 · P2 1–5 · P4 5–10 · P1 10–17 · P3 17–26`.
Waits: P1 = 17 − 8 = **9**; P2 = **0** (finishes at 5, arrived 1); P3 = 24 − 9 = **15**;
P4 = 7 − 5 = **2** → average 26/4 = **6.5**. Beats nonpreemptive SJF by **1.25** and FCFS by **2.25**.

**S3 — RR q = 2.** `P1 0–2 · P2 2–4 · P3 4–6 · P1 6–8 · P2 8–10 · P1 10–11`.
Waits: P1 = 11 − 5 = **6**; P2 = 10 − 4 = **6**; P3 = 6 − 2 = **4** → average 16/3 ≈ **5.33**.
Responses **0 / 2 / 4**. Switches: `ceil(5/2)−1 = 2`, `ceil(4/2)−1 = 1`, `ceil(2/2)−1 = 0` → **3**,
matching the chart (P1 preempted at 2 and 8, P2 at 4).

**S4 — preemptive priority.** t = 1: P2 (priority 1) preempts P1 (2). t = 2: P3 (3) cannot preempt.
t = 4: P2 done → P1 (2) beats P3 (3). Chart `P1 0–1 · P2 1–4 · P1 4–8 · P3 8–10`.
Waits: P1 = 8 − 5 = **3**; P2 = **0**; P3 = 8 − 2 = **6** → average 9/3 = **3**. The lowest-priority
job takes the worst deal — starvation in miniature.

**S5 — dual-core nonpreemptive SJF.** Core 1: `P1 0–7`. Core 2: idle 0–2 (no second process), then
`P2 2–6`, then the shortest ready `P3 6–7`. At t = 7 both cores free but only P4 remains →
`P4 7–11`. Waits: 0 / 0 / **2** / **2** → average **1.0**, against **4** on one core (§3.2).

**S6 — ties.** At t = 5 all three are ready with burst 5, and P1 finishes exactly then.
P2-then-P3: waits 0 / **0** / **5**. P3-then-P2: waits 0 / **5** / **0**. Both average 5/3 ≈ **1.67** —
equal bursts make the exchange gain zero.

**S7 — quantum vs overhead.** `ceil(30/4) = 8` slices → **7** switches. Overhead 7 × 1 = **7** units
on 30 of work → wall clock 37, so 7/37 ≈ **18.9 %** (23 % if measured against work — state your
denominator).

**S8 — (a)** exit and dispatch — the only two that would otherwise idle a core while work waits.
**(b)** SJF/SRTF for average waiting (optimal); RR for average response. **(c)** **False** — the
relationship is non-monotone and merely settles at the FCFS value once `q ≥ max burst` (§5.5).

---

## 11. Self-test questions

Answer out loud; the sketch is the minimum an examiner wants.

1. Why does a single running process leave the CPU idle, and what fixes it?
2. Define CPU burst and I/O burst. Which one does the scheduler control?
3. State the short-term scheduler's goal in one sentence.
4. Name the two transitions for which scheduling is mandatory, and explain why the other three are
   not.
5. Give the definition of preemptive and nonpreemptive scheduling in terms of the transitions.
6. Which hardware feature does a preemptive scheduler require?
7. Define turnaround, waiting and response time for one process with one CPU burst.
8. Why is `W = T − burst` invalid for a process with two CPU bursts?
9. Why is FCFS's average waiting time order-dependent? Give the two averages from S11/S12.
10. What is the convoy effect and what causes it?
11. State the difference between SJF and SRTF in one sentence.
12. Why is SJF optimal? Give the exchange argument in three lines.
13. What is the tie-break rule, and does it change the optimality result?
14. What are the two problems with SJF in a real system?
15. Explain starvation and aging; which schedulers need the cure?
16. Describe RR in four steps, and say what `(n − 1)q` bounds.
17. Compute the number of context switches for a burst of 10 with `q = 1`, `q = 6`, `q = 12`.
18. What happens to RR when `q` exceeds the longest burst, and why?
19. Why is "average turnaround decreases as `q` decreases" wrong?
20. Why partition a ready queue at all? Give the two inter-queue policies and their flaw/benefit.
21. Distinguish partitioned (AMP) from global (SMP) scheduling in three rows.
22. Why is mapping processes to cores NP-hard, and what heuristic does the deck suggest?
23. Name the three implementation costs of global scheduling.
24. Why can two cores not simply halve the single-core average waiting time?

### 11.1 Answer sketches (one line each)

1. I/O waits leave the core idle; **multiprogramming** keeps other ready processes to fill the gap.
2. CPU burst = one execution cycle; I/O burst = one I/O wait. The scheduler controls only *when* the
   bursts happen.
3. Pick processes from the ready queue and give them cores, one per core, keeping every core busy.
4. **Exit** and **dispatch**. The others only create an opportunity; skipping them just risks an idle
   core, which is exactly what nonpreemptive scheduling accepts.
5. Nonpreemptive = only 1 and 5 (plus 4 when a core is idle); preemptive = also 2, 3, 4 or any
   instant.
6. A **timer interrupt**.
7. `T = completion − arrival`; `W = T − burst`; `R = first start − arrival`.
8. The I/O gap is neither running nor ready — subtract `burst1 + I/O + burst2`.
9. Waiting = the sum of the bursts ahead of you, so order decides. S11: **17**; S12: **3**.
10. Short jobs behind an unpreemptable long job: nonpreemption + FIFO.
11. SJF compares **total** bursts at decision points; SRTF compares against **remaining** time at every
    arrival.
12. Swapping a long-before-short inversion changes the sum by `b_short − b_long < 0`, so the
    sorted order is optimal.
13. Equal bursts → earlier arrival (S15 notes); **any** tie-break keeps optimality (the swap gain is
    zero).
14. Bursts must be **predicted**, and long jobs **starve**.
15. Starvation = never selected; aging = raise priority while waiting. Needed by priority scheduling
    and fixed-priority multilevel queues.
16. Head → run `q` → tail if unfinished. `(n − 1)q` bounds **waiting**, not turnaround.
17. `ceil(10/q) − 1` → **9**, **1**, **0**.
18. Nothing is preempted, so RR **is** FCFS; average turnaround freezes at the FCFS value.
19. The curve is non-monotone: intermediate quanta can beat both extremes; it only *settles* at
    `q ≥ max burst`.
20. Different classes want different policies (foreground RR, background FCFS). Fixed priority
    starves; time slicing (80/20) guarantees a share but caps it.
21. Queues per-core vs global; mapping fixed/NP-hard vs none/dynamic; implementation simple vs
    complex.
22. Bin-packing/knapsack over burst sizes; heuristic **best-fit** when bursts are known.
23. Clock synchronisation, global selection overhead/contention, cache migration or a cold cache.
24. Speed-up is limited by available parallelism (S28 core 2 idles 0–2); rebuild the chart, never
    divide.

---

## 12. Glossary

| Term | Meaning |
|---|---|
| **CPU burst** | one continuous stretch of execution on a core (S03) |
| **I/O burst** | one continuous wait for an I/O operation or event (S03) |
| **Short-term scheduler** | the component that picks processes from the ready queue and dispatches them (S05) |
| **Preemption** | taking the CPU away from a running process before it blocks or terminates |
| **Turnaround time** | admitted → terminated (S09) |
| **Waiting time** | time spent in the ready state = turnaround − CPU bursts − I/O waits (S09) |
| **Response time** | admitted → first time in the running state (S09) |
| **CPU utilisation** | busy core-time ÷ (elapsed time × number of cores) (S07) |
| **Throughput** | completed processes per unit time (S07) |
| **FCFS** | first-come, first-served: FIFO ready queue, nonpreemptive (S11) |
| **Convoy effect** | short jobs delayed by an earlier long job in FCFS (S13) |
| **SJF** | shortest-job-first: pick the shortest burst; nonpreemptive (S14) |
| **SRTF** | shortest-remaining-time-first: preemptive SJF; preempt if the newcomer is shorter than what remains (S14) |
| **Priority scheduling** | pick the highest-priority process; smallest integer = highest priority (S17) |
| **Starvation** | a ready process that is never selected because something always outranks it (S17) |
| **Aging** | gradually raising the priority of a starved process (S17) |
| **Time quantum (`q`)** | the maximum continuous slice RR gives a process, typically 10–100 ms (S18) |
| **Round robin (RR)** | cyclic scheduling with a quantum; preemptive by construction (S18) |
| **Multilevel queue** | ready queue partitioned into classes, each with its own algorithm (S22) |
| **Inter-queue scheduling** | the policy that decides *between* queues: fixed priority or time slice (S23) |
| **AMP** | asymmetric multiprocessing = partitioned scheduling, processes pinned to cores (S25) |
| **SMP** | symmetric multiprocessing = global scheduling, one queue for all cores (S27) |
| **Cache migration** | moving a process's private cache data (or suffering a cold cache) after a core change (S30) |
