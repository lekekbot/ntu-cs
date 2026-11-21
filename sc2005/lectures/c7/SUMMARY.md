# Deadlocks — Summary (one page)

One deck, one question: **several processes each hold something and each want something another one
holds — when is the system stuck, how do you prove it, what do you do about it?**

---

## The 60-second version

1. **Deadlock** = a set of **blocked** processes, each **holding** a resource and **waiting** for one
   held by another process **in the set**. Not running, holding, waiting *inside a cycle*.
2. **Model it**: resource types `R1…Rm`, `Wi` identical instances each; a process
   **requests → uses → releases**. Draw it as a **resource-allocation graph**: `Pi → Rj` is a
   **request** edge, `Rj → Pi` is an **assignment** edge.
3. **No cycle ⇒ no deadlock.** A cycle with **one instance per type ⇒ deadlock**. A cycle with
   **several instances per type ⇒ possible, not certain** — the reason Banker's algorithm exists.
4. **Four conditions** must hold simultaneously: **mutual exclusion**, **hold-and-wait**,
   **no-preemption**, **circular wait**. **Necessary, not sufficient** — breaking any **one**
   prevents deadlock.
5. **Four strategies**: **prevention** (break a condition, design-time), **avoidance** (never enter
   an unsafe state), **detection + recovery** (let it happen, find it, fix it), **ignore** — the
   *ostrich* approach used by UNIX and most systems, for **efficiency**.
6. **Prevention, on dining philosophers**: mutual exclusion cannot be broken (chopsticks are not
   shareable); **hold-and-wait** → take both or neither; **no-preemption** → drop what you hold if the
   second is unavailable; **circular wait** → at most four hungry, or **request chopsticks in
   increasing ID order** (S22).
7. **Safe state** = a **safe sequence** `<P1…Pn>` exists in which each `Pi` is satisfiable from
   `Available + the holds of all earlier Pj`. **Safe ⇒ no deadlock. Unsafe ⇒ possibility only**,
   because the analysis assumes everyone holds resources until they finish.
8. **Banker's algorithm** = avoidance with multiple instances. `Need = Max − Allocation`.
   **Safety algorithm** asks "is this state safe?"; **resource-request algorithm** pretends to
   allocate, runs safety, and rolls back if the answer is unsafe.
9. **Detection** = the safety algorithm with `Request` instead of `Need`, run after the deadlock is
   already allowed. **Not examinable** (S39).
10. **Starvation** is the title's second word and the residual risk of every scheme here:
    all-or-nothing acquisition and fixed-victim recovery can both postpone one process forever.

---

## The four handling strategies

| Strategy | Decided | Needs to know | What it attacks | Price |
|---|---|---|---|---|
| **Prevention** | **design time**, by rule | nothing about the future | forces **one of the four conditions** false | the restriction applies always; utilisation drops |
| **Avoidance** (Banker's) | **every request**, before granting | every process's **maximum claim up front** | the *state*: denies any request that would leave **no safe sequence** | `Max` must be known; conservative; `O(n²m)`; a request can wait forever |
| **Detection + recovery** | **periodically**, after the fact | `Allocation` + **current** `Request` (no `Max`) | **none** — all four hold | detection cost, victim choice, rollback |
| **Ignore (ostrich)** | never | nothing | **none** | a rare hang; used by **most OSes incl. UNIX** — overhead of the other two is high |

Only **prevention** names a condition. **Avoidance** avoids the *state*, not the *condition* —
that distinction is worth a mark in each direction.

---

## Banker's algorithm

**Data structures** (`n` processes, `m` resource types)

| Structure | Shape | Meaning |
|---|---|---|
| `Available` | vector, length `m` | `Available[j] = k` → `k` free instances of `Rj` |
| `Max` | `n × m` | `Max[i,j] = k` → `Pi` may request **at most** `k` of `Rj` |
| `Allocation` | `n × m` | `Allocation[i,j] = k` → `Pi` currently holds `k` of `Rj` |
| `Need` | `n × m` | `Need[i,j] = k` → `Pi` still needs `k` more; **`Need = Max − Allocation`** |

**1. Safety algorithm** — is this state safe?

```
Work = Available ;  Finish[i] = false for all i
repeat:
  find i with Finish[i] == false and Need[i,*] <= Work        (*)
  if none -> go to the end
  Work = Work + Allocation[i,*] ;  Finish[i] = true           (**)
end
all Finish true -> SAFE (the order you picked is a safe sequence)
otherwise       -> UNSAFE
```

`Work` is `Available + everything held by the processes already marked finished`. Any order that
works is a valid answer — *"what if multiple answers? any one can be chosen"* (S30).

**2. Resource-request algorithm** — may `Pi` have `Request_i`?

```
1. Request_i <= Need_i      ?  no -> ERROR (exceeded its maximum claim)
2. Request_i <= Available   ?  no -> Pi waits
3. pretend:  Available -= Request_i
             Allocation_i += Request_i
             Need_i       -= Request_i          (Max is NOT changed)
4. run the safety algorithm
   safe   -> grant
   unsafe -> refuse, restore the old state, Pi waits
```

---

## Worked numbers worth remembering

### Safety algorithm — 5 processes, `A(10) B(5) C(7)` (S31–S33)

| Process | Allocation | Max | Need |
|---|---|---|---|
| P0 | (0,1,0) | (7,5,3) | (7,4,3) |
| P1 | (2,0,0) | (3,2,2) | (1,2,2) |
| P2 | (3,0,2) | (9,0,2) | (6,0,0) |
| P3 | (2,1,1) | (2,2,2) | (0,1,1) |
| P4 | (0,0,2) | (4,3,3) | (4,3,1) |

`Available = (3,3,2)`

| Step | Pick | `Need` | `Work` before | `Work` after |
|---|---|---|---|---|
| 1 | **P1** | (1,2,2) | (3,3,2) | **(5,3,2)** |
| 2 | **P3** | (0,1,1) | (5,3,2) | **(7,4,3)** |
| 3 | **P4** | (4,3,1) | (7,4,3) | **(7,4,5)** |
| 4 | **P0** | (7,4,3) | (7,4,5) | **(7,5,5)** |
| 5 | **P2** | (6,0,0) | (7,5,5) | **(10,5,7)** |

**Answer: safe, `<P1, P3, P4, P2, P0>`.** Only `P1 (1,2,2)` and `P3 (0,1,1)` fit inside `(3,3,2)`, so
a safe sequence must start with one of them; `P0` needs `(7,4,3)` and `P2` needs `(6,0,0)`.

**Then `P1` requests `(1,0,2)`** → `(1,0,2) ≤ Need1 (1,2,2)` ✓, `≤ Available (3,3,2)` ✓ →
`Available = (2,3,0)`, `Allocation1 = (3,0,2)`, `Need1 = (0,2,0)` → safe,
**`<P1, P3, P4, P0, P2>`**. Granted.

**A second `(1,0,2)` by P1 is refused at step 1**: `(1,0,2) ≰ (0,2,0)`. Error, not "wait".

**`P0` requests `(0,2,0)`** → state becomes `Available (2,1,0)`, `Need0 (7,2,3)` → **no** process
has `Need ≤ (2,1,0)` → **unsafe → restore**, `P0` waits.

### Detection algorithm — 5 processes, `A(7) B(2) C(6)` (S42–S44)

| Process | Allocation | Request |
|---|---|---|
| P0 | (0,1,0) | (0,0,0) |
| P1 | (2,0,0) | (2,0,2) |
| P2 | (3,0,3) | (0,0,0) |
| P3 | (2,1,1) | (1,0,0) |
| P4 | (0,0,2) | (0,0,2) |

`Available = (0,0,0)` → `Work (0,0,0) → P0 → (0,1,0) → P2 → (3,1,3) → P3 → (5,2,4) →
P1 → (7,2,4) → P4 → (7,2,6)` → **no deadlock**, `<P0, P2, P3, P1, P4>`.

Let **P2 request one more `C`**: `Request2 = (0,0,1)`, `Available` still `(0,0,0)`.
Only `P0` can finish (`Work` → `(0,1,0)`); then `P2` needs `C = 1 > 0` and nobody else fits.
**Deadlock: `P1, P2, P3, P4`** — only `P0`'s resources can be reclaimed.

---

## Ten things that decide exam marks

1. **Cycle ⇏ deadlock** when a resource type has several instances. Cycle ⇒ deadlock only with **one
   instance per type**.
2. **Safe ⇒ no deadlock. Unsafe ⇏ deadlock.** Unsafe means "no safe sequence", not "stuck".
3. **`Need = Max − Allocation`, and `Max` never changes.** Subtracting a granted request from `Max`
   is the commonest arithmetic error.
4. **`Request` (S34) ≠ the `Request` column on S26.** There it is the *remaining need* — Banker's
   `Need`. `Request` is a pending ask.
5. **The four conditions are necessary, not sufficient.** Violating one prevents deadlock; satisfying
   all four does not prove one.
6. **Avoidance ≠ prevention.** Prevention bans a condition forever; avoidance checks a *state* on
   every request and may deny a request because of the future.
7. **Banker's needs `Max` up front**, which is why no real OS uses it; detection needs only
   `Allocation` and `Request`.
8. **Detection is not examinable** (S39), but it is the cheapest check on your understanding: same
   loop as safety, `Request` instead of `Need`.
9. **Recovery is not free.** Backing one car off the bridge can force several to reverse (S05) — the
   victim's dependants pay too.
10. **Starvation is the residual risk.** Deadlock-freedom does not imply fairness: all-or-nothing
    acquisition and fixed-victim recovery can both postpone one process forever.

---

## What is *not* in this series

* **Recovery algorithms.** S39 says recovery is *"in textbook"* — victim selection, rollback and
  checkpointing are on no slide.
* **Deadlock detection, in detail.** **Not examinable** (S03, S39); the six slides S39–S44 exist for
  contrast only.
* **Starvation as a topic.** It is in the chapter title on every outline slide (S03, S06, S14, S17,
  S23, S38) but **no slide defines it or gives a starvation-avoidance algorithm.**
* **The odd-even philosophers solution.** S21 says *"see previous lecture"*; only the chopstick
  ordering fix (S22) is developed here.
* **Wait-for graphs** and the single-instance detection algorithm: one line on S39, nothing more.
