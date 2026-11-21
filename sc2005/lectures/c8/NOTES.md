# Memory Organization — Things to Take Note Of

This is the "before the exam" file: what the lecturer stressed, what is easy to get wrong, and where
the recordings/slides themselves are unreliable. It deliberately contains no new material — the
teaching is in [STUDY_GUIDE.md](STUDY_GUIDE.md).

---

## 1. What the lecturer repeatedly stresses

| Point | Where | Why it matters |
|---|---|---|
| **"It's very important to differentiate logical address space and physical address space"** | 01 @ 23:49 | Almost every later mistake (and exam mark) comes from confusing the two. Every process has a logical space; there is **one** physical memory. |
| **We assume execution-time binding from here on** | 01 @ 20:10 | Compile/load-time binding is described only to be dismissed. Everything later (compaction, swapping, virtual memory) needs dynamic relocation. |
| **The page table is itself in physical memory** | 03 @ 19:20, 21:32 | This single fact explains the doubled access time, PTBR/PTLR, and why the TLB exists. |
| **TLB hit vs miss, then the EMAT arithmetic** | 03 @ 25:51 → 28:15 | He derives the formula term by term on the whiteboard. Expect to reproduce it, not just quote it. |
| **Inverted table trades memory for time** | 03 @ 34:24 | "Save memory, but translation time becomes longer." Both halves are examinable. |
| **Segment limit check before adding base** | 05 @ 05:34 | The limit check is what distinguishes segmentation from paging; skipping it is a classic error. |

---

## 2. Exam traps

1. **Page vs frame.** Page = block of *logical* space; frame = block of *physical* memory. Same size,
   different address spaces.
2. **Offset bits come from the page size, not the address width.** 4 KB pages → 12 offset bits,
   always.
3. **Page table size scales with the logical address space; the inverted table scales with physical
   memory.** A question that changes RAM size changes only the inverted table.
4. **Two accesses, not one.** Without a TLB, EMAT = 2μ. Many answers forget the page-table access.
5. **The TLB does not remove the page table.** A miss still walks the page table. A hit *skips* it.
6. **Hit ratio arithmetic.** Use `α(ε+μ) + (1−α)(ε+2μ)`, not `αμ + (1−α)2μ` (the TLB lookup happens
   in **both** cases).
7. **Best-fit ≠ "best".** It minimises the leftover, which creates the most useless slivers.
   First-fit is the fastest; worst-fit leaves the largest usable hole.
8. **Compaction is not free and not always possible.** It costs copying, and needs execution-time
   binding.
9. **Paging has internal fragmentation, not external.** Only the last page can be partly unused.
   A question saying "paging suffers external fragmentation" is false.
10. **Segmentation has external, not internal, fragmentation.** Segments get exactly their size.
11. **Inverted page table needs the PID in each entry.** Without it, page 5 of process A is
    indistinguishable from page 5 of process B.
12. **Two-level paging does not reduce the total table size.** It removes the need for one
    **contiguous** 4 MB block; the entries still exist, just spread over pages (plus a small outer
    table).
13. **Multi-level costs more accesses on a miss.** Single-level miss = 2 accesses; two-level miss =
    3 accesses before the datum.
14. **The limit register / limit field checks the offset, not the base.**

---

## 3. Known slips in the lectures

These are errors in the live delivery or on the slides — not transcription errors. Learn the correct
version.

| Where | What was said | Correct version |
|---|---|---|
| 02 @ 17:30 | Compaction merges the holes into "500K" | The two holes are 300K and 260K → **560K**. Either way it fits P5; only the arithmetic is off. |
| 03 @ 02:30 | "we need to find **unavailable** frames" | **available** (free) frames — the next sentence says the OS tracks "which frame is currently free". |
| 05 @ 13:37 | "For segmentation … it's also suffered from **internal** fragmentation" | **External** fragmentation — he immediately describes holes "too small to be useful", which is the definition of external. |
| 05 @ 15:53 (wrap-up) | "**internal** fragmentation happens when we're using either dynamic partitioning or segmentation" | **External**. (Internal is fixed partitioning and paging.) |
| 04 @ 05:04 | "this big page table will be divided into 2^10 pages. So correspondingly, in the next level of page table, then there will be **2^20** entries" | The outer table needs **2^10** entries (one per page of the inner table). That is why P1 is 10 bits. |
| 04 @ 05:50 | Calls the P1-indexed table the "**second level / outer**" and the P2-indexed table the "**first level / inner**" | Textbook convention is the reverse (outer = level 1). Follow whichever numbering the question uses, but know the mapping: **P1 indexes the table of table-pages**. |

---

## 4. Slide numbering is section-based — do not rely on it

All recordings are from the same **SC2005/CE2005/CZ2005 Operating Systems** deck, but the numbering
is per-section and the series hops between sections:

| Content | Slide numbers seen |
|---|---|
| Part 7 overview | 7.1 |
| Contiguous allocation | 6.7 … |
| Paging, page-table implementation, TLB | 6.22 – 6.24 |
| Two-level paging (part 04) | 7.40 |
| Segmentation (part 05) | 7.29 – 7.31 … |

Two consequences:

* Slides are **not** in one ascending sequence across the recordings, so a slide number tells you
  nothing about the order of the videos.
* The deck covers the same material in two overlapping sections, which is why part 05's wrap-up
  re-defines fragmentation that part 02 already defined, and why the summary slides look like a
  different deck. It is the same course.

Use the transcript **timestamps** (and the coverage map in §5) rather than slide numbers.

---

## 5. Coverage map (what to watch when)

| Topic | Part | Timestamp |
|---|---|---|
| Why memory management; storage hierarchy | 01 | 00:00 – 03:43 |
| Process image (text/data/heap/stack), overflow | 01 | 03:43 – 06:53 |
| Compiler → linker → loader | 01 | 06:53 – 08:56 |
| Address binding: compile / load / execution | 01 | 08:56 – 21:02 |
| Logical vs physical address | 01 | 21:02 – 24:52 |
| Fixed partitioning | 02 | 00:59 – 04:02 |
| Dynamic partitioning + holes | 02 | 04:02 – 06:09 |
| Worked job-queue timeline | 02 | 06:09 – 11:46 |
| First-fit / best-fit / worst-fit | 02 | 11:46 – 13:54 |
| Fragmentation + compaction | 02 | 13:54 – 19:33 |
| Relocation register translation | 02 | 19:33 – 22:50 |
| Paging basics, page table, example | 03 | 00:00 – 08:03 |
| Address format and bit split | 03 | 08:03 – 14:40 |
| Worked translation `0111 → 27` | 03 | 14:40 – 19:20 |
| PTBR / PTLR / context switch | 03 | 19:20 – 21:32 |
| Two-access problem | 03 | 21:32 – 23:09 |
| TLB and EMAT derivation | 03 | 23:09 – 29:11 |
| Inverted page table | 03 | 29:11 – 36:12 |
| Why multi-level; 4 MB example | 04 | 00:00 – 03:39 |
| Structure and bit split | 04 | 03:39 – 09:16 |
| Two-level translation | 04 | 10:14 – 12:46 |
| Segmentation concepts and example | 05 | 00:00 – 07:42 |
| Segment translation + limit check | 05 | 05:34 – 11:23 |
| Segment allocation / fragmentation | 05 | 11:23 – 14:39 |
| Whole-chapter wrap-up | 05 | 14:39 – 19:34 |

---

## 6. Memory hooks that actually help

* **Page = paper (logical), Frame = photograph frame (physical).** Same size, different worlds.
* **Offset lives at the bottom of the address.** Page size decides how many low bits are "inside the
  block"; everything above is the block number.
* **First-fit stops early; best-fit squeezes tight; worst-fit takes the biggest.**
* **Internal = *inside* a block; external = *between* blocks.** The word tells you the location.
* **Paging → pages are invisible to the programmer; segmentation → segments are visible** (a
  subroutine, a stack, a data structure).
* **Inverted table = turn the page table inside out**: entries indexed by frame instead of page.
* **TLB = "table's greatest hits"** — a small cache of the translations you keep reusing.

---

## 7. ASR correction glossary

The `.srt` files are verbatim; the `.txt` files apply the substitutions below. Remaining oddities are
ASR, not lecture content.

| In the transcript | Actual term |
|---|---|
| offside / off-side / off-site | **offset** |
| "1, 2, 8" (part 05) | **128** |
| "base 2, 3, 2, 0, 0" (part 05) | **base 3200** — the slide's segment table is limit 1100 / base 3200 for segment 3 |
| TRB, translation look asset buffer | **TLB**, translation look-aside buffer |
| bias feet / by-speed | **best fit** |
| first of feet / first-speed | **first fit** |
| worst feet / worst-speed | **worst fit** |
| present image / precise image / preset image | **process image** |
| resistor | **register** |
| OIS | **OS** |
| 2.0 of nbis, 2 part of 10, 2.12, 2.20, 2.32 | **2^n bytes, 2^10, 2^12, 2^20, 2^32** |
| nbis / imbis | **n bits / m bits** |
| CELUN / EELIN | **epsilon (ε)** |
| assess / assessing | **access / accessing** |
| text session / heap session | **text section / heap section** |
| call down | **core dump** |
| contact switch | **context switch** |
| heat ratio | **hit ratio** |
| pitching scheme | **paging scheme** |
| nine contiguous | **non-contiguous** |
| "the person in the running state" | **the process in the running state** |
| 92 clase kollấp queens (02 @ 14:24) | untranscribable noise, removed |
| German-sounding gibberish (03 @ 23:49) | ASR hallucination, removed |
| Repeated "So in the next part, you can see the answer" (04 @ 13:00) | ASR repetition loop at end of file, removed |

---

## 8. Quick self-check before the exam

- [ ] Can you draw the process image and label all four sections?
- [ ] Can you state the three binding times and which one permits relocation?
- [ ] Can you reproduce the 2560K job-queue timeline without notes?
- [ ] Can you define internal vs external fragmentation in one sentence each, and assign each scheme?
- [ ] Can you split a 32-bit address into `p : d` for any page size?
- [ ] Can you derive `EMAT = ε + (2−α)μ` from the hit/miss paths?
- [ ] Can you explain why a page table is stored in memory and how PTBR/PTLR find it?
- [ ] Can you explain the inverted page table's entry format and its trade-off?
- [ ] Can you do the 10/10/12 two-level split from scratch, including the 4 MB motivation?
- [ ] Can you translate a segmentation address and say when it traps?
