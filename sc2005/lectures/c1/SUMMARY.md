# Introduction & Background — Summary (one page)

One deck, 46 slides, four questions: **what is an OS, what kinds exist, what does it control, and how
does a program reach it?**

> **S29 and S30 (storage hierarchy) are printed "This slide is not examinable."** Skip them.

---

## The 60-second version

1. An OS is **"a program that acts as an intermediary between a user and the computer hardware"**
   (S03). Its two goals are **user convenience** and **efficient hardware utilisation**, and the
   slide says outright that **"these two goals can be contradictory"** — a *better* allocation policy
   needs *more* information about user programs, and getting it costs overhead.
2. The system has **four components** — hardware, OS, application programs, users — and three names
   for the OS: **resource allocator**, **control program**, **kernel** (S05, S06). "Users" includes
   machines and other computers.
3. **Simple batch** keeps **one** job in memory and uses **automatic job sequencing** to reduce setup
   cost; when that job waits for I/O, **the CPU idles** (S10) — 20% utilisation in the standard
   example. **Multiprogramming** keeps **several** jobs resident and multiplexes the CPU (S11), which
   forces three OS features: **memory management, CPU scheduling, I/O device scheduling** (S12).
   **Time-sharing** adds on-line interaction: "when the OS finishes one command, it seeks the next
   command from the user" (S13).
4. **Desktop** favours convenience; **embedded/cyber-physical** systems are resource-constrained and
   favour efficiency; **real-time** means a **deadline** ("job must be completed within a deadline",
   airbag control); **handheld** (iOS/Android/HarmonyOS) must serve **both** goals. Real-time and
   handheld are both **subsets of embedded/CPS** (S15–S17).
5. **Multi-programming** = many programs, one CPU. **Multi-processing** = many CPUs/cores. A
   multiprocessor is **tightly coupled** (shared memory) and buys **throughput, economy, reliability**
   (S19).
6. I/O devices and the CPU run **concurrently**; each controller has a **local buffer** and signals
   completion with an **interrupt** (S23). An interrupt transfers control through the **interrupt
   vector**; **incoming interrupts are disabled** while one is handled; a **trap** is a CPU-generated
   interrupt (S24). Handling = **save registers + PC (a context switch), identify the type, dispatch
   the ISR** (S25).
7. **DMA** exists because one interrupt per byte is absurd: the OS sets up the counters once and the
   controller moves **blocks** to memory, giving **one interrupt per block** (S27).
8. **Dual-mode operation** separates **user mode** from **monitor/supervisor/system/kernel mode**;
   the **mode bit is 0 for monitor and 1 for user**; a trap or interrupt makes the **hardware** switch
   to monitor mode; **privileged instructions** run only there (S32, S33). **Root ≠ kernel mode**: root
   is an account, kernel mode is a hardware mode (S34).
9. **All I/O instructions are privileged** and must go through the OS (S35). Memory is protected by
   **base** (first legal address) and **limit** (the **size** of the range): legal iff
   `base ≤ addr < base + limit`, checked on every load/store, failure = **trap** = Linux
   **segmentation fault** (S36–S38).
10. A **system call** is "the interface between a user program and the OS" and **requires a switch to
    kernel mode** (S41). Layers: your program → **API** (`fopen`) → **system call** (`open`) → kernel
    (S42). The pair: **system call = CPU → device, trap, synchronous**; **interrupt = device → CPU,
    asynchronous** (S43, S44).

---

## The systems at a glance

| System | Jobs in memory | Goal that wins | Defining feature | Slide |
|---|---|---|---|---|
| Simple batch | **1** | efficiency (badly) | automatic job sequencing; CPU idles on I/O | S10 |
| Multiprogrammed | several | efficiency | CPU multiplexed; needs memory/CPU/I-O scheduling | S11, S12 |
| Time-sharing | several | responsiveness | **on-line** interaction; OS returns for the next command | S13 |
| Desktop | one user | **convenience** | many I/O devices ⇒ large driver code base | S14 |
| Embedded / cyber-physical | one | efficiency | monitored and controlled physical system; resource constrained | S15 |
| Real-time | one | **deadline** | fixed-time constraints; missing one = failure | S16 |
| Handheld | one | both | limited memory, slow CPU, small screen; clipping | S17 |
| Multiprocessor | many | throughput | tightly coupled; shared memory | S18, S19 |

---

## Definitions worth memorising verbatim

```
OS            = "a program that acts as an intermediary between a user and the computer hardware"
kernel        = "the one core program that is always ready to accept new commands from the users
                 as well as hardware (all else being application programs)"
trap          = "a CPU generated interrupt caused either by a software error or request"
interrupt     = device controller informs the CPU that it has finished its operation
DMA           = "only one interrupt is generated per block, rather than one interrupt per byte"
mode bit      = 0 -> monitor/supervisor/system/kernel    1 -> user
base register = holds the FIRST legal physical memory address
limit register= contains the SIZE of the legal range      (not the end address)
system call   = "the interface between a user program and the operating system"
```

---

## The two checks and the two diagrams

```
MEMORY PROTECTION (S36-S38)                    MODE SWITCHES
  legal <=> base <= addr < base + limit          entering: trap / interrupt, by HARDWARE
  check on every Load/Store(address)             leaving : privileged return-from-interrupt
  fail   -> trap -> segmentation fault
                                                 system call (S43)   interrupt (S44)
MODE BIT                                         1 program running   1 program running
  0 = monitor (kernel)                           TRAP! -> mode 0     INTERRUPT! -> mode 0
  1 = user                                       2 execute call      2 process interrupt
                                                 3 continue (mode 1) 3 continue (mode 1)
```

---

## Worked numbers worth remembering

**Memory protection (S37).** The figure is a multiprogrammed layout, and the notes read off:

```
base = 300 040        limit = 120 900
base + limit = 300 040 + 120 900 = 420 940
legal = [300 040 , 420 940)   ->  300 040 .. 420 939

300 039  trap         300 040  legal (first)      420 939  legal (last)
420 940  trap         0        trap
```

**Batch vs multiprogramming (derived from S10/S11).** A job with 20 ms of CPU and 80 ms of I/O:
batch gives `20 / 100 = 20 %` CPU utilisation; five such jobs resident gives `5 × 20 % = 100 %`. The
gain is **overlap**, not a faster CPU.

**Interrupts vs DMA (derived from S27's rule).**

```
1 TB = 2^40 B = 1 099 511 627 776 B
  one interrupt per byte     : 2^40 ~= 1.1 x 10^12 interrupts
  one interrupt per 4 KB     : 2^28 =    268 435 456 interrupts    -> 4096x fewer
```

---

## Ten things that decide exam marks

1. **Mode bit polarity: 0 = monitor, 1 = user.** The reverse of intuition, and a one-mark trap.
2. **The mode switch *into* the kernel is done by hardware**, not by the OS. Otherwise user code
   could decline to make the call.
3. **Root ≠ kernel mode.** "Jobs still execute in user mode, even when executed by a root/admin user."
4. **A trap is CPU-generated; an interrupt comes from a device.** S43 is even labelled `Trap!` — so
   a *system call* is a trap, not an interrupt.
5. **Limit is a size, not an end address**, and the upper bound is **exclusive**.
6. **`base + limit` is the first *illegal* address** — a failed check traps; the Linux name is
   segmentation fault.
7. **Multi-programming (programs) vs multi-processing (CPUs)** — independent concepts; multiprocessor
   is the tightly coupled, shared-memory case.
8. **DMA changes the interrupt rate from per byte to per block, and puts the data in memory** (not
   the device buffer).
9. **Real-time is about deadlines, not speed**; it is a subset of embedded/CPS, as are handhelds.
10. **S29 and S30 are not examinable** — but "interrupt-driven vs polling" (S24) and interrupt
    handling (S25) are.

---

## What is *not* in this series

* **Processes and context switching in detail** — S25 names the context switch and defers it: `c2`.
* **CPU scheduling algorithms** — S12 only says the OS must "choose among several jobs ready to
  run": `c3`.
* **Synchronisation and deadlock** — created by multiprogramming, but not listed on S12: `c5`, `c7`.
* **Paging and virtual memory** — base/limit protects one contiguous interval only; the scattered
  case is `c8`, `c9`.
* **Device drivers, disk I/O and file-system internals** — S27 stops at "OS sets up the memory
  blocks, counters" (`c12`), and `fopen`/`open` is used only as the system-call example (`c11`).
