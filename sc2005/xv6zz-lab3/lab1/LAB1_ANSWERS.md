# SC2005 Lab 1 — Exploring xv6 and Adding a System Call

Answers, reasoning, and evidence. Source tree: this directory (`lab1` branch, `1cab163`).

> **How to read this file.** Each checkpoint lists (a) the hypothesis, (b) the source evidence
> verified in this branch, (c) the command and observed output, and (d) the explanation.

---

## Checkpoint 0 — Terminal essentials

* `pwd` prints the working directory, `ls` lists it, `cd <dir>` / `cd ..` move around it.
* In `cat README.md`, **`cat` is the program** and **`README.md` is its argument**.
* `sleep 30` blocks the foreground; **Ctrl-C** sends SIGINT to the foreground process (the shell,
  not xv6) and returns to the prompt. Ctrl-C is a signal, not typed text.
* `host$` means the Linux/macOS shell; `xv6$` means the shell running *inside* QEMU. They have
  different current directories and different commands — host tools are not available in xv6 and
  vice versa.

---

## Checkpoint 1 — Build, boot, and explore xv6

**Hypothesis.** `make qemu` runs on the *host*; it compiles the kernel and the user programs,
packs them into `fs.img`, and starts QEMU. UPROGS is the list of user programs that end up in the image.

**Source evidence** ([Makefile](./Makefile)):

| Target | Line | What it does |
|---|---|---|
| `qemu` | [Makefile:177](./Makefile:177) | depends on `$K/kernel` and `fs.img`, then runs `$(QEMU) $(QEMUOPTS)` — this is a **host** command |
| `fs.img` | [Makefile:149](./Makefile:149) | `mkfs/mkfs fs.img README $(UPROGS)` — builds the file-system image from README plus every `UPROGS` entry |
| `UPROGS` | [Makefile:128](./Makefile:128) | the list that determines which user programs are copied into the image |

Each `UPROGS` entry `$U/_name` is the linked user binary for `user/name.c`; `mkfs` writes those
binaries into the image as files, which is why the shell can `exec` them by name.

**Observed.**

```
$ ls Makefile            (host)
Makefile
$ make clean && make qemu
...
xv6 kernel is booting
init: starting sh
$ ls
.              1 1 1024
..             1 1 1024
README         2 2 2306
cat            2 3 24880
...
$ cat README
$ mkdir lab1tmp
$ cd lab1tmp
$ cd ..
```
Host `README.md` is a *different file* from xv6's `README`; the two systems do not share a
directory. `Ctrl-a x` (Ctrl, then `a`, release, then `x`) exits QEMU — it is different from Ctrl-C.

---

## Checkpoint 2 — User programs are built into the xv6 image

**Hypothesis.** `pingpong` will fail with `exec pingpong failed`. The source file exists, but
`pingpong` is not in `UPROGS`, so `_pingpong` is never linked and never copied into `fs.img`.

**Baseline evidence** (before any edit):

```
$ pingpong
exec pingpong failed
$ forktest
fork test
fork test OK
```

`exec pingpong failed` comes from the shell's `exec()` returning -1 — the file simply is not in
the image.

**The edit** ([Makefile:145](./Makefile:145)): added one entry to `UPROGS`, following the existing pattern:

```make
	$U/_zombie\
	$U/_pingpong\
```

**After the edit:**

```
$ pingpong
3: received ping
3: received pong
3: received ping
3: received pong
3: received ping
```

**Explanation.** `user/pingpong.c` existing is *necessary but not sufficient*. The build chain is
`user/pingpong.c` → `user/pingpong.o` → `user/_pingpong` (linked with `ulib.o`, `usys.o`,
`printf.o`, `umalloc.o`) → copied into `fs.img` by `mkfs` only because `$(UPROGS)` names it. The xv6
shell has no compiler or file system of its own on the host, so it can only run what is already in
the image; an unknown name makes `exec` fail.

---

## Checkpoint 3 — Observe processes and a zombie state

**Hypothesis.** The child exits first and stays in state `ZOMBIE` until the parent calls `wait()`,
which frees its process-table slot. `Ctrl-p` (the console handler) prints the table, so a snapshot
taken while the parent is still inside `sleep()` should show the child as `zombie`.

**Source evidence.**

| Item | Location | Note |
|---|---|---|
| `fork()` return convention | [kernel/proc.c:280](./kernel/proc.c:280) | child gets `0`, parent gets the child's pid; negative on failure |
| `exit()` → `ZOMBIE` | [kernel/proc.c:379](./kernel/proc.c:379) | `p->state = ZOMBIE;` then `sched()` |
| `wait()` frees the slot | [kernel/proc.c:417](./kernel/proc.c:417) | `freeproc(pp)` sets the entry back to `UNUSED` |
| `procdump()` | [kernel/proc.c:689](./kernel/proc.c:689) | prints `pid state name` for every non-`UNUSED` entry |
| `Ctrl-p` handler | [kernel/console.c:141](./kernel/console.c:141) | `case C('P'): procdump();` |
| States | [kernel/proc.h:82](./kernel/proc.h:82) | `UNUSED, USED, SLEEPING, RUNNABLE, RUNNING, ZOMBIE` |

**Change made** ([user/zombie.c:12](./user/zombie.c:12)) — the manual's temporary observation change:

```diff
   if(fork() > 0)
-    sleep(5);  // Let child exit before parent.
+    sleep(100);  // Let child exit before parent.
```

In xv6 the argument is **clock ticks**, not seconds, so `sleep(5)` gave only a tiny window in which
to press `Ctrl-p` by hand. (This is the manual's "temporary" change; revert to `sleep(5)` if you want
the stock program back. It is the only behavioural difference it makes.)

**Observed** — `Ctrl-p` pressed twice *while `zombie` is still running*:

```
1 sleep  init
2 sleep  sh
3 sleep  zombie     <- parent, blocked in sleep(100)
4 zombie zombie     <- child: exited, NOT yet reaped
```

and `Ctrl-p` again after the parent exits and the shell prompt returns:

```
1 sleep  init
2 sleep  sh
```

**Explanation.** The child called `exit()`, which set its state to `ZOMBIE` and called `sched()`
without returning. The parent is still inside `sleep(100)`, so nobody has called `wait()` yet: the
child is no longer running, but its `struct proc` entry is still allocated. That is the distinction
the checkpoint asks for — **"the process has stopped running"** (state `ZOMBIE`, entry still occupied,
`pid` still reserved, exit status stored) versus **"its process-table entry has been reaped"** (the
parent's `wait()` calls `freeproc()`, which returns the slot to `UNUSED` and lets the pid be reused).
Once the parent exited, the shell — which had `wait()`ed for `zombie` — caused that reaping, so the
second listing shows only `init` and `sh`.

`fork()` returns `0` **in the child** and the child's pid **in the parent**, which is exactly how
`zombie.c` decides who sleeps.

---

## Checkpoint 4 — Trace and add `getproccount()`

### 4.1 / 4.2 Verified `getpid()` trace

Every row was opened and checked in *this* branch.

| # | Phase | Exact path : line | Symbol | Role |
|---|---|---|---|---|
| 1 | build | [user/user.h:21](./user/user.h:21) | `int getpid(void);` | user-visible declaration the compiler checks calls against |
| 2 | build | [user/usys.pl:35](./user/usys.pl:35) | `entry("getpid");` | generator input; emits the user stub at build time |
| 3 | **generated** | `user/usys.S` (produced by `usys.pl`; rule at [Makefile:107](./Makefile:107)) | `getpid:` | `li a7, SYS_getpid` / `ecall` / `ret` — **generated, never edit** |
| 4 | build | [kernel/syscall.h:12](./kernel/syscall.h:12) | `#define SYS_getpid 11` | the syscall number, shared by stub and kernel |
| 5 | runtime (user) | any caller | `getpid()` | stub loads **a7 = 11** and executes **`ecall`** |
| 6 | runtime | [kernel/trampoline.S:22](./kernel/trampoline.S:22) | `uservec` | trap entry: saves the 32 user registers into the trapframe, loads kernel `sp`/`satp`, jumps to `usertrap` |
| 7 | runtime | [kernel/trap.c:37](./kernel/trap.c:37) | `usertrap()` | checks `scause`; an `ecall` from user mode reaches [kernel/trap.c:67](./kernel/trap.c:67) | 
| 8 | runtime | [kernel/trap.c:61](./kernel/trap.c:61) | `p->trapframe->epc += 4;` | so `sret` resumes at the instruction *after* `ecall` |
| 9 | runtime | [kernel/syscall.c:139](./kernel/syscall.c:139) | `num = p->trapframe->a7;` | the generic dispatcher reads the number from the trapframe |
| 10 | runtime | [kernel/syscall.c:119](./kernel/syscall.c:119) → [kernel/syscall.c:143](./kernel/syscall.c:143) | `syscalls[num]()` | numbered dispatch-table entry `[SYS_getpid] sys_getpid`; the return value is stored in **`p->trapframe->a0`** |
| 11 | runtime | [kernel/syscall.c:93](./kernel/syscall.c:93) | `extern uint64 sys_getpid(void);` | handler prototype |
| 12 | runtime | [kernel/sysproc.c:19](./kernel/sysproc.c:19) | `sys_getpid()` | `return myproc()->pid;` — reads `struct proc.pid` |
| 13 | runtime | [kernel/trap.c:90](./kernel/trap.c:90) → [kernel/trampoline.S:101](./kernel/trampoline.S:101) → [kernel/trampoline.S:151](./kernel/trampoline.S:151) | `usertrapret()` / `userret` / `sret` | restores user registers from the trapframe; **a0 (x10)** carries the result back to the caller |

**Which file is generated, and which to edit.** `user/usys.S` is *generated* during the build from
`user/usys.pl`; the Makefile has a rule that runs `perl usys.pl > usys.S`. Editing `usys.S` is
pointless (it is rebuilt), so the edit goes in **`user/usys.pl`**.

**The number must match.** The stub hard-codes `li a7, SYS_getpid` (expanded from `kernel/syscall.h`)
and `syscall()` indexes `syscalls[]` with the *same* macro. If either side is out of step, the
dispatcher either finds a NULL slot or silently calls the wrong handler — and because the table is
designated-initialised, a missing entry is a NULL pointer, not a compile error.

**Why the trap path needs no per-syscall edit.** `uservec`/`usertrap`/`usertrapret` are *generic*:
they save and restore the whole trapframe and hand the number in `a7` to one shared dispatcher.
Adding a syscall therefore changes only data (a number, a table entry, a handler) — never the trap
machinery itself.

### 4.3 The contract

```c
int getproccount(void);
```
Returns *the number of process-table entries whose state is not `UNUSED` at the instant each entry is
inspected* — i.e. `USED`, `SLEEPING`, `RUNNABLE`, `RUNNING` and `ZOMBIE` all count.

### 4.4 Implementation checklist

| Action | Exact path : line, nearby symbol | Responsibility | Verified |
|---|---|---|---|
| inspect | [kernel/syscall.h:12](./kernel/syscall.h:12) `SYS_getpid` | numbering convention | ✔ |
| inspect | [kernel/syscall.c:108](./kernel/syscall.c:108) `syscalls[]` | dispatch table | ✔ |
| inspect | [kernel/proc.c:689](./kernel/proc.c:689) `procdump()` | existing proc[] scan to mirror | ✔ |
| **edit** | [user/user.h:22](./user/user.h:22) | declare `getproccount()` | ✔ |
| **edit** | [user/usys.pl:36](./user/usys.pl:36) | generate the user stub | ✔ |
| **edit** | [kernel/syscall.h:23](./kernel/syscall.h:23) | `#define SYS_getproccount 22` | ✔ |
| **edit** | [kernel/syscall.c:104](./kernel/syscall.c:104) + [:130](./kernel/syscall.c:130) | prototype + table entry | ✔ |
| **edit** | [kernel/sysproc.c:96](./kernel/sysproc.c:96) | syscall handler (registration side) | ✔ |
| **edit** | [kernel/proc.c:673](./kernel/proc.c:673) | `proccount()` (counting side) | ✔ |
| **edit** | [kernel/defs.h:109](./kernel/defs.h:109) | declare `proccount()` | ✔ |
| **create** | [user/proccount.c](./user/proccount.c) | the user program | ✔ |
| **edit** | [Makefile:146](./Makefile:146) | add `$U/_proccount` to `UPROGS` | ✔ |
| generated | `user/usys.S` | produced by `usys.pl` | don't touch |

The registration side (numbers, stubs, dispatch table, handler prototype) is deliberately separated
from the counting side (`proccount()` in `proc.c`, which owns `proc[]`).

### 4.5 The implementation

**Kernel counting** ([kernel/proc.c:673](./kernel/proc.c:673)) — mirrors `procdump()`'s scan:

```c
int
proccount(void)
{
  struct proc *p;
  int n = 0;

  for(p = proc; p < &proc[NPROC]; p++){
    if(p->state != UNUSED)
      n++;
  }
  return n;
}
```

**Handler** ([kernel/sysproc.c:96](./kernel/sysproc.c:96)):

```c
uint64
sys_getproccount(void)
{
  return proccount();
}
```

**User program** ([user/proccount.c](./user/proccount.c)):

```c
#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int
main(int argc, char *argv[])
{
  int n = getproccount();
  printf("proccount: %d process-table entries in use\n", n);
  printf("proccount: pid %d (this process is one of them)\n", getpid());
  exit(0);
}
```

### 4.6 Verify behaviour, not just compilation

```
$ proccount
proccount: 3 process-table entries in use
proccount: pid 3 (this process is one of them)

$                      (Ctrl-p pressed at the idle prompt)
1 sleep  init
2 sleep  sh
```

**Why `proccount` and `Ctrl-p` differ.**

* `proccount` runs as pid 3, so at the moment of the call it counts **three** entries: `init` (1,
  `SLEEPING`), `sh` (2, `SLEEPING`) and **`proccount` itself (3, `RUNNING`)**. It is counting a
  process that `Ctrl-p` cannot show, because `Ctrl-p` can only be pressed when the shell is at the
  prompt — that is, when `proccount` has already exited and its slot is `UNUSED`.
* More generally these are two *snapshots taken at different instants*, and the manual defines the
  result per-entry as it is inspected: processes can start, exit or change state between `proccount`'s
  first and last slot, so the number is a valid-but-instantaneous reading. `procdump()` has the same
  property (its own comment says "No lock to avoid wedging a stuck machine further").
* The value 3 is plausible and can be defended: after boot exactly two long-lived processes exist
  (`init`, `sh`), and the counting program adds itself.

---

## Checkpoint 5 — Communicate with two pipes

### 5.1 The abstraction in the source

| Item | Location |
|---|---|
| `pipe()` syscall side | [kernel/sysfile.c](./kernel/sysfile.c) `sys_pipe()` → `pipealloc()` |
| buffer, blocking, EOF, errors | [kernel/pipe.c:13](./kernel/pipe.c:13) `struct pipe`, [:23](./kernel/pipe.c:23) `pipealloc`, [:59](./kernel/pipe.c:59) `pipeclose`, [:77](./kernel/pipe.c:77) `pipewrite`, [:106](./kernel/pipe.c:106) `piperead` |
| descriptor duplication in `fork()` | [kernel/proc.c:280](./kernel/proc.c:280) `fork()` → `copyfile()` → `filedup()` |
| `filedup` / `fileclose` | [kernel/file.c:48](./kernel/file.c:48) and [:60](./kernel/file.c:60) (`f->ref++` / `f->ref--`) |

`pipe(int p[2])` makes one **unidirectional** byte stream: `p[0]` is the read descriptor,
`p[1]` the write descriptor ([kernel/pipe.c:38-45](./kernel/pipe.c:38)).

**Descriptors immediately after `fork()`** — every endpoint is duplicated, so *four* references exist
for two pipes:

```
                 p2c[0]  p2c[1]     c2p[0]  c2p[1]
  parent   :      keep    close      keep    close
  child    :      keep    close ~~~  close   keep
```

Crossed out = the unused endpoint in that process. The parent never reads `p2c` and never writes
`c2p`; the child is the opposite. Two pipes are needed because a single pipe is unidirectional — a
request **and** a reply therefore need one pipe in each direction.

### 5.2 Implementation

[user/two_pipes.c](./user/two_pipes.c) — added `_two_pipes` to `UPROGS` at [Makefile:147](./Makefile:147).

Order of operations (each process keeps only what it uses):

| | Parent | Child |
|---|---|---|
| 1 | `close(p2c[0]); close(c2p[1])` | `close(p2c[1]); close(c2p[0])` |
| 2 | `write(p2c[1], "ping", 4)` | `read(p2c[0], buf, 4)` → must be 4 bytes, else error |
| 3 | `close(p2c[1])` | `printf("%d: received %s\n", getpid(), buf)` |
| 4 | `read(c2p[0], buf, 4)` → must be 4 | `write(c2p[1], "pong", 4)` |
| 5 | `printf("%d: received %s\n", getpid(), buf)` | `close(p2c[0]); close(c2p[1]); exit(0)` |
| 6 | `close(c2p[0]); wait(0); exit(0)` | |

Error handling: `pipe()` and `fork()` failures print to fd 2 and `exit(1)`; every `read`/`write` is
checked and the short-write/short-read case is reported. Safe string handling: the buffer is
`char buf[5]`, exactly 4 bytes are requested, and `buf[n] = '\0'` terminates what was actually
received before `printf("%s")` — so the program never prints uninitialised stack bytes (the
supplied `pingpong.c` relies on luck here).

**Observed** — run three times in one boot:

```
$ two_pipes
4: received ping
3: received pong
$ two_pipes
6: received ping
5: received pong
$ two_pipes
8: received ping
7: received pong
```

PIDs vary; the ordering does not — the child always receives `ping` before the parent receives
`pong`, because the parent's `read(c2p[0])` cannot return until the child has both received the
request and replied, and the child's `read(p2c[0])` cannot return until the parent has written.

### 5.3 Investigating endpoint closure

**Prediction.** A `read()` on a pipe returns `0` (EOF) only when the pipe is empty **and no write
reference remains** — i.e. when `pi->writeopen == 0`, which `pipeclose()` sets when *the last* write
descriptor is closed. Holding an extra write-end descriptor in the parent therefore delays EOF: if
the child reads until EOF, it will block forever while the parent still holds `p2c[1]`.

**Source.** [kernel/pipe.c:59-75](./kernel/pipe.c:59) `pipeclose()` sets `writeopen = 0` and
`wakeup(&pi->nread)` only when the last reference to that end goes away; [kernel/pipe.c:106](./kernel/pipe.c:106)
`piperead()` loops `while(pi->nread == pi->nwrite && pi->writeopen)` and sleeps on `&pi->nread`.
`fork()` bumps the write-end reference via `filedup()` ([kernel/file.c:53](./kernel/file.c:53)), so the
parent and child each own one.

**Experiment A — all write references closed.** I temporarily changed the child to read in a loop
until `read()` returned 0, keeping the parent's `close(p2c[1])`:

```
4: child saw EOF after 4 bytes (read returned 0)
3: received pong
```

**Experiment B — parent keeps `p2c[1]` open.** Same child, parent's `close(p2c[1])` removed:

```
$ two_pipes
                    <- nothing; the program hangs
```

**Conclusion.** Both results match the prediction: with every write-end reference closed the child
observes EOF after the 4 real bytes; with one reference still held by the parent, `writeopen` stays 1,
the pipe never reports EOF, and the child blocks forever. The working implementation was restored
afterwards.

**Answer to the checkpoint's distinction:** closing *one* descriptor reference (one process's `close`)
just drops `f->ref` and leaves the *underlying pipe* open while other references remain; only closing
the **last** reference runs `fileclose()`'s cleanup and calls `pipeclose()`, which finally sets
`writeopen`/`readopen` to 0 and wakes the other side. That is also why an unused write descriptor left
open in the reader's own process is a classic "hang instead of EOF" bug.

---

## Final checkpoint — answer without AI

1. **Why is adding `user/program.c` alone insufficient?** The file is never compiled or linked and is
   never copied into `fs.img`, because `fs.img` is built from `$(UPROGS)`. The xv6 shell can only
   `exec` a name that exists as a file inside the image, so it reports `exec program failed`.
2. **What does the generated stub place in a7, and what enters the kernel?** `li a7, SYS_<name>` puts
   the syscall number in **a7** (for `getpid`, 11), then **`ecall`** raises the environment-call
   exception that traps into the kernel. Arguments go in a0–a5; the return value comes back in a0.
3. **Why can `getproccount()` differ from `Ctrl-p`?** They are snapshots taken at different instants —
   `Ctrl-p` can only be pressed at the idle shell, while `proccount` counts itself (pid 3, `RUNNING`)
   alongside `init` and `sh`. Neither takes a lock, so both are instantaneous readings of a changing table.
4. **Why does closing one post-`fork()` descriptor not close the pipe endpoint?** `fork()` duplicates
   the descriptor and `filedup()` increments the open-file reference count; `close()` only decrements
   it. The endpoint (and its `readopen`/`writeopen` flags) survives until the *last* reference is dropped.
5. **What distinguishes EOF from a write with no readers?** A read on a pipe whose write end is fully
   closed returns **0** once the buffer drains (EOF). A `write()` to a pipe whose read end is fully
   closed raises **SIGPIPE / kills the process** — xv6 returns **-1** from `pipewrite()` after
   `setkilled()` (see [kernel/pipe.c:84-87](./kernel/pipe.c:84)).

---

## Appendix A — Build blocker in `usertests.c`

`make qemu` could not build the image at all before any work:

```
user/usertests.c: In function 'fsfull':
user/usertests.c:2347:7: error: variable 'fsblocks' set but not used [-Werror=unused-but-set-variable=]
cc1: all warnings being treated as errors
```

`fsfull()` accumulates `fsblocks` and never reads it, and `CFLAGS` contains `-Wall -Werror`
([Makefile:65](./Makefile:65)). A newer host GCC (16.2.0 here) diagnoses this, so `fs.img` — and with
it `make qemu` — cannot be produced. Upstream MIT fixed it identically, so I applied their change at
[user/usertests.c:2391](./user/usertests.c:2391):

```diff
-  printf("fsfull test finished\n");
+  printf("fsfull test finished, %d blocks\n", fsblocks);
```

## Appendix B — Test results

| Run | Result |
|---|---|
| `pingpong` (baseline) | `exec pingpong failed` |
| `pingpong` (after UPROGS) | 5 alternating `received ping` / `received pong` |
| `forktest` | `fork test OK` |
| `usertests` (full suite, CPUS=3) | `ALL TESTS PASSED` (including `stacktest`, `sbrkbugs`, `diskfull`, `outofinodes`) |
| `zombie` + `Ctrl-p` | `4 zombie zombie` observed, then gone after the parent is reaped |
| `proccount` | `3 process-table entries in use`, pid 3 |
| `two_pipes` ×3 | child receives `ping`, parent receives `pong`; PIDs 3/4, 5/6, 7/8 |

## Appendix C — Files changed

| File | Change |
|---|---|
| [Makefile](./Makefile) | Added `$U/_pingpong`, `$U/_proccount`, `$U/_two_pipes` to `UPROGS` |
| [kernel/syscall.h](./kernel/syscall.h) | `SYS_getproccount 22` |
| [kernel/syscall.c](./kernel/syscall.c) | handler prototype + dispatch-table entry |
| [kernel/sysproc.c](./kernel/sysproc.c) | `sys_getproccount()` |
| [kernel/proc.c](./kernel/proc.c) | `proccount()` counting non-`UNUSED` entries |
| [kernel/defs.h](./kernel/defs.h) | `int proccount(void);` |
| [user/user.h](./user/user.h) | `int getproccount(void);` |
| [user/usys.pl](./user/usys.pl) | `entry("getproccount");` |
| [user/proccount.c](./user/proccount.c) | **new** user program |
| [user/two_pipes.c](./user/two_pipes.c) | **completed** two-pipe request/reply |
| [user/zombie.c](./user/zombie.c) | `sleep(5)` → `sleep(100)` (manual's temporary observation change) |
| [user/usertests.c](./user/usertests.c) | Pre-existing `-Werror` build blocker (Appendix A) |

## References

* SC2005 Lab 1 branch: <https://github.com/CPS-research-group/ntu-sc2005-xv6/tree/lab1>
* Russ Cox, Frans Kaashoek, Robert Morris, *xv6: a simple, Unix-like teaching operating system*,
  §§1.1–1.3, 2.2, 4.3, 9.3.
* MIT Missing Semester — *Course Overview + Introduction to the Shell*, *Command-line Environment*.
