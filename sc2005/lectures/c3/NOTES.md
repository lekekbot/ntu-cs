# CPU Scheduling — Things to Take Note Of

The "before the exam" file: what the deck stresses, what is easy to get wrong, and where the slides
themselves are unreliable. It deliberately contains no new teaching — that is
[STUDY_GUIDE.md](STUDY_GUIDE.md).

Thirty slides, no audio, so every reference here is a **slide number** (`S17`).

---

## 1. What the deck repeatedly stresses

| Point | Where | Why it matters |
|---|---|---|
| **"In the exam, I encourage you to draw the Gantt chart to help your calculation"** | S11 notes | The chart *is* the method. Every waiting time is read off it; the average is then arithmetic |
| **Keep the CPU busy — that is the whole objective** | S03 | Every algorithm is judged by how well it refills idle cores |
| **Only two state transitions make scheduling mandatory (1 and 5)** | S05 | The standard "when does the scheduler run" question, with a printed answer |
| **Voluntary release defines nonpreemptive** | S06, S13 | If you cannot say *why* FCFS is nonpreemptive, you cannot classify any algorithm |
| **SJF/SRTF is optimal for average waiting time** | S14 | The only optimality result in the chapter; expect "prove/explain" |
| **The convoy effect is FCFS's defining flaw** | S13 | Two slides of worked numbers exist purely to show it |
| **A tie can be broken any way; optimality survives** | S15 notes | Removes an excuse for an ambiguous answer — but you must state the rule you used |
| **Starvation → aging** | S17, S23 | The same cure is needed by priority scheduling and by fixed-priority multilevel queues |
| **Small quantum ⇒ many context switches** | S20 | Quantified: burst 10 gives 0, 1, 9 switches for q = 12, 6, 1 |
| **"No well-defined relationship between average turnaround time and quantum size"** | S21 | A trap in both directions: you cannot say it improves *or* worsens monotonically |
| **Turnaround freezes once `q ≥ max burst`** | S21 | Because RR has then degenerated into FCFS |
| **Mapping processes to cores is NP-hard** | S26 | "Similar to the well-known knapsack problem" |
| **Global scheduling's price is real** | S30 | Clock sync + selection overhead + cache migration; the deck lists all three |

---

## 2. Exam traps

1. **`W = T − burst` is not a definition.** It is the shortcut for the deck's model (*one* CPU burst,
   no I/O — S10). With two bursts you must subtract both bursts **and** the I/O wait:
   `W = T − bursts − I/O`. Writing `W = T − burst` for a multi-burst process is the single most
   common lost mark.
2. **Waiting time is not "finish − burst".** It is measured from **arrival**, so `T = completion −
   arrival` comes first.
3. **Response time counts only the *first* dispatch.** Not the average start, not the first
   preemption. P3 in S19 has response 37 and waiting 94 — different numbers, same process.
4. **FCFS is order-sensitive.** If a question changes only the arrival order, the average *must*
   change (S11: 17, S12: 3). An unchanged answer means an arithmetic slip.
5. **Nonpreemptive ⇒ response = waiting.** True only because nothing is preempted; do not carry it
   into RR or SRTF.
6. **The convoy effect is caused by nonpreemption, not by "bad luck".** One long unpreemptable job
   adds its whole burst to everyone behind it.
7. **SRTF compares against the *remaining* time**, not the newcomer's original burst and not the
   runner's original burst (S14: "less than the remaining CPU burst").
8. **SRTF preempts on "less than", not "less than or equal".** An exact tie does **not** preempt.
9. **A process that finishes exactly at the quantum boundary does not re-queue.** S19's P2 needed 17
   of a 20-unit quantum; the next process starts at 37, not at 40.
10. **`(n − 1)q` bounds waiting, not turnaround.** S18 says "waiting time is no more than `(n−1)q`".
    Using it as a turnaround formula is wrong (turnaround includes the process's own burst).
11. **`q ≥ max burst` makes RR *equal* FCFS.** So "RR is always fairer" is false in that regime — and
    the average turnaround stops changing there.
12. **Do not claim turnaround improves monotonically as `q` shrinks.** S21 states there is **no**
    well-defined relationship; the S21 curve goes up and down before it plateaus.
13. **Context switches during a burst = `ceil(B/q) − 1`.** The `−1` is because the last slice ends
    with completion, not with a timer interrupt. Getting `ceil(B/q)` is the usual error.
14. **SJF optimality is about the *sum*.** It says nothing about the worst individual process, and it
    is exactly why SJF starves long jobs.
15. **A tie-break never changes the average.** State a rule (earliest arrival, per S15 notes) and move
    on; do not spend marks agonising.
16. **Smallest integer = highest priority** (S17). Linux `[-20, 20]`: `-20` is the *most* urgent.
    Inverting this silently reverses the whole chart.
17. **Aging destroys strict priority order** — that is its purpose. An answer that says "aging keeps
    the original priorities" contradicts itself.
18. **Two cores ≠ half the time.** Rebuild the chart. S28's core 2 idles 0–2 because only P1 exists;
    you cannot divide by 2 and be right.
19. **In dual-core SRTF, preempt the process with the *largest* remaining time**, so that the two
    smallest remain running. In S28 that is P1(3) at t = 4 — not P2(2).
20. **AMP vs SMP is not about preemption.** It is about whether the ready queues are **per-core**
    (partitioned) or **global**. Both can be preemptive.
21. **"Knapsack" is the deck's shorthand, not the precise problem.** Assigning bursts to cores is
    bin-packing; the deck says it is "similar to" knapsack (S26). Say "NP-hard; like bin-packing /
    knapsack" and you cannot be marked down.
22. **CPU utilisation's denominator carries the core count**: `Σ busy / (time × cores)`. Without it
    you can report > 100 %.

---

## 3. Known slips and rough edges in these slides

These are slide/extraction issues, not errors in the theory. Know the correct version.

| Where | What the slide/extraction shows | Correct reading |
|---|---|---|
| **All Gantt slides (S11, S12, S15, S16, S19, S28, S29)** | The chart is a set of independent text boxes, so the extracted text is an unordered pile: `P1 P3 P2 4 2 11 0 P4 5 7 P2 P1 16`, `0 33 48 4`, `3 0 0 0 0` | The numbers are **boundary labels** and **remaining bursts** (`33`, `48`, `4`, `13`, `28` on S19 are remainders). Every chart in the study guide is rebuilt from the arrival/burst table and checked against the printed average |
| **S19** | Prints the chart and the qualitative claim, but **no average waiting time** | The deck never states 73. It is derived in `STUDY_GUIDE.md` §5.2 and cross-checked four ways |
| **S29** | Prints the dual-core RR chart but **no average at all** | Derived (guide §7.5): average waiting **19.5**, turnaround **60**, response **9.25**. Contrast with 73 / 113.5 / 28.5 on one core |
| **S21** | The graph is an image; the only numbers in the text are in the notes: `FCFS = (6+9+10+17)/4 = 10.5` | Those are **turnaround times** in FCFS order, i.e. bursts **6, 3, 1, 7** for P1…P4. Any numeric answer about the curve must be presented as a reconstruction, not as the slide's printed data |
| **S05** | "Only 1 and 5" — but the five arrows are numbered only on the **L2** diagram | Whatever the numbering, the substance is: **exit and dispatch are mandatory**; run→wait, run→ready and wait→ready merely create opportunities |
| **S07 vs S07 notes** | Slide: "percentage of time during which the CPU cores are busy … (sum of execution time on each core) divided by (total time multiplied by number of cores)" — reads like two different definitions | They are the same quantity; the notes' version (`Σ exec / (total time × cores)`) is the unambiguous one. Use it |
| **S23** | Slide text: "each queue gets a fixed time quantum on the CPU (e.g. **80 ms for foreground, 20 ms for background**, and then repeat)"; notes: "**80 %** for foreground, **20 %** for background" | Same 80/20 split, described once as durations and once as shares. In an answer, call it a **share of CPU time** and give the ratio |
| **S15** | The tie between P2 and P4 (both burst 4) is invisible on the slide | The tie-break rule (**earliest arrival**) exists only in the speaker notes. Quote it, and note that any rule preserves optimality |
| **S17 notes** | Gives Linux's range as `[-20, 20]` | The slide only says "smallest integer implies highest priority". Both are examinable; the Linux range is the concrete example |
| **S02 notes** | The note is cut off mid-word (`"…we talk about IPC, inter-proc"`) and starts with `@in our last lecture` | That is a **recap of L2** (process creation/termination, IPC) spoken before the deck proper. No L3 content is lost |
| **S28** | The extraction shows a stray column `P1 P2 P3 P4 / 3 0 0 0 0` | It is a **remaining-time readout** at t = 4–5 (P1 has 3 left), which is exactly why P1 is the process preempted. Not a separate table |
| **S29 scope** | The slide sits under "Global Scheduling" but never says "one queue" | Read it against S27: one **global** ready queue, so each core takes the head when it frees. Per-core queues would give a different (partitioned) chart |
| **S16 numbering** | The slide prints `P2 … P1 … P2 … P1` labels in a jumbled order | The order is `P1 0–2 · P2 2–4 · P3 4–5 · P2 5–7 · P4 7–11 · P1 11–16`; only this reproduces (9+1+0+2)/4 = 3 |

**No arithmetic errors were found on the slides.** Every printed average checks out by hand:
`(0+24+27)/3 = 17`, `(6+0+3)/3 = 3`, `(0+6+3+7)/4 = 4`, `(9+1+0+2)/4 = 3`, `(1+0+0+1)/4 = 0.5`.
The problems are in the **presentation** (unattached Gantt labels, a missing answer on S19/S29), not
in the numbers.

---

## 4. Coverage map

| Slide | Topic | Section in the guide |
|---|---|---|
| S01 | Course overview; this folder = `Scheduling (L3)` | §0 |
| S02 | Chapter outline: basic concepts → criteria → algorithms (uni, multi) | §0 |
| S03 | CPU–I/O bursts; objective = keep the CPU busy via multiprogramming | §1.1 |
| S04 | Figure: alternating CPU and I/O burst sequence | §1.1 |
| S05 | CPU scheduler goal; five transitions; answer "only 1 and 5" | §1.2 |
| S06 | Nonpreemptive vs preemptive, defined by transitions | §1.3 |
| S07 | System-wide criteria: CPU utilisation, throughput | §1.4 |
| S08 | Timeline figure: turnaround / waiting / response | §1.4 |
| S09 | Per-process criteria; `W = T − bursts − I/O`; averages | §1.4 |
| S10 | The five uniprocessor algorithms; simplifying assumptions | §1.5 |
| S11 | FCFS, order P1/P2/P3 → average 17 | §2.2 |
| S12 | FCFS, order P2/P3/P1 → average 3 | §2.3 |
| S13 | FCFS properties; convoy effect | §2.4 |
| S14 | SJF and SRTF definitions; optimality claim | §3.1 |
| S15 | Nonpreemptive SJF worked example (arrivals 0/2/4/5) → 4 | §3.2, §3.5 |
| S16 | Preemptive SJF / SRTF on the same data → 3 | §3.3 |
| S17 | Priority scheduling; starvation; aging; Linux `[-20, 20]` | §4, §4.3 |
| S18 | RR rule, quantum 10–100 ms, `(n−1)q` bound, large/small q | §5.1 |
| S19 | RR q = 20 worked example (53/17/68/24); better response | §5.2, §5.3 |
| S20 | Smaller quantum ⇒ more context switches (burst 10) | §5.4 |
| S21 | Turnaround vs quantum: no monotone relation; plateau | §5.5 |
| S22 | Multilevel queue: foreground RR, background FCFS | §6.1 |
| S23 | Inter-queue policies: fixed priority (starvation) vs time slice | §6.2, §6.3 |
| S24 | Multiprocessor: partitioned (AMP) vs global (SMP); one core per process | §7.1 |
| S25 | AMP: per-core queues, per-core algorithm, easy extension | §7.2 |
| S26 | AMP issue: mapping, load imbalance, NP-hard, best-fit heuristic | §7.2 |
| S27 | SMP: global queues, pick on idle, process may migrate | §7.3 |
| S28 | Dual-core SRTF worked example → average 0.5 | §7.4 |
| S29 | Dual-core RR q = 20 worked example | §7.5 |
| S30 | SMP costs: clock sync, selection overhead, cache migration | §7.7 |

**Every slide S01–S30 is covered.** The densest clusters are S10–S21 (algorithms, 12 slides) and
S24–S30 (multiprocessor, 7 slides) — that is where exam calculation comes from.

---

## 5. Memory hooks

* **FCFS = the convoy.** One truck, everyone late.
* **SJF = shortest first, SRTF = shortest *left*.** The `R` in SRTF is **Remaining**.
* **Waiting = queue time only.** If it is not queued, it is not waiting.
* **Response = first look.** Turnaround = whole life. Waiting = time spent waiting in line.
* **RR = a queue of metered slices.** Nobody hogs the meter; everybody pays switches for it.
* **`q` too small → the OS spends its day switching; `q` too big → it is FCFS with extra steps.**
* **`ceil(B/q) − 1`**: the last slice is a *finish*, not a *timeout*, so subtract one.
* **`(n−1)q` is the worst-case wait, not the answer.**
* **Two cores, two at a time.** In SRTF keep the two smallest remaining; in RR keep the two oldest
  queued.
* **AMP = assigned seats; SMP = free seating.** Assigned seats need a seating plan (NP-hard); free
  seating costs you your warm cache when you move.
* **70/20/10:** roughly how the marks split — 70 % chart-and-average arithmetic, 20 % definitions and
  comparisons, 10 % the multiprocessor discussion.

---

## 6. Self-check before the exam

- [ ] Can you define CPU burst, I/O burst, and say why multiprogramming is needed?
- [ ] Can you state the scheduler's goal and the five transitions, and justify "only 1 and 5"?
- [ ] Can you classify any algorithm as preemptive / nonpreemptive *and say why*?
- [ ] Can you define turnaround, waiting and response time, and convert between them?
- [ ] Can you reproduce FCFS on 24/3/3 in both arrival orders and explain the 17 vs 3 gap?
- [ ] Can you do nonpreemptive SJF on the 0/2/4/5 arrival set and get average 4?
- [ ] Can you do SRTF on the same set, including the remaining-time table, and get average 3?
- [ ] Can you state and prove (exchange argument) why SJF is optimal?
- [ ] Can you state the tie-break rule and why it cannot change the average?
- [ ] Can you draw the RR q=20 chart with all ten slices and compute 73 / 113.5 / 28.5?
- [ ] Can you compute context switches with `ceil(B/q) − 1` and turn it into an overhead percentage?
- [ ] Can you state the two S21 claims without contradicting yourself?
- [ ] Can you describe the two inter-queue policies and their flaw/benefit?
- [ ] Can you draw both dual-core charts (SRTF → 0.5, RR → 19.5) without dividing by two?
- [ ] Can you list the three costs of global scheduling and the one problem partitioned scheduling
      cannot solve?

---

## 7. What is *not* in this deck (do not import it)

* **Multilevel *feedback* queue** — the queues here are static; no migration between them (S22–S23
  never mention it).
* **Real-time scheduling** (rate-monotonic, EDF, priority inversion) — Part 6a, [`../c6a`](../c6a).
* **Disk scheduling** (SSTF, SCAN, C-SCAN, LOOK) — L12, [`../c12`](../c12). Only FCFS is shared, and
  the metrics are different (cylinders, not milliseconds).
* **Deadlock** and the **synchronisation** of a shared ready queue — L7 and L5–6.
* **Burst prediction** (exponential averaging) — mentioned only as the reason SJF is hard to use, not
  taught here.
* **Priority inversion / inheritance** — a real-time concern, not part of this chapter.
