# SC2005 Lab 2 — Revision Notes

Study material for the Lab 2 checkpoints. Command output and evidence live in
[LAB2_ANSWERS.md](./LAB2_ANSWERS.md); this file is the *learning*: the concepts, the "why", and the
traps. Everything here is answerable without the lab in front of you.

---

## The lab in one paragraph

A process is not one thing — it is **four** things that are easy to confuse: a `struct proc` (state
+ metadata), a saved **kernel context**, a **trapframe** (user registers), and an **address space**
(page tables). The kernel switches between processes by `swtch()`ing kernel contexts and changing
`satp`. You then bend that scheduler into a **strict even-PID priority** policy and watch it starve
an odd-PID process. Finally you build a **second, much smaller scheduler** in user space: cooperative
threads inside one process, switched by their own `thread_switch()` that saves a *subset* of the
same registers — because a user-level switch is just a function call that returns somewhere else.

---

## Checkpoint 0 — Orientation

**What it asks.** Branch, unmodified build and `uthread_test` behaviour, the files per part, and why a
clean build after a branch change.

**The answers.**

* Branch is `lab2`; the unmodified tree boots to the xv6 prompt.
* Unmodified `uthread_test` **prints nothing**. The library has a `thread_create()` that never builds
  a context and a `thread_schedule()` that only reassigns a pointer without switching stacks, so
  `main()` simply walks off the end and the process exits. *"Prints nothing" is the correct baseline,
  not a failure.*
* Files: Part 1 — `kernel/proc.h`, `kernel/proc.c`. Part 2 — those plus `kernel/swtch.S`,
  `kernel/trap.c`, `user/schedtest.c`, `user/starvetest.c`. Part 3 — `user/uthread.c`,
  `user/uthread_switch.S`, `user/uthread_test.c`.
* **Why clean**: `make clean` also removes **generated** files (`user/usys.S`, `fs.img`, `.asm`/`.sym`,
  `.o`). A different branch can have different `usys.pl`/`syscall.h`, and a stale generated stub mixed
  with new kernel code produces "unknown syscall" confusion. Clean makes the branch's sources
  authoritative.

---

## Checkpoint 1 — Process state and visibility

### The three state transitions

| Transition | Location | Owner |
|---|---|---|
| new child → `RUNNABLE` | [kernel/proc.c:322](./kernel/proc.c:322) (`np->state = RUNNABLE;`) | `fork()` |
| `RUNNABLE` → `RUNNING` | [kernel/proc.c:467](./kernel/proc.c:467) (`p->state = RUNNING;`) | `scheduler()` |
| `RUNNING` → `RUNNABLE` | [kernel/proc.c:518](./kernel/proc.c:518) (`p->state = RUNNABLE;`) | `yield()` |

**Why only a `RUNNABLE` entry may be selected.** Each state is *owned* by someone:

* `RUNNING` — already on a CPU. Selecting it would put the same process and the same kernel stack on
  two CPUs.
* `SLEEPING` — waiting on a channel. It must not run until `wakeup()` says the condition changed.
* `ZOMBIE` — exited; its address space and trapframe are gone, so there is nothing to switch to.
* `UNUSED`/`USED` — no runnable process there.

**The critical invariant:** the state change happens **while holding `p->lock`**, and the lock is
*handed to the process across* `swtch()`. That makes "the scheduler may pick it" and "it is really on
the CPU" a single atomic step. In `scheduler()` the sequence is `acquire(&p->lock)` → check
`RUNNABLE` → set `RUNNING` → `c->proc = p` → `swtch()` — all under one lock the process releases for
itself when it starts running ([kernel/proc.c:462-470](./kernel/proc.c:462)).

### The `fork → forkret` route (the guided trace)

```
user/sh.c: fork()
  -> kernel/proc.c:280  fork()
       -> :110  allocproc()      finds an UNUSED slot, allocates the kernel stack
                                 and a trapframe page, sets p->context.ra = forkret  (:146)
       -> :322  np->state = RUNNABLE
  -> :467-469 scheduler()          RUNNABLE -> RUNNING, swtch(&c->context, &p->context)
  -> :526  forkret()               the child's FIRST kernel code
       -> release(&p->lock)        (comment: "Still holding p->lock from scheduler")
       -> usertrapret()            -> back to user space
```

**The subtle bit.** `allocproc()` sets `ra = forkret`, so the child's very first `swtch()` ends in
`ret` jumping to `forkret`. And because `fork()` **copied the parent's trapframe**, the child returns
to user space with *the parent's* register state — which is exactly why the child "returns from
`fork()`" with a different value in `a0` and no other difference.

**So: `forkret()` is the return path of a process that has never run.**

### The four kinds of process state — do not confuse them

| | What it holds | Where | Switched by | Lifetime |
|---|---|---|---|---|
| **`struct proc`** | state, pid, name, parent, pointers | `proc[]` ([kernel/proc.c:11](./kernel/proc.c:11)) | `allocproc`/`fork`/`exit` | slot, reused |
| **kernel context** | `ra`, `sp`, `s0`–`s11` of the **kernel thread** | `p->context` ([kernel/proc.h:103](./kernel/proc.h:103)) | `swtch()` | per process |
| **trapframe** | the 32 **user** registers + kernel `sp`, `satp`, `epc` | `p->trapframe` ([kernel/proc.h:102](./kernel/proc.h:102)), one page | the trampoline (`uservec`/`userret`) | per process |
| **user address space** | text, data, stack, heap | `p->pagetable`, `p->sz` | `exec()`/`sbrk()`; `satp` switch in the trampoline | per process |

**Why an ordinary user program cannot dereference `proc[]`.** `proc[]` lives at a **kernel virtual
address**. User page tables contain only the process's own memory plus the trampoline page — there is
no valid user address for `proc[]` at all, so any attempt is a page fault (scause 13/15) and the
process is killed. Even if it were mapped, the table is only consistent while its locks are held.
**This is exactly why Lab 1 added a *syscall* (`getproccount`) rather than exporting the table.**

---

## Checkpoint 2 — Policy and mechanism

### Reading a `Ctrl-p` listing

`Ctrl-p` → [kernel/console.c:141](./kernel/console.c:141) `case C('P'): procdump();` → prints
`pid state name` for every non-`UNUSED` entry ([kernel/proc.c:673](./kernel/proc.c:673)).

| Column | Meaning |
|---|---|
| pid | process id (immutable while alive) |
| state | from a table inside `procdump()`: `unused`, `used`, `sleep `, **`runble`**, **`run`**, `zombie` |
| name | the `char name[16]` set by `exec` — **debugging only** |

Note the abbreviations: `RUNNABLE` prints as **`runble`** and `RUNNING` as **`run`**. Not the enum names.

**Why it is only a debugging snapshot.** The interrupt can arrive at any instant; it prints whatever
is true then; a process `run` in one listing can be `runble` in the next. And `procdump()` takes
**no locks** — its own comment says *"No lock to avoid wedging a stuck machine further"* — so it
accepts a possibly torn table rather than risk deadlocking a machine that is already stuck.

### One timer-triggered preemption

```
timer interrupt
  -> kernel/kernelvec.S kernelvec            (or uservec + usertrap if taken in user mode)
  -> kernel/trap.c:135 kerneltrap()
       devintr() == 2 (timer) -> if(which_dev == 2 && myproc() != 0) yield();   (:154)
  -> kernel/proc.c:514 yield()
       acquire(&p->lock);  p->state = RUNNABLE;  sched();
  -> kernel/proc.c:493 sched()
       asserts p->lock held, noff == 1, state != RUNNING, interrupts off
       swtch(&p->context, &mycpu()->context)                                    (:508)
  -> scheduler() resumes after its own swtch() (:469), clears c->proc,
     releases p->lock, looks for the next RUNNABLE process
```

### The two `swtch()` call sites (annotate these)

| Site | Saves | Restores | Think of it as |
|---|---|---|---|
| [kernel/proc.c:469](./kernel/proc.c:469) `swtch(&c->context, &p->context)` | the **per-CPU scheduler context** | the **selected process's kernel context** | CPU → process |
| [kernel/proc.c:508](./kernel/proc.c:508) `swtch(&p->context, &mycpu()->context)` | the **process's kernel context** | the **per-CPU scheduler context** | process → CPU |

**Per-process vs per-CPU.** `struct proc.context` belongs to a *process* — it is where that process's
kernel thread was last suspended. `struct cpu.context` belongs to a *CPU* — it is the context of
whatever kernel thread is currently executing there (usually `scheduler()`'s own stack). One CPU
services many processes, so there is exactly one `c->context` per CPU and one `p->context` per process.

**Where a suspended process resumes.** Its `sp`/`ra` were saved by `swtch()` called *from* `sched()`,
so when the scheduler later picks it again, `swtch()` returns **inside `sched()`**, which returns to
`yield()`/`sleep()`/`exit()`, which continues exactly where it stopped. A process preempted at
`yield()` resumes in the middle of `yield()`.

**Note this is a *kernel*-level switch.** The user registers were already saved in the **trapframe**
when the trap was entered, so `swtch()` only has to preserve the kernel thread's own state.

### Why `s0`–`s11`, `ra` and `sp` are sufficient

`struct context` ([kernel/proc.h:2](./kernel/proc.h:2)) is `ra`, `sp`, `s0`–`s11`; `swtch.S` stores
and loads exactly those 14 values at offsets 0, 8, 16 … 104.

The argument rests on `swtch()` being an **ordinary function call**:

* **Callee-saved `s0`–`s11`** are the only registers the calling convention guarantees survive a
  call, so any live value the *caller* of `swtch()` holds in them must be preserved — saving them is
  exactly what makes the switch invisible to the C code on both sides.
* **Caller-saved `a0`–`a7`/`t0`–`t6` need no saving** — they are *already* treated as dead across a
  call. The compiler spills them to the stack *before* calling `swtch()` and reloads them after. Their
  live values are already in memory, which `sp` covers.
* **`ra` is not callee-saved — and that is why it must be saved explicitly.** The convention is that a
  function needing to return saves `ra` itself. `swtch()` deliberately wants to "return" to a
  *different* place, so it stores the outgoing `ra` and loads the incoming one; the final `ret` jumps
  there.
* **`sp`** is the other half: `ra` says *where* to resume, `sp` says *with which stack*.

> Do not say "`ra` is callee-saved". It is not. It is saved **because** it is caller-saved.

### The strict even-PID policy

**The rule.** At each selection point, take a `RUNNABLE` **even**-PID process whenever one is found;
consider odd-PID processes only when no eligible even one exists. Process-table order is preserved
*within* each class.

**Implementation shape.** Wrap the existing scan in two passes and filter on parity — that is the
whole change:

```c
for(int pass = 0; pass < 2 && found == 0; pass++){
  int want_even = (pass == 0);
  for(p = proc; p < &proc[NPROC]; p++) {
    acquire(&p->lock);
    if(p->state == RUNNABLE && (((p->pid % 2) == 0) == want_even)) {
      p->state = RUNNING;  c->proc = p;  swtch(&c->context, &p->context);
      c->proc = 0;  found = 1;
    }
    release(&p->lock);
  }
}
```

**Invariants you must not break** (the checkpoint asks about these): `p->lock` held around the state
check and the transition; `RUNNABLE → RUNNING` under that lock; `c->proc` set before / cleared after
`swtch()`; the lock handed to the process over the switch; `wfi` only when nothing ran; and timer
preemption **kept** (`intr_on()`/`intr_off()` and `yield()` untouched). `p->pid` is immutable while a
process is alive, so reading it under `p->lock` is safe.

**Why the fallback scan does not restart per process.** The stock loop *continues to the next slot
after `swtch()` returns* rather than restarting from `proc[0]`. Keeping that is what preserves
round-robin *within* a class. If you restarted at `proc[0]` every time, a low-index process would be
re-selected immediately after each preemption and starve its own class-mates.

**Why odd children can appear first in `schedtest` and it is still correct.** All four children were
blocked on a gate pipe; the parent (odd) was chosen by the fallback because **no even process was
`RUNNABLE` at that selection point**. While the parent ran, its `write()` woke the children — and the
scheduler resumed *inside the same fallback pass*, picking up the newly-`RUNNABLE` odd children
before starting a fresh even-first pass. The policy is about eligibility **at the moment of
selection**; that condition was satisfied. This is a consequence of the deliberately non-atomic scan,
not a bug.

### Starvation

**What `schedtest` shows.** Under strict priority the even children (4, 6) run rounds 1–4
back-to-back and **exit** before the odd children (5, 7) finish. But because the workload is finite,
the odds eventually run — so `schedtest` demonstrates **postponement and later progress**, not
starvation. It cannot show starvation, and you must say so.

**What `starvetest` shows.** Two children loop forever with no sleep, I/O or exit. `Ctrl-p` under the
stock scheduler alternates the `run` marker between pid 4 and pid 5 (both progress). Under strict
priority, **pid 4 is always `run` and pid 5 is always `runble`**, in every snapshot.

**Why it can continue indefinitely.** The policy is *strict*: while **any** even-PID process is
`RUNNABLE` at a selection point, an odd one is never chosen. A preempted CPU-bound even process is
`RUNNABLE` again immediately, so the odd child's "no eligible even process" condition is never
satisfied. The odd process stays runnable forever without ever being selected.

**Two caveats worth marks.**

* **Snapshots prove postponement only over the observed interval** — they are not a proof of
  permanent starvation, which comes from the *policy argument*, not the listing.
* **This needs `CPUS=1`.** With three CPUs, an even process that is `RUNNING` on another CPU is *not*
  a `RUNNABLE` candidate for this CPU, so a single busy even process does not establish starvation.
  (`starvetest` notes this itself; the shell may also be starved, so use `Ctrl-a x` rather than
  relying on a shell `kill`.)

**Deliverable discipline.** Save the strict-priority code *and* its evidence, then **restore the
stock `scheduler()`** for Part 3 and final verification — otherwise strict priority would be imposed
on tests that assume eventual progress. A clean build does **not** restore the scheduler; `CPUS=3`
does not either.

---

## Checkpoint 3 — The cooperative user-thread switch

### Three levels of "thread" — keep them apart

| | xv6 process | its kernel thread | user threads in the library |
|---|---|---|---|
| Address space | its own (`satp`) | same as the process | **shared with each other** |
| Stack | kernel stack + user stack | kernel stack | **one private stack each** |
| Saved state | trapframe + `struct context` | `struct context` | `struct context` (library's own) |
| Who switches | the kernel | the kernel | the library, **cooperatively** |
| When | any trap (preemptive) | any trap | only at `thread_yield()`/`thread_exit()` |
| Trapframe per switch? | yes | — | **no** |

Each xv6 process has exactly **one** kernel thread. The library's user threads share that one kernel
thread and one address space — that is what makes the switch cheap and why a trapframe is unnecessary:
the user registers never need saving, because no trap occurs during a user-level switch.

### The context layout must match the assembly exactly

```c
struct context { uint64 ra, sp, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11; };
```

offsets: `ra`@0, `sp`@8, `s0`@16 … `s11`@104 — mirroring [kernel/proc.h:2](./kernel/proc.h:2) and
[kernel/swtch.S](./kernel/swtch.S), and matched field-for-field by
[user/uthread_switch.S](./user/uthread_switch.S).

**This is the classic silent failure:** a mismatched layout **compiles fine** and then restores
registers from the wrong offsets, producing a crash that looks nothing like the cause. Whenever you
edit one side, edit the other.

### Where the context lives

`struct thread` keeps a **pointer** to a context ([user/uthread.c:38](./user/uthread.c:38)) rather than
embedding it, so the context can sit at the **top of each thread's own stack** while still being
passed to `thread_switch(uint64, uint64)` as a plain 64-bit value — the supplied signature must not
change.

```
   high address
   +--------------------------+  <- stack[] + STACK_SIZE
   |   struct context (112B)  |  <- t->context points here  (also the initial sp)
   +--------------------------+
   |                          |
   |   the thread's stack     |  grows DOWN into here
   |                          |
   +--------------------------+  <- stack[]
   low address
```

**16-byte alignment** ([user/uthread.c:44](./user/uthread.c:44)): the ABI requires `sp` to be 16-byte
aligned on function entry, so the slot is computed as
`(top - sizeof(struct context)) & ~0xf`. `sizeof(struct context)` is 112 and `STACK_SIZE` is 8192, so
only the array's base address could break alignment — masking removes that dependency entirely.

**Thread 0 needs a context pointer too** ([user/uthread.c:54](./user/uthread.c:54)). `main()` is thread
0 and makes the first `thread_schedule()` call; `thread_switch()` writes the outgoing context
*through* `current_thread->context`. Left at its zero initialiser, the first switch would store to
address 0 — in xv6 user space that is the program **text** — and fault. Thread 0 runs on the
process's real stack, so its `stack[]` is used purely as a **save area**.

### New thread vs resumed thread

| | `ra` | `sp` | Where they come from |
|---|---|---|---|
| **new** thread | the thread function | the top of its own stack | **fabricated** by `thread_create()` |
| **resumed** thread | the return address inside `thread_schedule()` | its real stack pointer | **written** by `thread_switch()` itself |

`thread_create()` ([user/uthread.c:99](./user/uthread.c:99)) builds the new one:

```c
t->state = RUNNABLE;
t->context = thread_context_slot(t);
memset(t->context, 0, sizeof(struct context));
t->context->ra = (uint64)func;
t->context->sp = (uint64)t->context;   // 16-byte aligned
```

`ra = func` makes the final `ret` *begin the function*; `sp` pointing at the context slot gives it a
valid, aligned stack. The `s0`–`s11` values are irrelevant to a brand-new function (its prologue sets
`s0` itself) but are zeroed so nothing depends on uninitialised memory.

### One `thread_yield()`, end to end

```
thread_yield()
  current_thread->state = RUNNABLE
  thread_schedule()
    scan for the next RUNNABLE thread (starting at current_thread + 1, wrapping)
    next_thread->state = RUNNING
    t = current_thread                 <- outgoing, captured BEFORE reassignment
    current_thread = next_thread
    thread_switch((uint64)t->context, (uint64)next_thread->context)
      a0 = outgoing context:  save ra, sp, s0..s11
      a1 = incoming context:  load  ra, sp, s0..s11
      ret                              <- jumps to the INCOMING thread's ra
```

The outgoing thread's `ra` is the instruction after the `call thread_switch`, so when it is eventually
restored it resumes inside `thread_schedule()`, returns to `thread_yield()`, and carries on.

### The test and why the order varies

All three threads print `started`, set their flag, then busy-wait with `thread_yield()` until the
other two flags are set. Each yield re-enters `thread_schedule()`, which resumes its scan at
`current_thread + 1` and wraps — so the threads round-robin through the startup spins. Once the last
flag is set, all three are released together and the order in which they emit `0…99` is whatever the
scan happens to pick, **not** the `thread_create()` call order. The test asserts nothing about order,
only about the values.

**Checks that matter:** all three start; each prints its own 0…99 **exactly once** (no skips, no
repeats); each reports `exit after 100`; the library finally reports
`thread_schedule: no runnable threads`.

---

## Checkpoint 4 (optional, not examinable) — Debugging a switch with GDB

**Use function breakpoints, not line numbers**, because editing the source moves lines:

```
(gdb) file user/_uthread_test
(gdb) break thread_schedule
(gdb) break thread_switch
```

A user virtual address can be hit while a *different* process occupies the same address, so continue
until the stop really corresponds to `uthread_test`.

**What to inspect:** `*current_thread` and `*next_thread` (the outgoing and incoming contexts), then
`info registers ra sp s0 s1` and the context memory at those addresses, then `stepi` to watch `ret`
land on the incoming thread's `ra` with its `sp`.

**Why `ret` resumes a *different* thread.** `ret` is just `jalr x0, 0(ra)`. It does not "return to the
caller" in any semantic sense — it jumps to whatever address is in `ra`. Because `thread_switch()`
loaded `ra` (and `sp`) from the **incoming** context, the jump goes to the incoming thread's resume
point on the incoming thread's stack. There is no stack unwinding and no runtime bookkeeping; the
"thread switch" is entirely explained by two registers.

**Using it as a diagnostic.** A stop that shows plausible `ra`/`sp` but a crash afterwards suggests a
*C/assembly offset* mismatch; garbage `ra`/`sp` suggests a bad *initial context*; the right context but
the wrong thread running suggests a *switch-argument* or *state-transition* bug.

---

## Final self-check — answers without AI

1. **Why can `procdump()` read `proc[]` while a user program cannot?** It runs in kernel mode, where
   the kernel page table maps `proc[]`. A user program runs on its own page table, which maps only its
   own memory plus the trampoline page — `proc[]` has no valid user address. (`procdump()` also runs
   lock-free by design, accepting a torn snapshot to avoid deadlocking a stuck machine.)
2. **How does a timer interrupt lead from a running process to the scheduler and back?** Timer →
   `kerneltrap()` (or `usertrap()`), `devintr()` returns 2 → `yield()`: `RUNNING → RUNNABLE` under
   `p->lock` → `sched()` calls `swtch(&p->context, &mycpu()->context)`, saving the process context and
   restoring the per-CPU scheduler context → `scheduler()` resumes after its own `swtch()`, clears
   `c->proc`, releases `p->lock`, then later sets a `RUNNABLE` process to `RUNNING` and calls
   `swtch(&c->context, &p->context)` — which returns *inside that process's own* `sched()`, so it
   continues in `yield()`, returns to the trap handler, and `sret`s back to user mode.
3. **What workload can starve an odd-PID process?** One where an even-PID process stays `RUNNABLE`
   without ever blocking — a pure CPU loop with no sleep, I/O or exit (exactly `starvetest`). Strict
   priority selects an odd process only when no even one is `RUNNABLE` at that selection point, and a
   CPU-bound even process becomes `RUNNABLE` again immediately after every preemption. Use `CPUS=1`.
4. **Why are callee-saved registers, `ra` and `sp` sufficient?** `thread_switch()` is an ordinary
   function call, so caller-saved registers are already dead across it (spilled to the stack that `sp`
   covers), while callee-saved `s0`–`s11` must be preserved for the C code on both sides. `ra` is not
   callee-saved, which is exactly why it is saved explicitly — the switch wants to return elsewhere.
   `ra` + `sp` relocate execution to the incoming thread's resume point and stack.
5. **How does a never-run user thread begin at its function on its own stack?** `thread_create()`
   fabricates a context at the 16-byte-aligned top of that thread's `stack[]` with `ra = func` and
   `sp` = the context slot. When the scheduler selects it, `thread_switch()` loads that `ra`/`sp` and
   `ret`s to `func`; the frame then grows down into the thread's own stack.
6. **Kernel scheduling a process vs. the library scheduling a user thread.** The kernel switches
   *processes*: it saves a kernel `struct context` **and** the user registers in the trapframe, and
   changes `satp` so each process has its own memory; it is preemptive and can happen at any trap. The
   library switches *user threads inside one process*: they share one address space, one set of page
   tables and one kernel thread, only `ra`/`sp`/`s0`–`s11` are saved, and switching happens only
   cooperatively at `thread_yield()`/`thread_exit()` — so no trapframe is created per user thread.

---

## Traps that cost marks

| Trap | Correct version |
|---|---|
| "`ra` is callee-saved." | It is **caller-saved**; `swtch` saves it *because* it is not preserved across calls. |
| "Caller-saved registers must be saved by `swtch`." | They are already dead across the call — the compiler spilled them. Saving them is redundant. |
| "Selecting a `SLEEPING` process is fine, it will just block again." | It must stay `SLEEPING` until `wakeup()`, or its condition may not hold. |
| "A user program could read `proc[]` if it knew the address." | There is no valid user mapping for it — it faults. |
| "`Ctrl-p` gives an accurate process count." | It is a lock-free snapshot at an arbitrary instant, possibly torn. |
| "The `run`/`runble` strings are the enum names." | They are console abbreviations from a table in `procdump()`. |
| "`schedtest` proves the odd process starves." | It has finite work, so it shows **postponement** only. Starvation needs the policy argument (`starvetest`). |
| "Starvation can be shown with `CPUS=3`." | No — a `RUNNING` even process is not a `RUNNABLE` candidate elsewhere. Use `CPUS=1`. |
| "Restoring the scheduler happens automatically / via `CPUS=3`." | Neither. You must `git checkout` / re-edit `scheduler()` back by hand. |
| "A context field-order mistake will fail to compile." | It compiles and corrupts at runtime. **This is the classic bug.** |
| "`thread_create` needs to copy the function's stack." | It only needs `ra` and a 16-byte-aligned `sp`. |
| "Thread 0 doesn't need a context because it's already running." | It needs a **writable slot** for the first `thread_switch()` to save into. |
| "The startup order is the `thread_create()` order." | It is whatever the wrap-around scan picks; the test asserts nothing about order. |

---

## Cross-lab connections

* **Lab 1** introduced the `RUNNABLE`/`RUNNING`/`ZOMBIE` states through `Ctrl-p` and the zombie; this
  lab explains *who* chooses among them and how the choice is made atomically.
* **Lab 1**'s `fork()` trace stops at "the child returns"; this lab's `fork → forkret` route is the
  missing middle — *how* a brand-new process ever gets onto a CPU for the first time.
* **Lab 1 Checkpoint 4**'s trapframe is the user-register half of a context switch; this lab's
  `struct context` is the kernel half. Together they are everything a switch must preserve.
* **Lab 3** builds `sleep()`/`wakeup()` on top of the very `RUNNABLE`/`SLEEPING` transitions and the
  `swtch()` mechanism you study here — `sleep()` is a scheduling operation, not a delay.
* The user-level `thread_switch` here is a miniature of `swtch`: same register discipline, same
  "`ret` to a loaded `ra`" trick, but with no kernel, no trapframe and no page-table change.
