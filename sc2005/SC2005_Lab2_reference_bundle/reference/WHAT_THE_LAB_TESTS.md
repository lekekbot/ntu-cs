# What Lab 2 is actually testing

## The one-sentence version

**Can you explain how xv6 stops one execution context, saves enough state to resume it later,
chooses something else to run, and restores that other context?**

## Part 1 — What is a process?

Mental picture:

```text
struct proc
├── state       -> RUNNABLE / RUNNING / ...
├── pid
├── pagetable   -> user address space
├── trapframe   -> saved USER registers for trap/return
└── context     -> saved KERNEL registers for kernel context switching
```

The three state changes to know:

```text
fork():       child        -> RUNNABLE
scheduler(): RUNNABLE      -> RUNNING
yield():     RUNNING       -> RUNNABLE
```

## Part 2 — How does xv6 preempt and switch processes?

Core flow:

```text
Process A in user mode
        |
        | timer interrupt
        v
usertrap()
        |
        v
yield()
  A: RUNNING -> RUNNABLE
        |
        v
sched()
        |
        | swtch(&A.context, &CPU.scheduler_context)
        v
scheduler()
        |
        | choose a RUNNABLE process
        | state -> RUNNING
        v
swtch(&CPU.scheduler_context, &B.context)
        |
        v
Process B resumes
```

The strict-priority modification changes **selection policy**, not the context-switch mechanism:

```text
Is any even PID RUNNABLE?
   YES -> choose even
   NO  -> odd may be chosen
```

With one CPU, if an even process stays runnable forever, an odd process can remain runnable
forever without being selected: starvation.

## Part 3 — How can one process contain several user threads?

```text
xv6 kernel
   |
   | schedules ONE xv6 process
   v
+--------------------------------------+
| one user address space               |
|                                      |
| Thread A     Thread B     Thread C    |
| stack A      stack B      stack C     |
| context A    context B    context C   |
+--------------------------------------+
               ^
               |
      user thread library chooses
```

The kernel does **not** know about these cooperative user threads.

A user-thread switch is:

```text
Thread A
   |
thread_yield()
   |
thread_schedule()
   |
thread_switch(A.context, B.context)
   |                |
   | save A         | restore B
   v                v
              ret -> B's saved ra
```

## Why `ra` and `sp` matter

- `sp` tells the CPU which stack belongs to the resumed execution.
- `ra` tells `ret` where execution should continue.
- `s0`–`s11` are callee-saved registers, so the called switching routine must preserve them.

## Why a brand-new thread is special

A suspended thread has previously run, so it already has a saved `ra` and `sp`.

A brand-new thread has no old context. `thread_create()` must manufacture an initial context:

```text
ra -> thread's function
sp -> top of thread's own aligned stack
```

Then the first restore ends with `ret`, which jumps into that function.

## The most important distinction for the quiz

```text
KERNEL SCHEDULER
process A <----> process B
uses kernel process contexts
can be driven by timer preemption

USER THREAD LIBRARY
thread A <----> thread B
inside ONE process / ONE address space
switches cooperatively on thread_yield()/thread_exit()
```
