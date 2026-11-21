# SC2005 — Deadlocks: Study Guide

Companion to the deck **`Part5 (Deadlocks).pptx`** in this folder. There is no recording for this
chapter, so citations are **slide numbers**: **`S17`** means slide 17 of the 45-slide deck.

Transcript: [01 — slide deck S1–S45](transcripts/01-deadlocks-slides.md) (verbatim, `[NOTES]` =
speaker notes).

---

## 0. The chapter in one picture

Everything in these 45 slides answers one question:

> Several processes each **hold** something and each **want** something that another one holds.
> **When is the system stuck, how do you prove it, and what do you do about it?**

The deck's own answer is a tree of strategies:

```
                     a process wants a resource somebody else holds
                                        |
        +----------------+--------------+--------------+----------------+
        |                |                             |                |
   PREVENTION        AVOIDANCE                  DETECTION +         IGNORE
   break one of      never let the state        RECOVERY            (ostrich)
   the 4 conditions  become unsafe              let it happen,      do nothing
        |                |                      find it, fix it          |
   design-time      on every request          periodically after    most real OSes
   restriction      (Banker's algorithm)      the fact              incl. UNIX
        |                |                             |                |
   condition is     state is tested          graph cycle /        a rare hang
   always false     BEFORE granting          Request <= Work      is accepted
```

and in the middle of that tree sits the one idea that decides most exam marks:

```
   no cycle in the resource-allocation graph        ->  definitely no deadlock
   cycle, one instance per resource type            ->  definitely deadlock
   cycle, several instances per resource type       ->  MAYBE deadlock  -> need the matrices
```

Blocks of the deck:

| § | Slides | Topic | Why it matters |
|---|---|---|---|
| 1 | S04–S05 | The **deadlock problem**: definition, two-semaphore example, bridge crossing | the definition is quoted verbatim in exams |
| 2 | S07 | **System model**: resource types, instances, request/use/release | gives you the vocabulary the algorithms use |
| 3 | S08–S13 | **Resource-allocation graph** and the three worked graphs | *the conceptual core* |
| 4 | S15–S16 | The **four conditions** | necessary, not sufficient — the phrase is examined |
| 5 | S18 | **Handling strategies** (prevention / avoidance / detection / ignore) | the map for everything after it |
| 6 | S19–S22 | **Prevention**, on dining philosophers | standard "how would you prevent X?" answer |
| 7 | S24–S27 | **Avoidance**: safe state, safe sequence, safe vs unsafe | sets up Banker's |
| 8 | S28–S37 | **Banker's algorithm**: safety + resource-request | *the calculation question* |
| 9 | S39–S44 | **Detection** (multiple instances) | **not examinable**, kept for contrast |
| 15 | S45 | Advanced readings | — |

S01 (feedback-survey admin) and S02 (course overview) carry no examinable content; the outline slide
appears **six** times (S03, S06, S14, S17, S23, S38) as a section divider.

---

## 1. The deadlock problem (S04–S05)

### 1.1 The definition (S04)

> **Deadlock**: a set of **blocked** processes, each **holding** a resource and **waiting** to acquire
> a resource held by another process **in the set**.

Three clauses, and the third is the one people drop:

| Clause | What it rules out | What it means in the graph |
|---|---|---|
| **blocked** | a process that is merely slow or runnable | no outgoing request edge |
| **holding** | a process waiting for its first resource | it is the source of at least one assignment edge |
| **waiting for a holder *in the set*** | ordinary queuing in front of a resource | the waiting relation is **closed** — it forms a cycle |

A process queueing behind another process is not a deadlock. A **set** of processes each queueing
behind another **member of that set** is — because then no member can ever release, so no member can
ever proceed.

### 1.2 Example 1 — two tape drives (S04)

> *System has two different types of tape drives; both P1 and P2 need the two tapes to finish
> execution. P1 and P2 each hold one tape drive and need the other.*

```
        P1 --holds--> [ tape A ]  <--needs--  P2
        P2 --holds--> [ tape B ]  <--needs--  P1
```

Note the wording "**two different types** of tape drives". So this is **two resource types with one
instance each**, not one type with two instances. That distinction matters: with **one instance per
type**, the cycle in the graph is *sufficient* for deadlock (§3.3). If the two drives were identical
instances of one type, P1's need could be satisfied by the drive P2 is holding only after P2
releases — but the *reasoning* has to go through the multi-instance rule, and the answer would no
longer follow from the cycle alone.

### 1.3 Example 2 — two semaphores (S04)

> Semaphores `A` and `B`, initialised to 1. Both processes need both.

```
   P0                     P1
   wait(A);               wait(B);
   wait(B);               wait(A);
```

The slide marks **"Context switch points"** between the two statements. With the switches in the
worst places, the trace is:

| Step | Process | Action | `A` | `B` | State |
|---|---|---|---|---|---|
| 1 | P0 | `wait(A)` — succeeds, `A: 1 → 0` | 0 | 1 | P0 holds A |
| 2 | — | **context switch to P1** | 0 | 1 | |
| 3 | P1 | `wait(B)` — succeeds, `B: 1 → 0` | 0 | 0 | P1 holds B |
| 4 | P1 | `wait(A)` — **blocks** (A = 0) | 0 | 0 | P1 waits for P0 |
| 5 | — | context switch to P0 | 0 | 0 | |
| 6 | P0 | `wait(B)` — **blocks** (B = 0) | 0 | 0 | P0 waits for P1 |

Now P0 holds `A` and waits for `B`; P1 holds `B` and waits for `A`. Neither can reach its `signal`.
This is the same example as the synchronization chapter — the deck's note says *"We have seen this
example in the previous chapter"* — and it is the reason deadlock is taught immediately after
semaphores: **the bug is not in `wait()`; it is in the order the two processes acquire.**

Three observations to carry forward:

* the deadlock needs a **particular interleaving** — the same code usually runs fine;
* it needs **both** processes to hold one resource each, which is exactly **hold-and-wait**;
* it disappears if both processes acquire in the **same order** — the fix that becomes
  "chopstick ordering" on S22.

### 1.4 The bridge-crossing analogy (S05)

> *Only one car is allowed on the bridge. The bridge can be viewed as a shared resource. If a deadlock
> occurs, it can be resolved if one car backs up (release resource, i.e. the bridge, and rollback).
> Several cars may have to be backed up if a deadlock occurs.*

```
   ============ bridge: ONE car at a time ============
        car A  -->                               <--  car B
                        (meet in the middle)
```

The mapping is exact:

| Bridge | Operating system |
|---|---|
| car | process |
| bridge | a resource with **one instance** (mutual exclusion is inherent — two cars physically cannot pass) |
| car entering the bridge | `wait(bridge)` — the request was **granted** |
| car halfway across | **holding** the resource, partway through its critical section |
| "back up" | **release + rollback**: undo the partial work, not just release |
| several cars backing up | recovery costs fall on processes that were **not** deadlocked |

Three lessons the deck puts in the notes rather than the bullets:

1. **Recovery is not a `signal()`.** Backing up means *undoing progress*. In a real system that means
   checkpoint/rollback — you cannot "un-write" a half-finished file update just by freeing a lock.
2. **Recovery spreads.** *"Not only the process in the deadlock state are affected, but also other
   processes that have dependency on the deadlocked process."*
3. **Mutual exclusion is a property of the physical resource here.** No protocol can let two cars
   pass. So this is the standard illustration of a condition you *cannot* remove — which is exactly
   the point S20 makes about chopsticks.

---

## 2. System model (S07)

The graph and both algorithms need a precise model, and S07 gives it in three lines.

**Resource types** `R1, R2, …, Rm` — *"Memory space, I/O devices, semaphores, etc."*
**Instances** — each type `Ri` has `Wi` **identical** instances.

> *"For example, we have two hard disks in the system. `Ri` is the hard disk and `Wi = 2`. The
> instances are all identical."*

**Protocol** — a process uses a resource in exactly three steps:

| Step | Action | Effect on the graph |
|---|---|---|
| 1 | **Request** a *specific number* of instances | add request edge `Pi → Rj` |
| 2 | **Use** — only if the request was granted; otherwise the process **waits** | request edge stays until granted |
| 3 | **Release all the instances** | remove the assignment edge |

Two consequences that the whole chapter depends on:

* **Instances of a type are interchangeable.** So the state is a *count*: "P1 holds 2 of the 3
  instances of `R1`", never "P1 holds the second drive". This is what lets S29 and S40 describe the
  state as **vectors and matrices of integers**.
* **Requests are quantitative.** *"Request for a specific number of instances"* — a process may ask
  for several units at once. That is why `Request_i` is a vector, and why the algorithms compare
  vectors componentwise.

What the model deliberately leaves out: **time** (nothing says how long a hold lasts), **priority**
(instances have no owner preference), **fairness** (nothing prevents starvation), and **resource
identity** (identical instances). Keep that list in mind whenever an exam question asks "why does
Banker's not solve the general problem?" — the model has no notion of how long anyone will hold
anything, so it must assume the worst case.

---

## 3. The resource-allocation graph (S08–S13)

### 3.1 Vocabulary (S08–S09)

> *"Graph: a set of vertices `V` and a set of edges `E`."*

| Part | Definition | Contents |
|---|---|---|
| `V` | vertices, partitioned into two types | `P = {P1, …, Pn}` processes; `R = {R1, …, Rm}` resource **types** |
| `E` | edges, partitioned into two types | **request** edges and **assignment** edges |

| Edge | Written | Meaning | Added when | Removed when |
|---|---|---|---|---|
| **Request edge** | `Pi → Rj` | `Pi` is waiting for an instance of `Rj` | the request is made | **the request is granted** |
| **Assignment edge** | `Rj → Pi` | an instance of `Rj` is allocated to `Pi` | the request is granted | **the resource is released** |

The two "removed when" clauses are the same event seen twice: granting a request **converts** the
request edge into an assignment edge. Nothing else in the graph changes.

**Drawing conventions** (S09's legend):

| Symbol | Meaning |
|---|---|
| circle | a **process** `Pi` |
| rectangle | a **resource type** `Rj` |
| a dot inside the rectangle | **one instance** of that type — four dots = `Wj = 4` |
| arrow from a circle to a rectangle | `Pi` **requests** an instance of `Rj` |
| arrow from a **dot** to a circle | **that instance** is assigned to `Pi` |

The dot is not decoration: because an assignment edge starts at a *specific dot*, you can see at a
glance how many instances are free (dots with no outgoing arrow) — which is exactly what you need to
apply §3.3.

### 3.2 The three worked graphs (S10, S11, S12)

The extracted text keeps each slide's **conclusion** but not its arrows. The edge lists below are the
ones that make each conclusion true, and each is the standard textbook drawing the deck reproduces.
If your copy of the slide lays the arrows out differently, the *reasoning* is unchanged.

#### Graph 1 — no deadlock (S10)

Resources `R1` (1 instance), `R2` (2), `R3` (1), `R4` (3).

| Edge | Meaning |
|---|---|
| `P1 → R1` | P1 requests `R1` |
| `R2 → P1` | P1 holds one `R2` instance |
| `R1 → P2` | `R1` (its only instance) is held by **P2** |
| `R2 → P2` | P2 holds the **other** `R2` instance |
| `P2 → R3` | P2 requests `R3` |
| `R3 → P3` | `R3` is held by **P3** |
| — | `R4`'s three instances are held by nobody and requested by nobody |

In words: **P1 holds R2, wants R1. P2 holds R1 and R2, wants R3. P3 holds R3 and wants nothing.**

The slide prints the answer: **`P3 → P2 → P1`**.

**Why that order works, and why it is the only possible start.** At the snapshot every instance of
`R1`, `R2` and `R3` is allocated, and nobody wants `R4`; the only process that can make progress is
therefore the one that **asks for nothing**, P3.

| Step | Who can finish | Why | Resources released |
|---|---|---|---|
| 1 | **P3** | requests nothing | `R3` |
| 2 | **P2** | its pending request `R3 ≤ ` the instances now free | `R1`, one `R2` |
| 3 | **P1** | its pending request `R1 ≤ ` free | one `R2` |

Check the graph for cycles: every path runs `P1 → R1 → P2 → R3 → P3` and **stops**, because P3 has no
outgoing edge. **No cycle → no deadlock** — consistent with §3.3, and the reason the deck's first
question on this slide is *"can you identify a sequence of process executions so that all requests are
met?"*

#### Graph 2 — with a deadlock (S11)

Same four resource types: `R1` (1), `R2` (2), `R3` (1), `R4` (3).

| Edge | Meaning |
|---|---|
| `P1 → R1` | P1 requests `R1` |
| `R1 → P2` | `R1` is held by **P2** |
| `P2 → R3` | P2 requests `R3` |
| `R3 → P3` | `R3` is held by **P3** |
| `P3 → R2` | P3 requests `R2` |
| `R2 → P1`, `R2 → P2` | **both** instances of `R2` are held — one by P1, one by P2 |

In words: **P1 waits for P2. P2 waits for P3. P3 waits for P1 *and* P2.**

The notes count the cycles for you:

* **Cycle 1:** `P2 → R3 → P3 → R2 → P2` — P2 waits for P3, P3 waits for P2.
* **Cycle 2:** `P1 → R1 → P2 → R3 → P3 → R2 → P1` — the same ring with P1 attached.

There are **two** cycles, and *"no process can make any progress"*: P3 is the only process that could
break the ring, and P3 is itself waiting on both of the other two. This is a real deadlock.

Note what makes cycle 2 legal even though `R2` has **two** instances: P3's request is for `R2`, and
**both** instances are held, so P3 really is blocked. The multi-instance rule (§3.3) says a cycle is
*not enough* in general — here it happens to be conclusive because no instance of anything requested
is free.

#### Graph 3 — a cycle but **no** deadlock (S12)

> *"One cycle. But no deadlock. Because P2 can finish and release R1. Then P4 can finish. Then P3 and
> P1 can finish."*

Resources `R1` (1 instance), `R2` (2 instances).

| Edge | Meaning |
|---|---|
| `P1 → R1` | P1 requests `R1` |
| `R1 → P2` | `R1` is held by **P2** |
| `P2 → R2` | P2 has a **pending** request for one `R2` instance |
| `R2 → P1` | P1 holds **one** of the two `R2` instances |
| `P3 → R2`, `P4 → R2` | P3 and P4 also request `R2`; they hold nothing |

The cycle is `P1 → R1 → P2 → R2 → P1`: P1 waits for P2 (through `R1`) and P2 waits for P1 (through
`R2`). Yet the slide's answer is **no deadlock**, execution order **`P2 → P4 → P3 → P1`**.

The resolution is the **second instance of `R2`**, which is free:

| Step | Who | Why it can proceed | Instances freed |
|---|---|---|---|
| 1 | **P2** | its `R2` request can be met from the **free second instance**; P1's hold on the other one is irrelevant | `R1` |
| 2 | **P4** | `R2` instance now free | its `R2` instance |
| 3 | **P3** | `R2` instance now free | its `R2` instance |
| 4 | **P1** | `R1` was released at step 1 | — |

This is the single most important worked example in the chapter, so state the reason precisely:

> **The cycle exists in the drawing because `P2`'s request has not been granted *yet*; it does not
> exist in the "no process can finish" sense.** With one instance per type, a cycle means every
> waiter's target is uniquely owned and blocked, so the cycle is unbreakable. With several
> instances, a cycle can be **broken by an instance that is not in the cycle at all**.

That is what a *pending* request edge means for a multi-instance type, and it is why S13 immediately
splits the rule in two.

### 3.3 Basic facts (S13)

The slide is three lines; the notes supply the reason. (The extraction drops the `⇒` glyphs — the
slide reads:

```
If graph contains no cycles      no deadlock
If graph contains a cycle
    If only one instance per resource type, then deadlock
    If several instances per resource type, possibility of deadlock
```
)

| Graph | Instances per type | Conclusion | Why |
|---|---|---|---|
| **no cycle** | any | **no deadlock** | *"we do not have the problem of A waiting for B and B waiting for A"* — formally, a deadlock would be a closed waiting chain, i.e. a cycle |
| **cycle** | **one** per type | **deadlock** | every edge in the cycle is a unique ownership; no member can obtain its target, so *"no process can make any progress"* |
| **cycle** | **several** per type | **possibility of deadlock** | the cycle may be broken by an instance held outside it (Graph 3) — or may not be (Graph 2) |

The notes end the slide with the forward pointer that motivates the rest of the chapter:

> *"We will introduce Banker's algorithm to solve the problem with multiple instances later on."*

So the graph answers the **single-instance** case, and the matrices answer the **multi-instance** case.
Two more things worth saying in an answer:

* **The test is structural, not quantitative.** For single-instance resources you do not need to
  simulate; you look for a cycle.
* **No cycle is always conclusive.** You never need the instance count to answer "is there a
  deadlock?" when the graph is acyclic.

---

## 4. The four conditions (S15–S16)

> *"Deadlock may arise if the following four conditions hold simultaneously (necessary, but not
> sufficient)."*

| # | Condition | Slide definition | What it is a property of |
|---|---|---|---|
| 1 | **Mutual exclusion** | *"Only one process at a time can use a resource instance"* | the **resource** |
| 2 | **Hold and wait** | *"A process holding at least one resource is waiting to acquire additional resources held by other processes"* | the **process's request pattern** |
| 3 | **No preemption** | *"A resource can be released only voluntarily by the process holding it, after that process has completed its task"* | the **OS policy** |
| 4 | **Circular wait** | *"There exists a set `{P0, P1, …, Pn}` of waiting processes such that `P0` is waiting for a resource held by `P1`, `P1` is waiting for `P2`, …, `Pn` is waiting for `P0`"* | the **edge set / graph** |

### 4.1 Why "necessary, not sufficient" is the phrase to remember

* **Necessary**: all four must hold for a deadlock to exist. *"If any of them is violated, there is no
  deadlock"* (S15 notes). That is why prevention works: remove any one and you are done.
* **Not sufficient**: all four can hold and nothing is stuck — Graph 1 (S10) has mutual exclusion
  (tape drives), hold-and-wait (nobody requests before holding), no preemption, and… no deadlock,
  because the *specific* set of holders does not form a cycle. Circular wait in the formal sense is
  exactly the missing piece, and even a cycle may not be enough when instances are several (§3.3).

A useful way to hold the four together:

```
   mutual exclusion  +  hold-and-wait  +  no preemption   ->  a cycle CAN form
                                    circular wait        ->  a cycle HAS formed
```

### 4.2 Mapping the conditions onto the graph

* **Circular wait is literally a cycle** — *"Circular wait corresponds to a cycle in the resource
  allocation graph"* (S16 notes). This is why S13 and S16 are the same idea in two languages.
* **Hold-and-wait is what makes a cycle *closed*** — an edge out of `Pi` (a request) plus an edge into
  `Pi` (a hold). Without hold-and-wait there are no pairs of edges, hence no cycles.
* **Mutual exclusion** decides whether a resource vertex can have more than one assignment edge at a
  time. Several instances of a shareable resource would not need an assignment edge at all.
* **No preemption** is what prevents the OS from deleting an assignment edge by force. If it could,
  the cycle would be broken administratively — which is precisely the "no preemption" prevention
  technique on S21.

### 4.3 The four conditions and the four prevention techniques

The next section attacks them one at a time. The pairing to memorise:

| Condition | Prevention technique | Where |
|---|---|---|
| Mutual exclusion | *cannot be removed* for non-shareable resources (chopsticks) | S20 |
| Hold and wait | request **all** resources at once (all-or-nothing) | S20 |
| No preemption | **preempt**: if a further request cannot be met immediately, release everything held and restart | S21 |
| Circular wait | impose an **order** on resource types (chopstick IDs), or cap the number of concurrent holders | S21–S22 |

---

## 5. How to handle deadlocks at all (S18)

S18 is a three-line slide, and it is the map for the rest of the chapter:

1. **Ensure that the system will never enter a deadlock state** — that is **prevention** (S19–S22) and
   **avoidance** (S24–S37).
2. **Allow the system to enter a deadlock state and then recover** — that is **detection** +
   recovery (S39–S44).
3. **Ignore the problem and pretend that deadlocks never occur** — *"Used by most operating systems,
   including UNIX."*

The notes answer the obvious question — why would a textbook spend a chapter on something real
systems ignore?

> *"Why do most systems use Ostrich approach? Efficiency. The overhead of deadlock detection and
> prevention is high. Why do we learn about deadlock detection and prevention then…"*

The honest completion of that sentence, and the way to write it in an exam:

* deadlock is **rare**; prevention and detection costs are paid **always**;
* prevention restricts **every** request, even the 99.99 % that would never deadlock;
* avoidance requires every process to **declare its maximum claim in advance**, which is usually
  impossible to know;
* a hang is often survivable (the user reboots), so the expected cost of the rare deadlock is smaller
  than the certain cost of prevention.

---

## 6. Deadlock prevention (S19–S22)

> *"Prevent at least one of the four deadlock conditions. We will illustrate using
> Dining-Philosophers Problem."*

Prevention is a **design-time** decision: change how resources are requested, so that at least one of
the four conditions can never hold. It does not look at the current state and it does not know
anything about the future.

### 6.1 The baseline: dining philosophers with binary semaphores (S19)

> *"Recall dining-philosopher solution using semaphores. Each chopstick is a shared resource protected
> by a binary semaphore (`chopstick[5]`). Initially, for all `i`, `chopstick[i] = 1`."*

```
   Process Philosopher i
       while (1) {
           wait(chopstick[i]);                // pick up LEFT
           wait(chopstick[(i+1) % 5]);        // pick up RIGHT
           eat
           signal(chopstick[i]);
           signal(chopstick[(i+1) % 5]);
           think
       }
```

Five philosophers around a table, five chopsticks, philosopher `i` between chopstick `i` and
chopstick `(i+1) % 5`. Each chopstick is a **separate resource type with exactly one instance** — so
any cycle in the graph is conclusive (§3.3).

**Why it deadlocks.** The notes give the trigger:

> *"Does this solution have any problem? Each philosopher executes the first line and a context switch
> occurs → deadlock."*

Precisely (and the slide's shorthand compresses this): if **all five** philosophers complete their
first `wait` before any of them attempts the second, then

| Philosopher | holds | waits for | held by |
|---|---|---|---|
| P0 | chopstick 0 | chopstick 1 | P1 |
| P1 | chopstick 1 | chopstick 2 | P2 |
| P2 | chopstick 2 | chopstick 3 | P3 |
| P3 | chopstick 3 | chopstick 4 | P4 |
| P4 | chopstick 4 | chopstick 0 | P0 |

That is a **circular wait** of length 5 built out of **hold-and-wait**, on resources that are
**mutually exclusive** and **not preemptible**. All four conditions hold at once.

Degrees of freedom worth noting:

* With **one** philosopher there is no problem (it needs both chopsticks and nobody else competes).
* With **two** philosophers and two chopsticks the deadlock is already possible — each takes one.
* The deadlock needs a specific interleaving; that is why the naive solution usually *appears* to work.

### 6.2 Mutual exclusion (S20) — the condition that cannot be broken

> *"Chopsticks are not shareable (simultaneously), hence this condition cannot be eliminated."*

To remove mutual exclusion you would have to let two philosophers use the same chopstick at the same
time — which is not a chopstick any more. The same applies to a printer, a tape drive, or a
half-written file: **the exclusion is a property of the resource, not of the protocol.**

Two things to say in an answer:

* If the resource *is* shareable (a read-only file, a read-only device), there is no mutual exclusion
  and hence no deadlock on it — that is the one legitimate way to "remove" this condition.
* For non-shareable resources, this is the dead end of the checklist, so **you must attack one of the
  other three.** S20–S22 do exactly that.

### 6.3 Hold and wait (S20) — all-or-nothing

> *"Must guarantee that whenever a process requests a resource, it does not hold any other resource.
> Allow a philosopher to pick up chopsticks only if both the required chopsticks are available."*

The notes spell out the mechanism: *"at the beginning, the philosopher hasn't taken any chopstick. In
that case, there is no hold and wait. So, no deadlock."*

```
   wait(both available)   ->  take both atomically  ->  eat  ->  release both
   otherwise              ->  take nothing, wait
```

Graphically: **no process ever has an outgoing request edge and an incoming assignment edge at the
same time**, so no cycle can be closed (§4.2).

The price, which the deck leaves implicit but a good answer should state:

* **Utilisation drops** — a philosopher holding one chopstick is not "using" it productively, but
  under all-or-nothing it may not even start.
* **Starvation** — a philosopher may lose the race for both chopsticks indefinitely.
* **You must know the whole set in advance** — the same assumption Banker's needs (`Max`), and the same
  reason it is impractical.

### 6.4 No preemption (S21) — take it back

> *"If a philosopher cannot get the second chopstick, then preempt and release the chopstick that is
> being held."*

The general rule, from the notes:

> *"If a process that is holding some resources requests another resource that cannot be immediately
> allocated to it, then all resources currently being held are released. The process restarts
> later."*

Two consequences:

* **State must be saveable and discardable.** Releasing a chopstick is free; releasing a half-written
  file or a half-printed page is not. Preemption works for resources whose *use* can be rolled back.
* **It is expensive**: the process loses its progress and restarts. That is exactly the bridge
  analogy's "back up" (S05).

**Do not confuse this with a timeout.** S21's notes say *"if a philosopher cannot get another chopstick
for a long time, preempt"*; that is a **recovery** trigger (the deadlock happened, then a victim is
chosen), not prevention. For **prevention** the preemption must be unconditional and immediate:
whenever the second request cannot be met, the held resources are released **before** waiting.

### 6.5 Circular wait (S21–S22) — order the resources

Three variants appear on S21–S22.

**(a) Cap the number of concurrent holders.** *"Allow at most four philosophers to be hungry
simultaneously"* — *"This is because of pigeon hole theory"* (S21 notes).

With five chopsticks and at most four hungry philosophers, some philosopher must be able to get
**both** chopsticks: four philosophers can occupy at most four chopsticks, and the fifth is either
free or held by a philosopher who has already finished. Formally: with `k` resources and at most
`k − 1` competitors, a full cycle of `k` waiters cannot form — a cycle of length `k` needs `k`
holders, i.e. `k` hungry philosophers.

**(b) Odd-even solution.** S21 prints *"(see previous lecture)"*. The deck does not develop it; if it
appears in an exam question, it comes from the synchronization chapter. Note only the *shape* of the
idea: odd-numbered philosophers take the left chopstick first, even-numbered take the right, so the
two "directions" of acquisition cancel instead of meeting.

**(c) Chopstick ordering (S22).** The general technique, and the one to use in an answer.

> *"In the dining philosopher problem, each chopstick has an ID. Suppose each philosopher takes the
> chopstick with the small id first, and then takes the chopstick with the large id. First request in
> black. Second request in yellow. → No circular wait. → No deadlock."*

The drawing on S22 is a ring of the five chopsticks numbered `0–4` with philosophers `A–E` sitting
between neighbours; each philosopher makes one **black** (first) and one **yellow** (second) request.

Every philosopher sits between two adjacent chopsticks; each performs **one first request (black)** and
**one second request (yellow)**. Under the rule "lower ID first", the black arrows all point *down*
the numbering and the yellow arrows all point *up* it.

**The proof is one line.** A circular wait would be an ordering
`i0 < i1 < … < in < i0` of chopstick IDs (each philosopher's *first* request is the lower ID, so
travelling around the cycle the IDs must strictly increase). A strict order cannot close on itself, so
no cycle of waiters exists:

```
   if every process requests resources in increasing ID order,
   then any wait-for cycle would require  i0 < i1 < ... < i0   ->  contradiction
```

This is the technique real kernels use (lock ordering), and it is why the deque/deadlock bugs in
production code are almost always "acquired lock A then B" in one path and "B then A" in another.

### 6.6 Prevention, one table

| Condition | Dining-philosophers fix | General technique | Cost |
|---|---|---|---|
| **Mutual exclusion** | *cannot be removed* — chopsticks are not shareable | share only resources that are genuinely shareable | none for non-shareable resources; this condition is simply unavoidable |
| **Hold and wait** | take **both** chopsticks or neither | request the **whole set** up front; all-or-nothing | low utilisation, starvation, must know the set in advance |
| **No preemption** | drop the held chopstick if the second is unavailable | preempt: release everything, restart later | rollback cost; only for saveable state |
| **Circular wait** | ≤ 4 hungry; odd-even; **order by ID** | total order over resource **types**, request in increasing order | needs global agreement; forces a request order that may not suit the program |

**Prevention's defining weakness**, and the bridge to the next section: it is **static**. It forbids
requests that would never have caused a deadlock, and it forbids them all the time. Avoidance asks the
same question — *"could this request lead to a deadlock?"* — but answers it **per request**, using the
current state.

---

## 7. Deadlock avoidance (S24–S27)

### 7.1 The idea (S24)

> *"The deadlock-avoidance algorithm dynamically examines the resource-allocation state to ensure that
> the system never goes into an unsafe state. When a process requests an available resource, system
> must decide if immediate allocation leaves the system in a safe state. If safe, the request is
> granted, and otherwise, the process must wait."*

Three properties that separate it from prevention:

* it needs the **current state** (`Available`, `Allocation`), not just a rule;
* it needs the **future** — how much each process may still ask for (`Max`), so it must be **declared
  in advance**;
* it can **refuse a request that is physically satisfiable**, purely because of what might happen next.

### 7.2 Safe state and safe sequence (S24–S25)

> *"System is in a safe state if there exists a safe completion sequence of all processes without
> deadlock."*

> *"A process completion sequence `<P1, P2, …, Pn>` is safe, if for each `Pi`, the resources that `Pi`
> requests can be satisfied by currently available resources + resources held by all the `Pj, j < i`.
> If `Pi`'s needs cannot be immediately met, then `Pi` can wait until all `Pj, j < i` have finished.
> When `Pj (j<i)` are finished, `Pi` can obtain needed resources, execute, return allocated resources,
> and terminate."*

The condition is **cumulative**, and this is the arithmetic that catches people out:

```
        Need(Pi)  <=  Available  +  SUM over all Pj that appear BEFORE Pi in the sequence of Allocation(Pj)
```

Note what is *not* in the sum: `Allocation(Pi)` itself (a process cannot lend itself what it already
holds to satisfy its own request — but it does not need to, since `Need` is what it still lacks), and
any process later in the sequence.

### 7.3 The `Available: 1` example (S26)

| Process | Hold | Request (remaining need) |
|---|---|---|
| P1 | 1 | 1 |
| P2 | 1 | 2 |
| P3 | 1 | 3 |

`Available = 1`. Total instances in the system = `1 + 1 + 1 + 1 = 4`.

**Q1 — is `<P1, P2, P3>` safe?**

| Step | Process | Need | Available before | Has `Need ≤ Available`? | Available after (finish → release its hold) |
|---|---|---|---|---|---|
| 1 | P1 | 1 | 1 | **1 ≤ 1 ✓** | 1 + 1 = **2** |
| 2 | P2 | 2 | 2 | **2 ≤ 2 ✓** | 2 + 1 = **3** |
| 3 | P3 | 3 | 3 | **3 ≤ 3 ✓** | 3 + 1 = **4** |

**Yes.** The slide's three checks are exactly the cumulative condition:

```
   P1.request <= Available                       1 <= 1        ✓
   P2.request <= P1.Hold + Available            2 <= 1 + 1    ✓
   P3.request <= P1.Hold + P2.Hold + Available  3 <= 1 + 1 + 1 ✓
```

**Q2 — is `<P3, P2, P1>` safe?** **No**: `P3.request = 3 > Available = 1`. The sequence cannot even
start.

**Q3 — is the system safe?** **Yes**, because **one** safe sequence exists (`<P1, P2, P3>`). Safety is
an existential claim: you only need to find one order.

Note the shape of the argument: it is a **simulation** in which every process is assumed to run to
completion once it can, and to release everything at the end. That "release everything at the end"
assumption is the whole basis of the next slide.

### 7.4 Safe, unsafe and deadlock (S27)

```
        +---------------------------------------------------+
        |                       all states                  |
        |     +---------------------------------------+     |
        |     |              unsafe states            |     |
        |     |     +---------------------------+     |     |
        |     |     |       safe states         |     |     |
        |     |     |                           |     |     |
        |     |     |    +-----------------+    |     |     |
        |     |     |    |   DEADLOCKED    |    |     |     |
        |     |     |    |     states      |    |     |     |
        |     |     |    +-----------------+    |     |     |
        |     |     +---------------------------+     |     |
        |     +---------------------------------------+     |
        +---------------------------------------------------+

   safe     ->  no deadlock, guaranteed
   unsafe   ->  deadlock POSSIBLE, not certain
   deadlock ->  a subset of unsafe
```

> *"If a system is in a safe state → no deadlocks. If a system is in an unsafe state → possibility of
> deadlock."*

**Why unsafe does not imply deadlock** — the notes make the argument in one sentence:

> *"It only means possibility of a deadlock. Because we are considering the worst case in the safe
> sequence: the resources are released only when the process finishes (the worst case). If the process
> can release resources before termination, the later processes in the sequence can actually release
> the resources earlier. So the previous process has more resources to consume. The safe sequence does
> not consider this case."*

Restated: the safe-sequence test assumes every process **holds everything it has until it
terminates**. Real processes release early (a process often needs a resource only for one phase). An
"unsafe" state therefore only means *"if everyone behaves as badly as possible, somebody might get
stuck"*. It is a **conservative** verdict, and that conservatism is the price of a guarantee.

**Deadlock avoidance** is therefore: *"ensure that a system will never enter an unsafe state"*. It
never lets the state leave the inner-left circle, so it never has to deal with `unsafe` at all.

---

## 8. Banker's algorithm (S28–S37)

### 8.1 Purpose and assumptions (S28)

> *"An algorithm to check whether satisfaction of a resource request would lead to an unsafe state.
> For multiple instances of each resource type. When a process requests a resource it may have to wait
> (if the allocation leads to unsafe state)."*

| Assumption | Why it is needed | What breaks without it |
|---|---|---|
| **Every process declares the maximum instances of each resource type it may need** | `Need = Max − Allocation` requires `Max` | you cannot compute `Need`, so you cannot test safety |
| **When a process gets all its resources it returns them in a finite amount of time** | the safety simulation needs the release to actually happen | a process could hold forever and the "safe sequence" is a fiction |

The notes add the name's origin and the single-instance alternative:

> *"By its name: there are many bankers. They can borrow and lend money to each other. The banker's
> algorithm is to make sure that the bankers will not have a deadlock problem. … If all resource types
> have a single instance, what algorithm can we use? We can use resource-allocation graph, and see if
> the resource-allocation graph has a cycle."*

So the division of labour is: **graph for single instances, Banker's for multiple instances.**

### 8.2 The data structures (S29)

| Structure | Shape | Definition on the slide |
|---|---|---|
| `Available` | vector, length `m` | *"If `Available[j] == k`, there are `k` instances of resource type `Rj` available"* |
| `Max` | `n × m` matrix | *"If `Max[i,j] == k`, then process `Pi` may request at most `k` instances of resource type `Rj`"* |
| `Allocation` | `n × m` matrix | *"If `Allocation[i,j] == k`, then `Pi` is currently allocated `k` instances of `Rj`"* |
| `Need` | `n × m` matrix | *"If `Need[i,j] == k`, then `Pi` may need `k` more instances of `Rj` to complete its task"* |

```
        Need  =  Max  -  Allocation          (componentwise, all i, j)
        n = number of processes,  m = number of resource types
```

Two invariants worth writing down:

```
        for every resource type j:   Available[j] + SUM_i Allocation[i][j]  =  total instances of Rj
        for every process i:         Allocation[i] + Need[i]  =  Max[i]
```

The first is how you find a typo in an exam matrix in ten seconds. The second is why `Max` must not
change when a request is granted (S36).

### 8.3 Part 1 — the safety algorithm (S30)

> *"Let `Work` and `Finish` be vectors of length `m` and `n`, respectively; initially `Work =
> Available`, `Finish[i] = false` for `i = 1, 2, …, n`."*

```
 1.  Work = Available
     Finish[i] = false                       for all i

 2.  Find an i such that
        (a) Finish[i] == false
        (b) Need[i, *] <= Work               (componentwise)
     If no such i exists, go to step 4.

 3.  Work = Work + Allocation[i, *]
     Finish[i] = true
     go to step 2

 4.  If Finish[i] == true for all i  ->  the system is in a SAFE state
     otherwise                      ->  the system is in an UNSAFE state
```

Two annotations printed on the slide:

* **`Work = Available + resources held by all Pj (Finish[j] = true)`** — this is the invariant that
  makes step 3 meaningful. `Work` is *not* "the free resources": it is **the free resources plus
  everything the already-finished processes have handed back**, i.e. the total that the remaining
  processes could collectively draw on.
* **"What if multiple answers?"** — the notes answer it: *"Any one can be chosen."* Step 2 may find
  several eligible processes; picking any of them is correct, and different choices yield different
  valid safe sequences.

The output is a **safe sequence**: the order in which you marked the processes finished. Its existence
is the answer; the particular order is not.

Cost: at most `n` passes over `n` processes, each comparing `m` components → **`O(n²m)`** per test.
That is the "overhead is high" of S18 in concrete terms, and it is paid on **every** request.

### 8.4 The `T0` snapshot, and `Need` (S31–S32)

> *"5 processes: P0 through P4. 3 resource types: A (10 instances), B (5 instances) and C (7
> instances)."*

**`Allocation`** at `T0`

| Process | A | B | C |
|---|---|---|---|
| P0 | 0 | 1 | 0 |
| P1 | 2 | 0 | 0 |
| P2 | 3 | 0 | 2 |
| P3 | 2 | 1 | 1 |
| P4 | 0 | 0 | 2 |

**`Max`** (each process's declared maximum)

| Process | A | B | C |
|---|---|---|---|
| P0 | 7 | 5 | 3 |
| P1 | 3 | 2 | 2 |
| P2 | 9 | 0 | 2 |
| P3 | 2 | 2 | 2 |
| P4 | 4 | 3 | 3 |

**`Available` = (3, 3, 2)** — check: `Σ Allocation = (7, 2, 5)`, and `(7,2,5) + (3,3,2) = (10,5,7)`
= the declared totals of A, B and C. ✓

**`Need = Max − Allocation`** (S32), row by row:

| Process | `Max` | `Allocation` | `Need` | Working |
|---|---|---|---|---|
| P0 | (7,5,3) | (0,1,0) | **(7,4,3)** | 7−0, 5−1, 3−0 |
| P1 | (3,2,2) | (2,0,0) | **(1,2,2)** | 3−2, 2−0, 2−0 |
| P2 | (9,0,2) | (3,0,2) | **(6,0,0)** | 9−3, 0−0, 2−2 |
| P3 | (2,2,2) | (2,1,1) | **(0,1,1)** | 2−2, 2−1, 2−1 |
| P4 | (4,3,3) | (0,0,2) | **(4,3,1)** | 4−0, 3−0, 3−2 |

### 8.5 Running the safety algorithm (S33)

`Work = Available = (3,3,2)`, `Finish = (F,F,F,F,F)`.

| Step | Pick | `Need[i]` | `Need ≤ Work`? | `Work` before | `Work` after (`+ Allocation[i]`) | `Finish` |
|---|---|---|---|---|---|---|
| 1 | **P1** | (1,2,2) | 1≤3, 2≤3, 2≤2 ✓ | (3,3,2) | (3+2, 3+0, 2+0) = **(5,3,2)** | P1 ✓ |
| 2 | **P3** | (0,1,1) | 0≤5, 1≤3, 1≤2 ✓ | (5,3,2) | (5+2, 3+1, 2+1) = **(7,4,3)** | P3 ✓ |
| 3 | **P4** | (4,3,1) | 4≤7, 3≤4, 1≤3 ✓ | (7,4,3) | (7+0, 4+0, 3+2) = **(7,4,5)** | P4 ✓ |
| 4 | **P0** | (7,4,3) | 7≤7, 4≤4, 3≤5 ✓ | (7,4,5) | (7+0, 4+1, 5+0) = **(7,5,5)** | P0 ✓ |
| 5 | **P2** | (6,0,0) | 6≤7, 0≤5, 0≤5 ✓ | (7,5,5) | (7+3, 5+0, 5+2) = **(10,5,7)** | P2 ✓ |

Every process finished, and the final `Work` is `(10,5,7)` — all the instances in the system, which is
the arithmetic check that the trace is right.

> **The system is safe; the sequence `<P1, P3, P4, P2, P0>` is a safe sequence.**

**Which processes can be picked first?** Only a `Need ≤ (3,3,2)` qualifies:

| Process | `Need` | Eligible first? |
|---|---|---|
| P0 | (7,4,3) | ✗ — `A: 7 > 3` |
| P1 | (1,2,2) | **✓** |
| P2 | (6,0,0) | ✗ — `A: 6 > 3` |
| P3 | (0,1,1) | **✓** |
| P4 | (4,3,1) | ✗ — `A: 4 > 3` |

So a safe sequence must start with **P1 or P3**. Starting with P3 gives another valid answer:
`<P3, P1, P4, P0, P2>` (after P3, `Work = (5,4,3)`; then P1 → `(7,4,3)`; the rest as above). Both are
full marks — the deck's note says *"As long as you can find a completion sequence for the process, we
can say the system is safe."*

### 8.6 Part 2 — the resource-request algorithm (S34–S35)

> *"`Requesti` = Request vector for process `Pi`. If `Requesti[j] == k` then process `Pi` wants `k`
> instances of resource type `Rj`."*

```
 1.  if Request_i <= Need_i          ->  go to step 2
     else                                 ERROR: the process has exceeded its maximum claim

 2.  if Request_i <= Available       ->  go to step 3
     else                                 Pi must WAIT (resources are not available)

 3.  pretend to allocate, by modifying the state:
         Available     = Available     - Request_i
         Allocation_i  = Allocation_i  + Request_i
         Need_i        = Need_i        - Request_i            (Max_i is unchanged)

 4.  run the SAFETY algorithm on the pretend state
         safe    ->  the resources are allocated to Pi
         unsafe  ->  Pi must wait, and the OLD state is restored
```

Vector comparison is defined on the slide: `V1 <= V2` iff `V1[j] <= V2[j]` for **all** `j` — *"the
`i`th row of the matrix"* when one side is a matrix row.

The three checks mean three different things, and mixing them up costs marks:

| Check | Fails because | Response |
|---|---|---|
| `Request_i ≤ Need_i` | the process asked for more than it **promised** | **error** — a bug in the process, not a resource shortage |
| `Request_i ≤ Available` | the instances are not free **right now** | **wait** — an ordinary short-term shortage |
| safety test | granting would leave **no safe sequence** | **wait** — a *future* problem; the state must be restored |

### 8.7 Worked request: `P1` asks for `(1,0,2)` → granted (S36)

State = the `T0` snapshot of §8.4 (`Available = (3,3,2)`).

**Step 1.** `Request1 = (1,0,2) ≤ Need1 = (1,2,2)`? `1≤1, 0≤2, 2≤2` → **true**.

**Step 2.** `Request1 = (1,0,2) ≤ Available = (3,3,2)`? `1≤3, 0≤3, 2≤2` → **true**.

**Step 3.** Pretend to allocate:

| | `Available` | `Allocation1` | `Need1` |
|---|---|---|---|
| before | (3,3,2) | (2,0,0) | (1,2,2) |
| change | − (1,0,2) | + (1,0,2) | − (1,0,2) |
| **after** | **(2,3,0)** | **(3,0,2)** | **(0,2,0)** |

The new state:

| Process | Allocation | Max | Need |
|---|---|---|---|
| P0 | (0,1,0) | (7,5,3) | (7,4,3) |
| **P1** | **(3,0,2)** | (3,2,2) | **(0,2,0)** |
| P2 | (3,0,2) | (9,0,2) | (6,0,0) |
| P3 | (2,1,1) | (2,2,2) | (0,1,1) |
| P4 | (0,0,2) | (4,3,3) | (4,3,1) |

`Available = (2,3,0)`.

**Step 4.** Safety algorithm on the pretend state:

| Step | Pick | `Need[i]` | `Need ≤ Work`? | `Work` before | `Work` after |
|---|---|---|---|---|---|
| 1 | **P1** | (0,2,0) | 0≤2, 2≤3, 0≤0 ✓ | (2,3,0) | (2+3, 3+0, 0+2) = **(5,3,2)** |
| 2 | **P3** | (0,1,1) | 0≤5, 1≤3, 1≤2 ✓ | (5,3,2) | **(7,4,3)** |
| 3 | **P4** | (4,3,1) | ✓ | (7,4,3) | **(7,4,5)** |
| 4 | **P0** | (7,4,3) | 7≤7, 4≤4, 3≤5 ✓ | (7,4,5) | **(7,5,5)** |
| 5 | **P2** | (6,0,0) | ✓ | (7,5,5) | **(10,5,7)** |

Safe → **grant**. The slide's conclusion: *"Executing safety algorithm shows that sequence
`<P1, P3, P4, P0, P2>` is safe."*

Two details the notes stress and markers look for:

* *"What are the parameters that we need to change? Do we need to change `Max`? No."* — `Max` is the
  promise, not the balance.
* **P1 is first in the new sequence** even though the request came from P1: after the grant, P1's
  `Need` is `(0,2,0)`, which `Work` can satisfy immediately. Getting a resource can bring you
  *closer* to finishing.

### 8.8 The same request again → refused at step 1 (S37)

> *"Can a further request for `(1,0,2)` by `P1` be granted? Step 1: check if `Request1 ≤ Need1`:
> `(1,0,2) ≤ (0,2,0)` → false."*

`Need1` is now `(0,2,0)` because the first `(1,0,2)` was granted. The check fails on **A**: `1 > 0`.

This is **not** a "wait" — it is an **error**: P1 has asked for a total of `(2,0,2)` of A and C
against a declared `Max` of `(3,2,2)`; the request itself is legal, but `Need` has already been
reduced to zero on A, so a further request for A exceeds the maximum claim. In Banker's terms, a
process may not revise its promise upward.

### 8.9 `P0` asks for `(0,2,0)` → unsafe, state restored (S37)

State = after the §8.7 grant (`Available = (2,3,0)`).

**Step 1.** `(0,2,0) ≤ Need0 = (7,4,3)`? `0≤7, 2≤4, 0≤3` → **true**.
**Step 2.** `(0,2,0) ≤ Available = (2,3,0)`? `0≤2, 2≤3, 0≤0` → **true**.

**Step 3.** Pretend:

| | `Available` | `Allocation0` | `Need0` |
|---|---|---|---|
| before | (2,3,0) | (0,1,0) | (7,4,3) |
| change | − (0,2,0) | + (0,2,0) | − (0,2,0) |
| **after** | **(2,1,0)** | **(0,3,0)** | **(7,2,3)** |

**Step 4.** `Work = (2,1,0)`. Check every unfinished process:

| Process | `Need` | `Need ≤ (2,1,0)`? |
|---|---|---|
| P0 | (7,2,3) | ✗ |
| P1 | (0,2,0) | ✗ — `B: 2 > 1` |
| P2 | (6,0,0) | ✗ |
| P3 | (0,1,1) | ✗ — `C: 1 > 0` |
| P4 | (4,3,1) | ✗ |

No `i` can be found at step 2 → the loop ends immediately → `Finish` is not all true → **unsafe**.

> *"We cannot find `Needi ≤ Available` [read: `Need_i ≤ Work`]. → Restore the state."*

The notes make the lesson explicit: *"What should we do? We should restore the old state."* The
`(0,2,0)` grant is undone, `Available` returns to `(2,3,0)`, and P0 waits. **Nothing is allocated.**

This is the case that shows why the algorithm is worth its cost: `(0,2,0)` is *physically available*,
yet granting it would leave the system one request away from a state that cannot be unwound.

### 8.10 The homework request: `P4` asks for `(2,3,0)` (S37)

> *"How about a request for `(2,3,0)` by `P4`? … This is for your homework."*

Worked, from the restored state (`Available = (2,3,0)`, `Allocation4 = (0,0,2)`, `Need4 = (4,3,1)`):

**Step 1.** `(2,3,0) ≤ (4,3,1)`? `2≤4, 3≤3, 0≤1` → **true**.
**Step 2.** `(2,3,0) ≤ (2,3,0)`? → **true** (exactly equal — every free instance).
**Step 3.** Pretend: `Available = (0,0,0)`, `Allocation4 = (2,3,2)`, `Need4 = (2,0,1)`.
**Step 4.** `Work = (0,0,0)`:

| Process | `Need` | `Need ≤ (0,0,0)`? |
|---|---|---|
| P0 | (7,4,3) | ✗ |
| P1 | (0,2,0) | ✗ — `B: 2 > 0` |
| P2 | (6,0,0) | ✗ |
| P3 | (0,1,1) | ✗ |
| P4 | (2,0,1) | ✗ — `A: 2 > 0` |

No process is eligible → **unsafe → refuse, P4 waits, restore.**

Note that P4 is not eligible *even though it just received resources*: its own `Need` still starts with
`A: 2`, and `Work` is empty precisely because every free instance went to P4. This is the arithmetic
opposite of §8.7, where the granted process became immediately finishable.

### 8.11 What Banker's does and does not give you

| | |
|---|---|
| **Guarantees** | if every process honours its declared `Max` and eventually releases, the system never deadlocks |
| **Requires** | `Max` per process, known in advance — the fatal practical objection |
| **Cost** | `O(n²m)` safety test on **every** request; the test is a simulation of an imagined future |
| **Conservatism** | denies requests that are available and would, in fact, have been fine (unsafe ⇏ deadlock, §7.4) |
| **Starvation** | not prevented. A process whose request is repeatedly judged unsafe may wait forever while others retire |
| **Reality** | no mainstream OS uses it; UNIX and friends take the ostrich route (S18) |

---

## 9. Deadlock detection (S39–S44) — read for contrast, not for marks

S39 states the status of this whole block twice, on the slide and in the notes:

> *"This slide and the later slides in this chapter are not examinable."*
> *"The deadlock detection algorithm is actually similar to deadlock avoidance algorithm. If you are
> interested in them, you can refer to textbooks or just go through them in slides. They are not
> examinable."*

It is included here because it is the **cheapest possible check** on whether you really understand the
safety algorithm: same loop, one word changed.

### 9.1 The idea (S39)

| Step | Slide text |
|---|---|
| 1 | *"Allow system to enter deadlock state"* |
| 2 | *"Then invoke detection algorithms"* — for **single** instance per type, *"in textbook based on identifying cycle in resource-allocation graph"*; for **multiple** instances, *"next few slides"* |
| 3 | *"Then invoke recovery algorithm (in textbook)"* |

### 9.2 Data structures (S40)

| Structure | Shape | Definition |
|---|---|---|
| `Available` | vector, length `m` | number of available instances of each type |
| `Allocation` | `n × m` | instances of each type currently allocated to each process |
| `Request` | `n × m` | *"If `Request[i,j] = k`, then process `Pi` is requesting `k` more instances of resource type `Rj`"* |

**There is no `Max`.** Detection does not care what a process *might* ask for; it only cares what it is
asking for **now**. That is the whole difference in information requirements, and it is why detection
is usable in a real system while Banker's is not.

### 9.3 The algorithm (S41)

```
 1.  Work = Available
     for i = 1..n:  Finish[i] = false   if Allocation_i != 0
                    Finish[i] = true    otherwise        <-- note the seed

 2.  Find an i such that
        (a) Finish[i] == false
        (b) Request[i, *] <= Work
     If no such i exists, go to step 4.

 3.  Work = Work + Allocation[i, *]
     Finish[i] = true
     go to step 2

 4.  If Finish[i] == false for some i, then the system (process Pi) is DEADLOCKED
```

The only differences from the safety algorithm are the matrix (`Request` in place of
`Need`), the `Finish` seed, and the conclusion — see §10.2 for the three algorithms side by
side. The `Finish` seed matters: a process holding **nothing** cannot be part of a deadlock,
so marking it `true` stops it being reported as a victim. (S41's speaker notes are a
copy-paste of S30's; see [NOTES.md](NOTES.md) §3.)

### 9.4 Worked detection example (S42)

> *"Five processes: P0 through P4. Three resource types: A (7 instances), B (2 instances), and C
> (6 instances)."*

| Process | Allocation | Request |
|---|---|---|
| P0 | (0,1,0) | (0,0,0) |
| P1 | (2,0,0) | (2,0,2) |
| P2 | (3,0,3) | (0,0,0) |
| P3 | (2,1,1) | (1,0,0) |
| P4 | (0,0,2) | (0,0,2) |

`Available = (0,0,0)` — check: `Σ Allocation = (7,2,6)` = all of A, B and C. Nothing is free.

`Finish` seeds: every process has a non-zero `Allocation`, so `Finish = (F,F,F,F,F)`.

| Step | Pick | `Request[i]` | `Request ≤ Work`? | `Work` before | `Work` after | `Finish` |
|---|---|---|---|---|---|---|
| 1 | **P0** | (0,0,0) | ✓ (all zeros) | (0,0,0) | (0+0, 0+1, 0+0) = **(0,1,0)** | P0 ✓ |
| 2 | **P2** | (0,0,0) | ✓ | (0,1,0) | (0+3, 1+0, 0+3) = **(3,1,3)** | P2 ✓ |
| 3 | **P3** | (1,0,0) | 1≤3, 0≤1, 0≤3 ✓ | (3,1,3) | (3+2, 1+1, 3+1) = **(5,2,4)** | P3 ✓ |
| 4 | **P1** | (2,0,2) | 2≤5, 0≤2, 2≤4 ✓ | (5,2,4) | (5+2, 2+0, 4+0) = **(7,2,4)** | P1 ✓ |
| 5 | **P4** | (0,0,2) | 0≤7, 0≤2, 2≤4 ✓ | (7,2,4) | (7+0, 2+0, 4+2) = **(7,2,6)** | P4 ✓ |

All `Finish` true, final `Work = (7,2,6)` = the resource totals ✓.

> *"Sequence `<P0, P2, P3, P1, P4>` results in `Finish[i] = true` for all `i`"* — **no deadlock.**

Only P0 and P2 can start, because `Available = (0,0,0)` and they are the only processes whose `Request`
is all zeros. This is the mirror image of `Available: 1` on S26: with nothing free, the only way in is
through a process that asks for nothing.

### 9.5 The variant: `P2` requests an additional `C` (S43–S44)

> *"Suppose P2 requests an additional instance of type C."*

`Request2` becomes `(0,0,1)`; everything else is unchanged (`Available` is still `(0,0,0)` — the
request is merely *recorded*, which is exactly what the detection algorithm reads).

| Process | Allocation | Request |
|---|---|---|
| P0 | (0,1,0) | (0,0,0) |
| P1 | (2,0,0) | (2,0,2) |
| **P2** | (3,0,3) | **(0,0,1)** |
| P3 | (2,1,1) | (1,0,0) |
| P4 | (0,0,2) | (0,0,2) |

| Step | Pick | `Request[i]` | `Request ≤ Work`? | `Work` before | `Work` after | `Finish` |
|---|---|---|---|---|---|---|
| 1 | **P0** | (0,0,0) | ✓ | (0,0,0) | **(0,1,0)** | P0 ✓ |
| 2 | — | P1 (2,0,2) / P2 (0,0,1) / P3 (1,0,0) / P4 (0,0,2) | all ✗ | (0,1,0) | — | stuck |

`P2` now needs one `C` and `Work` has no `C`; `P3` needs `A`; `P1` needs `A` and `C`; `P4` needs two
`C`. Nobody can move.

> *"Can reclaim resources held by process P0, but insufficient resources to fulfill other process
> requests. Deadlock exists, consisting of processes P1, P2, P3, and P4."*

So the answer to a detection question is **a set of processes**, and it may be a strict subset of the
system. Note also that `(0,0,1)` could never be *granted* (`Available` has no free `C`), yet the
detection algorithm does not care: it is answering "is anybody stuck?", not "can this request be met?".

---

## 10. Putting it all together

### 10.1 Which question are you being asked?

| Wording in the question | The mechanism | What to do |
|---|---|---|
| "Identify **which condition** is violated / prevented" | the four conditions (§4) | name it, then say *why* |
| "Draw / read the graph; is there a deadlock?" | RAG (§3) | look for a cycle, then count instances per type |
| "**How could you prevent** this deadlock?" | prevention (§6) | pick a condition and give a mechanism + its cost |
| "Is the system in a **safe state**?" | safety algorithm (§8.3) | `Need = Max − Allocation`, then the `Work`/`Finish` trace |
| "**Can this request be granted?**" | resource-request algorithm (§8.6) | three checks, pretend, safety, restore if unsafe |
| "Which processes are **deadlocked**?" | detection (§9) | `Request ≤ Work` trace, report the `Finish == false` set |

### 10.2 The three algorithms on one page

| | Safety (§8.3) | Resource-request (§8.6) | Detection (§9.3) |
|---|---|---|---|
| Input | `Available`, `Allocation`, `Need` | + `Request_i` | `Available`, `Allocation`, `Request` |
| Extra step before the loop | — | three checks + pretend to allocate | seed `Finish` from `Allocation_i == 0` |
| Compared against `Work` | `Need[i]` | `Need[i]` (post-pretend) | `Request[i]` |
| Output | safe / unsafe + a safe sequence | grant / wait / error | deadlocked set |
| On failure | report unsafe | **restore the old state** | report the deadlock |

All three share the same skeleton — `Work = Available`, repeatedly finish any process whose vector fits,
add its `Allocation` back — which is why the notes say detection *"is actually similar to deadlock
avoidance"*. Learn the skeleton once, then learn the three differences.

---

## 11. Algorithm and definition sheet

```
DEADLOCK (S04)
    a set of blocked processes, each holding a resource and waiting for
    a resource held by another process in the set

FOUR CONDITIONS (S15-S16)   necessary, not sufficient
    mutual exclusion   one process at a time per instance
    hold and wait      holds >= 1 and waits for more
    no preemption      release only voluntarily, after completion
    circular wait      P0 waits for P1, ..., Pn waits for P0

SAFE SEQUENCE (S25)
    <P1..Pn> is safe iff for every Pi:
        Need(Pi) <= Available + SUM{ Allocation(Pj) : j < i }
    system is SAFE iff at least one safe sequence exists

BANKER'S DATA (S29)
    Need = Max - Allocation                       (Max never changes)
    Available[j] + SUM_i Allocation[i][j] = total instances of Rj

SAFETY (S30)
    Work = Available ; Finish[i] = false
    loop: pick i with Finish[i] == false and Need[i] <= Work
          Work += Allocation[i] ; Finish[i] = true
    all Finish true -> safe (pick order = safe sequence)

REQUEST (S34-S35)
    Request_i <= Need_i      else ERROR
    Request_i <= Available   else WAIT
    pretend: Available -= R ; Allocation_i += R ; Need_i -= R
    safety -> grant, else restore and wait

DETECTION (S41)
    Work = Available
    Finish[i] = (Allocation_i == 0)
    loop: pick i with Finish[i] == false and Request[i] <= Work
          Work += Allocation[i] ; Finish[i] = true
    any Finish[i] == false -> Pi is deadlocked

RAG (S08, S13)
    Pi -> Rj  request edge      (removed when granted)
    Rj -> Pi  assignment edge   (removed when released)
    no cycle            -> no deadlock
    cycle, 1 instance   -> deadlock
    cycle, >1 instance  -> possible deadlock
```

---

## 12. Practice problems

Try before reading the solutions.

**P1.** Two resource types, `R1` and `R2`, one instance each. `P1` holds `R1` and requests `R2`;
`P2` holds `R2` and requests `R1`. Draw the graph, and decide whether the system is deadlocked. Would
your answer change if `R2` had two instances and the second were free?

**P2.** Of the four conditions, which one is violated by each of: (a) a philosopher who must take both
chopsticks or neither; (b) chopsticks numbered and always taken low-to-high; (c) a philosopher who
drops a held chopstick when the other is unavailable; (d) two read-only readers of the same file.

**P3.** `Available = 1`. `P1` holds 1 and needs 1; `P2` holds 1 and needs 2; `P3` holds 1 and needs 3.
Is `<P3, P1, P2>` safe? Is `<P1, P2, P3>` safe? Is the system safe?

**P4.** Using the `T0` snapshot of §8.4, which processes can be chosen **first** by the safety
algorithm, and why can `P0` never be first?

**P5.** From the state after the §8.7 grant (`Available = (2,3,0)`, `Need0 = (7,4,3)`), can `P0`
request `(2,2,0)`? Show the three checks and the safety test.

**P6.** In the detection example of §9.4, suppose `P1`'s request becomes `(2,1,2)` instead of `(2,0,2)`.
Does the deadlock of §9.5 still occur?

**P7.** A system has 5 chopsticks and 5 philosophers. Explain, in one or two sentences, why "at most
four hungry philosophers at a time" makes deadlock impossible — and which condition it removes.

**P8.** Why does Banker's algorithm need `Max` when the detection algorithm does not? Give one practical
consequence.

### Solutions

**S1.** Edges: `P1 → R2`, `R2 → P2`, `P2 → R1`, `R1 → P1`. The cycle is
`P1 → R2 → P2 → R1 → P1`, and each type has **one** instance → **deadlock**. If `R2` had a second, free
instance, `P2`'s request could be satisfied from it; `P2` would finish, release `R1`, and `P1` would
then finish — **no deadlock**, exactly the S12 pattern ("cycle, but an instance outside the cycle breaks
it").

**S2.** (a) **hold and wait** — no process holds anything while waiting. (b) **circular wait** — a strict
order cannot close a cycle. (c) **no preemption** — the held resource is released by force. (d) none of
them: the resource is shareable, so **mutual exclusion** does not apply and there is nothing to
deadlock over.

**S3.** `<P3, P1, P2>`: `P3` needs 3, `Available = 1` → cannot start → **not safe**. `<P1, P2, P3>`:
`P1` needs 1 ≤ 1 ✓ → `Available = 1 + 1 = 2`; `P2` needs 2 ≤ 2 ✓ → `Available = 3`; `P3` needs 3 ≤ 3 ✓ →
**safe**. Since one safe sequence exists, **the system is safe** — safety is an existential claim.

**S4.** Only `P1` `(1,2,2)` and `P3` `(0,1,1)` fit inside `(3,3,2)`. `P0` needs `(7,4,3)`, and `7 > 3`
on resource A: no amount of simulation can start a process whose `Need` exceeds the free instances at
step 1. (`P2` `(6,0,0)` and `P4` `(4,3,1)` also exceed `A = 3`.)

**S5.** Step 1: `(2,2,0) ≤ Need0 (7,4,3)` ✓. Step 2: `(2,2,0) ≤ Available (2,3,0)` ✓. Pretend:
`Available = (0,1,0)`, `Allocation0 = (2,3,0)`, `Need0 = (5,2,3)`. Safety with `Work = (0,1,0)`:
`P0 (5,2,3)` ✗, `P1 (0,2,0)` ✗ (`B: 2 > 1`), `P2 (6,0,0)` ✗, `P3 (0,1,1)` ✗ (`C: 1 > 0`), `P4 (4,3,1)` ✗.
No process is eligible → **unsafe → refuse**, `P0` waits, state restored.

**S6.** `Request1 = (2,1,2)`. `Work = (0,0,0) → P0 (0,0,0) ✓ → (0,1,0)`. `P2 (0,0,0) ✓ → (3,1,3)`.
`P3 (1,0,0) ✓ → (5,2,4)`. `P1 (2,1,2) ≤ (5,2,4)` ✓ → `(7,2,4)`. `P4 (0,0,2) ✓ → (7,2,6)`.
**All finished — no deadlock.** Compare with §9.5: the extra `C` was fatal, the extra `B` is not,
because `C` was the resource that `Work` had none of.

**S7.** Each hungry philosopher holds at most one chopstick, so four philosophers can hold at most four
of the five; at least one chopstick is therefore free or held by a philosopher who can complete. A
circular wait of five needs five simultaneous holders. It removes **circular wait** (`k` competitors
for `k` resources cannot form a full ring).

**S8.** Safety/avoidance asks "**could** this lead to a deadlock?", which needs each process's future
maximum claim (`Max`) to compute `Need`. Detection asks "**is** anybody stuck now?", which needs only
the pending `Request`. Practical consequence: `Max` cannot be known in a general-purpose OS (a process's
future requests are not declared), so no mainstream OS runs Banker's — they ignore deadlocks (S18) and
detect them only if they care.

---

## 13. Self-test questions

1. Give the three-clause definition of deadlock and say which clause rules out ordinary queuing.
2. What are the two edge types in a resource-allocation graph, and when is each removed?
3. Why do the instance dots matter when you draw an assignment edge?
4. State the three "basic facts" about cycles.
5. In the S12 graph there is a cycle and no deadlock. What exactly breaks the cycle?
6. Name the four conditions, and say which one is a property of the resource rather than the protocol.
7. "The four conditions are necessary but not sufficient." Explain both halves.
8. Give four prevention techniques for dining philosophers, one per condition (or "impossible").
9. Why can mutual exclusion usually not be removed?
10. What is the difference between prevention and avoidance, in one sentence?
11. Define a safe sequence. Why is the condition cumulative?
12. Why does an unsafe state not imply a deadlock?
13. Write the four data structures of Banker's algorithm and the relation between them.
14. What changes on a granted request, and what deliberately does not?
15. Why is a request that fails the `Request ≤ Need` check an error rather than a wait?
16. Name two differences between the safety algorithm and the detection algorithm.
17. Why is detection not examined, and what is the one thing worth remembering about it?
18. Give two ways recovery can starve a process.

### Answer sketches

1. Blocked; holding; waiting for a resource held by another process **in the set**. The third clause —
   the closed waiting relation.
2. Request `Pi → Rj`, removed when granted; assignment `Rj → Pi`, removed when released.
3. Because the assignment edge starts at a **specific instance**, so the remaining dots tell you how
   many instances are free — which is what decides the multi-instance case.
4. No cycle ⇒ no deadlock; cycle with one instance per type ⇒ deadlock; cycle with several instances ⇒
   possible deadlock.
5. The **second, free instance** of the multi-instance type: `P2`'s pending request can be granted, so
   `P2` finishes and releases `R1`, which lets the rest proceed.
6. Mutual exclusion; hold-and-wait; no preemption; circular wait. **Mutual exclusion** is a property of
   the resource.
7. Necessary: all four must hold for a deadlock, so breaking one prevents it. Not sufficient: all four
   can hold with nothing stuck (no cycle, or a cycle that a free instance can break).
8. Mutual exclusion — impossible; hold-and-wait — take both or neither; no preemption — drop the held
   chopstick; circular wait — number the chopsticks and request low-to-high (or cap at four hungry).
9. Because two processes cannot use one chopstick / printer / tape simultaneously; "removing" it would
   mean the resource is shareable, i.e. it is not that resource any more.
10. Prevention removes a condition by rule, at design time; avoidance tests the current state on every
    request and refuses requests that could lead to an unsafe state.
11. `<P1…Pn>` where each `Pi` can be satisfied from `Available + Allocation` of all earlier `Pj`. It is
    cumulative because finishing `Pj` **releases** everything `Pj` held, which `Pi` can then use.
12. Because the test assumes the worst case — every process holds everything until it terminates. A
    process that releases early may let the system finish anyway.
13. `Available` (length `m`), `Max`, `Allocation`, `Need` (`n × m`), with `Need = Max − Allocation`.
14. `Available ↓`, `Allocation_i ↑`, `Need_i ↓`; `Max` is unchanged (it is the declared maximum).
15. Because it means the process asked for more than the maximum it declared — a violation of the
    algorithm's contract, not a shortage of resources.
16. Detection compares `Request` (not `Need`), seeds `Finish` from `Allocation_i == 0`, and reports a
    **deadlocked set** rather than safe/unsafe. It also needs no `Max`.
17. S39 says so. Worth remembering: it is the same loop with `Request` in place of `Need`.
18. (a) All-or-nothing acquisition: a process may always lose the race for the full set. (b) Recovery
    that always picks the cheapest victim: that process is rolled back forever.


---

## 14. Glossary

| Term | Meaning |
|---|---|
| **Deadlock** | a set of blocked processes, each holding a resource and waiting for one held by another process in the set |
| **Starvation** | indefinite postponement — a process is runnable but never gets the resource; *not* the same as deadlock |
| **Resource type / instance** | `Ri` is a kind of resource; `Wi` identical instances of it exist |
| **Resource-allocation graph (RAG)** | directed graph of processes and resource types with request and assignment edges |
| **Request edge** | `Pi → Rj`: `Pi` is waiting for an instance of `Rj`; removed when granted |
| **Assignment edge** | `Rj → Pi`: an instance of `Rj` is allocated to `Pi`; removed when released |
| **Cycle** | a closed path in the graph; conclusive evidence of deadlock only for single-instance types |
| **Mutual exclusion** | at most one process may use an instance at a time |
| **Hold and wait** | a process holding resources waits for more |
| **No preemption** | resources are released only voluntarily, after the holder finishes |
| **Circular wait** | a closed chain of waiters `P0 → P1 → … → Pn → P0` |
| **Prevention** | make one of the four conditions impossible, by design |
| **Avoidance** | refuse requests that would leave the system in an unsafe state |
| **Safe state** | at least one safe sequence of all processes exists |
| **Safe sequence** | an order in which every process's remaining need can be met from `Available` + what earlier processes release |
| **Unsafe state** | no safe sequence exists; deadlock is possible, not certain |
| **`Available`** | vector: free instances of each type |
| **`Max`** | matrix: each process's declared maximum claim |
| **`Allocation`** | matrix: instances currently held by each process |
| **`Need`** | matrix: `Max − Allocation`, what each process may still request |
| **`Request`** | matrix/vector: what a process is asking for **now** (detection and the request algorithm) |
| **`Work` / `Finish`** | the two working vectors of the safety and detection algorithms |
| **Banker's algorithm** | avoidance for multiple instances: safety algorithm + resource-request algorithm |
| **Detection** | letting deadlock happen, then finding the deadlocked set with `Request ≤ Work` |
| **Recovery** | breaking a detected deadlock — abort all, or abort victims one at a time |
| **Ostrich approach** | ignore deadlock entirely; used by most OSes, including UNIX (S18) |

---

## 15. Advanced readings (S45)

The deck closes with three pointers, *"if you want to know more beyond the text book"*:

| Reading | Note |
|---|---|
| *"The Deadlock Problem: An Overview"*, Sreekaanth S. Isloor & T. Anthony Marsland | PDF on NTULearn; the survey the chapter's framing comes from |
| *Java Concurrency* — `docs.oracle.com/javase/tutorial/essential/concurrency/` | the "Deadlock" and "Starvation and Livelock" pages are the practical version of §5–§6 |
| *Deadlock* — `en.wikipedia.org/wiki/Deadlock` | quick reference for the four conditions and the taxonomy |

Nothing in this list is examinable beyond what the slides already say; the Java tutorial is the most
useful of the three, because it shows the **lock-ordering** fix (§6.5) as it is actually written in
code.
