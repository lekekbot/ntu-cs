# Process Synchronization — Things to Take Note Of

The "before the exam" file: what the deck keeps hammering, what is easy to get wrong, and where the
slides themselves are unreliable. It contains **no new teaching** — the teaching is in
[STUDY_GUIDE.md](STUDY_GUIDE.md).

There is **no recording** for this deck, so every pointer here is a slide number (`S17` = slide 17).

---

## 1. What is repeatedly stressed

| Point | Where | Why it matters |
|---|---|---|
| **"Important but difficult"** — two whole weeks, an extra slide stack with animations on NTULearn | `S02` note | This is the chapter the course expects you to find hard. The animations are exactly the interleavings you are examined on. |
| **Enumerate the interleavings** — "We should consider context switches in **any** place of process execution" | `S03` note, `S11` note | Every property proof in the chapter is an interleaving argument. There is no other proof technique in the deck. |
| **All three properties, or it is wrong** | `S13` note | "If any of the three requirements is violated, the solution is wrong." Not "mostly right". |
| **You are not required to memorise the algorithms** — only to analyse them | `S21` note | The code of Alg 1–3 is on the slides; the marks are in the property table. |
| **"Questions on this part in every past exam paper"** | `S28` note | Semaphores are the highest-yield topic in the course. |
| **Remove all the `Wait`/`Signal` and the sequential logic is still correct** | `S38` note | The self-check that your semaphores are doing synchronisation and not computation. |
| **Atomicity is required even for blocking semaphores** | `S35` note | Students assume blocking removes the race. It does not; it only removes the spinning. |

---

## 2. Exam traps

1. **`counter++` is three instructions.** `load`, `add`, `store`. Any answer that treats it as one
   atomic operation loses the marks for the `counter = 5` question.
2. **The final value is not always 4.** With one produce and one consume from 5 you can get **4, 5 or
   6**; `S09` shows only the `4` case. Say which interleaving gives which.
3. **Mutual exclusion, progress and bounded waiting are three *different* failures.** A solution that
   lets one process spin forever fails **progress**, not mutual exclusion — nobody is inside, so ME is
   intact.
4. **Alg 1 fails progress, not ME.** The reason is that `turn` records *whose turn*, not *who wants
   in*, so an uninterested process in a long remainder section holds the other hostage.
5. **Alg 2 fails progress, not ME.** The `T0`/`T1` interleaving (`S19`) gives a **livelock**: both
   processes are running and spinning, neither is blocked.
6. **`S19`'s bounded-waiting line is an ME argument.** The slide ticks BW ✓ but justifies it with
   *"Once P0 sets `flag[0] = true`, process P1 cannot enter"* — that is mutual exclusion. If asked,
   say BW is only *vacuously* satisfied (nobody enters); the real defect is progress. See §3 below.
7. **`TestAndSet` fails bounded waiting** — this is *the* asked-for property analysis of the chapter.
   Ask yourself "which process is never granted?" rather than "can two enter?".
8. **`TestAndSet` always writes `true`.** It is not a conditional store; the caller learns the old
   value only from the return value.
9. **`TestAndSet`'s starvation has nothing to do with priorities.** The slide uses **plain
   round-robin with equal quantum**; the unfairness is in the lock, which has no queue.
10. **`Wait`/`Signal` must be atomic even with blocking semaphores.** Making only `S.value--` atomic
    is not enough — it is the *check-then-act pair* that must be indivisible.
11. **`if (S.value < 0) block()` not `<= 0`.** With `<=`, the process that took the **last** permit
    blocks itself: deadlock on the first acquisition.
12. **`if (S.value <= 0) wakeup()` not `< 0`.** From `-1`, `Signal` makes it `0`; the wakeup must
    happen at `0`. Using `< 0` steals the wakeup and leaves the waiter stranded.
13. **`S.value--` before `block()`, never after.** Decrementing after `block()` requires a context
    switch inside `Wait`, and `S36`'s four-step trace then puts two processes in the critical section.
14. **Negative `S.value` = number of waiting processes.** `-2` means two blocked. `0` means *no
    permits and nobody waiting* — a very common wrong answer is "0 means one is waiting".
15. **`Signal` never blocks.** It increments and, conditionally, wakes someone. Only `Wait` can block.
16. **Acquire the resource (counting) semaphore *before* the mutex.** `Wait(mutex); Wait(full);` on an
    empty buffer deadlocks — and the deadlock is *permanent*, not "unlikely".
17. **Swapping the `Signal`s is not a bug.** `Signal(full); Signal(mutex);` is correct, only slightly
    less efficient. Do not report it as a deadlock.
18. **`counter` disappears in the semaphore version.** `full` *is* the item count and `empty` is
    `n − full`; keeping `counter` would add a third shared variable for no information.
19. **`mutex` is unnecessary with one producer and one consumer**, and mandatory with two of either —
    because `in` (resp. `out`) becomes shared. The question is about *who writes*, not about the
    buffer.
20. **Dining philosophers deadlock needs all five philosophers to hold their first chopstick.** With
    fewer contenders than chopsticks, one chopstick is always free and the cycle cannot close.
21. **Each remedy breaks a named condition.** "At most four hungry" and odd/even ordering break
    **circular wait**; "pick up both only if both are available" breaks **hold and wait**. Answers
    that just say "it avoids deadlock" get nothing.
22. **`readcount == 1` / `readcount == 0`, not `>= 1` / `<= 1`.** Only the **first** reader takes `wrt`
    and only the **last** releases it. Any other test either double-takes or double-releases.
23. **Readers-preference ⇒ writers starve.** Arriving readers only need `mutex`, so a steady stream of
    readers postpones a waiting writer indefinitely. That is a `S41` starvation, by design.
24. **The first reader blocks on `wrt` while holding `mutex` — and it is fine.** No deadlock, because a
    writer never needs `mutex`. Do not "fix" it.
25. **Monitors are marked not examinable.** One slide (`S54`), banner on the slide itself. Do not spend
    revision time on condition variables.

---

## 3. Known slips, typos and inconsistencies in the slides

These are in the deck, not in the transcription. Learn the correct version.

| Where | What the slide shows | Correct / better version |
|---|---|---|
| `S19` | Marks **Bounded Waiting ✓** and justifies it with *"Once P0 sets `flag[0] = true`, process P1 cannot enter its critical section"* | That sentence is an argument for **mutual exclusion**. Alg 2's failure is **progress** (the `T0`/`T1` livelock). BW is only vacuously true because nobody ever enters. |
| `S27` | "Suppose for P0 lines 1-3 take 10ms and **2-6** also take 10ms" | The trace itself shows `P0 (4,5,6,2,3)` — i.e. the second quantum covers lines **4–6 plus the re-acquire**. The "2-6" in the text does not match the drawing. |
| `S28` | `Wait(S): if S > 0, S--; else, wait();` | A sketch of the *semantics*, not an implementation: an `if` cannot loop. `S30` gives the real busy-wait (`while (S <= 0);`) and `S32`–`S34` the blocking form. |
| `S28` | "Only accessible by two atomic **system calls**" | `Wait`/`Signal` are atomic *operations*; on the slides they are implemented with hardware/interrupt control, and the textbook versions can be user-level. "System call" is loose. |
| `S30` | "Pros: **No context switch overhead**" | No context switch *when the wait succeeds immediately* — spinning avoids the block/unblock pair. It still costs the loop's instructions. |
| `S34` | `wakeup(P)` — `P` appears without being bound; `block()` takes no argument | The slide is abbreviating: `block()` acts on the *current* process; `wakeup(P)` acts on the process dequeued from `L`. |
| `S36` | Alternative `Signal`: `if (S.value <= 1) wakeup(P);` | This is the mirror of `S.value--` at the end of `Wait`; the slide uses it only to make the pair consistent. Do not memorise it as a variant to use. |
| `S43` | "`in` replaced with `empty`, `out` replaced with `full`" | The *waiting role* of `in`/`out` is replaced. `in`/`out` (or equivalent indices) are still needed and are protected by `mutex`. |
| `S49` | "Each philosopher has 1 chopstick and needs another to eat" — only the five first `Wait`s are shown | Strictly each philosopher must **then attempt the second `Wait` and block**. The five first `Wait`s establish the hold; the deadlock completes on the second round. |
| `S50` | Lists **three** remedies | A fourth, the general form of the third: impose a **global order** — everyone takes the lower-numbered chopstick first. |
| `S51` | "Readers given preference (**writer preference also possible**)" | No writer-preference code is given. Be ready to describe the extra semaphore, not to write it from the slide. |
| `S53` | The first reader can block on `wrt` **while holding `mutex`** | Not discussed on the slide. Harmless (writers never take `mutex`), but it does serialise arriving readers behind a blocking writer. |
| `S54` | **"This slide is not examinable"** — yet it is slide 54 of 54 and closes the chapter | Treat it as context: know *what* a monitor is and that it is one level above semaphores. Do not memorise details. |
| `S02`, `S22`, `S37` | Outline lists *Race Condition & Critical-Section · User-level · OS-level · Synchronization Hardware · Semaphores · Classical Problems* | **Monitors are missing from the outline** although `S54` covers them. `S37` also renames the first item to "The Critical-Section Problem". Cosmetic, but do not be confused by the changing divider text. |
| `S16` | `turn = i  Pi can enter critical section` (operator missing), and per-process fragments printed as `0);` / `1;` | The missing glyph is `⇒`. The exit section is `turn = k`, i.e. `turn = 1` for `P0` and `turn = 0` for `P1`. |
| `S01` | Course overview says **`Synchronization (L5-6)`**, `Deadlocks (L7)` | Part 5 and Part 6a still print the **older scheme** `Synchronization (L4-5)` / `Deadlocks (L6)`. Same material, just renumbered — this folder is **L5–6**. |

---

## 4. Deck structure: slide numbers are the only citations

Unlike the memory/virtual-memory/file-system folders, this deck has **no audio**, so there are no
timestamps. Every cross-reference in this folder is a bare slide number.

The deck is one continuous sequence S01–S54, and the **section dividers repeat the six-part outline**
three times — `S02`, `S22` (after the software solutions) and `S37` (after the blocking semaphore).
Use them as bookmarks:

| Divider | Marks the start of |
|---|---|
| `S02` | the whole chapter |
| `S14` | *second* copy of the outline, immediately before "Initial Attempts" |
| `S22` | OS-level solutions / hardware |
| `S37` | classical problems |
| `S54` | monitors (no divider; the deck just ends) |

The `[NOTES]` blocks are speaker notes, and they are **content**, not commentary: the `S13` definition
of livelock, the `S33` policy remark, the `S38` "logical vs physical" distinction and the `S41` "aging"
answer exist *only* in the notes. §6 lists everything that is note-only.

---

## 5. Coverage map (slide → topic)

| Slides | Topic |
|---|---|
| S01 | Course overview: this deck is `Synchronization (L5-6)` |
| S02 | "Part 4: Process Synchronization" — outline, *Important but difficult* |
| S03 | Background: data inconsistency, race condition, causal ordering |
| S04–S05 | Producer-consumer with bounded buffer; shared `buffer`, `counter`, private `in`/`out` |
| S06–S07 | Producer loop and consumer loop; the empty `while (...);` wait; circular buffer |
| S08 | `counter++` vs `counter--` — the race |
| S09 | Register-level interleaving (`counter = 5` → 4) |
| S10 | Critical-section problem: definition, "at least one process writes" |
| S11 | Generic structure: entry / critical / exit / remainder |
| S12 | Assumptions; **mutual exclusion** |
| S13 | **Progress**, **bounded waiting**; livelock |
| S14 | Outline (repeat) |
| S15 | Initial attempts: two processes, user-level, no OS support |
| S16–S17 | **Algorithm 1** (`turn`): code, property analysis |
| S18–S19 | **Algorithm 2** (`flag[]`): code, property analysis, the livelock |
| S20–S21 | **Algorithm 3** (Peterson): code, property analysis, "extend to 3 processes?" |
| S22 | Outline (repeat) |
| S23 | OS support, three levels: hardware → semaphore → monitor |
| S24 | Atomicity; **`TestAndSet`** definition and interrupt handling |
| S25 | Critical section with Test-and-Set |
| S26 | Property analysis: ME ✓, progress ✓, BW ✗ (see next slide) |
| S27 | **Bounded-waiting failure**, 10 ms quantum trace |
| S28 | **Semaphore**: `Wait`/`Signal`, counting vs binary |
| S29 | Semaphore solution for the critical-section problem (`mutex = 1`) |
| S30 | **Busy-waiting** implementation + assembly + pros/cons |
| S31 | Why `Wait(S)` must be atomic (ME violation trace) |
| S32 | **Blocking** implementation: `typedef struct { int value; struct process *L; }` |
| S33 | `block()` and `wakeup()` — the three steps each |
| S34 | `Wait`/`Signal` for blocking; `-2` means 2 waiting |
| S35 | Atomicity still required: progress traces for `Wait` and `Signal` |
| S36 | Why **not** `S.value--` at the end of `Wait` (ME violation) |
| S37 | Outline (repeat) — classical problems next |
| S38 | **Best practices**: 3 steps, shared variable vs shared resource |
| S39 | Semaphore as a **general ordering tool** (`flag = 0`) |
| S40 | **Deadlock** from wrong acquisition order |
| S41 | **Starvation**; queue discipline; aging |
| S42 | The three classical problems |
| S43 | Bounded buffer with multiple producers/consumers: `full`/`empty`/`mutex` |
| S44 | Producer, step 2: protect shared data |
| S45 | Producer, step 3: manage shared resources |
| S46 | Consumer; the `Wait(mutex); Wait(full);` deadlock |
| S47 | Dining philosophers: the set-up |
| S48 | Initial solution: `chopstick[5]`, both `Wait`s |
| S49 | The deadlock interleaving |
| S50 | Three remedies |
| S51 | Readers-writers: the problem, `readcount`, `mutex`, `wrt` |
| S52 | Writer process |
| S53 | Reader process; first/last reader |
| S54 | **Monitors** — not examinable |

---

## 6. Content that exists only in the speaker notes

The `[NOTES]` blocks carry material the bullets do not. If you skipped them, you missed these:

| Slide | Note-only content |
|---|---|
| `S02` | An **extra slide stack with animations** was uploaded to NTULearn; the `S09` animation is in it |
| `S04`/`S05` | `in` = the slot the producer will fill; `out` = the item the consumer will take; both start at 0 with `counter` |
| `S06` | *"pay attention to the **semicolon**"* — the wait is an empty loop |
| `S07` | `counter` is the shared variable; `buffer` is shared as an **address**, effectively read-only |
| `S13` | **Livelock** — "corresponding to deadlock" — processes running but making no progress |
| `S17` | The **B-M-P analysis method**: assume one process is inside (ME); assume nobody is inside and see whether an entry section can block others (progress) |
| `S20`/`S21` | Peterson's algorithm was developed by **Leslie Lamport**; the textbook proof is "for your reference" |
| `S24` | Interrupts are **disabled before the first line and enabled after the last**; `*` is a C pointer dereference |
| `S28` | Semaphores appear in **every past exam paper** |
| `S31` | Non-atomic `Wait` breaks ME "same issue as with the `counter` variable in the producer-consumer problem" |
| `S32` | Blocking is used because busy waiting is "**not feasible on a single processor system**" |
| `S33` | The running process's **PCB sits at the head of the ready queue**; `wakeup`'s choice from `L` is a **policy**, "just like process scheduling" |
| `S35` | "Some possibility to allow **limited context switches** inside `Wait()`/`Signal()` — more details in the **tutorial**" |
| `S38` | Shared variables are **logical** (`counter`), shared resources are **physical** (printers); `value > 0` = instances, otherwise waiters |
| `S40` | Deadlock for two processes = "A waits for B and B waits for A" |
| `S41` | The cure for starvation is **aging** |
| `S48` | Chopstick `i` is the philosopher's **left**, `(i+1) % 5` his **right**; a philosopher cannot take another's chopstick |
| `S50` | The remedies guarantee "even when all five are hungry, **at least one can eat**" |
| `S51` | The reason for reader preference is **throughput** |
| `S54` | "You can consider it as a **Java class**" |

---

## 7. Memory hooks that actually help

* **`turn` = a baton, `flag` = a raised hand.** Alg 1 gives you a baton but nobody raises a hand; Alg 2
  raises hands but has no baton; Alg 3 has both.
* **Last writer of `turn` loses.** In Peterson the process that sets `turn = k` *last* is the one that
  waits.
* **`TestAndSet` = "take a ticket, no queue".** It hands out exactly one lock at a time and remembers
  nothing about who is waiting.
* **Negative value = a queue length.** `-2` → two people in the queue.
* **`Wait` test is `<`, `Signal` test is `<=`.** The decrement goes *below* zero; the increment only
  reaches zero.
* **"Decrement first, then block"** — pay *before* you sleep, otherwise someone else pays with your
  money.
* **Resource semaphore outside, mutex inside.** Get your slot before you take the key.
* **Empty → full is the producer's direction**; `empty` starts at `n`, `full` at `0`.
* **`Signal` = "there is one more of X"** — it never asks permission, so it never blocks.
* **Philosophers: all five must be holding one chopstick** for the deadlock. Four hungry, five
  chopsticks ⇒ someone eats.
* **Readers: first in takes `wrt`, last out gives it back.** `1` and `0`, not `>=1` and `<=1`.
* **Deadlock vs starvation:** deadlock = nobody progresses; starvation = everybody but you progresses.

---

## 8. Quick self-check before the exam

- [ ] Can you expand `counter++` into three instructions and give the `counter = 5` interleaving that
      ends at 4?
- [ ] Can you state ME, progress and bounded waiting in one sentence each, without reusing each
      other's words?
- [ ] Can you write Alg 1, Alg 2 and Peterson from memory, and say which property each fails?
- [ ] Can you explain why the **last** writer of `turn` is the one that waits?
- [ ] Can you write `TestAndSet` and prove mutual exclusion in two sentences?
- [ ] Can you reproduce the `S27` quantum-by-quantum trace and name the property that fails?
- [ ] Can you write both semaphore implementations (`while (S<=0);` and `value/L/block/wakeup`) and say
      when each is preferable?
- [ ] Can you explain, with a trace, why `Wait`/`Signal` must be atomic even when blocking?
- [ ] Can you explain why `S.value--` must precede `block()`?
- [ ] Given `S.value = -3`, can you say how many processes are waiting and what the next `Signal`
      does?
- [ ] Can you write the bounded-buffer solution and show the deadlock from swapping the `Wait`s?
- [ ] Can you explain why `counter` is not needed and why `mutex` is not needed for a single pair?
- [ ] Can you write the dining-philosophers solution, its deadlock, and three remedies with the
      condition each breaks?
- [ ] Can you write the readers-writers reader and writer and trace three readers and a writer?
- [ ] Can you name the difference between deadlock, starvation and livelock in one line each?
