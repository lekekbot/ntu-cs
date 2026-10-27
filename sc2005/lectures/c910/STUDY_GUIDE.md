# SC2005 — Virtual Memory: Study Guide

Companion to the five recordings in this folder. Timestamps refer to the transcript of the part
named, e.g. **`02 @ 14:30`** means part 02, 14 min 30 s.

Transcripts: [01](transcripts/01-virtual-memory-1-motivation-swapping-demand-paging.txt) ·
[02](transcripts/02-virtual-memory-2-page-replacement-algorithms.txt) ·
[03](transcripts/03-virtual-memory-3-beladys-anomaly-supplement.txt) ·
[04](transcripts/04-virtual-memory-4-frame-allocation-and-replacement-scope.txt) ·
[05](transcripts/05-virtual-memory-5-thrashing-and-working-set.txt)

---

## 0. Where this fits

In [memory organization](../c89) the logical address space of a process had to **fit in physical
memory**. Virtual memory removes that restriction:

```
        before:   logical address space  <=  physical memory
        after:    logical address space  can be much larger
                  only the pages needed *now* are in memory
                  everything else lives in the backing store (disk)
```

Everything in these five lectures follows from one chain of consequences:

```
logical space > physical memory
        => not all pages can be resident
        => a reference may miss  ("page fault")
        => the OS must fetch the page from disk  (slow!)
        => WHICH page do we evict if memory is full?   -> page replacement (part 02)
        => DOES eviction ever make things worse?       -> Belady's anomaly (part 03)
        => HOW MANY frames does each process get?      -> frame allocation  (part 04)
        => WHAT IF everyone has too few frames?        -> thrashing         (part 05)
```

| Part | Topic | Transcript |
|---|---|---|
| 01 | Motivation, swapping, **demand paging**, page-fault handling, EAT | [01](transcripts/01-virtual-memory-1-motivation-swapping-demand-paging.txt) |
| 02 | **Page replacement**: FIFO, optimal, LRU, second chance / clock | [02](transcripts/02-virtual-memory-2-page-replacement-algorithms.txt) |
| 03 | **Belady's anomaly** and the inclusion property (supplementary) | [03](transcripts/03-virtual-memory-3-beladys-anomaly-supplement.txt) |
| 04 | **Frame allocation** and **replacement scope** | [04](transcripts/04-virtual-memory-4-frame-allocation-and-replacement-scope.txt) |
| 05 | **Thrashing**, locality, working-set model, page-fault frequency | [05](transcripts/05-virtual-memory-5-thrashing-and-working-set.txt) |

---

## 1. Motivation and swapping (part 01, 00:00 – 07:28)

### 1.1 The problem

Without virtual memory:

* the whole process image must be loaded before it can run,
* so **program size is limited by installed physical memory**, and
* the degree of multiprogramming is limited by how many images fit.

**Goal of virtual memory: decouple the logical address space from physical memory**, so a program
can have a logical address space much larger than RAM.

### 1.2 Swapping

> **Swapping** = temporarily copy an entire **process image** out of memory to the backing store.

* **Backing store** = a fast disk, large enough to hold the images of *all* processes.
* **Swap out**: memory → backing store; the memory becomes free for other processes.
* **Swap in**: backing store → memory (possibly at a **different** physical location).
* Benefit: more processes can be resident → higher degree of multiprogramming.
* Cost: huge — the whole image is copied over a disk, and the process may have to be swapped in
  before it can be given the CPU, so **context-switch time increases significantly**.

Consequences:

1. Because a swapped-in image may land anywhere, the logical→physical translation must be
   **dynamic** (execution-time binding — the same requirement established in part 01 of `c89`).
2. We need a policy for **which process to swap out / in**. That is the **mid-term scheduler** (the
   swapper).

### 1.3 The three schedulers (01 @ 05:13)

| Scheduler | Also called | Decides |
|---|---|---|
| **Long-term** | job scheduler | which jobs from the job pool are admitted into memory |
| **Mid-term** | **swapper** | which processes are swapped out and swapped in |
| **Short-term** | CPU scheduler | which ready process gets the CPU next |

With swapping, the ready queue may contain processes whose image is **on disk**, so dispatching one
of them requires a swap-in first.

### 1.4 Why virtual memory works at all (01 @ 08:21)

A large program has many pages, but during any short period of execution it is confined to
**one routine** and a **few data structures** — the *locality* of the program (formalised in part 05).

So: **load only the pages needed now.** The rest stay on disk. The backing store becomes a *virtual
extension* of physical memory.

Consequences:

* a process needs far fewer frames than it has pages;
* more processes fit → higher degree of multiprogramming → better CPU utilisation …
* … **but only up to a point** — beyond it you get thrashing (part 05).

### 1.5 Swapping vs paging (01 @ 13:12)

| | Unit moved | When |
|---|---|---|
| **Swapping** | the **whole process image** | mid-term scheduler decision |
| **Paging in/out** | a **single page** | on demand, when a page is referenced |

Virtual memory uses **paging**, not whole-process swapping.

---

## 2. Demand paging (part 01, 13:12 → end)

> **Demand paging** = a page is loaded into memory only when it is actually referenced.

### 2.1 The valid–invalid bit

Each **page-table entry** gets a **valid–invalid bit**:

```
   page table entry
   +---------+-------------------------------+
   | V / I   | frame number  OR  disk address|
   +---------+-------------------------------+
       V  ->  page is in memory;  field = frame number
       I  ->  page is NOT in memory; field = its location in the backing store
```

* Initially **every** entry is `I` (nothing loaded) — this is **pure demand paging**.
* The OS assumes the **entire process image is always on the backing store**, so a missing page can
  always be found there.

### 2.2 The page-fault handling procedure (01 @ 20:20)

```
CPU references page 6  ->  PTE[6].valid == I
        |
        v
1. trap to the OS                       (context switch: user -> kernel)
2. OS locates page 6 in the backing store
3. OS finds a FREE frame
        |                       (if none free -> must evict a victim: part 02)
        v
4. read (page in) the page from disk into that frame      <-- the expensive step
5. update the PTE: valid = V, frame number = that frame
6. return control to the process                        (context switch: kernel -> user)
7. RESTART the faulting instruction  -> translation now succeeds
```

The lecture's example: pages 0, 2 and 5 are resident; a reference to page 6 faults.

### 2.3 Effective access time (01 @ 23:12)

Let **p** = probability that a memory reference causes a page fault (`0 ≤ p ≤ 1`).

```
EAT = (1 - p) × memory access time  +  p × page fault time
```

Since *page fault time ≫ memory access time*, even a small `p` dominates the average. The two big
components of page-fault time:

1. **context switch** overhead (trap in, return out),
2. **disk I/O** (locate + read the page, and possibly write a victim page out).

> Worked example. Let memory access = 200 ns and page-fault service = 8 ms. If p = 1/1000:
> `EAT = 0.999 × 200 ns + 0.001 × 8,000,000 ns ≈ 199.8 + 8000 ≈ 8.2 µs` — about **40× slower** than
> 200 ns. This is why the fault rate must stay tiny.

---

## 3. Page replacement (part 02)

### 3.1 What happens when memory is full (02 @ 00:00)

A fault occurs and there is **no free frame**. The OS must pick a **victim page**, evict it, and use
its frame:

```
1. choose a victim page            (page replacement algorithm)
2. page OUT the victim to disk     (only if it is dirty)
3. update the victim's PTE         valid = I
4. page IN the missing page
5. update the missing page's PTE   valid = V, frame = the freed frame
6. restart the instruction
```

That is **two disk I/Os** (one out, one in) instead of one — page-fault time increases further.

### 3.2 The dirty (modified) bit (02 @ 03:46)

A **dirty page** has been **modified since it was loaded**. The hardware/OS keeps a **modified
(dirty) bit** per page.

* **Clean** page: the disk copy is still identical → **no need to write it back**; just overwrite it.
* **Dirty** page: must be written out before the frame is reused.

So: **only dirty victims are paged out.**

### 3.3 How algorithms are compared (02 @ 06:17)

* Objective: **minimise the number of page faults**.
* Method: run the algorithm over a **page reference string** and count faults.
* The lecture uses the same string throughout:

```
reference string:  1 2 3 4 1 2 5 1 2 3 4 5
frames:            4
```

### 3.4 FIFO (02 @ 07:05)

Replace the **oldest** page (the one that has been in memory longest). Keep a FIFO queue.

Worked trace, 4 frames (`P` = page fault):

| ref | 1 | 2 | 3 | 4 | 1 | 2 | 5 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **F1** | 1 | 1 | 1 | 1 | 1 | 1 | **5** | 5 | 5 | 5 | **4** | 4 |
| **F2** |   | 2 | 2 | 2 | 2 | 2 | 2 | **1** | 1 | 1 | 1 | **5** |
| **F3** |   |   | 3 | 3 | 3 | 3 | 3 | 3 | **2** | 2 | 2 | 2 |
| **F4** |   |   |   | 4 | 4 | 4 | 4 | 4 | 4 | **3** | 3 | 3 |
| **fault?** | P | P | P | P | – | – | P | P | P | P | P | P |

**Total: 10 page faults.**

FIFO is trivial to implement but ignores how often/often-recently a page is used — a frequently used
page can still be the oldest.

### 3.5 Optimal (OPT / MIN) (02 @ 09:35)

Replace the page that **will not be used for the longest time in the future**.

* Same trace, 4 frames → **6 page faults** (the best possible).
* Needs knowledge of the **future reference string** → **not implementable** in a real system.
* Why keep it? It is the **benchmark**: no real algorithm can beat it, so it gives a lower bound to
  compare against.
* Tie-break when several pages are never used again: the lecture uses **FIFO** to break the tie.

### 3.6 LRU (02 @ 14:29)

Replace the page that **has not been used for the longest time in the past** — the exact mirror of
OPT, using history instead of the future.

* Same trace, 4 frames → **8 page faults** (better than FIFO, worse than OPT).
* Needs a way to order pages by last use. The lecture notes that the standard implementations
  (e.g. timestamp/counter registers, or a stack of page numbers) all cost **hardware support** and
  add overhead on every reference.
* In practice it is **approximated** (next section).

### 3.7 The reference bit and second-chance / clock (02 @ 19:24)

**Reference bit**: one bit per page, cleared when the page is loaded, **set by hardware whenever the
page is read or written**.

A page with `R = 0` has not been used since the bit was last cleared → a good victim. But many pages
may have `R = 0`, so a rule is needed.

**Second chance = FIFO + reference bit.** Take the oldest page as the candidate:

* `R = 1` → give it a **second chance**: clear `R`, move it to the back, continue;
* `R = 0` → **evict it**.

**Clock implementation**: keep the pages in a **circular list** in FIFO order with a **clock hand**
pointing at the oldest page. On a fault, advance the hand: clear `R` and skip pages with `R = 1`;
evict the first page with `R = 0`; then advance.

* Same trace → **8 page faults**, the same as LRU — that is why it is called an **LRU approximation**.
* **Best case**: behaves like LRU (reference bits spread out).
* **Worst case**: behaves like FIFO (all bits set → every page gets a second chance and the hand
  goes all the way round).

### 3.8 Comparison

| Algorithm | Victim chosen by | Faults (4 frames, string above) | Implementable? |
|---|---|---|---|
| **FIFO** | oldest arrival | **10** | yes, very cheap |
| **OPT** | farthest future use | **6** (optimal) | no — needs the future |
| **LRU** | oldest last use | **8** | yes, but needs hardware |
| **Second chance / clock** | oldest with `R = 0` | **8** | yes, cheap approximation of LRU |

---

## 4. Belady's anomaly (part 03)

> **Belady's anomaly**: for some algorithms, giving a process **more frames increases** the number of
> page faults.

The lecture's example, same reference string, **FIFO**:

| Frames | Page faults |
|---|---|
| 3 | **9** |
| 4 | **10** |

More memory made it worse.

### 4.1 The inclusion property

> **Inclusion property**: the set of pages in memory with **n** frames is a **subset** of the set in
> memory with **n+1** frames.

If an algorithm satisfies the inclusion property, it **cannot** suffer Belady's anomaly: adding a
frame can only add pages, never remove one that was already resident.

| Algorithm | Inclusion property | Belady's anomaly |
|---|---|---|
| **FIFO** | ✗ | **yes** |
| **OPT** | ✓ (keeps the next n pages to be referenced) | no |
| **LRU** | ✓ (keeps the n most recently referenced pages) | no |
| **Clock / second chance** | not guaranteed | can behave like FIFO in the worst case |

---

## 5. Frame allocation and replacement scope (part 04)

Two independent questions:

1. **How many frames** does each process get? → allocation policy
2. **Whose pages** may be evicted on a fault? → replacement scope

### 5.1 Allocation policy (04 @ 00:58)

| Policy | Meaning | Sub-policies |
|---|---|---|
| **Fixed** | the number of frames per process **never changes** | **equal** allocation (same for all) or **proportional** allocation (proportional to the size of the logical address space) |
| **Variable** | the number of frames per process **changes over time** | adjusted according to the process's fault behaviour |

Trade-off at the heart of part 05: giving each process **fewer** frames lets you run **more**
processes, but raises each process's fault rate. Past a point, extra processes only add faults.

### 5.2 Replacement scope (04 @ 03:55)

| Scope | Victim may come from | Consequence |
|---|---|---|
| **Local** | only the faulting process's **own** frames | frame count stays constant; but a process may **hoard** frames it is not using, hindering others |
| **Global** | **any** frame in physical memory | a process can take a frame from another; its performance now depends on **other processes** |

Worked example from the lecture: processes A, B, C; A references page 6, which is not resident; LRU
picks the earliest last-access time.

* **Local** → evict A's least-recently-used page (A5). A keeps the same number of frames.
* **Global** → evict the globally least-recently-used page (B3). **A gains a frame, B loses one.**

### 5.3 Which combinations make sense (04 @ 11:26)

| Combination | Possible? | Why |
|---|---|---|
| Fixed + local | **yes** (the usual pairing) | replacing only own pages keeps the count constant |
| Fixed + global | ✗ | taking another process's frame changes both counts |
| Variable + global | yes | frame counts drift as processes steal from each other |
| Variable + local | yes | start with a quota, adjust it from the observed fault rate |

**Variable + local in practice**: give the process an initial quota; on a fault, replace only its own
pages; **monitor its page-fault rate** — too high → give it more frames, consistently very low →
take frames away. The count changes over time, but each process only evicts its own pages.

---

## 6. Thrashing (part 05)

### 6.1 What it is (05 @ 00:00)

> **Thrashing**: a process (or the whole system) spends most of its time paging in and out instead of
> executing.

The failure spiral:

```
too few frames for a process
      -> it faults on almost every reference
      -> it evicts pages that other processes need
      -> those processes fault more
      -> more paging, less execution
      -> CPU utilisation collapses
```

The counter-intuitive part: **increasing the degree of multiprogramming makes it worse**, because
more processes compete for the same frames.

### 6.2 The CPU-utilisation curve (05 @ 02:01)

```
CPU
utilisation
    |            ****
    |         ***    ***
    |       **          **
    |     **              **
    |   **                  **
    | **                      **
    +----------------------------> degree of multiprogramming
      ^                        ^
      |                        |
  few processes            THRASHING
  (CPU idle waiting         (collapse)
   for I/O)
```

* Left of the knee: more processes → fewer idle periods → utilisation rises.
* At the knee: the average number of frames per process becomes inadequate.
* Right of the knee: fault rate explodes and utilisation falls.

### 6.3 Locality of reference (05 @ 04:05)

Thrashing is avoidable because programs do not reference memory uniformly.

| Type | Meaning | Examples from the lecture |
|---|---|---|
| **Temporal locality** | a location referenced recently is likely to be referenced again soon | sequential instruction execution; loops repeating a small block of instructions |
| **Spatial locality** | nearby locations are likely to be referenced together | array elements stored contiguously; a procedure's code placed contiguously |

Therefore, over a short interval a process needs only **a few pages** — its **locality**.

### 6.4 Working-set model (05 @ 10:53)

* **Working-set window Δ** = a fixed number of **most recent page references**.
* **Working set WS(t)** = the set of distinct pages referenced in the last Δ references.

Example from the slide, Δ = 10:

```
page references: ... 2 6 1 5 7 7 7 7 5 1 6 2 3 4 1 2 3 4 4 4 3 4 3 4 4 4 1 3 2 3 4 4 4 3 4 4 4 ...
                       <--- Δ --->                    <--- Δ --->
                            t1                              t2

WS(t1) = {1, 2, 5, 6, 7}
WS(t2) = {3, 4}
```

Sizing the system:

```
WSS_i = |WS_i|                 working-set size of process i
D     = Σ WSS_i                total demand (frames needed by all resident processes)
m     = total frames available

if D > m  ->  the system is thrashing
          ->  the OS must SUSPEND (swap out) some processes to reduce D
```

**Problem**: the optimal Δ is unknown. Too small → misses part of the locality; too large → spans
several localities and overestimates the need.

### 6.5 Page-fault-frequency (PFF) scheme (05 @ 14:30)

Instead of measuring locality, measure the **symptom** directly.

1. Define an **acceptable page-fault rate** with a **lower** and an **upper** bound.
2. Measure each process's actual page-fault rate.
3. **Rate > upper bound** → the process needs more frames → give it a frame from the free list.
4. **Rate < lower bound** → it has too many frames → take one away and return it to the free list.
5. **Free list empty and a process needs a frame** → **swap out** a process.

This adapts the allocation continuously and is simpler than tracking a working set.

### 6.6 Summary of part 05

* Thrashing = too many processes, too few frames each; time goes to paging, not execution.
* Cures: **working-set model** (keep D ≤ m) or **PFF** (keep each process's fault rate in bounds);
  both may end in **swapping a process out**.
* A **locality** is a set of pages actively used together; the process moves from one locality to
  another as it executes, so its **working set changes over time**.

---

## 7. Putting it together

### 7.1 The full picture

```
                     process references a logical address
                                   |
                                   v
                         page in memory?  (valid bit V)
                          /                 \
                        yes                  no  -> PAGE FAULT
                         |                        |
                    translate & access            v
                                          free frame available?
                                             /          \
                                           yes           no
                                            |             |
                                            |      choose victim (algorithm)
                                            |      dirty? -> write out
                                            |      update victim PTE
                                            v             v
                                       read page in, update PTE, restart instruction
```

### 7.2 Algorithm/decision summary

| Decision | Options | Part |
|---|---|---|
| How much to move | whole image (swapping) vs one page (demand paging) | 01 |
| Detect residency | valid–invalid bit | 01 |
| Choose a victim | FIFO / OPT / LRU / second chance | 02 |
| Avoid needless writes | dirty (modified) bit | 02 |
| Compare algorithms | page reference string, fault count | 02 |
| Guarantee no anomaly | inclusion property | 03 |
| Frames per process | fixed (equal/proportional) vs variable | 04 |
| Whose page to evict | local vs global | 04 |
| Prevent collapse | working set / PFF / suspend processes | 05 |

---

## 8. Formula sheet and practice

### 8.1 Formulas

```
EAT (demand paging)   = (1 - p) × memory access time + p × page fault time

working set           WS(t) = distinct pages in the last Δ references
working-set size      WSS_i = |WS_i|
total demand          D = Σ WSS_i
thrashing condition   D > m        (m = total frames)

page faults           counted over the reference string
```

### 8.2 Practice problems

**P1.** Memory access = 100 ns, page-fault service time = 10 ms, page-fault rate = 1 in 10,000.
Compute EAT. By what factor is it slower than 100 ns?

**P2.** Reference string `1 2 3 4 1 2 5 1 2 3 4 5`, **3 frames**. Run FIFO and LRU. Which has fewer
faults?

**P3.** Same string, FIFO, 3 vs 4 frames. What is the name of the effect, and which property does
FIFO violate?

**P4.** A system has 4 processes whose working-set sizes are 30, 45, 25 and 40 frames, and 128 frames
of memory. Is it thrashing? What can the OS do?

**P5.** Process A faults on page 6. A has frames holding pages {1,4,5} with last-use times 8, 12, 3.
Process B has pages {2,3} with last-use times 1, 9. Using LRU, which page is evicted under (a) local
replacement, (b) global replacement?

**P6.** Why does a clean victim page not need to be written back?

**P7.** Explain why OPT cannot be implemented but is still useful.

### 8.3 Solutions

<details>
<summary>Show solutions</summary>

**S1.** `EAT = 0.9999 × 100 ns + 0.0001 × 10,000,000 ns = 99.99 + 1000 ≈ 1,100 ns`.
That is about **11× slower** than 100 ns.

**S2.** With 3 frames: FIFO = **9** faults, LRU = **10** faults. Here FIFO wins — and note that
FIFO with 3 frames beats FIFO with 4 frames (P3).

**S3.** **Belady's anomaly**. FIFO violates the **inclusion property**.

**S4.** `D = 30 + 45 + 25 + 40 = 140 > 128` → **yes, thrashing**. The OS must **suspend/swap out** at
least one process so that D ≤ 128 (or reduce quotas via PFF).

**S5.** (a) Local: only A's pages qualify; earliest last-use is **A5 (time 3)** → evict A5.
(b) Global: earliest last-use overall is **B2 (time 1)** → evict B2; A gains a frame, B loses one.

**S6.** Its disk copy is still identical to the in-memory copy, so overwriting it loses nothing.

**S7.** It needs the future reference string, which the OS cannot know. It is still useful as a
**lower bound / benchmark** against which real algorithms are measured.

</details>

---

## 9. Self-test questions

1. What problem does virtual memory solve that paging alone does not?
2. What is a backing store, and how large must it be?
3. Which scheduler performs swapping?
4. State two costs of swapping.
5. Why must address translation be dynamic under swapping?
6. What does the valid–invalid bit mean in each state?
7. List the steps of page-fault handling in order.
8. Write the EAT formula and name each term.
9. Why are two disk I/Os needed when memory is full?
10. What is a dirty page, and why does the dirty bit matter?
11. Give the reference string used in the lecture and the fault counts for FIFO, OPT, LRU with 4 frames.
12. Why is OPT unimplementable, and what is it used for?
13. How does second chance differ from FIFO? When does it degrade to FIFO?
14. Define Belady's anomaly and the inclusion property.
15. Which of FIFO / OPT / LRU satisfy the inclusion property?
16. Distinguish fixed vs variable allocation and local vs global replacement.
17. Why is fixed + global impossible?
18. Define thrashing in one sentence.
19. Why can increasing the degree of multiprogramming reduce CPU utilisation?
20. Define the working set, WSS, D and the thrashing condition.
21. What are the two weaknesses of the working-set model, and what does PFF do instead?

<details>
<summary>Answer sketches</summary>

1. It lets a process run with a logical address space **larger than physical memory**.
2. Fast disk holding **all** process images; at least as large as the total logical space in use.
3. The **mid-term scheduler** (the swapper).
4. Disk copying overhead, and longer context-switch/dispatch time.
5. A swapped-in image may land in different physical frames.
6. `V` → page is in memory and the entry holds its frame number; `I` → not in memory and the entry
   holds its disk location.
7. Trap → locate on disk → find free frame → read page in → update PTE → return → restart instruction.
8. `EAT = (1−p)·mat + p·page-fault time`; p = fault probability.
9. One to write out the dirty victim, one to read in the missing page.
10. A page modified since loading; only dirty pages must be written back.
11. `1 2 3 4 1 2 5 1 2 3 4 5`; FIFO 10, OPT 6, LRU 8.
12. It needs future knowledge; used as a **benchmark/lower bound**.
13. Second chance uses the **reference bit** to skip recently used pages; it degrades to FIFO when
    all reference bits are set.
14. More frames can cause more faults; the inclusion property says the n-frame resident set is a
    subset of the (n+1)-frame resident set.
15. OPT and LRU (FIFO does not).
16. Fixed = quota never changes; variable = quota adapts. Local = evict own pages; global = evict
    anyone's.
17. Because taking another process's frame changes both processes' frame counts.
18. The system spends more time paging than executing.
19. Because more processes compete for the same frames, so each has fewer and faults more.
20. WS(t) = pages in the last Δ references; WSS = |WS|; D = Σ WSS; thrashing when D > m.
21. Δ has no known optimal value; measuring is costly. PFF instead bounds the **page-fault rate** and
    adds/removes frames accordingly.

</details>

---

## 10. Glossary

| Term | Meaning |
|---|---|
| **Virtual memory** | using disk to extend physical memory; logical space may exceed RAM |
| **Backing store** | disk area holding process images / non-resident pages |
| **Swapping** | moving a whole process image between memory and backing store |
| **Swap in / swap out** | bring an image in / push an image out |
| **Mid-term scheduler** | the swapper; decides swap in/out |
| **Demand paging** | load a page only when it is referenced |
| **Valid–invalid bit** | per-PTE flag: page resident or not |
| **Page fault** | reference to a page whose valid bit is `I` |
| **Page-fault time** | time to service a fault (context switches + disk I/O) |
| **EAT** | effective access time: average time per memory reference |
| **Victim page** | the page chosen for eviction |
| **Dirty (modified) bit** | set when a page is written; dirty pages must be written back |
| **Reference bit** | set by hardware on any read/write; basis of second chance |
| **Page replacement algorithm** | rule for choosing a victim (FIFO, OPT, LRU, clock) |
| **Page reference string** | sequence of pages referenced, used to evaluate algorithms |
| **Belady's anomaly** | more frames → more faults |
| **Inclusion property** | n-frame resident set ⊆ (n+1)-frame resident set |
| **Frame allocation** | deciding how many frames each process gets |
| **Replacement scope** | local (own frames) vs global (any frame) |
| **Thrashing** | system spends most time paging, CPU utilisation collapses |
| **Locality** | tendency to reuse a small set of pages/addresses (temporal, spatial) |
| **Working set** | pages referenced within the last Δ references |
| **WSS / D / m** | working-set size / total demand / total frames |
| **PFF** | page-fault-frequency scheme: adjust frames to keep fault rate in bounds |
