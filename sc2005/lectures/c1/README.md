# c1 — Introduction & Background (lecture 1)

Study material for **lecture 1** of SC2005 Operating Systems: what an operating system is, the types
of computing system, a review of computer-system architecture (interrupts, DMA, dual-mode operation,
memory protection), and operating-system services and system calls.

This is the first chapter of the course. Every later folder in `lectures/` is one of the four
questions this deck asks, made concrete.

## What is here

| File | What it is |
|---|---|
| [`STUDY_GUIDE.md`](STUDY_GUIDE.md) | Full teaching document: every concept on the slides, explained and derived, with comparison tables, the worked memory-protection example, practice problems with solutions and self-test questions |
| [`SUMMARY.md`](SUMMARY.md) | One-page cheat sheet — the whole deck in ~10 minutes |
| [`NOTES.md`](NOTES.md) | Emphasis list, exam traps, known slips and contradictions in the deck, coverage map S01–S46, memory hooks |
| [`transcripts/`](transcripts/) | Verbatim slide text, S1–S46, including the speaker notes |

## Source

| # | Source file | Extent | Content |
|---|---|---|---|
| 01 | `Part1 (Intro and Background)(1).pptx` | 46 slides | The complete Part 1 deck: S01–S46, with full text, tables and speaker notes |

**There is no audio for this lecture.** Slide text was extracted directly, so citations in this
folder are **slide numbers** — `S17` means slide 17 of the 46. Speaker notes (lines beginning
`[NOTES]` in the transcript) carry lecturer annotations and tie-breaking rules, and are treated as
content, not commentary.

Footers on S43/S44 read `CE2005/CZ2005 Operating Systems` — the same course under its older code.
See [NOTES.md](NOTES.md) §3.

## Structure of the deck

The deck prints the same four-item outline on **S01, S07, S20 and S39**, and those four slides are
its act dividers:

| Act | Slides | Section | Topic | Weight |
|---|---|---|---|---|
| I | S01–S06 | *Introduction* | Why learn OSes, the definition and its two goals, the four system components, the three definitions (resource allocator / control program / kernel) | definitional |
| II | S08–S19 | *Types of Computing Systems* | Batch → multiprogramming → time-sharing → desktop → embedded/CPS → real-time → handheld → multiprocessor | definitional + one comparison question |
| III | S21–S38 | *Computer System Architecture (Review)* | System operation and the bus (S22–S23), **interrupts** (S24–S25), the I/O timeline (S26), **DMA** (S27–S28), storage hierarchy (S29–S30, **not examinable**), **hardware protection**: dual mode, I/O, base/limit (S31–S38) | *the core* — expect the arithmetic |
| IV | S39–S44 | *Operating System Services* | The services figure (S40), **system calls** (S41), API → system call → OS (S42), and the trap/interrupt pair (S43–S44) | *the core* — expect the four-step diagrams |
| V | S45–S46 | — | Advanced readings, future operating systems | trivia |

Two slides carry the printed line **"This slide is not examinable."** — S29 and S30, the storage
hierarchy. They are flagged here, in `SUMMARY.md` and in `NOTES.md`, and are included in the study
guide only so that nothing is a surprise.

## Suggested study path

1. Read [`SUMMARY.md`](SUMMARY.md) once for the shape of the chapter.
2. Work through [`STUDY_GUIDE.md`](STUDY_GUIDE.md) §1–§3 quickly (definitions), then slowly through
   §4, §6 and §8 — the three "core" blocks.
3. Re-derive the base/limit range from S37 (`300 040 + 120 900 = 420 940`) and test one address on
   each side of the boundary. That single exercise covers the most likely calculation in the paper.
4. Do the practice problems in §12 with the slides closed, then the self-test questions in §13.
5. Read [`NOTES.md`](NOTES.md) the night before — it is the trap list, not new material. The mode-bit
   polarity (0 = monitor, 1 = user) and the trap/interrupt distinction are the two most commonly
   lost marks.

## Relationship to the rest of `lectures/`

| Folder | Topic | Lecture |
|---|---|---|
| [c1](../c1) | Introduction & background | L1 **(this folder)** |
| [c2](../c2) | Processes & threads | L2 (+ threads) |
| [c3](../c3) | CPU scheduling | L3 |
| [c5](../c5) | Synchronization | L5–6 |
| [c7](../c7) | Deadlocks | L7 |
| [c8](../c8) | Memory organization | L8 |
| [c9](../c9) | Virtual memory | L9–10 |
| [c11](../c11) | File systems | L11 |
| [c12](../c12) | I/O system & disk | L12 |
| [c6a](../c6a) | Real-time OS | Part 6a |
| [Virtualisation Part 1](</Users/bryangoh/Work/shtudy/sc2005/lectures/2026-10-02 SC2005 - Virtualisation (Part 1).md>) | Virtualization overview | Part 6b |

Three links in this chapter point forward and are worth recognising when they appear:

* **S12** names the three features multiprogramming forces — memory management, CPU scheduling, I/O
  device scheduling — which are the subjects of `c8`/`c9`, `c3` and `c12` respectively.
* **S25** says interrupt handling is "also called a context switch", and defers the details to the
  processes lecture: that is `c2`.
* **S16** points at the week-7 e-learning lecture for example real-time OSes; the course folder for
  that material is `c6a`.
