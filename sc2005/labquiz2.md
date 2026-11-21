# SC2005 — Lab 3 + Lab 4 Combined Notes (`labquiz2`)

Everything below is grounded in the two checkouts in this folder:

| Folder | Branch | Kernel | Key files |
|---|---|---|---|
| [lab3/](./lab3) | `lab3` | xv6-riscv | [kernel/semaphore.c](./lab3/kernel/semaphore.c), [kernel/spinlock.c](./lab3/kernel/spinlock.c), [kernel/proc.c](./lab3/kernel/proc.c), [user/race_test.c](./lab3/user/race_test.c) |
| [lab4/](./lab4) | `lab4` | xv6-riscv | [kernel/vm.c](./lab4/kernel/vm.c), [kernel/sysproc.c](./lab4/kernel/sysproc.c), [kernel/trap.c](./lab4/kernel/trap.c), [kernel/proc.c](./lab4/kernel/proc.c), [user/lazytest.c](./lab4/user/lazytest.c), [user/fault.c](./lab4/user/fault.c) |

Full write-ups with run transcripts live in [lab3/LAB3_ANSWERS.md](./lab3/LAB3_ANSWERS.md) and
[lab4/LAB4_ANSWERS.md](./lab4/LAB4_ANSWERS.md).

**How to read this file.** Every concept has two layers:

- `> **ELI5 —** ...` a plain-language analogy you can recall under exam pressure.
- `**Detail.**` the actual mechanism, xv6 code, and the sentence you should be able to say.

Back matter: **Part D traps**, **Part E scenarios**, **Part F quiz**, **Part G answer key**,
**Part H cheat sheet**, **Part I prompt/checkpoint coverage**, **Part J change log**.

Verified state (rebuilt and booted with `CPUS=3`, QEMU 11.1.1, `riscv64-elf-gcc` 16.2.0):

```
$ race_test
[sem_basic] PASS: Basic semaphore operations work.
[race_test] final counter=2000 (expected 2000)
[race_test] PASS: consistent counter
[producer_consumer] PASS: message delivered
ALL TESTS PASSED

$ lazytest
Before: VP=4, PP=4
After sbrk(122880): VP=34, PP=4
Success: PP count unchanged (lazy allocation verified)
Touching pages...
After touching: PP=34

$ fault read   → usertrap(): load page fault pid=4 va=0x4000 ...
$ fault write  → usertrap(): store page fault pid=5 va=0x4000 ...
```

---

# PART A — LAB 3: SYNCHRONIZATION AND SEMAPHORES

## A1. The problem: shared kernel state

> **ELI5 —** Two people editing the same Google Doc at the same time. Each opens the page, types,
> and saves. If both opened the same old copy, whoever saves second erases the other's sentence.
> Nothing was "broken" — the interleaving was.

**Detail.** Lab 3's shared objects live in **kernel memory**, not in either process:

- `int ucnt[16]` in [kernel/ucnt.c](./lab3/kernel/ucnt.c) — exposed as `ucnt_get(idx)` / `ucnt_set(idx, val)`.
- `struct ubuf` in [kernel/ubuf.c](./lab3/kernel/ubuf.c) — a 16-slot circular buffer exposed as `ubuf_read()` / `ubuf_write(val)`.

`fork()` copies *user* memory, but a child's `ucnt_get()` syscall reaches the same array as the
parent's. So parent and child are two independent instruction streams mutating one kernel object,
on one CPU (preemptive interleaving) or two (true parallel).

The counter increment in [user/race_test.c](./lab3/user/race_test.c) is:

```c
int val = ucnt_get(0);   // syscall 1: read
ucnt_set(0, val + 1);    // syscall 2: write
```

Each syscall is individually atomic *inside the kernel*, but the **pair is not**. Interleaving:

| Time | Process A | Process B | `ucnt[0]` |
|---|---|---|---|
| t1 | `get` → 10 | | 10 |
| t2 | | `get` → 10 | 10 |
| t3 | `set(11)` | | 11 |
| t4 | | `set(11)` | 11 |

Two increments, one net effect. With `N = 1000` per process and 2 processes the expected count is
`2 * N = 2000`; an unprotected run in this lab measured **1737**.

**The sentence to say:** "Read–modify–write across two system calls is not a critical section;
entering the kernel per call does not make the sequence atomic."

---

## A2. Spinlocks

> **ELI5 —** One bathroom key at a café. To use the bathroom you check "is the key on the hook?".
> If not, you stand there and keep checking (spinning). Taking the key and checking must be the
> *same* action — if you look, then reach, two people can both think the hook was full.
> Turning your phone off while inside (disabling interrupts) stops *you* being interrupted; it does
> nothing about the person at the second counter.

**Detail.** [kernel/spinlock.h](./lab3/kernel/spinlock.h):

```c
struct spinlock {
  uint locked;       // Is the lock held?
  char *name;
  struct cpu *cpu;   // which CPU holds it (debug + holding())
};
```

[kernel/spinlock.c](./lab3/kernel/spinlock.c) `acquire()` (L22–L45):

1. `push_off()` — disable interrupts on **this** hart, nesting-aware.
2. `if(holding(lk)) panic("acquire")` — non-reentrant.
3. `while(__sync_lock_test_and_set(&lk->locked, 1) != 0);` — atomic swap:
   `amoswap.w.aq a5, a5, (s1)`. The read and the write are one instruction, so two CPUs cannot both
   observe 0.
4. `__sync_synchronize()` — RISC-V `fence`; keeps critical-section loads/stores from moving above
   the acquisition.
5. `lk->cpu = mycpu()` — for `holding()` and debug.

`release()` (L47–L69) is the mirror: verify ownership, `fence`, `__sync_lock_release` (an
`amoswap.w zero, zero` — a single store, not a C assignment that could be split), `pop_off()`.

`push_off()` / `pop_off()` (L89–L120) are **matched counters**, not `intr_off()`:

```c
void push_off(void) {
  int old = intr_get();
  if(mycpu()->noff == 0){ intr_off(); mycpu()->intena = old; }
  mycpu()->noff += 1;
}
```

Nested acquires must not re-enable interrupts on the inner release; `noff` counts depth and only the
outermost `pop_off()` restores the original `intena`. If interrupts were already off on entry, they
stay off.

**Why interrupts-off ≠ mutual exclusion.** `intr_off()` clears `sstatus.SIE` on one hart. Another
hart executing the same code sees nothing. The spinlock's value in shared memory is the only thing
both CPUs agree on.

**Why the lock is still needed with interrupts off.** Two roles, not one:
interrupts-off prevents *this* CPU from taking a timer interrupt and context-switching inside the
critical section (a self-deadlock risk); the spinlock prevents *another* CPU from entering.

**Cost.** A spinning core burns cycles and cannot do useful work. That is why xv6 sleeps for long
waits and spins only for short ones.

---

## A3. `sleep()` and `wakeup()`

> **ELI5 —** A waiting room with a clipboard. Before napping you write your name and the reason
> ("waiting for semaphore #3") on the clipboard, then sleep. Anyone who changes the situation reads
> the clipboard and shakes the matching people awake. The trick is that writing your name and
> falling asleep must not have a gap, or someone can call your name while you are still walking to
> the chair.

**Detail.** [kernel/proc.c](./lab3/kernel/proc.c) L550–L574:

```c
void sleep(void *chan, struct spinlock *lk)
{
  struct proc *p = myproc();

  acquire(&p->lock);   // process lock: protects state + chan
  release(lk);         // condition lock: let the world change the condition

  p->chan = chan;      // "I am waiting for this object"
  p->state = SLEEPING;

  sched();             // never returns until someone wakes us

  p->chan = 0;         // tidy
  release(&p->lock);
  acquire(lk);         // caller gets its condition lock back
}
```

`wakeup(chan)` (L581–L596) walks the whole process table, and for every process that is
`SLEEPING` with `p->chan == chan`, takes `p->lock` and sets `state = RUNNABLE`. It never runs the
process itself; the scheduler does that later.

Two locks, two jobs:

| Lock | Protects | Held by |
|---|---|---|
| `lk` (condition lock, e.g. `&sem->lock`) | the shared data the waiter tests and the signaller updates | waiter while checking; signaller while updating + `wakeup` |
| `p->lock` (process lock) | `p->state`, `p->chan`, scheduling | `sleep`, `wakeup`, scheduler |

**The lost-wakeup race and why the ordering fixes it.** Suppose `sleep()` set `p->state` *before*
taking `p->lock`, and `wakeup()` did not take `p->lock`. Then:

| Time | Waiter | Signaller |
|---|---|---|
| t1 | checks condition → false | |
| t2 | | updates data, `wakeup(chan)` → sees waiter RUNNING, does nothing |
| t3 | sets `SLEEPING` | |
| t4 | sleeps forever | |

Holding `p->lock` across "set `chan` + set `SLEEPING`" closes the window: `wakeup()` must acquire
`p->lock` to inspect the state, so it either sees `RUNNING` *before* the waiter starts sleeping
(and the waiter will recheck the condition after `release(lk)`/re-`acquire(lk)`) or sees
`SLEEPING` *after* (and wakes it).

**Why the caller must recheck in a loop.** `wakeup()` only makes sleepers runnable; it reserves
nothing. Another process may consume the resource first, or the wake may be for a different event on
the same channel. Hence `while(cond) sleep(...)`, never `if(cond) sleep(...)`.

`chan` is just an address used for matching — it is not a message queue and carries no data.

**Comparison point for exams:** spin = busy-wait, cheap for a few cycles, wasteful for thousands;
sleep = block + two context switches, wasteful for a few cycles, correct for long waits. State your
assumptions (lock-holder can run in parallel? wakeup latency?).

---

## A4. The blocking semaphore

> **ELI5 —** A bouncer with a clicker. The count is how many people may still enter. At zero you
> queue outside and nap. Every "signal" clicks the counter up and taps one sleeper on the shoulder.
> A binary semaphore (count 1) is a single key: mutual exclusion.

**Detail.** Kernel object, [kernel/semaphore.c](./lab3/kernel/semaphore.c):

```c
#define MAX_SEMAPHORES 32

struct semaphore {
  struct spinlock lock;   // per-semaphore condition lock
  int value;
  int in_use;
};
struct semaphore semaphores[MAX_SEMAPHORES];
struct spinlock sem_table_lock;   // protects the free-list / in_use flags
```

Three different "inits" — a classic exam trap:

| Name | Where | What it does |
|---|---|---|
| `seminit()` | kernel/semaphore.c, called from `main()` at boot | initialises `sem_table_lock` and every per-semaphore `lock`; marks all slots unused |
| `sem_alloc(value)` | kernel | finds a free slot under `sem_table_lock`, sets `in_use = 1`, `value`, returns the index (the `semid`) or `-1` |
| `sem_init(value)` | user-visible syscall | `argint` then `sem_alloc(value)` — thin wrapper, no policy of its own |

User-facing contract (from the lab manual and [user/user.h](./lab3/user/user.h)):

| Call | Behaviour | Returns |
|---|---|---|
| `sem_init(value)` | allocate, initial count `value` | `semid`, or `-1` |
| `sem_free(semid)` | mark slot unused | `0`, or `-1` |
| `sem_wait(semid)` | block while 0, then decrement | `0`, or `-1` |
| `sem_signal(semid)` | increment and wake waiters | `0`, or `-1` |
| `sem_getvalue(semid)` | read count under the lock | count, or `-1` |

Implementation (L60–L104):

```c
int sem_wait(int semid) {
  if(semid < 0 || semid >= MAX_SEMAPHORES || !semaphores[semid].in_use) return -1;
  struct semaphore *sem = &semaphores[semid];
  acquire(&sem->lock);
  while(sem->value == 0)
    sleep(sem, &sem->lock);   // releases sem->lock, reacquires on wake
  sem->value--;
  release(&sem->lock);
  return 0;
}

int sem_signal(int semid) {
  ...
  acquire(&sem->lock);
  sem->value++;
  wakeup(sem);                // channel is the semaphore's address
  release(&sem->lock);
  return 0;
}

int sem_getvalue(int semid) {
  ...
  acquire(&sem->lock);
  int value = sem->value;
  release(&sem->lock);
  return value;
}
```

Why this is correct:

- The `while` recheck matters even though `wakeup()` was called under `sem->lock`: between `sched()`
  returning and `sem->lock` being re-acquired, another waiter can win the count.
- Channel identity is `sem` (the array slot address), so only waiters on *that* semaphore wake.
- The value never goes negative: waiters block at 0 instead of decrementing below it. The
  "negative value = number of waiters" convention from some textbooks is **not** used here.

`sem_free()` only clears `in_use`; it does **not** wake sleeping waiters. Hence the rule: free only
after every user has finished. Freeing with a sleeper still queued leaves that process asleep on a
channel nothing will ever signal.

Subtle (worth knowing, not required): the `in_use` check in `sem_wait`/`sem_signal` happens
*before* `acquire(&sem->lock)`, so `sem_free` racing with a user is unsynchronised by design. The
lab's "free after all users finish" rule is what makes it safe.

Syscall wiring is supplied: numbers `SYS_sem_init = 26` … `SYS_sem_free = 30` in
[kernel/syscall.h](./lab3/kernel/syscall.h), dispatch in [kernel/syscall.c](./lab3/kernel/syscall.c),
handlers at [kernel/sysproc.c](./lab3/kernel/sysproc.c) L123–L151.

---

## A5. The three Lab 3 tests

### A5.1 `sem_basic()` — the smoke test

Sequence `1 → 0 → 1`:

```c
int semid = sem_init(1);
T_ASSERT(sem_getvalue(semid) == 1);
sem_wait(semid);                     // 1 → 0
T_ASSERT(sem_getvalue(semid) == 0);
sem_signal(semid);                   // 0 → 1
T_ASSERT(sem_getvalue(semid) == 1);
sem_free(semid);
```

> **ELI5 —** Checks the clicker counts down and up. It does **not** prove that anyone ever napped.

**What it does not test:** the count never reaches 0 while a second process is waiting, so the
blocking path is not exercised. `sem_getvalue` returning `-1` (the placeholder) makes the first
assertion fail, which is how you know it is wired.

### A5.2 `race_test()` — mutual exclusion

```c
int N = 1000;

void do_work(int pid, int semid) {
    for (int i = 0; i < N; i++) {
        sem_wait(semid);
        int val = ucnt_get(0);
        ucnt_set(0, val + 1);
        sem_signal(semid);
    }
}

void race_test() {
    ucnt_set(0, 0);
    int semid = sem_init(1);   // binary: mutual exclusion
    int pid = fork();
    if (pid == 0) { do_work(pid, semid); exit(0); }
    else { do_work(getpid(), semid); wait(0);
           T_ASSERT(ucnt_get(0) == 2*N); }
    sem_free(semid);
}
```

> **ELI5 —** Only one person may hold the pen at a time. 1000 lines each, two people, so exactly
> 2000 lines.

Points that earn marks:

- Initial count **1** (not 0): the first waiter must proceed immediately.
- The wait/signal wrap the **whole** read–modify–write, not each syscall.
- `sem_init` happens **before** `fork()`, so both processes inherit the same `semid`. A `semid` is a
  kernel array index, so the child's copy still names the same kernel object.
- The parent `wait(0)`s before reading the counter — otherwise it could read early.
- `sem_free` after the child is reaped, i.e. after all users finished.

Protecting the two syscalls *separately* would still allow the interleaving in A1 — the lock would
be dropped between them.

### A5.3 `producer_consumer()` — counts plus exclusion

Workload: `MSG_SIZE = 48`, two producers, so the consumer performs `48 * 2 = 96` reads from a buffer
of `UBUF_SIZE = 16` slots. The terminating NUL is not sent.

> **ELI5 —** A shelf with 16 slots. `empty` counts free slots, `filled` counts occupied ones.
> `mutex` is the "only one person may touch the shelf at a time" key. You must **wait for space or
> data before** grabbing the key — otherwise you hold the key while waiting for something that only
> the person you just locked out could produce.

Counts:

| Semaphore | Initial | Derived from | Role |
|---|---|---|---|
| `empty` | **16** (`UBUF_SIZE`) | buffer starts empty → all slots free | producer waits, consumer signals |
| `filled` | **0** | nothing produced yet | consumer waits, producer signals |
| `mutex` | **1** | unlocked | protects `ubuf_read` / `ubuf_write` as a whole |

Call order per byte:

```
producer: sem_wait(empty) → sem_wait(mutex) → ubuf_write(c) → sem_signal(mutex) → sem_signal(filled)
consumer: sem_wait(filled) → sem_wait(mutex) → ubuf_read()    → sem_signal(mutex) → sem_signal(empty)
```

**Why `mutex` alone is not enough:** counts do not protect `head`/`tail`. Two processes can pass
their resource wait and then interleave inside the buffer.

**Why the buffer needs a mutex at all — the `yield()` window.** [kernel/ubuf.c](./lab3/kernel/ubuf.c):

```c
char ubuf_read(void) {
    char data = ubuf.data[ubuf.head];
    yield();                                  // <-- window
    ubuf.head = (ubuf.head + 1) % UBUF_SIZE;
    return data;
}
void ubuf_write(char val) {
    ubuf.data[ubuf.tail] = val;
    yield();                                  // <-- window
    ubuf.tail = (ubuf.tail + 1) % UBUF_SIZE;
}
```

Reads use `head`, writes use `tail`. The comment above `struct ubuf` says the reverse — **follow the
function bodies**, as the manual warns. Without `mutex`, a producer can be descheduled between
storing the byte and advancing `tail`, and another producer then overwrites the same slot.

**Deadlock argument (a checkpoint question).** If a producer did `sem_wait(mutex)` then
`sem_wait(empty)`: it holds `mutex` while `empty == 0`. Only a consumer can raise `empty`, but the
consumer cannot reach `ubuf_read` because `mutex` is held. Circular wait → hang. Same for a consumer
holding `mutex` and waiting on `filled`.

**Cleanup order:** consumer finishes all 96 reads in the parent → `wait(0)` twice to reap both
producers → `sem_free(mutex)`, `sem_free(filled)`, `sem_free(empty)`. Freed last, after all users
are done.

**What the test proves — and does not.** `T_ASSERT(valid[(unsigned char)tmp])` only checks that each
received byte belongs to the character set of `msg`. It does not count, order, or detect duplicates
or losses. Do not claim it proves correctness of the stream; the correctness argument comes from
counts (`sem_signal(filled)` total = `sem_wait(filled)` total = 96) plus mutual exclusion.

**Wiring detail:** `struct buf_sem` holds three `int` semids and is passed **by value** into the
children. That is fine — the IDs are handles, not the objects.

---

## A6. What you must not change in Lab 3

| File | Rule |
|---|---|
| [kernel/spinlock.c](./lab3/kernel/spinlock.c) / `.h` | Part 1 is analysis only; leave the implementation alone |
| [kernel/ucnt.c](./lab3/kernel/ucnt.c) | counter is deliberately unsynchronised; the point is to protect it from user space |
| [kernel/ubuf.c](./lab3/kernel/ubuf.c) | keep the `yield()` calls, and keep the read/write bodies as they are |
| [user/race_test.c](./lab3/user/race_test.c) | keep `N`, `MSG_SIZE`, `NUM_PROD`, the message, loop counts and assertions; fill the TODOs only |

Pre-existing build fix in both labs: `user/usertests.c`'s `fsfull()` sets `fsblocks` and never reads
it, which `-Werror=unused-but-set-variable` rejects on GCC 16; the variable and its increment were
removed. Unrelated to lab behaviour.

---

# PART B — LAB 4: VIRTUAL MEMORY MANAGEMENT

## B1. Address translation (Sv39)

> **ELI5 —** A three-level phone book. Level 2 says which street directory to open, level 1 says
> which house directory inside it, level 0 says which actual house. The last 12 bits are which room
> inside the house — they are never translated.

**Detail.** Sv39 = 39-bit virtual addresses, 3 levels, 4 KiB pages, 8-byte PTEs.

| Field | Bits (inclusive) | Width | Selects |
|---|---|---|---|
| Level-2 (root) index | 38–30 | 9 | entry in the root page table |
| Level-1 index | 29–21 | 9 | entry in a level-1 page table |
| Level-0 index | 20–12 | 9 | the leaf PTE mapping the page to a frame |
| Page offset | 11–0 | 12 | byte inside the 4096-byte frame |

Each table page holds `4096 / 8 = 512` entries → 9 index bits each. `MAXVA = 1L << 38`
([kernel/riscv.h](./lab4/kernel/riscv.h) L380); bits 63–39 are zero for the user half.

The macros:

```c
#define PXSHIFT(level)  (PGSHIFT+(9*(level)))          // PGSHIFT = 12
#define PX(level, va) ((((uint64)(va)) >> PXSHIFT(level)) & PXMASK)   // PXMASK = 0x1FF
#define PA2PTE(pa)  ((((uint64)pa) >> 12) << 10)
#define PTE2PA(pte) (((pte) >> 10) << 12)
#define PTE_FLAGS(pte) ((pte) & 0x3FF)
```

PTE layout: **bits 53–10 = PPN**, bits 9–0 = flags, of which xv6 defines

| Flag | Bit | Meaning |
|---|---|---|
| `PTE_V` | 0 | valid — the entry may be used |
| `PTE_R` | 1 | readable |
| `PTE_W` | 2 | writable |
| `PTE_X` | 3 | executable |
| `PTE_U` | 4 | user-mode access allowed |

A valid entry **with none of R/W/X** is a *pointer* to the next level (non-leaf).

**`walk()`** ([kernel/vm.c](./lab4/kernel/vm.c) L86–L104):

```c
for(int level = 2; level > 0; level--) {
    pte_t *pte = &pagetable[PX(level, va)];
    if(*pte & PTE_V) pagetable = (pte_t*)PTE2PA(*pte);
    else {
      if(!alloc || (pagetable = (pde_t*)kalloc()) == 0) return 0;
      memset(pagetable, 0, PGSIZE);
      *pte = PA2PTE(pagetable) | PTE_V;
    }
}
return &pagetable[PX(0, va)];
```

Key facts:
- `walk(alloc=1)` may allocate **page-table pages** (frames holding PTEs), never process data frames.
- It returns the **address of the level-0 PTE without checking it** — the entry can be invalid.
- It panics above `MAXVA`.

**`walkaddr()`** (L109–L124) is the safe version used by `copyin`/`copyout`/`copyinstr`: `walk(alloc=0)`,
then reject a missing PTE, an invalid PTE, and an entry without `PTE_U`. That `PTE_U` check is why the
stack guard page is invisible to kernel copies but still visible to a raw `walk()`.

**Worked example** — `va = 0x0000003FC0DEA123`:

```
L2 = (va >> 30) & 0x1FF = 0x0FF
L1 = (va >> 21) & 0x1FF = 0x006
L0 = (va >> 12) & 0x1FF = 0x1EA
offset                  = 0x123
```

So: root[0xFF] → level-1 table[0x006] → level-0 table[0x1EA] → frame + 0x123.

> **ELI5 —** 3 lookups to find the frame, then the offset picks the byte. A TLB hit skips all three.

---

## B2. Pages vs frames

> **ELI5 —** A page is a numbered sheet in your binder (virtual). A frame is a physical tray in the
> cupboard. Same size, different worlds. Two binders can have "sheet 5"; there is only one tray 5.

| Term | Space | Unit | Notes |
|---|---|---|---|
| Page | virtual | 4096 B | what a process names |
| Frame | physical | 4096 B | where data actually sits |
| PTE | — | 8 B | PPN + flags |
| Page table | physical memory | 4096 B per level | itself occupies frames |

`p->sz` is the process size in bytes ([kernel/proc.h](./lab4/kernel/proc.h)); `p->pagetable` is its
user page table; the kernel stack and the trampoline live above `p->sz`.

Paging can only have **internal** fragmentation (partly used last page), never external — the last
page is the only waste.

---

## B3. The eager allocation path (`sbrk` before Lab 4)

> **ELI5 —** Ordering a 30-dish banquet and having all 30 cooked immediately, even if you only eat
> one.

**Detail.** Trace:

```
umalloc morecore()  →  sbrk(n)  →  sys_sbrk()  →  growproc(n)  →  uvmalloc()
```

[kernel/sysproc.c](./lab4/kernel/sysproc.c) `sys_sbrk()`:

```c
argint(0, &n);
addr = myproc()->sz;             // old break
if(growproc(n) < 0) return -1;
return addr;                     // sbrk returns the PREVIOUS break
```

`growproc(n)` stock:

```c
if(n > 0){
  if((sz = uvmalloc(p->pagetable, sz, sz + n, PTE_W)) == 0) return -1;
} else if(n < 0){
  sz = uvmdealloc(p->pagetable, sz, sz + n);
}
p->sz = sz;
```

`uvmalloc` per page: `kalloc()` → `memset(..., 0, PGSIZE)` → `mappages(..., PTE_R|PTE_U|xperm)`;
on failure it frees what it mapped and returns 0. `mappages` calls `walk(..., 1)` (creating missing
page-table pages) and panics if the leaf is already valid.

Semantics to quote: positive `n` grows (eagerly, initially), `n == 0` returns the old break without
growing, negative `n` shrinks and frees; a successful call always returns the **old** break.

---

## B4. `countvp()` and `countpp()`

> **ELI5 —** `countvp` counts the pages in your binder (all of them, even the half-used last sheet).
> `countpp` counts how many actual trays in the cupboard are holding your stuff — the guard-page
> tray counts, because a tray is used even though you are not allowed to touch it.

**Detail.** Both describe the current process (`myproc()`), range `[0, p->sz)`.

```c
uint64 sys_countvp(void) {
  return PGROUNDUP(myproc()->sz) / PGSIZE;
}

uint64 sys_countpp(void) {
  struct proc *p = myproc();
  uint64 npages = PGROUNDUP(p->sz) / PGSIZE;
  uint64 n = 0;
  for(uint64 a = 0; a < npages * PGSIZE; a += PGSIZE){
    pte_t *pte = walk(p->pagetable, a, 0);      // alloc = 0: inspect only
    if(pte == 0 || (*pte & PTE_V) == 0) continue;
    if(PTE_FLAGS(*pte) == PTE_V) continue;      // non-leaf pointer, not a data frame
    n++;
  }
  return n;
}
```

Rules encoded:

| Question | Answer | Why |
|---|---|---|
| Partly used final page? | counts as 1 | `PGROUNDUP` |
| Guard page counted? | **yes**, in both | it has a valid PTE and a frame; only `PTE_U` is cleared |
| Page-table frames counted? | no | they are not mapped by any PTE in the user range |
| `TRAMPOLINE` / `TRAPFRAME` counted? | no | they sit above `p->sz` |
| Allocations triggered? | none | `walk(..., 0)` |

Why the guard page matters: `exec()` maps `USERSTACK + 1` pages and clears `PTE_U` on the lowest one
([kernel/exec.c](./lab4/kernel/exec.c) L83–L86, `uvmclear()`), so the guard has a frame but is not
user-accessible. `countpp` counts frames, not permissions.

Syscall wiring: `SYS_countvp = 22`, `SYS_countpp = 23`; dispatch in `syscall.c`; stubs in
`user/usys.pl`; declarations already in `user/user.h`; placeholders removed from `lazytest.c`.

---

## B5. Page faults and the trap path

> **ELI5 —** A smoke alarm. The CPU smells smoke, jumps to a fixed emergency exit (the trampoline),
> the kernel reads the alarm panel (`scause`, `stval`, `sepc`), decides, and either fixes the room
> and re-runs your instruction — or escorts you out.

**Detail.** [kernel/trap.c](./lab4/kernel/trap.c) `usertrap()`:

```c
p->trapframe->epc = r_sepc();

if(r_scause() == 8){                 // system call
    p->trapframe->epc += 4;          // skip the ecall
    intr_on();
    syscall();
} else if((which_dev = devintr()) != 0){
    // interrupt (timer etc.)
} else if(r_scause() == 13 || r_scause() == 15){
    // load / store page fault
} else {
    // unexpected: kill
}
...
if(which_dev == 2) yield();          // timer: give up the CPU
usertrapret();
```

| `scause` | Meaning |
|---|---|
| 8 | environment call from user (syscall) |
| 12 | instruction page fault |
| 13 | load page fault |
| 15 | store/AMO page fault |
| `0x8000…0005` | supervisor timer interrupt (MSB set → interrupt, not exception) |

Three registers, three different questions:

| Register | Answers |
|---|---|
| `scause` | *why* did we trap |
| `stval` | *which virtual address* faulted |
| `sepc` | *which instruction* caused it |

**The trampoline** ([kernel/trampoline.S](./lab4/kernel/trampoline.S)): `uservec` saves user
registers into `p->trapframe` and switches to the kernel page table; `userret` restores and switches
back. It is mapped at the *same* virtual address (`TRAMPOLINE = MAXVA - PGSIZE`) in both page tables,
so execution continues across the `satp` switch.

**The `epc` rule — the single most examinable detail:**

| Path | `epc` | Effect on return |
|---|---|---|
| System call | `+4` | return to the instruction after `ecall` |
| Repaired page fault | unchanged | re-execute the faulting load/store |
| Fatal fault | unchanged, then `setkilled` | process exits, never returns |

If a lazy handler advanced `epc`, the faulting access would be **skipped** (wrong data / silent
corruption) and the page might never be mapped. If a syscall handler did *not* advance `epc`, the
`ecall` would loop forever.

**`fault`** ([user/fault.c](./lab4/user/fault.c)) takes `read` or `write`, computes
`target = PGROUNDUP(sbrk(0))`, prints pid/break/target/mode, then performs one `volatile` access. It
never reserves the page, so the access must stay invalid even after lazy allocation.

---

## B6. Lazy allocation

> **ELI5 —** You reserve a table at a restaurant without the kitchen cooking anything. When you
> actually order a dish (first touch), the kitchen cooks it (allocates a frame). Never order, never
> cook. Cancel the booking and nothing is thrown away.

**Detail.** Two changes.

**(1) Reserve, don't map** — [kernel/proc.c](./lab4/kernel/proc.c) `growproc()`:

```c
if(n > 0){
    if(sz + n < sz || sz + n >= TRAMPOLINE)   // wrap, or reach trap mappings
      return -1;
    sz += n;                                   // no uvmalloc()
} else if(n < 0){
    sz = uvmdealloc(p->pagetable, sz, sz + n);
}
p->sz = sz;
```

`sz + n < sz` catches unsigned wraparound; `>= TRAMPOLINE` keeps the break away from
`TRAMPOLINE`/`TRAPFRAME` (`MAXVA - PGSIZE`, `MAXVA - 2*PGSIZE`). No PTE and no frame is created; the
range is a hole.

**(2) Repair the first touch** — `usertrap()` load/store branch:

```c
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
    if(mem == 0){ setkilled(p); }
    else {
      memset(mem, 0, PGSIZE);
      if(mappages(p->pagetable, PGROUNDDOWN(va), PGSIZE, (uint64)mem,
                  PTE_W|PTE_R|PTE_U) != 0){
        kfree(mem);
        setkilled(p);
      }
    }
} else {
    printf("usertrap(): %s page fault pid=%d va=0x%lx sepc=0x%lx\n", ...);
    setkilled(p);
}
```

Classification truth table — memorise this:

| Fault address | PTE state | Verdict |
|---|---|---|
| `va < p->sz` | missing table, or invalid level-0 PTE | **lazy**: allocate + map + retry |
| `va < p->sz` | valid PTE **without** `PTE_U` (guard page) | **protection fault**: kill |
| `va >= p->sz` | anything | **out of range**: kill (this is `fault`) |
| `va >= MAXVA` | — | kill |

Why each detail is there:

- `va < p->sz` **before** `PGROUNDDOWN`: rounding first could pull in a page that starts below `sz`
  but whose address is outside the reserved range.
- `walk(..., 0)` not `walkaddr`: `walkaddr` also rejects `!PTE_U` and returns a physical address, so
  it cannot distinguish "absent" from "protected".
- `PGROUNDDOWN(va)` because `mappages` panics on unaligned `va`.
- `kalloc` + `memset` + `mappages` mirrors `uvmalloc`, so a lazy page is zero-filled like an eager one.
- Free the frame if `mappages` fails; otherwise mark killed — never leak or half-map.
- Do **not** advance `epc`: the load/store must be retried.

**Rollback note:** if `mappages` fails part-way it can have created intermediate page-table pages;
those are reclaimed later by `freewalk` when the process exits.

---

## B7. Reclaiming a partly allocated heap

> **ELI5 —** Empty trays in the cupboard should be skipped when cleaning up, not treated as a
> disaster. But a tray that is actually a stack of smaller trays (a page table) is still a bug if you
> try to throw it out as food.

**Detail.** [kernel/vm.c](./lab4/kernel/vm.c) `uvmunmap()`:

```c
for(a = va; a < va + npages*PGSIZE; a += PGSIZE){
    if((pte = walk(pagetable, a, 0)) == 0)
      continue;                       // no intermediate page table at all
    if((*pte & PTE_V) == 0)
      continue;                       // invalid level-0 entry: never touched
    if(PTE_FLAGS(*pte) == PTE_V)
      panic("uvmunmap: not a leaf");   // retained: pointer to another table
    if(do_free){
      uint64 pa = PTE2PA(*pte);
      kfree((void*)pa);
    }
    *pte = 0;
}
```

The two `continue`s only convert the old panics into "skip the hole". The not-a-leaf panic stays — a
valid entry with no R/W/X would mean unmapping a page *table*, which is a kernel bug.

`uvmdealloc(old, new)` computes `npages = (PGROUNDUP(old) - PGROUNDUP(new)) / PGSIZE` and calls
`uvmunmap(PGROUNDUP(new), npages, 1)`. Both `sbrk(-n)` and process exit (`uvmfree`) go through it, so
both tolerate untouched holes. `freewalk()` then releases the page-table pages that do exist.

---

## B8. The numbers from Lab 4

| Point | VP | PP | Reading |
|---|---|---|---|
| Start (eager or lazy) | 4 | 4 | 2 program pages + 1 guard + 1 stack (`USERSTACK = 1`) |
| After `sbrk(30 * 4096)`, **eager** | 34 | **34** | frames allocated immediately → "PP count changed immediately" |
| After touching, **eager** | 34 | 34 | nothing new; the final "success" is a **false positive** |
| After `sbrk(...)`, **lazy** | 34 | **4** | reservation only |
| After touching all 30, **lazy** | 34 | **34** | exactly +30 |
| Partial touch (1 of 30) | 34 | **5** | +1 only, exit without panic |
| After `sbrk(-122880)` | 4 | 4 | old break returned, holes skipped |

Why the eager success line is a false positive: `pp_after_touch - pp_before >= n_pages` evaluates
`34 - 4 >= 30`, counting the increase that happened at `sbrk()` time. Only the intermediate
`After sbrk` line distinguishes eager from lazy.

`fault read` / `fault write` print `target = PGROUNDUP(break) = 0x4000` and the kernel prints
`va=0x4000`; both are killed because `va < p->sz` is false (`p->sz == 0x4000`).

---

## B9. Limits of the Lab 4 solution

Deliberately out of scope (the manual says so):

- `uvmcopy()` still panics on a hole → `fork()` of a process with untouched lazy pages is unsupported.
- `copyin()`/`copyout()` use `walkaddr()`, which returns 0 for an absent page → kernel copies into an
  untouched heap page fail instead of allocating.
- `lazytest` exercises neither path, so a pass does not prove them.
- Concurrency: two threads faulting on the same page simultaneously are not tested.

Optional stack-growth discussion: recognise a fault just below the stack base, allocate a page, move
the guard (clear `PTE_U` on the new lowest page via `uvmclear`), and cap growth so it cannot collide
with the heap.

---

# PART C — HOW THE TWO LABS FIT TOGETHER

| Theme | Lab 3 | Lab 4 |
|---|---|---|
| Kernel object shared by processes | semaphore array (`semid` index) | page table (`p->pagetable`), `p->sz` |
| Syscall boundary | `sem_*` handlers in `sysproc.c` | `sys_sbrk`, `sys_countvp`, `sys_countpp` |
| Per-object lock | `sem->lock` | none needed: page faults happen on the faulting process's own page table |
| Blocking | `sleep(chan, lk)` + `wakeup(chan)` | never blocks; `kalloc` may panic on OOM only in tests |
| Atomic unit | read–modify–write in user space | single instruction retried by the kernel |
| Evidence | counter = 2000, 96 bytes delivered | VP/PP counts, fault diagnostics |

Lecture material **not** exercised by either lab (but examinable): TLB and EMAT arithmetic, page
replacement (FIFO/OPT/LRU/Clock), thrashing and working set, inverted page tables, deadlock
prevention/avoidance (Banker's). Conversely, the labs cover material the textbook chapters do not
show: xv6's `sleep`/`wakeup` protocol and lazy heap allocation.

---

# PART D — TRAPS (learn these as "if you see X, do not say Y")

| # | Trap | Correct version |
|---|---|---|
| 1 | "Disabling interrupts gives mutual exclusion." | It only stops *this* hart being preempted. Cross-CPU exclusion needs the atomic lock. |
| 2 | "`acquire()` could be `if(!locked) locked = 1;`" | Two CPUs can both read 0. Must be one atomic test-and-set. |
| 3 | "`push_off()` = `intr_off()`." | Matched nesting; the outermost `pop_off` restores the original state. |
| 4 | "A spinlock and a semaphore are interchangeable." | Spin = busy-wait, no sleep; semaphore = block/wake with a count. |
| 5 | "`wakeup()` runs the sleeper." | It only sets `RUNNABLE`; the scheduler decides. |
| 6 | "`chan` carries the data." | It is only a matching address. |
| 7 | "`if(value==0) sleep(...)` is fine." | Must recheck: `while (value == 0)`. |
| 8 | "`sleep` sets state before taking `p->lock`." | It takes `p->lock`, *then* releases `lk`, then sets `chan`/`state` — that is what prevents lost wakeups. |
| 9 | "Semaphore values may go negative." | Not here: block at 0, then decrement. `-1` is only the error return. |
| 10 | "`sem_free` wakes waiters." | It only clears `in_use`; free after all users finish. |
| 11 | "`sem_init` is `seminit`." | `sem_init` = user syscall → `sem_alloc`; `seminit` = boot-time array init. |
| 12 | "Protect each syscall separately in `do_work`." | Protect the whole read–modify–write. |
| 13 | "Initial count 0 is safer for a mutex." | Must be 1, or the first waiter deadlocks itself. |
| 14 | "Wait for `empty` while holding `mutex`." | Deadlock: only the locked-out party can free a slot. |
| 15 | "`ubuf` writes to `head`, reads from `tail`." | Comment is reversed: read uses `head`, write uses `tail`. |
| 16 | "The producer-consumer pass proves no loss/reorder." | It checks membership only. |
| 17 | "512 entries per table, so 10 index bits." | 512 → **9** bits; offset is 12. |
| 18 | "Offset bits come from address width." | They come from page size: 4 KiB → 12 bits, always. |
| 19 | "`walk()` allocates data frames." | It allocates only page-table pages, and only with `alloc != 0`. |
| 20 | "`walk()` guarantees a valid leaf." | It returns the leaf PTE unchecked. Use `walkaddr` for validity + `PTE_U`. |
| 21 | "The guard page is not a physical frame." | It has a frame; only `PTE_U` is cleared. `countpp` counts it. |
| 22 | "`countpp` can use `walkaddr()`." | `walkaddr` rejects `!PTE_U` and returns a PA; use `walk(...,0)` and inspect the PTE. |
| 23 | "`sbrk` returns the new break." | It returns the **previous** break; `sbrk(0)` reads it. |
| 24 | "Advance `epc` after repairing a fault." | Never — the instruction must be retried. Only syscalls do `epc += 4`. |
| 25 | "Round the fault address down, then check `va < p->sz`." | Check first, round second. |
| 26 | "A valid PTE always means the access is legal." | `PTE_V` without `PTE_U` = protection fault (guard page). |
| 27 | "`uvmunmap` should panic on a hole." | Skip holes; keep the not-a-leaf panic. |
| 28 | "Lazy allocation supports `fork()`." | `uvmcopy` still panics on holes — out of scope. |
| 29 | "`growproc` only needs to check the return of `uvmalloc`." | In lazy mode it must reject wrap (`sz+n<sz`) and `>= TRAMPOLINE`. |
| 30 | "`lazytest`'s final success line proves laziness." | It is `>=`, so the eager kernel also prints it. Read `After sbrk`. |

---

# PART E — SCENARIO DRILLS (with worked answers)

**E1. Two CPUs, split acquire.** `acquire` is `if (lk->locked == 0) lk->locked = 1;`. Both CPUs are
at t1. What happens, and what fixes it?
<details><summary>Answer</summary>

Both read 0, both write 1, both enter. Interrupts-off cannot help because the interleaving is between
CPUs. Fix: one atomic test-and-set (`amoswap`) so read+write is indivisible, plus a fence so the
critical section's memory ops cannot move before it.
</details>

**E2. Lost wakeup.** `sleep` sets `p->state = SLEEPING` *before* `acquire(&p->lock)`. A signal arrives
between the condition check and the state change. Trace it.
<details><summary>Answer</summary>

Signaller updates the data and calls `wakeup(chan)`, which (under `p->lock`) sees state `RUNNING`
(or `p->chan` unset) and does nothing. The waiter then sets `SLEEPING` and `sched()`s forever. In real
xv6 `p->lock` is acquired **before** `release(lk)` and before `chan`/`state` are set, so `wakeup`
cannot observe the process in the gap. The post-wake recheck loop handles a wake for a consumed
resource.
</details>

**E3. `if` instead of `while`.** `if(sem->value == 0) sleep(sem, &sem->lock); sem->value--;` with two
waiters and one signal. What breaks?
<details><summary>Answer</summary>

xv6's `wakeup()` marks **all** sleepers on the channel `RUNNABLE`, so both waiters return from
`sleep()`. With `if`, both decrement: the first takes 1→0, the second takes 0→−1 and returns success
with no resource. The non-negative invariant is broken and a later `sem_wait` can pass incorrectly.
With `while`, the loser re-tests, sees 0, and sleeps again.
</details>

**E4. Producer waits for space inside the mutex.** Timeline with an empty buffer and a producer
holding `mutex`.
<details><summary>Answer</summary>

`sem_wait(mutex)` succeeds → `sem_wait(empty)` blocks because `empty == 0`. A consumer that would
free a slot must first take `mutex`, which the producer holds. Circular wait: producer holds `mutex`
and waits for `empty`; consumer waits for `mutex`. Nobody proceeds. Correct order: resource wait
*outside*, `mutex` *inside*.
</details>

**E5. Buffer without mutex.** Two producers, one consumer, `empty`/`filled` correct but no `mutex`.
Use the `yield()` placement to show the failure.
<details><summary>Answer</summary>

P1 calls `ubuf_write('a')`: stores at `tail=0`, then `yield()`. P2 runs, stores at `tail=0` (still 0),
`yield()`, advances `tail` to 1. P1 resumes and advances `tail` to 2. Slot 0 holds P2's byte and P1's
byte is lost while `tail` skips slot 1. Counts still balance, so only mutual exclusion prevents it.
</details>

**E6. Address breakdown.** `va = 0x0000000080000ABC`. Give L2/L1/L0/offset and the number of memory
accesses on a TLB miss.
<details><summary>Answer</summary>

L2 = 2, L1 = 0, L0 = 0, offset = 0xABC. Without a TLB: three page-table reads (levels 2, 1, 0) plus
the data access = 4 accesses; with a single-level table it would be 2. With a TLB hit: 1 data access
(TLB lookup is separate/parallel in the EMAT formula).
</details>

**E7. Counting.** `p->sz = 0x5123` on the lazy kernel, with pages at virtual addresses 0, 0x1000,
0x2000, 0x3000, 0x4000 present and nothing mapped at 0x5000. What are `countvp` and `countpp`?
<details><summary>Answer</summary>

`countvp = PGROUNDUP(0x5123)/0x1000 = 0x6000/0x1000 = 6`. `countpp = 5` (the five present leaf
entries). The partly used sixth page is counted virtually but has no frame.
</details>

**E8. Fault at the break.** `p->sz = 0x4000`, a program writes to 0x4000. Does the lazy handler map
it? Why not, and what would the program have to do instead?
<details><summary>Answer</summary>

No: `va < p->sz` is false (`0x4000 < 0x4000` is false), so the process is killed as out of range. The
program must first `sbrk(4096)` (or more) so the address falls inside the reserved range. This is
exactly why `fault` must always terminate while `lazytest` survives.
</details>

**E9. Guard page fault.** A program writes one page *below* the stack. `va < p->sz` is true. What
happens?
<details><summary>Answer</summary>

`walk` finds a **valid** PTE (the guard page) without `PTE_U`. The `lazy` flag stays 0, so the
handler prints a store page fault and kills the process. Correct: that is a protection fault, not a
missing heap page. Mapping it would silently allow stack overflow.
</details>

**E10. `epc` bug.** A lazy handler does `p->trapframe->epc += 4` after mapping. Effect?
<details><summary>Answer</summary>

The faulting load/store is skipped and execution continues with a register holding garbage; the page
is mapped but the intended access never happens. Symptom: `lazytest` counts may still pass while real
programs misbehave. Only the syscall path advances `epc`.
</details>

**E11. `uvmunmap` before the fix.** A process `sbrk`s 30 pages, touches 1, then exits. What did the
stock kernel do, and why does the fix work?
<details><summary>Answer</summary>

Stock `uvmunmap` panicked ("uvmunmap: walk" / "not mapped") on the 29 untouched pages during
`uvmfree`. The fix skips a missing PTE or an invalid level-0 entry, frees only present leaves, and
still panics on a non-leaf entry (which would mean a page table, not data).
</details>

**E12. `fork` after lazy `sbrk`.** Parent reserves 30 pages, touches none, then `fork()`s. What
happens?
<details><summary>Answer</summary>

`uvmcopy` walks each page and panics on the absent ones. Unsupported by design; supporting it means
skipping holes in `uvmcopy` (the child inherits `p->sz` and faults its own pages in), plus teaching
`copyin`/`copyout` to allocate for `va < p->sz`.
</details>

---

# PART F — QUIZ

Answer key in Part G. Aim for closed-book.

## F1. Multiple choice

1. `acquire()` loops on `__sync_lock_test_and_set` because
   a) it is faster than a normal load b) read and write must be one indivisible operation
   c) it disables interrupts d) it wakes sleepers

2. `push_off()`/`pop_off()` are matched because
   a) locks can be taken recursively b) nested critical sections must not re-enable interrupts early
   c) interrupts are per-process d) `pop_off` frees memory

3. A lost wakeup is prevented mainly by
   a) `wakeup` taking the condition lock b) `sleep` holding `p->lock` while publishing `chan`/`state`
   c) disabling interrupts in user space d) using a binary semaphore

4. `wakeup(chan)` sets matching processes to
   a) RUNNING b) RUNNABLE c) SLEEPING d) ZOMBIE

5. `sem_wait` must recheck the value because
   a) `wakeup` reserves the resource b) another waiter may consume it first c) the value can be negative
   d) the lock is unfair

6. The initial value of the producer's `empty` semaphore is
   a) 0 b) 1 c) `UBUF_SIZE` d) 96

7. In `ubuf`, `yield()` sits between
   a) the wait and the signal b) the slot access and the index update c) two `fork`s d) two syscalls

8. `countvp` for `p->sz = 0x5123` is
   a) 5 b) 6 c) 0x5123 d) 4

9. `countpp` counts the guard page because
   a) it has `PTE_U` b) it has a valid PTE and a frame c) it is above `p->sz` d) `walkaddr` returns it

10. `walk(pagetable, va, 0)` returns 0 only when
    a) the leaf PTE is invalid b) an intermediate page table is missing
    c) the leaf lacks `PTE_U` d) the page is swapped out

11. `mappages` panics if
    a) `va` is unaligned b) the leaf is already valid c) `size == 0` d) all of the above

12. A repaired page fault returns to
    a) the next instruction b) the same instruction c) the shell d) `usertrapret`'s caller

13. `sbrk(4096)` returns
    a) the new break b) the previous break c) 4096 d) 0

14. After lazy `sbrk(30 pages)` and touching all 30, `PP` changes by
    a) 0 b) +30 c) +34 d) −30

15. `uvmunmap` must still panic when a valid entry
    a) is absent b) has no R/W/X (points to a page table) c) belongs to the guard page d) is dirty

## F2. Short answer

16. Why is `intr_off()` insufficient for mutual exclusion on a 3-CPU machine?
17. Name the two locks used by `sleep()` and say what each protects.
18. Why must a producer wait on `empty` *before* taking `mutex`?
19. Give the exact call orders for one byte through the producer and the consumer.
20. What three things does `sem_free` *not* do?
21. State the Sv39 bit ranges for L2, L1, L0 and the offset.
22. Distinguish `walk()` from `walkaddr()` in one sentence each.
23. What does `PTE_FLAGS(*pte) == PTE_V` mean, and why is it checked?
24. Why does the guard page count in `countpp` but not appear accessible to user code?
25. Give the four checks that make a fault "lazy-eligible".
26. Why must `PGROUNDDOWN(va)` be used for `mappages` but not for the range check?
27. Why does the lazy handler free the frame when `mappages` fails?
28. Why is `lazytest`'s last success message not proof of laziness?
29. Which two paths still break with a lazily reserved heap?
30. Explain in two sentences why `sem_getvalue` needs the lock.

---

# PART G — ANSWER KEY

## F1

1. **b** — atomicity of check-and-set.
2. **b** — nesting; only the outermost restore re-enables interrupts.
3. **b** — `p->lock` closes the publish/sleep gap; the condition lock alone does not.
4. **b** — RUNNABLE; the scheduler runs it later.
5. **b** — wakeups reserve nothing.
6. **c** — 16, one per slot.
7. **b** — after the slot access, before the index update.
8. **b** — `PGROUNDUP(0x5123) = 0x6000`.
9. **b** — frame exists; only `PTE_U` is cleared.
10. **b** — with `alloc == 0` it returns 0 when a level-2/level-1 entry is invalid; if the tables
    exist, it returns the address of the (possibly invalid) leaf PTE, so callers must still test
    `PTE_V`.
11. **d** — all three are panics.
12. **b** — same instruction, because `epc` is untouched.
13. **b** — the previous break.
14. **b** — +30, matching the 30 touched pages.
15. **b** — a non-leaf entry means a page table, not data.

## F2

16. It clears `SIE` only on the calling hart; another hart runs the same instructions on the same
    memory. Exclusion comes from the shared, atomically updated `locked` word.
17. `lk` (the caller's condition lock) protects the shared data and the condition; `p->lock` protects
    the process's `state` and `chan` plus the scheduling transition.
18. Because a free slot can only be produced by a consumer, and the consumer needs `mutex` to reach
    the buffer. Holding `mutex` while waiting creates a circular wait.
19. Producer: `wait(empty)`, `wait(mutex)`, `ubuf_write`, `signal(mutex)`, `signal(filled)`.
    Consumer: `wait(filled)`, `wait(mutex)`, `ubuf_read`, `signal(mutex)`, `signal(empty)`.
20. It does not wait for users, does not wake sleepers, and does not reset `value` (it only clears
    `in_use`); it also does not take the per-semaphore lock.
21. L2 = 38–30, L1 = 29–21, L0 = 20–12, offset = 11–0.
22. `walk` returns the address of the level-0 PTE, allocating page-table pages when asked, without
    validating the leaf; `walkaddr` never allocates and returns a physical address only if the leaf
    is valid and has `PTE_U`.
23. A valid entry with no R/W/X — i.e. a pointer to the next-level page table; the check avoids
    treating (and freeing) a page table as a data frame.
24. It has a valid PTE and a real frame, but `exec()`/`uvmclear()` cleared `PTE_U`, so user accesses
    trap while `countpp` only counts valid mapped frames.
25. `scause` is 13 or 15; `va < p->sz` and `va < MAXVA`; `walk(...,0)` returns 0 or a non-valid PTE.
26. The range check must use the exact faulting address so rounding cannot pull in a page outside the
    reservation; `mappages` requires a page-aligned `va`, hence the round-down.
27. Otherwise the frame leaks: no PTE refers to it, so nothing will ever free it.
28. Because the check is `pp_after_touch - pp_before >= n_pages`, which the eager kernel also
    satisfies (frames were allocated at `sbrk` time).
29. `fork()` (`uvmcopy` panics on holes) and kernel copies (`copyin`/`copyout` via `walkaddr` return 0).
30. Otherwise the read could interleave with `sem_signal`/`sem_wait` and return a torn/stale count;
    the lock makes the read a snapshot consistent with the semaphore's own updates.

---

# PART H — CHEAT SHEET

```
PGSIZE 4096   PTE 8B   entries/table 512   index bits 9   offset bits 12
Sv39: L2 38-30 | L1 29-21 | L0 20-12 | offset 11-0
MAXVA 0x40_0000_0000   TRAMPOLINE 0x3F_FFFF_F000   TRAPFRAME 0x3F_FFFF_E000
PTE_V 1 PTE_R 2 PTE_W 4 PTE_X 8 PTE_U 16      PTE_FLAGS = pte & 0x3FF
scause: 8 syscall | 12 instr fault | 13 load fault | 15 store fault | 0x800...5 timer

Lab 3: MAX_SEMAPHORES 32 | UBUF_SIZE 16 | MSG_SIZE 48 | NUM_PROD 2 | reads 96 | N 1000 | expected 2000
       sem syscalls 26..30 | guard: value never negative | free after all users
Lab 4: initial VP=PP=4 | lazy after sbrk(30) VP=34 PP=4 | after touch PP=34 | partial PP=5
       syscalls countvp 22 countpp 23 | USERSTACK 1 | guard = lowest stack page, PTE_U cleared
```

**Five sentences that answer most lab questions:**

1. A spinlock's value is checked and set by one atomic instruction; interrupts-off only protects the
   local hart from preemption.
2. `sleep` publishes `chan` and `SLEEPING` while holding `p->lock`, which `wakeup` must also take, so
   no wakeup can slip between the condition check and sleeping.
3. A semaphore blocks at zero and decrements after waking, and the waiter rechecks in a loop because
   a wakeup reserves nothing.
4. Sv39 walks three 512-entry page tables using 9-bit indexes and never translates the low 12 bits.
5. Lazy allocation moves `p->sz` without mapping; the fault handler maps a zeroed frame only when the
   address is below `p->sz`, has no valid PTE, and then retries the same instruction.

---

# PART I — ASK-GEMINI PROMPTS & CHECKPOINTS (all answered)

The manuals contain **10 "Ask Gemini Notebook" prompts** (6 in Lab 3, 4 in Lab 4) and **10 checkpoints**
(CP0–CP4 in each). Every one is restated and answered below; the "Depth" pointers lead to the long
treatment in Parts A–B, and **I.4–I.7** hold the worked detail behind the short answers.

## I.1 Lab 3 — the six Ask-Gemini prompts

### P1 — Spinlock internals and the two-CPU interleaving *(p. 4)*

> Identify the lock state, the atomic acquisition operation and the interrupt-management calls; then
> construct an interleaving in which two CPUs both enter a critical section if acquisition used a
> separate read and write.

**Answer.** The state is `uint locked` (plus `name` and the owning `cpu`). Acquisition is
`while(__sync_lock_test_and_set(&lk->locked, 1) != 0);` — one `amoswap.w.aq` instruction — followed by
`__sync_synchronize()` (a `fence`). Interrupt management is `push_off()` on entry and `pop_off()` on
exit, nested through `noff`/`intena` so only the outermost release restores interrupts. With
`if(lk->locked == 0) lk->locked = 1;`, CPU A reads 0, CPU B reads 0, A writes 1, B writes 1, and both
enter. Test-and-set makes the read and the write one indivisible operation, so exactly one CPU can
observe 0.
*Depth: **A2**.*

### P2 — `sleep`/`wakeup` trace and the lost wakeup *(p. 5)*

> Trace `sleep(chan, lk)` and `wakeup(chan)`; say where the condition lock and each process lock are
> held, released and reacquired; explain how that prevents a lost wakeup, which state transitions
> occur, and why the waiter rechecks after waking.

**Answer.** `sleep` takes `p->lock`, releases `lk`, sets `p->chan = chan`, sets `SLEEPING`, calls
`sched()`, then on return clears `chan`, releases `p->lock` and reacquires `lk`. `wakeup` takes each
process's `p->lock`, sets matching sleepers to `RUNNABLE`, and releases it; it never touches `lk`. The
ordering matters because `wakeup` cannot inspect the state without `p->lock`: it either sees the
process before it sleeps (and the condition recheck catches the change) or sees it `SLEEPING` and wakes
it. Transitions: `RUNNING → SLEEPING → RUNNABLE → RUNNING`. The recheck is required because `wakeup`
reserves nothing — another process may take the resource first.
*Depth: **A3**.*

### P3 — The `kernel/semaphore.c` TODOs *(p. 7)*

> Explain the TODO comments and how the supplied semaphore spinlock plus `sleep()`/`wakeup()` support
> the required behaviour.

**Answer.** The TODOs ask for: retrieve `struct semaphore *sem = &semaphores[semid]`; `sleep(sem, &sem->lock)`
while `value == 0`; decrement under the lock; increment and `wakeup(sem)`; and a locked read for
`sem_getvalue`. `sem->lock` makes every value update atomic, `sleep` releases it while blocked and
reacquires it before returning, and using the semaphore's address as the channel wakes exactly the
waiters of that semaphore. The supplied `-1` error returns and 32-slot table stay untouched.
*Depth: **A4**.*

### P4 — Lost-update interleaving and the shared `semid` *(p. 8)*

> Construct the lost-update interleaving; say which operations form one critical section; explain why
> the child's copied `semid` still identifies the same kernel semaphore; reason about initial count,
> protected region and cleanup order.

**Answer.** A reads 10, B reads 10, A writes 11, B writes 11 — one increment is lost. The critical
section is both syscalls together (`ucnt_get` **and** `ucnt_set`), because entering the kernel per call
does not make the pair atomic. `semid` is an index into the kernel's `semaphores[32]` array inherited
across `fork()`, so both processes name the same kernel object. Initial count is 1 (mutex); wait/signal
wrap the whole read–modify–write; free only after the child is reaped.
*Depth: **A1**, **A5.2**.*

### P5 — Producer/consumer counts, ordering and deadlock *(p. 10)*

> Derive the semaphore counts and the order of waits and signals; explain how the `yield()` calls
> expose missing mutual exclusion and why waiting for space or data while holding the mutex deadlocks.

**Answer.** `empty = 16` (`UBUF_SIZE`, all slots free), `filled = 0`, `mutex = 1`. Producer:
`wait(empty) → wait(mutex) → ubuf_write → signal(mutex) → signal(filled)`. Consumer:
`wait(filled) → wait(mutex) → ubuf_read → signal(mutex) → signal(empty)`. `ubuf_write` stores at
`tail`, then `yield()`s **before** advancing `tail`, so without `mutex` a second producer overwrites the
same slot. Waiting for `empty`/`filled` while holding `mutex` creates a circular wait: the only process
that can change the condition needs the mutex the waiter is holding.
*Depth: **A5.3**.*

### P6 — Diagnosing a failing or hanging `producer_consumer` *(p. 10)*

> Given a failure or hang, produce a diagnostic checklist for count initialisation, lock lifetime, wait
> channels, wait/signal ordering and cleanup, and explain what a Ctrl-p snapshot can show.

**Answer (summary).** Counts `16/0/1` and all `sem_init` calls before the fork loop; never free while a
user is alive; `empty`/`filled` must not be swapped; resource waits outside the mutex; `wait(0)` twice
before the three `sem_free`. Ctrl-p calls `procdump()`, which prints only `pid state name` in this
build: all-`sleep` means blocked (deadlock/lost wakeup), `runble`/`run` means spinning/livelock, and a
`zombie` means an un-reaped child. It cannot reveal the channel or the count.
*Full checklist: **I.5**.*

## I.2 Lab 4 — the four Ask-Gemini prompts

### P1 — Tracing `walk` and `walkaddr` *(p. 5)*

> Trace both functions; how are the three indexes used; what does each return; when may `walk` allocate
> a frame for a page table; how does a page-table frame differ from a data frame?

**Answer.** `PX(2, va)`, `PX(1, va)`, `PX(0, va)` select 9-bit entries at levels 2, 1 and 0; the low 12
bits are the offset. `walk` returns `&pagetable[PX(0, va)]` — a pointer to the level-0 PTE, whose
validity it does **not** check. With `alloc != 0` and a missing intermediate entry it calls `kalloc()`,
zeroes the new page, and installs a pointer entry (`PA2PTE(...) | PTE_V`, no R/W/X). `walkaddr` calls
`walk(..., 0)` and returns a physical address only if the leaf is valid and has `PTE_U`, else 0. A
page-table frame is reachable only through another PTE and has no R/W/X (non-leaf); a data frame is a
leaf PTE with permissions, i.e. something a user virtual address can name.
*Depth: **B1**, **B2**.*

### P2 — Counting rules and syscall wiring *(p. 8)*

> Reason about the required counts; why does the guard page count without `PTE_U`; how can mappings be
> inspected without creating them; which files connect a user call to its kernel handler?

**Answer.** `countvp = PGROUNDUP(p->sz)/PGSIZE` (a partly used last page still counts). `countpp` walks
every page in `[0, p->sz)` with `walk(..., 0)`, skips missing tables and invalid PTEs, skips non-leaf
entries, and counts the rest. The guard page has a valid PTE and a real frame — only `PTE_U` was
cleared by `uvmclear()` — so it counts as a frame but is not user-accessible. Inspect without creating
by always passing `alloc = 0`. The chain is `user.h` → `usys.pl` (generates `usys.S`) → `syscall.h`
(number) → `syscall.c` (dispatch table) → `sysproc.c` (handler), with prototypes in `defs.h`.
*Depth: **B4**, **I.6**.*

### P3 — Page fault through the trampoline *(p. 10)*

> Trace a load or store fault through `trampoline.S` and `trap.c`; which register holds the faulting
> address and which the instruction; where is the process killed; why must the trampoline stay mapped?

**Answer.** `uservec` saves the user registers into `p->trapframe`, loads the kernel page table into
`satp`, and jumps to `usertrap`. There `scause` is 13 (load) or 15 (store), `stval` holds the faulting
virtual address, and `sepc` holds the faulting instruction's address. A non-repairable fault calls
`setkilled(p)`, and `usertrap` then `exit(-1)`s the process while the shell continues. The trampoline is
mapped at the same virtual address (`MAXVA - PGSIZE`) in both page tables so the instruction stream
stays valid across the `satp` switch.
*Depth: **B5**.*

### P4 — Planning lazy allocation *(p. 12)*

> Plan lazy heap allocation using `sys_sbrk`, `usertrap` and the VM helpers; how do you distinguish an
> absent heap page from a protection fault; what must happen before mapping, on allocation failure, and
> before retrying the instruction?

**Answer.** `growproc` raises `p->sz` (rejecting wrap and `>= TRAMPOLINE`) without mapping. On a
load/store fault, the handler treats the page as lazy only if `va < p->sz && va < MAXVA` **and**
`walk(..., 0)` yields no valid leaf. Before mapping: `kalloc`, `memset` to zero, and `mappages` at
`PGROUNDDOWN(va)` with `PTE_W|PTE_R|PTE_U`. On failure: `kfree` the new frame and mark the process
killed. Before retrying: leave `p->trapframe->epc` unchanged so the same load/store re-executes.
*Depth: **B6**.*

## I.3 Checkpoints — every bullet answered

### Lab 3 — CP0 (p. 3)

1. **Confirm the `lab3` branch and a three-CPU boot.** `git branch --show-current` prints `lab3`;
   `make CPUS=3 qemu` prints `hart 2 starting` / `hart 1 starting` and reaches `$`.
2. **Locate `kernel/spinlock.c`, `kernel/proc.c`, `kernel/semaphore.c`, `kernel/ucnt.c`,
   `kernel/ubuf.c`, `user/race_test.c`.** Roles and line numbers are in **I.4.1**.
3. **Identify how to select one test function in `main()`.** Keep that call and `exit(0)`; comment out
   the other two calls **and** the `ALL TESTS PASSED` print; leave definitions and assertions intact
   (**I.4.2**).

### Lab 3 — CP1 (p. 5)

1. **Compare spinning with sleeping, stating assumptions.** ~10 cycles: spin (a wakeup costs two
   context switches). ~10,000 cycles: sleep (spinning wastes a core). Assumes the holder makes progress
   (or runs elsewhere) and wakeup latency is small relative to the wait — see **I.7**.
2. **Identify the condition lock, wait channel and process lock.** Condition lock = the caller's `lk`
   (`&sem->lock` in the semaphore); wait channel = `p->chan`, set to the semaphore's address; process
   lock = `p->lock`, protecting `state` and `chan` (**A3**).
3. **Why must a woken process recheck?** `wakeup` only sets `RUNNABLE`; it reserves nothing, and another
   waiter may consume the value first, so the test is `while`, not `if`.
4. **Why can't separate reads and writes replace atomic acquisition?** Two CPUs can both read 0 and
   both write 1; a single test-and-set makes the pair indivisible (**A2**).

### Lab 3 — CP2 (p. 7)

1. **Distinguish `sem_init`, `seminit`, `sem_alloc`.** `sem_init` is the user syscall; it reaches
   `sem_alloc(value)`, which scans the 32-slot table under `sem_table_lock` and returns the index.
   `seminit()` runs at boot to initialise the table lock and per-semaphore locks (**A4**).
2. **Which lock and channel do wait/signal use?** `sem->lock` for the value update; the channel is
   `sem` (the slot's address), so only waiters on that semaphore wake.
3. **Why recheck for a positive value after waking?** Because wakeups are advisory; the count may have
   been taken again, and a decrease from 0 would break the non-negative invariant.
4. **Show the basic sequence and what it leaves untested.** `sem_init(1)` → `getvalue == 1` →
   `wait` → `0` → `signal` → `1`. It never blocks a second waiter, so the sleeping path is untested
   (**A5.1**).
5. **When is it safe to free?** Only after every user has finished; `sem_free` clears `in_use` and does
   not wake sleepers, so freeing early strands them.

### Lab 3 — CP3 (p. 8)

1. **Demonstrate the lost update.** A reads 10, B reads 10, A writes 11, B writes 11; final 11 instead
   of 12 (**A1**).
2. **Why is protecting the two syscalls separately insufficient?** The lock is released between
   `ucnt_get` and `ucnt_set`, leaving the interleaving intact.
3. **Expected final count and the shared semaphore.** `2 * N = 2000`; the `semid` created **before**
   `fork()`, so parent and child name the same kernel object.
4. **Why does the parent wait before validating and freeing?** `wait(0)` guarantees the child has
   finished its increments, so the counter is final; and freeing cannot strand a user
   (**A5.2**).

### Lab 3 — CP4 (p. 10)

1. **Each semaphore's role and initial value.** `empty = 16` (free slots), `filled = 0` (data
   available), `mutex = 1` (unlocked) — derived from an empty 16-slot buffer (**A5.3**).
2. **Trace one byte each way.** Producer: `empty 16→15`, `mutex 1→0`, write, `mutex→1`, `filled 0→1`.
   Consumer: `filled 1→0`, `mutex 1→0`, read, `mutex→1`, `empty 15→16`.
3. **Why don't counts protect the indices?** `head`/`tail` are shared; counts say *how many* slots are
   free/full, not that a read–modify of the index is atomic — hence the `yield()` window.
4. **Show completion with both producers reaped.** Consumer performs 96 reads, then `wait(0)` twice,
   then `sem_free` on all three.
5. **Limits of the membership check.** `valid[tmp]` only proves each byte is in `msg`'s character set;
   it does not detect duplication, loss or reordering.

### Lab 4 — CP0 (p. 3)

1. **Confirm the checkout and that it boots.** `git branch --show-current` → `lab4`;
   `make CPUS=3 qemu` reaches `init: starting sh` (**I.4.3**).
2. **Locate `sys_sbrk()`, `walk()`, `usertrap()` and the two placeholders.** `sysproc.c` L39, `vm.c`
   L86, `trap.c` L37; the placeholders are two `return 0` functions in `user/lazytest.c` on a fresh
   checkout (already deleted here).

### Lab 4 — CP1 (p. 6)

1. **Define virtual address, PTE, physical frame.** A virtual address is what the CPU generates and the
   program names; a PTE is an 8-byte entry holding a 44-bit PPN plus flags; a frame is a 4096-byte
   physical block of RAM (**B1**, **B2**).
2. **What may `walk` allocate, and how does that differ from heap data?** Only page-table pages, and
   only with `alloc != 0`; it never allocates a data frame, which is what `uvmalloc` does with
   `kalloc` + `memset` + `mappages` (**B1**, **B3**).
3. **Trace a positive `sbrk` and where eager allocation happens.** `umalloc` → `sbrk` → `sys_sbrk` →
   `growproc` → `uvmalloc` → `kalloc`/`memset`/`mappages` (**B3**).

### Lab 4 — CP2 (p. 8)

1. **Explain the counting boundary and the guard page.** `[0, p->sz)` rounded up; the guard page is
   inside it, has a frame, and counts in both `countvp` and `countpp`, even though `PTE_U` is cleared
   (**B4**).
2. **Show `lazytest` reaches the syscalls, not the placeholders.** A fresh checkout prints
   `Before: VP=0, PP=0` (placeholders); the finished tree prints `VP=4, PP=4`, which can only come from
   the syscalls (**I.6**).
3. **Explain the eager counts within one run.** `sbrk(30 pages)` gives `VP +30` and `PP +30`
   immediately; touching changes nothing further, and the final "success" line is a false positive
   because it uses `>=` (**B8**).

### Lab 4 — CP3 (p. 10)

1. **Demonstrate a fault and distinguish address from instruction.** `fault read`/`fault write` print
   `target 0x4000`; the kernel prints `va=0x4000` (`stval`) and `sepc=0xc2`/`0x94` (the instruction)
   (**B5**, **B8**).
2. **Why does `fault` select an unallocated page, and how does its target relate to the diagnostic?**
   It computes `PGROUNDUP(sbrk(0))` and never calls a positive `sbrk`, so `target == p->sz` and the
   handler's `va < p->sz` test fails; the printed target equals the printed `va`.
3. **Trace trap entry and the shared trampoline.** `uservec` saves registers, switches `satp`, enters
   `usertrap`; `userret` restores and returns. The trampoline is mapped at the same VA in both page
   tables so execution survives the switch.

### Lab 4 — CP4 (p. 13)

1. **Show reservation then allocation on first touch.** After `sbrk(30 pages)`: `VP +30`, `PP +0`
   (`PP=4`); after touching all 30: `PP +30` (`PP=34`) (**B8**).
2. **How does the handler distinguish a missing heap page from a protection fault?** Missing = inside
   `p->sz` **and** no valid level-0 PTE; protection = a valid PTE without `PTE_U` (guard page); outside
   the range = kill (**B6**).
3. **Why does a repaired fault retry the same instruction?** `epc` is not advanced, so `sret` returns to
   the faulting load/store; only the syscall path does `epc += 4`.
4. **Show a partially touched heap is released without panic.** Touching 1 of 30 pages gives `PP=5`,
   then exit/shrink skips the 29 holes because `uvmunmap` continues on missing/invalid PTEs (**B7**).
5. **Why does lazy allocation save memory, and what are the test's limits?** Untouched reserved pages
   never get frames; `lazytest` does not test `fork()`, kernel `copyin`/`copyout` on untouched pages
   (`uvmcopy` still panics), or concurrent faults (**B9**).

## I.4 Checkpoint 0 — the concrete checks

### I.4.1 Lab 3: branch, boot, files

```
host$ git checkout lab3 && git branch --show-current      → lab3
host$ make CPUS=3 qemu
xv6 kernel is booting
hart 2 starting
hart 1 starting
init: starting sh
```

| File | What you must be able to point at |
|---|---|
| [kernel/spinlock.c](./lab3/kernel/spinlock.c) / `.h` | `struct spinlock.locked`; `acquire` L22 (atomic swap + `push_off`), `release` L47 |
| [kernel/proc.c](./lab3/kernel/proc.c) | `sleep` L550, `wakeup` L581 |
| [kernel/semaphore.c](./lab3/kernel/semaphore.c) | array + `sem_table_lock`; `sem_wait` L60, `sem_signal` L77, `sem_getvalue` L93 |
| [kernel/ucnt.c](./lab3/kernel/ucnt.c) | `ucnt_get`/`ucnt_set` over `int ucnt[16]` |
| [kernel/ubuf.c](./lab3/kernel/ubuf.c) | 16-slot ring, `head` for reads, `tail` for writes, `yield()` windows |
| [user/race_test.c](./lab3/user/race_test.c) | `sem_basic`, `race_test`, `producer_consumer`, `N = 1000` |

Three CPUs matter: with `CPUS=1` the race is much harder to reproduce and the spinlock's cross-CPU
purpose is invisible.

### I.4.2 Lab 3: selecting one test function

In `main()` of [user/race_test.c](./lab3/user/race_test.c) three calls run in order:

```c
int main() {
    sem_basic();
    race_test();
    producer_consumer();
    printf("ALL TESTS PASSED\n");
    exit(0);
}
```

To work on one part, keep only that call and `exit(0)`; comment out the other two **and** the
`ALL TESTS PASSED` print. Keep every function definition and every `T_ASSERT` untouched.

| Part | Keep | Why |
|---|---|---|
| 2 | `sem_basic()` | counter/buffer code may still be TODO |
| 3 | `race_test()` | producer/consumer not needed |
| 4 | `producer_consumer()` | counter exercise not a prerequisite |

An "aborted" run can leave semaphores allocated and children unreaped; exit QEMU and restart before
retrying (the lab manual says this explicitly).

### I.4.3 Lab 4: branch, boot, symbols

```
host$ git checkout lab4 && git branch --show-current      → lab4
host$ make CPUS=3 qemu
xv6 kernel is booting / hart 1 starting / hart 2 starting / init: starting sh
```

| Symbol | Location | What to see |
|---|---|---|
| `sys_sbrk()` | [kernel/sysproc.c](./lab4/kernel/sysproc.c) L39 | reads `n`, saves `p->sz`, calls `growproc`, returns the **old** break |
| `walk()` | [kernel/vm.c](./lab4/kernel/vm.c) L86 | three-level loop, `kalloc` only when `alloc != 0` |
| `usertrap()` | [kernel/trap.c](./lab4/kernel/trap.c) L37 | `scause == 8` syscall branch, `devintr`, page-fault branch |
| placeholders | [user/lazytest.c](./lab4/user/lazytest.c) on a **fresh** checkout | `countvp()` and `countpp()` both `return 0`; they are deleted in this finished tree |

## I.5 producer_consumer diagnostic checklist (Ask-Gemini #6)

Use this when the run hangs or an assertion fires. Work top-down; each line is falsifiable in the
source.

**1. Count initialisation** (before the fork loop)

| Check | Correct | Classic bug |
|---|---|---|
| `empty` | `UBUF_SIZE` (16) | initialised to 0 → producers block immediately |
| `filled` | `0` | initialised to 16 → consumer reads garbage |
| `mutex` | `1` | initialised to 0 → first user deadlocks |
| allocation order | all three `sem_init` **before** `fork()` | created inside the child → parent has a different/­invalid id |
| results | all three `>= 0` asserted | ignoring `-1` from a full table (32 slots) |

**2. Lock lifetime**

- `sem_free` only after the consumer finished **and** both `wait(0)` calls returned.
- Freeing while a producer is still running leaves that process asleep on a dead channel forever.
- Do not free before the loop that reaps producers.

**3. Wait channels**

- Producer waits/signals `empty` and `filled`; consumer the reverse. Swapped `empty`/`filled` is the
  most common hang: the producer waits for data nobody produced yet.
- Every `sem_wait` uses the same `semid` as its matching `sem_signal`.

**4. Wait/signal ordering**

| Pattern | Result |
|---|---|
| `wait(empty)` → `wait(mutex)` → `ubuf_write` → `signal(mutex)` → `signal(filled)` | correct |
| `wait(mutex)` → `wait(empty)` | deadlock (holds the key while waiting for space) |
| `signal(mutex)` before `signal(filled)` | safe; the reverse order is also safe here, but keep signals balanced |
| missing `signal(filled)` | consumer sleeps after the buffer drains |

**5. Cleanup**

- Consumer loop count exactly `MSG_SIZE * NUM_PROD = 96`.
- `wait(0)` twice, then three `sem_free`.
- The message must be 48 non-NUL characters; the producer loop stops at `\0`, so a short string makes
  the consumer wait for bytes that never arrive → hang at `sem_wait(filled)`.

**6. What a Ctrl-p snapshot shows**

`consoleintr()` maps `Ctrl-p` to `procdump()` ([kernel/console.c](./lab3/kernel/console.c) L142). In
this build `procdump()` prints **`pid state name` only** — no channel, no semaphore value.

| Snapshot | Reading |
|---|---|
| all `race_test` processes `sleep` | everyone is blocked — deadlock or lost wakeup (check counts/order, not the buffer) |
| one `runble`/`run` and no progress | spinning or livelock; check for a missing `signal` or a busy loop |
| a `zombie` | child exited, parent has not reaped — cleanup order bug (`wait(0)` missing/misordered) |
| missing producer processes | they exited early (assertion inside the child) |

Because the channel is not printed, Ctrl-p can separate "blocked" from "runnable" but cannot prove
*which* semaphore is the culprit; the counts and the call order in the source do that.

## I.6 The user-call → kernel-handler chain (Lab 4 Ask-Gemini #2)

Every syscall in xv6, including `countvp`/`countpp` and the `sem_*` calls, is wired through five
places:

| Step | File | What it contributes |
|---|---|---|
| 1. user declaration | [user/user.h](./lab4/user/user.h) | `int countvp(void);` — makes the call compile |
| 2. stub generator | [user/usys.pl](./lab4/user/usys.pl) | `entry("countvp");` → generates `usys.S` (one `li a7, SYS_countvp; ecall; ret` per entry) |
| 3. syscall number | [kernel/syscall.h](./lab4/kernel/syscall.h) | `#define SYS_countvp 22` — matches `a7` |
| 4. dispatch | [kernel/syscall.c](./lab4/kernel/syscall.c) | `extern uint64 sys_countvp(void);` + `[SYS_countvp] sys_countvp,` in `syscalls[]` |
| 5. handler | [kernel/sysproc.c](./lab4/kernel/sysproc.c) | `sys_countvp()` reads args with `argint`/`argaddr` and calls the kernel function |

Any helper that other kernel files call also needs a prototype in [kernel/defs.h](./lab4/kernel/defs.h)
(e.g. the `sem_*` functions).

**Proof that `lazytest` reaches the syscalls, not the placeholders.** On a fresh checkout the two local
functions return `0`, so the test prints `Before: VP=0, PP=0` and `Error: VP count did not increase`.
The completed tree prints `Before: VP=4, PP=4` — that `4` can only come from `sys_countvp()` /
`sys_countpp()` reading `p->sz` and walking the page table.

## I.7 Spinning vs sleeping — assumptions to state (Lab 3 CP1)

| Wait | Prefer | Reasoning | Assumption |
|---|---|---|---|
| ~10 CPU cycles | spin | a context switch costs on the order of 10²–10⁴ cycles; sleeping costs two switches | the lock holder is running elsewhere and will release soon |
| ~10,000 cycles | sleep | spinning wastes a whole core for that duration; the scheduler can run useful work | wakeup latency (`wakeup` → `sched` → run) is small relative to the wait |
| unknown / long / I/O-bound | sleep | bounded by correctness, not throughput | no priority inversion; wakeups are not lost (they aren't, thanks to `p->lock`) |
| holder descheduled on the same CPU | sleep | spinning on a uniprocessor with the holder off-CPU never terminates | preemption exists |

These are not measured xv6 thresholds; state them as assumptions. xv6's own choice: spin for short
kernel critical sections (`acquire`), sleep for semaphores and I/O (`sleep`/`wakeup`).

---

# PART J — WHAT WAS CHANGED (change log + verification)

Everything below is the actual state of the two checkouts (`git diff` against the `lab3` / `lab4`
branches), plus the edits made while building this document. Nothing else was touched.

## J.1 At a glance

| Lab | Files changed | +/− | Purpose |
|---|---|---|---|
| 3 | [kernel/semaphore.c](./lab3/kernel/semaphore.c) | +22 / −9 | implement `sem_wait`, `sem_signal`, `sem_getvalue` |
| 3 | [user/race_test.c](./lab3/user/race_test.c) | +22 / −8 | mutual exclusion + producer/consumer semaphores |
| 3 | [user/usertests.c](./lab3/user/usertests.c) | 0 / −2 | pre-existing `-Werror` build fix |
| 3 | [.gitignore](./lab3/.gitignore) | +5 / −0 | keep sibling `lab1/`, `lab2/` checkouts out of the index |
| 4 | [kernel/sysproc.c](./lab4/kernel/sysproc.c) | +32 / −0 | `sys_countvp`, `sys_countpp` |
| 4 | [kernel/trap.c](./lab4/kernel/trap.c) | +33 / −0 | fault diagnostic + lazy first-touch handling |
| 4 | [kernel/proc.c](./lab4/kernel/proc.c) | +5 / −2 | `growproc` reserves instead of mapping |
| 4 | [kernel/vm.c](./lab4/kernel/vm.c) | +4 / −2 | `uvmunmap` skips unallocated holes |
| 4 | [kernel/syscall.h](./lab4/kernel/syscall.h) | +2 / −0 | `SYS_countvp 22`, `SYS_countpp 23` |
| 4 | [kernel/syscall.c](./lab4/kernel/syscall.c) | +4 / −0 | externs + dispatch entries |
| 4 | [user/usys.pl](./lab4/user/usys.pl) | +2 / −0 | `entry("countvp")`, `entry("countpp")` |
| 4 | [user/lazytest.c](./lab4/user/lazytest.c) | 0 / −9 | delete the two `return 0` placeholders |
| 4 | [user/usertests.c](./lab4/user/usertests.c) | 0 / −2 | same build fix as Lab 3 |

Totals: Lab 3 = **49 insertions, 19 deletions**; Lab 4 = **82 insertions, 15 deletions**.

## J.2 Lab 3 — what the code now does

**`kernel/semaphore.c`** (only the three TODOs; allocation/free were already supplied):

| Function | Before | After |
|---|---|---|
| `sem_wait` (L60) | retrieved nothing, returned 0 | `acquire(&sem->lock)`; `while(value == 0) sleep(sem, &sem->lock);` `value--`; release |
| `sem_signal` (L77) | returned 0 | `acquire`; `value++`; `wakeup(sem)`; release |
| `sem_getvalue` (L93) | always `-1` | locked copy of `value` |

Kept unchanged: the `-1` argument/in-use checks, the 32-slot table, `sem_table_lock` for allocation,
and the non-negative invariant (no negative-value variant).

**`user/race_test.c`**:

```c
// race_test(): created before fork so parent and child share it
int semid = sem_init(1);            // binary semaphore = mutex

void do_work(...) {
    sem_wait(semid);                // wraps the WHOLE read-modify-write
    int val = ucnt_get(0);
    ucnt_set(0, val + 1);
    sem_signal(semid);
}

struct buf_sem { int empty, filled, mutex; };   // 3 semids, passed by value
producer: wait(empty) → wait(mutex) → ubuf_write → signal(mutex) → signal(filled)
consumer: wait(filled) → wait(mutex) → ubuf_read → signal(mutex) → signal(empty)
init: empty = sem_init(UBUF_SIZE), filled = sem_init(0), mutex = sem_init(1)  // before the fork loop
free: sem_free(mutex/filled/empty) after the consumer finishes and both wait(0) calls
```

**`user/usertests.c`** — `fsfull()` had `int fsblocks` that was incremented but never read; GCC 16's
`-Werror=unused-but-set-variable` rejected it, so `fs.img` could not be built. The variable and its
increment were deleted (2 lines); the test's behaviour is unchanged.

**`.gitignore`** — adds `lab1/` and `lab2/` so the sibling checkouts (separate repositories) are not
picked up by Lab 3's index.

## J.3 Lab 4 — what the code now does

| Change | Effect |
|---|---|
| `sysproc.c` + `syscall.*` + `usys.pl` + `lazytest.c` | two counting syscalls wired end-to-end; local placeholders deleted, so `countvp()`/`countpp()` call into the kernel |
| `proc.c` `growproc` | positive `n` rejects wraparound and the trap mappings (`sz + n < sz` or `sz + n >= TRAMPOLINE`), then does `sz += n` — reservation only; negative `n` still goes through `uvmdealloc` |
| `trap.c` `usertrap` | new branch for `scause` 13 and 15: classify (`va < p->sz`, no valid leaf) → `kalloc`/`memset`/`mappages(PGROUNDDOWN(va), …)` with `PTE_W`, `PTE_R`, `PTE_U`; on failure `kfree` + `setkilled`; otherwise print the labelled fault and kill; `epc` never advanced |
| `vm.c` `uvmunmap` | `continue` on a missing PTE or invalid level-0 entry; keeps `panic("uvmunmap: not a leaf")`; frees and clears real leaves |
| `usertests.c` | same 2-line `fsblocks` build fix |

## J.4 Edits made while producing this document (not lab tasks)

| Edit | Why |
|---|---|
| `race_test.c`: removed `#define UBUF_SLOTS 16`, now uses `UBUF_SIZE` from [user/user.h](./lab3/user/user.h) | a second hard-coded 16 could drift from the buffer; the manual says the count derives from `UBUF_SIZE` |
| [lab3/LAB3_ANSWERS.md](./lab3/LAB3_ANSWERS.md) Appendix B rewritten | it described a `printf("… %d blocks", fsblocks)` fix that is **not** in the tree; it now documents the actual delete-the-variable fix, matching Lab 4's Appendix A |
| Directories renamed `xv6zz-lab3/` → [lab3/](./lab3), `xv6-lab4/` → [lab4/](./lab4) | requested naming; branches (`lab3`, `lab4`) and remotes are unaffected, no source referenced the old paths |
| This file (`labquiz2.md`) created, then expanded with Part I (all prompts/checkpoints answered) and Part J | study notes |

## J.5 Verification log

Every result below was produced in this environment: QEMU 11.1.1, `riscv64-elf-gcc` 16.2.0,
`CPUS=3`, QEMU launched with `-snapshot` (so `fs.img` is not modified by runs).

**Builds.** `make -B CPUS=3` completed with no errors in both labs (only the stock
`LOAD segment with RWX permissions` linker warnings).

**Lab 3** — `race_test`:

```
[sem_basic] PASS: Basic semaphore operations work.
[race_test] final counter=2000 (expected 2000)
[race_test] PASS: consistent counter
[producer_consumer] PASS: message delivered
ALL TESTS PASSED
```

**Lab 4** — `lazytest`, then both fault modes in the same boot:

```
Before: VP=4, PP=4
After sbrk(122880): VP=34, PP=4
Success: PP count unchanged (lazy allocation verified)
Touching pages...
After touching: PP=34

fault read  → usertrap(): load page fault pid=4 va=0x4000 sepc=0xc2
fault write → usertrap(): store page fault pid=5 va=0x4000 sepc=0x94
```

**Lab 4 — the extra Part 4.4 checks** (temporary test edits, then reverted):

| Temporary edit | Observed | Manual expectation |
|---|---|---|
| touch loop → 1 iteration | `After touching: PP=5`, exit 0, no panic | PP +1, no cleanup panic |
| touch loop → 1, then `sbrk(-122880)` | `returned 0x0000000000022000`, `After shrink: VP=4, PP=4`, no panic | old break returned, holes skipped |

**Regression spot-checks** under the lazy kernel:

```
$ usertests sbrkbasic
test sbrkbasic: OK
ALL TESTS PASSED

$ usertests stacktest
test stacktest: usertrap(): load page fault pid=6 va=0xfe90 sepc=0x1dba
OK
ALL TESTS PASSED
```

`stacktest` is the useful one: the guard page fault (`va=0xfe90`, valid PTE without `PTE_U`) is
rejected instead of being lazily mapped, which is the protection invariant the handler must preserve.

**Restoration proof.** After the two temporary variants, `user/lazytest.c` was compared with the saved
copy (`diff` → identical), `make CPUS=3 fs.img` was re-run, and `git status` in both labs shows only
the intended lab modifications — no stray test edits, no modified `fs.img`.

## J.6 Deliberately not changed

| File | Reason |
|---|---|
| [lab3/kernel/spinlock.c](./lab3/kernel/spinlock.c) / `.h` | Part 1 is analysis only; the manual says leave it untouched |
| [lab3/kernel/ucnt.c](./lab3/kernel/ucnt.c) | the counter must stay unprotected from the kernel side; that is what the lab tests |
| [lab3/kernel/ubuf.c](./lab3/kernel/ubuf.c) | keep the `yield()` calls and the access/advance order; the comment above `struct ubuf` is intentionally left as supplied |
| test constants and assertions in `race_test.c` / `lazytest.c` / `fault.c` | the manual requires `N`, `MSG_SIZE`, `NUM_PROD`, message, loops and assertions unchanged |
| `kernel/exec.c`, `kernel/vm.c` `uvmcopy`, `copyin`/`copyout` | lazy support for `fork()` and kernel copies is explicitly out of scope |

## J.7 Reproduce it

```
# Lab 3
cd lab3
make clean && make CPUS=3 qemu
xv6$ race_test                     # Ctrl-a x to leave QEMU

# Lab 4
cd lab4
make clean && make CPUS=3 qemu
xv6$ lazytest
xv6$ fault read
xv6$ fault write
```

**Not re-run in this session:** the Part 2.3 *eager* baseline (`VP=34, PP=34`, "PP count changed
immediately"), which needs a build with `growproc` reverted to `uvmalloc`; the transcript is preserved
in [lab4/LAB4_ANSWERS.md](./lab4/LAB4_ANSWERS.md). The trampoline trace is code reading, not a run.


