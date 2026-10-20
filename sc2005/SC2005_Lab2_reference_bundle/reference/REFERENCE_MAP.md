# Reference map — original public `lab2` branch

These locations refer to the **original** `CPS-research-group/ntu-sc2005-xv6` `lab2` branch,
before applying this bundle's patches.

| Topic | Exact source reference | Why it matters |
|---|---|---|
| Global process table | `kernel/proc.c:11` — `struct proc proc[NPROC]` | Kernel-owned table that `scheduler()` and `procdump()` inspect |
| Kernel saved context | `kernel/proc.h:2-19` — `struct context` | Defines `ra`, `sp`, `s0`–`s11` layout used by `swtch()` |
| Trapframe | `kernel/proc.h:31-80` — `struct trapframe` | Stores user register state across trap/return |
| Process states | `kernel/proc.h:82` — `enum procstate` | `UNUSED`, `USED`, `SLEEPING`, `RUNNABLE`, `RUNNING`, `ZOMBIE` |
| Per-process fields | `kernel/proc.h:85-107` — `struct proc` | Contains state, PID, pagetable, trapframe, context, etc. |
| New kernel context | `kernel/proc.c:110-150` — `allocproc()` | Initializes a child's saved context; `ra=forkret`, `sp=kernel stack top` at 143-147 |
| Child becomes runnable | `kernel/proc.c:280-325` — `fork()` | Child's state becomes `RUNNABLE` at line 322 |
| Stock scheduler | `kernel/proc.c:445-483` — `scheduler()` | Scans `proc[]`, changes `RUNNABLE -> RUNNING`, then `swtch()` |
| Scheduler's `swtch` | `kernel/proc.c:467-473` | Saves CPU scheduler context and restores process context |
| Process-to-scheduler switch | `kernel/proc.c:493-510` — `sched()` | `swtch(&p->context, &mycpu()->context)` at line 508 |
| Yield transition | `kernel/proc.c:514-521` — `yield()` | Changes `RUNNING -> RUNNABLE` at line 518, then calls `sched()` |
| First child scheduling | `kernel/proc.c:523-535+` — `forkret()` | Comment explicitly says a fork child's first schedule switches to `forkret()` |
| User timer preemption | `kernel/trap.c:37-83` — `usertrap()` | Timer interrupt (`which_dev == 2`) calls `yield()` at 79-81 |
| Kernel timer preemption | `kernel/trap.c:135-157` — `kerneltrap()` | Timer interrupt can call `yield()` at 153-155 |
| Kernel assembly switch | `kernel/swtch.S:9-40` — `swtch` | Saves old `ra/sp/s0-s11`, restores new values, then `ret` |
| Unfinished user-thread state | `user/uthread.c:14-18` | Original `struct thread` TODO |
| User-thread selection | `user/uthread.c:34-64` — `thread_schedule()` | Chooses next `RUNNABLE` thread; original switch-call TODO at 60-61 |
| New user thread | `user/uthread.c:67-77` — `thread_create()` | Original new-context/stack TODO |
| Cooperative yield | `user/uthread.c:80-84` — `thread_yield()` | Marks current user thread `RUNNABLE` then schedules |
| Cooperative exit | `user/uthread.c:86-89` — `thread_exit()` | Marks current user thread `FREE` then schedules |
| Unfinished user switch | `user/uthread_switch.S:9-11` | Original assembly save/restore TODO |
| User-thread workload | `user/uthread_test.c:7-74` | Three functions start, yield repeatedly, count to 100, then exit |

## Two `swtch()` directions to memorize

### Process -> scheduler
`kernel/proc.c:sched()`

```text
swtch(&p->context, &mycpu()->context)
      save process      restore scheduler
```

### Scheduler -> process
`kernel/proc.c:scheduler()`

```text
swtch(&c->context, &p->context)
      save scheduler    restore process
```

## New process vs new user thread

A newly allocated **process** gets:

```text
p->context.ra = forkret
p->context.sp = top of kernel stack
```

A newly created **user thread** in the reference implementation gets the analogous idea:

```text
thread context ra = thread function
thread context sp = top of that thread's private user stack
```

The mechanism is conceptually similar, but one happens in the kernel's process scheduler and
the other happens entirely in a cooperative user-space library.
