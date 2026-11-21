# Introduction & Background — Things to Take Note Of

The "before the exam" file: what the deck stresses, what is easy to get wrong, and where the slides
themselves are unreliable. It contains no new material — the teaching is in
[STUDY_GUIDE.md](STUDY_GUIDE.md).

Because this lecture has **no recording**, every reference is a **slide number**: `S17` = slide 17 of
46. Speaker notes (transcript lines beginning `[NOTES]`) are cited as `S17 notes`.

---

## 1. What the deck repeatedly stresses

| Point | Where | Why it matters |
|---|---|---|
| **"These two goals can be contradictory"** — convenience vs efficiency | S03 | The organising idea of the whole chapter; every system type in §3 is a position on this axis |
| **Simple batch's CPU idles on I/O; multiprogramming fixes it by keeping several jobs resident** | S10, S11 notes | The reason multiprogramming exists, and the reason S12's three features exist |
| **"The key point is on scheduling the usage of shared resources: memory, CPU and devices"** | S12 notes | Names three later chapters; a direct pointer to the examinable material |
| **Interrupt handling has exactly three steps** (save state, identify type, dispatch ISR) | S25 | Repeated in the notes of S29 as a recap — an explicit "you should know this" |
| **A trap is a CPU-generated interrupt** | S24 | The single most testable sentence on the slide |
| **"All I/O instructions are privileged instructions"** | S35 | Justifies every mode switch in the chapter |
| **"No, they are not the same"** — kernel mode vs root | S34 | A whole slide devoted to one misconception |
| **The mode switch into monitor mode is hardware-controlled, "not OS"** | S33 notes | The argument for *why* protection cannot be implemented in software |
| **"The load instructions for the base and limit registers are privileged"** | S38 | Closes the obvious loophole in memory protection |
| **"Only one interrupt is generated per block, rather than one interrupt per byte"** | S27 | The definition of DMA; the size of the win is exactly the block size |
| **"The execution of a system call requires the switch from the user to the kernel mode"** | S41 | Why a system call costs more than a function call |
| **"If you are puzzled, fine … we will introduce them in later lectures"** | S01 notes, S40 notes | S40 is a map; do not over-revise the services list |

---

## 2. Exam traps

1. **Mode-bit polarity.** **0 = monitor/kernel, 1 = user.** Writing "1 = kernel" is the classic
   one-mark loss.
2. **Who performs the mode switch.** The **hardware** does it, on a trap or interrupt (S33). If the
   OS did it, it would have to decide *in user mode*, and the program could decline to ask.
3. **A system call is a trap, not an interrupt.** S43 labels the transition `Trap!` even though the
   call is voluntary. "Interrupt" is reserved for device→CPU events (S24, S44).
4. **Synchronous vs asynchronous.** Traps and system calls are synchronous (a known point in the
   program); device interrupts are asynchronous (whenever the device finishes).
5. **Root ≠ kernel mode.** Root's instructions still run in **user mode**; root gains *permission*,
   not *privilege level*, and reaches the kernel only through a system call or a kernel module.
6. **Limit register holds a size, not an end address.** Legal is `base ≤ a < base + limit`.
7. **The upper bound is exclusive.** With base 300 040 and limit 120 900, `420 940` is **illegal**;
   the last legal byte is `420 939`.
8. **`limit` copied from the slide is "size"** even though S37's notes describe the range loosely as
   "300 040 to 420 940".
9. **Multi-programming (programs) ≠ multi-processing (CPUs).** They are independent; you can have
   each without the other, and S11 (multiprogramming on one CPU) is a valid example of the first
   alone.
10. **Multi-processing ≠ multiprocessor hardware requirement.** The definitions are in the notes of
    S19, not on a slide of their own — quote them as "the notes define…".
11. **"Not very efficient" for batch means idle, not slow.** The hardware is fully used *while
    computing*; the waste is the I/O wait.
12. **Time-sharing vs multiprogramming.** The bodies of S11 and S13 are nearly identical. The one
    differentiator is S13's last sentence: the OS returns to the user for the next command.
13. **Real-time means deadline, not speed.** "Well-defined fixed-time constraints" is the phrase.
14. **Real-time and handheld are subsets of embedded/CPS**, not siblings of it (S15 lists them as
    domains of it; S16 and S17 notes confirm).
15. **DMA changes two things, not one.** The interrupt rate (per byte → per block) *and* where the
    data lands (device buffer → main memory).
16. **Interrupts are disabled during handling** — the slide's stated reason is "to prevent any loss of
    interrupts". Do not substitute your own explanation (nesting, simplicity) for the slide's.
17. **Polling is the alternative to interrupts**, not an error condition. "If the OS is not interrupt
    driven, it would be required to poll."
18. **A context switch happens on *every* interrupt**, not only on a process switch (S25 says so
    directly).
19. **Privileged instructions are a short list**, not "everything the kernel does": set the mode bit,
    do I/O, load base/limit, return from interrupt, disable interrupts.
20. **S29/S30 are not examinable.** Do not quote the storage hierarchy as if it were required; a
    one-sentence answer is the most you should ever need.

---

## 3. Known slips, typos and contradictions in the deck

These are problems in the slides or their notes — not in the extraction — unless marked otherwise.
Learn the correct version.

| # | Where | What the deck says | Correct version |
|---|---|---|---|
| 1 | **S43, S44** (also S02) | Footers read **`CE2005/CZ2005 Operating Systems`** on S43 and S44, but **`SC2005 Operating Systems`** on S02 | **Same course.** SC2005 is the current code; CE2005/CZ2005 are the older/parallel codes. The content is SC2005 content |
| 2 | **S11 vs S13** | S11 is titled "Multiprogrammed (Time-Sharing) Systems" and S13 is titled "Time-Sharing Systems"; **their body text is almost word-for-word the same** | Treat S11 as multiprogramming and S13 as time-sharing; use S13's final sentence (on-line communication, next command) to separate them |
| 3 | **S29 vs S30** | Two slides with the same topic (storage hierarchy), the second containing only a diagram | S29 is the bullet version, S30 the figure. **Both are marked "This slide is not examinable."** |
| 4 | **S29 notes vs S29 slide** | The slide is marked not examinable, yet its notes open with a recap of the *previous* lecture — multiprogramming, multiprocessing, the interrupt-handling steps, interrupt-driven I/O vs DMA | The recap is **examinable** (it summarises S11, S19, S25, S27); only the storage-hierarchy content is exempt |
| 5 | **S38 notes** | "we first check whether it is **larger than the base register**. If failed, a trap is issued" | The test is `address >= base`. As worded, an address **equal** to base would fail (it is legal). Then `address < base + limit` |
| 6 | **S37 notes** | "the memory range for job 2 is from 300040 to **420940**" | The upper end is **exclusive**; the last legal byte is **420 939** |
| 7 | **S37 notes** | "Btw, is it a simple batch system? No. it is multiprogrammed system." | Not a slip — a deliberate prompt, because base/limit only makes sense with several jobs resident |
| 8 | **S46 notes** | Identical to S45's notes ("Those are advanced readings, if you want to know more beyond the text book") | Copy-paste error: S46 is the **future operating systems** slide (unikernels, seL4), not a readings slide |
| 9 | **S16** | Heading "Example real-time OSes" but no list of OSes is present in the slide text | The notes point to the **week-7 e-learning lecture**; see also [`../c6a`](../c6a) |
| 10 | **S42** | `Int fd;` — capital **I** | `int` |
| 11 | **S11** | "System is highly interactive; **t** supports multiple online users" — stray character from the layout | "systems" |
| 12 | **S02** | "Operating systems (**OS-s**)" | OSs |
| 13 | **S24** | "Unhandled exceptions in user program" is a bare fragment under the trap definition | An **example** of the "software error" that makes a trap |
| 14 | **S09** | "A Short Review on Computers" — the slide announces a video and carries no content | Nothing to learn from this slide; the history it refers to is background only |
| 15 | **S18, S28, S37, S40** | Figure-only slides (dual-core design, modern computer, memory layout, OS services) | The figure is the content; the notes carry the words. Do not treat them as empty slides |
| 16 | **Extraction artefact** | Many `[NOTES]` blocks stop mid-sentence (S01, S03, S05, S06, S11, S33, S17…) | This is truncation in the extracted text, not on the slide. Where a summary sentence ends prematurely, the meaning is usually recoverable from the next clause |

---

## 4. Coverage map (S01–S46)

| Slide | Topic |
|---|---|
| S01 | **Roadmap** (act I divider): the four topics |
| S02 | **Why learn OSes**: hide complexity; abstractions, policies, mechanisms; two audiences |
| S03 | **Definition**; two goals; the contradiction; "smart allocation may require lot of information" |
| S04 | **Computer system components** (figure): hardware/OS/apps/users |
| S05 | The same four components with definitions |
| S06 | **Three definitions**: resource allocator, control program, kernel |
| S07 | **Roadmap** (act II divider): types of computing systems |
| S08 | The seven types, in historical order |
| S09 | "A Short Review on Computers" — video slide, no content |
| S10 | **Simple batch**: batching, automatic job sequencing, one job in memory, CPU idles |
| S11 | **Multiprogramming**: several jobs resident, CPU multiplexed, swapping, interactive |
| S12 | **Three features needed**: memory management, CPU scheduling, I/O device scheduling |
| S13 | **Time-sharing**: multiplexed CPU + on-line communication + next command |
| S14 | **Desktop**: single user, many devices, responsiveness, Windows/MacOS/UNIX/Linux |
| S15 | **Embedded & cyber-physical**: monitored/controlled, resource constrained, domains |
| S16 | **Real-time**: fixed-time constraints, deadline, airbag control |
| S17 | **Handheld**: limited memory, slow processors, small screens, iOS/Android/HarmonyOS |
| S18 | **A dual-core CPU design** (figure): shared memory, per-core registers and caches |
| S19 | **Multiprocessor systems**: tightly coupled, throughput/economy/reliability |
| S20 | **Roadmap** (act III divider): architecture — operation, hierarchy, protection |
| S21 | The three architecture sub-topics |
| S22 | **Computer-system operation** (figure): CPU, controllers, buffers, bus, interrupt |
| S23 | The five facts: concurrency, one controller per device type, local buffers, transfer, interrupt |
| S24 | **Interrupts**: vector, disabling, trap definition, interrupt-driven vs polling |
| S25 | **Interrupt handling**: save state (context switch), identify type, dispatch from the vector |
| S26 | **Interrupt-driven I/O timeline**: Job 1 / Job 2 / OS; device idle vs transferring |
| S27 | **DMA**: high-speed devices, OS sets up counters, block transfer, one interrupt per block |
| S28 | **How a modern computer works** (figure): CPU, memory, device; where the data lands |
| S29 | **Storage hierarchy** + **caching** — **"not examinable"** |
| S30 | **Storage/memory hierarchy** diagram — **"not examinable"** |
| S31 | **Hardware protection**: dual mode, I/O protection, memory protection |
| S32 | **Dual-mode operation**: user mode vs monitor/supervisor/system/kernel mode |
| S33 | **Mode bit** (0 = monitor, 1 = user), hardware switch, privileged instructions |
| S34 | **Kernel mode vs root/admin**: not the same; kernel module is the indirect route |
| S35 | **I/O protection**: two cases, all I/O instructions privileged, trap on bypass |
| S36 | **Memory protection**: base and limit registers; protect at least the vector and ISRs |
| S37 | **Worked example**: base 300 040, limit 120 900 → 420 940 |
| S38 | **The check**: privileged loads, trap on failure, `Load/Store(address)`, segmentation fault |
| S39 | **Roadmap** (act IV divider): OS services |
| S40 | **A view of OS services** (figure): user interfaces, system calls, services |
| S41 | **System calls**: the interface, assembly instructions, requires a mode switch |
| S42 | **API → system call → OS**: `fopen` in libc calls `open` |
| S43 | **System call processing** (CPU→device): ❶ run ❷ TRAP ❸ execute ❹ continue |
| S44 | **Interrupt processing** (device→CPU): ❶ run ❷ handle ❸ continue |
| S45 | **Advanced readings**: iOS, Android, "History of Operating Systems" |
| S46 | **Future OSes**: unikernel, formally verified kernel (seL4) |

---

## 5. Memory hooks that actually help

* **0 = mOnitor** (both have an *o*); **1 = User** (*one* for the user). The one place where a
  mnemonic is worth the effort.
* **Base = beginning, Limit = length.** Two words that start differently from what they mean if you
  read too fast.
* **A trap is the program tripping itself.** An interrupt is the doorbell ringing.
* **Root is a *who*, kernel is a *where*.**
* **`base + limit` is the first address you may *not* touch** — the fence post, not the last plank.
* **DMA = "Don't Move Anyway"** — the CPU does not move the bytes; it sets the counters and waits
  for one interrupt per block.
* **Batch = one job in the room; multi-programming = a queue; multi-processing = more rooms.**
* **The interrupt vector is the phone book**: the type is the name, the vector page is the number.
* **The OS is interrupt-driven** — it reacts, it does not watch.
* **System call = the program asks; interrupt = the hardware tells.**

---

## 6. Quick self-check before the exam

- [ ] Can you state S03's definition and the two goals, and explain *why* they can contradict?
- [ ] Can you give the three definitions of an OS from S06, and keep kernel / kernel mode / root
      apart?
- [ ] Can you explain why batch wastes the CPU and name the three features multiprogramming needs?
- [ ] Can you give the one sentence that separates time-sharing from multiprogramming?
- [ ] Can you place real-time, handheld and embedded/CPS in a containment diagram?
- [ ] Can you state the distinction between multi-programming and multi-processing without hesitating?
- [ ] Can you list the three advantages of multiprocessors with the mechanism behind each?
- [ ] Can you give the three steps of interrupt handling, in order, and say what each needs?
- [ ] Can you say what problem DMA solves and give the improvement factor in general terms?
- [ ] Can you state the mode-bit values, what forces the transition into monitor mode, and what a
      privileged instruction is?
- [ ] Can you answer "can root run code in kernel mode?" in one sentence with the indirect route?
- [ ] Can you write the base/limit test, and evaluate an address at exactly `base` and exactly
      `base + limit`?
- [ ] Can you reproduce S37's arithmetic (`300 040 + 120 900 = 420 940`) and say which end is
      exclusive?
- [ ] Can you draw S43 and S44 from memory, and label one `Trap!` and the other `Interrupt!`?
- [ ] Can you explain why the mode switch happens at all, in terms of privileged I/O instructions?
- [ ] Can you say which two slides are not examinable, and what they cover?
