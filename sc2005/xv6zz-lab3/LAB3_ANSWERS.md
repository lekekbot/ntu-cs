# SC2005 Lab 3 — Synchronization and Semaphores

Answers, reasoning, and evidence. Branch: `lab3` (commit `269bf05`). All runs use `make CPUS=3 qemu`.

---

## Checkpoint 0 — Orient yourself before editing

| Item | Status |
|---|---|
| Branch | `git checkout lab3` → `git branch --show-current` prints `lab3` |
| Three-CPU boot | `make CPUS=3 qemu` prints `hart 2 starting` / `hart 1 starting` |
| Files located | [kernel/spinlock.c](./kernel/spinlock.c), [kernel/spinlock.h](./kernel/spinlock.h), [kernel/proc.c](./kernel/proc.c), [kernel/semaphore.c](./kernel/semaphore.c), [kernel/ucnt.c](./kernel/ucnt.c), [kernel/ubuf.c](./kernel/ubuf.c), [user/race_test.c](./user/race_test.c) |
| Selecting one test | Comment out the other two calls in `main()` and the `ALL TESTS PASSED` print, keeping `exit(0)` |

One pre-existing blocker had to be fixed before anything could run (see [Appendix B](#appendix-b--build-blocker-in-usertestsc)).

---

## Part 1 — Spinlocks and sleep/wakeup

### 1.1 Why lock acquisition must be atomic, and why `intr_off()` is not enough

In [kernel/spinlock.h](./kernel/spinlock.h) the lock state is the field `locked` (`uint locked;`). In
[kernel/spinlock.c](./kernel/spinlock.c) `acquire()` is:

```c
push_off();                      // disable interrupts to avoid deadlock      (line 24)
while(__sync_lock_test_and_set(&lk->locked, 1) != 0)                          // line 32
  ;
__sync_synchronize();                                                         // line 39
```

`push_off()` only clears the interrupt-enable bit **of this hart** (via `intr_off()` → `sstatus`/`sie`).
It is a *local* action: it stops this CPU from taking a timer interrupt and switching away in the middle
of the critical section. It does nothing whatsoever to another hart, which is executing the same
instructions on the same memory. On a three-CPU (`CPUS=3`) machine another hart can be sitting in
`acquire()` at the same instant. So interrupts-off gives you *no* mutual exclusion between CPUs; it only
protects against the local timer/preemption deadlock.

Now suppose acquisition were written as two separate operations — "read `locked`, then write 1":

```c
if (lk->locked == 0)      // step R
    lk->locked = 1;       // step W
```

with the lock initially free, two CPUs can interleave:

| Time | CPU A | CPU B | `locked` |
|---|---|---|---|
| t1 | reads `locked` → 0 (R) | | 0 |
| t2 | | reads `locked` → 0 (R) | 0 |
| t3 | writes `locked` = 1 (W) | | 1 |
| t4 | | writes `locked` = 1 (W) | 1 |
| t5 | enters critical section | enters critical section | 1 |

Both CPUs observed `locked == 0` and both therefore believe they hold the lock, so both enter the
critical section at once. Interrupts-off on either CPU does not change this, because the interleaving
happens *between two CPUs*, not between a CPU and its own interrupt handler.

`__sync_lock_test_and_set(&lk->locked, 1)` removes the window because the read and the write are a
single indivisible operation. On RISC-V it compiles to an atomic swap (the comment at
[kernel/spinlock.c:31](./kernel/spinlock.c:31) shows `amoswap.w.aq a5, a5, (s1)`). Whichever hart
executes `amoswap` first sees the old value `0` and wins; every other hart's `amoswap` sees `1` and
keeps spinning in the `while` loop. Exactly one CPU can ever observe `0`.

Two more details matter:

* `__sync_synchronize()` after the loop is a fence. Without it the compiler or the processor could move
  a load or store of the critical section *above* the acquisition point, so the protected data would be
  accessed before the lock was actually held.
* `release()` mirrors this: `__sync_synchronize()` then `__sync_lock_release()` (an atomic
  `amoswap.w zero, zero, ...`), so every store inside the critical section is visible to the next
  holder before the lock is observed as free.

### 1.2 The two lock roles in `sleep()` / `wakeup()`

Declarations: `void sleep(void*, struct spinlock*)` and `void wakeup(void*)` in
[kernel/defs.h:104](./kernel/defs.h:104). Bodies: [kernel/proc.c:550](./kernel/proc.c:550) (`sleep`)
and [kernel/proc.c:581](./kernel/proc.c:581) (`wakeup`).

**The two lock roles**

* `lk` — the **condition lock**. It protects the shared data whose condition the caller tests and
  updates (for a semaphore, `sem->value` alongside `sem->lock`).
* `p->lock` — the **process lock**. It protects the scheduling state (`p->state`, `p->chan`) of one
  process `p`, and it is the lock the scheduler itself requires (`sched()` panics unless `p->lock` is
  held — [kernel/proc.c:498](./kernel/proc.c:498)).

`chan` is only an identifying tag, not storage: it is written to `p->chan` and compared in `wakeup()`.
No data is passed through it.

**Trace of the waiter**, starting while it holds `lk`:

| Step | Where | Lock state |
|---|---|---|
| 1. tests the condition with `lk` held | caller loop | holds `lk` |
| 2. calls `sleep(chan, lk)` | [proc.c:550](./kernel/proc.c:550) | holds `lk` |
| 3. `acquire(&p->lock)` | [proc.c:561](./kernel/proc.c:561) | holds `lk` **and** `p->lock` |
| 4. `release(lk)` | [proc.c:562](./kernel/proc.c:562) | holds `p->lock` |
| 5. `p->chan = chan; p->state = SLEEPING;` | [proc.c:565-566](./kernel/proc.c:565) | holds `p->lock` |
| 6. `sched()` → `swtch()` into the scheduler | [proc.c:568](./kernel/proc.c:568) | holds `p->lock`; `p->lock` is handed to the scheduler, which releases it after the switch ([proc.c:462-476](./kernel/proc.c:462)) |
| 7. process later made `RUNNABLE` by `wakeup()`, then picked by the scheduler, which re-`acquire(&p->lock)` and `swtch`es back into `sleep()` | [proc.c:462-476](./kernel/proc.c:462) | holds `p->lock` again |
| 8. `p->chan = 0; release(&p->lock);` | [proc.c:571-574](./kernel/proc.c:571) | `p->lock` dropped |
| 9. `acquire(lk)` | [proc.c:575](./kernel/proc.c:575) | holds `lk` again — returns to the caller with `lk` held, exactly as it was passed in |

**State transitions:** `RUNNING` → `SLEEPING` in step 5; `SLEEPING` → `RUNNABLE` in `wakeup()`
([proc.c:589](./kernel/proc.c:589)); `RUNNABLE` → `RUNNING` when the scheduler picks it
([proc.c:463-466](./kernel/proc.c:463)).

**Why a wakeup cannot be lost.** The waker must hold the *same* `lk` while it changes the shared data
and calls `wakeup()`. The waiter holds `lk` continuously from its condition test (step 1) until step 4,
and it acquires `p->lock` *before* releasing `lk` (step 3). So when the waker holds `lk`, the waiter is
in one of exactly two places: either it has not yet entered the check/sleep region — in which case it
will acquire `lk` after the waker is done and will see the updated condition and not sleep at all — or
it has already stored `SLEEPING` in step 5. And because `wakeup()` inspects `p->state` under
`p->lock` ([proc.c:587-591](./kernel/proc.c:587)), and step 5 stores `SLEEPING` under the same
`p->lock`, `wakeup()` is serialised with the state transition: it either sees `SLEEPING` and sets
`RUNNABLE`, or the waiter has not reached step 5 yet — which, as argued, means it will re-check the
condition and find it true. The critical property is the *ordering* in `sleep()`: `p->lock` is taken
**before** `lk` is dropped.

**Why the waiter must recheck.** `wakeup()` only flips `SLEEPING` → `RUNNABLE`. It is not a hand-off:
it does not run the waiter immediately, does not reserve the resource, and does not even guarantee the
condition is still true — it wakes *every* process sleeping on that channel
([proc.c:581-593](./kernel/proc.c:581)). Between being marked `RUNNABLE` and actually running, another
process can consume the resource (e.g. another waiter decrements `sem->value` back to 0), and several
woken waiters can race for one unit of resource. Therefore the condition must be re-evaluated in a
`while` loop, with `lk` held, on every wake-up. A single `if` would be a bug.

### 1.3 Spinning vs. sleeping

Costs involved in sleeping (not just "one switch"): `acquire(&p->lock)`, `release(lk)`, state change,
`sched()`, one `swtch()` out, the scheduler loop, a later `swtch()` back in, plus the waker's
`wakeup()`, which scans all `NPROC` process slots and does an `acquire`/`release` on each `p->lock`.
That is on the order of hundreds to a few thousand cycles, and it is spent on the *waiter's* and
*waker's* behalf. Spinning is a few cycles per attempt (an `amoswap` plus a branch), but it consumes a
full CPU for the whole wait, and in xv6 `acquire()` spins with interrupts disabled, so the spinning CPU
can do nothing else.

**≈10 cycles.** Spinning is cheaper. 10 cycles is shorter than even one `swtch()`, never mind two
switches plus a `wakeup()` scan. Going to sleep would cost far more than the wait itself.

**≈10,000 cycles.** Sleeping is cheaper, *provided the lock holder can actually run and finish*. 10,000
cycles of spinning would burn a whole CPU (one of only three here) that could instead be running the
process that releases the resource — with `CPUS=3` and three runnable processes, spinning can actively
delay the producer you are waiting for. Sleeping releases the CPU and lets useful work proceed.

**Assumptions I am making.**

1. The holder of the resource is running concurrently on another CPU, or can be scheduled while we
   sleep. On a uniprocessor where the holder is descheduled and interrupts are off for the spinner,
   spinning would deadlock, and sleeping is the only option.
2. "Cheaper" means total cycles consumed by the system, not latency of this one process: sleeping adds
   wake-up latency, so a latency-critical short wait may still prefer spinning.
3. 10 and 10,000 are *illustrative* magnitudes, not measured xv6 thresholds. The crossover is roughly
   "cost of the wait exceeds ≈ two context switches plus a `wakeup()` scan".

### Checkpoint 1

* **Spinning vs. sleeping costs, with assumptions:** above (1.3).
* **Condition lock, wait channel, process lock:** `lk` = condition lock guarding the predicate;
  `chan` = the identifying tag (I use the address of the `struct semaphore`); `p->lock` = protects
  `p->state`/`p->chan` and is required by `sched()`.
* **Why a woken process must recheck:** `wakeup()` does not reserve the resource and wakes all sleepers
  on the channel; the resource may have been taken by someone else before this process is scheduled.
* **Why separate reads and writes cannot replace atomic acquisition:** the read-then-write interleaving
  above lets both CPUs see `locked == 0` and enter the critical section; the atomic `amoswap`
  (plus the fence) makes acquisition a single indivisible, ordered operation.

---

## Part 2 — Completing the blocking semaphore

### 2.1 The three different "init"s, and the interface

These are three distinct things and it is easy to conflate them:

| Name | Where | What it does |
|---|---|---|
| `sem_init(value)` | user-facing, declared [user/user.h:38](./user/user.h:38) | A **system call**. Its number is `SYS_sem_init` ([kernel/syscall.h:33](./kernel/syscall.h:33)). |
| `sys_sem_init()` | [kernel/sysproc.c:123](./kernel/sysproc.c:123) | Reads the argument with `argint(0, &value)` and calls `sem_alloc(value)`; returns the semid to user space. |
| `sem_alloc(value)` | [kernel/semaphore.c:31](./kernel/semaphore.c:31) | The real allocator: takes `sem_table_lock`, finds a free slot, marks `in_use = 1`, stores the initial `value`, returns the index or `-1` if the table is full. |
| `seminit()` | [kernel/semaphore.c:21](./kernel/semaphore.c:21) | **Boot-time** initialisation only, called once from `main()` ([kernel/main.c:31](./kernel/main.c:31)). It initialises `sem_table_lock` and every per-semaphore lock, and marks every slot unused. It does **not** hand out a semaphore and has no return value. |

So a semaphore is *initialised at boot* (`seminit`) but *allocated on demand* (`sem_init` →
`sem_alloc`), and `semid` is just an index into `semaphores[]`.

The syscall wiring is already supplied: `SYS_sem_*` numbers in [kernel/syscall.h](./kernel/syscall.h),
handlers in [kernel/sysproc.c:122-151](./kernel/sysproc.c:122), stubs in [user/usys.pl](./user/usys.pl),
declarations in [user/user.h](./user/user.h) and [kernel/defs.h](./kernel/defs.h).

### 2.2 The implementation

Completed in [kernel/semaphore.c](./kernel/semaphore.c):

```c
int
sem_wait(int semid)
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

int
sem_signal(int semid)
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

int
sem_getvalue(int semid)
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

**Which lock and which channel.** Each `struct semaphore` owns its own `struct spinlock lock`
(initialised in `seminit()`), and that lock is used as the condition lock `lk` for exactly this
semaphore. The channel is the **address of the `struct semaphore` itself**: `sleep(sem, &sem->lock)`
and `wakeup(sem)`. Because the address differs per semaphore, a `sem_signal` on semaphore 3 can never
wake a waiter on semaphore 5. Note the waker passes `sem` (the channel) but `wakeup()` does not touch
`sem->lock` for the caller — the caller already holds it, which is what makes the wakeup
unloseable (Part 1.2).

**Why the waiter rechecks in a `while` loop.** `wakeup()` is not a hand-off: it only marks sleepers
`RUNNABLE` and it wakes *all* sleepers on the channel. With two waiters and one `signal`, both are
woken but only one unit of count exists. The loser re-runs the loop body, sees `sem->value == 0` and
sleeps again. If this were an `if`, the loser would fall through and decrement the count to `-1`, which
is exactly the "negative semaphore value" implementation this lab forbids.

**Why the decrement must be inside the lock.** `sem->value--` is a read-modify-write on shared state. It
happens with `sem->lock` held and while the condition is known true, so a concurrently-running
`sem_signal` cannot interleave between the test and the decrement. `sem_signal` makes the increment and
the `wakeup` one atomic step for the same reason.

### 2.3 Result of `sem_basic()` — and what it does **not** test

```
$ race_test
[sem_basic] Initializing semaphore to 1...
[sem_basic] Waiting (should decrement to 0)...
[sem_basic] Posting (should increment to 1)...
[sem_basic] PASS: Basic semaphore operations work.
```

The count sequence 1 → 0 → 1 holds, and `sem_free` succeeds.

**What this leaves untested.** `sem_basic` never calls `sem_wait` when `value == 0`, so it never
executes `sleep()` at all, and therefore never executes `wakeup()`, the recheck loop, or `sched()`. It
is a single-threaded test, so there is no contention. It also does not test: two waiters and one
signal; allocation exhaustion at `MAX_SEMAPHORES`; the `-1` error paths; or what happens if you free a
semaphore that still has users.

To make the blocking path *observable* I can state from the implementation: `sem_wait` on a value of 0
holds `sem->lock`, finds `sem->value == 0`, calls `sleep(sem, &sem->lock)`, which drops `sem->lock`
after taking `p->lock` (Part 1.2). A later `sem_signal` takes `sem->lock`, increments to 1, calls
`wakeup(sem)`, which finds the sleeper's `p->chan == sem` and marks it `RUNNABLE`. When that process is
scheduled, `sleep()` returns with `sem->lock` re-acquired; the `while` re-tests `sem->value`, now 1, so
it exits the loop and decrements to 0. Part 4 exercises this path for real: the consumer's first
`sem_wait(b.filled)` blocks because `filled` starts at 0.

### When is it safe to free a semaphore?

`sem_free()` ([kernel/semaphore.c:47](./kernel/semaphore.c:47)) only clears `in_use`; it neither wakes
nor waits for users. So it is safe only when no process can still call `sem_wait`/`sem_signal` on that
`semid`:

* In `race_test()`: after `wait(0)` has reaped the child, so all the child's increments are finished.
* In `producer_consumer()`: after the consumer has read all 96 bytes *and* both producers have been
  reaped by the two `wait(0)` calls.

Freeing earlier is dangerous because the slot can be reallocated to an unrelated semaphore, so a
process still sleeping on the old channel would be woken by — or worse, decrement — the new one.

### Checkpoint 2

* **`sem_init` vs `seminit` vs `sem_alloc`:** table in 2.1.
* **Lock and channel:** per-semaphore `sem->lock`; channel = `&semaphores[semid]`.
* **Why recheck:** `wakeup()` reserves nothing and wakes every sleeper on the channel; a loser would
  otherwise drive the count negative.
* **Basic sequence passing / untested:** shown in 2.3; the zero-count sleep path is untested by
  `sem_basic` and is exercised instead by Part 4.
* **When safe to free:** after all users have finished; in this lab, after `wait()` has reaped the
  children.

---

## Part 3 — Protecting the shared counter

### 3.1 The lost update

`ucnt_get()` and `ucnt_set()` ([kernel/ucnt.c:13-24](./kernel/ucnt.c:13)) are ordinary load and store on
the global `int ucnt[UCNT_MAX]`. The increment in `do_work()` is two syscalls:

```c
int val = ucnt_get(0);      // syscall: kernel reads ucnt[0], returns it
ucnt_set(0, val + 1);       // syscall: kernel writes ucnt[0]
```

Entering the kernel does **not** make the pair atomic. Each syscall is atomic only in the sense that
one instruction sequence runs in the kernel; between the two syscalls the kernel returns to user space,
`usertrapret`s, and the process may be preempted, may `yield`, or simply be slow — and on
`CPUS=3` the other process may be running the same code on a different hart at the same moment.

Interleaving with both starting from a counter of 100:

| Time | Parent | Child | `ucnt[0]` |
|---|---|---|---|
| t1 | `val = ucnt_get(0)` → 100 | | 100 |
| t2 | | `val = ucnt_get(0)` → 100 | 100 |
| t3 | `ucnt_set(0, 101)` | | 101 |
| t4 | | `ucnt_set(0, 101)` | 101 |

Two increments happened, but the counter moved by one: one update was **lost**.

### 3.2 The fix and the evidence

```c
void do_work(int pid, int semid) {
    for (int i = 0; i < N; i++) {
        sem_wait(semid);            // enter critical section
        int val = ucnt_get(0);
        ucnt_set(0, val + 1);
        sem_signal(semid);          // leave critical section
    }
}
```

and in `race_test()` the semaphore is created before the `fork()`:

```c
int semid = sem_init(1);   // binary semaphore => mutual exclusion
T_ASSERT(semid >= 0);
```

Initial count **1** is what makes it a mutex: the first `sem_wait` succeeds immediately (1 → 0) and
everyone else blocks until the holder `sem_signal`s (0 → 1). The child inherits `semid` through `fork()`
by value, but `semid` is only an index into the kernel's `semaphores[]`, which is *not* copied on
`fork` — it lives in kernel memory. So both processes' `sem_wait(semid)`/`sem_signal(semid)` refer to
exactly the same kernel object, which is precisely why the protection works across the fork.

**Why protecting the two syscalls separately would be insufficient.** The invariant is not "a syscall
must not be interrupted" — the invariant is "the value I read must still be the value I write". That
spans *both* calls. Locking inside each syscall (which is effectively already the case, each runs in
the kernel) leaves the gap between them open, and the table in 3.1 is exactly that gap. The critical
section is the read–modify–write **pair**, so the lock has to be held across the pair — from user space.

**Evidence (both directions).**

Unprotected version (I temporarily removed `sem_wait`/`sem_signal` from `do_work`, rebuilt, then
restored):

```
[race_test] final counter=1737 (expected 2000)
Assertion failed at user/race_test.c:53: final == 2*N
```

(Line 53 is where the assertion sat in that temporary build — with the two protection lines removed,
everything below `do_work()` shifted up by two; in the final file the same assertion is at
[user/race_test.c:55](./user/race_test.c:55).)

The lost update is real and reproducible; the counter is short by 263 increments.

Protected version:

```
$ race_test
[race_test] final counter=2000 (expected 2000)
[race_test] PASS: consistent counter
```

**Why the parent waits before validating and freeing.** `wait(0)` blocks until the child has exited, so
when the parent reads `ucnt_get(0)` all 1000 of the child's increments have completed — otherwise the
final read could see a partially-complete total and fail spuriously. The same `wait(0)` is what makes
`sem_free(semid)` at the end of `race_test()` safe: after it, no process can still be using that
semaphore.

### Checkpoint 3

* **Lost-update interleaving:** table in 3.1, plus the observed `1737 != 2000`.
* **Why protecting the two calls separately is insufficient:** the invariant spans both calls; the
  read and the write must be one critical section.
* **Expected final count and the shared semaphore:** 2000 = `2*N`; the semaphore created by
  `sem_init(1)` in `race_test()` before `fork()`, shared by parent and child via the same kernel
  `semid`.
* **Why the parent waits first:** to ensure the child's increments are complete before validating, and
  to ensure no user remains before freeing.

---

## Part 4 — Producers and a consumer

### 4.1 The supplied buffer

[kernel/ubuf.c](./kernel/ubuf.c) is a 16-slot circular buffer with a shared `head` and `tail`. Note the
comment on [kernel/ubuf.c:6](./kernel/ubuf.c:6) ("buffer writes to head and read from tail") is
**wrong**; as the manual says, follow the bodies: `ubuf_write()` uses `tail`, `ubuf_read()` uses `head`.

```c
char ubuf_read(void) {                       // ubuf.c:14
    char data = ubuf.data[ubuf.head];
    yield();                                 // <-- descheduled mid-operation!
    ubuf.head = (ubuf.head + 1) % UBUF_SIZE;
    return data;
}

void ubuf_write(char val) {                  // ubuf.c:21
    ubuf.data[ubuf.tail] = val;
    yield();                                 // <-- descheduled mid-operation!
    ubuf.tail = (ubuf.tail + 1) % UBUF_SIZE;
}
```

Neither function checks empty/full. The `yield()` sits between the data access and the index update
precisely to widen the window and expose missing mutual exclusion. Workload: two producers, each
sending 48 characters from `msg`; the parent is the consumer and performs `MSG_SIZE * NUM_PROD = 96`
reads. The terminating NUL is not sent.

### 4.2 Counts and call order

```c
#define UBUF_SLOTS 16 // must match UBUF_SIZE in kernel/ubuf.c

struct buf_sem {
    int empty;   // counts free slots,  initialised to UBUF_SLOTS
    int filled;  // counts filled slots, initialised to 0
    int mutex;   // binary, protects the buffer indices, initialised to 1
};
```

| Semaphore | Initial value | Derived from | Role |
|---|---|---|---|
| `empty` | **16** | the buffer starts empty, so all `UBUF_SIZE = 16` slots are free | counts *space*. A producer waits on it, a consumer signals it. |
| `filled` | **0** | the buffer starts empty, so no slot holds data | counts *data*. A consumer waits on it, a producer signals it. |
| `mutex` | **1** | unlocked | binary; protects the `data`/`head`/`tail` critical section |

```c
void producer(const char* msg, struct buf_sem b) {
    for (const char* p = msg; *p != '\0'; p++) {
        sem_wait(b.empty);    // 1. wait for space  (outside the mutex!)
        sem_wait(b.mutex);    // 2. take the mutex
        ubuf_write(*p);       // 3. critical section (contains a yield)
        sem_signal(b.mutex);  // 4. release the mutex
        sem_signal(b.filled); // 5. announce one more item
    }
}

void consumer(struct buf_sem b, int loops, int valid[]) {
    char tmp;
    for(int i = 0; i < loops; i++) {
        sem_wait(b.filled);   // 1. wait for data   (outside the mutex!)
        sem_wait(b.mutex);    // 2. take the mutex
        tmp = ubuf_read();    // 3. critical section (contains a yield)
        sem_signal(b.mutex);  // 4. release the mutex
        sem_signal(b.empty);  // 5. announce one more free slot
        T_ASSERT(valid[(unsigned char)tmp]);
    }
}
```

**Why `empty`/`filled` are waited for *before* taking `mutex` — otherwise deadlock.** Suppose a
producer held `mutex` and then blocked on `empty`. A free slot is only ever created by a consumer
calling `sem_signal(empty)`, and the consumer can only get there after `ubuf_read()`, which it can only
reach after `sem_wait(mutex)`. But `mutex` is held by the blocked producer forever. So the consumer
spins at `sem_wait(mutex)`, `empty` never rises above 0, and the producer never wakes: a classic
deadlock (circular wait: producer holds `mutex` and waits for `empty`; consumer waits for `mutex`,
which is a prerequisite for producing `empty`). Waiting for the resource count *first*, while holding
no lock, removes the cycle.

### 4.3 Tracing one byte

Produce (in a producer):

1. `sem_wait(b.empty)` — if all 16 slots are full, the producer sleeps on the `empty` channel until a
   consumer signals it; otherwise `empty` goes 16 → 15 and it proceeds.
2. `sem_wait(b.mutex)` — 1 → 0; the producer is now the only one allowed inside the buffer.
3. `ubuf_write(c)` — stores `c` at `ubuf.data[tail]`, then **yields**. Another process may now be
   descheduled in. Any other producer or the consumer will immediately block at `sem_wait(b.mutex)`,
   because `mutex` is 0, so no one can touch `head`/`tail` while this producer is paused between the
   store and the index update. This is exactly the property `yield()` is there to test.
4. `sem_signal(b.mutex)` — 0 → 1, `wakeup(mutex)` releases whoever is waiting.
5. `sem_signal(b.filled)` — 0 → 1, `wakeup(filled)` makes the waiting consumer runnable.

Consume (in the parent):

1. `sem_wait(b.filled)` — blocks while there is no data (this is the very first thing the consumer
   does, since `filled` starts at 0).
2. `sem_wait(b.mutex)`; 3. `ubuf_read()` reads `data[head]`, yields, advances `head` — protected the
   same way; 4. `sem_signal(b.mutex)`; 5. `sem_signal(b.empty)` frees a slot and wakes a blocked
   producer.

Invariant: at any instant, `empty + filled + (slots being handled inside the critical section)` equals
16, and `head`/`tail` are only ever touched with `mutex` held, so the ring never advances inconsistently.

**Why counting slots alone does not protect the buffer.** A counting semaphore enforces *how many*
processes may be inside, not *who may not overlap with whom* on the shared indices. If the code took
only `empty`/`filled`, two producers could pass `sem_wait(empty)` (both find `empty > 0`) and both land
on `ubuf.data[ubuf.tail] = val` with the same `tail`: the second write silently overwrites the first
(one byte lost, and `tail` advanced twice). Likewise a reader could read `data[head]` while a writer is
halfway through, or two readers could both read the same slot under one `filled` token, producing a
duplicated byte. `head` and `tail` are shared mutable state that must be updated atomically as a unit
with the payload access, and only `mutex` (held across the *whole* function, including past the
`yield()`) provides that.

**Cleanup.** The consumer runs in the parent process; after it returns, the parent `wait(0)`s twice to
reap both producers, and only then frees all three semaphores:

```c
sem_free(b.mutex);
sem_free(b.filled);
sem_free(b.empty);
```

### Result

```
$ race_test
[sem_basic] PASS: Basic semaphore operations work.
[race_test] final counter=2000 (expected 2000)
[race_test] PASS: consistent counter
[producer_consumer] PASS: message delivered
ALL TESTS PASSED
```

And with only `producer_consumer()` selected in `main()`:

```
[producer_consumer] PASS: message delivered
```

The blocking path really is exercised here: the consumer's first `sem_wait(b.filled)` must sleep
because `filled` starts at 0, and with 96 bytes to write into 16 slots, producers must block on `empty`
whenever the consumer falls behind.

**Limits of the supplied check.** The assertion is

```c
T_ASSERT(valid[(unsigned char)tmp]);
```

which only verifies that each received byte is *one of* the characters in `msg`. It does not count
occurrences, does not check order, and does not detect a byte that is duplicated, lost or reordered —
as long as the byte that arrives is in the set. So this test alone cannot prove the absence of
duplication, loss or reordering, and I do not claim that it does. What it *does* establish is that no
corrupted/foreign byte ever appeared and that the run completed without a deadlock. The stronger
correctness argument comes from the design: total `sem_signal(filled)` equals total `sem_wait(filled)`
= 96, and `mutex` makes each `ubuf_read`/`ubuf_write` indivisible with respect to the indices.

### Checkpoint 4

* **Each semaphore's role and initial value:** `empty = 16` (all slots free), `filled = 0` (nothing
  produced), `mutex = 1` (unlocked).
* **Trace of one byte:** section 4.3.
* **Why slot counts alone are not enough:** section 4.3 — `head`/`tail` are shared state; counts do not
  prevent two processes from entering the buffer function at once.
* **Completion:** the consumer finishes all 96 reads in the parent, both producers are reaped with
  `wait(0)`, then all three semaphores are freed.
* **Limits of the membership check:** it only proves each byte is in the character set; it cannot prove
  no duplication, loss or reordering.

---

## Appendix A — All verified runs

Full sequence, all with `CPUS=3`:

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

Run three times back-to-back in one boot to check for timing flakiness — all three passed with
`final counter=2000` each time. The unprotected counter variant failed with `final counter=1737`.

---

## Appendix B — Build blocker in `usertests.c`

Before any of the above could run, `make` failed while building the file system:

```
user/usertests.c: In function 'fsfull':
user/usertests.c:2347:7: error: variable 'fsblocks' set but not used [-Werror=unused-but-set-variable=]
cc1: all warnings being treated as errors
make: *** [user/usertests.o] Error 1
```

`fsfull()` counts blocks written into `fsblocks` but never reads it, and the Makefile compiles user
programs with `-Wall -Werror` ([Makefile:65](./Makefile:65)). A newer host GCC (16.2.0 here) diagnoses
this, so `fs_create`/`fs.img` — and therefore `make qemu` — cannot be built at all on this machine.
Upstream MIT fixed this in the same way, so I applied their change to
[user/usertests.c:2391](./user/usertests.c:2391):

```diff
-  printf("fsfull test finished\n");
+  printf("fsfull test finished, %d blocks\n", fsblocks);
```

`fsblocks` is now read, and `fsfull` prints one extra number at the end — behaviour of the rest of the
test is unchanged.

---

## Appendix C — Files changed

| File | Change |
|---|---|
| [kernel/semaphore.c](./kernel/semaphore.c) | Implemented `sem_wait` (sleep-on-zero + recheck + decrement), `sem_signal` (increment + wakeup), `sem_getvalue` (locked read). |
| [user/race_test.c](./user/race_test.c) | `do_work()` wraps the read–modify–write in a binary semaphore; `race_test()` creates it; `struct buf_sem` gains `empty`/`filled`/`mutex`; `producer()`/`consumer()` implement wait → mutex → buffer → mutex → signal; `producer_consumer()` initialises and frees the semaphores. |
| [user/usertests.c](./user/usertests.c) | Pre-existing `-Werror` failure fixed with the upstream MIT change (Appendix B). |

`kernel/spinlock.c`, `kernel/ucnt.c` and `kernel/ubuf.c` were deliberately left unchanged, as the lab
requires.

---

## References

* SC2005 Lab 3 branch: <https://github.com/CPS-research-group/ntu-sc2005-xv6/tree/lab3>
* Russ Cox, Frans Kaashoek, Robert Morris, *xv6: a simple, Unix-like teaching operating system*,
  §6.0–6.3 (locking) and §7.5–7.7 (sleep/wakeup, semaphores).
