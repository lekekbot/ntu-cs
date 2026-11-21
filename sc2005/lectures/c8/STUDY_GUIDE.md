# SC2005 — Memory Organization: Study Guide

Companion to the five-part lecture series in this folder. Timestamps refer to the transcript of the
part named, e.g. **`03 @ 10:10`** means part 03, 10 min 10 s.
Transcripts: [part 01](transcripts/01-memory-organization-1-intro-and-address-binding.txt) ·
[part 02](transcripts/02-memory-organization-2-contiguous-allocation.txt) ·
[part 03](transcripts/03-memory-organization-3-paging-tlb-inverted-page-table.txt) ·
[part 04](transcripts/04-memory-organization-4-two-level-paging-supplement.txt) ·
[part 05](transcripts/05-memory-organization-5-segmentation-and-wrap-up.txt)

---

## 0. The chapter in one picture

Everything in these five lectures answers one question:

> A process runs in its **own logical address space**, starting at 0.
> The machine has **one physical memory**, shared by every process.
> **How is a logical address turned into a physical address, and what does that cost?**

Each allocation scheme is just a different answer to that question.

```
                         How do we place a process in physical memory?
                                        |
                 +----------------------+----------------------+
                 |                                             |
        CONTIGUOUS ALLOCATION                        NON-CONTIGUOUS ALLOCATION
        (process occupies one run of frames)         (process is scattered)
                 |                                             |
        +--------+--------+                       +------------+------------+
        |                 |                       |                         |
  Fixed partitioning  Dynamic partitioning     Paging                  Segmentation
  (pre-cut blocks)    (holes, on demand)   (fixed-size pages)     (variable-size segments)
        |                 |                       |                         |
   internal frag     external frag          internal frag              external frag
   relocation reg.   relocation reg.    page table / TLB /         segment table
                                          multi-level / inverted     (base + limit)
```

Parts of the series:

| Part | Topic | Transcript |
|---|---|---|
| 01 | Why memory management; storage hierarchy; process image; compile → link → load; **address binding**; logical vs physical address | [01](transcripts/01-memory-organization-1-intro-and-address-binding.txt) |
| 02 | **Contiguous allocation**: fixed partitioning, dynamic partitioning, first/best/worst fit, fragmentation, compaction | [02](transcripts/02-memory-organization-2-contiguous-allocation.txt) |
| 03 | **Paging**: frames/pages, page table, address splitting, PTBR/PTLR, **TLB + EMAT**, **inverted page table** | [03](transcripts/03-memory-organization-3-paging-tlb-inverted-page-table.txt) |
| 04 | **Two-level (multi-level) paging** — supplementary recording | [04](transcripts/04-memory-organization-4-two-level-paging-supplement.txt) |
| 05 | **Segmentation**, then the whole-chapter wrap-up | [05](transcripts/05-memory-organization-5-segmentation-and-wrap-up.txt) |

---

## 1. Why memory management exists (part 01, 00:00)

* In a **multiprogramming** system the OS wants a *supply of ready processes* so the CPU never idles.
  That means several processes must be resident in memory at once.
* Memory is the resource being shared, and it is finite. The OS must decide **who gets which bytes,
  and how a process's addresses are mapped onto them**.
* Three related but separate topics in the course:

| Topic | Question it answers | Resources involved |
|---|---|---|
| **Memory organization** (this series) | How is space allocated to a process inside physical memory? | main memory |
| **Virtual memory** (next series) | How do we pretend memory is bigger than it is? | memory + disk |
| **File systems** | How is space allocated to files? | disk |

### 1.1 Storage hierarchy (01 @ 01:26)

```
        registers          <- on CPU, ~1 cycle          } primary storage,
        cache              <- on CPU, ~10 cycles        } registers+cache are
        main memory        <- ~100 cycles               } hardware-managed
        flash / SSD        <- ~1 M cycles               } secondary storage
        traditional disk   <- ~10 M cycles              }
        remote storage     <- network (e.g. Internet)
   top: fast, small, expensive        bottom: slow, large, cheap
```

Going **down** the hierarchy: capacity ↑, access time ↑, cost per byte ↓.
The OS manages main memory and everything below it; registers and cache are hardware-managed.

### 1.2 The process image (01 @ 03:43)

To run a program, memory must be allocated for the **process image**:

```
low address
  +------------------+
  |      text        |  code (the program itself)
  +------------------+
  |      data        |  globals, static/global parameters, constants
  +------------------+
  |      heap        |  dynamically allocated objects (malloc / new)
  |        |         |
  |        v         |  grows upward
  +------------------+
  |        ^         |
  |        |         |
  |      stack       |  function parameters, local variables, return addresses
  +------------------+
high address
```

* Heap and stack grow **towards each other** from opposite ends.
* **Heap overflow / leak**: keep allocating objects and never free them → heap exhausted → the
  program is killed (core dump).
* **Stack overflow**: typically unbounded recursion → stack exhausted → program killed.
* The CPU, while executing, only ever emits addresses into this space. This space has several
  names used interchangeably in the lecture:
  **logical address space = process image = logical memory**.
* It always starts at 0 and is **byte-addressable**. Every process has its own; there is only one
  physical memory.

### 1.3 How the process image is produced (01 @ 06:53)

```
source code --[compiler]--> object module(s) --[linker]--> load module --[loader]--> process image
                              (per source file)            (+ libraries)          (in memory)
        on disk ------------------------------------------------------------------> in memory
```

| Tool | Job |
|---|---|
| **Compiler** | source code → object code (one object module per compilation unit) |
| **Linker** | combines object modules with libraries and **resolves cross-references** → a single load module |
| **Loader** | **allocates memory** for the process image and **loads** it into that memory |

---

## 2. Address binding (part 01, 08:56 → end)

The CPU emits address references while executing (`LOAD X`, `JMP Y`). **Can that reference be used
directly as a physical address?** The answer depends on *when* the program's code and data were
bound to physical addresses.

### 2.1 The three binding times

| Binding time | What the compiler emits | Who fixes the address | Can the process be moved later? |
|---|---|---|---|
| **Compile time** | **absolute** code (assumes it will load at a known address) | compiler | No — must recompile |
| **Load time** | **relocatable** code (offsets from start of image) | loader adds the load address once | No — must reload |
| **Execution time** | **relocatable** code | hardware adds the base **on every reference** | **Yes** |

### 2.2 Worked example — same program, three bindings

The process is to be loaded at physical address **1024**. It contains a `LOAD` of a datum at offset
800 and a `JMP` to offset 400.

**Compile-time binding**

```
compiler knows the load address is 1024
  -> emits absolute addresses directly:   LOAD 1824      JMP 1424
loader copies verbatim; no translation needed.
```

**Load-time binding**

```
compiler emits relocatable addresses:     LOAD 800       JMP 400
loader adds base 1024 while copying:      800 + 1024 = 1824
                                          400 + 1024 = 1424
after loading, code in memory is absolute.
```

**Execution-time binding**

```
compiler emits relocatable addresses:     LOAD 800       JMP 400
loader copies verbatim (still relative).
at run time, for every reference:         physical = base register (1024) + 800 = 1824
```

### 2.3 Why the course only cares about execution-time binding

Static binding (compile/load time) freezes the process in place. But almost every interesting
memory technique needs to **move a process while it is running**:

* **compaction** (part 02) — shuffle processes to merge holes,
* **swapping** — evict to disk and bring back somewhere else,
* **virtual memory** — pages move between disk and arbitrary frames.

None of these work if addresses were baked in. So:

> **From part 01 onwards, the assumption is execution-time (dynamic) binding.**

### 2.4 Logical vs physical address (01 @ 21:02)

| | Logical (virtual) address | Physical address |
|---|---|---|
| Generated by | CPU, during execution | memory unit, after translation |
| Space | one per process, starts at 0 | one, shared by all processes |
| Visible to | the process | the memory hardware |
| Size | can exceed physical memory (later, with VM) | limited by installed RAM |

* With **static** binding the two are identical (no translation needed).
* With **dynamic** binding they differ and every reference must be translated.
* **How** it is translated depends on the allocation scheme — that is exactly what parts 02–05
  cover:
  * contiguous → `base + offset` (relocation register)
  * paging → page table lookup (`frame number : offset`)
  * segmentation → segment table lookup (`base + offset`, after a limit check)

---

## 3. Contiguous allocation (part 02)

> The logical address space of the process stays **contiguous** in physical memory.

Two flavours: **fixed partitioning** and **dynamic partitioning**.

### 3.1 Fixed partitioning (02 @ 00:59)

Memory is **pre-divided** into a fixed number of partitions of fixed size, decided at boot time.
To run a process, the OS finds a partition large enough and assigns it.

```
physical memory                time ---->
+------------------+  <- partition 1     P1 runs here, then partition is freed
|   partition 1    |
+------------------+
|   partition 2    |  <- P2
+------------------+
|   partition 3    |  <- P3
+------------------+
|   partition 4    |  <- free
+------------------+
```

Problems:

1. **How many partitions, and how big?** The OS does not know future process sizes in advance.
2. A process usually does not fill its partition → the leftover **inside** the partition is wasted.
   This is **internal fragmentation**.
3. A process larger than the biggest partition can never run.

### 3.2 Dynamic partitioning (02 @ 04:02)

Partitions are created **on demand**; there is no pre-cut layout.

* **Hole** = a block of free memory. At boot there is one giant hole.
* A new process is placed in a hole big enough for it.
* When a process exits, its block becomes a hole again.
* The OS must track **allocated partitions** and **free partitions (holes)**.

Over time, create/terminate cycles chop memory into holes of assorted sizes — the memory becomes
**fragmented**.

### 3.3 Worked example — the job-queue timeline (02 @ 06:09)

Memory = **2560K**, of which the OS occupies **0–400K**, leaving **2160K** free.

| Process | Size | Burst (time units) |
|---|---|---|
| P1 | 600K | 10 |
| P2 | 1000K | 5 |
| P3 | 300K | 20 |
| P4 | 700K | 8 |
| P5 | 500K | 15 |

All five start in the **job queue** (new state), waiting to be loaded into memory.

**t = 0.** Load P1 (600), P2 (1000), P3 (300) → 1900K used, **260K** left.
P4 needs 700K, P5 needs 500K → neither fits. They stay in the job queue.

```
0      400   1000        2000  2300 2560
+--------+-----+-----------+-----+----+
|   OS   | P1  |    P2     | P3  |260K|   <- hole 260K
+--------+-----+-----------+-----+----+
```

**t = 5.** P2 finishes (burst 5). Its 1000K becomes a hole; P4 (700K) fits → 300K remains.

```
0      400       1000      1700 2000 2300  2560
+--------+---------+----------+-----+-----+----+
|   OS   |   P1    |    P4    |300K | P3  |260K|
+--------+---------+----------+-----+-----+----+
```

Holes are 300K and 260K; P5 (500K) still does not fit.

**t = 10.** P1 finishes. Its 600K becomes a hole; P5 (500K) fits → 100K remains.

```
0      400     900 1000      1700 2000 2300  2560
+--------+-------+---+----------+-----+-----+----+
|   OS   |  P5   |100|    P4    |300K | P3  |260K|
+--------+-------+---+----------+-----+-----+----+
```

Final holes: **100K, 300K, 260K** — classic **external fragmentation**.

**Ready-queue timeline:** t=0 {P1,P2,P3} → t=5 {P1,P3,P4} → t=10 {P3,P4,P5}.

### 3.4 Which hole? Dynamic storage-allocation policies (02 @ 11:46)

| Policy | Rule | Search cost | Leftover hole |
|---|---|---|---|
| **First-fit** | allocate the **first** hole that is big enough | stop at first match (fastest) | whatever is left; can be tiny |
| **Best-fit** | allocate the **smallest** hole that is big enough | must scan the whole list (unless kept sorted by size) | **smallest** leftover (creates many useless slivers) |
| **Worst-fit** | allocate the **largest** hole | must scan the whole list | **largest** leftover (leaves a usable hole) |

Memory hook: *first* = stop early, *best* = tightest fit, *worst* = biggest hole.
Best-fit produces the smallest leftover, **not** the best overall behaviour — small leftovers are
often unusable, which worsens external fragmentation.

### 3.5 Fragmentation and compaction (02 @ 13:54)

| | **Internal fragmentation** | **External fragmentation** |
|---|---|---|
| Where | **inside** an allocated block | **between** allocated blocks |
| Meaning | allocated more than was asked for; the excess is unusable | enough total free memory exists but it is **not contiguous** |
| Caused by | fixed partitioning, paging (last page) | dynamic partitioning, segmentation |
| Fix | smaller block size | **compaction**, or non-contiguous allocation |

**Compaction** = shuffle the contents of memory to push all holes together into one large hole.

Back to the example at t = 5: the 300K hole and the 260K hole are separated by P3 (300K).
Move P3 into the 300K hole; the old P3 area and the trailing 260K hole become **one 560K hole**,
big enough for P5 — so P5 loads at **t = 5** instead of t = 10.

*(The lecturer quotes 500K; summing 300K + 260K gives 560K. Either way it fits P5.)*

Costs / requirements of compaction:

* **Overhead**: copying every byte of every moved process.
* Requires **execution-time binding** — if addresses were absolute, moving a process would break it.

### 3.6 Address translation for contiguous allocation (02 @ 19:33)

```
        logical address (offset from start of image)
                 |
                 v
   +-----------------------------+
   | relocation register = base  |----> +  = physical address
   +-----------------------------+            |
                                              v
                                        physical memory
```

* **Relocation register** holds the **base** — the physical address where the process image starts
  (1024 in the example).
* The logical address is the **offset** from the start of the image.
* `physical address = base + offset`.
* The companion **limit register** holds the length of the image; `offset ≥ limit` is a fault.
* The add happens **at run time**, on every reference.

---

## 4. Paging (part 03)

> Non-contiguous allocation: the logical address space is scattered over physical memory.

### 4.1 The basic scheme (03 @ 00:00)

* Physical memory is divided into fixed-size blocks called **frames**.
* The logical address space is divided into blocks of the **same size** called **pages**.
* Typical size: a power of 2 between **512 B and 8192 B**.
* To load a process of *n* pages, the OS needs *n* **free frames** anywhere in memory.
* The OS tracks:
  1. **which frames are free**, and
  2. **which page is in which frame** → the **page table** (one entry per page).

Consequences:

* **No external fragmentation** — any free frame can be used, so there is never unusable space
  *between* allocations.
* **Internal fragmentation remains**, but only in the **last page**, because the logical address
  space is not necessarily a multiple of the page size.

### 4.2 The canonical example (03 @ 04:30)

```
logical address space: 16 bytes = 4 pages, page size 4 bytes
physical memory:       32 bytes = 8 frames, frame size 4 bytes

page 0  -> frame 5
page 1  -> frame 6
page 2  -> frame 1
page 3  -> frame 2

page table (index = page number, content = frame number)
   +---+---+
   | 0 | 5 |
   | 1 | 6 |
   | 2 | 1 |
   | 3 | 2 |
   +---+---+
```

Nothing is contiguous: page 0 is in frame 5 while page 1 is in frame 6, page 2 jumps back to
frame 1.

### 4.3 Splitting the logical address

Let the logical address space be **2^m bytes** and the page size be **2^n bytes**.

```
   m bits of logical address
   +---------------------+-----------+
   |   page number (p)   | offset (d)|
   +---------------------+-----------+
     m - n bits            n bits
```

| Quantity | Formula |
|---|---|
| Number of pages | `2^m / 2^n = 2^(m-n)` |
| Bits for offset | `n = log2(page size)` |
| Bits for page number | `m - n` |
| Page-table entries | one per page = `2^(m-n)` |
| Page-table size | `2^(m-n) × entry size` |

Rule of thumb: **the page size decides where you cut the address.** The low `n` bits are always the
offset, because pages are aligned to their own size.

### 4.4 Worked translation (03 @ 14:40)

Logical address space 16 bytes (m = 4), page size 4 bytes (n = 2). Translate logical address
`0111`.

```
logical address  0 1 | 1 1
                 p=01  d=11
                 page 1, offset 3   (the last byte of page 1)

page table[1] = 6        -> frame 6 = 110 in binary
physical address = f : d = 110 : 11 = 11011 (binary) = 27
```

So logical `0111` → physical `11011`.

The three steps, every time:

1. split the logical address into `p | d`;
2. `f = page_table[p]`;
3. physical address = `f | d` (concatenate, i.e. `f × page_size + d`).

### 4.5 Where is the page table? (03 @ 19:20)

* The page table lives **in physical memory** (it is far too big for registers).
* **PTBR** — Page-Table **Base** Register: physical address of the current process's page table.
* **PTLR** — Page-Table **Length** Register: size of that page table (bounds check).
* Both describe **the running process only**. On a **context switch** they are saved into and
  restored from the **PCB** (process control block).

### 4.6 The performance problem (03 @ 21:32)

Every memory reference now costs **two** memory accesses:

```
1. read the page table entry  (page table is in memory)
2. read the actual datum      (physical memory)
```

If a memory access takes μ, then **EMAT = 2μ** — memory access time has doubled. (The slide states
this explicitly: *"Effective memory access time = 2μ (assuming memory cycle time is μ)"*.)

### 4.7 Translation look-aside buffer (TLB) (03 @ 23:09)

A **TLB** (also called **associative registers**) is a small, very fast hardware cache of recent
**page-number → frame-number** translations.

```
                 +-----------+
   logical addr  |  p  |  d |
                 +-----+-----+
                    |
                    v
             +-------------+   hit  (probability α)          +----------------+
             |     TLB     |----------------------------->   |                |
             +-------------+                                 |  physical      |
                    | miss (probability 1-α)                |  memory        |
                    v                                        |                |
             +-------------+                                 |                |
             | page table  |-------------------------------->|                |
             +-------------+      frame number               +----------------+
                  (in memory)
```

| Path | Cost |
|---|---|
| **TLB hit** | TLB lookup `ε` + one memory access `μ` |
| **TLB miss** | TLB lookup `ε` + page-table access `μ` + data access `μ` = `ε + 2μ` |

With hit ratio **α**:

```
EMAT = α (ε + μ)  +  (1 - α)(ε + 2μ)
     = ε + μ + (1 - α) μ
     = ε + (2 - α) μ
```

Sanity checks:

* α = 0 (never hits) → `ε + 2μ`, i.e. the TLB adds a small cost to the 2-access scheme.
* α = 1 (always hits) → `ε + μ`, i.e. nearly the speed of no paging at all.
* Since `ε ≪ μ`, high hit ratios make paging almost free.

The slide annotates the same formula by hand as `α × (ε + μ) + (1-α) × (ε + μ + μ)`, which is the
same thing written out: the TLB is consulted in **both** cases, the page table only on a miss.

### 4.8 Inverted page table (03 @ 30:20)

Problem: one page table **per process**, with one entry per page. Big logical address space → big
page table → a lot of memory spent just on tables (and each table needs contiguous space — see
part 04).

Solution: **one table for the whole system**, with **one entry per physical frame**.

| | Normal page table | Inverted page table |
|---|---|---|
| How many tables | one per process | **one for the entire system**, shared |
| Entries | one per **page** (logical) | one per **frame** (physical) |
| Table size depends on | size of logical address space | size of **physical memory** |
| Entry contents | frame number | **`<PID, page number>`** |
| Ordered by | page number | **frame number** |
| Lookup | direct index by page number, **O(1)** | **search** for `<PID, page>` — slower |
| Memory cost | high (many tables) | low (single table) |

Why `PID` must be in the entry: the table is shared, so "page 5" alone does not say *whose* page 5.

Translation:

```
logical address  ->  ( PID | page number | offset )

search the inverted page table for the entry <PID, page number>
  if the match is at entry i, then this page is in frame i
physical address = i : offset
```

Trade-off: **saves memory, costs time** (linear search, unless accelerated by hashing or a TLB).

---

## 5. Two-level paging (part 04, supplementary)

> This is the recording the main lecture skips. Part 05 @ 18:02: *"we didn't cover multi-level
> paging… you can look at the textbook."* This video covers it properly.

### 5.1 Why one level is not enough (04 @ 00:00)

Assume a 32-bit logical address and a 4 KB page.

| Step | Calculation |
|---|---|
| Page size | 4 KB = **2^12** → offset = **12 bits** |
| Page number | 32 − 12 = **20 bits** |
| Pages in logical space | **2^20** |
| Page-table entries | **2^20** (one per page) |
| Entry size | assume **4 bytes** |
| Page-table size | 2^20 × 4 B = **4 MB** |

A **4 MB page table must be contiguous in physical memory** — finding such a hole is a serious
problem. And that is *per process*.

### 5.2 The idea

**Page the page table itself.** Split the 4 MB table into 4 KB pages and load those pages into any
available frames. To find a page of the page table you need… another table: the **outer page table**.

```
                         logical address
        +----------------+----------------+----------------+
        |  P1 (10 bits)  |  P2 (10 bits)  |   offset (12)  |
        +--------+-------+--------+-------+--------+-------+
                 |                |                |
                 v                |                |
      +---------------------+     |                |
      |  OUTER page table   |     |                |
      |  (one entry per     |     |                |
      |   inner-table page) |     |                |
      +----------+----------+     |                |
                 | gives the frame  |                |
                 | holding an inner |                |
                 | page-table page  |                |
                 v                  |                |
      +---------------------+       |                |
      |  INNER page table   |       |                |
      |  (one page of it)   |       |                |
      +----------+----------+       |                |
                 | P2 indexes within |                |
                 | this page; gives  |                |
                 | the data frame f  |                |
                 v                  v                v
            +---------------------------------------------+
            |        physical address = f : offset        |
            +---------------------------------------------+
```

### 5.3 Sizing the split (04 @ 08:19)

| Question | Working | Answer |
|---|---|---|
| How big is the page table? | 2^20 entries × 4 B | 2^22 B = **4 MB** |
| How many pages is that? | 2^22 / 2^12 | **2^10** pages |
| How many entries does the outer table need? | one per page of the inner table = 2^10 | 2^10 → **P1 = 10 bits** |
| How many entries fit in one inner page? | page size / entry size = 2^12 / 4 = 2^10 | 2^10 → **P2 = 10 bits** |
| Offset | page size 2^12 | **12 bits** |
| Check | 10 + 10 + 12 | **32 bits** ✓ |

### 5.4 The translation walk-through (04 @ 10:14)

1. **PTBR** points at the start of the **outer** page table in physical memory.
2. `P1` indexes the outer table → entry contains the **frame number of one inner page table page**.
3. Go to that frame; `P2` indexes **within that page** → entry contains the **frame number of the
   data page**.
4. Concatenate that frame number with `offset` → **physical address**.

Cost: **three memory accesses** for a miss (outer entry, inner entry, datum), versus two for
single-level paging. That is precisely why TLBs matter even more here.

### 5.5 Generalising

Three-level paging pages the inner page table again; four-level paging does it once more. The
concept is identical — you just split the page-number field into more pieces, and each level adds
one more memory access on a miss.

> **Terminology warning.** The lecturer calls the table indexed by P1 the **"second level" / "outer"**
> table and the table indexed by P2 the **"first level" / "inner"** table. Standard textbooks
> (e.g. Silberschatz) number them the other way: **outer = level 1**, **inner = level 2**. The
> mechanism is the same; just be careful which numbering a question uses.

---

## 6. Segmentation (part 05)

> A logical address space is a **collection of segments** — not a flat byte sequence.

### 6.1 What a segment is (05 @ 00:00)

* A **segment** is a **logical unit of the program**: the main program, a subroutine/procedure, a
  specific data structure, the stack, the symbol table…
* Each segment is a sequence of bytes, but **different segments have different sizes** — segments
  are **variable-sized**.
* Segments of one process are **not contiguous** in physical memory.

Contrast with paging:

| | Paging | Segmentation |
|---|---|---|
| Division of logical space | fixed-size **pages** | variable-size **segments** |
| Chosen by | hardware/OS (invisible to programmer) | the program's logical structure (visible) |
| Logical address | `page number : offset` | `segment number : offset` |
| Table | page table (one entry per page) | segment table (one entry per segment) |
| Table entry | frame number | **base + limit** |
| Fragmentation | **internal** (last page) | **external** |
| Size limit | page size fixed | segment size varies |

### 6.2 Segment table and registers (05 @ 03:26)

Each entry has exactly two fields:

* **base** — starting physical address of the segment
* **limit** — length of the segment

Registers:

* **STBR** — Segment-Table **Base** Register: where the segment table is in memory.
* **STLR** — Segment-Table **Length** Register: number of segments (bounds check on the *segment
  number*).
* Saved/restored in the **PCB** on a context switch, exactly like PTBR/PTLR.

### 6.3 Address translation (05 @ 05:34)

```
logical address  =  <s, d>

1. if s >= STLR                    -> trap (invalid segment number)
2. base, limit = segment_table[s]
3. if d >= limit                   -> trap: addressing error
4. physical address = base + d
```

The **limit check is the defining feature of segmentation**: it catches an offset that runs off the
end of the segment, which paging cannot do (a page offset always fits inside a page).

### 6.4 Worked example (05 @ 07:42)

Segment table from the slide:

| segment | limit | base |
|---|---|---|
| 0 | 1000 | 1400 |
| 1 | 400 | 6300 |
| 2 | 400 | 4300 |
| 3 | **1100** | **3200** |
| 4 | 1000 | 4700 |

Translate `<3, 128>`:

```
s = 3, d = 128
segment_table[3] = (base 3200, limit 1100)
128 < 1100                    -> legal
physical = 3200 + 128 = 3,328
```

If the offset had been `1500`, it would exceed the limit (1100) → **trap**, handled by the OS.

### 6.5 Allocating segments and fragmentation (05 @ 12:42)

* Each segment needs a **hole large enough** for it — this is exactly the **dynamic
  storage-allocation problem** from part 02, so **first-fit / best-fit / worst-fit** apply.
* Segments come and go → holes of varying size appear **between** segments → **external
  fragmentation**.
* Segmentation does **not** cause internal fragmentation: a segment gets exactly its size.

> The transcript at 05 @ 13:37 has the lecturer saying *"it's also suffered from internal
> fragmentation"*, then immediately describing holes that are "too small to be useful" — which is
> **external** fragmentation. See [NOTES.md](NOTES.md#3-known-slips-in-the-lectures).

---

## 7. Putting it all together

### 7.1 Scheme comparison

| Scheme | Allocation | Address translation | Table | Internal frag. | External frag. |
|---|---|---|---|---|---|
| **Fixed partitioning** | contiguous, pre-cut | `base + offset` (relocation register) | none | **yes** | no |
| **Dynamic partitioning** | contiguous, on demand | `base + offset` (relocation register) | none | no | **yes** |
| **Paging** | non-contiguous, fixed frames | page table → `frame : offset` | page table (1 entry/page) | **yes** (last page) | **no** |
| **Segmentation** | non-contiguous, variable | segment table → `base + offset` + limit check | segment table (1 entry/segment) | no | **yes** |
| **Inverted paging** | non-contiguous | search `<PID,page>` → `frame : offset` | one system-wide table (1 entry/frame) | yes (last page) | no |

### 7.2 "Which table is it?" summary

| Table | One entry per | Entry contains | Base register |
|---|---|---|---|
| Page table | **page** (logical) | frame number (+ flags) | PTBR |
| Inverted page table | **frame** (physical) | `<PID, page number>` | — (single table) |
| Segment table | **segment** | base + limit | STBR |
| Outer page table (2-level) | page of the inner table | frame number | PTBR |

### 7.3 Fragmentation matrix (memorise this)

| Scheme | Fragmentation |
|---|---|
| Fixed partitioning | internal |
| Dynamic partitioning | external |
| Paging | internal (last page only) |
| Segmentation | external |

---

## 8. Formula sheet

```
page / frame size          = 2^n
logical address space      = 2^m
number of pages            = 2^(m-n)
offset bits                = n = log2(page size)
page-number bits           = m - n

page table size            = number_of_pages × entry_size
inverted table size        = number_of_frames × entry_size  (independent of #processes)

physical address (paging)  = frame_number × page_size + offset
physical address (contig.) = base + offset            (offset < limit)

EMAT, no TLB               = 2μ
EMAT, with TLB             = α(ε + μ) + (1-α)(ε + 2μ)
                           = ε + (2 - α)μ

two-level split            = P1 bits | P2 bits | offset bits
  P2 bits = log2(page size / PTE size)
  P1 bits = log2(number of PT pages)
  P1 + P2 + offset = m
```

Symbols: `μ` = memory access time, `ε` = TLB (or memory cycle) time, `α` = TLB hit ratio.

---

## 9. Practice problems

Try these before reading the solutions.

**P1.** A system has a 64 KB logical address space and 4 KB pages, with 8-byte page-table entries.
(a) How many pages? (b) How many bits for offset and page number? (c) How big is the page table?

**P2.** A 32-bit machine uses 8 KB pages and 4-byte PTEs, with two-level paging.
Give the P1 / P2 / offset split.

**P3.** TLB access = 2 ns, memory access = 100 ns, hit ratio = 90 %.
(a) EMAT with the TLB? (b) EMAT with no TLB?

**P4.** Free holes in address order: 100K, 500K, 200K, 300K, 600K. A request for 250K arrives.
Which hole does first-fit, best-fit and worst-fit choose, and what is left over?

**P5.** Segment table: segment 2 has base 6000, limit 400. Translate `<2, 350>` and `<2, 450>`.

**P6.** Physical memory is 4 GB, frame size 4 KB. How many entries does an inverted page table need?

### Solutions

<details>
<summary>Show solutions</summary>

**S1.** (a) 64 KB / 4 KB = 16 pages. (b) offset = log2(4096) = **12 bits**; page number =
16 − 12 = **4 bits**. (c) 16 × 8 B = **128 B**.

**S2.** Offset = log2(8192) = **13 bits**. Pages = 2^32 / 2^13 = 2^19. Entries per inner page
= 8192 / 4 = 2048 = 2^11 → **P2 = 11 bits**. Number of inner pages = 2^19 / 2^11 = 2^8 → **P1 =
8 bits**. Check: 8 + 11 + 13 = 32 ✓.

**S3.** (a) `ε + (2−α)μ = 2 + (2 − 0.9) × 100 = 2 + 110 = **112 ns**`.
Check by hand: hit = 0.9 × (2 + 100) = 91.8; miss = 0.1 × (2 + 200) = 20.2; total 112 ns ✓.
(b) `2μ = **200 ns**`.

**S4.** First-fit → **500K** (leftover 250K). Best-fit → **300K** (leftover 50K). Worst-fit →
**600K** (leftover 350K).

**S5.** `<2,350>`: 350 < 400 → legal; physical = 6000 + 350 = **6350**.
`<2,450>`: 450 ≥ 400 → **trap (addressing error)**.

**S6.** 4 GB / 4 KB = 2^32 / 2^12 = 2^20 = **1,048,576 entries** — one per frame, regardless of how
many processes exist.

</details>

---

## 10. Self-test questions

1. Why does multiprogramming require several processes in memory at once?
2. Name the three binding times and say which one allows a process to be moved while running.
3. In load-time binding, what exactly does the loader add?
4. Give the two conditions under which logical and physical addresses are identical.
5. What is the difference between a page and a frame?
6. Why does paging eliminate external fragmentation but not internal fragmentation?
7. A logical address is 32 bits with 4 KB pages. How many bits are the page number?
8. Where is the page table stored, and how does the CPU find the current one?
9. Why does paging without a TLB double the memory access time?
10. State the EMAT formula with a TLB and explain each term.
11. Why must an inverted page-table entry contain the PID?
12. What problem does two-level paging solve, and what does it cost?
13. Give the bit split for a 32-bit address with 4 KB pages and 4-byte PTEs using two-level paging.
14. In segmentation, what does the limit field protect against?
15. Which schemes suffer external fragmentation, and which suffer internal fragmentation?
16. Why is compaction impossible with compile-time binding?

<details>
<summary>Answer sketches</summary>

1. To keep the ready queue non-empty so the CPU never idles; I/O-bound processes would otherwise
   leave the CPU idle.
2. Compile time, load time, execution time. Only **execution time** binding allows movement.
3. The **load (base) address** of the process image, to every relocatable address, once.
4. When binding is static — compile time or load time.
5. A **page** is a fixed-size block of the **logical** address space; a **frame** is a fixed-size
   block of **physical** memory. Same size.
6. Any free frame will do, so no unusable space is left *between* allocations. The last page can
   still be partly empty → internal fragmentation.
7. 32 − 12 = **20 bits**.
8. In **physical memory**; **PTBR** points to it and **PTLR** gives its length; both are reloaded
   from the PCB on a context switch.
9. One access for the page-table entry plus one for the datum.
10. `EMAT = α(ε+μ) + (1−α)(ε+2μ) = ε + (2−α)μ` — α = hit ratio, ε = TLB lookup, μ = memory access.
11. Because one table is shared by all processes; the same page number can exist in several
    processes, so `<PID, page>` is needed to identify the owner.
12. It removes the need for one huge **contiguous** page table (e.g. 4 MB for a 32-bit address
    space) by paging the page table. Cost: an extra memory access on a TLB miss.
13. **10 | 10 | 12**.
14. An offset that runs past the end of the segment — producing a trap instead of silently reading
    another segment's memory.
15. External: **dynamic partitioning, segmentation**. Internal: **fixed partitioning, paging**.
16. Because compaction moves a process, which invalidates absolute addresses baked in at compile
    time.

</details>

---

## 11. Glossary

| Term | Meaning |
|---|---|
| **Process image** | the memory layout of a running program: text, data, heap, stack. Same as logical address space / logical memory |
| **Logical (virtual) address** | address emitted by the CPU; relative to the start of the process image |
| **Physical address** | address presented to the memory unit |
| **Binding** | fixing code/data to specific physical addresses (compile / load / execution time) |
| **Relocation register** | holds the base address of the process image; added to every logical address |
| **Limit register** | holds the length of the process image; used for bounds checking |
| **Hole** | a block of free memory in dynamic partitioning |
| **Frame** | fixed-size block of physical memory |
| **Page** | fixed-size block of the logical address space (same size as a frame) |
| **Page table** | per-process map: page number → frame number |
| **PTBR / PTLR** | page-table base / length registers for the running process |
| **TLB** | translation look-aside buffer; fast cache of page→frame translations |
| **Hit ratio (α)** | fraction of references whose translation is found in the TLB |
| **Inverted page table** | single system-wide table, one entry per frame, holding `<PID, page>` |
| **Segment** | variable-size logical unit of a program (code, data, stack, …) |
| **Segment table** | per-process map: segment number → (base, limit) |
| **STBR / STLR** | segment-table base / length registers |
| **Internal fragmentation** | wasted space *inside* an allocated block |
| **External fragmentation** | enough total free space, but not contiguous |
| **Compaction** | shuffling memory to merge holes; needs execution-time binding |
| **Context switch** | changing the running process; PTBR/PTLR/STBR/STLR are saved to and restored from the PCB |
