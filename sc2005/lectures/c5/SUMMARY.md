# Process Synchronization — Summary (one page)

One deck, one question: **two processes, one shared variable, one preemptible CPU — what can go
wrong, and what does the OS give you to stop it?** Citations are slide numbers (`S17` = slide 17);
there is no recording for this deck.

---

## The 60-second version

1. **The bug.** `counter++` is three instructions (`load`, `add`, `store`). A context switch between
   any two of them lets a second process read a stale value. That is a **race condition** — the
   result depends on the interleaving, not on the code.
2. **The rule.** Put every access to shared data in a **critical section**, and guarantee *at most
   one process inside at any time*. Entry section asks; exit section notifies; the rest is the
   remainder section.
3. **The test.** Any solution must satisfy **mutual exclusion**, **progress** and **bounded
   waiting**. All three, or it is wrong.
4. **Software tries.** Alg 1 (`turn`) — ME yes, **progress no**: an uninterested process can block
   you. Alg 2 (`flag[]`) — ME yes, **progress no**: both wait forever. Alg 3 (`flag[] + turn`,
   Peterson) — all three, but only for two processes and far too subtle to trust.
5. **Hardware answers.** `TestAndSet(&lock)` is one atomic instruction: read the old value, write
   `true`. ME ✓, progress ✓ — but **bounded waiting ✗**: the lock has no queue, so a fast re-acquirer
   wins forever (`S27`).
6. **The OS answers.** A **semaphore** is an integer plus two atomic operations, `Wait` and
   `Signal`. Binary (init 1) = mutex; counting (init *n*) = *n* instances of a resource; init 0 =
   ordering ("B only after A").
7. **Two implementations.** **Busy waiting** (spin, no context-switch cost, burns CPU) and
   **blocking** (`value` + list `L` + `block()`/`wakeup()`). *Both* still need `Wait`/`Signal` to be
   atomic — the check and the update must be one indivisible step.
8. **Misuse kills.** Wrong acquisition order → **deadlock** (`S40`). Wrong queue discipline →
   **starvation** (`S41`). Cure for the latter: aging.
9. **The three set pieces.** Bounded buffer (`mutex`/`empty`/`full`), dining philosophers
   (`chopstick[5]`, deadlock, three remedies), readers-writers (`readcount`/`mutex`/`wrt`).
10. **Monitors** wrap the whole thing into a type whose methods are automatically exclusive —
    *"This slide is not examinable"* (`S54`).

---

## The five solutions, side by side

| Technique | Entry section | Mutual exclusion | Progress | Bounded waiting |
|---|---|---|---|---|
| **Algorithm 1** — `turn` | `while (turn != i);` | ✓ | ✗ uninterested process blocks the other | ✓ |
| **Algorithm 2** — `flag[]` | `flag[i]=true; while (flag[k]);` | ✓ | ✗ both spin forever | ✓ (vacuous: nobody enters) |
| **Algorithm 3** — Peterson | `flag[i]=true; turn=k; while (flag[k] && turn==k);` | ✓ | ✓ | ✓ |
| **TestAndSet** — `lock` | `while (TestAndSet(&lock));` | ✓ | ✓ | ✗ a starved process can wait forever |
| **Semaphore** — `mutex` | `Wait(mutex);` | ✓ | ✓ | ✓ if the queue is FIFO (✗ with priority/LIFO, `S41`) |

Why each failure happens, in one line each:

* **Alg 1** knows *whose turn it is*, not *who wants in*.
* **Alg 2** knows *who wants in*, but neither backs off when both do.
* **Alg 3** adds the tie-break: the **last** writer of `turn` loses.
* **TestAndSet** implements a **lock**, not a **queue** — fairness needs memory of the waiters.
* **Semaphore** keeps that memory in `L`.

---

## Semaphore pseudocode

```c
/* abstraction (S28) */                 /* busy waiting (S30) */
Wait(S):   if (S > 0) S--; else wait();  Wait(S):   while (S <= 0); S--;
Signal(S): S++;                          Signal(S): S++;

/* blocking (S32-S34) */
typedef struct { int value; struct process *L; } semaphore;

Wait(S):   S.value--;  if (S.value <  0) block();
Signal(S): S.value++;  if (S.value <= 0) wakeup(P);

/* the two idioms */
binary  mutex = 1;   Wait(mutex); ... critical section ... Signal(mutex);
counting empty = n, full = 0;   producer: Wait(empty) ... Signal(full)   consumer: Wait(full) ... Signal(empty)
ordering flag = 0;   Pi: A; Signal(flag);        Pk: Wait(flag); B
```

The two comparisons are deliberately opposite: after a **decrement**, `< 0` means "I did not get a
permit"; after an **increment**, `<= 0` means "someone was already waiting".

---

## Worked numbers worth remembering

**`counter = 5`, one produce, one consume (`S09`).**

```
P: reg1 = counter (5)      C: reg2 = counter (5)
P: reg1 = reg1 + 1 (6)     C: reg2 = reg2 - 1 (4)
        -- switch -->              -- switch -->
P: counter = reg1 -> 6     C: counter = reg2 -> 4
```

Final value **4**, not 5 — one item lost. Possible finals are **{4, 5, 6}**: 4 = lost increment,
6 = lost decrement, 5 = the two sequences did not interleave.

**Negative semaphore values (`S34`).**

```
S.value =  3  ->  3 free instances
S.value =  0  ->  none free, nobody waiting
S.value = -2  ->  2 processes blocked in L      |L| = -S.value
```

Transitions: `1 --Wait--> 0` (enter) · `0 --Wait--> -1` (block) · `-1 --Signal--> 0` (**wakeup**) ·
`0 --Signal--> 1` (**no wakeup**) · `-2 --Signal--> -1` (wakeup).

**`TestAndSet` starvation (`S27`).** RR, quantum 10 ms; acquire = 10 ms; full loop = 10 ms.
Quanta: `P0(1,2,3)` acquires · `P1(1,2)` only tests · `P0(4,5,6,2,3)` releases **and re-acquires** ·
`P1(2)` only tests · repeat. P1 never enters → bounded waiting ✗.

**Bounded buffer, `n = 5`.** After 5 items: `full = 5`, `empty = 0`. A 6th `Wait(empty)` → `-1` and
the producer blocks. Invariant (while nothing is blocked): `full = n − empty`.

**Readers-writers.** `readcount` 0→3 as three readers arrive: `wrt` taken once by reader #1, released
once by reader #3. `readcount == 1` ⇒ take `wrt`; `readcount == 0` ⇒ release `wrt`.

---

## Ten things that decide exam marks

1. **`counter++` is not atomic** — three instructions, three preemption points.
2. **Progress is not bounded waiting.** Progress = the system always admits *someone*; bounded
   waiting = *you* are admitted within a bounded number of others.
3. **Alg 1 and Alg 2 both fail progress** (not mutual exclusion). Alg 2's failure is a livelock.
4. **Bounded waiting is the property `TestAndSet` fails** — and a plain lock cannot fix it.
5. **`Wait`/`Signal` must be atomic even in the blocking implementation**; the update *and* the test.
6. **`S.value--` comes before `block()`**, or mutual exclusion breaks (`S36`).
7. **Negative `S.value` = number of waiting processes**; `0` = none free, nobody waiting.
8. **`Signal` never blocks** — it only increments and maybe wakes someone.
9. **Acquire the counting semaphore before the mutex**, or you deadlock when the buffer is empty
   (`S46`).
10. **Dining philosophers deadlock needs all five holding their first chopstick**; the fix must break
    circular wait or hold-and-wait.

---

## What is *not* in this series

* **Deadlock and starvation as a topic.** `S40`–`S41` are semaphore *misuse* only. Conditions,
  prevention, avoidance (Banker's), detection, recovery → [`../c7`](../c7).
* **Monitors beyond one slide.** `S54` is marked *"not examinable"*; no condition variables, no
  `wait`/`signal` inside a monitor.
* **The textbook's bounded-waiting `TestAndSet` algorithm** — `S26` says explicitly it is *"in the
  textbook – not examinable"*.
* **Real code.** No `pthread_mutex`, no `mutex_lock()`, no memory-ordering or cache-coherence
  discussion.
* **Proofs.** `S21` says the Peterson proof is *"just for your reference"*; the examinable skill is
  the interleaving argument.
