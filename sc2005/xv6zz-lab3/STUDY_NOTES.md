# SC2005 Lab 3 — Revision Notes

Study material for the Lab 3 checkpoints. Command output and evidence live in
[LAB3_ANSWERS.md](./LAB3_ANSWERS.md); this file is the *learning*: the concepts, the "why", and
the traps. Everything here is answerable without the lab in front of you.

---

## The lab in one paragraph

Two processes share kernel objects (a counter, a circular buffer). *Entering the kernel does not
make a sequence of operations atomic*, so any check-then-act on shared state can be interleaved.
You build one primitive — a **blocking semaphore** — out of two things xv6 already has: a
**spinlock** (for the short protected update) and **`sleep`/`wakeup`** (for the wait). Then you use
it twice: as a **mutex** to make a read-modify-write indivisible, and as **counting semaphores +
a mutex** to coordinate producers and a consumer.

---

## The single idea behind everything in this lab

> **A check and the action that depends on it must happen as one indivisible step.**

It shows up four times, at four different levels, and every one of them is the *same* bug:

| Level | The check | The action | How xv6 makes it one step |
|---|---|---|---|
| Lock acquisition | `locked == 0`? | `locked = 1` | `amoswap` (`__sync_lock_test_and_set`) — one instruction |
| Semaphore wait | `value > 0`? | `value--` | both under the semaphore's `lock` |
| Counter increment | read `ucnt[0]` | write `ucnt[0]+1` | both inside one `sem_wait`/`sem_signal` pair *in user space* |
| Sleep/wakeup | is the condition true? | go to sleep | `p->lock` taken **before** the condition lock is released |

If you internalise only this, you can re-derive the whole lab.

---

## Checkpoint 1 — Synchronization mechanisms

### 1.1 Why lock acquisition must be atomic

**What it asks.** Where is the lock state, what is the atomic operation, what interrupts are doing —
and why is disabling interrupts *not* enough?

**The answers.**

* Lock state is the `locked` field, [kernel/spinlock.h:3](./kernel/spinlock.h:3).
* The atomic operation is `__sync_lock_test_and_set(&lk->locked, 1)`
  ([kernel/spinlock.c:32](./kernel/spinlock.c:32)) — on RISC-V a single `amoswap.w.aq`, i.e. an
  indivisible read-and-write.
* Interrupt handling is `push_off()` / `pop_off()` ([kernel/spinlock.c:24](./kernel/spinlock.c:24),
  [kernel/spinlock.c:89](./kernel/spinlock.c:89)), which clear and restore this hart's interrupt
  enable bit.

**Why interrupts-off is not enough.** `push_off()` changes a bit in **this CPU's** `sstatus`. It
stops this CPU from being interrupted — it does nothing to another hart, which has its own
`sstatus` and is executing the same instructions on the same memory. Mutual exclusion between CPUs
must come from the *memory operation*, not from the interrupt flag.

**The interleaving that breaks a read-then-write lock.** With "check `locked`, then set it to 1" as
two operations and a free lock:

```
CPU A: read locked -> 0
CPU B: read locked -> 0        <- both saw "free"
CPU A: write locked = 1
CPU B: write locked = 1
CPU A: enters CS
CPU B: enters CS               <- two processes in the critical section
```

`amoswap` closes the window because the *read* and the *write* are one indivisible operation:
exactly one hart can observe `0`; every other hart's swap returns `1` and spins.

**Why interrupts-off is still needed.** Not for mutual exclusion — for **deadlock avoidance**. If a
CPU took a timer interrupt while holding a spinlock, the handler could try to acquire the same lock
(or the scheduler could switch to a process that wants it) and spin forever on a lock that can only
be released by the code it just interrupted.

**Don't forget the fences.** `__sync_synchronize()` after acquiring
([kernel/spinlock.c:39](./kernel/spinlock.c:39)) and before releasing
([kernel/spinlock.c:60](./kernel/spinlock.c:60)) stop the compiler/CPU from moving critical-section
memory accesses *outside* the locked region.

### 1.2 The two lock roles in `sleep`/`wakeup`

**What it asks.** Where the condition lock and each process lock are held/released; why that order
prevents a lost wakeup; what the state transitions are; and why the waiter rechecks.

**The two locks.**

* `lk` — the **condition lock**. Protects the shared data whose condition the caller tests.
* `p->lock` — the **process lock**. Protects `p->state` and `p->chan`, and is the lock the scheduler
  itself requires (`sched()` panics unless it is held).

`chan` is only an **identifying tag** — a value written to `p->chan` and compared in `wakeup()`. No
data travels through it.

**The order that prevents a lost wakeup** ([kernel/proc.c:550](./kernel/proc.c:550)):

```
caller holds lk
  sleep():
    acquire(&p->lock)     <-- take p->lock FIRST
    release(lk)           <-- only then drop lk
    p->chan = chan
    p->state = SLEEPING   <-- state change made under p->lock
    sched()               <-- hands p->lock to the scheduler
    ...
    release(&p->lock)
    acquire(lk)           <-- returns with lk held, exactly as passed in
```

The waker must hold the **same** `lk` while changing the condition and calling `wakeup()`. So when
the waker holds `lk`, the waiter is in one of only two places:

1. **It has not yet tested the condition** — it will acquire `lk` after the waker finishes, see the
   updated condition, and not sleep at all; or
2. **It has already stored `SLEEPING`** — and `wakeup()` inspects `p->state` under the *same*
   `p->lock` that protected that store, so it is guaranteed to see it and flip it to `RUNNABLE`.

There is no third possibility, so the wakeup cannot fall between the check and the sleep. The key
mechanical detail is **`p->lock` is acquired before `lk` is released**.

**State transitions.** `RUNNING → SLEEPING` in `sleep()` ([kernel/proc.c:566](./kernel/proc.c:566));
`SLEEPING → RUNNABLE` in `wakeup()` ([kernel/proc.c:589](./kernel/proc.c:589));
`RUNNABLE → RUNNING` when `scheduler()` picks it ([kernel/proc.c:467](./kernel/proc.c:467)).

**Why the waiter must recheck.** `wakeup()` is **not a hand-off**:

* it does not run the waiter immediately, only marks it `RUNNABLE`;
* it does not reserve the resource;
* it wakes **every** process sleeping on that channel — so with two waiters and one unit of
  resource, both wake and only one can proceed.

Between "marked RUNNABLE" and "actually running", another process can consume the resource. Hence
the condition is re-tested in a **`while` loop**, with `lk` held, on every wake-up. An `if` would let
a loser fall through and consume a resource that is not there.

### 1.3 Spin vs sleep

**What it asks.** 10 cycles vs 10,000 cycles — which is cheaper, and under what assumptions?

**What "sleeping" actually costs.** Not just one switch: `acquire(&p->lock)`, `release(lk)`, a state
change, `sched()`, a `swtch()` out, the scheduler loop, a later `swtch()` back in — **plus** the
waker's `wakeup()`, which scans all `NPROC` process slots taking each `p->lock`. That is hundreds to
a few thousand cycles. Spinning costs a few cycles per attempt, but burns a whole CPU.

| Wait length | Cheaper | Why |
|---|---|---|
| ~10 cycles | **spin** | shorter than even a single `swtch()`, never mind two switches + a `wakeup()` scan |
| ~10,000 cycles | **sleep** | thinking of total system cycles; the spinning CPU could be running the process that releases the resource |

**Assumptions you must state.**

1. The holder can actually run — another CPU, or scheduling while we sleep. On a uniprocessor with
   the holder descheduled and interrupts off, spinning **deadlocks**; sleeping is the only option.
2. "Cheaper" means total system cycles, not this process's latency — sleeping adds wake-up latency,
   so a latency-critical short wait may still prefer spinning.
3. 10 and 10,000 are illustrative magnitudes, **not** measured xv6 thresholds. The crossover is
   roughly "the wait exceeds ≈ two context switches plus a `wakeup()` scan".

**Why xv6's spinlocks hold for very short regions.** They are held with interrupts off, so a holder
can never be preempted; spinning for a few hundred cycles is safe and cheap. Sleeping inside a
spinlock would be a bug.

---

## Checkpoint 2 — The blocking semaphore

### The three different "init"s (exam favourite)

| Name | Where | What it really is |
|---|---|---|
| `sem_init(value)` | [user/user.h:38](./user/user.h:38) | a **syscall**: `SYS_sem_init` → `sys_sem_init()` ([kernel/sysproc.c:123](./kernel/sysproc.c:123)) → `sem_alloc(value)` |
| `sem_alloc(value)` | [kernel/semaphore.c:31](./kernel/semaphore.c:31) | the **allocator**: takes `sem_table_lock`, finds a free slot, marks `in_use`, stores the initial value, returns the index or `-1` |
| `seminit()` | [kernel/semaphore.c:21](./kernel/semaphore.c:21) | **boot-time** setup only, called once from `main()` ([kernel/main.c:31](./kernel/main.c:31)); initialises the locks and marks every slot free. Returns nothing, hands out nothing. |

A semaphore is **initialised at boot** but **allocated on demand**, and `semid` is just an index
into `semaphores[]`.

### What the implementation must do

```c
sem_wait:   acquire(&sem->lock);  while(sem->value == 0) sleep(sem, &sem->lock);
            sem->value--;  release(&sem->lock);
sem_signal: acquire(&sem->lock);  sem->value++;  wakeup(sem);  release(&sem->lock);
sem_getvalue: read sem->value under sem->lock (so you get a consistent snapshot, not a torn read)
```

* **Lock** = that semaphore's own `sem->lock` (its condition lock).
* **Channel** = the address of the `struct semaphore` itself. Distinct per semaphore, so signalling
  semaphore 3 can never wake a waiter on semaphore 5.

### Why `while`, not `if`

Two reasons, both consequences of `wakeup()` not reserving anything:

1. **Multiple waiters, one signal.** `wakeup()` wakes *all* sleepers on the channel. With two waiters
   and `value == 1`, both wake; the loser re-tests, sees `0`, and sleeps again. With `if`, the loser
   falls through and decrements to `-1`.
2. **Spurious-looking wakeups.** Even a single waiter can be woken and find the resource already gone.

`value` must stay **non-negative** — that is the definition of the semaphore in this lab, and it is
precisely what the `while` loop guarantees.

### What `sem_basic` does *not* prove

It checks the sequence `1 → 0 → 1` and that `sem_free` succeeds. Because it never calls `sem_wait`
on a **zero** value, it never executes `sleep()`, `wakeup()`, the recheck loop, or `sched()` — the
entire blocking path is untested, and it is single-threaded so there is no contention. (Part 4 does
exercise blocking: the consumer's first `sem_wait(b.filled)` must sleep because `filled` starts at 0.)

**Lesson: a passing test only proves what it actually exercises.**

### When is it safe to free a semaphore?

`sem_free()` only clears `in_use` — it **neither wakes nor waits** for users. So it is safe only when
no process can still call `sem_wait`/`sem_signal` on that id:

* `race_test()` — after `wait(0)` has reaped the child.
* `producer_consumer()` — after the consumer has read everything **and** both producers are reaped.

Freeing earlier is dangerous: the slot can be reallocated to an unrelated semaphore, and a process
still sleeping on the old channel would be woken by — or decrement — the new one.

---

## Checkpoint 3 — Protecting the shared counter

### The lost update

`ucnt_get()`/`ucnt_set()` are an ordinary load and store ([kernel/ucnt.c:13](./kernel/ucnt.c:13)).
The increment is **two syscalls**:

```c
int val = ucnt_get(0);      // syscall: kernel reads ucnt[0]
ucnt_set(0, val + 1);       // syscall: kernel writes ucnt[0]
```

**Entering the kernel does not make the pair atomic.** Each syscall is atomic in the sense that one
instruction sequence runs in the kernel; between the two, the process returns to user space and can
be preempted, and on `CPUS=3` the other process can be doing the same thing on another hart.

Interleaving from a counter of 100:

```
parent: val = get()  -> 100
child:  val = get()  -> 100      <- both read the same value
parent: set(101)
child:  set(101)                 <- one increment vanishes
```

Two increments happened; the counter moved by one.

### Why protecting the two syscalls *separately* is not enough

This is the conceptual heart of Part 3. The invariant is not "a syscall must not be interrupted" —
it is:

> **the value I read must still be the value I write.**

That invariant spans **both** calls. Locking inside each syscall (which is effectively already true —
each runs in the kernel) leaves the gap *between* them wide open, and the interleaving above lives
exactly in that gap. So the lock must be held across the **pair**, which means it must be taken in
**user space** around the pair.

### The fix

```c
void do_work(int pid, int semid) {
    for (int i = 0; i < N; i++) {
        sem_wait(semid);          // enter
        int val = ucnt_get(0);
        ucnt_set(0, val + 1);
        sem_signal(semid);        // leave
    }
}
```
with `sem_init(1)` — **initial count 1** is what makes it a *mutex* (first wait succeeds 1 → 0,
everyone else blocks until the holder signals 0 → 1).

### Why the child's copied `semid` is the same semaphore

`fork()` copies the process's **user memory**, so the child gets a copy of the variable `semid`. But
`semid` is only an **index** into the kernel's `semaphores[]`, which lives in kernel memory and is
**not** copied by `fork()`. Both processes therefore name the same kernel object — which is exactly
why the protection works across the fork. (Contrast: a *copy* of the semaphore would not help at all.)

### Why the parent waits first

`wait(0)` blocks until the child has exited, so when the parent reads the final counter all 1000 of
the child's increments have completed — otherwise it could read a partially complete total and fail
spuriously. The same `wait(0)` is what makes the later `sem_free()` safe.

**Expected result: `2 * N = 2000`.** One unprotected run giving 2000 proves nothing — races are
nondeterministic.

---

## Checkpoint 4 — Producers, consumer, and progress

### The three semaphores and where their counts come from

| Semaphore | Initial | Derived from | Role |
|---|---|---|---|
| `empty` | **16** | buffer starts empty → all `UBUF_SIZE` slots free | counts **space**; producer waits, consumer signals |
| `filled` | **0** | buffer starts empty → no data | counts **data**; consumer waits, producer signals |
| `mutex` | **1** | unlocked | binary; protects the shared `head`/`tail`/`data` |

```c
producer:  sem_wait(empty); sem_wait(mutex); ubuf_write(c); sem_signal(mutex); sem_signal(filled);
consumer:  sem_wait(filled); sem_wait(mutex); tmp = ubuf_read(); sem_signal(mutex); sem_signal(empty);
```

### The ordering rule (and the deadlock if you break it)

**Wait for space/data *before* taking the mutex.**

Suppose a producer held `mutex` and *then* blocked on `empty`. A free slot is only ever created by
the consumer calling `sem_signal(empty)`, and the consumer can only reach that after `ubuf_read()`,
which it can only reach after `sem_wait(mutex)` — which is held by the blocked producer, forever.

That is a **circular wait**: producer holds `mutex`, wants `empty`; consumer wants `mutex`, which is
the prerequisite for producing `empty`. Classic deadlock. Waiting for the resource count first, while
holding no lock, breaks the cycle. (This is the general rule: **never hold a lock while waiting for a
resource that requires that lock to free.**)

### Why slot counts alone do not protect the buffer

A counting semaphore enforces **how many** processes may be inside — not **who may not overlap with
whom** on the shared indices.

`head`/`tail` are shared mutable state, and `ubuf_write`/`ubuf_read` deliberately `yield()` *between*
the payload access and the index update to widen the window. With only `empty`/`filled`:

* two producers can both pass `sem_wait(empty)` and both land on `ubuf.data[ubuf.tail] = val` with
  the **same** `tail` → one byte silently overwritten;
* two readers can both read the same slot under one `filled` token → a duplicated byte;
* a reader can read `data[head]` while a writer is midway through.

`mutex` is held across the **whole** buffer function — including past the `yield()` — which is what
makes the payload access and the index advance one indivisible step. **Condition counts and mutual
exclusion are different jobs; you need both.**

### Completion and cleanup

The consumer runs in the parent; after it returns, the parent `wait(0)`s twice to reap both
producers, and only then frees the semaphores. The invariant to state: **total
`sem_signal(filled)` == total `sem_wait(filled)` == 96** (48 chars × 2 producers).

### What the test does *not* prove

```c
T_ASSERT(valid[(unsigned char)tmp]);
```

This only checks that each received byte is **one of** the characters in `msg`. It does not count
occurrences, does not check order, and cannot detect a byte that is duplicated, lost or reordered —
as long as the byte that arrives is in the set.

So a pass establishes: *no corrupted/foreign byte appeared* and *the run completed without
deadlock*. The stronger correctness argument comes from the **design** (counts + mutex), not from the
test. Being able to say this is the point of the checkpoint.

---

## Traps that cost marks

| Trap | Correct version |
|---|---|
| "A kernel syscall is atomic, so the two counter calls are safe." | Atomicity is per-syscall; the invariant spans **two** calls. |
| "`sem_wait` should be an `if`." | `wakeup` reserves nothing and wakes everyone → must be a `while`. |
| "Signal first, then wake." | Increment and `wakeup` must be under the **same** lock, or a waiter can miss it. |
| "Take the mutex, then wait for `empty`." | Deadlock. Wait for the resource first. |
| "`wait()` isn't needed before the final read." | Without it you may read a partial total — and you must not `sem_free` while users remain. |
| "`seminit` creates a semaphore." | It only initialises the table at boot; `sem_alloc` allocates. |
| "`sleep(5)` in user land means 5 seconds." | `sleep(int)` takes **clock ticks**. |
| "Disabling interrupts gives mutual exclusion." | It only affects **this** hart. |
| "One unprotected run gave 2000, so it's race-free." | Races are nondeterministic; absence of a failure is not absence of the bug. |

---

## Cross-lab connections

* **Lab 2** asked *which* process runs next. **Lab 3** is what a process does when it must **not**
  run — `sleep()` is a scheduling operation, and `wakeup()` is a scheduling decision in disguise.
* The `RUNNABLE` state in Lab 2 is exactly what `wakeup()` produces; `SLEEPING` is what `sleep()`
  produces. `swtch()` appears in both labs as the mechanism behind "stop running here".
* **Lab 4**'s focus on files builds on the same idea that a *sequence* of operations, not a single
  operation, is what needs protecting.
