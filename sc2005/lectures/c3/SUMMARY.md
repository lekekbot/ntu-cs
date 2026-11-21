# CPU Scheduling — Summary (one page)

Thirty slides, one question: **when the CPU is free, who runs next — and what does that cost in
waiting time?**

---

## The 60-second version

1. A process alternates **CPU bursts** and **I/O bursts** (S03). One process alone cannot keep a core
   busy, so we keep several ready: that is **multiprogramming**.
2. The **short-term scheduler** picks processes from the ready queue and gives them cores, one
   process per core (S05). It runs on state changes; only **two** of the five transitions *must*
   trigger it (the slide's answer: **1 and 5**).
3. **Nonpreemptive** = the process holds the CPU until it terminates or blocks. **Preemptive** = the
   OS may take the CPU away (S06).
4. Two system-wide metrics: **CPU utilisation** and **throughput**. Three per-process metrics:
   **turnaround**, **waiting**, **response** — all minimised, all averaged (S07–S09).
5. **FCFS** is a FIFO queue: nonpreemptive, trivial, and it suffers the **convoy effect** — one long
   job in front inflates everybody behind it (S13). Arrival order changes the average: same three
   jobs give average waiting **17** or **3** (S11–S12).
6. **SJF** gives the CPU to the shortest burst; **SRTF** is its preemptive form (preempt if the
   newcomer is shorter than what is left of the runner). SJF/SRTF **minimise average waiting time**
   (S14).
7. **Priority scheduling** generalises both: FCFS = priority by arrival, SJF = priority by burst
   length. Its disease is **starvation**; the cure is **aging** (S17).
8. **Round robin** gives each process a **quantum q** (10–100 ms), then re-queues it; it is
   preemptive by construction and gives the best **response** time (S18–S19).
9. Quantum size trades **overhead** against **fairness**: small `q` → many context switches; large
   `q` → FCFS. Average **turnaround has no monotone relationship with `q`**, but it stops changing
   once `q ≥` the longest burst (S20–S21).
10. **Multilevel queue** splits the ready queue (foreground RR / background FCFS) and then has to
    decide *between* the queues — fixed priority (starves) or time slice (S22–S23).
11. On **multiple cores**, either pin processes to cores ahead of time (**partitioned / AMP** — easy,
    but mapping is NP-hard) or keep one global queue (**global / SMP** — no mapping problem, but
    global clocks, global selection and cache migration cost you) (S24–S30).

---

## The algorithms at a glance

| Algorithm | Preemptive? | Starvation? | Average waiting | Overhead | Good for |
|---|---|---|---|---|---|
| **FCFS** | no | **yes** (convoy effect) | order-dependent, can be terrible | minimal | batch, no interactivity |
| **SJF** (nonpreemptive) | no | yes (long jobs) | **optimal** | needs burst estimates | batch |
| **SRTF** (preemptive SJF) | yes | yes (long jobs) | **optimal** | more switches | batch |
| **Priority** | either | **yes** → aging | depends on priorities | low | mixed importance |
| **RR** | yes | no | worse than SJF, up to `(n−1)q` | `q` small ⇒ high | interactive, time-sharing |
| **Multilevel queue** | either | yes (fixed priority) | depends | moderate | foreground vs background |
| **AMP (partitioned)** | either (per core) | per core possible | fixed by the partition | low | simple, static loads |
| **SMP (global)** | either (global) | possible | best of the two on average | clock sync + migration | dynamic loads |

**Optimal for average waiting time:** SJF, and SRTF among preemptive ones. Nothing beats them; RR,
priority and FCFS do not.

---

## Formulas

```
turnaround time   T_i = completion_i − arrival_i          (admitted → terminated)
waiting time      W_i = T_i − Σ CPU bursts − Σ I/O waits   (time spent READY)
                      = T_i − burst_i        when a process has one CPU burst
response time     R_i = first_dispatch_i − arrival_i       (admitted → 1st time RUNNING)

average           = (Σ over all n processes) / n

CPU utilisation   = Σ(execution time on each core) / (total time × number of cores)
throughput        = number of "exit" transitions / unit time

RR queue bound    waiting ≤ (n − 1) × q                    for n ready processes
context switches  = ceil(burst / q) − 1                    for one process, alone
RR plateau        average turnaround stops changing once q ≥ max burst (RR = FCFS then)
```

Note `W = T − burst` only for a **single CPU burst** with no I/O wait. With two bursts it is
`W = T − (burst1 + burst2)`.

---

## Worked numbers worth remembering

**FCFS, bursts 24 / 3 / 3, all at t = 0 (S11–S12).**
Order `P1,P2,P3`: waits `0, 24, 27` → **average 17**.
Order `P2,P3,P1`: waits `6, 0, 3` → **average 3**. Same jobs, same total time, 5× difference.

**Nonpreemptive SJF, arrival 0/2/4/5, burst 7/4/1/4 (S15).**
Timeline `P1 0–7 · P3 7–8 · P2 8–12 · P4 12–16`.
Waits `0, 6, 3, 7` → **average 4**.

**Preemptive SJF / SRTF, same four processes (S16).**
Timeline `P1 0–2 · P2 2–4 · P3 4–5 · P2 5–7 · P4 7–11 · P1 11–16`.
Waits `9, 1, 0, 2` → **average 3**.

**RR with q = 20, bursts 53 / 17 / 68 / 24, all at t = 0 (S19).**
Ten slices, last at 154–162. Waits `81, 20, 94, 97` → **average 73**;
turnarounds `134, 37, 162, 121` → average **113.5**; responses `0, 20, 37, 57`.

**Dual-core SRTF, the S16 processes (S28).**
Timeline core 1 `P1 0–4 · P3 4–5 · P1 5–8`, core 2 `P2 2–6 · P4 6–10`.
Waits `1, 0, 0, 1` → **average 0.5** (versus 3 on one core).

**Dual-core RR with q = 20, the S19 processes (S29).**
Waits `20, 0, 21, 37` → **average 19.5** (versus 73 on one core); last slice ends at **89**.

**Quantum vs context switches, one burst of 10 (S20).** `q = 12` → 0 switches, `q = 6` → 1,
`q = 1` → 9.

**Turnaround vs quantum (S21).** The notes give the plateau value: FCFS average turnaround
`(6 + 9 + 10 + 17)/4 = 10.5`. Intermediate quanta are *not* ordered — smaller `q` can be better or
worse.

---

## Ten things that decide exam marks

1. **Draw the Gantt chart.** Every waiting time is read straight off it; the average is then
   arithmetic you cannot get wrong.
2. **`W = T − burst`**, not "finish − burst". Waiting time excludes the process's own execution.
3. **FCFS is order-sensitive.** If a question changes the arrival order and the average does not
   change, you have made an error.
4. **SRTF preempts on *remaining* time**, not on the newcomer's total burst. Recompute the remaining
   time of the running process at every arrival.
5. **SJF ties**: equal bursts → earlier arrival first (S15 notes). Any tie-break keeps optimality;
   announce the rule you use.
6. **SJF/SRTF are optimal for average *waiting*, not for response time.** RR wins on response.
7. **RR: a process that finishes exactly at its quantum boundary does not re-queue.**
8. **`(n−1)q` is a bound on waiting, not a formula for it** — and it is not a turnaround formula.
9. **Small `q` costs context switches, not correctness.** Say "overhead", not "slower CPU".
10. **Dual-core ≠ halved time.** Two cores overlap work; the average falls (73 → 19.5 for RR,
    3 → 0.5 for SRTF) but the schedule must be re-derived; do not divide.

---

## What is *not* in this series

* **Multi-level *feedback* queue** (queues that processes migrate between) — the deck only has
  multilevel queue with static queues (S22–S23).
* **Real-time scheduling** (rate-monotonic, EDF, priority inversion) — that is
  [`../c6a`](../c6a), Part 6a.
* **Disk scheduling** (SSTF, SCAN, C-SCAN, LOOK) — that is [`../c12`](../c12), L12.
* **Deadlock** consequences of scheduling, and the **concurrency** inside the scheduler — L7 and
  L5–6 respectively.
* **Linux/Windows production schedulers** (CFS, O(1)) — only the Linux priority *range* `[-20, 20]`
  is mentioned (S17 notes).
* Numerical **simulation or queueing theory** (arrival rates, Little's law) — every example here is
  deterministic with known bursts.
