# SC2005 Lab 1 — Revision Notes

Study material for the Lab 1 checkpoints. Command output and evidence live in
[LAB1_ANSWERS.md](./LAB1_ANSWERS.md); this file is the *learning*: the concepts, the "why", and the
traps. Everything here is answerable without the lab in front of you.

---

## The lab in one paragraph

You learn where the boundary between *user* and *kernel* actually is. xv6 is built on the host,
packed into a disk image, and booted; a user program only becomes a command if the build puts it in
that image; a process that exits is not gone until its parent reaps it; and a system call is a
number in a register plus a trap, wired together at build time by a **generated** stub and at
runtime by a **numbered dispatch table**. Then you add one syscall end to end, and use two pipes to
get data flowing both ways between a parent and a child.

---

## Checkpoint 0 — Two shells, two worlds

**What it asks.** Navigate with `pwd`/`ls`/`cd`; identify the command and argument in `cat
README.md`; stop `sleep 30` with Ctrl-C.

**The knowledge.**

* In `cat README.md`, **`cat` is the program** and **`README.md` is the argument**. A command line is
  `program [arguments…]`; the shell splits on whitespace and `exec`s the first word.
* **Ctrl-C is a signal (SIGINT), not text.** The terminal driver turns the keypress into a signal to
  the *foreground process group*; `sleep 30` dies and the shell prints another prompt. You never type
  `^C`.
* **`host$` and `xv6$` are different machines, conceptually.** The host shell runs on Linux/macOS
  with a full toolchain and file system. The xv6 shell runs inside QEMU with its own, much smaller
  file system and no compiler. They share nothing: not a working directory, not a file, not a
  command set. Host tools like `grep`/`make`/tab-completion do not exist in xv6 unless that program
  is in the image.

**The most common confusion** is running a host command at the xv6 prompt (or vice versa). Ask
yourself: *what did I just launch, and what output appeared last?*

---

## Checkpoint 1 — Build, boot, and UPROGS

**What it asks.** Boot and exit; is `make qemu` host or xv6; what is `UPROGS` for?

**The build pipeline** — three stages, and only the last one makes a command:

```
user/name.c  -->  user/name.o  -->  user/_name  -->  fs.img  -->  "name" at the xv6 prompt
   source          compile        link w/ ulib,      mkfs        (exec-able file)
                                  usys, printf,      copies
                                  umalloc
```

**`make qemu` runs on the host.** It compiles `kernel/kernel`, builds `fs.img`, then runs
`qemu-system-riscv64 -kernel kernel/kernel -drive file=fs.img,…`. You cannot run `make` inside xv6.

**`UPROGS` is the list of user programs that go into the image** ([Makefile:128](./Makefile:128)).
`fs.img` is built by `mkfs/mkfs fs.img README $(UPROGS)` ([Makefile:149](./Makefile:149)) — so
`UPROGS` literally *is* the manifest of what the xv6 shell will be able to run. Adding a line to
`UPROGS` is what "installs" a program.

**`Ctrl-a x` exits QEMU.** It is a QEMU escape sequence, not something xv6 sees: hold Ctrl, press
`a`, release both, press `x`. Different from Ctrl-C, which signals a program *inside* the guest.

**Why `make clean` matters after switching branches.** It also removes **generated** files —
`user/usys.S`, `fs.img`, the `.asm`/`.sym` dumps, every `.o`. A different branch can have a different
`usys.pl` or `syscall.h`, so a stale `usys.S` mixed with new kernel code produces confusing
"unknown syscall" behaviour. Clean makes the branch's own sources authoritative.

---

## Checkpoint 2 — A source file is not a command

**What it asks.** Why was `pingpong` unavailable, and what changed?

**The answer.** `user/pingpong.c` existed, but `_pingpong` was not in `UPROGS`, so the file was never
compiled, never linked, and never copied into `fs.img`. At the prompt, the shell's `exec("pingpong")`
found no such file in the xv6 file system and reported `exec pingpong failed`.

**The mental model:** *the xv6 file system is a build artifact, not your source directory.* Nothing
you write is visible inside xv6 until the build puts it in the image.

| Symptom | Cause |
|---|---|
| `exec foo failed` | `foo` is not a file in `fs.img` — usually a missing `UPROGS` entry |
| A stale build behaves oddly | generated files from another branch — `make clean` |

---

## Checkpoint 3 — Processes, `fork()`, and the zombie

**What it asks.** The `fork()` return convention; a `Ctrl-p` listing with a zombie; and the
difference between *stopped running* and *reaped*.

**`fork()` return convention** ([kernel/proc.c:280](./kernel/proc.c:280)):

| In | Return value | Meaning |
|---|---|---|
| child | **0** | "you are the new process" — the child's pid is not knowable *as* 0, so 0 is the sentinel |
| parent | **child's pid** (> 0) | so the parent can `wait(pid)` / `kill(pid)` |
| either | **-1** | fork failed (no free slot, no memory) |

This single integer is how one piece of code becomes two behaviours — which is why every `fork()`
example in the lab is wrapped in `if (pid == 0) { child } else { parent }`.

**The zombie lifecycle.**

```
fork()            child: RUNNABLE
child exit()      state = ZOMBIE           <- exited, but the slot is still occupied
parent wait()     freeproc(child)          <- slot returns to UNUSED
```

`exit()` ([kernel/proc.c:379](./kernel/proc.c:379)) sets `ZOMBIE` and calls `sched()` **without
returning** — so a zombie is a process that will never run again, yet still owns its `struct proc`
entry, its pid and its exit status. `wait()`
([kernel/proc.c:417](./kernel/proc.c:417)) is what calls `freeproc()`, returning the slot to
`UNUSED` and letting the pid be reused.

**The distinction the checkpoint wants.**

| | Stopped running (`ZOMBIE`) | Entry reaped (`UNUSED`) |
|---|---|---|
| Is it on a CPU? | no | no |
| Does the `struct proc` slot exist? | **yes** | **no** — returned to the pool |
| Is the pid reserved? | yes | no, reusable |
| Is the exit status available? | yes, for the parent to collect | no |
| Who makes this happen? | the child's own `exit()` | the parent's `wait()` |

A zombie is *information waiting to be collected*. Without `wait()`, the parent would leak the slot —
`zombie.c` deliberately creates this state to make it visible.

**`Ctrl-p`** is the console interrupt handler calling `procdump()` ([kernel/console.c:141](./kernel/console.c:141)),
which prints `pid state name` for every non-`UNUSED` entry
([kernel/proc.c:689](./kernel/proc.c:689)). The state strings come from a table inside it: a
`RUNNABLE` process prints as **`runble`**, a `RUNNING` one as **`run`** — the abbreviations, not the
enum names. `procdump()` deliberately takes **no locks** ("no lock to avoid wedging a stuck machine
further"), so it is a *debugging snapshot*, not a measurement: it can read a torn table, and a
process that is `run` in one listing may be `runble` in the next.

**Why `sleep(5)` made this hard to see.** xv6's `sleep(int)` counts **clock ticks**, not seconds.
`sleep(5)` is a tiny window; the manual's temporary change to `sleep(100)` is purely to widen it so a
human can press `Ctrl-p` in time.

---

## Checkpoint 4 — The system-call boundary

This is the biggest checkpoint in the lab. The point is to see that a syscall is **two wires** — one
laid at *build time*, one followed at *runtime*.

### Build-time path (creates the user-side call stub)

| Step | File | What happens |
|---|---|---|
| 1 | [user/user.h:21](./user/user.h:21) | `int getpid(void);` — the declaration the compiler checks calls against |
| 2 | [user/usys.pl:35](./user/usys.pl:35) | `entry("getpid");` — a **Perl generator** |
| 3 | `user/usys.S` (**generated**) | the generator's output: `li a7, SYS_getpid` / `ecall` / `ret` |
| 4 | [kernel/syscall.h:12](./kernel/syscall.h:12) | `#define SYS_getpid 11` — the shared number |

`usys.pl` is run by a Makefile rule ([Makefile:107](./Makefile:107)) on **every build**, and the result
is included in every user program by the linker.

### Runtime path (follows the number)

| Step | File | What happens |
|---|---|---|
| 5 | caller | stub loads **a7 = 11** and executes **`ecall`** |
| 6 | [kernel/trampoline.S:22](./kernel/trampoline.S:22) `uservec` | saves all 32 user registers into the **trapframe**, loads kernel `sp`/`satp`, jumps to `usertrap` |
| 7 | [kernel/trap.c:37](./kernel/trap.c:37) `usertrap()` | dispatches on `scause`; an `ecall` from user mode → `syscall()` |
| 8 | [kernel/trap.c:61](./kernel/trap.c:61) | `p->trapframe->epc += 4;` so `sret` resumes *after* the `ecall` |
| 9 | [kernel/syscall.c:139](./kernel/syscall.c:139) | `num = p->trapframe->a7;` — the generic dispatcher reads the number |
| 10 | [kernel/syscall.c:143](./kernel/syscall.c:143) | `p->trapframe->a0 = syscalls[num]();` — call through the table, result into **a0** |
| 11 | [kernel/syscall.c:119](./kernel/syscall.c:119) | `[SYS_getpid] sys_getpid,` — the numbered dispatch-table entry |
| 12 | [kernel/sysproc.c:19](./kernel/sysproc.c:19) | `sys_getpid()` → `return myproc()->pid;` |
| 13 | [kernel/trap.c:90](./kernel/trap.c:90) → [kernel/trampoline.S:101](./kernel/trampoline.S:101) → [:151](./kernel/trampoline.S:151) | `usertrapret()` / `userret` / `sret` — restores user registers; **a0 carries the result back** |

**The register rules worth memorising:** number in **a7**, arguments in **a0–a5**, return value in
**a0**. The trapframe is *the* place a syscall's arguments and results live while the kernel runs.

### Why the number must match on both sides

The stub hard-codes `li a7, SYS_getpid` (expanded from `syscall.h`), and `syscall()` indexes
`syscalls[]` with the *same* macro. Because the table is **designated-initialised**
(`[SYS_getpid] = sys_getpid`), a missing entry is a **NULL pointer**, not a compile error — so a
mismatch doesn't fail loudly, it silently calls the wrong handler or returns `-1`. That is why the
number is defined in exactly one place and used in both.

### Why the trap path needs no per-call edit

`uservec`/`usertrap`/`usertrapret` are **generic**: they save/restore the whole trapframe
indiscriminately and hand one number to one shared dispatcher. Adding a syscall changes only **data**
— a number, a table entry, a handler — never the machinery. This is the design lesson: the
trap/interrupt path is a *mechanism*, and syscalls are *policy* plugged into it.

### Adding a syscall: the four categories

| Category | What it means | `getproccount` examples |
|---|---|---|
| **inspect** | read to understand the pattern | `syscalls[]`, `procdump()`, `SYS_getpid` |
| **edit** | existing file you must change | `user/user.h`, `user/usys.pl`, `kernel/syscall.h`, `kernel/syscall.c`, `kernel/sysproc.c`, `kernel/proc.c`, `kernel/defs.h`, `Makefile` |
| **create** | new file | `user/proccount.c` |
| **generated** | produced by the build — **never edit** | `user/usys.S` |

**Plan the change in two halves**, as the manual insists:

* **registration** — number, stub generator, dispatch table, handler prototype;
* **implementation** — the actual counting, which lives with the data it counts (`proc[]` in
  `kernel/proc.c`, not in the syscall wrapper).

Keeping them separate is why `sys_getproccount()` is a one-liner that calls `proccount()`.

### `getproccount()`'s contract

> The number of process-table entries whose state is not `UNUSED` **at the instant each entry is
> inspected**. `USED`, `SLEEPING`, `RUNNABLE`, `RUNNING` and `ZOMBIE` all count.

The wording matters: it is a **per-entry snapshot**, not an atomic view. That is why the natural
implementation is the same lock-free scan as `procdump()`.

### Why `proccount` and `Ctrl-p` disagree

They are **snapshots taken at different instants**, and one of them can see a process the other
cannot:

* `proccount` runs as a process. At the moment it calls the syscall, it is `RUNNING` and therefore
  counts **itself** — so at a fresh boot it prints **3** (`init`, `sh`, `proccount`).
* `Ctrl-p` can only be pressed when the shell is idle at the prompt, i.e. *after* `proccount` has
  exited and its slot is `UNUSED` — so it prints **2** (`init`, `sh`).

Neither takes a lock, so both can read a table that is changing underneath them.

---

## Checkpoint 5 — Pipes

### The abstraction

`pipe(int p[2])` makes **one unidirectional byte stream**:

* **`p[0]` is the read end**;
* **`p[1]` is the write end**.

It reads like a file of unknown length: bytes come out in order, `read()` blocks when empty, and
`write()` blocks when full (the buffer is `PIPESIZE` = 512 bytes,
[kernel/pipe.c:11](./kernel/pipe.c:11)).

**Why two pipes for a request-reply.** A pipe is one-way — one end is readable, the other writable
([kernel/pipe.c:38-45](./kernel/pipe.c:38)). The parent needs to *send* and also to *receive*, so it
needs one pipe in each direction:

```
  parent  ---ping--->  p2c  --->  child
  parent  <--pong----  c2p  <---  child
```

### Descriptors after `fork()`

`fork()` duplicates the **whole descriptor table**, so immediately after the fork **each process holds
all four endpoints**:

```
            p2c[0]   p2c[1]   c2p[0]   c2p[1]
parent:      keep    close ~   keep    close ~
child:       keep    close ~  close ~   keep
```

**Why close the unused ends promptly.** Two reasons:

1. **Correctness — EOF.** A reader sees EOF only when the pipe is empty *and* no write reference
   remains. If the parent keeps its copy of `p2c[1]` open forever, the child's read-until-EOF blocks
   forever, because the pipe still has a writer (`writeopen == 1`).
2. **Tidiness — descriptor budget.** `NOFILE` descriptors per process is small; leaked ends exhaust
   it.

### Reference counting: the crux of the checkpoint

`fork()` does **not** copy the pipe; it copies the *descriptor* and increments a reference count on
the shared open-file object ([kernel/file.c:53](./kernel/file.c:53) `f->ref++`). So:

| Action | Effect |
|---|---|
| `close(fd)` in one process | `f->ref--`; the underlying pipe stays open if other references remain |
| the **last** reference closes | `fileclose()` runs the cleanup → `pipeclose()` sets `writeopen`/`readopen = 0` and wakes the other side ([kernel/pipe.c:59](./kernel/pipe.c:59)) |

**So "closing one descriptor" and "closing the endpoint" are different events.** This is *the* reason
an unused write descriptor left open in the reader's own process causes a hang instead of EOF — a
classic bug, and the one the manual asks you to test by prediction.

### EOF vs. writing with no readers

| Operation | Condition | Result |
|---|---|---|
| `read()` | buffer empty **and** all write ends closed | returns **0** — EOF, a normal value |
| `write()` | all read ends closed | error: xv6 returns **-1** after `setkilled()`, killing the process ([kernel/pipe.c:84](./kernel/pipe.c:84)); POSIX would raise SIGPIPE |

The distinction: EOF is a *value* a read can return; a broken pipe is an *error* a write raises. They
are not symmetric.

---

## Final checkpoint — answers without AI

1. **Why is adding `user/program.c` alone insufficient?** It is never compiled, linked or copied into
   `fs.img`, which is built from `$(UPROGS)`. The xv6 shell can only `exec` a name that exists as a
   file inside the image.
2. **What does the generated stub place in a7, and what enters the kernel?** `li a7, SYS_<name>` puts
   the syscall **number** in **a7**; **`ecall`** raises the environment-call exception that enters
   the kernel. Arguments ride in a0–a5; the return value comes back in a0.
3. **Why can `getproccount()` differ from `Ctrl-p`?** Different instants, and `proccount` counts
   *itself* (a `RUNNING` process) while `Ctrl-p` can only be taken at the idle prompt after it has
   exited. Neither takes a lock.
4. **Why does closing one post-`fork()` descriptor not close the endpoint?** `fork()` duplicated the
   descriptor and bumped the open-file reference count; `close()` only decrements it. The endpoint
   lives until the **last** reference is dropped.
5. **What distinguishes EOF from a write with no readers?** A read on a fully-closed write end returns
   **0** (EOF); a write to a fully-closed read end **fails** (xv6 returns -1 and kills the process).

---

## Traps that cost marks

| Trap | Correct version |
|---|---|
| "The source file exists, so the command should work." | Only `UPROGS` entries reach `fs.img`. |
| "`make qemu` runs inside xv6." | It runs on the **host**; it starts QEMU. |
| "Ctrl-C exits QEMU." | `Ctrl-a x` exits QEMU; Ctrl-C signals the guest's foreground program. |
| "`fork()` returns the child's pid in the child." | The **child gets 0**; the parent gets the pid. |
| "`exit()` frees the process slot." | `exit()` sets `ZOMBIE`; the **parent's `wait()`** frees it. |
| "`usys.S` is a source file — just add a line." | It is **generated** from `usys.pl` on every build. |
| "Add a syscall by editing the trap handler." | The trap path is generic; edit the number, the table, the handler. |
| "`read()` returning 0 means 'nothing available'." | 0 means **EOF**; emptiness makes it *block*. |
| "`close()` closes the pipe." | It drops one reference; the pipe closes when the **last** one goes. |
| "`sleep(5)` sleeps 5 seconds." | xv6's `sleep(int)` counts **clock ticks**. |

---

## Cross-lab connections

* **Lab 2** takes the `RUNNABLE`/`RUNNING`/`SLEEPING` states you first meet here (via `Ctrl-p`) and
  asks who chooses among them. The `fork → forkret` route is the full story behind step 3 of this
  lab's `fork()`.
* **Lab 3** picks up the `wait()`/`wakeup()` machinery and the idea that *a sequence*, not a single
  operation, is what needs protecting — the same lesson as the two-syscall counter here.
* The trap/trapframe/dispatch-table design in Checkpoint 4 is the same mechanism Lab 3's `sleep()`
  relies on when a process blocks inside a syscall.
