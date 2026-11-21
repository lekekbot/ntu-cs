# SC2005 — Process Synchronization: Study Guide

Companion to `Part4 (Synchronization).pptx` — **54 slides, no recording**, so every citation in this
document is a slide number: **`S17`** means slide 17. Where the deck's speaker notes add something
the bullet text does not, the note is quoted.

Verbatim deck text: [transcripts/01-synchronization-slides.md](transcripts/01-synchronization-slides.md)

This deck is lecture **L5–6** in the course overview (`S01`) and the largest in the course. The deck
itself calls it *"Important but difficult"* (`S02`), and the speaker notes add that semaphores appear
*"in every past exam paper"* (`S28`). Two weeks, one chapter, one family of questions: **can you read
a piece of concurrent code and say exactly what can go wrong?**

---

## 0. The chapter in one picture

`c2` gave you processes that run concurrently; `c3` gave you a scheduler that may preempt any of them
at any instruction. Put the two together and every read-modify-write on shared data becomes a
potential disaster. This chapter builds the machinery that makes concurrent access safe.

```
                    the situation
   two or more processes, one shared variable, a preemptive scheduler
                                |
        (S03 - S09)   data inconsistency / race condition
                      "the value depends on when the context switch happens"
                                |
        one sentence that defines the whole chapter:
        "when one process is in the code that touches the shared data,
         no other process may be in that code"
                                |
        (S10 - S13)   the critical-section problem
                      the three required properties: ME, Progress, Bounded Waiting
                                |
   +-----------------+------------------+-------------------+-----------------+
   |                 |                  |                   |                 |
 (S15-S21)       (S24-S27)          (S28-S36)            (S38-S41)        (S54)
 user-level      atomic hardware    semaphores           how to *use*     monitors
 software        TestAndSet         Wait / Signal        them badly       (not examinable)
 Alg 1, 2, 3     ME + Progress      busy-wait  (S30-31)  deadlock
 ME only         BW fails (S27)     blocking   (S32-36)  starvation
   |                 |                  |
   +-----------------+------------------+
                     |
        (S42 - S53)  how to use them well:
                     bounded buffer, dining philosophers, readers-writers
```

Everything in the deck follows from one chain:

```
shared data + preemption  =>  a race condition is possible          (S03-S09)
race condition            =>  we need a protocol around the shared data  (S10)
protocol                  =>  three properties to satisfy            (S12-S13)
software protocols        =>  correct but unbelievably hard to write (S15-S21)
hardware instruction      =>  ME + Progress for free, no fairness   (S24-S27)
semaphore                 =>  same guarantee, usable by n processes (S28-S39)
misuse                    =>  deadlock and starvation               (S40-S41)
three classical problems  =>  the patterns you are examined on      (S42-S53)
```

---

## 1. Background: why any of this exists (S03)

Two claims on `S03`:

> Access to shared data from concurrent processes may result in **data inconsistency**.
> **Inconsistent data**: the data value depends on the order of instruction executions from
> concurrent processes — that is, it depends on **when context switches occur**.

So the source of all evil is not "two processes" — it is **two processes plus a context switch in the
wrong place**. The speaker note is explicit about the method:

> We should consider context switches in **any** place of process execution in order to consider all
> the possible interleaving orders.

And the fix:

> Maintaining data consistency requires mechanisms to ensure the **orderly execution** of concurrent
> processes — **causal ordering (sequencing) of reads and writes** to the shared data.

Three vocabulary points that examiners use interchangeably, so know all three:

| Phrase | Meaning |
|---|---|
| **Concurrent / cooperating processes** | processes that share data (`S04`: producer and consumer share a buffer) |
| **Data inconsistency** | the final value is not any of the values a sequential execution would produce |
| **Race condition** | the bug: *"the actual value depends on the order of process executions"* (`S08`, `S09`) |

> **Exam framing.** "Explain why a race condition can occur" is answered with three ingredients, not
> one: (1) **shared, mutable** data; (2) each access is compiled into **several** machine
> instructions; (3) the scheduler can **preempt between any two of them**. Remove any of the three
> and the race disappears.

---

## 2. The running example: bounded buffer (S04–S09)

### 2.1 The set-up (S04–S05)

Two processes run concurrently. The **producer** puts items into a shared circular buffer, the
**consumer** takes them out.

| Variable | Declared in | Role (`S04` note) |
|---|---|---|
| `item buffer[BUFFER_SIZE]` | shared | the shared buffer itself, `BUFFER_SIZE` = 10 |
| `int counter = 0` | shared | **number of items currently in the buffer** |
| `int in = 0` | producer | "the next-to-fill empty slot" |
| `int out = 0` | consumer | "the next-to-process item" |

```c
#define BUFFER_SIZE 10
typedef struct {. . .} item;
int in = 0;    // the next-to-fill empty slot (producer variable)
int out = 0;   // the next-to-process item   (consumer variable)

/* Shared data */
item buffer[BUFFER_SIZE];
int counter = 0;   // Number of items in buffer
```

`S07` asks the question and answers it in the note: **which variables are really shared?**

* `counter` — shared, and **written by both**. This is the dangerous one.
* `buffer` — shared as an *address*, but each process only touches its own slot, and the note calls
  it "read-only" in the sense that neither process rewrites the array wholesale. `in` and `out` are
  private to one process each, so they never race.

This distinction — *shared and written by more than one process* vs merely shared — is exactly the
`S38` split between "shared variables" and "shared resources".

### 2.2 The two loops (S06–S07)

```c
/* Producer process */
item nextProduced;
while (1) {
    while (counter == BUFFER_SIZE);   // wait for space
    buffer[in] = nextProduced;        // produce item
    in = (in + 1) % BUFFER_SIZE;      // prepare for next item
    counter++;
}

/* Consumer process */
item nextConsumed;
while (1) {
    while (counter == 0);             // wait for buffer to receive an item
    nextConsumed = buffer[out];       // consume the item
    out = (out + 1) % BUFFER_SIZE;    // prepare for next item
    counter--;
}
```

Two things the speaker notes insist on:

* **"pay attention to the semicolon"** (`S06`) — `while (counter == BUFFER_SIZE);` is an *empty*
  loop. That single `;` is the entire wait. (And exactly the construction that `TestAndSet`-style
  busy waiting reuses later.)
* **`(in + 1) % BUFFER_SIZE`** makes the buffer **circular**: when `in` reaches the end it wraps to
  zero.

Note the shape: `counter` is *both* the loop guard (`== 0`, `== BUFFER_SIZE`) *and* the variable
being updated. That is why the whole example collapses once two processes touch it.

### 2.3 `counter++` is not one instruction (S08–S09)

`S08` isolates the two statements:

```
Producer:  counter++;
Consumer:  counter--;
```

> They may create inconsistent value for variable `counter` due to **race condition**. The actual
> value depends on **when the producer or consumer process context switches**.

`S09` gives the compiler's expansion — the model every exam answer should use:

```
counter++  is implemented as:        counter--  is implemented as:
    register1 = counter                  register2 = counter
    register1 = register1 + 1            register2 = register2 - 1
    counter   = register1                counter   = register2
```

Now the interleaving on the slide, with `counter = 5` and **one** produce and **one** consume:

| Step | Who | Instruction | `register1` | `register2` | `counter` |
|---|---|---|---|---|---|
| 1 | P (producer) | `register1 = counter` | 5 | – | 5 |
| 2 | P | `register1 = register1 + 1` | 6 | – | 5 |
| 3 | — | **context switch P → C** | 6 | – | 5 |
| 4 | C (consumer) | `register2 = counter` | 6 | **5** | 5 |
| 5 | C | `register2 = register2 - 1` | 6 | 4 | 5 |
| 6 | — | **context switch C → P** | 6 | 4 | 5 |
| 7 | P | `counter = register1` | 6 | 4 | **6** |
| 8 | — | **context switch P → C** | 6 | 4 | 6 |
| 9 | C | `counter = register2` | 6 | 4 | **4** |

> **Counter value is 4 instead of 5!** (`S09`)

Why that is wrong: one item was produced (5 → 6) and one consumed (6 → 5), so the buffer must still
hold **5** items. The value 4 means **one item has vanished** — the consumer's decrement was applied
to a stale snapshot (`5`) and it overwrote the producer's increment.

The mirror-image interleaving (consumer reads 5, producer writes 6 last) gives `counter = 6`: an item
appears out of nowhere. Both are wrong; the correct value depends on **serialising** the two
read-modify-write sequences.

### 2.4 The three things this example is used to prove

1. **Sequential reasoning is not enough.** Each statement is correct on its own; the *composition* is
   wrong.
2. **The bug is invisible in testing.** It needs a context switch at one precise instruction, so it
   will not reproduce on demand.
3. **`counter` being `int` is not the issue.** Even an atomic value type is non-atomic when read,
   modified and written.

> **Trap.** "The final value is always 4." No — it is `5` (no problem), `6` (lost decrement) or `4`
> (lost increment) depending on the interleaving. `S09` shows only the `4` case.

> **Trap.** Do not say `counter++` "is atomic because it is one C statement". Statements are not
> instructions. Three machine instructions, three preemption points.

---

## 3. The critical-section problem (S10–S14)

### 3.1 Definition (S10)

> `n` processes all competing to use some shared data. Each process has a code segment, called
> **critical section**, in which the shared data is accessed. […] **At least one process modifies
> (writes to)** the shared data.
>
> **Problem:** design a protocol to ensure that when one process is executing in its critical
> section, no other process is allowed to execute in its critical section.

The examples the slide gives for "accessing shared data": changing shared variables, updating a
shared table, writing a shared file. Note the explicit qualifier **at least one writes** — pure
readers cannot destroy consistency (this is exactly why readers-writers on `S51` allows several
readers at once).

The speaker note states the goal in the strongest form: *"at any time, there is at most one process
in the critical section."*

Also from the note: in the previous example, **`counter++` and `counter--` are the critical
sections**. They are two lines of code, not two "blocks".

### 3.2 The generic structure (S11)

```c
while (1) {
    entry section        // ask permission to enter critical section
        critical section // access the shared data
    exit section         // leave, and notify other processes
        remainder section// non-critical work
}
```

| Section | Its job (`S11`) | Typical content in later slides |
|---|---|---|
| **entry** | "ask permission to enter critical section" | `while (turn != i);` · `flag[i] = true; while (flag[k]);` · `while (TestAndSet(&lock));` · `Wait(mutex);` |
| **critical** | the shared-data access | `counter++`, `buffer[in] = nextProduced`, `x = x + 1` |
| **exit** | "exit critical section (notify other processes)" | `turn = k;` · `flag[i] = false;` · `lock = false;` · `Signal(mutex);` |
| **remainder** | everything else | `i++;` … |

The `while (1)` is not decoration. The note says why:

> The loop is to allow you to explore **all possible orders of executions** (different places to
> perform context switches). Our implementation of the entry/exit section should be **correct for
> all the possible orders**.

That is the analysis method of the whole chapter: **enumerate interleavings**, and a solution is
correct only if every interleaving is safe.

### 3.3 The assumptions (S12)

Stated before the properties, and examinable because questions often hinge on them:

| Assumption | Wording on `S12` |
|---|---|
| Progress *within* the sections | "Each process is guaranteed to make progress over time in these sections" — a process does not get stuck forever inside its critical or remainder section |
| Speed | "**No assumption** about relative execution speed of different processes in these sections (may execute at different speeds)" |

The second assumption is what forbids arguments like "P0 will finish its critical section quickly, so
P1's wait is short". You may **never** assume a process runs faster than another, or that a
particular process gets scheduled. The only timing assumption the deck ever makes is an explicit
one, e.g. "round-robin with quantum 10 ms" on `S27` or "turn is updated fairly" on `S17`.

### 3.4 The three required properties (S12–S13)

| Property | Definition (`S12`, `S13`) | What it forbids |
|---|---|---|
| **Mutual Exclusion** | "If a process is executing in its critical section, then no other process can be executing in its critical section at the same time" | two processes inside at once |
| **Progress** | "If no process is executing in its critical section and there exist processes that wish to enter their critical section, then the selection of the next process to enter the critical section **cannot be postponed indefinitely**" | an idle entry section blocking everybody |
| **Bounded Waiting** | "After a process has requested to enter its critical section and before that request is granted, other processes are allowed to enter their critical section only a **bounded number of times**" | one process being overtaken forever |

`S13` adds the reason the last two exist as a pair:

> These two properties together ensure that a process is **not stuck in the entry section forever**.

And the pass mark:

> A correct solution […] should satisfy **all three** requirements. If any of the three requirements
> is violated, the solution is **wrong**. (`S13` note)

Precise readings worth memorising, because marks are lost on sloppy wording:

* **Progress is a global condition, not a fairness condition.** It is about the *system*: if the CS
  is empty and someone wants in, *someone* must get in. It does not say *which* process.
* **Bounded waiting is the per-process fairness condition.** It says *you* will get in after at most
  a bounded number of others. This is the one `TestAndSet` fails (`S27`).
* **Progress ≠ "everybody makes progress".** A protocol where each process spins forever fails
  progress even though no process is "blocked" in the OS sense. The note names this:
  *"There is a circumstance called **live-lock** (corresponding to deadlock)…"* — spinning processes
  are not blocked, yet nothing happens.

> **Trap.** A solution can fail progress while satisfying mutual exclusion and bounded waiting. All
> three software algorithms on `S16`–`S21` do exactly that kind of partial pass; see §4.

---

## 4. User-level solutions (S15–S21)

### 4.1 The setting (S15)

> We start with only 2 processes `P0` and `P1`. Although `P0` and `P1` have the same generic
> structure, they may have **different implementations for the four sections**.
> We look at **user-level software approaches w/o OS support**.

So: pure shared variables, no special instruction, no syscall. And two reasons the lecturer gives for
studying them at all (`S15` note):

1. *"We learn how to **analyse** whether a solution can satisfy the three requirements."*
2. *"Here, we want to use these examples to show you: these software approaches are **difficult to
   write**, even for two processes. Thus, it is necessary for OS to provide support."*

> **Exam framing.** The deck's own conclusion about Algorithms 1–3 is *"you are not required to
> remember"* the code (`S21` note). What **is** required is the property analysis. Learn the three
> algorithms by their **failure**, not by their syntax:
> Alg 1 fails **progress** (a process that is not interested blocks the other); Alg 2 fails
> **progress** (both politely wait forever); Alg 3 is correct.

Throughout, `k` denotes *the other* process: `k = 1 - i`.

### 4.2 Algorithm 1 — a single `turn` variable (S16–S17)

```c
int turn;              // shared; initially turn = 0

/* Process Pi */
while (1) {
    while (turn != i);     // entry:  turn = i  =>  Pi can enter critical section
        critical section
    turn = k;              // exit:   hand the turn to the other process
        remainder section
}
```

`S16` prints this twice, once per process, with the entry/exit labelled:

```
Process P0                       Process P1
  while (turn != 0);               while (turn != 1);
      critical section                 critical section
  turn = 1;                        turn = 0;
      remainder section                remainder section
```

**Property analysis (`S17`)**

| Property | Verdict | The argument on the slide |
|---|---|---|
| **Mutual Exclusion** | ✓ | "Suppose `turn = 0` and P0 enters critical section. `turn` is only updated in exit section, when P0 exits critical section. Process P1 therefore cannot enter its critical section." |
| **Progress** | ✗ | "`turn = 0` and P0 is in a long remainder section (think `while(1)` loop or **blocked I/O**), and P1 wants to enter critical section" |
| **Bounded Waiting** | ✓ | "Assuming `turn` is updated in a **fair** (e.g., round-robin) manner among the two concurrent processes" |

Read the failure carefully, because it is the archetype of a progress violation: **the entry section
is a function of another process's private business.** P1 asks "may I enter?" and the answer depends
on whether P0 feels like entering. If P0 is not interested at all, P1 is stuck — `turn` will not
change, because only the *exit* section writes it, and P0 never even reaches its exit section.

The fix that Alg 1 cannot express: P1 must be able to tell *"P0 does not want in"* from *"it is not
P0's turn"*. That needs one bit **per process**, i.e. a flag.

### 4.3 Algorithm 2 — one `flag` per process (S18–S19)

```c
boolean flag[2];       // shared; initially flag[0] = flag[1] = false

/* Process Pi */
while (1) {
    flag[i] = true;        // entry:  flag[i] = true  =>  Pi ready to enter its critical section
    while (flag[k]);       //         wait until the other process is not ready
        critical section
    flag[i] = false;       // exit
        remainder section
}
```

`S18` states the motivation in one line:

> Algorithm 1 had an issue that it **did not know if a process wants to enter** its critical section.
> Issue solved in Algorithm 2 by using one flag for each process to express **interest**.

**The failure (S19).** Interleaving:

```
T0 : P0 sets flag[0] = true
T1 : P1 sets flag[1] = true
     Now P0 and P1 are looping forever in their respective while statements.
```

Both processes have politely announced interest, and each is now waiting for the *other* to leave.
Neither entered, so neither will ever exit, so neither flag will ever be cleared. This is exactly the
**livelock** the `S13` note named: nothing is blocked, nothing progresses.

| Property | Verdict | Argument (`S19`) |
|---|---|---|
| **Mutual Exclusion** | ✓ | "Suppose P0 enters critical section, then `flag[1] = false` and `flag[0] = true`. `flag[0]` is only updated to `false` in the exit section of P0. Process P1 therefore cannot enter its critical section." |
| **Progress** | ✗ | the `T0`/`T1` interleaving above |
| **Bounded Waiting** | ✓ | "Once P0 sets `flag[0] = true`, process P1 cannot enter its critical section" |

> **Careful with the last row.** The slide ticks bounded waiting, but the *justification it gives* is
> an argument for mutual exclusion, not for fairness. The defensible statement is: bounded waiting
> is **vacuously** satisfied here because nobody enters the critical section at all (so "others enter
> a bounded number of times" is trivially true). The real defect of Alg 2 is **progress**. In an exam,
> say "progress is violated (both spin forever); bounded waiting is not the property that fails";
> see [NOTES.md](NOTES.md#3-known-slips-typos-and-inconsistencies-in-the-slides).

**What Alg 2 still cannot do:** choose. When both want in at the same instant, both back off. Alg 2
has interest but no **tie-break**.

### 4.4 Algorithm 3 — Peterson's algorithm (S20–S21)

Variables are a combination of Algorithms 1 and 2:

```c
boolean flag[2];       // initially flag[0] = flag[1] = false   -- interest
int turn;              // initially turn = 0                    -- tie-break

/* Process Pi */
while (1) {
    flag[i] = true;                        // I am interested
    turn = k;                              // but you may go first
    while (flag[k] && turn == k);          // wait only if you are interested AND it is your turn
        critical section
    flag[i] = false;                       // exit
        remainder section
}
```

> Algorithm 2 could not **choose** between two processes that wanted to enter their critical section
> at the same time. Issue solved in Algorithm 3 by using the **`turn` variable to denote whose turn
> it is**. (`S20`)

The whole trick is in the two entry lines and their order: `flag[i] = true` (I want in) then
`turn = k` (**you** go first if you also want in). The last writer of `turn` loses the tie. Because
both processes execute the same two lines, at most one of them can end up with `turn` equal to its
own index after both have announced interest — the *later* writer overwrites the earlier one.

Also note the condition is an **`and`**, not an `or`: `while (flag[k] && turn == k)`. You wait only
if the other process is *both* interested *and* has priority. If the other is not interested
(`flag[k] == false`), you go straight in — that is the part Alg 1 was missing.

**Property analysis (`S21`)**

| Property | Verdict | Argument on the slide |
|---|---|---|
| **Mutual Exclusion** | ✓ | "If P0 enters critical section, then `flag[0] = true`. If P1 now wants to enter critical section, then it will first set `turn = 0`. P1 then cannot enter because `turn = 0` and `flag[0] = true`." |
| **Progress** | ✓ | "Suppose P0 wants to enter critical section. If P1 is in remainder section then `flag[1] = false` and P0 can enter. If P1 is in entry section, then access is granted either to P0 or P1 depending on the latest value of `turn`." |
| **Bounded Waiting** | ✓ | "Assuming `turn` is updated fairly" |

Note how the two failures are repaired one at a time:

| Algorithm | Has interest? | Has tie-break? | Fails |
|---|---|---|---|
| 1 (`turn`) | ✗ — you cannot tell "not interested" from "not your turn" | ✓ | Progress |
| 2 (`flag[]`) | ✓ | ✗ — nobody breaks the symmetry | Progress |
| 3 (`flag[]` + `turn`) | ✓ | ✓ | — |

Two side notes from `S21`:

* The speaker note credits the algorithm: *"developed by a famous Microsoft researcher named
  **Leslie Lamport**"*. (The slide's own question — *"How to extend Algorithm 3 for say three
  processes?"* — is left open; Peterson's construction does not generalise, which is why the deck
  immediately moves to hardware support.)
* The slide mentions a **proof** in the textbook and says it is *"just for your reference"*. The
  examinable part is the property table above, argued by interleaving as on `S17`, `S19`, `S21`.

> **Trap.** Do not present Alg 3's mutual exclusion argument as "`turn` is a lock". `turn` alone is
> Alg 1, which fails progress. `flag[]` alone is Alg 2, which deadlocks. Only the **combination**
> works, and the `&&` matters: `while (flag[k] || turn == k)` is wrong.

### 4.5 Why software solutions are a dead end (S15, S21, S23)

Three reasons, all stated on the slides or in the notes:

1. **They are hard to write even for two processes** (`S15` note) — three attempts, two wrong.
2. **They do not scale.** `S23`: *"Previous software approaches are difficult to implement for more
   than two processes."* Alg 3 is a two-process construction.
3. **They assume things real hardware breaks.** `flag[i] = true; turn = k;` must be visible to the
   other process in program order — i.e. they rely on memory ordering that a modern CPU or compiler
   may reorder. (Not on the slide; do not spend exam marks on it, but it is worth knowing why the
   world uses hardware instructions.)

Hence `S23`: the OS provides three kinds of support, "low level to high level":
**synchronization hardware → semaphore → monitor**.

---

## 5. What the OS provides (S22–S23)

`S22` is a section divider (identical bullet list to `S02`). `S23` is the map for the rest of the
deck:

| Level | Mechanism | Slides | Guarantee |
|---|---|---|---|
| Lowest | **Synchronization hardware** (atomic instructions, e.g. `TestAndSet`) | S24–S27 | ME + progress; **no fairness** |
| Middle | **Semaphore** (`Wait` / `Signal`) | S28–S39 | ME + progress + fairness, *if used correctly* |
| Highest | **Monitor** | S54 | ME enforced by the compiler/runtime; not examinable |

The `S23` note also contains the model revision summary of the previous week, which is a good
one-paragraph recap of §3–§4:

> We started with the critical section problem. There are **three requirements: mutual exclusion,
> progress and bounded waiting. […] We have three algorithms for solving the critical section problem
> of two processes. **Algorithms 1 and 2 have progress violations**, and **Algorithm 3 satisfies all
> three** requirements.

Note the section divider on `S22` splits the deck into exactly the six parts named on `S02`:
*Race Condition & Critical-Section → User-level Solutions → OS-level Solutions → Synchronization
Hardware → Semaphores → Classical Problems of Synchronization*. The word **"OS-level Solutions"**
on the divider is served by S23–S27 (hardware) and S28–S36 (semaphores).

---

## 6. Synchronization hardware: `TestAndSet` (S24–S27)

### 6.1 Atomicity (S24)

> Modern processors provide special **atomic** hardware instructions. **Atomic = non-interruptible
> (no context switches)**.
> `TestAndSet`: test and modify the content of a main memory word **atomically**.

And the note pins down what "atomic" buys:

> An atomic operation means the operation is executed **in order without preemption**. […] there is
> **no context switch from the first line till the last line**.

So the hardware supplies exactly the missing piece of §4: a read-modify-write that the scheduler
cannot split. No flags, no `turn`, no interleaving to enumerate — that is the whole point.

### 6.2 The instruction (S24)

```c
boolean TestAndSet (boolean *target) {
    boolean rv = *target;   // get current value
    *target = true;         // store true
    return rv;              // return old value
}
```

The slide annotates the three lines with the machine-level view:

```
   [ interrupt is disabled ]      <- OS disables context switches before the first line
        get current value
        store true
        return old value
   [ interrupt is enabled  ]      <- and re-enables them after the last
```

The return value is the **old** value, and that is the entire interface. Note the C detail the note
explains: `*target` is a pointer dereference, so callers pass `&lock`.

> **Trap.** `TestAndSet` **always sets the word to `true`** — whether it was `false` or already
> `true`. It is not a conditional store. The caller learns what happened only from the return value.

### 6.3 Using it for mutual exclusion (S25)

```c
boolean lock;          // shared; initially lock = false

/* Process Pi */
while (1) {
    while (TestAndSet(&lock));   // ACQUIRE lock
        critical section
    lock = false;                // RELEASE lock
        remainder section
}
```

Two readings of the spin line:

* `lock == false` → `TestAndSet` returns `false` and sets `lock = true`. The `while` sees `false`,
  exits immediately, and the process is now **holding** the lock. It enters.
* `lock == true` → returns `true`, sets `lock = true` (no change). The `while` repeats.

Note the symmetry with `S06`: the wait is again an empty `while (...);`. `S29` will make the point
that a semaphore hides this loop inside `Wait`.

### 6.4 Why mutual exclusion holds (S26)

> A process enters critical section → `lock = false` immediately before it executes
> `TestAndSet(&lock)` and `lock = true` thereafter. `lock` is reset to `false` **only in the exit
> section** of the process. No process can thereafter enter critical section since `lock = true`.

Formally, the argument is a **single atomic step**: the transition "observe `false` → leave it
`true`" happens indivisibly. Between two processes, the hardware orders them, so exactly one observes
`false`. Compare with the busy-waiting semaphore on `S31`, which fails *precisely because* its test
and its decrement are two separate instructions.

**Progress (`S26`)** ✓: "If `lock = false`, then the **first** process that executes
`TestAndSet(&lock)` will immediately enter critical section." Nobody is prevented from trying: the
entry section cannot be held hostage by a process in its remainder section — the exact Alg 1 defect,
now gone.

**Bounded waiting (`S26`)** ✗ — and the slide is honest about the workaround:

> See next slide. More complex solution with `TestAndSet` that satisfies bounded waiting is in the
> **textbook – not examinable**.

### 6.5 The bounded-waiting failure trace (S27)

This slide is the single most examinable trace in the chapter, because it combines `c3` scheduling
with `c5` synchronisation.

```c
Process P0                            Process P1
 1. Initialization code                1. while (1) {
 2. while (1) {                        2.    while (TestAndSet(&lock));
 3.    while (TestAndSet(&lock));      3.       critical section
 4.       critical section             4.    lock = false;
 5.    lock = false;                   5. }
 6. }
```

Timing assumptions, all given on the slide:

* P0's lines **1–3** take **10 ms** (initialisation + the whole acquire).
* P0's lines **2–6** (one full iteration after acquiring) take **10 ms**.
* Scheduling is **round-robin with quantum 10 ms**.

Trace:

| Quantum | Who runs | What executes | `lock` at end | Effect |
|---|---|---|---|---|
| 1 | P0 | lines **1, 2, 3** — initialises, `TestAndSet` returns `false`, **acquires** | `true` | P0 is now *inside* the critical section when its quantum expires |
| 2 | P1 | lines **1, 2** — `TestAndSet` returns `true`, spins for the rest of the quantum | `true` | P1 never reaches its critical section |
| 3 | P0 | lines **4, 5, 6, 2, 3** — finishes CS, releases (`lock = false`), remainder, **re-acquires** | `true` | P0 owns the lock again |
| 4 | P1 | line **2** only — `TestAndSet` returns `true` again and spins | `true` | P1 gets exactly one instruction of opportunity, and it is the wrong one |
| 5 | P0 | lines **4, 5, 6, 2, 3** | `true` | repeats forever |

`S27`'s own caption for these context-switch points:

```
P0 (1,2,3) | P1 (1,2) | P0 (4,5,6,2,3) | P1 (2) | P0 (4,5,6,2,3) | ...
```

> Whenever P0 context switches out, it holds the lock (is in critical section). […] . . .

**Why this is a *bounded waiting* failure and not a mutual exclusion failure.** At every instant at
most one process is inside, so ME holds. Progress holds too: whenever the lock is free, whoever tests
it first gets in. But P1's *request* is never granted: P0 re-acquires before P1 ever gets a quantum
that contains line 3.

**The mechanism** is that `lock` is a **single bit with no memory of who is waiting**. `TestAndSet`
implements a lock, not a **queue**. Any process that is running when the lock is free takes it, and
scheduling decides who is running — so the loser can lose forever.

> **Exam framing.** Reproduce the trace with a per-quantum table: quantum number, which process,
> which lines, what `lock` is, and the conclusion. Three quanta are enough to demonstrate the cycle;
> a fourth shows it repeating.

> **Trap.** The tempting answer "P1 is starved because P0 has higher priority" is wrong — the slide
> uses **plain round-robin**, equal quantum. Fairness in the scheduler does **not** rescue
> `TestAndSet`; the unfairness is in the lock protocol.

---

## 7. Semaphores: the abstraction (S28–S29)

### 7.1 Definition (S28)

> **Semaphore `S`**: integer shared variable.
> Only accessible by two **atomic** system calls: `Wait` and `Signal`.
>
> ```
> Wait (S):   if S > 0, S--; else, wait();
> Signal (S): S++;
> ```

`S28` gives the one-line definition first because it is the whole abstraction: **an integer, and two
atomic operations, and nothing else.** You may not read, write or test `S` directly — that is what
makes it a synchronisation primitive rather than a shared variable.

Two types:

| Type | `S28` definition | Use |
|---|---|---|
| **Counting semaphore** | "Integer value can range over an unrestricted domain" | counting **resource instances** (`empty`, `full` on `S43`) |
| **Binary semaphore** | "Integer value can never be greater than 1" | **mutual exclusion** (`mutex`, `wrt`, `chopstick[i]`) |

The lecturer's framing (`S28` note) is worth quoting because it is close to what an exam question
asks for:

> The hardware solutions are **too low level, and are complicated to use**. So, operating system
> provides a **higher level** synchronization mechanism called **semaphore**. […] not only because we
> have questions on this part in **every past exam paper**, but also because semaphore is a widely
> used process synchronization mechanism.

Also note the *semantics* the slide writes in pseudo-code — `else, wait();` — which already hints at
the two implementations: `wait()` either **spins** (`S30`) or **blocks** (`S32`).

### 7.2 The `mutex` idiom (S29)

```c
semaphore mutex;      // initially mutex = 1

/* Process Pi */
while (1) {
    Wait(mutex);          // acquire semaphore
        critical section
    Signal(mutex);        // release semaphore
        remainder section
}
```

> If `mutex = 1` and process executes `Wait(mutex)`, then it can enter critical section. (`S29`)
> […] this implementation is **simpler** than the previous solution using atomic instructions. There
> is **no while-loop**, because it is already implemented in `wait`. (`S29` note)

Compare the three entry sections line by line — this is the "why semaphores won" argument in one
table:

| Mechanism | Entry section | Exit section | What the programmer must understand |
|---|---|---|---|
| Alg 1 | `while (turn != i);` | `turn = k;` | whose turn it is |
| Alg 3 | `flag[i]=true; turn=k;` `while (flag[k] && turn==k);` | `flag[i]=false;` | interest + tie-break |
| `TestAndSet` | `while (TestAndSet(&lock));` | `lock = false;` | the atomic instruction |
| **Semaphore** | `Wait(mutex);` | `Signal(mutex);` | **only that the semaphore is held/released** |

The counting interpretation of `mutex = 1` is the key insight that unifies §7 with §12: a binary
semaphore initialised to 1 is *"one instance of a resource"* called "the right to be in the critical
section".

> **Trap.** `Wait` and `Signal` are the **only** legal operations. `if (S.value > 0) S.value--;` is
> not a semaphore operation — it is a race condition with extra steps.

---

## 8. Implementation 1: busy waiting (S30–S31)

### 8.1 The implementation (S30)

```c
Wait (S):
    while (S <= 0)
        ;        // busy wait
    S--;

Signal (S):
    S++;
```

with the assembly the slide prints alongside:

```
Assembly for Wait(S):        Assembly for Signal(S):
loop1: ldr ax, [S]                    ldr ax, [S]
       cmp ax, 0                      add ax, 1
       jle loop1                      str [S], ax
       sub ax, 1
       str [S], ax
```

Note the guard is `S <= 0` here (not the `if (S > 0)` of `S28`) — for a boolean-int semaphore these
are the same condition, written from the other side.

**The trade-off, exactly as the slide states it:**

| | `S30` |
|---|---|
| **Pros** | "**No context switch overhead** (busy waiting)" |
| **Cons** | "**Inefficient** if critical sections are long"; "Busy waiting **wastes CPU cycles**" |

The note adds the nuance that makes it a *conditional* win:

> Busy waiting has the advantage that **no context switches occur**. That is particularly good for a
> **short waiting time**. However […] busy waiting is inefficient if the critical section is **long**,
> because the while loop will consume too many CPU cycles.

So: **good when the expected wait is shorter than the cost of two context switches** (as on a
multiprocessor, or a very short critical section); bad otherwise, and *"not feasible on a single
processor system"* (`S32` note) because the spinner can be the only runnable process.

### 8.2 Why `Wait` must be atomic (S31)

This is the slide that ties the whole chapter back to §2.

> To avoid race condition, `S++` and `S--` must be atomic. `Wait(S)` must be atomic to ensure mutual
> exclusion.

The trace, with `S > 0` initially:

```
Process P0 executes while (S <= 0);  and exits the busy wait
Context switch from P0 to P1
Process P1 executes while (S <= 0);  and S--;
Context switch from P1 to P0
Process P0 executes S--;
              =>  Mutual Exclusion violated
```

As a table, starting from `S = 1`:

| Step | Who | What | `S` | Note |
|---|---|---|---|---|
| 0 | — | initial | 1 | one permit available |
| 1 | P0 | `ldr`/`cmp`: `S <= 0` is **false**, so the loop exits | 1 | P0 has *decided* it may proceed |
| 2 | — | **context switch** | 1 | P0 has not decremented yet |
| 3 | P1 | loop exits too, then `sub`/`str`: `S = 0` | 0 | P1 consumes the only permit |
| 4 | — | **context switch** | 0 | |
| 5 | P0 | resumes at `sub ax, 1; str [S], ax` → `S = -1` | −1 | P0 also "takes" a permit that does not exist |
| 6 | — | | −1 | **both P0 and P1 enter the critical section** |

The bug is one instruction wide: the **test** (`cmp`/`jle`) and the **update** (`sub`/`str`) are
separate instructions, so a context switch between them lets two processes both pass a test that only
one should have passed. This is *exactly* the `counter++` race of `S09`, just with the comparison
attached.

> **Exam framing.** "Why must `Wait` be atomic?" → because `Wait` is a **check-then-act** sequence;
> if the scheduler intervenes between the check and the act, two processes can act on the same
> observation. Give the 6-step trace, not the sentence.

> **Trap.** Making `S--` atomic is **not** enough. It is the *pair* `while (S <= 0)` + `S--` that must
> be indivisible, or two processes can both exit the loop.

---

## 9. Implementation 2: blocking (S32–S36)

### 9.1 The record (S32)

> Because the busy waiting implementation is **not feasible on a single processor system**, current
> operating systems have another implementation: **blocking**.
>
> The basic idea is that when a process enters its critical section, other processes that want to
> enter their critical section will be **blocked**. A process is blocked means it will be put into the
> **waiting** state. So the process waiting to enter the critical section **does not consume CPU
> cycles**.

```c
typedef struct {
     int value;
     struct process *L;
} semaphore;
```

| Field | Meaning |
|---|---|
| `int value` | the count: **> 0** = *number of free resource instances*; **< 0** = *number of processes blocked on `L`* (magnitude); **0** = none free, none waiting |
| `struct process *L` | head of the **list of processes blocked on this semaphore** (the note: the semaphore's own wait queue, *not* the ready queue) |

Why a pointer to a process list is needed at all: a blocked process has to be remembered somewhere,
and it is not on the ready queue any more. `L` is that place.

### 9.2 `block()` and `wakeup()` (S32–S33)

Two "simple operations" (`S32`), each of which touches **three** data structures:

**`block()`** (`S33`)

1. **Dequeue** the current process from the **ready queue**.
2. **Enqueue** the process to **list `L`**.
3. Change state of the process to **waiting**.

**`wakeup()`** (`S33`)

1. **Dequeue** a process from **list `L`**.
2. **Enqueue** the process to the **ready queue**.
3. Change state of the process to **ready**.

The note supplies two details the bullets hide:

> **Block**: first dequeue current process from ready queue (we suppose that the **PCB of the running
> process is also stored in the head of the ready queue**), and then enqueue current process to
> `L`. The process state changes from **running to waiting**.
> **Wakeup**: dequeue a process `P` from `L`. **We can have different policies here, just like
> process scheduling.** Then enqueue `P` to the ready queue. The state changes from **waiting to
> ready**.

The word "**policies**" matters: *which* process `wakeup` picks from `L` is a scheduling decision, and
that choice is where **starvation** comes from on `S41` (priority-based or LIFO dequeue).

### 9.3 `Wait` and `Signal` (S34)

```c
Wait(S):
    S.value--;
    if (S.value < 0) {
        block();
    }

Signal(S):
    S.value++;
    if (S.value <= 0) {
        wakeup(P);
    }
}
```

**Read the two comparisons character by character — they are opposite, and that is not a typo:**

| | `Wait` | `Signal` |
|---|---|---|
| update | `S.value--` **first** | `S.value++` **first** |
| test | `if (S.value < 0)` — strict | `if (S.value <= 0)` — non-strict |
| action | `block()` | `wakeup(P)` |
| why | after decrementing, a negative value means "I decremented below zero" ⇒ there is no permit for me ⇒ block | after incrementing, `<= 0` means "there was at least one waiter before my increment" ⇒ someone can proceed |

The `S34` note derives the `<=` explicitly — this is a favourite exam question:

> Why we need to check `if (s.value <= 0)` and not `if (s.value < 0)`? Consider `s.value = -1` (only
> one process waiting in list `L`) before executing `signal`. After `S.value++`, what is the value?
> `S.value = 0`. That is why we need to consider `s.value == 0` as well for waking up processes.

### 9.4 The state machine — and the negative-value question

The slide's own question:

> **If `S.value = -2`, how many processes are waiting in list `L`?** → **2**

That is the whole meaning of a negative value. Build the table of all transitions, because every
question in this area can be answered from it:

| `S.value` before | Operation | `S.value` after | Effect |
|---|---|---|---|
| 1 | `Wait` | 0 | caller proceeds; permit consumed |
| 0 | `Wait` | −1 | caller **blocks**; 1 waiter |
| −2 | `Wait` | −3 | caller **blocks**; 3 waiters |
| 1 | `Signal` | 2 | **nobody woken** (`2 > 0`) |
| 0 | `Signal` | 1 | **nobody woken** (`1 > 0`) |
| −1 | `Signal` | 0 | **one woken** (`0 <= 0`) |
| −2 | `Signal` | −1 | **one woken** |

Three invariants to carry into the exam:

```
S.value >= 0   =>  S.value = number of available resource instances  (0 = none, but nobody waiting)
S.value <  0   =>  |S.value| = number of processes blocked in L
S.value == 0   =>  no permits left, and no one is waiting
```

**Full worked trace.** `mutex` initialised to 1; P0, P1, P2 all call `Wait` before anyone calls
`Signal`:

| Step | Action | `value` | `L` | Who is where |
|---|---|---|---|---|
| 0 | init | 1 | `[]` | all ready |
| 1 | P0 `Wait` → `0`, `0 < 0` false | 0 | `[]` | **P0 inside CS** |
| 2 | P1 `Wait` → `-1`, blocks | −1 | `[P1]` | P1 waiting |
| 3 | P2 `Wait` → `-2`, blocks | −2 | `[P1,P2]` | P2 waiting |
| 4 | P0 `Signal` → `-1`, `-1 <= 0` ⇒ wakeup | −1 | `[P2]` | P1 becomes ready |
| 5 | P1 `Wait`? (no — P1 resumes after `Wait`) | −1 | `[P2]` | **P1 inside CS** |
| 6 | P1 `Signal` → `0`, `0 <= 0` ⇒ wakeup | 0 | `[]` | P2 becomes ready |
| 7 | P2 resumes; `Wait` already returned | 0 | `[]` | **P2 inside CS** |
| 8 | P2 `Signal` → `1`, `1 > 0` ⇒ no wakeup | 1 | `[]` | back to start |

Note step 8: the semaphore returns to 1 with **no** wakeup, because `L` is empty. Signal does not
"transfer" a permit to a process — it *increments* and *optionally* wakes someone.

> **Trap.** `S.value = 0` does **not** mean "one process is waiting". Zero means the last permit was
> taken but the taker is not blocked. Waiting processes show up as **negative** values only.

### 9.5 Even the blocking version needs atomic `Wait`/`Signal` (S35)

> **Both `Wait()` and `Signal()` must be executed atomically** (at least all updates and checks for
> semaphore `S`), even if the blocking semaphore implementation is used. […] It can also lead to
> violation of mutual exclusion because of the update to `S` (same issue as with the `counter`
> variable in the producer-consumer problem). (`S35` note)

The slide gives two traces. **Trace A — `Wait` without atomicity, progress violated:**

```
Initially, S.value = 1
Process P0 executes S.value--;
Context switch from P0 to P1
Process P1 executes S.value--;  and blocks since S.value = -1
Context switch from P1 to P0
Process P0 also blocks
                     =>  Progress for P0 and P1 violated
```

| Step | Who | `value` | Consequence |
|---|---|---|---|
| 0 | — | 1 | one permit |
| 1 | P0 | 0 | P0 has taken the permit but has not yet tested |
| 2 | — | 0 | **context switch** |
| 3 | P1 | −1 | P1 sees `-1 < 0` and **blocks** |
| 4 | — | −1 | **context switch** |
| 5 | P0 | −2 | P0 resumes, tests its own decremented value `-1 < 0`, and **blocks** |

End state: `value = -2`, **both** processes blocked, **nobody** in the critical section, and the
critical section is unreachable. The permit that P0 legitimately took has been "lost" because P0's
test was based on the *shared* value that P1 had already modified. This is a **progress** violation:
the CS is empty and a process wishes to enter, yet entry is postponed forever.

**Trace B — `Signal` without atomicity, progress for a third process violated:**

```
Initially, S.value = -1  (P2 blocked for S)
Process P0 executes S.value++;
Context switch from P0 to P1
Process P1 executes S.value++; and exits. No wakeup(P); since S.value = 1
Context switch from P1 to P0
Process P0 also exits without wakeup(P);
                     =>  Progress for P2 violated
```

| Step | Who | `value` | Consequence |
|---|---|---|---|
| 0 | — | −1 | P2 waiting; one "debt" to pay |
| 1 | P0 | 0 | should have triggered a wakeup, but P0 is suspended before testing |
| 2 | — | 0 | **context switch** |
| 3 | P1 | 1 | `1 <= 0` is false ⇒ **no wakeup** |
| 4 | — | 1 | **context switch** |
| 5 | P0 | 1 | P0 tests `1 <= 0` ⇒ false ⇒ **no wakeup** |

Two `Signal`s happened, `value` went from `-1` to `+1`, and **P2 is still blocked** — a stolen
wakeup plus a stolen permit. The lesson: it is not the *increment* alone that needs protecting, it is
the increment **together with the test that decides whether to wake someone**. Both traces are
instances of one rule:

```
the update of S.value and the check that follows it must be one indivisible step
```

The note also contains an exam-relevant aside:

> There is some **possibility to allow limited context switches inside `Wait()` and `Signal()`**.
> More details about this are in the tutorial.

i.e. atomicity *at the level of the value update + test* is what is required; not necessarily
"interrupts off for the whole call". If a question asks whether a context switch is allowed between
`block()` and the return from `Wait`, the answer is yes — after `block()` the process is in the
waiting state, and *"the process that is currently holding the semaphore"* can run.

### 9.6 Why `S.value--` must come *before* `block()` (S36)

The slide poses the tempting rewrite and demolishes it:

```c
Wait(S):                                 Signal(S):
    if (S.value <= 0) {                      S.value++;
        block();                             if (S.value <= 1) {
    }                                            wakeup(P);
    S.value--;                               }
```

> **Problems:** This would require a **context switch between `block()` and `S.value--`** if the
> process blocks. If this context switch is allowed, **mutual exclusion will be violated**.

The counter-example (`S36`), starting from `S.value = 0`:

| Step | Who | Action | `value` | Consequence |
|---|---|---|---|---|
| 0 | — | initial | 0 | permit taken by someone else |
| 1 | P0 | `Wait`: `0 <= 0` ⇒ `block()` | 0 | P0 moves to **waiting**, still *before* its `S.value--` |
| 2 | P1 | `Signal`: `1`, and `1 <= 1` ⇒ `wakeup(P0)` | 1 | P0 becomes **ready** — it will resume *after* `block()` |
| 3 | P2 | `Wait`: `1 <= 0` false ⇒ `S.value--` | 0 | **P2 enters the critical section** |
| 4 | P0 | resumes from `block()` at its `S.value--` | −1 | **P0 also enters the critical section** |

Two processes inside the critical section: **mutual exclusion violated**, and the semaphore count is
negative despite nobody being queued.

The reason is structural. With `S.value--` **first**, the count is decremented *before* the process
can possibly be suspended, so the permit accounting is always consistent: a process that blocks has
already paid for the permit it did not get. With `S.value--` **last**, the process blocks *first* and
pays *later* — and "later" can be after another process has legitimately taken the permit and after
`wakeup` has made the first process runnable again. The note puts it plainly:

> If we allow context switch between `block()` and `S.value--` inside `Wait()`, this can lead to
> violation of mutual exclusion.

### 9.7 Busy waiting vs blocking — the comparison

| | **Busy waiting** (`S30`–`S31`) | **Blocking** (`S32`–`S36`) |
|---|---|---|
| State while waiting | stays **running/ready** and spins | **waiting** (`block()`) |
| CPU cost | wastes cycles while spinning | none while blocked |
| Wake-up cost | none — the spinner notices | **two context switches** (`block` out, `wakeup` in) |
| Good when | wait is **short**; multiple CPUs | wait may be **long** |
| Bad when | critical sections are long; **uniprocessor** | wait is trivially short (overhead dominates) |
| Needs | atomic test-and-decrement | atomic update + test, **plus** a queue `L` |
| Fairness | none unless coded | provided by the `L` dequeue policy (`S41`) |
| Data structure | one integer | `struct { int value; struct process *L; }` |

---

## 10. Using semaphores properly (S37–S39)

`S37` is the section divider. The next two slides are the **method** you are expected to apply to any
problem on the exam.

### 10.1 The three steps (S38)

> **Step 1**: Understand the application scenario and identify the following: **shared
> variables/data**, **shared resources**.
> **Step 2**: Protect the **shared variables** — identify the critical section, use a **binary**
> semaphore, and add entry section (`Wait`) and exit section (`Signal`).
> **Step 3**: Protect the **shared resources** — identify each kind of resource, **one semaphore per
> kind**, initial value = **number of resource instances**; `Wait` when requested/consumed, `Signal`
> when released.

The single most useful distinction in the chapter, spelled out in the note:

> **Shared variables are logical: `counter` in producer/consumer. Shared resources are physical:
> number of printers.**

| | Shared variable / data | Shared resource |
|---|---|---|
| Examples | `counter`, `readcount`, `in`, `out` | buffer slots, chopsticks, database, printers |
| Semaphore type | **binary**, initial **1** (`mutex`) | **counting**, initial **n** (`empty = n`, `full = 0`, `chopstick[i] = 1`) |
| Semaphore name on the slides | `mutex` | `empty`, `full`, `chopstick[]` |
| What it protects | the **code** that updates the variable | the **quantity** of the thing |
| Number of semaphores | one per critical section | one per **kind** of resource |

And the diagnostic that tells you whether your semaphores are doing anything:

> **If you remove all the Wait/Signal, the logic of the code is still correct in sequential
> executions. However, it is not correct in concurrent executions.** (`S38` note)

That is a genuinely useful self-check: a semaphore never changes *what* the program computes, only
*when* the processes are allowed to compute it.

The note also restates §9.4's meaning of the value:

> The semaphore value represents the **number of instances for that kind of resource** (`> 0`).
> Otherwise, represents the **number of processes waiting** in the waiting queue (list `L`).

### 10.2 Semaphores as a general ordering tool (S39)

This is the slide that says semaphores are **not only for mutual exclusion**.

> We wish to execute code segment **B** in process `Pk` **only after** code segment **A** in process
> `Pi`. Use a semaphore `flag` initialised to **0**.
>
> ```
>         Pi                          Pk
>         A
>         Signal(flag)                Wait(flag)
>                                     B
> ```

Three things to notice:

1. The semaphore is initialised to **0** — not 1. A zero semaphore means "the event has not happened
   yet", so `Pk` blocks until it does. This is a **notification**, not a lock.
2. The `Wait` and `Signal` are in **different processes**, and there is no critical section at all.
   `Signal` *happens-before* `Wait` in the intended order; the semaphore encodes **causal ordering**
   (`S03`'s "causal ordering (sequencing) of reads and writes").
3. The pattern generalises to a chain: `A; Signal(s1);` → `Wait(s1); B; Signal(s2);` → `Wait(s2); C;`
   gives `A → B → C`.

`S39`'s speaker note is a revision summary of the whole lecture so far, and reads like a marking
scheme:

> We start with talking about **atomic operations**. There is no context switch from the first line to
> the last line. We give one example of showing how to implement process synchronization with atomic
> operation **`TestAndSet`**. **Semaphore** is implemented as a shared integer variable. It supports
> two atomic operations: `Wait` and `Signal`. With the semaphore, it is easy to implement the process
> synchronization among **multiple** processes. Then we have talked about **two implementations** of
> semaphores in operating systems: **busy waiting** and **blocking**.

| Pattern | Initial value | Where `Wait`/`Signal` live | Purpose |
|---|---|---|---|
| **Mutual exclusion** | 1 | same process, around the CS | at most one inside |
| **Ordering / notification** | 0 | **different** processes | B runs after A |
| **Resource counting** | number of instances | any process | at most `n` concurrent users |

> **Trap.** A semaphore initialised to **0** used as a mutex deadlocks immediately — the first
> `Wait` blocks forever. Always state the initial value and *why*.

---

## 11. Incorrect use: deadlock and starvation (S40–S41)

These two slides are the **only** treatment of deadlock and starvation in this deck, and they are
presented purely as **semaphore misuse**. The full chapter (four necessary conditions, prevention,
avoidance, Banker's algorithm, detection, recovery) is [`../c7`](../c7); do not expand it here, but do
know these two definitions and the difference between them.

### 11.1 Deadlock (S40)

> **Deadlock**: two or more processes are waiting indefinitely for an event that can be caused by
> **only one of the waiting processes**.

The note makes it concrete: *"for two processes A and B, a deadlock occurs if A waits for B and B
waits for A. None of them can make any progress."*

```c
semaphore S = 1, Q = 1;

P0                          P1
Wait(S);                    Wait(Q);
Wait(Q);                    Wait(S);
    ...                         ...
Signal(S);                  Signal(Q);
Signal(Q);                  Signal(S);
```

Each process acquires **in the opposite order**. The interleaving on the slide:

```
P0 executes Wait(S);
Context switch from P0 to P1
P1 executes Wait(Q);  and Wait(S);   <- blocks on S
Context switch from P1 to P0
P0 executes Wait(Q);                 <- blocks on Q
```

| Step | Who | Action | `S` | `Q` | State |
|---|---|---|---|---|---|
| 0 | — | initial | 1 | 1 | |
| 1 | P0 | `Wait(S)` succeeds | 0 | 1 | P0 holds S |
| 2 | — | context switch | 0 | 1 | |
| 3 | P1 | `Wait(Q)` succeeds | 0 | 0 | P1 holds Q |
| 4 | P1 | `Wait(S)` **blocks** | 0 | 0 | P1 waits for S (held by P0) |
| 5 | — | context switch | 0 | 0 | |
| 6 | P0 | `Wait(Q)` **blocks** | 0 | 0 | P0 waits for Q (held by P1) |

Circular wait: **P0 holds `S` and wants `Q`; P1 holds `Q` and wants `S`.** Neither can reach a
`Signal`, because both `Signal`s are *after* the second `Wait`. Deadlock is permanent — the slide's
definition gives the reason: the event that would release each one can only be caused by the other.

> **Exam framing.** "Show that this program can deadlock" → draw the hold-and-wait table above and
> name the cycle. "How would you fix it?" → impose a **global order** on acquisition (everyone takes
> `S` before `Q`), which is the same circular-wait-breaking remedy as the dining-philosophers fix on
> `S50`.

### 11.2 Starvation (S41)

> **Starvation**: **indefinite postponement** (no progress).
> A process may never have a chance to be removed from the semaphore queue (list `L`) due to **queue
> discipline**.
>
> Examples of queue disciplines that can cause starvation:
> * **Priority-based**: a low-priority process may starve if higher-priority processes keep joining
>   the queue
> * **Last-In-First-Out** policy

Note the mechanism: the process is not deadlocked — from the semaphore's point of view it is an
ordinary waiter, and the system as a whole is making progress. Only *that one* process never gets
picked, because `wakeup()` always chooses someone else from `L`.

The note gives the remedy in one word: **aging** (raise a long-waiting process's priority over time,
i.e. `c3`'s starvation fix).

### 11.3 Deadlock vs starvation vs livelock

| | Deadlock (`S40`) | Starvation (`S41`) | Livelock (`S13` note) |
|---|---|---|---|
| Who is stuck | a **cycle** of processes | one (or a few) **unlucky** process | processes are **running** but achieving nothing |
| Is the system making progress? | no | **yes** (others proceed) | no |
| Cause here | wrong **acquisition order** | wrong **queue discipline** | wrong protocol (`flag[]` both true) |
| Can it ever resolve by itself? | no | no (needs bounded waiting) | no |
| Fix | global resource ordering | **aging**, FIFO queue | a tie-break (`turn`) |

---

## 12. The three classical problems (S42–S53)

`S42` names them and states the learning objective precisely:

> **Bounded-Buffer (Producer-Consumer) Problem**, **Dining-Philosophers Problem**, **Readers and
> Writers Problem**. […] After learning those examples, we should learn **two** things: firstly we
> should know how to **write** a process synchronization with semaphore; secondly, we should be able
> to **analyse the correctness** of the program with semaphore.

So every problem below gets the same three-part treatment: **what is shared → the semaphores and
their initial values → why it is correct (and what breaks it)**.

### 12.1 Bounded buffer, generalised (S43–S46)

#### The change from S04–S09

The §2 version had **one** producer and **one** consumer. `S43` escalates to **multiple** producers
and **multiple** consumers, which changes what is shared:

> We used `counter`, `in` and `out` variables for a producer-consumer pair. **`in`/`out` are also
> shared variables now** (`in` – producers, `out` – consumers).

| Item | Classification (`S43`) |
|---|---|
| `item buffer[n]` | **shared data structure** |
| the **slots** in the buffer | **shared resources** (there are exactly `n` of them) |
| `in` (multiple producers) | shared **variable** |
| `out` (multiple consumers) | shared **variable** |
| `counter` | **not used** — see below |

#### The three semaphores

```c
semaphore full, empty, mutex;
full = 0;  empty = n;  mutex = 1;
```

| Semaphore | Type | Initial | Counts | `Wait` on it means | `Signal` on it means |
|---|---|---|---|---|---|
| `empty` | **counting** | `n` | free slots | "consume one empty slot" (producer) | "a slot became free" (consumer) |
| `full` | **counting** | `0` | filled slots / items | "consume one full slot" (consumer) | "an item is available" (producer) |
| `mutex` | **binary** | `1` | the buffer's integrity | enter the buffer-update critical section | leave it |

`S43`'s annotations say exactly this:

> `full` — *counting semaphore for consumers to identify full buffer to consume*;
> `mutex` — *binary semaphore for mutual exclusion to update buffer*;
> `empty` — *counting semaphore for producers to identify empty buffer to fill*.
> *`in` replaced with `empty`, `out` replaced with `full`, `counter` not used (why?)*

**Why `counter` disappears.** `full` **is** the counter: the number of items in the buffer. And
`empty` is `n − full`. Keeping `counter` as well would mean a *third* shared variable that must be
protected and kept consistent with the other two, for zero information gain. The information that
`counter` used to provide (`counter == 0` / `counter == n`) is now provided by the semaphores' own
blocking behaviour — and provided **atomically**, which `counter` never was.

**Why `in`/`out` need no separate semaphore.** They are updated *inside* the `mutex` critical
section, so the mutex protects them. That is the `S43` note's point: *"Any access to the buffer must
be protected by this semaphore [mutex]."*

#### Step 2: protect the shared data (S44)

```c
/* Producer process (Step 2) — Protect Shared Data */
item nextProduced;
while (1) {
    ...
    produce nextProduced;
    ...
    Wait(mutex);
      ...
      add nextProduced to buffer;
      ...
    Signal(mutex);
}
```

The note: *"`add nextProduced to buffer;` is a critical section"* — it is the read-modify-write of the
buffer contents **and** of `in`.

#### Step 3: manage the shared resources (S45)

```c
/* Producer process (Step 3) — Manage Shared Resources */
item nextProduced;
while (1) {
        ...
        produce nextProduced;
        ...
        Wait(empty);          // consume one empty slot
        Wait(mutex);
            ...
            add nextProduced to buffer;
            ...
        Signal(mutex);
        Signal(full);         // signal consumers
}
```

#### The consumer (S46)

```c
/* Consumer process — Protect Shared Data and Manage Shared Resources */
item nextConsumed;
while (1) {
    Wait(full);               // consume one full slot
    Wait(mutex);
        ...
        nextConsumed = item from buffer;
        ...
    Signal(mutex);
    Signal(empty);            // signal producers
        ...
        consume the item nextConsumed;
}
```

Note the deliberate asymmetry: the consumer **signals `empty` and then leaves the item consumption
outside** the critical section. Only the *buffer manipulation* is protected; the actual "use the
item" work runs concurrently. Producers likewise `produce nextProduced` outside.

#### Why this is correct — the boundary table

| Violation that would occur without protection | Prevented by | Where |
|---|---|---|
| producer writes when all `n` slots are full | `Wait(empty)` | blocks the producer until a slot exists |
| consumer reads when the buffer is empty | `Wait(full)` | blocks the consumer until an item exists |
| two producers updating `in` / the buffer simultaneously | `Wait(mutex)` | one at a time |
| two consumers updating `out` simultaneously | `Wait(mutex)` | one at a time |
| producer and consumer touching the same slot simultaneously | `Wait(mutex)` | one at a time |

And the conservation law that makes the whole thing analysable:

```
full = n - empty        true while no producer is blocked; when empty < 0, full = n
```

#### The order of the `Wait`s — the deadlock on S46

> **What if we swap as below?**
> ```
> Wait(mutex);
> Wait(full);
> ```
> **DEADLOCK if buffer is empty!**

Trace it. `buffer` empty ⇒ `full = 0`:

| Step | Who | Action | `mutex` | `full` | Consequence |
|---|---|---|---|---|---|
| 0 | — | initial | 1 | 0 | buffer empty; a producer may be about to produce |
| 1 | Consumer | `Wait(mutex)` succeeds | 0 | 0 | consumer **holds the mutex** |
| 2 | Consumer | `Wait(full)` — `full = 0` ⇒ **blocks** | 0 | 0 | consumer is waiting for an item **while holding the mutex** |
| 3 | Producer | produces an item, then `Wait(mutex)` — **blocks** | 0 | 0 | producer can never insert, so can never `Signal(full)` |

Circular wait: the consumer holds `mutex` and waits for `full`; `full` can only be signalled by a
producer; the producer needs `mutex`, which the consumer holds. **Deadlock.**

The rule to memorise:

> **Acquire the counting (resource) semaphore *before* the binary (mutex) semaphore, always.**
> Waiting for a resource must never be done while holding the lock that would let someone supply the
> resource.

Two more facts worth having ready:

* Swapping the **`Signal`s** at the end is **not** a bug. `Signal(full); Signal(mutex);` is still
  correct; it merely lets a woken consumer run and immediately block on `mutex`. Only the **`Wait`
  order** is a correctness issue.
* With **one** producer and **one** consumer, `mutex` is unnecessary — `buffer[in] = …` and
  `buffer[out] = …` touch different slots, and `in`/`out` are private. `mutex` becomes necessary the
  moment there are **two** producers or **two** consumers, because `in` (resp. `out`) is then shared.
  `S43`'s "multiple producers/consumers" is precisely the case where it is mandatory.

### 12.2 Dining philosophers (S47–S50)

#### The problem (S47)

> Five philosophers seated in a round table alternating between **eating** and **thinking**. Five
> plates (one for each philosopher) and only **five chopsticks** (one between each plate).
> **Problem**: devise a strategy to enable the philosophers to eat peacefully!

The note adds the rules that make it a synchronisation problem:

> A philosopher can only pick the chopstick **one at a time**. He **cannot take the chopsticks from
> others**. He can eat only when he picks **both** chopsticks. When he finishes eating, he puts down
> the chopsticks.

So: a philosopher `i` needs chopstick `i` (his left) and chopstick `(i+1) % 5` (his right, shared
with philosopher `i+1`). Chopsticks are the **shared resources**.

#### The initial solution (S48)

> Each philosopher is a process. Each chopstick is a shared resource protected by a **binary
> semaphore** (`chopstick[5]`). Initially, for all `i`, `chopstick[i] = 1`.

```c
/* Code (Philosopher i) */
while (1) {
    Wait(chopstick[i]);
    Wait(chopstick[(i + 1) % 5]);
    eat
    Signal(chopstick[i]);
    Signal(chopstick[(i + 1) % 5]);
    think
}
```

Follows `S38` exactly: one semaphore **per kind of resource instance** (five chopsticks = five
semaphores, each with 1 instance), `Wait` on acquisition, `Signal` on release.

#### The deadlock (S49)

> Consider the following interleaving (`Pi` = Philosopher `i`):
> ```
> P0 executes Wait(0); and then context switch to P1
> P1 executes Wait(1); and then context switch to P2
> P2 executes Wait(2); and then context switch to P3
> P3 executes Wait(3); and then context switch to P4
> P4 executes Wait(4);
> ```
> **Each philosopher has 1 chopstick and needs another to eat → Deadlock!**

| Step | Who | Action | `chopstick[]` | Holds |
|---|---|---|---|---|
| 0 | — | init | `[1,1,1,1,1]` | |
| 1 | P0 | `Wait(chopstick[0])` | `[0,1,1,1,1]` | P0 holds c0 |
| 2 | P1 | `Wait(chopstick[1])` | `[0,0,1,1,1]` | P1 holds c1 |
| 3 | P2 | `Wait(chopstick[2])` | `[0,0,0,1,1]` | P2 holds c2 |
| 4 | P3 | `Wait(chopstick[3])` | `[0,0,0,0,1]` | P3 holds c3 |
| 5 | P4 | `Wait(chopstick[4])` | `[0,0,0,0,0]` | P4 holds c4 |
| 6 | P0 | `Wait(chopstick[1])` — held by P1 ⇒ blocks | all 0 | waits for c1 |
| 7 | P1 | `Wait(chopstick[2])` — held by P2 ⇒ blocks | all 0 | waits for c2 |
| … | … | circular | | P4 waits for c0, held by P0 |

Circular wait around the table, and no philosopher can reach a `Signal` because every `Signal` comes
after the second `Wait`.

> **Exam framing.** The deadlock needs **all five** philosophers to hold their first chopstick
> simultaneously. With **four or fewer** hungry philosophers, at least one chopstick is free, so
> somebody always has two — the pigeonhole argument. Say this; it explains *why* remedy (a) works.

#### The remedies (S50)

| # | Remedy (`S50`) | Mechanism | Which condition it breaks |
|---|---|---|---|
| **a** | "Allow at most **four** philosophers to be **hungry simultaneously**" | add one counting semaphore initialised to **4**, `Wait`ed before the first chopstick and `Signal`ed after the second | **circular wait** cannot form — with only 4 contenders, one chopstick of the five is unheld, so one philosopher can always get both |
| **b** | "Allow a philosopher to pick up his chopsticks **only if both are available**" | acquire the *pair* atomically — e.g. a `mutex` around both `Wait`s, or an AND-semaphore | **hold and wait** — the philosopher never holds one while waiting for the other |
| **c** | "Use an **asymmetric** solution: an **odd** philosopher picks up first his **left** chopstick then his **right**; an **even** philosopher picks up first his **right** then his **left**" | different acquisition orders for neighbours | **circular wait** — the cycle is broken between at least one pair of neighbours |
| **d** | *(not on the slide)* impose a **global order** on resources: every philosopher takes the **lower-numbered** chopstick first | total ordering of resource acquisition | **circular wait** — the standard, general version of (c) |

The slide's own promise, which is why the deck stops here:

> Here, you just need to know that those solutions will make sure: **even when all five philosophers
> are hungry at the same time, at least one philosopher can eat.** […] We will talk more in our next
> chapter.

Remedy (b)'s cost, worth a sentence in an answer: it reduces concurrency — a philosopher can be
blocked even when his two chopsticks are individually free but someone else is in the middle of
grabbing another pair, so throughput drops.

Remedy (a) is the cheapest to write:

```c
semaphore room = 4;      /* at most four hungry philosophers */

while (1) {
    Wait(room);
    Wait(chopstick[i]);
    Wait(chopstick[(i + 1) % 5]);
    eat
    Signal(chopstick[(i + 1) % 5]);
    Signal(chopstick[i]);
    Signal(room);
    think
}
```

### 12.3 Readers and writers (S51–S53)

#### The problem (S51)

> **Scenario** in a database or file: a **writer requires exclusive access**; **multiple readers can
> concurrently access**.
> * The **first reader**: before reading, it must **block the writers**.
> * The **last reader**: after reading, it can **allow writers**.
> * **Readers given preference** (writer preference also possible).

The note explains why the asymmetry is deliberate:

> For system throughput, we try to **maximize the probability of concurrent accesses from readers**.
> Suppose a reader is accessing the database. During this period, if another reader comes, we allow
> multiple readers to access and **block the writers**. Only after the **last reader** has exited […]
> do we let a writer in.

So the rule is not "one at a time"; it is **"any number of readers, or exactly one writer"** — a
read-write lock.

| Item | Classification (`S51`) |
|---|---|
| `int readcount = 0` | shared **variable** — "tracks # readers in the database" |
| the database itself | shared **resource** |
| `mutex = 1` | binary semaphore — "protects access to `readcount`" |
| `wrt = 1` | binary semaphore — "mutual exclusion to database" |

The two semaphores have completely different jobs, and mixing them up is the classic error:

* `wrt` is the **database lock** — held by a writer, *or* by the reader collective (via its first
  reader). It is what keeps writers out.
* `mutex` is the **`readcount` lock** — held only for the few instructions that inspect/increment/
  decrement `readcount`. It is never held while reading.

#### The writer (S52)

```c
/* Writer process */
Wait(wrt);
    ...
    writing is performed
    ...
Signal(wrt);
```

Three lines. A writer is *always* exclusive: it does not care how many readers there are, because
`wrt` is only free when `readcount == 0`.

#### The reader (S53)

```c
/* Reader process */
Wait(mutex);
readcount++;
if (readcount == 1) Wait(wrt);      /* the FIRST reader: request access to database */
Signal(mutex);
            ...
        reading is performed
            ...
Wait(mutex);
readcount--;
if (readcount == 0) Signal(wrt);    /* the LAST reader: release database */
Signal(mutex);
```

`S53`'s annotations, mapped onto the code:

| Line | `S53` label | Meaning |
|---|---|---|
| `Wait(mutex); readcount++;` | *When a reader comes* | enter the `readcount` critical section |
| `if (readcount == 1) Wait(wrt);` | *The first reader: Request access to database* | reader #1 takes the database lock **on behalf of all readers** |
| `Signal(mutex);` | | leave the `readcount` critical section — **then** read |
| `Wait(mutex); readcount--;` | *When a reader leaves* | re-enter the `readcount` critical section |
| `if (readcount == 0) Signal(wrt);` | *The last reader: Release database* | reader #n hands the database back to the writers |
| `Signal(mutex);` | | leave |

The note: *"`readcount` is the shared variable. So we need to use a `mutex` for synchronization."*

#### Why it is correct — a state table

| `readcount` | `wrt` | Who is inside | Who can enter next |
|---|---|---|---|
| 0 | 1 (free) | nobody | a reader (becomes first, takes `wrt`) or a writer |
| 0 → 1 | 1 → 0 | reader #1 | more readers (they only take `mutex`) |
| ≥ 1 | 0 (held) | readers only | more readers; **writers blocked** |
| 1 → 0 | 0 → 1 | last reader is leaving | a writer |
| — | 0 | one writer | nobody (readers block on `wrt`, writers block on `wrt`) |

Invariant: **`wrt` is held iff (`readcount > 0` or a writer is writing)**. Both entries into `wrt`
take it exactly once per "reader generation", and both exits release it exactly once — that is what
the `== 1` / `== 0` tests guarantee.

#### The subtleties examiners like

1. **Why can't two readers both take `wrt`?** Because only the reader that observes
   `readcount == 1` **after incrementing** takes it. The `readcount++` and the test are inside
   `mutex`, so exactly one reader sees the transition `0 → 1`.
2. **The first reader blocks on `wrt` while holding `mutex`.** That looks like the `S46` deadlock,
   but it is not: a writer only ever needs `wrt`, never `mutex`, so it will finish and release `wrt`.
   The cost is that other arriving readers queue on `mutex` instead of on `wrt`.
3. **Reader preference ⇒ writer starvation.** While any reader is inside, new readers are admitted
   (they only need `mutex`), so a continuous stream of readers can postpone a writer forever. This is
   a `S41` starvation, caused by the policy choice on `S51` ("readers given preference").
4. **The writer-preference variant** adds a semaphore that arriving readers must also `Wait` on, so a
   waiting writer is admitted next; that in turn can starve readers. You cannot have both without
   fairness machinery.

> **Trap.** Protecting `readcount` with `wrt` "to save a semaphore" collapses the two roles into one.
> The first reader would have to `Wait(wrt)` to reach `readcount`, and then `Wait(wrt)` **again** as
> the readers' representative — a **self-deadlock**, because a binary semaphore is not recursive.
> With a single semaphore you can have mutual exclusion *or* reader concurrency, never both.

---

## 13. Monitors (S54)

The last slide, and the only one on the highest-level construct:

> **Monitor**: a **high-level synchronization construct** that allows the **sharing of variables**
> among concurrent processes.
> * Monitor is a collection of **procedures and data**.
> * Processes may **call procedures within the monitor** to access and update the data.
> * **Only one process can be active in the monitor at any one time** (i.e., only one process can be
>   executing a monitor procedure at any one time).
> * **Data within the monitor can only be accessed by procedures within it.**

The slide carries the banner **"This slide is not examinable"** — so this is orientation, not content
to memorise. The useful mental model is in the note:

> You can consider it as a **Java class**. Processes call the procedures within the monitor to access
> the shared data. The operating system ensures that only one process is active inside at any one
> time.

| | Semaphore | Monitor |
|---|---|---|
| Who enforces ME | the **programmer**, by placing `Wait`/`Signal` correctly | the **compiler / runtime** |
| Where the synchronisation lives | scattered through the code | **inside** the data structure's methods |
| Failure mode | misuse ⇒ deadlock / starvation (`S40`, `S41`) | misuse is largely impossible by construction |
| Analogy | a flag you must remember to raise | an object with synchronized methods |

The progression of the chapter — and the answer to "why does `S23` list three levels?" — is exactly
this table read top to bottom: *hardware (one lock, no fairness) → semaphore (`Wait`/`Signal`, fair but
easy to misuse) → monitor (correct by construction)*.

---

## 14. One-page reference

### The five protocols, side by side

```c
/* Alg 1 — turn */                      /* Alg 2 — per-process flag */
while (turn != i);                      flag[i] = true;
    critical section                    while (flag[k]);
turn = k;                                   critical section
                                        flag[i] = false;

/* Alg 3 — Peterson */                  /* TestAndSet */
flag[i] = true;                         while (TestAndSet(&lock));
turn = k;                                   critical section
while (flag[k] && turn == k);           lock = false;
    critical section
flag[i] = false;

/* Semaphore as mutex */
Wait(mutex);   /* mutex = 1 */
    critical section
Signal(mutex);
```

### Properties

| Protocol | Mutual exclusion | Progress | Bounded waiting |
|---|---|---|---|
| **Algorithm 1** (`turn`) | ✓ | ✗ — uninterested process blocks the other | ✓ (fair `turn`) |
| **Algorithm 2** (`flag[]`) | ✓ | ✗ — both wait forever | ✓ (vacuous) |
| **Algorithm 3** (Peterson) | ✓ | ✓ | ✓ (fair `turn`) |
| **`TestAndSet`** (single `lock`) | ✓ | ✓ | ✗ — `S27` trace |
| **Semaphore** (`Wait`/`Signal`) | ✓ | ✓ | ✓ if the queue is FIFO; ✗ with priority/LIFO (`S41`) |

### Semaphore semantics

```
counting   : value in [0, n]     binary : value in {0, 1}

value > 0  ->  # free resource instances
value = 0  ->  none free, nobody waiting
value < 0  ->  # of processes blocked in L   (|value|)

Wait(S):   S.value--;  if (S.value <  0) block();
Signal(S): S.value++;  if (S.value <= 0) wakeup(P);
```

### Decision procedure for any problem on this topic

```
1. What is shared?          a variable (logical)  -> binary semaphore, init 1
                            a resource (physical) -> counting semaphore, init #instances
2. Where is the critical section?  surround it with Wait(mutex)/Signal(mutex)
3. What ordering is required?      semaphore init 0, Signal in the earlier process, Wait in the later
4. Order the Waits:  resource semaphore FIRST, mutex SECOND  (else deadlock — S46)
5. Check: deadlock (cycle of holds-and-waits)? starvation (queue policy)?
```

### Invariants worth quoting

| System | Invariant |
|---|---|
| bounded buffer | `0 <= full <= n`, and `full = n - empty` while `empty >= 0` |
| dining philosophers | each chopstick is held by at most one philosopher; deadlock needs **all five** to be holding one |
| readers-writers | `wrt` held iff (`readcount > 0` ∨ a writer is writing) |
| semaphore | `value < 0` ⇒ the list `L` holds exactly `-value` processes |




---

## 15. Practice problems

Try each before reading the solution.

**P1.** `counter = 5`, and each of `counter++` / `counter--` compiles to three register instructions
(`load`, `add/sub`, `store`). One producer and one consumer each execute their statement exactly
once. List **every** possible final value of `counter` and say which interleaving produces it.

**P2.** Algorithm 1 uses `while (turn != i);` with `turn` initialised to `0`. Both `P0` and `P1` want
to enter, but `P0` is currently blocked on I/O in its remainder section. What happens to `P1`?
Which property fails, and what exactly in the code causes it?

**P3.** Algorithm 2 with `flag[0] = flag[1] = false`. Trace the interleaving
`P0: flag[0] = true` → switch → `P1: flag[1] = true`. What are the two processes doing at the next
step, and which property is violated?

**P4.** Peterson's algorithm with the wait condition written as `while (flag[k] || turn == k);`
instead of `while (flag[k] && turn == k);`. Run **one** process, `P0`, with `P1` never executing at
all. What happens? Which property breaks — and does mutual exclusion break too?

**P5.** Two processes use `while (TestAndSet(&lock));` with `lock = false` initially. Round-robin,
quantum `Q`. `P0`'s acquire (lines 1–3) takes exactly `Q`; one full loop of `P0`'s body (acquire,
critical section, release, re-acquire) takes exactly `Q`. Show that `P1` never enters its critical
section. Which property does this violate, and which one does it *not*?

**P6.** A counting semaphore `S` is initialised to `2`. Execute, in order:
`Wait(S)`, `Wait(S)`, `Wait(S)`, `Signal(S)`, `Wait(S)`, `Wait(S)`, `Signal(S)`, `Signal(S)`.
Give `S.value` and `|L|` after every operation, and state who is in the critical section.

**P7.** A student writes the blocking `Wait` as
`S.value--; if (S.value <= 0) block();`
— that is, `<` replaced by `<=`. Using `mutex = 1`, show what goes wrong on the very first `Wait`.

**P8.** Bounded buffer with `n = 5`, semaphores `full = 0, empty = 5, mutex = 1`. A producer produces
6 items before the consumer runs at all. Give `full`, `empty` and the producer's state after each
`Wait(empty)`/`Signal(full)` pair.

**P9.** In the bounded-buffer solution, `Wait(empty); Wait(mutex);` deadlocks if swapped. Is
`Signal(full); Signal(mutex);` (swapped) also a bug? Justify.

**P10.** Five philosophers, five chopsticks. (a) Show the deadlock interleaving. (b) Would the same
solution deadlock with only **four** philosophers and four chopsticks? (c) Which of the `S50`
remedies changes the *number* of processes that can be contending, and which change the *order* of
acquisition?

**P11.** Readers-writers with `readcount = 0`, `wrt = 1`, `mutex = 1`. Trace: R1 arrives, R2
arrives, W1 arrives, R3 arrives, R1 leaves, R2 leaves, R3 leaves. Give `readcount`, `wrt`, and who
is blocked at each step.

**P12.** Three processes must execute `A` (in `P1`), then `B` (in `P2`), then `C` (in `P3`). Write
the semaphore code, including initial values.

**P13.** A system has **3** identical printers, and any number of processes may request one. Write the
`acquire`/`release` code and give the semaphore's initial value. What does a value of `-2` mean here?

**P14.** Explain why `Signal(S)` never blocks the calling process, even when `L` is empty.

### Solutions

**S1.** `5`, `6`, or `4`.
* `5` — the two read-modify-write sequences do **not** interleave: one process completes `load`,
  `add`, `store` before the other starts. (Either order gives 5.)
* `4` — the consumer's `load` reads `5` *before* the producer stores `6`, and the consumer's `store`
  is the **last** write. This is the `S09` trace: the increment is lost.
* `6` — the mirror image: the producer's `load` reads `5`, the consumer completes to `4`, and the
  producer's `store` of `6` is last. The decrement is lost.
A value outside `{4, 5, 6}` is impossible: every interleaving ends with one of the three stores or a
store of a value computed from `5`.

**S2.** `turn = 0`, so `P1` spins in `while (turn != 1);` forever. `P0` never reaches its **exit
section**, so `turn` is never set to `1`. **Progress** is violated. The cause is that `turn` encodes
only *whose turn it is*, not *who wants in* — the entry section of one process depends on the
progress of another process's remainder section, which `S12`'s assumption explicitly does not allow
you to rely on.

**S3.** Both flags are `true`; `P0` spins on `while (flag[1]);` and `P1` spins on `while (flag[0]);`.
Neither can enter, so neither can execute its exit section to clear its flag — a **livelock**.
**Progress** is violated. (Mutual exclusion is trivially intact: nobody is inside.)

**S4.** `P0` executes `flag[0] = true; turn = 1;` and then evaluates
`flag[1] (=false) || turn == 1 (=true)`. The second operand is **true — because `P0` itself just
wrote `turn = 1`**. So `P0` spins forever and never enters the critical section, even though nobody
else is interested and the section is empty. **Progress** is violated.

Mutual exclusion is *not* violated; it fails in the opposite direction (nobody can ever enter, so
never two at once). Symmetrically, if both processes run, each writes `turn` against itself and both
spin — a livelock. `&&` is essential because it is what encodes "wait only if the other is
**interested** *and* has **priority**"; `||` drops the "interested" part, and the algorithm
degenerates into Algorithm 1's defect.

**S5.** Quantum 1: `P0` runs lines 1–3 and **acquires** the lock (it is inside the CS when its quantum
expires). Quantum 2: `P1` runs lines 1–2, `TestAndSet` returns `true`, and it spins for the rest of
its quantum. Quantum 3: `P0` runs release + remainder + acquire, so `lock` is `true` again. Quantum 4:
`P1`'s quantum again contains only the failing `TestAndSet`. `P1`'s request is never granted:
**bounded waiting** is violated. Mutual exclusion and progress are **not** violated — at most one
process is ever inside, and the lock is genuinely available in the instants between `P0`'s release and
re-acquire.

**S6.** Start `S = 2`, `|L| = 0`.

| # | Op | `S.value` | waiters in `L` | Effect |
|---|---|---|---|---|
| 1 | `Wait` | 1 | 0 | A enters |
| 2 | `Wait` | 0 | 0 | B enters |
| 3 | `Wait` | −1 | 1 | C blocks |
| 4 | `Signal` | 0 | 0 | C woken → ready |
| 5 | `Wait` | −1 | 1 | whoever runs blocks (say C) |
| 6 | `Wait` | −2 | 2 | second waiter blocks |
| 7 | `Signal` | −1 | 1 | one woken |
| 8 | `Signal` | 0 | 0 | one woken |

Two permits existed, so at most **two** processes are ever inside the critical section; at step 4 the
`0` (not `< 0`) test is what performs the wakeup.

**S7.** With `mutex = 1`, the first `Wait` does `S.value--` → `0`, then tests `0 <= 0` → **true** →
`block()`. The process blocks although it is entitled to the permit, and it holds the permit while
blocked. Nobody else can ever enter (they see `-1`), and the blocker cannot proceed because it is in
the waiting state: **deadlock / progress violated on the very first acquisition**. Hence `<` after a
decrement, and `<=` after an increment.

**S8.** `n = 5`, so `empty` counts empty slots and `full` counts items.

| Item # | `Wait(empty)` → | inserts | `Signal(full)` → | Producer state |
|---|---|---|---|---|
| 1 | 5 → 4 | item 1 | 0 → 1 | proceeds |
| 2 | 4 → 3 | item 2 | 1 → 2 | proceeds |
| 3 | 3 → 2 | item 3 | 2 → 3 | proceeds |
| 4 | 2 → 1 | item 4 | 3 → 4 | proceeds |
| 5 | 1 → 0 | item 5 | 4 → 5 | proceeds |
| 6 | 0 → −1 | — | — | **blocks** on `empty`; one producer queued |

`full = 5` and `empty = −1` ⇒ the buffer holds 5 items and **one** producer is waiting for a free
slot. The invariant needs a caveat: while `empty >= 0`, `empty = n − full` (hence `full = n − empty`);
once `empty` goes negative the buffer is full, `full = n`, and `|empty|` is the number of producers
blocked on it. So `empty + full = n` is **not** an identity across a block — it is an identity of the
countable state only.

**S9.** Not a bug. `Signal` is a pure *increment plus optional wakeup*; reordering the two signals
only changes **who runs when**. With `Signal(full)` first, a woken consumer may immediately try
`Wait(mutex)`, fail, and block again — wasted work but still correct, because the producer will
`Signal(mutex)` a moment later. The `Wait` order is different in kind: it determines whether a
process can be **blocked while holding a lock somebody else needs**, which is a permanent circular
wait. `Signal` order affects performance only; `Wait` order affects correctness.

**S10.**
(a) `P0` takes `chopstick[0]`, `P1` takes `chopstick[1]`, …, `P4` takes `chopstick[4]`, then each
blocks on the next chopstick — a 5-cycle, nobody can reach a `Signal` (`S49`).
(b) The question only makes sense with **five chopsticks** still on the table, and then the answer is
**no**: with at most four contenders, at most four chopsticks are held, so one is free — and that
free chopstick is the second chopstick of one of the four contenders, who can then eat. The general
rule: the deadlock needs **every** contender to hold one chopstick while waiting for the next, i.e.
all `k` of `k` philosophers must be in the entry section at once. Reduce the number of contenders
below the number of chopsticks and the cycle cannot close.
(c) Remedy **(a)** (at most four hungry) changes the **number** of contenders — four contenders, five
chopsticks, so one chopstick is always free and the cycle cannot close. Remedies **(b)**, **(c)** and
**(d)** change the **order**/**atomicity** of acquisition: (b) makes the pair atomic (no
hold-and-wait), (c) and (d) impose a partial or total order on the chopsticks so no cycle can form.

**S11.** `readcount` (r), `wrt` (w), `mutex` (m).

| Step | Event | r | w | Who is inside / blocked |
|---|---|---|---|---|
| 0 | init | 0 | 1 | — |
| 1 | R1 arrives: `m--`(0), `r=1`, `1==1 ⇒ Wait(w)` (w=0), `Signal(m)`(1) | 1 | 0 | **R1 reading** |
| 2 | R2 arrives: `m--`(0), `r=2`, `2!=1`, `Signal(m)`(1) | 2 | 0 | **R1, R2 reading** |
| 3 | W1 arrives: `Wait(wrt)` — `w=0` ⇒ **blocks** | 2 | 0 | W1 blocked on `wrt` |
| 4 | R3 arrives: `m--`, `r=3`, `3!=1`, `Signal(m)` | 3 | 0 | **R1, R2, R3 reading**; W1 still blocked |
| 5 | R1 leaves: `r=2`, `2!=0`, `Signal(m)` | 2 | 0 | R2, R3 reading |
| 6 | R2 leaves: `r=1`, `1!=0` | 1 | 0 | R3 reading |
| 7 | R3 leaves: `r=0`, `0==0 ⇒ Signal(wrt)` (w=1) | 0 | 1 | W1 wakes → **W1 writing** |

Step 4 is the reader-preference behaviour: R3 was admitted **while a writer was already waiting**.
Repeat step 4 forever and W1 starves.

**S12.**
```c
semaphore sAB = 0, sBC = 0;

P1:  A;  Signal(sAB);
P2:  Wait(sAB);  B;  Signal(sBC);
P3:  Wait(sBC);  C;
```
Each semaphore is initialised to **0** because each is a **notification**, not a lock. The chain gives
`A → B → C`; note `P2` both waits and signals, which is how transitivity is built.

**S13.**
```c
semaphore printers = 3;      // one per instance of the resource

acquire:  Wait(printers);
release:  Signal(printers);
```
`value` starts at **3** = number of instances. `-2` means **two** processes are blocked waiting for a
printer (all three printers are in use). At most three processes are ever printing, which is the
correctness condition.

**S14.** `Signal(S)` only ever **increases** `S.value`, and increments cannot make a process unable to
proceed. The `wakeup(P)` branch is guarded by `S.value <= 0` **after** the increment, i.e. it fires
only when there was at least one waiter *before* the increment — and if there was, `L` is non-empty by
definition, so there is a process to dequeue. The asymmetry with `Wait` is fundamental: `Wait` may
have to **wait** for a condition; `Signal` merely **reports** that a condition became true.

---

## 16. Self-test questions

1. State the three ingredients necessary for a race condition, and explain what each contributes.
2. Why is `counter++` unsafe even though it is a single C statement? Show the three-instruction
   expansion.
3. `counter = 5`; one producer and one consumer each execute once. Give all possible final values
   and the interleaving that produces each.
4. Define **critical section**, and give the one-line statement of the critical-section problem.
5. Draw the generic process structure and label all four sections with their purpose.
6. State the two assumptions of `S12`. Why does the "no assumption about relative speed" assumption
   matter for proofs?
7. Define mutual exclusion, progress and bounded waiting **without** using the words of the others.
8. Which two properties together guarantee "no process is stuck in the entry section forever", and
   why is neither sufficient alone?
9. For Algorithm 1: which property fails, and what is the precise code reason?
10. For Algorithm 2: which property fails, and what is the precise interleaving? What does the slide
    claim about bounded waiting, and how should you phrase it in an exam?
11. Write Peterson's algorithm from memory. Then delete either `flag[]` or `turn` and say which
    property dies.
12. Define **atomic** and explain what the hardware disables to make `TestAndSet` atomic.
13. Write `TestAndSet` and explain why the return value is the **old** value.
14. Prove mutual exclusion for the `TestAndSet` lock in two sentences.
15. Reproduce the `S27` bounded-waiting trace with a per-quantum table. Which property fails, and
    which one plainly does not?
16. Why does `TestAndSet` fail bounded waiting but the semaphore does not?
17. Define a semaphore, and give the two types with their value ranges.
18. Give the busy-waiting implementation and both sides of its trade-off. When is busy waiting the
    *better* choice?
19. Show, with a trace, that a non-atomic `Wait` violates mutual exclusion even for a binary
    semaphore initialised to 1.
20. Write the blocking semaphore record and the full `Wait`/`Signal` bodies. Why is one test `< 0`
    and the other `<= 0`?
21. `S.value = -2`: how many processes are waiting? What does `0` mean? What does `+3` mean?
22. Why must `S.value--` happen **before** `block()`? Give the four-step trace that violates mutual
    exclusion when it does not.
23. Explain why `Signal` never blocks, using the post-increment test.
24. Is a blocking semaphore immune to the atomicity requirement? Justify with the two `S35` traces.
25. Distinguish a **shared variable** from a **shared resource** and give the semaphore type and
    initial value for each.
26. Write the semaphore code that guarantees `B` runs only after `A`, and explain why the semaphore
    is initialised to 0.
27. Define deadlock and starvation, and explain why the `S40` program deadlocks while the `S41`
    scenario is *not* a deadlock.
28. Write the producer and consumer of the bounded buffer with `mutex`/`empty`/`full`, then show the
    deadlock caused by swapping `Wait(mutex)` and `Wait(full)`.
29. Why is `counter` not needed in the semaphore version? Why is `mutex` not needed with a single
    producer and single consumer but needed with two producers?
30. Write the dining-philosophers initial solution and its deadlock interleaving. Then give the three
    remedies on `S50` and say which condition each breaks.
31. Why can the deadlock only happen when **all five** philosophers hold a chopstick?
32. Write the readers-writers reader and writer. Why `readcount == 1` and `readcount == 0`?
33. Why does readers-preference starve writers, and what is the writer-preference fix's own cost?
34. What is a monitor, and which member of the `S23` hierarchy does it correspond to? Is it
    examinable?

---

## 17. Glossary

| Term | Meaning |
|---|---|
| **Race condition** | a bug in which the final value of shared data depends on the order of instruction execution, i.e. on where context switches occur (`S08`, `S09`) |
| **Data inconsistency** | the outcome of a race: a value that no sequential execution could produce (`S03`) |
| **Critical section** | the code segment in which a process accesses shared data (`S10`) |
| **Entry section** | the code that asks permission to enter the critical section (`S11`) |
| **Exit section** | the code that leaves the critical section and notifies others (`S11`) |
| **Remainder section** | all non-critical code (`S11`) |
| **Mutual exclusion** | at most one process in the critical section at any time (`S12`) |
| **Progress** | if the CS is empty and processes wish to enter, one of them must be admitted — the choice cannot be postponed indefinitely (`S13`) |
| **Bounded waiting** | after requesting entry, a process may be overtaken only a bounded number of times (`S13`) |
| **Livelock** | processes are not blocked but make no progress (both spinning in their entry sections) (`S13` note) |
| **Atomic** | non-interruptible; no context switch from the first instruction to the last (`S24`) |
| **TestAndSet** | atomic instruction returning the old value of a word and setting it to `true` (`S24`) |
| **Spin / busy wait** | repeatedly testing a condition in a loop, consuming CPU (`S30`) |
| **Semaphore** | integer shared variable accessible only through the atomic operations `Wait` and `Signal` (`S28`) |
| **Counting semaphore** | semaphore whose value ranges over an unrestricted domain; counts resource instances (`S28`) |
| **Binary semaphore** | semaphore whose value never exceeds 1; used as a mutex (`S28`) |
| **`Wait(S)`** | acquire: decrement; block if the result is negative (`S28`, `S34`) |
| **`Signal(S)`** | release: increment; wake a waiter if the result is `<= 0` (`S28`, `S34`) |
| **`block()`** | dequeue the running process from the ready queue, enqueue it to `L`, set state to waiting (`S33`) |
| **`wakeup()`** | dequeue a process from `L`, enqueue it to the ready queue, set state to ready (`S33`) |
| **`L`** | the semaphore's list of blocked processes; when `S.value < 0` it holds `-S.value` of them (`S32`) |
| **Mutex** | a binary semaphore initialised to 1, used to protect a critical section (`S29`) |
| **Deadlock** | two or more processes waiting indefinitely for an event that only another waiting process can cause (`S40`) |
| **Starvation** | indefinite postponement: a process is never selected from the semaphore queue because of the queue discipline (`S41`) |
| **Aging** | raising the priority of a long-waiting process; the standard cure for starvation (`S41` note) |
| **Readers-writers** | synchronisation pattern allowing concurrent readers or one exclusive writer (`S51`) |
| **`readcount`** | number of readers currently inside; protected by `mutex` (`S51`) |
| **`wrt`** | binary semaphore protecting the database from writers; held by a writer or by the readers collectively (`S51`) |
| **Monitor** | high-level construct: procedures + data, with at most one process active inside; **not examinable** (`S54`) |

---

## 18. Where this goes next

Two threads leave this chapter:

* **Deadlock, properly.** `S40` gives only the two-process circular-wait example as a *semaphore
  misuse*. The mechanisms — the four necessary conditions, prevention, avoidance (Banker's
  algorithm), detection and recovery — are the next chapter, [`../c7`](../c7).
* **Real-time systems.** Priority inversion, one of the classic consequences of priority-based
  waiting, is discussed with scheduling guarantees and inheritance protocols in [`../c6a`](../c6a).

Before moving on, make sure you can write, from memory and without hesitation, the bounded-buffer
solution with `mutex`/`empty`/`full` (§12.1) and the readers-writers solution (§12.3): those two are
the reusable skeletons. Everything else in the chapter is an argument about *why* they are correct.
