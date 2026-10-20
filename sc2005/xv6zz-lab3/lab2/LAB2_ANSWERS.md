# SC2005 Lab 2 — Processes, Scheduling, and User Threads

Answers, reasoning, and evidence. Source tree: this directory (`lab2` branch, `269bf05`-era branch head).

---

## Checkpoint 0 — Orient yourself before editing

| Item | Evidence |
|---|---|
| Active branch | `git branch --show-current` → `lab2` |
| Unmodified build | boots to `init: starting sh` |
| Unmodified `uthread_test` | prints **nothing** — the library is not implemented, `thread_schedule()` never switches stacks |
| Files per part | Part 1: [kernel/proc.h](./kernel/proc.h), [kernel/proc.c](./kernel/proc.c) · Part 2: same + [kernel/swtch.S](./kernel/swtch.S), [kernel/trap.c](./kernel/trap.c), [user/schedtest.c](./user/schedtest.c), [user/starvetest.c](./user/starvetest.c) · Part 3: [user/uthread.c](./user/uthread.c), [user/uthread_switch.S](./user/uthread_switch.S), [user/uthread_test.c](./user/uthread_test.c) |

**Why a clean build after a branch change.** `make clean` also removes *generated* files —
`user/usys.S`, `fs.img`, the `.asm`/`.sym` dumps, and every `.o`. A different branch can have
different `usys.pl`/`syscall.h` contents, so a stale `usys.S` or a stale `fs.img` could mix an old
generated stub with new kernel code. Cleaning makes the branch's own sources authoritative.

---

## Part 1 — Trace processes in xv6

### 1.1 The three state assignments

| Transition | Location | Enclosing function |
|---|---|---|
| new child becomes `RUNNABLE` | [kernel/proc.c:322](./kernel/proc.c:322) (`np->state = RUNNABLE;`) | `fork()` |
| `scheduler()` makes it `RUNNING` | [kernel/proc.c:467](./kernel/proc.c:467) (`p->state = RUNNING;`) | `scheduler()` |
| `yield()` makes it `RUNNABLE` again | [kernel/proc.c:518](./kernel/proc.c:518) (`p->state = RUNNABLE;`) | `yield()` |

(The boot-time `init` process follows the same pattern at [kernel/proc.c:252](./kernel/proc.c:252) inside
`userinit()`.)

**Why only a `RUNNABLE` entry may be selected.** `RUNNABLE` means "ready to run but not currently on
any CPU". The other states are all owned by someone else:

* `RUNNING` — already executing on a CPU. Selecting it would have two CPUs running the same
  `struct proc` and the same kernel stack.
* `SLEEPING` — waiting on a channel; it must not be resumed until `wakeup()` sets it `RUNNABLE`, or
  the condition it is waiting on may not hold.
* `ZOMBIE` — exited; its address space and trapframe are gone, so there is nothing to switch to.
* `UNUSED`/`USED` — the slot holds no runnable process.

The state is changed **while holding `p->lock`** ([kernel/proc.c:462](./kernel/proc.c:462)), and the
lock is handed to the process across `swtch()`; the process releases it once it is safely running.
That is what makes "the scheduler may pick it" and "the process is really on the CPU" one atomic step.

### 1.2 Trace a newly forked command, from `sh` to `forkret()`

Route for `ls`:

1. **`user/sh.c`** — the shell parses the line and calls `fork()` to get a child.
2. **[kernel/proc.c:280](./kernel/proc.c:280) `fork()`** — `allocproc()` is called first
   ([kernel/proc.c:110](./kernel/proc.c:110)): it finds an `UNUSED` slot, allocates the kernel stack
   and a trapframe page, and sets the context's **`ra` to `forkret`** ([kernel/proc.c:146](./kernel/proc.c:146)).
   `fork()` then copies the trapframe, opens file references, and finally sets
   **`np->state = RUNNABLE`** ([kernel/proc.c:322](./kernel/proc.c:322)).
3. **[kernel/proc.c:467-469](./kernel/proc.c:467) `scheduler()`** — finds the child `RUNNABLE`, sets it
   `RUNNING`, records `c->proc = p`, and calls **`swtch(&c->context, &p->context)`**. This is the
   first `swtch()` call site: **saves the per-CPU scheduler context, restores the per-process kernel
   context**.
4. **[kernel/proc.c:526](./kernel/proc.c:526) `forkret()`** — the child's kernel context was built with
   `ra = forkret` and `sp` = the top of its kernel stack, so `swtch()`'s `ret` lands here on the
   child's first scheduling.
5. `forkret()` releases `p->lock` (the comment says *"Still holding p->lock from scheduler"*) and
   returns to user space through `usertrapret()`.

**Interesting subtlety of `fork()`: the trapframe is copied too**, so `forkret()`'s caller-visible
register state is the *parent's* state as of the `ecall` — which is precisely why the child "returns
from `fork()`" with the same user registers and a different return value in `a0` (0 instead of the pid).

**How the child reaches `forkret()`.** `scheduler()` `swtch()`es to `p->context`, whose `ra` was set
to `forkret` by `allocproc()`; `swtch()` ends with `ret`, which jumps to that `ra`. So `forkret()` is
the function *every* newly created process first returns through — it is the "return path" of a
process that has never actually been running.

### 1.3 Trapframe vs. saved kernel context vs. user address space

| | What it is | Where | Who switches it |
|---|---|---|---|
| **trapframe** | the 32 **user** registers plus kernel `sp`, `satp`, `epc`, hart id — one page per process, mapped in *both* page tables | `struct trapframe *trapframe` ([kernel/proc.h:102](./kernel/proc.h:102)), allocated in `allocproc()` | the trampoline (`uservec`/`userret`) on every trap in/out |
| **saved kernel context** | `ra`, `sp` and the 12 callee-saved registers of the **kernel** thread | `struct context context` ([kernel/proc.h:2](./kernel/proc.h:2), [kernel/proc.h:103](./kernel/proc.h:103)) | `swtch()` ([kernel/swtch.S](./kernel/swtch.S)) on a kernel-level context switch |
| **user address space** | the process's user page table: text, data, stack, heap | `pagetable_t pagetable` + `uint64 sz` | `exec()`/`sbrk()`/`fork()`; installed by switching `satp` in the trampoline |

**Why a user program cannot dereference `proc[]`.** `proc` is a kernel global
([kernel/proc.c:11](./kernel/proc.c:11)) living at a kernel virtual address. It is *not* mapped in
any user page table — user page tables contain only the process's own memory and the trampoline page.
There is no way to form a valid user virtual address for it, so any attempt traps as a page fault
(scause 13/15) and the process is killed. Even if it were mapped, `p->lock` makes the table
inconsistent to read from outside the kernel. That is exactly the problem `getproccount()` in Lab 1
solved by adding a *system call* instead of exporting the table.

---

## Part 2 — Scheduling and context switching

### 2.1 Baseline (stock scheduler, `CPUS=1`)

`uthread_test` printed nothing (unimplemented library).

`starvetest` baseline (`Ctrl-p` pressed three times during the run):

```
starvetest: even pid 4; odd pid 5
starvetest: releasing children; Ctrl-p to inspect; Ctrl-a x to stop

1 sleep  init
2 sleep  sh
3 sleep  starvetest
4 runble starvetest
5 run    starvetest

1 sleep  init
2 sleep  sh
3 sleep  starvetest
4 run    starvetest
5 runble starvetest

1 sleep  init
2 sleep  sh
3 sleep  starvetest
4 runble starvetest
5 run    starvetest
```

**Reading the columns**: `pid`, `state`, `name`. The state strings come from the table inside
`procdump()` ([kernel/proc.c:673](./kernel/proc.c:673)); a `RUNNABLE` entry prints as **`runble`**
and a `RUNNING` one as **`run`**. In the baseline the `run` marker **alternates between pid 4 and
pid 5** — the stock round-robin scan gives both children CPU time.

`procdump()` is reached from the console interrupt handler — `case C('P'): procdump();`
([kernel/console.c:141](./kernel/console.c:141)). It is a **debugging snapshot**, not a measurement:
the `Ctrl-p` interrupt can arrive at any instant, it prints whatever states happen to be true then,
and a process that is `run` in one listing may be `runble` in the next. `procdump()` deliberately
takes **no locks** — its own comment says *"No lock to avoid wedging a stuck machine further"* — so it
can read a torn table rather than risk deadlocking a machine that is already stuck. That is also why
the kernel can read `proc[]` while a user program cannot (§1.3).

Baseline `schedtest` (4 children, pids 5–8) — all four children completed all four rounds and the
run ended with `schedtest: all children finished`.

### 2.2 Preemption and the two `swtch()` call sites

Path for one timer-triggered preemption:

1. The timer interrupt is taken in **kernel** mode → [kernel/kernelvec.S](./kernel/kernelvec.S)
   `kernelvec` → [kernel/trap.c:135](./kernel/trap.c:135) `kerneltrap()`.
2. `devintr()` returns 2 for a timer interrupt, and `kerneltrap()` does
   `if(which_dev == 2 && myproc() != 0) yield();` ([kernel/trap.c:154](./kernel/trap.c:154)).
   (A timer interrupt taken while the process is in *user* mode goes through `usertrap()` instead,
   with the same `if(which_dev == 2) yield();` at [kernel/trap.c:80](./kernel/trap.c:80).)
3. **[kernel/proc.c:514](./kernel/proc.c:514) `yield()`** — `acquire(&p->lock)`, sets
   `p->state = RUNNABLE` ([kernel/proc.c:518](./kernel/proc.c:518)), then calls `sched()`.
4. **`sched()`** ([kernel/proc.c:493](./kernel/proc.c:493)) — asserts `p->lock` is held, that no
   other lock is held (`noff == 1`), that the state is not `RUNNING`, and that interrupts are off;
   then calls **`swtch(&p->context, &mycpu()->context)`** at [kernel/proc.c:508](./kernel/proc.c:508).
5. **`scheduler()`** resumes after its own `swtch()` at [kernel/proc.c:469](./kernel/proc.c:469),
   clears `c->proc`, releases `p->lock`, and continues scanning for the next `RUNNABLE` process.

**The two `swtch()` call sites**

| Site | Location | Saves | Restores |
|---|---|---|---|
| `scheduler()` → process | [kernel/proc.c:469](./kernel/proc.c:469) `swtch(&c->context, &p->context)` | the **per-CPU scheduler context** — the context of whatever kernel thread happens to be executing on this CPU | the **selected process's kernel context**, i.e. where that process last called `swtch()` inside `sched()` |
| process → `scheduler()` | [kernel/proc.c:508](./kernel/proc.c:508) `swtch(&p->context, &mycpu()->context)` | the **process's kernel context** — its place in `yield()`/`sleep()`/`exit()` | the **per-CPU scheduler context**, i.e. the middle of `scheduler()`'s scan |

**Where a suspended process resumes.** Its `sp` and `ra` were saved inside `swtch()` called from
`sched()`, so when the scheduler later picks it again, `swtch()` returns *inside `sched()`*, which
returns to `yield()`/`sleep()`/`exit()`, which continues from exactly where it stopped. A process that
was preempted in the middle of `yield()` therefore resumes in the middle of `yield()`.

Note this is a *kernel*-level context switch: the user registers were already saved in the
**trapframe** when the trap was entered, so `swtch()` only has to preserve the kernel thread's own
state.

### 2.3 Why the callee-saved rule is enough

`struct context` ([kernel/proc.h:2](./kernel/proc.h:2)) is exactly `ra`, `sp` and `s0`–`s11`, and
[kernel/swtch.S](./kernel/swtch.S) stores/loads exactly those 14 values at offsets 0, 8, 16, …, 104.
This set is sufficient because `swtch()` is an **ordinary function call**:

* **Callee-saved registers (`s0`–`s11`)** are the only registers the RISC-V integer calling
  convention guarantees survive a call. Any live value the *caller* of `swtch()` had in a
  callee-saved register is, by definition, a value `swtch()` must preserve — so saving them is enough
  to make the switch invisible to the C code on either side.
* **Caller-saved registers (`a0`–`a7`, `t0`–`t6`) need no saving.** They are *already* treated as
  dead across a call: the compiler spills them to the stack *before* calling `swtch()` and reloads
  them after it returns. So their live values are on the stack — which `sp` points at — not in the
  registers. Saving them would be redundant work.
* **`ra` is not callee-saved, and that is precisely why it must be saved explicitly.** By the ABI,
  `ra` may be clobbered by any call; the convention is that a function which needs to return saves
  `ra` itself (normally to its own stack frame). `swtch()` wants to "return" to a *different* place
  than its caller, so it stores `ra` into the outgoing context and loads the incoming `ra` from the
  new one; the final `ret` then jumps there.
* **`sp`** is what makes the other half work: `ra` says *where* to resume, `sp` says *with which
  stack*. Restoring both is what makes the resumed thread see a consistent kernel stack.

Together: `ra` + `sp` relocate execution, and `s0`–`s11` preserve the C-level state that cannot be
recomputed. Nothing else is needed.

### 2.4 The required policy

> At each CPU's scheduling selection point, select a RUNNABLE process with an even PID whenever an
> eligible even-PID process is found; select an odd-PID RUNNABLE process only after the scheduler has
> found no eligible even-PID process.

Implemented in `scheduler()` by wrapping the existing scan in a two-pass loop:

```c
    int found = 0;

    // Strict even-PID priority: the first pass considers only RUNNABLE
    // even-PID processes. The second pass considers odd-PID processes,
    // and is reached only when the first pass ran nothing at all.
    for(int pass = 0; pass < 2 && found == 0; pass++){
      int want_even = (pass == 0);

      for(p = proc; p < &proc[NPROC]; p++) {
        acquire(&p->lock);
        if(p->state == RUNNABLE &&
           (((p->pid % 2) == 0) == want_even)) {
          // Switch to chosen process.  It is the process's job
          // to release its lock and then reacquire it
          // before jumping back to us.
          p->state = RUNNING;
          c->proc = p;
          swtch(&c->context, &p->context);

          // Process is done running for now.
          // It should have changed its p->state before coming back.
          c->proc = 0;
          found = 1;
        }
        release(&p->lock);
      }
    }
    if(found == 0) {
      asm volatile("wfi");
    }
```

**Invariants preserved.** Everything inside the `if` is byte-for-byte the stock code: `p->lock` is
acquired before looking at `p->state` and released on every path; the `RUNNABLE → RUNNING` transition
happens while holding `p->lock`; `c->proc` is set before and cleared after `swtch()`; the lock is
handed to the process over the switch; and `wfi` is still reached only when nothing ran. Timer
preemption is untouched — `intr_on()`/`intr_off()` at the top of the loop and `yield()` are unchanged.
`p->pid` is immutable for a live process, so reading it under `p->lock` is safe (and for a slot that
is not `RUNNABLE` the parity is irrelevant).

The strict version is saved as [part2_strict_even_scheduler.patch](./part2_strict_even_scheduler.patch)
(`git apply part2_strict_even_scheduler.patch` to reproduce). `scheduler()` in the working tree is
back to the **stock** implementation, as the manual requires for Part 3.

### 2.5 Results and starvation analysis

**`starvetest` under the stock scheduler** — the `run` marker alternates between pid 4 (even) and
pid 5 (odd) across snapshots: both children progress.

**`starvetest` under strict even-PID priority** — same workload, `CPUS=1`:

```
starvetest: even pid 4; odd pid 5
starvetest: releasing children; Ctrl-p to inspect; Ctrl-a x to stop

1 sleep  init
2 sleep  sh
3 sleep  starvetest
4 run    starvetest      <- even: runs
5 runble starvetest      <- odd: runnable but never selected

1 sleep  init
2 sleep  sh
3 sleep  starvetest
4 run    starvetest
5 runble starvetest

1 sleep  init
2 sleep  sh
3 sleep  starvetest
4 run    starvetest
5 runble starvetest
```

The prediction is confirmed: **pid 4 is always `run`, pid 5 is always `runble`** — postponement over
the whole observation interval, in every snapshot.

**`schedtest` under strict even-PID priority** (children pid 4/even, 5/odd, 6/even, 7/odd):

```
parent: created child 0 as pid 4 (even)
parent: created child 1 as pid 5 (odd)
parent: created child 2 as pid 6 (even)
parent: created child 3 as pid 7 (odd)
child 1: pid 5 (odd) start
child 1: pid 5 (odd) round 1/4
child 3: pid 7 (odd) start
child 3: pid 7 (odd) round 1/4
child 3: pid 7 (odd) round 2/4
child 0: pid 4 (even) start
child 0: pid 4 (even) round 1/4
child 0: pid 4 (even) round 2/4
child 2: pid 6 (even) start
child 2: pid 6 (even) round 1/4
...
child 0: pid 4 (even) done
child 2: pid 6 (even) done
child 1: pid 5 (odd) round 2/4
child 3: pid 7 (odd) round 3/4
child 3: pid 7 (odd) round 4/4
child 3: pid 7 (odd) done
child 1: pid 5 (odd) round 3/4
child 1: pid 5 (odd) round 4/4
child 1: pid 5 (odd) done
schedtest: all children finished
```

**Difference from the baseline, using the actual PIDs.** In the baseline, pids 5/6/7/8 interleaved
throughout. Under strict priority the **even** children (4 and 6) ran rounds 1–4 back-to-back and
exited *before the odd children (5 and 7) were allowed to finish their remaining rounds*. The odds get
CPU time in this workload only because the evens eventually **exit** and stop being `RUNNABLE` — the
test has finite work, so it demonstrates *postponement* and eventual progress, not indefinite
starvation. That is exactly the manual's warning: `schedtest` alone cannot show starvation.

**Why the odds appear first, and why that is still the policy.** This looked surprising, so I
instrumented the scheduler temporarily and confirmed it: the print below fires when the *fallback*
(odd) pass selects a process, and lists every `RUNNABLE`/`RUNNING` process **after** that selection
returned (`state 3` = `RUNNABLE`):

```
DBG fallback select pid=3 runnable: 4/3 5/3 6/3 7/3
child 1: pid 5 (odd) start
```

The sequence is: all four children were blocked reading the gate pipe. The parent (pid 3, odd) was
selected by the fallback because **no even process was `RUNNABLE` at that moment**. While the parent
ran, its `write(gate[1], …)` woke all four children. The scheduler then resumed *inside the same pass-1
scan*, and because the stock structure **continues to the next slot after `swtch()` rather than
restarting the pass**, it picked up the newly-`RUNNABLE` odd children (pid 5, then pid 7) before ever
starting a fresh even-first pass. That is faithful to the required policy — the odd children were not
*eligible even* candidates **at that selection point**, and the manual explicitly says to keep the
"inner scan continues to the next slot; only a new full pass starts at `proc[0]`" behaviour. The
instrumentation was removed afterwards (the saved patch contains no debug output).

**Why the odd process can starve indefinitely.** The policy is *strict*: as long as **any** even-PID
process is `RUNNABLE` at a selection point, an odd one is never chosen. In `starvetest` the even child
is a pure CPU loop with no `sleep`, no I/O and no `exit`; when timer preemption turns it `RUNNABLE`
again, the very next selection point finds an eligible even process again. Nothing ever satisfies the
odd child's "no eligible even process is found" condition, so it is never selected while the even child
keeps running — the odd child remains `runble` forever. Note this needs `CPUS=1`: with three CPUs the
even process could be `RUNNING` on one CPU while the odd process is `RUNNABLE` and gets picked by
another CPU's scheduler (a `RUNNING` process is not a `RUNNABLE` candidate), so a single busy even
process does not establish starvation on `CPUS=3`.

---

## Part 3 — Completing the user-level threading library

### 3.1–3.2 The saved thread context and stack design

Added to [user/uthread.c:16](./user/uthread.c:16), mirroring `struct context` in
[kernel/proc.h:2](./kernel/proc.h:2) so the same save/restore layout can be used:

```c
struct context {
  uint64 ra;
  uint64 sp;

  // callee-saved
  uint64 s0;  uint64 s1;  uint64 s2;  uint64 s3;
  uint64 s4;  uint64 s5;  uint64 s6;  uint64 s7;
  uint64 s8;  uint64 s9;  uint64 s10; uint64 s11;
};
```

and to `struct thread` ([user/uthread.c:38](./user/uthread.c:38)):

```c
  struct context *context;      /* saved context, at the top of stack[] */
```

**Design check 1 — field order agrees with every assembly offset.** The offsets are
`ra`@0, `sp`@8, `s0`@16 … `s11`@104, each `uint64` = 8 bytes, so the C field order matches
[user/uthread_switch.S](./user/uthread_switch.S) exactly (`sd ra, 0(a0)` … `sd s11, 104(a0)`).
This is the failure mode the manual warns about: a mismatched layout *compiles* and then corrupts
registers at runtime.

**Design check 2 — a new thread enters its function on its own stack.** `thread_create()` builds a
context whose `ra` is the thread function and whose `sp` is inside that thread's own `stack[]`. When
`thread_switch()` restores the context and executes `ret`, `ret` jumps to the address in `ra` with
`sp` already pointing into the new thread's stack — so the function's prologue builds its frame there,
never on the creator's stack.

**Design check 3 — 16-byte stack alignment.** The ABI requires `sp` to be 16-byte aligned on function
entry. The slot is computed at [user/uthread.c:44](./user/uthread.c:44):

```c
static struct context *
thread_context_slot(struct thread *t)
{
  uint64 top = (uint64)t->stack + STACK_SIZE - sizeof(struct context);
  return (struct context *)(top & ~(uint64)0xf);
}
```

`sizeof(struct context)` is 112 and `STACK_SIZE` is 8192 (a multiple of 16), so the only thing that
could break alignment is the base address of the array itself; masking the address down to a multiple
of 16 removes that dependency. The initial `sp` is set to **exactly this 16-byte-aligned address**
([user/uthread.c:112](./user/uthread.c:112)), so the thread function starts correctly aligned, and its
stack grows downwards into the remaining `STACK_SIZE - 112` bytes.

**Why a `struct context *` rather than an embedded struct.** The macro `thread_switch(uint64, uint64)`
declaration is supplied and must not change; storing a *pointer* to the context location lets the
context live at the top of each thread's stack while still being passed as a plain 64-bit value.

**`thread_init()` must initialise thread 0's context too** ([user/uthread.c:54](./user/uthread.c:54), assignment at [:63](./user/uthread.c:63)).
`main()` is thread 0 and makes the first `thread_schedule()` call, and `thread_switch()` writes the
outgoing context *through* `current_thread->context`. If that pointer were left at its zero
initialiser, the very first switch would store to address 0 — which in xv6 user space is the
program text — and fault. Thread 0 runs on the process's real stack (the one the kernel set up), so it
only needs `stack[]` as a *save area*: pointing it at the top of `all_thread[0].stack` is exactly right,
and if thread 0 were ever resumed the saved `sp` would restore its real stack.

### 3.3 First execution of a new thread

`thread_create()` ([user/uthread.c:99](./user/uthread.c:99)):

```c
  t->state = RUNNABLE;
  // A never-run thread has no saved state, so construct one: thread_switch()
  // restores ra and sp, and `ret` then starts func on this thread's own stack.
  t->context = thread_context_slot(t);
  memset(t->context, 0, sizeof(struct context));
  t->context->ra = (uint64)func;
  t->context->sp = (uint64)t->context;   // 16-byte aligned, grows down
```

**Contrast with a resumed thread.** A *resumed* thread's context was written by `thread_switch()`
itself: `ra` is the return address inside `thread_schedule()` and `sp` is its real stack pointer. A
*new* thread has no such history, so it is faked: `ra = func` makes the final `ret` begin the thread
function, and `sp = the context slot` gives it a valid, aligned stack. The `s0`–`s11` values are
irrelevant to the new thread (the function prologue sets `s0` itself), but they are zeroed so nothing
depends on uninitialised memory.

### 3.4 The switch itself

`thread_schedule()` ([user/uthread.c:93](./user/uthread.c:93)) passes the outgoing and incoming
contexts:

```c
    next_thread->state = RUNNING;
    t = current_thread;
    current_thread = next_thread;
    thread_switch((uint64)t->context, (uint64)next_thread->context);
```

Note `t` is captured *before* `current_thread` is reassigned — it is the outgoing thread. The
state change happens first, so by the time the outgoing thread is resumed (if ever) its state is
already correct.

[user/uthread_switch.S](./user/uthread_switch.S) — identical register layout to `kernel/swtch.S`,
but on the *user* library's own context type:

```asm
thread_switch:
	sd ra, 0(a0)
	sd sp, 8(a0)
	sd s0, 16(a0)
	...            /* through s11 at 104 */
	ld ra, 0(a1)
	ld sp, 8(a1)
	ld s0, 16(a1)
	...            /* through s11 at 104 */
	ret    /* return to ra, now the incoming thread's */
```

`a0` is the outgoing context, `a1` the incoming one. Saving `ra` *as well as* `sp` at the very start
means a later restore of this context resumes right after the call, on the same stack.

### 3.5 Verification

Full run (`CPUS=3`), checked programmatically:

| Check | Result |
|---|---|
| `thread_a started`, `thread_b started`, `thread_c started` | present |
| each thread prints its own values 0…99 | 100 values each, **all unique**, range `[0]..[99]` |
| each thread reports exit after 100 | `thread_a: exit after 100`, `thread_b: …`, `thread_c: …` |
| library reports no runnable threads | `thread_schedule: no runnable threads` |

Tail of the run:

```
thread_c 99
thread_a 99
thread_b 99
thread_c: exit after 100
thread_a: exit after 100
thread_b: exit after 100
thread_schedule: no runnable threads
```

**Baseline comparison.** The unmodified library printed **nothing**: `thread_create()` never built a
context and `thread_schedule()` only reassigned a pointer without switching stacks, so `main()`
walked off the end of `thread_exit()` and the process exited. The four TODOs that changed this were
(1) the context field, (2) the new-thread `ra`/`sp` setup, (3) the `thread_switch()` arguments, and
(4) the register save/restore in assembly.

**Why the counting order differs from the `thread_create()` order.** All three threads begin by
printing `<name> started`, setting their `*_started` flag, and then busy-waiting on
`thread_yield()` until the *other two* flags are set. Because each `thread_yield()` re-enters
`thread_schedule()`, which resumes its scan from `current_thread + 1` and wraps around, the three
threads round-robin through the startup spins; once the last flag is set they are all released
together and the order in which they emit `0, 1, 2, …` is simply the order the scan happens to pick
them, not the `thread_create()` call order. `thread_c` happens to be resumed first, which is why the
counts read `c, a, b` — the test asserts nothing about order, only about the values.

**Repeatability.** `uthread_test` was run twice in one boot after `make clean`: both runs produced
2 × `thread_schedule: no runnable threads` and 6 × `exit after 100` (three threads × two runs), with
the counts verified as 0–99 exactly once each. `forktest` also reports `fork test OK` with the stock
scheduler.

---

## Final self-check questions

1. **Why can `procdump()` read `proc[]` while a normal user program cannot?** `procdump()` runs in
   kernel mode, where the kernel page table maps `proc[]` and the kernel stack. A user program runs on
   its own page table, which maps only its own memory plus the trampoline page, so `proc[]` has no
   valid user address at all. (`procdump()` also deliberately runs lock-free — "no lock to avoid
   wedging a stuck machine further" — accepting a torn snapshot in exchange for never deadlocking.)
2. **How does a timer interrupt lead from a running process to the scheduler and back?**
   Timer → `kerneltrap()` (or `usertrap()`), `devintr()` returns 2 → `yield()`: `RUNNING` →
   `RUNNABLE` under `p->lock` → `sched()` checks the locks and calls
   `swtch(&p->context, &mycpu()->context)`, saving the process's kernel context and restoring the
   per-CPU scheduler context → `scheduler()` resumes after its own `swtch()`, clears `c->proc`,
   releases `p->lock`, and later picks a `RUNNABLE` process, setting it `RUNNING` and calling
   `swtch(&c->context, &p->context)` — which returns *inside the process's own* `sched()`, so it
   continues in `yield()`, returns to the trap handler, and `sret`s back to user mode.
3. **What workload can starve an odd-PID process?** Any workload with an even-PID process that stays
   `RUNNABLE` without ever blocking — a pure CPU loop with no `sleep`, I/O or exit (exactly
   `starvetest`). Strict priority means an odd process is chosen only when *no* even process is
   `RUNNABLE` at that selection point, and a CPU-bound even process is `RUNNABLE` again immediately
   after each preemption. Use `CPUS=1`: on several CPUs the even process may be `RUNNING` elsewhere
   and therefore not a `RUNNABLE` candidate.
4. **Why are the callee-saved registers, `ra` and `sp`, sufficient for this cooperative switch?**
   `thread_switch()` is an ordinary function call, so caller-saved registers are already dead across
   it (the compiler spills them to the stack, which `sp` covers), while callee-saved registers
   `s0`–`s11` *must* be preserved for the C code on either side. `ra` is not callee-saved, which is
   exactly why it is saved explicitly — the switch wants to return somewhere else. `ra` + `sp`
   together relocate execution to the incoming thread's resume point and stack.
5. **How does a never-run user thread begin at its function on its own stack?** `thread_create()`
   fabricates a context at the 16-byte-aligned top of that thread's `stack[]`, with `ra = func` and
   `sp` pointing at the context slot. When `thread_schedule()` selects it, `thread_switch()` loads
   that `ra`/`sp` and `ret`s to `func`; because the context is the first thing at the top of the
   stack, `func`'s frame grows down into the thread's own stack.
6. **Kernel scheduling an xv6 process vs. the library scheduling a user thread.** The kernel switches
   between *processes*: it saves the kernel context (`struct context`) plus the user registers
   (`trapframe`) and changes `satp` to a different address space, so each process has its own memory
   and its own kernel thread; the switch is *preemptive* and can happen at any trap. The library
   switches between *user threads inside one process*: they share one address space, one set of page
   tables and one kernel thread, and only `ra`/`sp`/`s0`–`s11` are saved; switching happens only
   *cooperatively*, at `thread_yield()`/`thread_exit()`, so no trapframe is created per user thread.

---

## Appendix A — Build blocker in `usertests.c`

As in Lab 1, `make` could not build `fs.img` at all:

```
user/usertests.c: In function 'fsfull':
user/usertests.c:2347:7: error: variable 'fsblocks' set but not used [-Werror=unused-but-set-variable=]
```

`fsfull()` accumulates `fsblocks` and never reads it, and `CFLAGS` carries `-Wall -Werror`
([Makefile:62](./Makefile:62)). Applied the upstream MIT fix at
[user/usertests.c:2391](./user/usertests.c:2391):

```diff
-  printf("fsfull test finished\n");
+  printf("fsfull test finished, %d blocks\n", fsblocks);
```

## Appendix B — Files changed

| File | Change |
|---|---|
| [user/uthread.c](./user/uthread.c) | `struct context`; `struct thread.context` pointer; `thread_context_slot()` helper; thread 0's context in `thread_init()`; new-thread `ra`/`sp` in `thread_create()`; `thread_switch()` arguments in `thread_schedule()` |
| [user/uthread_switch.S](./user/uthread_switch.S) | Save/restore `ra`, `sp`, `s0`–`s11` |
| [user/usertests.c](./user/usertests.c) | Pre-existing `-Werror` build blocker (Appendix A) |
| [part2_strict_even_scheduler.patch](./part2_strict_even_scheduler.patch) | **Saved** Part 2 strict even-PID `scheduler()` (not applied to the working tree) |

`kernel/proc.c` is **restored to the stock lab2 implementation**, as the manual requires before
Part 3 and final verification.

## Appendix C — Raw evidence index

| Evidence | Where |
|---|---|
| Stock `starvetest` Ctrl-p (alternating `run`) | §2.1 |
| Strict `starvetest` Ctrl-p (even always `run`, odd always `runble`) | §2.5 |
| Baseline `schedtest` (all four children interleaved) | §2.1 |
| Strict `schedtest` (evens complete, then odds) | §2.5 |
| Scheduler fallback instrumentation | §2.5 |
| `uthread_test` full run, 0–99 verified | §3.5 |
| `uthread_test` ×2 + `forktest` after `make clean` | §3.5 |

## References

1. SC2005 xv6 Lab 2 branch: <https://github.com/CPS-research-group/ntu-sc2005-xv6/tree/lab2>
2. Russ Cox, Frans Kaashoek, Robert Morris, *xv6: a simple, Unix-like teaching operating system*,
   §§1.1, 2.5, 7.1–7.3.
3. MIT 6.1810 — *Multithreading*, user-level thread switch exercise.
4. RISC-V ABIs Specification §1.1 Table 1 and §2.1: <https://riscv-non-isa.github.io/riscv-elf-psabi-doc/>
