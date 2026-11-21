# Deadlocks — Things to Take Note Of

Exam-focused companion to [STUDY_GUIDE.md](STUDY_GUIDE.md): what the deck stresses, what is easy to
get wrong, and where the deck is unreliable. No new material.

There is **no recording** for this chapter, so every citation is a **slide number** (`S17`), never a
timestamp. The speaker notes ([`[NOTES]`](transcripts/01-deadlocks-slides.md)) are part of the
content — much of the reasoning exists only there.

---

## 1. What the deck repeatedly stresses

| Point | Slide | Why it matters |
|---|---|---|
| **The definition has three parts: blocked, holding, waiting — and the waiter must be in the set** | S04 | "Waiting for a resource" alone is not a deadlock; the closure of the waiting relation is |
| **The graph is the model; the cycle is the test** | S08–S13 | Every graph question is answered by "is there a cycle, and how many instances per type?" |
| **"Does this mean a cycle in the graph always indicates a deadlock?"** | S11 | Asked explicitly, answered on S13: **no** when a type has several instances |
| **The four conditions are necessary, but not sufficient** | S15 | The exact wording is on the slide, and the notes repeat it |
| **Violating any *one* condition prevents deadlock** | S15 notes | This is what makes prevention a checklist, not a mystery |
| **`Why do most systems use Ostrich approach? Efficiency.`** | S18 notes | The deck's answer to "why is there no deadlock handling in my OS?" |
| **Chopsticks are not shareable, "hence this condition cannot be eliminated"** | S20 | Mutual exclusion is usually *not* breakable; you must attack a different condition |
| **Order the chopsticks by ID: smaller first** | S22 | The one general-purpose prevention technique in the deck |
| **"What if multiple answers? Any one can be chosen."** | S30 | Any valid safe sequence earns full marks |
| **"Do we need to change Max? No."** | S36 notes | `Max` is the declared promise; only `Allocation`, `Need` and `Available` move |
| **"We should restore the old state."** | S37 notes | The pretend-allocation is a *transaction*: unsafe ⇒ undo it |
| **Detection is not examinable** | S03, S39 | `Due to the time constraint, we cannot cover all the details about deadlock detection` |

---

## 2. Exam traps

1. **A cycle does not imply deadlock when a resource type has several instances.** A cycle implies
   deadlock only if **every** type has exactly **one** instance. S12 is the counter-example
   (one cycle, no deadlock). Writing "cycle ⇒ deadlock" unqualified loses the mark.
2. **Safe ⇒ no deadlock, but unsafe ⇏ deadlock.** Unsafe means *no safe sequence exists*, and the
   sequence test assumes everyone holds resources until termination (S27 notes). An unsafe state can
   still finish if a process releases early.
3. **Banker's requires `Max` up front.** It is an *avoidance* algorithm; without declared maximum
   claims it cannot compute `Need` and cannot run. This is exactly why it is not used in real
   systems.
4. **`Max` never changes.** A granted request moves `Available ↓`, `Allocation ↑`, `Need ↓`. Writing
   `Max = Max − Request` is the single most common arithmetic error in this chapter.
5. **`Request` on S34 is not the `Request` column on S26.** S26's column is the *remaining need* —
   Banker's `Need`. `Request` is one pending ask. Also: S42's detection matrix has a `Request` column
   and **no** `Max`/`Need` at all.
6. **The four conditions are necessary, not sufficient.** Satisfying all four proves nothing;
   violating one proves there is no deadlock.
7. **Prevention ≠ avoidance ≠ detection.** Prevention removes a **condition** at design time;
   avoidance tests a **state** on every request and may deny it because of the future; detection lets
   the deadlock **happen** and repairs it. Only prevention names a condition.
8. **Safety uses `Need`; detection uses `Request`.** Swapping them turns one algorithm into the
   other — and gives a wrong answer for the question asked.
9. **The two algorithms initialise `Finish` differently.** Safety: `Finish[i] = false` for all `i`.
   Detection: `Finish[i] = false` only if `Allocation[i] ≠ 0`, otherwise `true` (a process holding
   nothing cannot be part of a deadlock).
10. **Safety answers "is the state safe?"; detection answers "which processes are deadlocked?"**
    A finished `Finish[i] == false` is a *deadlocked* `Pi`, not an "unsafe" one.
11. **`Need ≤ Work` is componentwise**, all `j` at once. Summing the vectors and comparing totals is
    wrong and produces safe sequences that do not exist.
12. **`Work` is not `Available`.** `Work` starts at `Available` and **grows**; comparing a request
    against the original `Available` (S37's notes say "cannot find `Needi < Available`" — it means
    `Work`) gets the wrong trace.
13. **Step-1 failure is an error, not a wait.** `Request_i ≰ Need_i` means the process broke its
    contract (it asked for more than its declared maximum). Only step 2 failing means "wait".
14. **Starvation is the residual risk of every strategy here.** All-or-nothing acquisition (prevention
    of hold-and-wait) and fixed-victim recovery (detection) can both postpone one process forever.
    Deadlock-freedom does not imply fairness — and the chapter title says "and Starvation" even
    though no slide defines it.
15. **Recovery costs more than the victims.** Backing one car off the bridge can force several to
    reverse (S05), and processes *depending on* a deadlocked process are affected too.
16. **A timeout is not prevention.** "Preempt if the philosopher cannot get the chopstick **for a long
    time**" (S21 notes) is a *recovery* trigger: the deadlock already happened and is then broken.
    Prevention must preempt **before** waiting.
17. **Request-edge direction.** `Pi → Rj` points **at the resource**; the assignment edge `Rj → Pi`
    points **at the holder**. Reversing them turns "P1 needs R1" into "P1 holds R1".
18. **The graph is a snapshot.** Deadlock is a property of a *state*; edges disappear when a request
    is granted and when a resource is released (S08). Do not reason about a graph as if it were the
    program.
19. **Single-instance ⇒ cycle detection suffices; multiple-instance ⇒ you need the matrix.** That is
    the split on S13/S39 and the reason Banker's exists at all.
20. **Show the `Work` column.** In a matrix question the marks are in the trace (which process was
    picked at each step and what `Work` became), not in the final sequence alone.

---

## 3. Known slips, typos and internal contradictions

| # | Slip | Slides | Correct version |
|---|---|---|---|
| 1 | **The chapter's own overview slide prints a stale lecture numbering**: `Synchronization (L4-5)` / `Deadlocks (L6)` | S02 | Parts 2 and 4 print the newer scheme, `Synchronization (L5-6)` / `Deadlocks (L7)`. This folder is `c7` to match the newer scheme. The stale slide also puts `Special: Real-time OS & virtualization (L7)` in the same L7 slot — the slot was reassigned between editions. |
| 2 | **Only the first outline slide says "not examinable"**: S03 prints `Deadlock Detection – not examinable`, but the five repeats (S06, S14, S17, S23, S38) print `Deadlock Detection` bare | S03 vs S06–S38 | Detection **is** not examinable; S39 states it again explicitly (*"This slide and the later slides in this chapter are not examinable"*). The repeats just dropped the annotation. |
| 3 | **S41's speaker notes are the safety-algorithm notes from S30**, pasted onto the detection slide: *"the algorithm determines whether the current system is in a safe state…"* | S30 vs S41 | S41 is the **detection** algorithm: `Request` not `Need`, `Finish` seeded from `Allocation == 0`, and the conclusion is "these processes are deadlocked", not "this state is unsafe". |
| 4 | **S07's speaker notes stop mid-sentence**: *"If the request is granted, the process uses the resource, and after sometime, r"* | S07 | The model is **request → use → release**, and release returns **all** the instances the process holds of that type. |
| 5 | **S37's notes compare `Need` against `Available`**: *"We cannot find `Needi < Available`"* | S37 | It is `Need_i ≤ Work`, and `Work` has already been reduced by the pretend-allocation. Same verdict here, but the wrong quantity. |
| 6 | **S26's column header `Request`** | S26 | That column is the **remaining need** (Banker's `Need`). `Request` is defined on S34 as a pending ask. |
| 7 | **S21's note softens preemption into a timeout**: *"if a philosopher cannot get another chopstick for a long time, preempt"* | S21 | For **prevention**, preempt immediately whenever the second chopstick is unavailable. A timeout is **detection + recovery**. |
| 8 | **S19's code is a typeset fragment**: ragged mixed-tab indentation, `eat` and `think` as bare statements, braces on their own lines | S19 | Read it as `while (1) { wait(chopstick[i]); wait(chopstick[(i+1)%5]); eat; signal(chopstick[i]); signal(chopstick[(i+1)%5]); think; }` |
| 9 | **S19's note says one context switch causes the deadlock**: *"Each philosopher executes the first line and a context switch occurs → deadlock"* | S19 | It needs **all five** to have completed their first `wait` before anyone performs the second. One switch is enough only if it is a switch *away* that lets the other four run. |
| 10 | **`V1<=V2 ≣ V1[j]<=V2[j]`** — the `≣` is a mangled `≡` | S34 | The definition is: `V1 ≤ V2` iff `V1[j] ≤ V2[j]` for **all** `j`. |
| 11 | **S30's steps lost their bullet numbers** in the extraction (`Find an i … go to step 4` appears as a bare paragraph) | S30 | It is the standard 4-step safety algorithm; see [STUDY_GUIDE](STUDY_GUIDE.md) §8.3 |
| 12 | **The extraction drops `→`, `≤` and `⇒` glyphs** | S08, S13, S30, S41 | `Pi  Rj` on S08 is `Pi → Rj`; `no cycles  no deadlock` on S13 is `⇒ no deadlock`; `Need[i,*]  Work` is `≤ Work`. Read the transcript with that in mind. |
| 13 | **Animated table columns land at the bottom of the extracted slide** — S32's `Need` values, S33's `Work` column, S36/S37's new `Available` and `Allocation` rows | S32, S33, S36, S37 | The numbers are correct; they are just detached from their cells. Reassembled in [STUDY_GUIDE](STUDY_GUIDE.md) §8.4–§8.9. |
| 14 | **S43 shows only a fragment of its `Work` table** (a single `0 0 0` row and a stray "Finished"), and S44 answers the rest in words | S43–S44 | The full trace is in [STUDY_GUIDE](STUDY_GUIDE.md) §9.5 |
| 15 | **S37 sets the `P4 → (2,3,0)` request as homework** with no answer | S37 | Answer: refused — the pretend state has `Available = (0,0,0)`, so nothing can be finished. Worked in [STUDY_GUIDE](STUDY_GUIDE.md) §8.10. |

---

## 4. Slides and diagrams: what the text alone does not convey

| Slide | Diagram | What to take from it |
|---|---|---|
| S09 | RAG legend | Circle = **process**; rectangle = **resource type**, with **one dot per instance**; arrow `Pi → Rj` = request; arrow from a **dot** to `Pi` = that instance is assigned to `Pi`. The dot matters — it is what makes multi-instance resources drawable. |
| S10 | Graph with **no cycle** | Three processes, four resource types (`R2` has 2 instances, `R4` has 3). Answer printed on the slide: **`P3 → P2 → P1`**. |
| S11 | Graph **with** a deadlock | **Two** cycles: `P2 ↔ P3`, and `P1 → P2 → P3 → P1`. The question *"does a cycle always indicate a deadlock?"* is the transition into S13. |
| S12 | Graph with a **cycle but no deadlock** | **One** cycle. The multi-instance resource is what saves it. Answer printed: **`P2 → P4 → P3 → P1`**. |
| S22 | Chopstick-ordering ring | Five chopsticks numbered **0–4** around the table, five philosophers **A–E** between them. **Black arrows = first request, yellow = second.** After ordering, every second request points the same way round the ring — that is the visual proof that no cycle can form. |
| S26 | `Available: 1` table | Three processes, each holding 1, requesting 1 / 2 / 3. The cumulative checks printed under the table *are* the safe-sequence condition. |
| S31–S33 | The `T0` matrices | `Allocation`, `Max` and `Available` on S31; `Need = Max − Allocation` filled in on S32; the `Work`/`Finish` trace animated on S33 with the answer `〈P1, P3, P4, P2, P0〉`. |
| S36–S37 | Request matrices | The **changed** row is highlighted, and the recomputed `Available` is shown underneath. S37's last state is the **restored** one, not the refused one. |
| S42–S44 | Detection matrices | Same layout as Banker's but with `Request` in place of `Max`/`Need`, and `Available = (0,0,0)` — so the first pass can only be started by a process whose `Request` is all zeros. |

**S01 is not content.** It is the "Comments are Welcome / online feedback systems (SFTs)" administrative
slide. Nothing on it is examinable.

---

## 5. Coverage map (S1–S45)

| Slides | Topic | Study guide § |
|---|---|---|
| S01 | Admin: SFT feedback | — |
| S02 | Course overview (stale lecture numbering) | — |
| S03 | Chapter outline (detection marked not examinable) | 0 |
| S04–S05 | Deadlock problem: definition, two-semaphore example, bridge crossing | 1 |
| S06 | Outline repeated | — |
| S07 | System model: resource types, instances, request/use/release | 2 |
| S08–S09 | Resource-allocation graph: `V`, `E`, request/assignment edges, drawing conventions | 3.1 |
| S10 | Graph 1 — no deadlock, order `P3 → P2 → P1` | 3.2 |
| S11 | Graph 2 — deadlock, two cycles | 3.2 |
| S12 | Graph 3 — cycle but no deadlock, order `P2 → P4 → P3 → P1` | 3.2 |
| S13 | Basic facts: cycle vs instances | 3.3 |
| S14 | Outline repeated | — |
| S15–S16 | The four conditions | 4 |
| S17 | Outline repeated | — |
| S18 | Three (four) ways to handle deadlocks; the ostrich approach | 5 |
| S19 | Dining philosophers with semaphores; how it deadlocks | 6.1 |
| S20 | Prevention: mutual exclusion (can't), hold-and-wait (all at once) | 6.2–6.3 |
| S21 | Prevention: no-preemption, circular-wait (four hungry / odd-even) | 6.4–6.5 |
| S22 | Chopstick ordering vs circular wait | 6.5 |
| S23 | Outline repeated | — |
| S24–S25 | Avoidance; safe state; definition of a safe sequence | 7.1–7.2 |
| S26 | `Available: 1` safety example, three questions | 7.3 |
| S27 | Safe / unsafe / deadlock states | 7.4 |
| S28 | Banker's algorithm: purpose and assumptions | 8.1 |
| S29 | Data structures: `Available`, `Max`, `Allocation`, `Need` | 8.2 |
| S30 | Safety algorithm | 8.3 |
| S31–S33 | Worked safety example → `〈P1, P3, P4, P2, P0〉` | 8.4–8.5 |
| S34–S35 | Resource-request algorithm | 8.6 |
| S36 | `P1` requests `(1,0,2)` → granted, `〈P1, P3, P4, P0, P2〉` | 8.7 |
| S37 | Second `(1,0,2)` refused; `P0` requests `(0,2,0)` → unsafe, restored; `P4` homework | 8.8–8.10 |
| S38 | Outline repeated | — |
| S39 | Detection idea; detection/recovery are **not examinable** | 9.1 |
| S40–S41 | Detection data structures and algorithm | 9.2–9.3 |
| S42 | Worked detection example — no deadlock | 9.4 |
| S43–S44 | `P2` requests one more `C` → deadlock `{P1, P2, P3, P4}` | 9.5 |
| S45 | Advanced readings | 15 |

Six slides (S03, S06, S14, S17, S23, S38) are the same outline; treat them as section dividers. The
real content is ~36 slides.

---

## 6. Memory hooks

* **"Hold, wait, circle"** — the definition in three words. If a process is waiting but nothing in the
  set is waiting on it, it is just slow.
* **"One instance, cycle = dead. Many instances, cycle = maybe."** The whole of S13.
* **"Safe means a sequence exists; deadlock means no sequence ever will."** Safe is a stronger,
  checkable claim; deadlock is the outcome.
* **"Banker lends only if every customer's worst case can still be met."** That is `Need ≤ Work`.
* **"`Max` is the promise, `Allocation` is the balance drawn, `Need` is what is left to draw."**
* **"`Work` = what is free now + what the finished ones handed back."** This is why `Work` grows.
* **"Request arrow points at what you want; assignment arrow points at who has it."**
* **"Prevention never asks; avoidance asks first; detection asks forgiveness; the ostrich doesn't
  care."**
* **"Small chopstick first"** — always climb the ladder from the same end and you can never meet
  someone coming down.
* **"Four hungry, five chopsticks"** — pigeonhole: someone always gets both.
* **"The victim's friends pay"** — bridge analogy; recovery is not local.

---

## 7. Quick self-check before the exam

- [ ] Can you state the definition of deadlock with all three clauses?
- [ ] Can you draw a RAG and label a request edge vs an assignment edge, including the instance dots?
- [ ] Can you explain — with the S12 counter-example — why a cycle does not always mean deadlock?
- [ ] Can you name the four conditions in order and say which one is usually unbreakable?
- [ ] Can you list four prevention techniques for dining philosophers and the price of each?
- [ ] Can you define a safe sequence formally (`Available + Σ holds of earlier processes`)?
- [ ] Can you do the `Available: 1` example and explain why `<P3, P2, P1>` fails?
- [ ] Can you compute `Need` from `Max − Allocation` for five processes without a slip?
- [ ] Can you run the safety algorithm to `〈P1, P3, P4, P2, P0〉` and show the `Work` column?
- [ ] Can you decide `Request1 = (1,0,2)` twice — grant, then refuse at step 1 — and say *why* the
      second is an error rather than a wait?
- [ ] Can you say what changes on a grant (three structures) and what does not (`Max`)?
- [ ] Can you explain why unsafe does not imply deadlock?
- [ ] Can you name the two ways recovery can starve a process?
- [ ] Can you state, in one sentence each, the difference between prevention, avoidance and detection?
