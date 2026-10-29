# c12 — I/O System & Disk (lecture notes + tutorial)

Transcription and study material for the chapter the course deck calls **"Part 10: I/O System &
Disk"**: I/O hardware and the kernel's I/O structure, blocking vs asynchronous I/O and buffering,
disk geometry and access-time arithmetic, the five disk-scheduling algorithms, disk management, and
reliability through striping / mirroring / RAID. Plus **Tutorial 12**, which is examined I/O
scheduling.

This is the chapter that [`../c11`](../c11) (file systems) points forward to. `c11` ends at
*"which block does byte *x* live in?"* — `c12` asks *"how expensive is it to actually fetch that
block, and in what order should we fetch the queued ones?"*

**There is no video for c12.** The source material is two PDFs (a 46-slide deck and a one-page
tutorial). If you are looking for the four `LTI Launch*.mp4` files, they belong to
[`../c11`](../c11) and were already transcribed there.

## What is here

| File | What it is |
|---|---|
| [`STUDY_GUIDE.md`](STUDY_GUIDE.md) | Full teaching document: every concept, the disk-time derivations, all five scheduling traces line by line, RAID layouts, formula sheet, Tutorial 12 worked solutions, practice problems with solutions, self-test questions, glossary |
| [`SUMMARY.md`](SUMMARY.md) | One-page cheat sheet — the whole chapter in ~10 minutes |
| [`NOTES.md`](NOTES.md) | Emphasis list, exam traps, the deck's internal contradictions, coverage map S1–S46, answers to the two questions the slides leave open, memory hooks |
| [`transcripts/`](transcripts/) | Verbatim transcripts: the slide deck (S1–S46) and Tutorial 12 |

## Sources

| # | Source file | Extent | Content |
|---|---|---|---|
| 01 | `IO and Disk.pdf` | 46 slides | The complete chapter deck — S1–S46, footers `10.1`–`10.46` |
| 02 | `tut12.pdf` | 1 page | Tutorial 12 — I/O Systems: 4 questions (T/F on caching/scheduling/device drivers; the read-process loop; a SCAN question that turns out not to need SCAN; SSTF with arrival times) |

Citations in this folder are **slide numbers** (`S17`), because there is no audio to time-stamp.
Where a slide's printed footer disagrees with its position in the deck, the transcript records both.

## Order of the material

There is only one deck, so order is not in question — but the deck itself has a clear three-act
structure, and the middle act is the examined one:

| Act | Slides | Topic | Weight |
|---|---|---|---|
| I | S1–S12 | **I/O systems**: hardware, kernel structure, services, performance | definitional; expect short-answer |
| II | S13–S37 | **Disks**: geometry, access time, **scheduling** | *the core* — expect a calculation |
| III | S38–S46 | **Disk management and RAID** | factual; RAID 0+1 vs 1+0 is the sharp edge |

## Suggested study path

1. Read [`SUMMARY.md`](SUMMARY.md) once for the shape of the chapter.
2. Work through [`STUDY_GUIDE.md`](STUDY_GUIDE.md) §6–§7 and **re-derive 14 ms / 112 ms / 3.59 s /
   28.7 s** yourself. Every later number depends on those four.
3. Redo the five scheduling traces (§8.3) from the raw queue with the slide closed. The rule is
   always the same: *list the service order, then sum the absolute differences including the final
   leg.* If your total is 640, 236, 236, 382 or 322, you have all five.
4. Do Tutorial 12 (§12) **timed**, then the practice problems in §13.
5. Read [`NOTES.md`](NOTES.md) the night before — it is the trap list, not new material.

## Relationship to the rest of `lectures/`

| Folder | Topic | Ends by announcing |
|---|---|---|
| [`../c89`](../c89) | Memory organization | virtual memory |
| [`../c910`](../c910) | Virtual memory | file systems and disk scheduling |
| [`../c11`](../c11) | File systems (allocation, inodes, free space) | *"disk scheduling, I/O systems, RAID — not covered"* |
| `c12` (this folder) | I/O systems, disks, scheduling, RAID | the last topic in this sequence |
| [`../slides`](../slides) | Original slide decks | — |

Two links across the folder boundaries are worth keeping in mind:

* **S37** (file allocation determines the request pattern) is the direct bridge back to `c11`:
  **contiguous** allocation produces short seeks, **linked** and **indexed** produce long ones. This
  is Tutorial 12 Q2(b).
* The **layered kernel I/O structure** (S5) explains the two bottom layers `c11` named but skipped —
  **basic file system** and **I/O control (device driver, interrupts)**.
