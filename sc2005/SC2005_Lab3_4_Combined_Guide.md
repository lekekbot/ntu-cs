# SC2005 — Labs 3 & 4 Combined Guide

**Lab 3 · Synchronization and Semaphores**  
**Lab 4 · Virtual Memory Management**

One document: every checkpoint question from both labs, the answer to give, the reasoning behind it,
an ELI5 for each hard idea, the full list of code changes, and the run output that proves each
result.

| | Lab 3 | Lab 4 |
|---|---|---|
| Tree | [xv6zz-lab3/](./xv6zz-lab3/) | [xv6-lab4/](./xv6-lab4/) |
| Question it answers | *How do two CPUs avoid stepping on each other?* | *When does a promise of memory become real memory?* |
| Kernel files touched | `semaphore.c` | `proc.c`, `trap.c`, `vm.c`, `sysproc.c`, `syscall.c`, `syscall.h` |
| User files touched | `race_test.c` | `lazytest.c`, `usys.pl` |
| Test programs | `race_test` | `lazytest`, `fault` |
| Run | `make CPUS=3 qemu` → `race_test` | `make CPUS=3 qemu` → `lazytest`, `fault read`, `fault write` |

Companion sources, if you want raw evidence rather than the combined narrative:

* [LAB3_ANSWERS.md](./xv6zz-lab3/LAB3_ANSWERS.md) — Lab 3 answers and command output
* [Lab 3 STUDY_NOTES.md](./xv6zz-lab3/STUDY_NOTES.md) — Lab 3 revision notes
* [LAB4_ANSWERS.md](./xv6-lab4/LAB4_ANSWERS.md) — Lab 4 answers and command output
* [Lab 4 STUDY_NOTES.md](./xv6-lab4/STUDY_NOTES.md) — Lab 4 revision notes

---

## Table of contents

1. [Orientation](#0-orientation) — the two trees, the 60-second summary, how to build
2. [ELI5 first](#1-eli5-first) — both labs in plain language
3. [One question, two labs](#2-one-question-two-labs)
4. [**Lab 3**](#3-lab-3--synchronization-and-semaphores)
   * [Checkpoint 0](#30-checkpoint-0--orientation)
   * [Checkpoint 1](#32-checkpoint-1--synchronization-mechanisms)
   * [Checkpoint 2](#33-checkpoint-2--the-blocking-semaphore)
   * [Checkpoint 3](#34-checkpoint-3--protecting-the-shared-counter)
   * [Checkpoint 4](#35-checkpoint-4--producers-and-a-consumer)
   * [What was edited / added](#36-what-was-edited--added-in-lab-3)
   * [Evidence](#37-evidence-lab-3)
5. [**Lab 4**](#4-lab-4--virtual-memory-management)
   * [Checkpoint 0](#40-checkpoint-0--orientation)
   * [Background: Sv39](#41-background-you-must-have-cold-sv39)
   * [Checkpoint 1](#42-checkpoint-1--the-eager-path-from-sbrk-to-kalloc)
   * [Checkpoint 2](#43-checkpoint-2--counting-virtual-pages-vs-physical-frames)
   * [Checkpoint 3](#44-checkpoint-3--page-faults-and-the-trap-path)
   * [Checkpoint 4](#45-checkpoint-4--allocate-frames-on-demand)
   * [Optional: stack growth](#46-optional-discussion--stack-growth)
   * [What was edited / added](#47-what-was-edited--added-in-lab-4)
   * [Evidence + regressions](#48-evidence-lab-4)
6. [Traps that cost marks](#5-traps-that-cost-marks)
7. [Self-check questions with answers](#6-self-check-questions-with-answers)
8. [One-page revision card](#7-one-page-revision-card)
9. [Change log for this guide](#8-change-log-for-this-guide)

---

## 0. Orientation

### 0.1 The two trees

```
sc2005/
├── xv6zz-lab3/     lab3 branch — semaphores, race_test
└── xv6-lab4/       lab4 branch — lazy allocation, lazytest, fault
```

Both are forks of MIT's `xv6-riscv` running on RISC-V under QEMU. Neither tree contains the lab
manual; the checkpoints below are reconstructed from the lab's own questions and the code.

### 0.2 The whole of Lab 3 in one paragraph

Two processes share kernel objects — a counter and a circular buffer. **Entering the kernel does not
make a sequence of operations atomic**, so any check-then-act on shared state can be interleaved.
You build one primitive, a **blocking semaphore**, from two things xv6 already has: a **spinlock**
(for the short protected update) and **`sleep`/`wakeup`** (for the wait). Then you use it twice: as a
**mutex** to make a read–modify–write indivisible, and as **counting semaphores + a mutex** to
coordinate two producers and a consumer.

### 0.3 The whole of Lab 4 in one paragraph

xv6 allocates physical memory **eagerly**: the moment `sbrk()` returns, every page of the new range
already has a frame. This lab measures that (`countvp`/`countpp`), proves it is wasteful, then
replaces it with **demand paging**: `sbrk()` only moves a number (`p->sz`), and the *first access*
to each page traps into the kernel, which allocates and maps a frame and then retries the faulting
instruction. The whole exercise is one sentence — **separating "the address is reserved" from "the
memory exists"** — and the price of that separation is that every place which assumed
"reserved ⇒ mapped" must now tolerate holes.

### 0.4 Build and run

```sh
cd xv6zz-lab3      # or xv6-lab4
make clean
make CPUS=3 qemu
```

Inside the xv6 shell:

```
$ race_test          # Lab 3
$ lazytest           # Lab 4
$ fault read
$ fault write
```

Leave QEMU with `Ctrl-a`, release both, then `x`.

`CPUS=3` matters for Lab 3: on one CPU the lost-update race is far less likely to reproduce, and the
spin-vs-sleep argument assumes other harts exist.

---

## 1. ELI5 first

### 1.1 Lab 3 — the shared kitchen

> **ELI5.** Two cooks share one kitchen and one whiteboard. Each cook reads the number on the
> whiteboard, adds one, writes it back. If both read "100" before either writes, both write "101" and
> one meal disappears. The whiteboard is `ucnt[0]`.
>
> **A spinlock** is a single physical key hanging by the door. You can only take it if it is
> hanging there — and "look, then take" must be *one* motion, or two cooks both see it hanging and
> both grab. The instruction that makes it one motion is `amoswap`.
>
> **A semaphore** is a door with a counter above it. `wait` decrements; if the counter is already 0
> you sit in the waiting room (`sleep`). `signal` increments and calls everyone in the waiting room
> (`wakeup`). But calling everyone in does not mean they all get in — so each one looks at the
> counter again before entering. That is the `while` loop.
>
> **Producer/consumer** is a 16-slot pass-through hatch. `empty` counts free slots, `filled` counts
> ready dishes, and `mutex` means "only one pair of hands inside the hatch at a time". If you grab
> the hatch lock *before* checking for free space, you can deadlock: you hold the only way in, and
> the person who would free a slot needs that way in.

### 1.2 Lab 4 — the hotel

> **ELI5.** `sbrk()` is a hotel taking a **reservation**: it writes your name in the book and promises
> you room 34. **Eager allocation** is a hotel that also sends a maid to make the bed in every
> reserved room the instant you book — even if you never show up. **Lazy allocation** is a hotel that
> only makes the bed when you actually open the door (the **page fault**), then lets you walk in
> again and carry on.
>
> The PTE is the **key card**: it says which physical room your room number maps to, and what you may
> do there (read/write/enter). No key card = reservation with no room.
>
> The **guard page** is the "staff only" door at the bottom of the stairwell. The room exists and is
> paid for, but your key does not open it — so a stack overflow trips an alarm instead of walking
> into the lift shaft.
>
> `walk()` is the receptionist walking down three levels of index cards to find the right key-card
> slot. On the last level she hands you the *slot*, not the key — you must look inside yourself.

### 1.3 Vocabulary decoder

| Term | Means | Not to be confused with |
|---|---|---|
| **hart** | a RISC-V hardware thread / CPU core | a process |
| **spinlock** | busy-wait lock, held for a few instructions | a sleeping lock (`sleeplock`) |
| **condition lock** | lock guarding the *predicate* a waiter tests | `p->lock` |
| **process lock** (`p->lock`) | lock guarding one process's `state`/`chan`; required by `sched()` | the condition lock |
| **wait channel** (`chan`) | an identifying *tag* (an address) | a queue or a mailbox; no data passes through it |
| **semaphore count** | how many units of a resource are available | how many processes are inside |
| **mutex** | a semaphore initialised to 1 | any semaphore |
| **virtual page** | a 4 KiB slot in a process's address space | a physical frame |
| **PTE** | 8-byte page-table entry: PPN + permission flags | the frame itself |
| **PPN** | physical page number stored in a PTE | a virtual address |
| **frame** | 4 KiB of real RAM | a *page-table* frame (holds PTEs) |
| **`sbrk` break** (`p->sz`) | end of the process's address space | the amount of RAM in use |
| **demand paging** | map a frame on first touch | pre-faulting / eager mapping |
| **`walk(alloc=0)`** | pure lookup, no side effects | `walk(alloc=1)` allocates page tables |

---

## 2. One question, two labs

The two labs are the same intellectual move applied to different machinery:

| | Lab 3 | Lab 4 |
|---|---|---|
| The dangerous gap | between **checking** a condition and **acting** on it | between **reserving** an address and **backing** it |
| What closes it | one indivisible operation (`amoswap`, or test+decrement under a lock) | one trap handler that repairs the mapping before the instruction retries |
| The failure mode if you get it wrong | two processes in the critical section; a lost update; a lost wakeup | a wild pointer gets a frame; a guard page becomes writable; a cleanup panics on a hole |
| The invariant to re-check | "the value I read is still the value I write" | "reserved ⇒ mapped" — now false |
| Where the re-check lives | `while` loop in `sem_wait`; `p->lock` before dropping `lk` | three-way fault classification in `usertrap` |

> **The single sentence that covers both labs:**
> *a data structure's invariant must be re-checked after every change to the mechanism that maintains it.*

---

# 3. Lab 3 — Synchronization and Semaphores

## 3.0 Checkpoint 0 — orientation

| Item | What to show |
|---|---|
| Active branch | `git checkout lab3` → `git branch --show-current` prints `lab3` |
| Three-CPU boot | `make CPUS=3 qemu` prints `hart 2 starting` / `hart 1 starting` |
| Files located | [kernel/spinlock.c](./xv6zz-lab3/kernel/spinlock.c), [kernel/spinlock.h](./xv6zz-lab3/kernel/spinlock.h), [kernel/proc.c](./xv6zz-lab3/kernel/proc.c), [kernel/semaphore.c](./xv6zz-lab3/kernel/semaphore.c), [kernel/ucnt.c](./xv6zz-lab3/kernel/ucnt.c), [kernel/ubuf.c](./xv6zz-lab3/kernel/ubuf.c), [user/race_test.c](./xv6zz-lab3/user/race_test.c) |
| Selecting one test | comment out the other calls in `main()` and the `ALL TESTS PASSED` print, keep `exit(0)` |

The three test parts live in one program, [user/race_test.c](./xv6zz-lab3/user/race_test.c):
`sem_basic()`, `race_test()`, `producer_consumer()`.

---

## 3.1 Background: the four mechanisms

### 3.1.1 The spinlock

Lock state is one field:

```c
// kernel/spinlock.h
struct spinlock {
  uint locked;   // 0 = free, 1 = held
  ...
};
```

Acquisition ([kernel/spinlock.c](./xv6zz-lab3/kernel/spinlock.c)):

```c
void acquire(struct spinlock *lk) {
  push_off();                                        // interrupts off on THIS hart
  if(holding(lk)) panic("acquire");

  while(__sync_lock_test_and_set(&lk->locked, 1) != 0)  // atomic swap
    ;

  __sync_synchronize();                              // fence: no reordering
  lk->cpu = mycpu();
}
```

`__sync_lock_test_and_set` compiles to a single RISC-V instruction, `amoswap.w.aq`. The read and the
write are one indivisible operation. Release is the mirror image: fence, then
`__sync_lock_release` (`amoswap.w zero, zero, ...`).

`push_off()` clears the interrupt-enable bit in **this hart's** `sstatus`. It exists to avoid
*deadlock*, not to provide mutual exclusion: if a timer interrupt fired while holding a spinlock,
the handler (or a process it switches to) could spin forever on a lock held by the code it just
interrupted.

### 3.1.2 `sleep` and `wakeup`

```c
// kernel/proc.c
void sleep(void *chan, struct spinlock *lk) {
  struct proc *p = myproc();
  acquire(&p->lock);   // take the process lock FIRST
  release(lk);         // only then drop the condition lock
  p->chan = chan;
  p->state = SLEEPING;
  sched();             // switch to the scheduler; p->lock goes with us
  p->chan = 0;
  release(&p->lock);
  acquire(lk);         // return holding lk, exactly as passed in
}

void wakeup(void *chan) {
  for(p = proc; p < &proc[NPROC]; p++) {
    if(p != myproc()){
      acquire(&p->lock);
      if(p->state == SLEEPING && p->chan == chan)
        p->state = RUNNABLE;
      release(&p->lock);
    }
  }
}
```

Three facts that carry the whole lab:

1. `chan` is a **tag**, not storage. Equal tags mean "same waiting room".
2. `acquire(&p->lock)` happens **before** `release(lk)`. That ordering is what makes a wakeup
   impossible to lose.
3. `wakeup()` wakes **all** sleepers on the channel and reserves **nothing**. Hence every waiter
   must re-test its condition in a `while` loop.

State machine: `RUNNING → SLEEPING` (sleep) → `RUNNABLE` (wakeup) → `RUNNING` (scheduler).

### 3.1.3 The semaphore interface

| Layer | Name | What it does |
|---|---|---|
| user API | `sem_init(value)`, `sem_wait(id)`, `sem_signal(id)`, `sem_getvalue(id)`, `sem_free(id)` | libc-style wrappers, [user/user.h](./xv6zz-lab3/user/user.h) |
| stub | `entry("sem_wait")` … | generated into `user/usys.S` by [user/usys.pl](./xv6zz-lab3/user/usys.pl) |
| kernel handler | `sys_sem_wait()` … | [kernel/sysproc.c](./xv6zz-lab3/kernel/sysproc.c) — `argint()` then call |
| kernel object | `sem_wait()`, `sem_signal()`, … | [kernel/semaphore.c](./xv6zz-lab3/kernel/semaphore.c) |

Syscall numbers: `SYS_sem_init 26`, `SYS_sem_wait 27`, `SYS_sem_signal 28`,
`SYS_sem_getvalue 29`, `SYS_sem_free 30` ([kernel/syscall.h](./xv6zz-lab3/kernel/syscall.h)).
The table holds `MAX_SEMAPHORES = 32` entries.

### 3.1.4 The test harness

`race_test()` forks one child; each side runs `N = 1000` increments of `ucnt[0]`; the parent waits
and asserts `ucnt[0] == 2000`. `producer_consumer()` forks two producer children and consumes in the
parent: `48 chars × 2 producers = 96` reads.

---

## 3.2 Checkpoint 1 — synchronization mechanisms

### The question

1. Where does the lock keep its state, what is the atomic operation, what are interrupts doing — and
   why is disabling interrupts **not** enough for mutual exclusion?
2. In `sleep()`/`wakeup()`, what are the two locks, when is each held and released, what are the
   state transitions, why can a wakeup not be lost, and why must the waiter re-check?
3. A wait of ≈10 cycles vs ≈10,000 cycles — spinning or sleeping, and under what assumptions?

### 3.2.1 Why acquisition must be atomic, and why `intr_off()` is not enough

**The answer.** Lock state is `uint locked` in [kernel/spinlock.h](./xv6zz-lab3/kernel/spinlock.h).
The atomic operation is `__sync_lock_test_and_set(&lk->locked, 1)` — one `amoswap.w.aq`.
Interrupts are cleared/restored by `push_off()`/`pop_off()`, which touch **this hart's** `sstatus`.

`intr_off()` gives you no mutual exclusion between CPUs, because another hart has its own
`sstatus` and is executing the same instructions on the same memory. Suppose acquisition were
"read, then write":

| Time | CPU A | CPU B | `locked` |
|---|---|---|---|
| t1 | reads `locked` → 0 | | 0 |
| t2 | | reads `locked` → 0 | 0 |
| t3 | writes `1` | | 1 |
| t4 | | writes `1` | 1 |
| t5 | enters critical section | enters critical section | 1 |

Both saw `0` and both believe they hold the lock. `amoswap` removes the window: exactly one hart
observes `0`; everyone else's swap returns `1` and keeps spinning.

Two supporting details:

* `__sync_synchronize()` **after** acquisition stops the compiler/CPU from hoisting a critical-section
  access above the lock point.
* `release()` fences **before** clearing, so all critical-section stores are visible to the next
  holder before the lock appears free.

> **ELI5.** Two people look at a door sign that says FREE, both walk in, and both hang up their own
> "OCCUPIED" sign. Turning off your own phone ringer does not stop the other person from walking in.

### 3.2.2 The two lock roles in `sleep`/`wakeup`

| Lock | Role | Protects |
|---|---|---|
| `lk` | **condition lock** | the shared data the caller tests (`sem->value`, `ticks`, …) |
| `p->lock` | **process lock** | that one process's `p->state` and `p->chan`; required by `sched()` |

**Waiter trace** (entering with `lk` held):

| Step | Where | Holds |
|---|---|---|
| 1. test condition | caller's `while` | `lk` |
| 2. `sleep(chan, lk)` | [proc.c](./xv6zz-lab3/kernel/proc.c) | `lk` |
| 3. `acquire(&p->lock)` | | `lk` **and** `p->lock` |
| 4. `release(lk)` | | `p->lock` only |
| 5. `p->chan = chan; p->state = SLEEPING;` | | `p->lock` |
| 6. `sched()` → `swtch()` | | `p->lock` handed to scheduler |
| 7. later: `RUNNABLE`, scheduler picks it, `swtch` back | | `p->lock` again |
| 8. `p->chan = 0; release(&p->lock);` | | nothing |
| 9. `acquire(lk)` | | `lk` — returns exactly as it was passed in |

**Why the wakeup cannot be lost.** The waker holds the *same* `lk` while it changes the shared data
and calls `wakeup()`. So when the waker holds `lk`, the waiter is in exactly one of two places:

1. it has **not yet** tested the condition → it will acquire `lk` afterwards, see the new value, and
   never sleep; or
2. it has **already stored `SLEEPING`** → and it did that under `p->lock`, which `wakeup()` also
   takes before inspecting `p->state`, so `wakeup()` is guaranteed to see it and set `RUNNABLE`.

There is no third possibility. The mechanical reason is the ordering: **`p->lock` is acquired
*before* `lk` is released**.

**Why the waiter must re-check.** `wakeup()`:

* does not run the waiter immediately — it only marks it `RUNNABLE`;
* does not reserve the resource;
* wakes **every** process on that channel.

With two waiters and one unit, both wake and only one can proceed. Between "marked RUNNABLE" and
"actually running", the resource can vanish. So the test is a `while`, not an `if`. An `if` lets the
loser fall through and decrement the count to `-1`.

> **ELI5.** You wait for a table at a restaurant. The host shouts "table free!" to everyone waiting
> — not just to you. You still have to look at the board when you get there. If you assumed the
> shout was a personal reservation, you would sit down at a table someone else took.

### 3.2.3 Spinning vs sleeping

**What sleeping really costs.** Not one switch: `acquire(&p->lock)`, `release(lk)`, a state change,
`sched()`, `swtch()` out, the scheduler loop, `swtch()` back, plus the waker's `wakeup()` scan over
all `NPROC` = 64 slots taking each `p->lock`. Hundreds to a few thousand cycles. Spinning costs a few
cycles per attempt but burns an entire CPU — and xv6 spins with interrupts off, so that CPU can do
nothing else.

| Wait length | Cheaper | Why |
|---|---|---|
| ≈10 cycles | **spin** | shorter than a single `swtch()`, never mind two switches plus a `wakeup()` scan |
| ≈10,000 cycles | **sleep** | on total system cycles: the spinning CPU could run the process that releases the resource |

**Assumptions to state:**

1. The holder can actually run — another CPU, or scheduling while we sleep. On a uniprocessor with
   the holder descheduled and interrupts off, spinning deadlocks; sleeping is the only option.
2. "Cheaper" means **total system cycles**, not this process's latency. Sleeping adds wake-up
   latency, so a latency-critical short wait may still prefer spinning.
3. 10 and 10,000 are illustrative magnitudes, **not measured xv6 thresholds**. The crossover is
   roughly "wait > two context switches + one `wakeup()` scan".

### Checkpoint 1 answer box

* Lock state `locked`; atomic op `amoswap` via `__sync_lock_test_and_set`; interrupts disable only
  this hart → **no cross-CPU exclusion**; read-then-write lets both CPUs see `0`.
* `lk` = condition lock, `chan` = tag, `p->lock` = scheduling state; `p->lock` is taken **before**
  `lk` is dropped → no lost wakeup; `wakeup` reserves nothing → re-check in a `while`.
* 10 cycles: spin. 10,000: sleep. Assumptions: holder can run, "cheaper" = system-wide,
  magnitudes illustrative.

---

## 3.3 Checkpoint 2 — the blocking semaphore

### The question

1. Distinguish the three "init"s and describe the user→kernel interface.
2. Implement `sem_wait`/`sem_signal`/`sem_getvalue`: which lock, which channel, why `while`, where
   the decrement goes.
3. What does `sem_basic()` prove, and what does it leave untested?
4. When is it safe to free a semaphore?

### 3.3.1 The three different "init"s (exam favourite)

| Name | Where | What it really is |
|---|---|---|
| `sem_init(value)` | [user/user.h](./xv6zz-lab3/user/user.h) | a **syscall**: `SYS_sem_init` → `sys_sem_init()` → `sem_alloc(value)` |
| `sem_alloc(value)` | [kernel/semaphore.c](./xv6zz-lab3/kernel/semaphore.c) | the **allocator**: takes `sem_table_lock`, finds a free slot, sets `in_use = 1`, stores the initial value, returns the index or `-1` |
| `seminit()` | [kernel/semaphore.c](./xv6zz-lab3/kernel/semaphore.c) | **boot-time** setup, called once from `main()`; initialises `sem_table_lock` and every slot's lock, marks all slots free. Returns nothing, hands out nothing. |

So: **initialised at boot, allocated on demand**, and `semid` is merely an index into
`semaphores[]`.

### 3.3.2 The implementation

```c
int sem_wait(int semid)
{
  if(semid < 0 || semid >= MAX_SEMAPHORES || !semaphores[semid].in_use)
    return -1;

  struct semaphore *sem = &semaphores[semid];

  acquire(&sem->lock);
  while(sem->value == 0)
    sleep(sem, &sem->lock);
  sem->value--;
  release(&sem->lock);

  return 0;
}

int sem_signal(int semid)
{
  if(semid < 0 || semid >= MAX_SEMAPHORES || !semaphores[semid].in_use)
    return -1;

  struct semaphore *sem = &semaphores[semid];

  acquire(&sem->lock);
  sem->value++;
  wakeup(sem);
  release(&sem->lock);

  return 0;
}

int sem_getvalue(int semid)
{
  if(semid < 0 || semid >= MAX_SEMAPHORES || !semaphores[semid].in_use)
    return -1;

  struct semaphore *sem = &semaphores[semid];

  acquire(&sem->lock);
  int value = sem->value;
  release(&sem->lock);

  return value;
}
```

**Lock** = that semaphore's own `sem->lock`, used as the condition lock.
**Channel** = `sem`, the address of the `struct semaphore`. Because the address differs per
semaphore, a `sem_signal` on semaphore 3 can never wake a waiter on semaphore 5.

**Why `while`.** `wakeup()` is not a hand-off and wakes all sleepers on the channel; the loser must
re-test and sleep again. This is also what keeps `value` **non-negative**, which is the semaphore
definition this lab requires.

**Why the decrement is inside the lock.** `sem->value--` is a read–modify–write on shared state; it
must not be interleaved with a `sem_signal`. `sem_signal` makes increment+wakeup one atomic step for
the same reason — signalling outside the lock allows a waiter to miss the wakeup.

### 3.3.3 What `sem_basic()` proves and what it does not

```
[sem_basic] Initializing semaphore to 1...
[sem_basic] Waiting (should decrement to 0)...
[sem_basic] Posting (should increment to 1)...
[sem_basic] PASS: Basic semaphore operations work.
```

It proves the count sequence `1 → 0 → 1` and that `sem_free` succeeds.

It **never calls `sem_wait` on a zero value**, so it never executes `sleep()`, `wakeup()`, the
re-check loop, or `sched()`. It is single-threaded, so there is no contention. It also does not test
two waiters + one signal, table exhaustion at `MAX_SEMAPHORES`, the `-1` error paths, or freeing a
semaphore that still has users.

Part 4 exercises the blocking path for real: the consumer's first `sem_wait(b.filled)` must sleep
because `filled` starts at 0.

> **ELI5.** A test that opens and closes a door proves the handle turns. It says nothing about what
> happens when forty people push at once. **A passing test only proves what it exercises.**

### 3.3.4 When is it safe to free a semaphore?

`sem_free()` only clears `in_use`: it neither wakes nor waits for users. So it is safe only when no
process can still call `sem_wait`/`sem_signal` on that id:

* in `race_test()`: after `wait(0)` has reaped the child;
* in `producer_consumer()`: after all 96 reads **and** both producers reaped.

Freeing earlier is dangerous: the slot can be reallocated to an unrelated semaphore, and a process
still sleeping on the old channel would be woken by — or decrement — the **new** one.

### Checkpoint 2 answer box

* `sem_init` = syscall; `sys_sem_init` = handler; `sem_alloc` = allocator; `seminit` = boot setup.
* Per-semaphore `sem->lock`; channel = `&semaphores[semid]`; `while` because wakeup reserves
  nothing and wakes everyone; decrement under the lock.
* `1 → 0 → 1` passes; zero-count sleep path untested (Part 4 covers it).
* Free only after all users have finished; here, after `wait()`.

---

## 3.4 Checkpoint 3 — protecting the shared counter

### The question

1. Show the lost-update interleaving.
2. Why is protecting the two syscalls *separately* insufficient?
3. What is the expected final count, how is the semaphore shared across `fork()`, and why does the
   parent wait before reading it?

### 3.4.1 The lost update

```c
int val = ucnt_get(0);      // syscall: kernel reads ucnt[0]
ucnt_set(0, val + 1);       // syscall: kernel writes ucnt[0]
```

Each syscall is atomic only in the sense that one kernel instruction sequence runs. Between them the
process returns to user space and can be preempted — and on `CPUS=3` the other process can run the
same code at the same instant.

| Time | Parent | Child | `ucnt[0]` |
|---|---|---|---|
| t1 | `get()` → 100 | | 100 |
| t2 | | `get()` → 100 | 100 |
| t3 | `set(101)` | | 101 |
| t4 | | `set(101)` | 101 |

Two increments, one unit of progress.

**Measured with the protection removed:**

```
[race_test] final counter=1737 (expected 2000)
Assertion failed at user/race_test.c:53: final == 2*N
```

Short by 263 increments. (Line 53 in that temporary build; in the final file the assertion is at
[user/race_test.c](./xv6zz-lab3/user/race_test.c) line 55.)

### 3.4.2 Why separate locks per syscall cannot work

The invariant is not "a syscall must not be interrupted". It is:

> **the value I read must still be the value I write.**

That spans **both** calls. Locking inside each syscall (already effectively true — each runs in the
kernel) leaves the gap *between* them open, and the interleaving above lives exactly in that gap.
The critical section is the read–modify–write **pair**, so the lock must be taken in **user space**
around the pair.

> **ELI5.** Two people fill in the same form. Each is careful to use the pen alone. That does not
> help if both read the old total before either writes the new one — the pen was never the problem.

### 3.4.3 The fix

```c
void do_work(int pid, int semid) {
    for (int i = 0; i < N; i++) {
        sem_wait(semid);            // enter critical section
        int val = ucnt_get(0);
        ucnt_set(0, val + 1);
        sem_signal(semid);          // leave critical section
    }
}

void race_test() {
    ucnt_set(0, 0);
    int semid = sem_init(1);        // initial count 1 => mutex
    T_ASSERT(semid >= 0);

    int pid = fork();
    ...
    do_work(getpid(), semid);
    wait(0);                        // child's increments must be finished
    int final = ucnt_get(0);
    ...
    sem_free(semid);                // safe: no users left
}
```

Initial count **1** is what makes it a mutex: the first `sem_wait` succeeds (1 → 0) and everyone else
blocks until the holder signals (0 → 1).

**Why the child's copied `semid` is the same semaphore.** `fork()` copies user memory, so the child
gets a copy of the integer. But that integer is only an **index** into the kernel's `semaphores[]`,
which lives in kernel memory and is not copied. Both processes therefore name the same kernel
object — which is exactly why the protection works across the fork.

**Why the parent waits first.** `wait(0)` blocks until the child exits, so the final read sees all
1000 child increments. It is also what makes the later `sem_free()` safe.

**Expected: `2 * N = 2000`.** One unprotected run returning 2000 proves nothing — races are
nondeterministic.

### Checkpoint 3 answer box

* Interleaving table above; observed `1737 != 2000`.
* The invariant spans both calls; a per-syscall lock leaves the gap open.
* `2000 = 2*N`; `sem_init(1)` before `fork()`; `semid` indexes one shared kernel table.
* `wait(0)` first: complete the total, and no users remain before freeing.

---

## 3.5 Checkpoint 4 — producers and a consumer

### The question

1. Give each semaphore's role and initial value, and derive the values.
2. Trace one byte from producer to consumer.
3. Why do slot counts alone not protect the buffer?
4. How does the run complete and clean up?
5. What does the supplied membership assertion actually prove?

### 3.5.1 The supplied buffer

[kernel/ubuf.c](./xv6zz-lab3/kernel/ubuf.c) is a 16-slot ring with shared `head` and `tail`. The
comment "buffer writes to head and read from tail" is **wrong**; follow the bodies —
`ubuf_write()` uses `tail`, `ubuf_read()` uses `head`.

```c
char ubuf_read(void) {
    char data = ubuf.data[ubuf.head];
    yield();                                   // descheduled MID-operation
    ubuf.head = (ubuf.head + 1) % UBUF_SIZE;
    return data;
}

void ubuf_write(char val) {
    ubuf.data[ubuf.tail] = val;
    yield();                                   // descheduled MID-operation
    ubuf.tail = (ubuf.tail + 1) % UBUF_SIZE;
}
```

Neither function checks empty/full. The `yield()` sits between the data access and the index update
precisely to widen the window and expose missing mutual exclusion.

### 3.5.2 Counts and call order

```c
#define UBUF_SLOTS 16   // must match UBUF_SIZE in kernel/ubuf.c

struct buf_sem {
    int empty;    // free slots,  initialised to UBUF_SLOTS
    int filled;   // filled slots, initialised to 0
    int mutex;    // binary, initialised to 1
};
```

| Semaphore | Initial | Derived from | Role |
|---|---|---|---|
| `empty` | **16** | buffer starts empty → all `UBUF_SIZE` slots free | counts **space**; producer waits, consumer signals |
| `filled` | **0** | buffer starts empty → no data | counts **data**; consumer waits, producer signals |
| `mutex` | **1** | unlocked | binary; protects `data`/`head`/`tail` |

```c
producer:  sem_wait(empty); sem_wait(mutex); ubuf_write(c); sem_signal(mutex); sem_signal(filled);
consumer:  sem_wait(filled); sem_wait(mutex); tmp = ubuf_read(); sem_signal(mutex); sem_signal(empty);
```

**Why `empty`/`filled` must be waited for before `mutex`.** Suppose a producer held `mutex` and then
blocked on `empty`. A free slot is only created by the consumer calling `sem_signal(empty)`, and the
consumer can only reach that after `ubuf_read()`, which it can only reach after `sem_wait(mutex)` —
held by the blocked producer forever.

```
producer: holds mutex, waits for empty
consumer: waits for mutex, which is needed to create empty
          └── circular wait ── deadlock
```

Waiting for the resource count first, holding no lock, removes the cycle. General rule: **never hold
a lock while waiting for a resource whose release requires that lock.**

### 3.5.3 Tracing one byte

Produce:

1. `sem_wait(b.empty)` — if all 16 slots are full, sleep on the `empty` channel; otherwise 16 → 15.
2. `sem_wait(b.mutex)` — 1 → 0; this producer is now the only one allowed inside the buffer.
3. `ubuf_write(c)` — store `c` at `data[tail]`, then **yield**. Anyone else who runs now blocks at
   `sem_wait(mutex)` (it is 0), so `head`/`tail` cannot be touched while this producer is paused
   between the store and the index update. That is exactly what `yield()` is there to test.
4. `sem_signal(b.mutex)` — 0 → 1, `wakeup(mutex)` releases a waiter.
5. `sem_signal(b.filled)` — 0 → 1, `wakeup(filled)` makes the consumer runnable.

Consume:

1. `sem_wait(b.filled)` — blocks while empty (the first thing the consumer does, since `filled` = 0).
2. `sem_wait(b.mutex)` — 1 → 0.
3. `ubuf_read()` — reads `data[head]`, yields, advances `head`; protected the same way.
4. `sem_signal(b.mutex)` — 0 → 1.
5. `sem_signal(b.empty)` — frees a slot and wakes a blocked producer.

Invariant: at any instant `empty + filled + (bytes inside the critical section)` = 16, and
`head`/`tail` are only touched with `mutex` held.

> **ELI5.** `empty`/`filled` are the "how many seats left" sign. `mutex` is the turnstile. A sign
> saying "3 seats" does not stop two people from sitting on the same chair while the usher is
> looking away.

### 3.5.4 Why slot counts alone are not enough

A counting semaphore enforces **how many** processes may be inside, not **who may not overlap with
whom** on shared indices. Taking only `empty`/`filled`:

* two producers both pass `sem_wait(empty)` and both write `data[tail]` with the **same** `tail` →
  one byte silently overwritten, `tail` advanced twice;
* two readers both take one `filled` token and read the same slot → duplicate byte;
* a reader reads `data[head]` while a writer is midway through.

`head`/`tail` are shared mutable state; only `mutex`, held across the **whole** function (including
past the `yield()`), makes payload access + index advance one indivisible step.
**Condition counts and mutual exclusion are different jobs — you need both.**

### 3.5.5 Completion and cleanup

The consumer runs in the parent. After it returns, the parent `wait(0)`s twice to reap both
producers, and only then frees all three semaphores:

```c
sem_free(b.mutex);
sem_free(b.filled);
sem_free(b.empty);
```

Totals that must balance: `sem_signal(filled)` == `sem_wait(filled)` == **96** (48 chars × 2).

### 3.5.6 What the test does *not* prove

```c
T_ASSERT(valid[(unsigned char)tmp]);
```

This only checks that each received byte is **one of** the characters in `msg`. It does not count
occurrences, does not check order, and cannot detect a duplicated, lost or reordered byte — as long
as the byte that arrives is in the set.

So a pass establishes: *no corrupted/foreign byte appeared* and *the run completed without a
deadlock*. The stronger correctness argument comes from the **design** (counts + mutex), not from
the test. Being able to say this is the point of the checkpoint.

### Checkpoint 4 answer box

* `empty = 16`, `filled = 0`, `mutex = 1`, derived from "buffer starts empty" and "locked".
* Trace in 3.5.3.
* Counts do not serialise the indices; `head`/`tail` need `mutex`.
* 96 reads in the parent, two `wait(0)`, then three `sem_free`.
* Membership-only assertion: cannot prove absence of duplication, loss or reordering.

---

## 3.6 What was edited / added in Lab 3

### 3.6.1 File-by-file

| File | Status | Change |
|---|---|---|
| [kernel/semaphore.c](./xv6zz-lab3/kernel/semaphore.c) | **edited** | Implemented `sem_wait` (sleep-on-zero + `while` re-check + decrement under the lock), `sem_signal` (increment + `wakeup` under the lock), `sem_getvalue` (locked read). |
| [user/race_test.c](./xv6zz-lab3/user/race_test.c) | **edited** | `do_work()` wraps the counter read–modify–write in a binary semaphore; `race_test()` creates it with `sem_init(1)` and frees it after `wait(0)`; `struct buf_sem` filled in with `empty`/`filled`/`mutex`; `producer()`/`consumer()` implement wait → mutex → buffer → mutex → signal; `producer_consumer()` initialises and frees the three semaphores. |
| [user/usertests.c](./xv6zz-lab3/user/usertests.c) | untouched (lab logic) | Contains no lab logic; see the build note below. |
| `kernel/spinlock.c`, `kernel/spinlock.h` | **unchanged by design** | The lab asks you to read them, not modify them. |
| `kernel/ucnt.c`, `kernel/ubuf.c` | **unchanged by design** | Provided; the bug they model must be fixed from user space. |

The scaffolding was already present and was **not** written by the lab work: syscall numbers 26–30,
the `sys_sem_*` handlers, the `usys.pl` stubs, the `user.h`/`defs.h` declarations, the `seminit()`
call in `main()`, and `semaphore.o`/`ucnt.o`/`ubuf.o` in the `Makefile`.

### 3.6.2 `kernel/semaphore.c` — the functions that were filled in

**Before:** `sem_wait`, `sem_signal`, `sem_getvalue` were unimplemented (the table, locks, allocator
and `sem_free` already existed).

**After:** the three bodies shown in [3.3.2](#332-the-implementation). The only structural change is
that each function now (a) validates `semid` including `in_use`, (b) takes `sem->lock`, (c) does its
work, (d) releases.

### 3.6.3 `user/race_test.c` — the three edits

**Edit 1 — protect the increment.**

```diff
 void do_work(int pid, int semid) {
     for (int i = 0; i < N; i++) {
+        sem_wait(semid);
         int val = ucnt_get(0);
         ucnt_set(0, val + 1);
+        sem_signal(semid);
     }
 }
```

**Edit 2 — create and free the mutex around the `fork()`.**

```diff
 void race_test() {
     ucnt_set(0, 0);
+    int semid = sem_init(1); // binary semaphore: mutual exclusion
+    T_ASSERT(semid >= 0);
 
     int pid = fork();
```

```diff
         printf("[race_test] PASS: consistent counter\n");
     }
+
+    sem_free(semid);
 }
```

**Edit 3 — the producer/consumer semaphore discipline.**

```diff
 struct buf_sem {
-    int empty;
-    int filled;
-    int mutex;
+    int empty;   // counts free slots, initialised to UBUF_SLOTS
+    int filled;  // counts filled slots, initialised to 0
+    int mutex;   // binary semaphore protecting the buffer indices, initialised to 1
 };
```

```diff
 void consumer(struct buf_sem b, int loops, int valid[]) {
     char tmp;
     for(int i = 0; i < loops; i++) {
+        sem_wait(b.filled);
+        sem_wait(b.mutex);
         tmp = ubuf_read();
+        sem_signal(b.mutex);
+        sem_signal(b.empty);
         T_ASSERT(valid[(unsigned char)tmp]);
     }
 }

 void producer(const char* msg, struct buf_sem b) {
     for (const char* p = msg; *p != '\0'; p++) {
+        sem_wait(b.empty);
+        sem_wait(b.mutex);
         ubuf_write(*p);
+        sem_signal(b.mutex);
+        sem_signal(b.filled);
     }
 }
```

```diff
+    struct buf_sem b;
+    b.empty = sem_init(UBUF_SLOTS); // buffer starts empty
+    b.filled = sem_init(0);         // nothing to consume yet
+    b.mutex = sem_init(1);          // unlocked
+    T_ASSERT(b.empty >= 0 && b.filled >= 0 && b.mutex >= 0);
```

Plus the two `wait(0)` calls after the consumer returns, and the three `sem_free` calls.

### 3.6.4 Build note (host toolchain, not lab logic)

With GCC 16 the tree's `-Wall -Werror` promotes `-Wunused-but-set-variable`, which used to break
`user/usertests.c:fsfull()` before any lab code could build:

```
user/usertests.c:2347:7: error: variable 'fsblocks' set but not used [-Werror=unused-but-set-variable=]
```

The recorded fix was to make the count observable, e.g.
`printf("fsfull test finished, %d blocks\n", fsblocks);`. In the tree as it stands, `fsfull()`
accumulates `total` and prints it, so the blocker is already gone and **no lab logic lives in
`usertests.c`**.

---

## 3.7 Evidence (Lab 3)

Full run, `CPUS=3`, all three parts enabled:

```
xv6 kernel is booting

hart 2 starting
hart 1 starting
init: starting sh
$ race_test
[sem_basic] Initializing semaphore to 1...
[sem_basic] Waiting (should decrement to 0)...
[sem_basic] Posting (should increment to 1)...
[sem_basic] PASS: Basic semaphore operations work.
[race_test] final counter=2000 (expected 2000)
[race_test] PASS: consistent counter
[producer_consumer] PASS: message delivered
ALL TESTS PASSED
```

* Three consecutive runs in one boot: all `final counter=2000` — no timing flakiness observed.
* With `producer_consumer()` alone: `[producer_consumer] PASS: message delivered`.
* Unprotected counter variant: `final counter=1737`, assertion failure — the race is real.

---

# 4. Lab 4 — Virtual Memory Management

## 4.0 Checkpoint 0 — orientation

| Item | Evidence |
|---|---|
| Active branch | `git checkout lab4` → `git branch --show-current` prints `lab4` |
| Boots to shell | `xv6 kernel is booting` / `hart 1 starting` / `hart 2 starting` / `init: starting sh` |
| `sys_sbrk()` | [kernel/sysproc.c](./xv6-lab4/kernel/sysproc.c) |
| `walk()` | [kernel/vm.c](./xv6-lab4/kernel/vm.c) |
| `usertrap()` | [kernel/trap.c](./xv6-lab4/kernel/trap.c) |
| Placeholders | [user/lazytest.c](./xv6-lab4/user/lazytest.c) originally defined `countvp()`/`countpp()` returning `0` |

---

## 4.1 Background you must have cold: Sv39

### 4.1.1 The bit layout

xv6 uses the low half only: `MAXVA = 1L << 38` ([kernel/riscv.h](./xv6-lab4/kernel/riscv.h)).

```
 bit 38    30 29    21 20    12 11         0
+-----------+---------+---------+-----------+
| L2 idx    | L1 idx  | L0 idx  |  offset   |
| 9 bits    | 9 bits  | 9 bits  |  12 bits  |
+-----------+---------+---------+-----------+
```

* page = 4096 B = 2¹² ⇒ offset needs **12** bits;
* one page holds `4096 / 8 = 512` PTEs = 2⁹ ⇒ each index needs **9** bits;
* `12 + 9 + 9 + 9 = 39` ⇒ **Sv39**.

Bits 63–39 must be zero for xv6's low half (bit 38 is always 0, so no sign extension).

### 4.1.2 The PTE

8 bytes: `PPN[2:0]` (44 bits) plus flags in the low 10 bits.

| Flag | Bit | Meaning |
|---|---|---|
| `PTE_V` | 0 | valid — entry is meaningful |
| `PTE_R` | 1 | readable |
| `PTE_W` | 2 | writable |
| `PTE_X` | 3 | executable |
| `PTE_U` | 4 | user mode may use this mapping |

`PTE2PA`/`PA2PTE` shift between encoded PPN and physical address.
`PTE_FLAGS(pte) = pte & 0x3FF`.

**The "valid but no permission bits" trick.** A *non-leaf* entry — one pointing to the next level of
the tree — is `PTE_V` only, with no `R/W/X`. So:

```c
PTE_FLAGS(*pte) == PTE_V   ⇒  this entry points to another PAGE TABLE, not a frame
```

That single test appears in both `uvmunmap()` and `countpp()`. Forgetting it in either place is a real
bug: you free or count a page table as if it were process data.

### 4.1.3 `walk()` — the one function to be able to draw

```c
for(int level = 2; level > 0; level--) {
  pte_t *pte = &pagetable[PX(level, va)];
  if(*pte & PTE_V) {
    pagetable = (pagetable_t)PTE2PA(*pte);   // descend
  } else {
    if(!alloc || (pagetable = (pde_t*)kalloc()) == 0)
      return 0;                              // missing table and alloc==0 → give up
    memset(pagetable, 0, PGSIZE);
    *pte = PA2PTE(pagetable) | PTE_V;        // install pointer entry (V only)
  }
}
return &pagetable[PX(0, va)];                // level 0: return the slot, UNEXAMINED
```

Four facts:

1. It descends levels 2 → 1 only. Level 0 is returned **by address** and not checked.
2. It can therefore return a pointer to a **non-valid** leaf PTE. "`walk()` succeeded" ≠ "the page is
   mapped". You must test `*pte & PTE_V` yourself.
3. `alloc != 0` allocates **page-table pages**. Never data frames.
4. `alloc == 0` is a pure lookup with no side effects — which is why `countpp()` and `uvmunmap()`
   use it.

> **ELI5.** `walk()` is a receptionist who will build new floors of the filing cabinet if you ask
> her to (`alloc=1`), but she never puts a document in the drawer. On the last level she points at
> the drawer and says "here". Whether it is empty is your problem.

### 4.1.4 `walkaddr()` — `walk()` plus the permission check

[kernel/vm.c](./xv6-lab4/kernel/vm.c) calls `walk(alloc=0)`, then rejects: no PTE, not `PTE_V`, and —
crucially — **not `PTE_U`**. It returns a *physical address*, and is used by `copyin`/`copyout`/
`copyinstr`.

The `!PTE_U` rejection is the guard-page question: the guard page is valid and backed, but not
user-accessible. `walkaddr()` refuses it; a raw `walk()` reports it as present.
**Choosing `walk` vs `walkaddr` is choosing whether the guard page counts.**

---

## 4.2 Checkpoint 1 — the eager path from `sbrk()` to `kalloc()`

### The question

1. Trace a virtual address through the page-table walk; what is the state of each level?
2. Follow a `morecore()`/`sbrk()` request down to where frames are allocated.
3. Distinguish virtual address / PTE / physical frame, and say which kind of frame `walk()` allocates.

### 4.2.1 The chain to recite

```
user: malloc() → morecore()                      user/umalloc.c
  → sbrk(nu * sizeof(Header))
  → stub: li a7, SYS_sbrk ; ecall                user/usys.S (generated)
kernel: syscall() indexes syscalls[a7]           kernel/syscall.c
  → sys_sbrk()  addr = p->sz ; growproc(n)       kernel/sysproc.c
  → growproc()  n>0: uvmalloc(...)               kernel/proc.c
  → uvmalloc()  loop: kalloc + memset + mappages kernel/vm.c
  → mappages()  walk(...,1) + install leaf PTE   kernel/vm.c
```

```c
// uvmalloc, in essence
oldsz = PGROUNDUP(oldsz);
for(a = oldsz; a < newsz; a += PGSIZE){
  mem = kalloc();            // data frame
  memset(mem, 0, PGSIZE);
  mappages(pagetable, a, PGSIZE, (uint64)mem, PTE_W|PTE_R|PTE_U);
}
```

That is **eager allocation**: frames exist as soon as `sbrk()` returns, before the program touches
the memory.

### 4.2.2 `sbrk()` returns the *old* break

```c
uint64 sys_sbrk(void) {
  uint64 addr = myproc()->sz;      // BEFORE growing
  if(growproc(n) < 0) return -1;
  return addr;                     // start of the new region
}
```

| `n` | Effect |
|---|---|
| `n > 0` | grow: `uvmalloc()` (eager) or just move `p->sz` (lazy) |
| `n == 0` | nothing changes; used to **query** the break (`fault.c` does this) |
| `n < 0` | `uvmdealloc()` → `uvmunmap()`, frees whole pages only |

`n == 0` is a favourite trick: `fault.c` learns the break *without* reserving anything, which is why
its target stays invalid even after lazy allocation exists.

### 4.2.3 Three different things people blur together

| | Virtual page | PTE | Physical frame |
|---|---|---|---|
| What | 4 KiB slot in the address space | 8-byte entry mapping one page + permissions | 4 KiB of real RAM |
| Created by | `sbrk()` moving `p->sz` | `mappages()` | `kalloc()` |
| Exists after lazy `sbrk()`? | **yes** | no | no |

`walk(alloc=1)` allocates **page-table frames** (bookkeeping, holding PTEs). `uvmalloc()`'s explicit
`kalloc()` allocates **data frames**. They are not the same thing, and only the latter hold process
data.

### Checkpoint 1 answer box

* Sv39: 9/9/9/12 bits; `walk` descends 2 → 1, returns the level-0 slot unchecked.
* A positive `sbrk()` → `growproc()` → `uvmalloc()` → `kalloc` + `memset` + `mappages`.
* `walk` allocates **page tables**, never data frames; lazy allocation still creates page tables on
  first touch of a new 2 MiB region, but no data frames until the page is used.

---

## 4.3 Checkpoint 2 — counting virtual pages vs physical frames

### The question

1. What exactly does each count include and exclude?
2. Why must the frame counter use `walk()` and not `walkaddr()`?
3. Wire two new syscalls and remove the user-space placeholders.
4. Run the test on the eager kernel and interpret every line.

### 4.3.1 The two handlers

```c
// Number of virtual pages intersecting [0, p->sz).
uint64 sys_countvp(void) {
  return PGROUNDUP(myproc()->sz) / PGSIZE;
}

// Number of frames backing [0, p->sz).
uint64 sys_countpp(void) {
  struct proc *p = myproc();
  uint64 npages = PGROUNDUP(p->sz) / PGSIZE;
  uint64 n = 0;

  for(uint64 a = 0; a < npages * PGSIZE; a += PGSIZE){
    pte_t *pte = walk(p->pagetable, a, 0);          // alloc = 0
    if(pte == 0 || (*pte & PTE_V) == 0) continue;   // hole / no page table
    if(PTE_FLAGS(*pte) == PTE_V) continue;          // points to another table
    n++;
  }
  return n;
}
```

Three details:

* `walk(..., 0)` counts existing mappings **without creating any** — the counting syscalls have no
  side effects.
* `walk()` not `walkaddr()`: `walkaddr()` rejects `!PTE_U`, which would drop the **guard page**, and
  the lab requires counting its frame.
* the `PTE_FLAGS(*pte) == PTE_V` check skips a valid entry that points to a lower-level table.

### 4.3.2 What is inside and outside `[0, p->sz)`

Inside, rounded up: program text/data, data, heap, user stack, **stack guard page**.

Outside:

* **page-table frames** — reachable only through `satp`, never through a user virtual address;
* the **kernel stack** — mapped in the kernel page table, not `p->pagetable`;
* **`TRAMPOLINE`** (`MAXVA - PGSIZE`) and **`TRAPFRAME`** (`MAXVA - 2*PGSIZE`) — fixed mappings far
  above any allowed `p->sz`.

A partly used final page counts as one whole virtual page (`PGROUNDUP`), because the hardware
translates whole pages.

### 4.3.3 The guard page

`exec()` allocates `USERSTACK + 1` pages and calls `uvmclear()` on the lowest one
([kernel/exec.c](./xv6-lab4/kernel/exec.c), [kernel/vm.c](./xv6-lab4/kernel/vm.c)).
`uvmclear()` clears `PTE_U` and leaves `PTE_V` and the physical address alone.

So the guard page:

* **has** a frame → it is counted, and later freed;
* is **not** user-accessible → overflowing the stack traps instead of corrupting data.

Visible consequence: `Before: VP=4, PP=4`, not `PP=3`.

> **ELI5.** The guard page is the "staff only" door. The room behind it is real and paid for, so the
> inventory counts it. Your key card just does not open it.

### 4.3.4 Eager result and how to read it

```
Starting lazy allocation test...
Before: VP=4, PP=4
After sbrk(122880): VP=34, PP=34
Error: PP count changed immediately (should be lazy)
Touching pages...
After touching: PP=34
Success: PP count increased after touching pages
```

| Line | Means |
|---|---|
| `Before: VP=4, PP=4` | 2 program pages + 1 guard page + 1 stack page (`USERSTACK` is 1); every page backed |
| `After sbrk(122880): VP=34, PP=34` | 30 pages reserved **and** 30 frames allocated at once → eager |
| `Error: PP count changed immediately` | the **expected** eager label — the test wanted lazy |
| `After touching: PP=34` | touches cause no faults; frames already existed |
| `Success: PP count increased after touching pages` | **false positive** |

Why the last line is a false positive: the check is `pp_after_touch - pp_before >= n_pages`, i.e.
`34 - 4 >= 30`. It is counting the increase that happened at `sbrk()` time. The label alone proves
nothing; only the intermediate `After sbrk(...)` line distinguishes eager from lazy.

**Eager signature:** `PP` rises **at** `sbrk`, is **flat** at touch, and **equals** `VP` throughout.
**Lazy signature:** `PP` flat at `sbrk` (`VP=34, PP=4`), then rising to `VP` only after touches.

### 4.3.5 Wiring

| Layer | Change |
|---|---|
| Numbers | `SYS_countvp 22`, `SYS_countpp 23` — [kernel/syscall.h](./xv6-lab4/kernel/syscall.h) |
| Dispatch | `extern` declarations + table entries — [kernel/syscall.c](./xv6-lab4/kernel/syscall.c) |
| Handlers | `sys_countvp`, `sys_countpp` — [kernel/sysproc.c](./xv6-lab4/kernel/sysproc.c) |
| Stubs | `entry("countvp")`, `entry("countpp")` — [user/usys.pl](./xv6-lab4/user/usys.pl) |
| Declarations | already in [user/user.h](./xv6-lab4/user/user.h) |
| Placeholders | removed from [user/lazytest.c](./xv6-lab4/user/lazytest.c) |

`user/usys.S` is generated, so only `usys.pl` was edited.

**Proof the calls reach the kernel:** with the placeholders still in place the program printed
`VP=0, PP=0` everywhere, and `VP` never moved even though `sbrk()` succeeded. After removing them,
`VP` jumps by exactly the 30 requested pages. And because `lazytest.c` no longer defines either
symbol, a missing syscall would fail to **link** instead of silently printing zeros.

### Checkpoint 2 answer box

* `[0, p->sz)` rounded up; excludes page tables, kernel stack, TRAMPOLINE/TRAPFRAME.
* Guard page: valid frame, `!PTE_U`; counted because we use `walk`, not `walkaddr`.
* Wiring table above; placeholders removed.
* Eager: `PP` +30 at `sbrk`, flat at touch; the "Success" line is a false positive.

---

## 4.4 Checkpoint 3 — page faults and the trap path

### The question

1. Add a diagnostic to `usertrap()` that prints the fault type, faulting VA and instruction address.
2. Run `fault read` / `fault write` on the eager kernel and interpret.
3. Trace the fault through the trampoline.

### 4.4.1 Reading a fault

| Register | Holds |
|---|---|
| `scause` | **why**: 12 = instruction page fault, 13 = load page fault, 15 = store/AMO page fault |
| `stval` | **the faulting virtual address** |
| `sepc` | **the address of the faulting instruction** |

```c
} else if(r_scause() == 13 || r_scause() == 15){
  uint64 va = r_stval();
  printf("usertrap(): %s page fault pid=%d va=0x%lx sepc=0x%lx\n",
         r_scause() == 13 ? "load" : "store", p->pid, va, r_sepc());
  setkilled(p);
}
```

Other traps keep their original handling; every faulting process is killed at this stage.

### 4.4.2 Fault test on the eager kernel

```
$ fault read
fault: pid 4, break 0x0000000000004000, target 0x0000000000004000, mode read
usertrap(): load page fault pid=4 va=0x4000 sepc=0xc2
$ fault write
fault: pid 5, break 0x0000000000004000, target 0x0000000000004000, mode write
usertrap(): store page fault pid=5 va=0x4000 sepc=0x94
```

`fault.c` does `sbrk(0)` to learn the break without growing it, then targets
`PGROUNDUP(break)`. With the break already page-aligned at `0x4000`, that is the **first byte of the
next, never-reserved page**.

* the printed target matches `stval` exactly;
* `sepc` (`0xc2`, `0x94`) is a *code* address, clearly different from `0x4000`;
* the fault is from the **data access** at `stval`, not from fetching at `sepc`.

`setkilled(p)` makes `usertrap()` call `exit(-1)`; the shell is a different process, so it prints the
next prompt. `fault: ERROR: access returned` is never reached.

> **ELI5.** `stval` is the address you *touched*. `sepc` is the line of code you *were on*. They are
> different numbers because the instruction is not stored at the address it reads.

### 4.4.3 The trampoline in four steps

1. CPU records `sepc`/`scause`/`stval`, enters supervisor mode, jumps to `stvec` — set by
   `usertrapret()` to `TRAMPOLINE + (uservec - trampoline)`.
2. `uservec` runs **with the user page table still active**: saves user registers into `TRAPFRAME`,
   loads `kernel_sp`, `kernel_satp`, `kernel_trap`, `kernel_hartid`, executes `sfence.vma`, and
   writes `satp` with the kernel page table.
3. Jumps to `usertrap()`, which reads `r_scause()`, `r_sepc()`, `r_stval()` and handles the fault.
4. `usertrapret()` → `userret`: switches `satp` back to the user table, restores registers, `sret`.

**Why `TRAMPOLINE` must be the same virtual address in both page tables:** the code performing the
`satp` switch is itself executing. The instant `satp` changes, the old mapping is gone — so the very
next instruction must still translate. Only a page mapped identically in both tables survives the
switch. `TRAPFRAME` sits one page below it, also fixed, so `uservec` can find the saved state
without knowing anything about this process.

### Checkpoint 3 answer box

* Load and store faults shown; `stval` (data address) ≠ `sepc` (instruction address).
* `fault` targets `PGROUNDUP(sbrk(0))`, which it never reserves → `stval` matches exactly.
* `uservec` (user table) → switch → `usertrap` → `userret` (switch back) → `sret`; both stubs live in
  the shared trampoline mapping.

---

## 4.5 Checkpoint 4 — allocate frames on demand

### The question

1. Make `sbrk()` reserve without allocating.
2. Handle a valid first access in `usertrap()`.
3. Make cleanup tolerate pages that were never touched.
4. Verify within one run: reserve, touch some, touch all, shrink, and a wild access.

### 4.5.1 Reserve the range

```c
int growproc(int n)
{
  uint64 sz;
  struct proc *p = myproc();

  sz = p->sz;
  if(n > 0){
    if(sz + n < sz || sz + n >= TRAMPOLINE)
      return -1;
    sz += n;
  } else if(n < 0){
    sz = uvmdealloc(p->pagetable, sz, sz + n);
  }
  p->sz = sz;
  return 0;
}
```

* `p->sz` still moves, so `sbrk(0)` and the returned old break stay correct.
* The wrap test `sz + n < sz` and the `TRAMPOLINE` ceiling keep the break away from the reserved trap
  mappings.
* No frame and not even a leaf PTE is created: the range is a **hole** that will fault on first
  access.

### 4.5.2 Handle a valid first access

```c
} else if(r_scause() == 13 || r_scause() == 15){
  uint64 va = r_stval();
  pte_t *pte = 0;
  int lazy = 0;

  if(va < p->sz && va < MAXVA){
    pte = walk(p->pagetable, va, 0);
    if(pte == 0 || (*pte & PTE_V) == 0)
      lazy = 1;
  }

  if(lazy){
    char *mem = kalloc();
    if(mem == 0){
      setkilled(p);
    } else {
      memset(mem, 0, PGSIZE);
      if(mappages(p->pagetable, PGROUNDDOWN(va), PGSIZE, (uint64)mem,
                  PTE_W|PTE_R|PTE_U) != 0){
        kfree(mem);
        setkilled(p);
      }
      // epc is NOT advanced: the faulting instruction is retried
    }
  } else {
    printf("usertrap(): %s page fault pid=%d va=0x%lx sepc=0x%lx\n",
           r_scause() == 13 ? "load" : "store", p->pid, va, r_sepc());
    setkilled(p);
  }
}
```

**The condition is a conjunction of three requirements.** Drop any one and the kernel is wrong:

| Requirement | What breaks if you drop it |
|---|---|
| `va < p->sz` | wild pointers anywhere get frames; `fault`'s target (`== p->sz`) would be repaired |
| no valid PTE | a **protection** fault (guard page: valid, `!PTE_U`) becomes a usable page, destroying the overflow check |
| `va < MAXVA` | an address above `MAXVA` reaches `walk()`, which panics |

**The three-way classification** — this is the checkpoint's real content:

| Fault address | PTE | Verdict |
|---|---|---|
| `< p->sz` | absent | lazy first touch → allocate, map, retry |
| `< p->sz` | valid, `!PTE_U` (guard page) | protection fault → kill |
| `>= p->sz` | anything | invalid access → kill |

`p->trapframe->epc` is **not** advanced, unlike the syscall path (`ecall` must not re-execute).
Not advancing it *is* the retry: `sret` returns to the same load/store, which now finds the page
mapped.

Error handling never leaks: `kalloc()` failure kills; `mappages()` failure `kfree()`s the fresh
frame and kills; `usertrap()` then exits, which unwinds through `uvmfree()` → `uvmunmap()` —
successfully, because holes are skipped.

### 4.5.3 Reclaim a partially allocated heap

```c
for(a = va; a < va + npages*PGSIZE; a += PGSIZE){
  if((pte = walk(pagetable, a, 0)) == 0)
    continue;                       // no intermediate page table at all
  if((*pte & PTE_V) == 0)
    continue;                       // reserved, never touched
  if(PTE_FLAGS(*pte) == PTE_V)
    panic("uvmunmap: not a leaf");  // RETAINED
  if(do_free) kfree((void*)PTE2PA(*pte));
  *pte = 0;
}
```

Both `uvmdealloc()` (shrink) and `uvmfree()` (exit) route through `uvmunmap()`, so both now tolerate
holes. `freewalk()` later releases the page-table pages that do exist.

The panic is **kept on purpose**: a valid entry with no `R/W/X` bits points to a page table, not a
frame, and unmapping it would be a kernel bug. Skipping that case would hide a real error.

### 4.5.4 Verification within one run

Full test:

```
Starting lazy allocation test...
Before: VP=4, PP=4
After sbrk(122880): VP=34, PP=4
Success: PP count unchanged (lazy allocation verified)
Touching pages...
After touching: PP=34
Success: PP count increased after touching pages
```

| Point | Expected | Measured |
|---|---|---|
| After reserving 30 pages | VP +30, PP unchanged | VP 4 → 34 (+30), PP 4 → 4 (0) |
| After touching all 30 | VP still 34, PP +30 | PP 4 → 34 (+30) |

The final increase is exactly 30, not "at least 30": no extra frames came from the test's own
`printf()` or loop bookkeeping.

**Partial touch** (loop temporarily reduced to one iteration, reservation unchanged):

```
After sbrk(122880): VP=34, PP=4
Touching pages...
After touching: PP=5
```

`PP` rises by exactly 1 and the process exits without a panic — the 29 untouched pages were skipped
by `uvmunmap()`.

**Negative `sbrk()`** (reserve 30, touch 1, then `sbrk(-122880)`):

```
After touching: PP=5
sbrk(-122880) returned 0x0000000000022000
After shrink: VP=4, PP=4
```

Old break returned, the one present heap frame freed, 29 holes skipped, no panic.

**`fault read` / `fault write` after lazy allocation:**

```
fault: pid 4, break 0x0000000000004000, target 0x0000000000004000, mode read
usertrap(): load page fault pid=4 va=0x4000 sepc=0xc2
fault: pid 5, break 0x0000000000004000, target 0x0000000000004000, mode write
usertrap(): store page fault pid=5 va=0x4000 sepc=0x94
```

Both still terminate. `fault` never calls a positive `sbrk()`, so its target equals `p->sz` and the
`va < p->sz` test fails. `lazytest`, by contrast, reserves the range first, so the same kind of
first-touch fault is repaired, retried, and execution continues. **This pair is the whole lab in two
runs.**

### 4.5.5 Limits of this solution (say this out loud — it earns marks)

Per the manual, this exercise covers user accesses to the heap and cleanup only:

* `uvmcopy()` still panics on an untouched page → `fork()` of a process with lazy holes is
  unsupported.
* `copyin()`/`copyout()` still use `walkaddr()` → a kernel copy to/from an untouched heap page fails
  instead of allocating.
* `lazytest` exercises neither path, so its success does not prove them.

The fixes would be: skip holes in `uvmcopy()` (the child inherits the same `p->sz` and faults pages
in lazily), and teach `copyin`/`copyout` to allocate for `va < p->sz`.

### Checkpoint 4 answer box

* `PP=4` right after `sbrk()`, `PP=34` only after touches → reservation ≠ allocation.
* Three-way classification: missing heap page vs protection fault vs outside the range.
* Instruction retried because `epc` is unchanged.
* Partially touched heap released without panic (partial-touch + shrink runs).
* Lazy saves memory because untouched reserved pages never get a data frame; `fork`, `copyin`/
  `copyout` and concurrent faults are out of scope.

---

## 4.6 Optional discussion — stack growth

Downward stack growth is the mirror image of lazy heap: the fault address is **below** the current
stack, not inside `[0, p->sz)`.

1. In `usertrap()`, treat the fault as legitimate growth only if `va` is within one page (or a small
   bounded distance) **below** the current stack base and its PTE is absent.
2. `kalloc()` + `memset()` + `mappages()` a new user page.
3. **Move the guard:** the old guard page becomes an ordinary user page, and the page below the new
   lowest page gets `uvmclear()`.
4. Cap growth so the stack cannot collide with the heap, and re-check that an overflow beyond the new
   limit still traps.

Step 3 is mandatory. Leaving the old guard `!PTE_U` makes the *newly grown* page unusable; removing
the guard entirely turns stack overflow into silent data corruption.

`exec()` currently lays out `USERSTACK + 1` pages with the lowest cleared, which is exactly the
layout this scheme would update.

> **ELI5.** You are allowed one more step down the stairs, but the "staff only" rope has to move down
> with you. If you leave the rope where it was, you cannot use the step you just gained. If you take
> the rope away, you can fall all the way down.

---

## 4.7 What was edited / added in Lab 4

### 4.7.1 File-by-file

| File | Status | Change |
|---|---|---|
| [kernel/syscall.h](./xv6-lab4/kernel/syscall.h) | **edited** | added `SYS_countvp 22`, `SYS_countpp 23` |
| [kernel/syscall.c](./xv6-lab4/kernel/syscall.c) | **edited** | `extern` declarations + two dispatch-table entries |
| [kernel/sysproc.c](./xv6-lab4/kernel/sysproc.c) | **edited** | added `sys_countvp()`, `sys_countpp()`; `sys_sbrk()` unchanged |
| [kernel/proc.c](./xv6-lab4/kernel/proc.c) | **edited** | `growproc()` reserves instead of calling `uvmalloc()` |
| [kernel/trap.c](./xv6-lab4/kernel/trap.c) | **edited** | page-fault branch: diagnostic + lazy first-touch repair |
| [kernel/vm.c](./xv6-lab4/kernel/vm.c) | **edited** | `uvmunmap()` skips holes; leaf panic retained |
| [user/usys.pl](./xv6-lab4/user/usys.pl) | **edited** | `entry("countvp")`, `entry("countpp")` |
| [user/lazytest.c](./xv6-lab4/user/lazytest.c) | **edited** | local `countvp`/`countpp` placeholders removed |
| [user/fault.c](./xv6-lab4/user/fault.c) | **added** | the supplied negative-control test |
| `Makefile` | **edited** | `$U/_lazytest`, `$U/_fault` in `UPROGS` |
| [user/usertests.c](./xv6-lab4/user/usertests.c) | untouched (lab logic) | see build note |

### 4.7.2 Wait — `user/fault.c` is a supplied file

Its header says so:

```c
// Supplied Lab 4 test. Install as user/fault.c and add $U/_fault to UPROGS.
// Run "fault read" or "fault write" in the xv6 shell.
```

It is part of the lab's starting material, not a solution. The lab work is the kernel side.

### 4.7.3 `growproc()` — before and after

```diff
   sz = p->sz;
   if(n > 0){
-    if((sz = uvmalloc(p->pagetable, sz, sz + n, PTE_W)) == 0) {
-      return -1;
-    }
+    // Reserve virtual space only; usertrap() installs a frame on the
+    // first access to each page. Reject growth that wraps or reaches
+    // the reserved trap mappings.
+    if(sz + n < sz || sz + n >= TRAMPOLINE)
+      return -1;
+    sz += n;
   } else if(n < 0){
     sz = uvmdealloc(p->pagetable, sz, sz + n);
   }
   p->sz = sz;
```

### 4.7.4 `uvmunmap()` — before and after

```diff
   for(a = va; a < va + npages*PGSIZE; a += PGSIZE){
+    // A lazily reserved page may never have been touched: it has no
+    // page table at all, or an invalid level-0 entry.
     if((pte = walk(pagetable, a, 0)) == 0)
-      panic("uvmunmap: walk");
+      continue;
     if((*pte & PTE_V) == 0)
-      panic("uvmunmap: not mapped");
+      continue;
     if(PTE_FLAGS(*pte) == PTE_V)
       panic("uvmunmap: not a leaf");
     if(do_free){
       uint64 pa = PTE2PA(*pte);
       kfree((void*)pa);
     }
     *pte = 0;
   }
```

Two `panic`s became `continue`; the third stayed. That asymmetry is the point: a hole is normal, a
non-leaf is a bug.

### 4.7.5 `usertrap()` — before and after

```diff
   } else if((which_dev = devintr()) != 0){
     // ok
+  } else if(r_scause() == 13 || r_scause() == 15){
+    // load or store page fault: stval is the faulting address,
+    // sepc the instruction that made the access.
+    uint64 va = r_stval();
+    pte_t *pte = 0;
+    int lazy = 0;
+
+    if(va < p->sz && va < MAXVA){
+      pte = walk(p->pagetable, va, 0);
+      // Only an absent page in the reserved range is a lazy first touch.
+      // A present but protected mapping (e.g. the stack guard page) is not.
+      if(pte == 0 || (*pte & PTE_V) == 0)
+        lazy = 1;
+    }
+
+    if(lazy){
+      char *mem = kalloc();
+      if(mem == 0){
+        setkilled(p);
+      } else {
+        memset(mem, 0, PGSIZE);
+        if(mappages(p->pagetable, PGROUNDDOWN(va), PGSIZE, (uint64)mem,
+                    PTE_W|PTE_R|PTE_U) != 0){
+          kfree(mem);
+          setkilled(p);
+        }
+        // epc is not advanced, so the faulting instruction is retried.
+      }
+    } else {
+      printf("usertrap(): %s page fault pid=%d va=0x%lx sepc=0x%lx\n",
+             r_scause() == 13 ? "load" : "store", p->pid, va, r_sepc());
+      setkilled(p);
+    }
   } else {
```

### 4.7.6 The counting syscalls — added

```diff
+// Number of virtual pages intersecting [0, p->sz): a partly used
+// final page still counts as one.
+uint64
+sys_countvp(void)
+{
+  return PGROUNDUP(myproc()->sz) / PGSIZE;
+}
+
+// Number of physical frames backing [0, p->sz). Includes the stack guard
+// page, whose PTE is valid but lacks PTE_U. Excludes page-table frames and
+// the TRAMPOLINE/TRAPFRAME mappings, which lie above p->sz.
+uint64
+sys_countpp(void)
+{
+  ...
+}
```

### 4.7.7 Build note

GCC 16 promotes `-Wunused-but-set-variable` and the tree uses `-Werror`, so an unused counter in
`user/usertests.c:fsfull()` blocked `make` on this host:

```
user/usertests.c:2347:7: error: variable 'fsblocks' set but not used [-Werror=unused-but-set-variable=]
```

Two recorded remedies exist:

* make the count observable: `printf("fsfull test finished, %d blocks\n", fsblocks);`
* remove the unused variable and its increment.

In the trees as they stand, `fsfull()` accumulates `total`, prints it, and compiles. **No lab logic
lives in `usertests.c`.**

---

## 4.8 Evidence (Lab 4)

### 4.8.1 Full lazy run

```
Starting lazy allocation test...
Before: VP=4, PP=4
After sbrk(122880): VP=34, PP=4
Success: PP count unchanged (lazy allocation verified)
Touching pages...
After touching: PP=34
Success: PP count increased after touching pages
```

### 4.8.2 Regression checks

`usertests` cases touching memory management, run individually under the lazy kernel:

| Test | Result | Relevant diagnostic |
|---|---|---|
| `stacktest` | `ALL TESTS PASSED` | guard page `load page fault va=0xfe90` → child killed, no allocation |
| `sbrkbasic` | `ALL TESTS PASSED` | — |
| `sbrkmuch` | `ALL TESTS PASSED` | — |
| `sbrkbugs` | `ALL TESTS PASSED` | expected `scause 0xc` from the test's own bad jumps |
| `nowrite` | `ALL TESTS PASSED` | store faults on `0x0`, `0x80000000`, `0x3fffffe000`, … all rejected |
| `sbrk8000` | `ALL TESTS PASSED` | — |

`stacktest` is the important one: the guard page still faults and still kills, so Part 4 did not
accidentally turn protection faults into allocations.

### 4.8.3 Environment

QEMU 11.1.1, `riscv64-elf-gcc` 16.2.0, `make CPUS=3 qemu`.

---

## 5. Traps that cost marks

### Lab 3

| Trap | Correct version |
|---|---|
| "A kernel syscall is atomic, so the two counter calls are safe." | Atomicity is per-syscall; the invariant spans **two** calls. |
| "`sem_wait` should be an `if`." | `wakeup` reserves nothing and wakes everyone → must be a `while`. |
| "Signal first, then wake." | Increment and `wakeup` under the **same** lock, or a waiter can miss it. |
| "Take the mutex, then wait for `empty`." | Deadlock. Wait for the resource first. |
| "`wait()` isn't needed before the final read." | You may read a partial total — and must not free while users remain. |
| "`seminit` creates a semaphore." | It only initialises the table at boot; `sem_alloc` allocates. |
| "`sleep(5)` in user land means 5 seconds." | `sleep(int)` takes **clock ticks**. |
| "Disabling interrupts gives mutual exclusion." | It only affects **this** hart. |
| "One unprotected run gave 2000, so it's race-free." | Races are nondeterministic; absence of a failure is not absence of the bug. |

### Lab 4

| Trap | Correct version |
|---|---|
| "`walk()` allocates frames, so lazy allocation still allocates on `sbrk`." | `walk(alloc=1)` allocates **page-table pages** only; data frames come from `uvmalloc`'s `kalloc`. |
| "`walk()` returned non-NULL, so the page is mapped." | Level 0 is returned unchecked; test `*pte & PTE_V` yourself. |
| "Use `walkaddr()` to count frames." | It rejects `!PTE_U`, so the guard page is missed. Use `walk(...,0)`. |
| "The guard page has no frame." | It has one; only `PTE_U` is cleared. It is counted, and later freed. |
| "`countvp` should count non-zero pages." | It counts **whole virtual pages** in `[0, p->sz)`, hence `PGROUNDUP`. |
| "`sbrk(n)` returns the new break." | It returns the **old** break (the start of the new region). |
| "`PP` went up, so lazy allocation works." | Check **when**: at `sbrk` (eager) or at touch (lazy). `lazytest`'s last line proves neither. |
| "`stval` is the instruction address." | `stval` is the **data** address for faults 13/15; `sepc` is the instruction. |
| "`scause == 13` is an instruction fault." | 12 = instruction, 13 = load, 15 = store/AMO. |
| "The handler must increment `epc` to retry." | Not incrementing `epc` *is* the retry. Only the syscall path does `epc += 4`. |
| "Any fault below `p->sz` should be repaired." | Only if no valid PTE — otherwise a guard-page protection fault becomes an allocation. |
| "`uvmunmap` should skip non-leaf entries too." | No: `PTE_FLAGS == PTE_V` on a valid entry means a page table — keep the panic. |
| "`fork()` works because `lazytest` passes." | `uvmcopy()` still panics on holes; `lazytest` never forks. |
| "Lazy allocation makes `sbrk` free." | It makes it cheap; frames are still allocated on touch, and `kalloc` failure must be handled. |

---

## 6. Self-check questions with answers

**Q1. Trace `0x4000` through Sv39. Which index selects the root table, and what does `walk()` return
for it in a process whose `p->sz` is `0x4000`?**

`0x4000` = bit 14 set. Fields: offset `0x000`, L0 index `0x4`, L1 index `0x0`, L2 index `0x0`. The
root (level-2) index is therefore **0**. `walk(alloc=0)` descends level 2 entry 0 and level 1 entry 0
(both page tables exist, because lower addresses are mapped), then returns
`&level0_table[PX(0, va)] = &level0_table[4]` — the address of an entry whose `PTE_V` is **0**,
because page `0x4000` was never mapped. `walk()` returning non-NULL here means "the slot exists", not
"a frame exists".

**Q2. Why does `countpp()` use `alloc = 0`? What would change with `alloc = 1`?**

`alloc = 0` makes the query side-effect-free: no page-table pages are created just by counting, so
`countvp`/`countpp` cannot change the thing they measure. With `alloc = 1`, counting a 30-page range
could allocate up to one page-table page per 2 MiB region, consume memory, could fail under memory
pressure, and would mutate the address space from a read-only-looking syscall. It would still not
count data frames — the counter only increments on leaf entries.

**Q3. A process has `p->sz = 4096`. How many virtual pages does `countvp()` report, and how many
frames does `countpp()` report if nothing is mapped yet? What if the range is the freshly `exec`'d
image?**

`countvp = PGROUNDUP(4096)/4096 = 1`. With nothing mapped, `countpp = 0` (no valid leaf PTE). For a
freshly `exec`'d process the observed layout is 4 pages — 2 program pages + 1 guard page + 1 user
stack page (`USERSTACK` is 1) — and every one is backed, so `countvp = countpp = 4`.

**Q4. Give the exact condition under which the page-fault handler allocates a frame, and name the
two other cases it must reject.**

Allocate only when **all** hold: `r_scause()` is 13 or 15; `va < p->sz`; `va < MAXVA`; and
`walk(p->pagetable, va, 0)` returns `0` or an entry with `PTE_V == 0`.
Reject: (a) a **present** mapping — e.g. the guard page, valid but `!PTE_U` — which is a protection
fault; (b) any `va >= p->sz`, which is an invalid access (this is what `fault` triggers).

**Q5. Why must `TRAMPOLINE` be mapped at the same virtual address in both page tables?**

Because `uservec`/`userret` switch `satp` while executing there. The instruction immediately after
the `satp` write must translate under the **new** table, so the code's own virtual address must be
valid in both. `TRAPFRAME` is likewise fixed, one page below, so `uservec` can locate the saved
registers without depending on the current process.

**Q6. After removing `uvmalloc()` from `growproc()`, which three call sites would panic or fail on a
hole, and what is the minimal change for each?**

1. `uvmunmap()` — reached from `uvmdealloc()` (shrink) and `uvmfree()` (exit): make the two hole
   cases `continue` instead of `panic` (done).
2. `uvmcopy()` — reached from `fork()`: skip pages whose PTE is absent instead of panicking (the
   child inherits `p->sz` and faults them in).
3. `walkaddr()` — reached from `copyin`/`copyout`/`copyinstr`: allocate for `va < p->sz` (or have
   those copies tolerate a fault) instead of returning 0.

**Q7. `fault write` and `lazytest` both cause store page faults at `0x4000`. Why does one terminate
the process and the other continue?**

`lazytest` first calls `sbrk(30 * 4096)`, so `0x4000` lies **inside** `p->sz` and the PTE is absent —
a lazy first touch. The handler allocates, maps, and returns without advancing `epc`, so the store is
retried and succeeds. `fault` only calls `sbrk(0)`, so its target **equals** `p->sz`; the
`va < p->sz` test fails, the diagnostic prints, and `setkilled()` terminates the process.

---

## 7. One-page revision card

### Lab 3

```
acquire:  push_off(); amoswap(locked,1); fence        ← atomic, per-CPU interrupts irrelevant
sleep:    acquire(p->lock) THEN release(lk)           ← ordering prevents lost wakeup
          state=SLEEPING; sched(); ...; acquire(lk)
wakeup:   scan all NPROC, mark SLEEPING+RUNNABLE      ← reserves nothing, wakes ALL
sem_wait: lock; while(value==0) sleep(sem,&sem->lock); value--; unlock
sem_sig:  lock; value++; wakeup(sem); unlock
counter:  sem_wait; get; set(+1); sem_signal          ← mutex across BOTH syscalls
buffer:   empty=16, filled=0, mutex=1
          wait(empty) BEFORE wait(mutex)              ← else deadlock
          mutex held across ubuf_write/read incl. yield()
```

### Lab 4

```
Sv39:     9 | 9 | 9 | 12   (MAXVA = 1<<38; bits 63-39 zero)
PTE:      PPN | flags: V R W X U
non-leaf: PTE_FLAGS == PTE_V   (V only) → page table, not a frame
walk:     descends 2→1, returns &l0[PX(0,va)] UNCHECKED
walkaddr: walk + reject !PTE_V and !PTE_U   (kills guard page)

eager:  sbrk → growproc → uvmalloc → kalloc+memset+mappages
lazy:   sbrk → p->sz only          (hole)
fault:  alloc if  va < p->sz  AND no valid PTE   → kalloc, memset, mappages, retry (epc untouched)
reject: present-but-protected (guard) | va >= p->sz | va >= MAXVA
cleanup: uvmunmap skips holes, keeps non-leaf panic
counts:  VP = PGROUNDUP(sz)/PGSIZE   PP = valid leaf PTEs in [0,sz)
reserve: VP +30 immediately; PP +30 only on touch
```

### The three-way fault table (memorise)

| `va` | PTE | Verdict |
|---|---|---|
| `< p->sz` | absent | allocate + retry |
| `< p->sz` | valid, `!PTE_U` | protection fault → kill |
| `>= p->sz` | anything | invalid → kill |

### The one comparison that ties both labs together

| Lab 3 | Lab 4 |
|---|---|
| check condition → act, must be one step | reserve address → back it, must be one step |
| `amoswap`, or test+decrement under a lock | fault handler repairs, then instruction retries |
| hazard: interleaving | hazard: stale assumption "reserved ⇒ mapped" |

---

## 8. Change log for this guide

This file is **new**. Nothing was deleted or modified; it consolidates four existing documents.

| Change | Detail |
|---|---|
| **Added** [SC2005_Lab3_4_Combined_Guide.md](./SC2005_Lab3_4_Combined_Guide.md) | Single study guide covering both labs: all checkpoint questions and answers, ELI5 explanations, background theory, code changes with diffs, run evidence, traps, and self-check answers. |
| Merged from [LAB3_ANSWERS.md](./xv6zz-lab3/LAB3_ANSWERS.md) | Lab 3 checkpoint answers, verified run output, build-blocker note, file-change table. |
| Merged from [Lab 3 STUDY_NOTES.md](./xv6zz-lab3/STUDY_NOTES.md) | The one-idea framing, the `while`-vs-`if` reasoning, deadlock argument, exam traps. |
| Merged from [LAB4_ANSWERS.md](./xv6-lab4/LAB4_ANSWERS.md) | Lab 4 checkpoint answers, eager/lazy run output, partial-touch and shrink evidence, regression table. |
| Merged from [Lab 4 STUDY_NOTES.md](./xv6-lab4/STUDY_NOTES.md) | Sv39/PTE/`walk` background, three-way fault classification, limits, stack-growth discussion, self-check questions. |
| New material in this guide | ELI5 sections for both labs, the vocabulary decoder, the "one question, two labs" comparison, the combined trap table, answers to every self-check question, and the one-page revision card. |
| **Unchanged** | `xv6zz-lab3/**` and `xv6-lab4/**` source and the four source documents above. |

### Where things live

```
sc2005/
├── SC2005_Lab3_4_Combined_Guide.md   ← this file
├── xv6zz-lab3/
│   ├── LAB3_ANSWERS.md
│   ├── STUDY_NOTES.md
│   ├── kernel/semaphore.c            ← implemented
│   └── user/race_test.c              ← semaphore discipline
└── xv6-lab4/
    ├── LAB4_ANSWERS.md
    ├── STUDY_NOTES.md
    ├── kernel/{proc,trap,vm,sysproc,syscall}.c, syscall.h   ← lazy allocation
    └── user/{lazytest,fault,usys.pl}
```

---

### References

* Russ Cox, Frans Kaashoek, Robert Morris, *xv6: a simple, Unix-like teaching operating system* —
  §6 (locking), §7.5–7.7 (sleep/wakeup, semaphores), §3.3–3.6 (page tables, `sbrk`, page faults).
* SC2005 xv6 fork: <https://github.com/CPS-research-group/ntu-sc2005-xv6> (`lab3`, `lab4` branches).
