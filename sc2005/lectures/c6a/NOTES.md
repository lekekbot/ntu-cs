# Real-Time OS — Things to Take Note Of

The "before the exam" file for Part 6a: what the deck stresses, what is easy to get wrong, and where
the slides themselves are unreliable. It contains **no new teaching** — that is in
[`STUDY_GUIDE.md`](STUDY_GUIDE.md).

The deck is 19 slides with **no recording**, so "where" is always a slide number.

---

## 1. What the deck repeatedly stresses

| Point | Slide | Why it matters |
|---|---|---|
| **"Real-Time ≠ Fast. Real-Time = Predictable even in the worst-case"** | S06 | The most quotable line in the deck, and the one that decides whether an answer is right. Every later design choice (RM's static priority, "predictability under high load") follows from it. |
| **Correctness has two halves** — functional **and** temporal | S04 note, S07 definition | A correct-but-late answer is a **failure**, not a slow success. |
| **Key measure = timeliness / predictability**, not throughput or average response | S07 | This is the explicit replacement for the c3 metrics. |
| **Deadlines come from the application, not the OS** | S05, S07 | The OS can only be *given* `R`, `C`, `D`. |
| **RM ignores `D`** | S17 (title and note) | The single sentence that explains the whole S17 failure. |
| **EDF assigns priority by instance deadline, not by `D`** | S18 | Written in capitals on the slide: "NOT the same as parameter D". |
| **RM is simple and predictable under load; EDF is powerful but unpredictable under load** | S19 | The trade-off *is* the exam question, not a preamble to "EDF wins". |
| **Worst case must include mechanics and communication**, not just CPU | S07 note | The bound is end-to-end. |

---

## 2. Exam traps

1. **"Real-time means fast."** Wrong. Real-time means **bounded worst case**. A slow system with a
   provable 10 ms bound is real-time; a fast one with a 100 ms tail is not.
2. **A missed deadline is a correctness failure**, not a performance issue. Never write "the response
   time got worse"; write "the instance missed its deadline and the system is incorrect".
3. **`D` is relative.** The deadline is `R + D`. For `P3<5,10,35>` that is **t = 40**. Every wrong
   answer in this chapter usually starts here.
4. **EDF's priority is `R + D`, not `D`.** Two instances of the same process share `D` and still have
   different EDF priorities. RM, by contrast, gives them the *same* priority forever.
5. **RM is static, EDF is dynamic.** "Fixed priority" is fixed **per process across all its
   instances** (S15) — not "fixed once the system starts running".
6. **RM is not globally optimal.** S17 is the counter-example: a feasible schedule exists and RM
   misses. What you may say is weaker and safer — *RM is the best you can do without looking at `D`*.
7. **Changing `D` does not change an RM schedule you have already drawn.** Priorities depend only on
   `T`, so S17's timeline is character-for-character S16's. Many students re-order the timeline and
   lose the point.
8. **Do not forget preemption.** Both algorithms are preemptive: a released instance that wins the
   comparison takes the CPU *immediately*, and the interrupted one resumes with its **remaining** `C`.
9. **Finishing exactly at the deadline is on time.** `[R, R+D)` is the window; completion at `R+D`
   meets it. (P4 in the S13 set finishes exactly at 50 and is correct.)
10. **`T` is a period, not a deadline.** In `P<10,5,7>` the period is 10 and the deadline is 7. Writing
    "period 7" is an instant mark loss.
11. **"EDF is more powerful" ≠ "use EDF".** S18's note says more powerful; S19 immediately explains why
    industry still picks RM. An answer that stops at "EDF is better" has thrown away the slide.
12. **"Predictable under high load" means the *failure mode* is predictable**, not that deadlines are
    met. Under overload somebody must fail; RM chooses the lowest-priority process in advance, EDF
    does not.
13. **`U ≤ 1` is necessary, not sufficient**, when `D < T`. Say "the set is not schedulable" only when
    `U > 1`; otherwise draw the schedule.
14. **The S13 processes are not periodic.** They are five one-shot `<R,C,D>` jobs with `R` given per
    process. The periodic problem starts at S14. Mixing the two gets the instance arithmetic wrong.
15. **All three classic algorithms miss two of five deadlines** on S13. Do not claim FCFS "works
    better" because it finishes P4 early — count deadlines, not earliness.
16. **Ties are arbitrary** under both RM (equal periods) and EDF (equal deadlines). Say so rather than
    inventing a rule.
17. **Do not quote a Rate Monotonic utilisation bound as slide content.** The deck never states one
    (see §7). It is external knowledge and not examinable in that form here.

---

## 3. Slips and inconsistencies in the deck

Learn the correct version; do not reproduce the slip.

| Where | What the slide says | What is right |
|---|---|---|
| **S08 header** | **"Part 5: Real-Time OS & Virtualization"** | It is **Part 6a**. S02 and S12 both label the same outline "Part 6a"; S08 is a stale copy with the old part number (and the old title, with "Virtualization" appended). |
| **S02 speaker note** | Ends with "Finally, we take a look at some of the techniques for **hardware virtualization**…" | That paragraph is the **Part 6b** introduction. Part 6a stops at S19 and never mentions virtualisation again; the note was copied from the combined deck. |
| **S10 speaker note** | "Depending on the nature of repetition, there are **two** broad types… We will look at these in the next couple of slides." | Only **periodic** gets a slide (S11). The second type, **sporadic**, appears only inside the phrase "periodic/sporadic" on S14 and S16 — it is never defined. |
| **S15 speaker note** | "We will look at **two examples** of this class of schedulers." | Only **Rate Monotonic** is presented as a named algorithm (S16). The second is presumably Deadline Monotonic (DM), which is never defined; the S19 note mentions "RM/DM" in passing, also undefined. |
| **S18 process set** | Silently changes **P2 from `<19,4,19>` to `<19,4,17>`** | No explanation is given. It is harmless (P2 meets both), but a student copying S17's set into the EDF question will get a *slightly* different timeline. Quote the set you are using. |
| **S07 title vs text** | Heading "Real-Time CPS / Real-Time OS", but the "Definition:" line defines a **real-time system** | The definition given is of the *system*; the RTOS is the second bullet ("provides OS services to such systems"). Do not answer "an RTOS is a system whose correctness depends…". |
| **S13 / S14 / S16 / S18 Gantt figures** | Bar labels come out of the text extractor **out of time order** (S13's round-robin row reads `P1 P1 P1 P1 P2 P5 P4 P4 P3 P3`) | The figures are drawn as per-process rows, so extraction scrambles them. The **multiset** of bars matches a hand trace, so the schedules are correct — rebuild them yourself (STUDY_GUIDE §3.3–§3.5, §5.3, §6.1). |
| **S13 FCFS row** | Its label order (`P1 P2 P5 P3 P4`) puts P5 ahead of P3, which FCFS by arrival cannot do | FCFS by arrival is `P1 P2 P3 P4 P5`. The verdict is unaffected (P2 and P5 miss either way). |
| **S19 speaker note** | "…where `n` is the number of" | Sentence is **truncated** in the deck. The missing phrase is "processes/tasks". |
| **S03, S04, S09 speaker notes** | All end mid-word ("to inter-o…", "which is …", "How often or when the appli…") | Truncated boxes, not lost content that you are expected to reconstruct. |
| **S09** | `<R,C,D>` is called a "real-time process", and S10 then says *each instance* of a recurrent process is one | Both uses are standard, but be precise in an answer: `<R,C,D>` is an **instance/job**; `<T,C,D>` is the **process**. |

---

## 4. Slide numbering and lecture numbering

All citations here are slide numbers `S01`–`S19`. Two numbering traps sit in the deck itself:

1. **S01's course map uses an older lecture scheme.** It prints `Synchronization (L4-5)`,
   `Deadlocks (L6)`, `Memory organization (L8)`, `Virtual memory (L9-10)`, `Filesystems (L11)`,
   `I/O & disk (L12)`, and `Special: Real-time OS & virtualization (L7)`. The newer scheme printed on
   the Part 2 and Part 4 overview slides is **`Synchronization (L5-6) / Deadlocks (L7)`**.
2. **The two schemes collide on L7.** Under the old map, deadlocks are L6 and the special topic is L7;
   under the new map, deadlocks are L7. Two different topics cannot both be L7, which proves S01 was
   never updated after the renumbering.

Practical rule: **cite this material by part and slide ("Part 6a, S17"), not by lecture number.**
The sibling folders in `../README.md` use the newer scheme.

---

## 5. Coverage map

| Slide | Topic |
|---|---|
| S01 | Course overview — where the special topic sits (older lecture numbers) |
| S02 | Part 6a outline: what is an RTOS → specification → scheduling (note leaks into 6b) |
| S03 | Cyber-physical systems: definition, four domains, "systems of systems" |
| S04 | Relevance of real-time: sense → control law → actuate; two examples |
| S05 | What is a "reasonable time"? functionality / environment / failure mitigation |
| S06 | Common misconception: real-time ≠ fast; the river quotation |
| S07 | Definition of a real-time system and an RTOS; four performance bullets |
| S08 | The part outline again — **with the wrong part number** |
| S09 | `<R,C,D>`: release time, execution requirement, relative deadline; single CPU burst |
| S10 | Recurrent real-time processes; each instance is an `<R,C,D>` |
| S11 | Periodic processes `<T,C,D>`; released at `0, T, 2T, …`; example `P<10,5,7>` |
| S12 | Scheduling section outline: fixed-priority vs dynamic-priority |
| S13 | Why classic algorithms fail: FCFS, SJF, RR(q=5) on five one-shot processes |
| S14 | The scheduling problem statement; running example `P1<10,6,10>`, `P2<19,4,19>`, `P3<20,2,20>` |
| S15 | Fixed-priority scheduling; the "newer instance outranks an older one" chain |
| S16 | Rate Monotonic: shorter `T` = higher priority, ties arbitrary; schedule of the example |
| S17 | RM and deadlines: `P3<20,2,14>` → deadline miss; RM ignores `D` |
| S18 | Earliest Deadline First; dynamic priority by instance deadline; `≠ D` |
| S19 | RM vs EDF: implementation cost and predictability under high load |

---

## 6. Memory hooks

* **The river.** Average depth 0.2 m, one 2 m hole. *Predictable, not fast* — say it in every answer
  about what real-time means.
* **`<R, C, D>` = "Released, Costs, Due".** Released at `R`, costs `C`, due `R+D`.
* **RM = "Rate" Monotonic.** Rate = 1/period. The faster the beat, the higher the priority.
* **EDF reads the calendar; RM reads the contract.** EDF looks at *this instance's* due date; RM looks
  at the *process's* standing agreement (its period) and never re-reads it.
* **RM is a fixed-rent tenant, EDF is a daily booking.** One priority forever vs re-decided at every
  release.
* **The S17 "one decision".** At `t = 6`: RM compares `19 < 20`; EDF compares `14 < 17`. Whoever reads
  the deadline saves P3.
* **Overload: RM sacrifices the tail, EDF spreads the pain.** That is the whole of S19 in seven words.
* **Starvation** is the [`../c7`](../c7) word for what S17 shows: P3 is outranked, so it misses again
  and again, not once.

---

## 7. What the deck does not say

* **No Rate Monotonic utilisation bound.** The Liu & Layland result `n(2^(1/n) − 1)` is **not on any
  slide** and is not examinable in that form here — quote it only as external knowledge, if at all.
* **No Deadline Monotonic** definition, despite the S15 "two examples" promise and the S19 "RM/DM"
  mention.
* **No sporadic-process slide**, no aperiodic servers, no response-time analysis.
* **No shared resources**: no blocking, no priority inversion, no priority inheritance or ceiling —
  even though S09's single-burst assumption is exactly what makes them unnecessary here.
* **No multiprocessor scheduling**, no utilisation bound of any kind.
* **No virtualisation** — that is Part 6b, the two loose files one level up in `lectures/`.

---

## 8. Quick self-check before the exam

- [ ] Can you state the definition of a real-time system in one sentence, naming **both** halves of
      correctness?
- [ ] Can you explain the river quotation in two sentences without using the word "fast"?
- [ ] Can you convert `<T,C,D>` into releases and absolute deadlines for `k = 0,1,2`?
- [ ] Can you draw FCFS, non-preemptive SJF and RR(q=5) for the S13 set and name **which** two
      deadlines each one loses?
- [ ] Can you compute `U` for the S14 example and say why 0.911 leaves no room for error?
- [ ] Can you reproduce the S16 RM timeline from 0 to 20, including both preemptions?
- [ ] Can you explain, in one sentence, why **changing `D` does not change an RM schedule**?
- [ ] Can you name the instant (t = 6) and the two numbers (14 and 19) at the heart of S17?
- [ ] Can you run EDF on the same set and show P3's first instance finishing at 8 instead of 18?
- [ ] Can you give S19's two RM claims and two EDF claims, and say what "predictable under high load"
      actually buys a designer?
- [ ] Can you state `U ≤ 1` as a *necessary* condition without claiming it is sufficient?
