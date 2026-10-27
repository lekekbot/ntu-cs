# Virtual Memory — Things to Take Note Of

Exam-focused companion to [STUDY_GUIDE.md](STUDY_GUIDE.md): what the lecturer stresses, what is easy
to get wrong, and where the recordings are unreliable. No new material.

---

## 1. What the lecturer repeatedly stresses

| Point | Where | Why it matters |
|---|---|---|
| **Virtual memory decouples logical space from physical memory** | 01 @ 07:28 | This is the one-sentence answer to "what is virtual memory for?" |
| **Page fault time ≫ memory access time** | 01 @ 24:06 | Every performance argument (EAT, thrashing) rests on this |
| **Only dirty pages are written back** | 02 @ 03:46 | The dirty bit exists purely to save a disk write |
| **Objective of replacement = minimise page faults** | 02 @ 05:27 | Not "maximise hits" as an abstract goal — count faults on the string |
| **OPT is a benchmark, not an implementation** | 02 @ 12:44 | Expect the question "why study an algorithm we cannot run?" |
| **FIFO can get worse with more memory** | 03 @ 02:05 | Belady's anomaly; the inclusion property is the explanation |
| **Fixed allocation forces local replacement** | 04 @ 11:26 | The combination table is a favourite exam item |
| **More multiprogramming is not always better** | 05 @ 02:01 | The thrashing curve is the counter-intuitive result of the chapter |

---

## 2. Exam traps

1. **A page fault is normal, not an error.** It means "the page is not resident".
2. **Valid bit `V` → frame number; `I` → disk address.** The PTE means different things in the two
   states.
3. **The faulting instruction is restarted**, not continued or skipped.
4. **Two disk I/Os** are needed when memory is full (page out + page in) — one is needed when a free
   frame exists.
5. **A clean victim needs no write-back.**
6. **FIFO uses arrival time, LRU uses last-reference time, OPT uses next-reference time.** Mixing
   these up is the most common mistake.
7. **OPT cannot be implemented** — it needs the future. It is the lower bound.
8. **Belady's anomaly applies to FIFO**, not to LRU/OPT. More frames can mean more faults.
9. **Inclusion property** = n-frame resident set ⊆ (n+1)-frame resident set.
10. **Second chance worst case = FIFO** (all reference bits set); best case = LRU.
11. **Fixed allocation ⇒ local replacement.** Global replacement necessarily changes frame counts, so
    it conflicts with a fixed quota.
12. **Global replacement makes performance non-deterministic** — it depends on other processes.
13. **Thrashing is caused by too few frames per process**, not by a slow disk. Adding processes makes
    it worse.
14. **Working set ≠ all pages of the process.** It is only the pages in the last Δ references.
15. **D > m means thrashing**, where D is the sum of all working-set sizes and m is the total frames.
16. **PFF acts on the fault rate, the working-set model acts on the page set.** Know which is which.

---

## 3. Known slips / unclear points in the lectures

| Where | What was said | Correct version |
|---|---|---|
| 04 @ 03:07 | "if the OS replaced a page that belongs to another process, then the total number of frames assigned to the process will now be a constant, will now be fixed" | It is the opposite: replacing another process's page means the count **is no longer constant**. The very next sentence, on variable allocation, says so. |
| 02 @ 11:47 (OPT) | "we don't have any information about pages 1, 2, 3, so we use first-in-first-out to break the tie" | Correct, but note this is a **tie-break convention**, not part of the OPT definition. Any consistent rule gives the same fault count here. |
| 03 @ 02:57 | "inclusion property says, the pages that's currently in the memory when using n frames n plus 1 frames" | The property is: the resident set with **n** frames is a **subset** of the resident set with **n+1** frames. |
| 02 @ 07:23 | FIFO example narration calls each fault "page four" | ASR for "page fault" — do not confuse with page number 4. See the glossary. |
| 04 @ 00:00 | "we look at the **free modification**" | **frame allocation**. |

No arithmetic errors were found in these five recordings (unlike the `c89` batch): the fault counts
(10 / 6 / 8 / 8), the Belady figures (9 vs 10) and the working-set example all check out by hand.

---

## 4. Slide numbering is section-based

All recordings use the same **SC2005/CE2005/CZ2005 Operating Systems** deck, but slides are numbered
per section, and this batch crosses a section boundary:

| Content | Slide numbers seen |
|---|---|
| Demand paging / performance | 7.12 |
| FIFO example | 7.19 |
| Global vs local allocation | 7.29 |
| Working-set model | 8.8 |

So slide numbers do not run continuously across the five videos. Use the transcript timestamps.

---

## 5. Coverage map (what to watch when)

| Topic | Part | Timestamp |
|---|---|---|
| Why virtual memory; roadmap of the series | 01 | 00:00 – 01:07 |
| Swapping; backing store; costs | 01 | 01:07 – 03:14 |
| Swap-in/out implications; three schedulers | 01 | 03:14 – 07:28 |
| Program size limit; objective of VM | 01 | 07:28 – 08:21 |
| Locality argument; backing store as extension | 01 | 08:21 – 13:12 |
| Paging in/out vs swapping | 01 | 13:12 – 14:18 |
| Demand paging; valid–invalid bit | 01 | 14:18 – 17:16 |
| Page fault and page-fault handling | 01 | 17:16 – 23:12 |
| EAT formula and overheads | 01 | 23:12 – 27:20 |
| Fault with full memory; victim procedure | 02 | 00:00 – 03:46 |
| Dirty / modified bit | 02 | 03:46 – 05:27 |
| Objective; page reference string | 02 | 05:27 – 07:05 |
| FIFO (10 faults) | 02 | 07:05 – 09:35 |
| Optimal (6 faults) | 02 | 09:35 – 14:29 |
| LRU (8 faults) | 02 | 14:29 – 18:15 |
| Implementation cost; reference bit | 02 | 18:15 – 21:01 |
| Second chance / clock algorithm (8 faults) | 02 | 21:01 – 30:22 |
| Belady's anomaly (9 vs 10) | 03 | 00:00 – 02:57 |
| Inclusion property; OPT and LRU proofs | 03 | 02:57 – 05:32 |
| Frame allocation: fixed/variable, equal/proportional | 04 | 00:00 – 03:07 |
| Replacement scope: global/local + example | 04 | 03:55 – 10:26 |
| Combining allocation with scope | 04 | 10:26 – 14:39 |
| Thrashing: mechanism and CPU curve | 05 | 00:00 – 03:03 |
| Locality: temporal and spatial | 05 | 04:05 – 08:31 |
| Working-set model, Δ, WSS, D > m | 05 | 09:38 – 14:30 |
| Page-fault-frequency scheme | 05 | 14:30 – 15:34 |
| Summary | 05 | 15:34 – 16:43 |

---

## 6. Memory hooks

* **FIFO = first in, first out (arrival). LRU = least recently used (past). OPT = optimal (future).**
  One word each: *arrival / past / future*.
* **"Second chance" is FIFO with a lawyer** — it pleads the reference bit to avoid eviction.
* **Clock = FIFO arranged in a circle**; the hand is the "oldest" pointer.
* **Belady = "more memory, more faults"** — only FIFO among the four.
* **Inclusion property = the small set is inside the big set**; if true, adding frames can only help.
* **Thrashing = the system is doing the paging, not the program.**
* **Working set = the pages you touched recently**, not every page you own.
* **PFF = watch the fault rate, not the page set.**

---

## 7. ASR correction glossary

The `.srt` files are verbatim; the `.txt` files apply the substitutions below.

| In the transcript | Actual term |
|---|---|
| page full / page force / page for handling / page forward | **page fault / page faults / page-fault handling / page fault** |
| page for read / page for frequency | **page-fault rate / page-fault frequency** |
| belated anomaly | **Belady's anomaly** |
| 5-4, five form, five algorithm | **FIFO** |
| rru, arial, LRO | **LRU** |
| cloud hand | **clock hand** |
| reference speed | **reference bit** |
| weekly page / waiting page / audience page | **victim page / victim page / oldest page** |
| working side / working site | **working set** |
| threshing / stretching / subtraction | **thrashing** |
| special locality | **spatial locality** |
| OIs / ORS / old eyes | **OS** |
| preset / preset image / precise image | **process / process image** |
| person | **process** |
| backing stop / back-in store / back-end store / backing style / backing star | **backing store** |
| contact switch | **context switch** |
| disk ILO | **disk I/O** |
| assessment | **access** |
| logic address | **logical address** |
| free modification (04 @ 00:00) | **frame allocation** |
| street possesses (04 @ 05:44) | **three processes** |
| "page four" (part 02) | often **page fault**, but sometimes literally page number 4 — left as-is in the text |

---

## 8. Quick self-check before the exam

- [ ] Can you explain why virtual memory needs **dynamic** address translation?
- [ ] Can you draw the PTE with the valid bit and say what the entry holds in each state?
- [ ] Can you list the page-fault handling steps from trap to restart?
- [ ] Can you write and interpret the EAT formula?
- [ ] Can you run FIFO, OPT and LRU over `1 2 3 4 1 2 5 1 2 3 4 5` with 4 frames and get 10 / 6 / 8?
- [ ] Can you explain the clock algorithm and its worst case?
- [ ] Can you state Belady's anomaly and the inclusion property, and say which algorithms obey it?
- [ ] Can you fill in the allocation × scope combination table?
- [ ] Can you define WSS, D, m and the thrashing condition?
- [ ] Can you describe the PFF scheme step by step?
