# SC2005 — Real-Time OS: Study Guide

Companion to the **Part 6a slide deck** (`Part6a (RTOS).pptx`, 19 slides). There is no recording for
this deck, so every citation is a **slide number**: `S17` = slide 17. Speaker notes are quoted where
they carry content the slide leaves implicit. Slide text:
[`transcripts/01-rtos-slides.md`](transcripts/01-rtos-slides.md).

---

## 0. The deck in one picture

```
 CPS: sense -> control law -> actuate                                   S03
   "the answer must be ready by a given time"  =>  a DEADLINE           S04
   correctness = functional AND temporal                                S07
   => real-time = PREDICTABLE, not fast                                 S06
   => guarantee what?  a specification:  <R,C,D>, periodic <T,C,D>  S09-S11
   => the short-term CPU scheduler (Week 3) must respect it             S12
   => FCFS/SJF/RR do not (they never read D)                            S13
        |
        +-- fixed priority  (per PROCESS)  S15 -> RM (shorter T)         S16
        |      ignores D -> can miss                                      S17
        +-- dynamic priority (per INSTANCE) S18 -> EDF (earliest R+D)   S18
        |
        RM vs EDF: simple/predictable vs powerful/unpredictable           S19
```

One line: **an RTOS is judged on whether the worst case meets the deadline, so it needs a
specification containing a deadline and a scheduler that respects it.**

---

## 1. What a real-time OS is (S01 – S08)

### 1.1 Where the topic sits (S01, S02)

S01 (`Course Overview`) branches the module into CPU management (`Processes (L2)`, `Scheduling (L3)`),
memory (`Memory organization (L8)`, `Virtual memory (L9-10)`), filesystems (`Filesystems (L11)`,
`I/O & disk (L12)`), synchronization (`Synchronization (L4-5)`, `Deadlocks (L6)`) — plus one extra
branch: **Special: Real-time OS & virtualization**.

Real-time is therefore a **cross-cutting special topic** laid over the scheduling chapter, not a
thirteenth chapter after I/O — which is why S12 can say the real-time scheduler *is* "the short-term
scheduler from Week 3": same object, different acceptance criterion.

S02 gives the deck's outline:

| # | Question | Slides |
|---|---|---|
| 1 | What is a Real-Time OS (RTOS)? | S03 – S07 |
| 2 | Real-Time Process Specification | S09 – S11 |
| 3 | Real-Time CPU Scheduling | S12 – S19 |

### 1.2 Cyber-physical systems (S03)

> Physical/engineered systems whose operations are **monitored, coordinated and controlled** by a
> **reliable computing and communication core**.

| Domain | Examples on the slide |
|---|---|
| Automotive | autonomous driving, parking assist, **airbag control** |
| Avionics | flight navigation & control |
| Manufacturing | robotics, process control |
| Medical | robotic surgery, implanted devices |
| … | the S03 note adds environmental monitoring, cargo ships, factories, assisted living |

The S03 note adds the trend: sensor-class processors are getting **smaller and more plentiful**, and
these systems are becoming **systems of systems**. "Cyber-physical" is not decoration — it is *why*
timing is hard: the computer sits in a **control loop with a physical process**, so a late answer is
an answer about a world that has moved on.

### 1.3 Why real-time is the shared requirement (S04)

What the S03 examples have in common:

1. **collect data** from sensing devices,
2. **execute the control law(s)** to determine the response,
3. **send actuator commands** in a reasonable amount of time.

> *"Not only does the application have to produce a functionally correct output, but it must do so
> within this deadline… both functional/logical correctness as well as temporal correctness or
> timeliness are equally important."* (S04 note)

Examples: **collision avoidance and braking**, and the **pacemaker timing diagram** (a pulse must
land inside the heart's electrical window — too early and too late are both wrong).

Drawn as the pacemaker slide draws it: `sense → compute → actuate`, repeated every `T`, with the
response due `D` after each release.

```
 ---+-----------+-----------+-----------+-----------+--> t
    |<---- T (period) ----->|
    |<-- response -->|
    |<-------- D (deadline) ------------->|
```

### 1.4 What is a "reasonable time"? (S05)

No number; three questions instead:

| Question | Decides | Examples on the slide |
|---|---|---|
| **What is the functionality?** | the order of magnitude | collision avoidance: **milliseconds**; pacemaker: **up to a second**; robotic surgery: **varies greatly** |
| **What are the environment constraints?** | what is achievable | resources; timing of sensors, actuators, operations |
| **What are the failure-mitigation strategies?** | how much margin | time to detect and **recover**; e.g. **execution replication** |

The note adds the cut-off: real-time spans "a few milliseconds to potentially even few minutes" —
longer "would usually **not** be considered real-time requirements, but **design-time planning**". So
the deadline is a property of the **application**, never of the OS (S07).

### 1.5 Real-time ≠ fast (S06)

> **Real-Time ≠ Fast**
> **Real-Time = Predictable even in the worst-case**
> — *"Man drowned in a river with average depth 20 cms"*

The joke is the exam answer. The man is ~1.8 m tall; the river is 0.2 m **on average**; on average he
can walk it. What kills him is the **maximum** depth at the one point he stands in. Real-time systems
are judged exactly like that — **on the worst case, not the average**.

| | **Average-case thinking** (Week 3) | **Worst-case thinking** (real-time) |
|---|---|---|
| Question | "how long does a job take *typically*?" | "how long can it take **at worst**?" |
| Metric | mean waiting / turnaround / response | **max** response vs the deadline |
| Good answer | low mean | a **provable bound** |
| Tolerates | an occasional slow job (averaged away) | **nothing** — one late job is a failure |

A slow system with a provable 10 ms worst case is real-time; a fast one with an occasional 100 ms tail
is not.

### 1.6 The definition (S07)

> **Definition:** System whose correctness depends not only on the **logical/functional** aspects,
> but also on the **temporal** aspects.
> * Application has **deadlines that must be met**.
> * A **real-time OS (RTOS)** provides OS services to such systems (e.g. **FreeRTOS**, **MicriumOS**).

| Bullet on S07 | Meaning |
|---|---|
| Key measure: **timeliness/predictability** | not throughput, not utilisation, not average waiting — this replaces the [`../c3`](../c3) metrics |
| **Worst-case over average-case** | the guarantee is on the worst case; the mean is a comfort statistic |
| **Deadlines come from application requirements** | the OS cannot choose them, only be given them |
| (note) worst case includes mechanics, computation, **communication** | the bound is end-to-end: sensor + CPU + actuator |

An RTOS supplies the standard services **"over and above"** with timing features (S02 note). The deck
never lists them — S09–S19 *are* that answer; do not invent a feature checklist (priority inheritance,
tickless kernels…).

---

## 2. Real-time process specification (S09 – S11)

### 2.1 `<R, C, D>` (S09)

> **Definition:** A real-time process is specified as **`<R, C, D>`**, where `R` is **release time**,
> `C` is **execution requirement** and `D` is **relative deadline**.
> * Requires **`C` time units of CPU in the interval `[R, R+D)`**.

| Parameter | Meaning | Where it comes from |
|---|---|---|
| `R` | instant the process becomes available | application requirement |
| `C` | CPU time needed, **worst case** | the hard one — §2.2 |
| `D` | how long after release it must finish | application requirement |

Three readings examiners test:

1. **`D` is relative**; the absolute deadline is `R + D`. For `P3<5,10,35>` that is **t = 40**, not 35.
2. **The window is half-open** `[R, R+D)`: work is *placed* in it. Completing exactly at `R + D` is
   **on time**.
3. **`C` is a requirement, not a duration** — fitting it in is the scheduler's problem.

S09's example:

```
P1 <0, 5, 10>     released 0,  needs 5,  must finish by 0+10 = 10
P2 <5, 10, 35>    released 5,  needs 10, must finish by 5+35 = 40
P3 <20, 10, 30>   released 20, needs 10, must finish by 20+30 = 50
```

Trivially feasible: P1 `0–5`, P2 `5–15`, P3 `20–30`. P2's window `[5,40)` is 35 units long for 10
units of work — the spec states the slack; the scheduler spends it.

### 2.2 The hard parameter, and the one assumption (S09)

> *"We need to know how much CPU cycles it needs **in the worst-case**… Only with these parameters
> can the RTOS manage the processes to ensure that their real-time requirements can be met."*
> *"`R` and `D` are straightforward…"* (S09 note, truncated)

`R` and `D` come from the physics of the loop; `C` must be **bounded** by measurement or analysis. If
`C` is under-estimated, every later deadline calculation used the wrong number — S06's discipline
applied to a parameter.

> *"In this lecture, we assume processes only have a **single CPU burst**; `C` is the duration of this
> burst."*

That assumption makes the chapter tractable — no I/O waits, no blocking, each instance is one
contiguous lump of CPU demand placed in its window — and it is the assumption a real RTOS cannot make,
which is why priority inversion exists in practice but not here.

### 2.3 Recurrent processes (S10)

> *"Each instance of such a recurrent real-time process is a real-time process with parameters
> `<R,C,D>`."*

Motivation unchanged from S04: sense → control law → actuate, **regularly**. Examples: airbag control,
flight control, collision avoidance, pacemaker.

* "Does it meet its deadline?" must hold for **every instance, forever** — a recurrent process is an
  infinite job stream.
* The **process** (`T,C,D`) and the **instance** (`R,C,D`) are different objects: S09 defines the
  instance, S11 the process.

The note promises "**two** broad types… in the next couple of slides", but only **periodic** gets a
slide; the other — **sporadic** — appears only in passing on S14/S16.

### 2.4 Periodic processes (S11)

> **Definition:** A process that repeats **periodically**, generated by a **time-triggered**
> phenomenon (a sensor sending data periodically).
> * Specified as **`<T, C, D>`**, where `T` is the **process period**.
> * Released at **`R = 0, T, 2T, …`**

Example `P<10, 5, 7>`: a job every 10 units, needing 5, due 7 after each release; `u = C/T = 0.5`.

`D` need **not** equal `T` — here `D = 7 < T = 10`. S16 uses `D = T` throughout, then S17 sets
`D = 14` with `T = 20`, and that one change is what makes RM miss. `T` also doubles as the **minimum
release separation** for a sporadic process — hence S16's phrase "process periods / minimum
release-separation time".

### 2.5 From `<T, C, D>` to a family of instances

```
instance k (k = 0, 1, 2, …):  release R_k = kT   absolute deadline d_k = kT + D   demand C
```

For the S17/S18 culprit `P3<20, 2, 14>`:

| k | release `R_k` | absolute deadline `d_k` |
|---|---|---|
| 0 | 0 | **14** |
| 1 | 20 | **34** |
| 2 | 40 | 54 |

Two instances of the *same process* have **different absolute deadlines**. A **dynamic-priority**
scheduler (S18) re-decides per row; a **fixed-priority** scheduler (S15) decides once, for the
process.

---

## 3. Why classic CPU schedulers fail (S12 – S13)

### 3.1 The metric changes (S12)

> *"We see how the algorithms we studied in Week 3 perform for real-time processes and what new
> algorithms we can consider for this specific application domain."*

FCFS, SJF and RR ([`../c3`](../c3)) were designed against **average** waiting time, **average**
turnaround time, response time. Every one of those is an average, and S06 has just said averages are
the wrong currency.

| | c3 metric | Real-time metric |
|---|---|---|
| Unit of judgement | the whole workload | **each instance, individually** |
| Good schedule | small mean | **zero missed deadlines** |

Trading job A against job B is fine when averages absorb it; under a deadline metric it is not
allowed, because one late job is a failure. So the S13 failure is not a bug in FCFS — FCFS answers the
question it was built for; it is being asked a different one.

### 3.2 The S13 process set

| Process | `R` | `C` | `D` | absolute deadline `R+D` |
|---|---|---|---|---|
| P1 | 0 | 20 | 30 | **30** |
| P2 | 0 | 5 | 10 | **10** |
| P3 | 5 | 10 | 35 | **40** |
| P4 | 20 | 10 | 30 | **50** |
| P5 | 25 | 5 | 10 | **35** |

```
total demand = 20+5+10+10+5 = 50        span available = 0 .. 50 (last deadline)
```

Demand **equals** span: a feasible schedule must keep the CPU busy 0→50 **and** order the work
correctly. Zero slack — every wrong decision costs a deadline. (Verified: the deadline order
`P2, P1, P5, P3, P4` meets all five; it is the schedule EDF produces in §3.6.)

S13's verdict, before any detail: *"They don't prioritize deadlines and hence perform poorly."*

### 3.3 FCFS

Arrival order P1, P2 (0), P3 (5), P4 (20), P5 (25).

| Interval | 0–20 | 20–25 | 25–35 | 35–45 | 45–50 |
|---|---|---|---|---|---|
| CPU | **P1** | **P2** | **P3** | **P4** | **P5** |

| Process | Deadline | Finishes | Result |
|---|---|---|---|
| P1 | 30 | 20 | ✅ |
| **P2** | **10** | **25** | ❌ **15 late** |
| P3 | 40 | 35 | ✅ |
| P4 | 50 | 45 | ✅ |
| **P5** | **35** | **50** | ❌ **15 late** |

**What went wrong:** P1 arrived at the same instant as P2 and happened to be first, so a 20-unit job
ran while a 5-unit job with a 10-unit deadline waited. FCFS is a **convoy**: a long job at the head
delays everything behind it, including an emergency.

### 3.4 SJF (non-preemptive, as drawn)

| Interval | 0–5 | 5–15 | 15–35 | 35–40 | 40–50 |
|---|---|---|---|---|---|
| CPU | **P2** | **P3** | **P1** | **P5** | **P4** |

| Process | Deadline | Finishes | Result |
|---|---|---|---|
| **P1** | **30** | **35** | ❌ **5 late** |
| P2 | 10 | 5 | ✅ |
| P3 | 40 | 15 | ✅ |
| P4 | 50 | 50 | ✅ exactly |
| **P5** | **35** | **40** | ❌ **5 late** |

**What went wrong:** SJF prefers *short* jobs to *urgent* ones. At t=15 the only ready job is P1 (20
units), and non-preemptive SJF cannot react when P5 — released at 25, 5 units, due 35 — arrives.
**Shortest ≠ most urgent.**

### 3.5 Round robin, q = 5

Convention (the tie matters): when a quantum expires the preempted process returns to the **tail**
before a process arriving at that same instant joins.

| # | Interval | Process | Left after |
|---|---|---|---|
| 1 | 0–5 | P1 | 15 |
| 2 | 5–10 | P2 | 0 — **done 10, d 10 ✅** |
| 3 | 10–15 | P1 | 10 |
| 4 | 15–20 | P3 | 5 |
| 5 | 20–25 | P1 | 5 |
| 6 | 25–30 | P3 | 0 — done 30 ✅ |
| 7 | 30–35 | P1 | 0 — **done 35, d 30 ❌** |
| 8 | 35–40 | P4 | 5 |
| 9 | 40–45 | P5 | 0 — **done 45, d 35 ❌** |
| 10 | 45–50 | P4 | 0 — done 50 ✅ |

Slice order: `P1 P2 P1 P3 P1 P3 P1 P4 P5 P4`. **P1 5 late, P5 10 late**; P2/P3/P4 met.

**What went wrong:** RR is *fair*, and fairness is not urgency. It gives P1 four 5-unit slices across
35 units and spends the set's zero slack on rotating; P5 (5 units, released 25, due 35) is not served
until 40. The exact slice order depends on the quantum-boundary tie-break (the opposite convention
finishes P1 at 50 and loses three deadlines) — **memorise the conclusion, not the trace.**

### 3.6 The verdict, and the question it forces

| Algorithm | Late by | Missed |
|---|---|---|
| FCFS | 15, 15 | P2, P5 |
| SJF (non-preemptive) | 5, 5 | P1, P5 |
| RR (q=5) | 5, 10 | P1, P5 |
| *order by deadline* | — | **none** |

Every classic algorithm misses **two of five** deadlines on a set that *is* schedulable, for one
structural reason: **none of them looks at `D`**. FCFS looks at arrival, SJF at length, RR at
fairness.

```
the same set, always serving the earliest absolute deadline:

0    5          25    30        40        50
|P2 |---- P1 --------|P5  |--- P3 ---|-- P4 --|
d10        d30        d35    d40        d50
done 5     done 25    done 30 done 40   done 50      all met
```

*(That row is not drawn on S13 — it is what S18's EDF rule produces. It is the bridge to §6.)*

---

## 4. The real-time scheduling problem (S14)

> **Given a set of periodic/sporadic real-time processes, find a uni-processor CPU scheduling
> algorithm that can meet process deadlines.**

Four words carry the weight: **"an algorithm"** means a rule that works for any set it is handed (a
hand-drawn schedule proves feasibility but schedules nothing); **"periodic/sporadic"** means infinite
job streams, unlike S13's one-shot jobs; **"uni-processor"** excludes hiding lateness in parallelism;
**"can meet deadlines"** means every instance, forever.

The note adds: *"the same techniques can be applied to sporadic processes as well"* — `T` is then
only a minimum separation.

Running example `P1 <10,6,10>`, `P2 <19,4,19>`, `P3 <20,2,20>`:

| Process | `T` | `C` | `D` | `C/T` |
|---|---|---|---|---|
| P1 | 10 | 6 | 10 | 0.600 |
| P2 | 19 | 4 | 19 | 0.211 |
| P3 | 20 | 2 | 20 | 0.100 |
| | | | | **U = 0.911** |

`U = 6/10 + 4/19 + 2/20 = 0.9105` — 91 % utilisation with no slack to waste. The deck never computes
`U`; do it anyway, it is the fastest sanity check you have. The axis marks `0, 6, 10, 16, 19, 20, 26,
30, 38` are exactly the switch/release/completion points of §5.3 — evidence that the intended
schedule is the preemptive one.

---

## 5. Fixed-priority scheduling and Rate Monotonic (S15 – S17)

### 5.1 What "fixed priority" means (S15)

> **Priorities are fixed for each recurrent process.**
> **Priorities are fixed across instances of recurrent processes.**

One priority per **process**, inherited by every instance, forever. The S15 consequence chain is more
surprising than it looks:

> Suppose instance of `P1(R=0)` has higher priority than instance of `P2(R=0)`. Then
> * `P1(R=10)` has higher priority than `P2(R=0)`
> * `P1(R=10)` has higher priority than `P2(R=19)`
> * `P1(R=20)` has higher priority than `P2(R=19)` …

A **newer** instance of P1 — just released, deadline further away — outranks an **older** instance of
P2 already waiting and due **sooner**. Only the process name enters the decision. That is not an
implementation flaw; it is the **definition** of fixed priority, and it is the mechanism behind S17's
missed deadline.

### 5.2 Rate Monotonic (S16)

> **Assign priorities based on process periods / minimum release-separation time (`T`).**
> **Shorter `T` implies higher priority.** Ties are broken arbitrarily.

| Process | `T` | RM priority |
|---|---|---|
| P1 | 10 | **1 (highest)** |
| P2 | 19 | 2 |
| P3 | 20 | **3 (lowest)** |

Justification worth writing: a short-period process must *also* finish quickly to keep up with its own
arrival stream, so period is a cheap **proxy** for urgency — computed **once**, offline.

### 5.3 The RM schedule for the running example

| Interval | Runs | Why | Check |
|---|---|---|---|
| 0–6 | **P1₁** | highest priority | d 10, done 6 ✅ |
| 6–10 | **P2₁** | P1₁ done; P3₁ outranked | d 19, done 10 ✅ |
| 10–16 | **P1₂** | released at 10 | d 20, done 16 ✅ |
| 16–18 | **P3₁** | last one left | d 20, done 18 ✅ |
| 18–19 | *idle* | | |
| 19–20 | **P2₂** (1 of 4) | released at 19 | |
| 20–26 | **P1₃** | released 20 → **preempts** P2₂ | d 30, done 26 ✅ |
| 26–29 | **P2₂** (3 left) | resumes | d 38, done 29 ✅ |
| 29–30 | **P3₂** (1 of 2) | released 20, waiting | |
| 30–36 | **P1₄** | released 30 → **preempts** P3₂ | d 40, done 36 ✅ |
| 36–37 | **P3₂** (1 left) | resumes | d 40, done 37 ✅ |
| 38–… | **P2₃** … | repeats | d 57 |

**Every deadline met**, and the schedule is legible: P1 takes its 6 units immediately, P2 fills gaps,
P3 takes what is left — exactly S16's note, *"for high-priority periodic/sporadic processes it gives a
very predictable schedule"*. Note the preemptions at t = 20 and t = 30; a non-preemptive reading
(P2₂ 19–23, P1₃ 23–29, P3₂ 29–31) also meets everything here, but the axis marks 20/26/30 belong to
the preemptive one.

### 5.4 Why industry uses RM (S16, S19)

* **Predictable** for high-priority processes; **important processes get high priority** by giving
  them a short period (S16 note).
* **Simple implementation**: one queue per recurrent process; **`O(1)`** with **bitmaps** — S19:
  *"A simple priority-based queue data structure would suffice… efficient O(1) time complexity
  implementations are available for RM using bitmaps."*
* **Stays predictable under high load** (S19).

All of it is possible **because the priority never changes**: compute once per process, one queue
each, never think about it again.

### 5.5 RM's limitation (S17)

> **"RM is good, but still does not always prioritize urgent processes."**
> Modified set: `P1<10,6,10>`, `P2<19,4,19>`, **`P3<20,2,14>`**

One character changes: P3's deadline 20 → **14**. Periods — hence every RM priority — are untouched,
so the schedule is *identical* to §5.3:

| Interval | Runs | Check |
|---|---|---|
| 0–6 | P1₁ | d 10 ✅ |
| 6–10 | P2₁ | d 19 ✅ |
| 10–16 | P1₂ | d 20 ✅ |
| 16–18 | **P3₁** | d **14**, done **18** ❌ **4 late** |
| 19–20 | P2₂ | |
| 20–26 | P1₃ | d 30 ✅ |
| 26–29 | P2₂ | d 38 ✅ |
| 29–30 | P3₂ (1 of 2) | |
| 30–36 | P1₄ | d 40 ✅ |
| 36–37 | **P3₂** | d **34**, done **37** ❌ **3 late** |

```
 0    6   10   16 18 19 20      26  29 30      36 37
 |P1₁ |P2₁ |P1₂ |P3₁| |P2₂|----P1₃----|P2₂ |P3₂|--P1₄----|P3₂|
                ^
                deadline 14, served 16-18
```

**It misses again on the next instance** (34 → 37). Nothing about a process's priority changes, so
the miss is not a one-off: it is starvation in miniature (the vocabulary is [`../c7`](../c7)'s).

### 5.6 Diagnosing the miss

> *"Since RM **ignores the relative deadline parameter `D`**, it can potentially miss deadlines for
> some process sets as shown in this slide."*

Trace it to the single decision. At `t = 6`:

| Instance | `T` (RM's only input) | absolute deadline | RM picks |
|---|---|---|---|
| P2₁ | 19 | **19** | ✔ 6–10 |
| P3₁ | 20 | **14** ← urgent | ✘ waits until 16 |

RM compares **19 < 20**; the deadlines say **14 < 19**. The rule read the wrong number. From t = 6
P3₁ cannot finish before 18, and the deadline at 14 is lost.

1. **A feasible schedule exists** (§6.1) — this is not overload, the rule is wrong for this set.
2. **It is not a bug.** RM did exactly what it promises; its promise just does not mention `D`.
3. **RM is the best rule *among those that ignore `D`*.** Do not claim it is optimal full stop — S17
   is the counter-example, on the very next slide.

---

## 6. Earliest Deadline First (S18)

> **Dynamic-priority scheduler that assigns priorities based on process instance deadlines.**
> **Instances with shorter deadline are given higher priority.** **NOT the same as parameter `D`.**
> Ties are broken arbitrarily.

**"Deadline" means absolute deadline.** For `P<10,6,7>` the instances share `D = 7` but have absolute
deadlines `7, 17, 27`. EDF compares `7, 17, 27`; RM compares `T` and treats them as identical by
construction. This is the most common notation error in the chapter.

### 6.1 EDF on the S17/S18 set

S18 keeps P3's short deadline and shortens P2's: `P1<10,6,10>`, **`P2<19,4,17>`**, **`P3<20,2,14>`**.
Absolute deadlines: P1₁ 10, P1₂ 20, P1₃ 30, P1₄ 40; P2₁ **17**, P2₂ 36; P3₁ **14**, P3₂ 34.

| Interval | Runs | Candidates (absolute deadline) | Check |
|---|---|---|---|
| 0–6 | **P1₁** | P1₁ 10, P3₁ 14, P2₁ 17 → **10** | d 10, done 6 ✅ |
| 6–8 | **P3₁** | P3₁ 14, P2₁ 17 → **14** | d **14**, done **8** ✅ |
| 8–12 | **P2₁** | only P2₁ | d 17, done 12 ✅ |
| 10 | *no switch* | P1₂ released with d 20; P2₁ has d **17** | |
| 12–18 | **P1₂** | P1₂ 20 | d 20, done 18 ✅ |
| 18–19 | *idle* | | |
| 19–20 | **P2₂** (1 of 4) | P2₂ 36 | |
| 20–26 | **P1₃** | P1₃ 30, P3₂ 34, P2₂ 36 → **30** | d 30, done 26 ✅ |
| 26–28 | **P3₂** | P3₂ 34, P2₂ 36 → **34** | d 34, done 28 ✅ |
| 28–31 | **P2₂** (3 left) | at 30 P1₄ arrives with d 40 > 36 → **no preemption** | d 36, done 31 ✅ |
| 31–37 | **P1₄** | P1₄ 40 | d 40, done 37 ✅ |
| 38–… | **P2₃** … | repeats | d 55 |

**Zero misses, including the instance RM lost.** Note where EDF *declines* to preempt (t = 10, t = 30):
a dynamic scheduler is not "always preempting", it is "always comparing deadlines", and sometimes the
running instance still has the earliest one.

### 6.2 Why EDF fixes it — one decision

| | Pending at t = 6 | Rule | Chosen | P3₁'s fate |
|---|---|---|---|---|
| **RM** | P2₁, P3₁ | `T`: 19 < 20 | **P2₁** | waits → done 18, **misses d 14** |
| **EDF** | P2₁, P3₁ | `R+D`: 14 < 17 | **P3₁** | runs 6–8, **meets d 14 with 6 to spare** |

Same set, same releases, same `C`. The only difference is **which number the rule reads**: a static
property of the process, or the deadline of the instance in front of it.

### 6.3 What EDF costs

A job's priority is only known **when it is released** (its `R` is needed, and for sporadic processes
`R` is unknown offline), so the ready queue must be **sorted online**, instances of one process
**cannot** share a queue, and the best known cost is `O(log n)` not `O(1)`. That is §7.

---

## 7. RM versus EDF (S19)

| **RM** | **EDF** |
|---|---|
| Simpler implementation (separate queue for each recurrent process) | Harder implementation (online sorting of queue based on instance deadlines) |
| Predictability for high priority processes, **even under high load** | **Can be unpredictable under high load** |

Decoded, row by row:

| Axis | **RM** | **EDF** |
|---|---|---|
| Priority type | static, fixed per process | dynamic, per instance |
| Complexity | one priority queue per process; **`O(1)`** with bitmaps | one sorted queue; **`O(log n)`** best known |
| Predictability | high-priority processes unaffected by anything below them | any instance may be outranked by a more urgent one |
| Under overload (`U > 1`) | fails **predictably**: the lowest-priority process misses; high-priority ones still meet theirs | fails **unpredictably**: any process can miss, depending on arrivals |
| Utilisation bound | **none stated in this deck** — see the honesty note | **none stated in this deck** |
| Feasible sets | may miss a deadline a feasible schedule would have met (S17) | meets every deadline whenever a schedule exists, for the sets this course uses |

**Why "predictability under high load" is decisive.** Under overload *somebody* must fail. RM picks
the victim **in advance** — the longest-period, i.e. least important, process — so an engineer can
reason about failure: "telemetry degrades, the brake controller does not." EDF gives no such
guarantee: losses are spread over whatever happened to be due. The deck states the two bullets; this
is what they mean (practice problem P7 works it out).

**"Which is better?" — always a conditional.** Known set, generous deadlines, must survive overload
→ **RM** (simpler, `O(1)`, bounded failure). Every deadline must be met, releases sporadic, `D` maybe
tighter than `T` → **EDF** (it uses the deadline information RM discards). In one sentence: *EDF is
stronger when you can afford it; RM is chosen when you need to know in advance how the system will
fail.*

---

## 8. The method

```
1. SPECIFY  Rewrite each process as <T,C,D> (or <R,C,D>); spread it into instances:
            R_k = kT,  d_k = kT + D,  demand C.
2. BUDGET   U = sum(C_i/T_i).  If U > 1 no algorithm meets every deadline — say so and stop.
3. PRIORITY RM  -> order by T, smaller first; fixed for the whole timeline.
            EDF -> order by absolute deadline d_k at every instant.
4. DRAW     Advance to the next event: a release, a completion, or a deadline. At a release
            re-apply the rule and PREEMPT if the new instance wins.
5. CHECK    finish <= R_k + D for every instance. Finishing exactly at the deadline is ON TIME.
6. NAME     If something missed: which instance, how late, and the one decision that caused it
            (for RM: "it compared T, not D").
```

* Write the **absolute** deadline beside every instance before drawing — almost every error here is a
  `D` used where `R+D` was meant.
* **Never idle while work is ready** on a tight set (S13); idle time is automatically a miss. A
  preempted instance resumes with its **remaining** `C`, not its full `C`.

---

## 9. Formula sheet

```
SPECIFICATION
  <R, C, D>   R release, C worst-case execution requirement, D relative deadline
              needs C units of CPU in [R, R+D)
  <T, C, D>   T period (also minimum release separation for sporadic)
  instance k  R_k = kT,  absolute deadline d_k = kT + D

DEADLINE TEST     met  <=>  completion <= R_k + D
UTILISATION       U_i = C_i/T_i,   U = sum C_i/T_i
                  U <= 1 is NECESSARY, not sufficient when D < T

PRIORITY KEYS     RM : T      (smaller = higher, static)
                  EDF: R + D  (smaller = higher, dynamic)
                  ties broken arbitrarily under both
```

> **Honesty note.** A Rate Monotonic **utilisation bound** (Liu & Layland `n(2^(1/n) − 1)`) is **not
> stated anywhere in this deck** and is not examinable in that form here. All you need for SC2005 is:
> shorter period ⇒ higher priority, then draw the schedule.

---

## 10. Practice problems

**P1.** Give the releases and absolute deadlines of the first three instances of `P<10,5,7>`. Which
parameter does RM use? Which does EDF use?

**P2.** For the S13 set, compute total demand and the span to the last deadline. What does that imply
for idle time, and why does it make ordering decisive?

**P3.** `P1<10,6,10>`, `P2<19,4,19>`, `P3<20,2,20>`: compute `U`, assign RM priorities, draw the
timeline 0–20. Any misses?

**P4.** Change only P3 to `P3<20,2,14>`. Redraw RM 0–20. Which instance misses, by how much, and at
which instant was the fatal choice made?

**P5.** Same set, EDF. Which instance does EDF serve at `t = 6`, and why? Any misses?

**P6.** `P1<6,2,6>`, `P2<12,3,12>`, `P3<24,4,24>`: compute `U`, draw RM 0–24 marking preemptions,
check every deadline, and say whether EDF differs.

**P7.** `P1<4,3,4>`, `P2<6,4,6>`: compute `U`, schedule with RM and with EDF 0–24, count misses for
each. Which S19 claim does this illustrate?

### Solutions

**S1.** Releases `0, 10, 20`; absolute deadlines `7, 17, 27`. RM uses **`T` only** (10) — `C` and `D`
never enter. EDF uses **`R_k + D`**, so `7, 17, 27` are three different priorities even though `D = 7`
for all three.

**S2.** Demand `= 50`, span `= 0…50`, so demand **equals** span: the CPU may never idle **and** the
order must be right. Any idle unit, or any long job ahead of an urgent one, becomes a missed deadline.

**S3.** `U = 0.600 + 0.211 + 0.100 = 0.911`; priorities **P1 (10) > P2 (19) > P3 (20)**. Timeline is
the one in §5.3: `P1₁ 0–6`, `P2₁ 6–10`, `P1₂ 10–16`, `P3₁ 16–18`.

P1₁ 6 ✅, P2₁ 10 ✅, P1₂ 16 ✅, P3₁ 18 ✅ — **all met** (P2₂ finishes 29, inside 38).

**S4.** `U` and all priorities unchanged (P3's `T` is still 20), so the timeline is identical up to
t = 18: P1₁ 0–6, P2₁ 6–10, P1₂ 10–16, P3₁ 16–18. **P3₁ misses by 4** (d 14, done 18). The fatal
decision is at **t = 6**: P2₁ (d 19) and P3₁ (d 14) both ready, and RM compared periods (19 < 20)
instead of deadlines (14 < 19). Had P3₁ run 6–8 it would have finished 6 units early.

**S5.** At t = 6 EDF compares `14` (P3₁) with `19` (P2₁) and serves **P3₁**.

```
 0    6  8   12   18 19 20
 |P1₁ |P3₁|P2₁ |P1₂ | |P2₂|…
  d10  d14 d19   d20    d36
```

P3₁ done 8 ✅ (6 early), P2₁ done 12 ✅, P1₂ done 18 ✅. **Nothing misses** — one different decision
was enough.

**S6.** `U = 0.333 + 0.250 + 0.167 = 0.750`; **P1 > P2 > P3**.

```
 0  2    5  6  8     11 12  14   17 18  20    24  26
 |P1₁|P2₁|P3₁|P1₂|P3₁|  |P1₃|P2₂|  |P1₄|      |P1₅|…
   d6  d12 d24 d12 d24     d18 d24    d24        d30
```

Completions: P1₁ 2, P2₁ 5, P3₁ **11** (ran 5–6, preempted at 6 by P1₂, resumed 8–11), P1₂ 8, P1₃ 14,
P2₂ 17, P1₄ 20, P1₅ 26 — **all within their deadlines**, with idle time 20–24 unused. EDF produces the
**same** schedule: at every decision the earliest absolute deadline coincides with the shortest
period.

**S7.** `U = 0.75 + 0.667 = 1.417 > 1` — not schedulable; deadlines must be lost.

```
RM   0-3 P1₁ | 3-4 P2₁ | 4-7 P1₂ | 7-8 P2₁ | 8-11 P1₃ | 11-12 P2₁ | 12-15 P1₄ | 15-16 P2₁ | …
     every P1 instance meets its deadline; every P2 instance misses (by 10, 14, …)
EDF  0-3 P1₁ | 3-7 P2₁ | 7-10 P1₂ | 10-14 P2₂ | 14-17 P1₃ | 17-20 P1₄ | 20-24 P2₃ | …
     P1₂ 2 late, P1₃ 5 late, P1₄ 4 late, P2₁ 1 late, P2₂ 2 late
```

**RM loses only the low-priority process; EDF loses deadlines across both.** That is S19's
"predictability for high priority processes, even under high load" versus "can be unpredictable under
high load" — why an overloaded safety-critical system may still prefer RM.

---

## 11. Self-test questions

1. Define a cyber-physical system and give the three steps common to the S03/S04 examples.
2. State the definition of a real-time system. Which two kinds of correctness does it combine, and
   which key performance measure follows from that?
3. Explain the river quotation. What exactly is wrong with average response time?
4. Name the three S05 factors that decide a "reasonable time", with the slide's examples.
5. Write `<R,C,D>`, giving each parameter's meaning and origin. Why is `C` the hard one, and what
   assumption does the deck make about it?
6. Define recurrent and periodic processes, and give the `<T,C,D>` release pattern.
7. For `P<10,5,7>`, list the releases and absolute deadlines of the first four instances.
8. Why do FCFS, SJF and RR all miss deadlines on the S13 set? Name the decision each gets wrong.
9. State the real-time CPU scheduling problem. What does "uni-processor" exclude?
10. What does "fixed priority" mean, why does a newer P1 instance outrank an older P2 instance, and
    which single number does RM (including its tie-break) use?
11. Reproduce the S16 timeline 0–20. Which instances are preempted, and by whom?
12. S17 changes one parameter — which, and to what? Why is the schedule unchanged, which instance
    then misses and by how much, and at which instant was the wrong choice made?
13. State the EDF rule. Why is "the deadline" not the same as the parameter `D`? Run EDF on the S17
    set and show `P3₁` meeting its deadline of 14.
14. Give S19's two implementation claims and two predictability claims, and say what each means for
    a designer.
15. Under overload, which processes fail under RM and which under EDF? Why might RM be safer?

---

## 12. Glossary

| Term | Meaning |
|---|---|
| **Real-time system** | system whose correctness depends on **temporal** as well as logical aspects |
| **RTOS** | OS providing services to real-time systems so deadlines can be guaranteed (FreeRTOS, MicriumOS) |
| **Deadline** | instant by which an instance must complete; missing it is a **correctness** failure |
| **Execution requirement `C`** | worst-case CPU time an instance needs (one CPU burst) |
| **Relative vs absolute deadline** | `D` vs `R + D` |
| **Recurrent process** | process that executes its function repeatedly; each instance is an `<R,C,D>` process |
| **Period `T`** | release interval; also the minimum release separation for a sporadic process |
| **Utilisation `U`** | `Σ Cᵢ/Tᵢ` — the fraction of CPU the set demands |
| **Fixed-priority scheduling** | one priority per process, fixed across its instances |
| **Dynamic-priority scheduling** | priority recomputed per instance |
| **Rate Monotonic (RM)** | fixed priority by period: shorter `T` ⇒ higher priority |
| **Earliest Deadline First (EDF)** | dynamic priority by absolute deadline: earliest `R+D` first |
| **Preemption** | a winning released instance takes the CPU immediately |
| **Overload** | `U > 1`; some deadline must be missed whatever the algorithm |
| **Predictability** | ability to state in advance that deadlines will be met — and, under overload, which will not |
