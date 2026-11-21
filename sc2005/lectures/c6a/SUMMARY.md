# Real-Time OS — Summary (one page)

Part 6a, 19 slides, one question: **how does an OS guarantee that an answer arrives before its
deadline?**

---

## The 60-second version

1. A **cyber-physical system** is a physical system monitored and controlled by a computing core —
   cars, avionics, robots, medical devices (S03). Its common loop is *sense → run the control law →
   actuate* (S04).
2. The output must be produced **within a pre-defined time** = the **deadline**. So correctness has
   **two** halves: functional **and** temporal (S04, S07).
3. **Real-time ≠ fast.** Real-time means **predictable in the worst case**, not fast on average
   (S06). *"Man drowned in a river with average depth 20 cm."*
4. An **RTOS** is an OS that provides its services so that those deadlines can be **guaranteed**
   (FreeRTOS, MicriumOS). Its key performance measure is **timeliness / predictability**, not
   throughput or average response time (S07).
5. A real-time process is specified as **`<R,C,D>`**: released at *R*, needs *C* units of CPU
   **inside** `[R, R+D)` (S09). Recurrent processes repeat; a **periodic** one is **`<T,C,D>`**,
   released at `0, T, 2T, …` (S10, S11).
6. **Classic algorithms fail** because none of them looks at deadlines: FCFS, SJF and RR all miss
   deadlines on the S13 set (S13).
7. **Fixed priority** = one priority per process, fixed across all its instances (S15).
   **Rate Monotonic** gives the **shorter period the higher priority** (S16).
8. RM **ignores `D`**, so it can run a less urgent instance first and miss a deadline (S17).
9. **EDF** is **dynamic**: at every instant it runs the instance with the **earliest absolute
   deadline** `R+D` (S18). It meets the deadline RM missed.
10. **RM is simpler and predictable under load; EDF is more powerful but needs online sorting and is
    unpredictable under load** (S19). That trade-off — not raw "which is better" — is the exam
    answer.

---

## RM versus EDF

| | **Rate Monotonic (RM)** | **Earliest Deadline First (EDF)** |
|---|---|---|
| Priority type | **Static / fixed** — assigned per process, constant across instances | **Dynamic** — recomputed per instance from its absolute deadline |
| Rule | shorter `T` (period / minimum release separation) ⇒ higher priority | earliest `R+D` (release **and** relative deadline) ⇒ higher priority |
| Ties | broken arbitrarily | broken arbitrarily |
| Complexity (S19) | **simple** — one priority queue per recurrent process; O(1) with bitmaps | **harder** — needs **online sorting** of the ready queue; best known O(log n) |
| Predictability (S19) | **predictable for high-priority processes even under high load** | **can be unpredictable under high load** |
| Utilisation bound | **none stated in this deck** — see the honesty note | **none stated in this deck** |
| Under overload | high-priority processes keep meeting deadlines; the **lowest-priority** ones miss | deadlines can be missed by **any** process, including high-priority ones |
| Popularity (S16, S18, S19) | "a very popular short-term CPU scheduler in the real-time CPS industry" | "more powerful than RM" (S18), yet the harder one to deploy |

> **Honesty note.** The Liu & Layland bound `n(2^(1/n) − 1)` is **not on any slide** — external
> knowledge, not examinable in that form for this deck.

---

## Notation

```
<R, C, D>   R = release time            process is available from R
            C = execution requirement   worst-case CPU time needed (one CPU burst)
            D = relative deadline       must finish by R + D

instance k of <T, C, D>:   release = kT          absolute deadline = kT + D

deadline met  <=>  completion time <= release + D

CPU utilisation            U = sum over processes of C_i / T_i
necessary condition        U <= 1   (not sufficient when D < T)
```

The deck assumes **one CPU burst per instance** and a **single (uni)processor** (S09, S14).

---

## Worked numbers worth remembering

**S13 — why classic algorithms fail.** `P1<0,20,30>`, `P2<0,5,10>`, `P3<5,10,35>`, `P4<20,10,30>`,
`P5<25,5,10>`. Total demand **50** units, and the last deadline is at 50 → the CPU may never idle.

| Algorithm | Order | Missed |
|---|---|---|
| FCFS | P1 0–20, P2 20–25, P3 25–35, P4 35–45, P5 45–50 | **P2** (by 15), **P5** (by 15) |
| SJF | P2 0–5, P3 5–15, P1 15–35, P5 35–40, P4 40–50 | **P1** (by 5), **P5** (by 5) |
| RR q=5 | P1 P2 P1 P3 P1 P3 P1 P4 P5 P4 | **P1** (done 35, d 30), **P5** (done 45, d 35) |

Every one of them misses two deadlines. Ordering by urgency (`P2, P1, P5, P3, P4`) misses none.

**S17 — the modified set** `P1<10,6,10>`, `P2<19,4,19>`, `P3<20,2,14>` (P3's `D` cut from 20 to 14).

```
RM   0-6 P1 | 6-10 P2 | 10-16 P1 | 16-18 P3 <- needs 14, finishes 18: MISS
EDF  0-6 P1 | 6-8 P3  | 8-12 P2  | 12-18 P1  ... P3 done at 8: MET
```

One difference at `t = 6` decides it: RM must serve P2 (period 19 beats period 20); EDF compares
deadlines (14 beats 17) and serves **P3**.

---

## Ten things that decide exam marks

1. **Real-time ≠ fast.** Say "predictable in the worst case", never "fast".
2. A missed deadline is a **correctness failure**, not a performance problem.
3. `<R,C,D>`: `R` is a *time*, `C` is a *worst-case CPU requirement*, `D` is *relative*.
4. The instance window is **half-open**: `[R, R+D)`. Finishing exactly at `R+D` is **on time**.
5. `T` is a period, so a `<T,C,D>` process is really an infinite family of `<kT, C, D>` instances.
6. **RM = static, by period; EDF = dynamic, by absolute deadline.** `D` is *not* the EDF priority;
   `R+D` is.
7. RM is simple (per-process queue) — that is *why* industry uses it, not because it is optimal.
8. RM can miss a deadline **even when a feasible schedule exists** — S17 is that proof.
9. Both are **preemptive**: a newly released higher-priority instance interrupts the CPU at once.
10. Under overload RM fails **lowest priority first**; EDF can fail **anywhere**. That asymmetry is
    the whole point of S19.

---

## What is *not* in this series

* A **Rate Monotonic utilisation bound** — not on the slides (see the honesty note).
* **Deadline Monotonic** (priority by `D`) — mentioned only as "RM/DM" in the S19 speaker notes,
  never defined.
* **Sporadic** processes get no slide of their own; S10 promises "two broad types" and only
  periodic arrives. S14/S16 notes say the same techniques apply to sporadic ones.
* No **response-time analysis**, no blocking/priority inheritance, no shared resources, no
  multiprocessor scheduling, no aperiodic servers.
* No **virtualisation** — that is Part 6b, the two loose files one level up.
* No worked **EDF optimality proof** and no **feasibility test** beyond "can you draw a schedule
  that meets every deadline".
