# c7 — Deadlocks (Part 5)

Study material for the chapter the course deck calls **"Part 5: Deadlocks and Starvation"**: what a
deadlock is, how to model it with a resource-allocation graph, the four conditions that must hold,
and the four ways a system can respond — prevention, avoidance (**Banker's algorithm**), detection
and recovery, or the ostrich approach that real operating systems actually use.

This is the chapter that [`../c5`](../c5) (synchronization) warns about: `c5` gives you
`wait()`/`signal()`, and this deck shows the first thing that goes wrong when you use them — two
semaphores acquired in opposite orders (S04).

## What is here

| File | What it is |
|---|---|
| [`STUDY_GUIDE.md`](STUDY_GUIDE.md) | Full teaching document: every slide, all three resource-allocation graphs, the four conditions, the dining-philosophers prevention walkthrough, and every matrix of the safety / resource-request / detection algorithms worked row by row, plus practice problems with solutions and a self-test |
| [`SUMMARY.md`](SUMMARY.md) | One-page cheat sheet — the whole chapter in ~10 minutes |
| [`NOTES.md`](NOTES.md) | Emphasis list, exam traps, the deck's stale lecture numbering and internal slips, coverage map S1–S45, memory hooks |
| [`transcripts/`](transcripts/) | Verbatim deck text, `[NOTES]` = speaker notes |

## The source deck

| | |
|---|---|
| File | `Part5 (Deadlocks).pptx` |
| Extent | **45 slides**, S01–S45 |
| Audio | **none** — this chapter was never recorded, so **citations are slide numbers** (`S17`), never timestamps |
| Speaker notes | present and used; they carry the explanations the bullet text leaves out (e.g. *"Why do most systems use Ostrich approach? Efficiency."*) |

Because there is no video, the deck *is* the lecture. That makes the speaker notes unusually
important: several slides are a bare list of bullets whose reasoning exists only in the notes
(S13 "basic facts", S30 "what if multiple answers", S37 "restore the old state").

## Structure of the deck

S01 is an administrative slide (SFT feedback) and S02 is the course overview; **six** of the
remaining slides (S03, S06, S14, S17, S23, S38) are the same outline slide repeated as a section
divider. The content is therefore ~36 slides in seven blocks:

| Block | Slides | Topic | Weight |
|---|---|---|---|
| I | S04–S05 | **The deadlock problem**: definition, the two-semaphore example, the bridge-crossing analogy | definitional |
| II | S07–S13 | **System model** and the **resource-allocation graph**, including the cycle-but-no-deadlock case | *the core idea* — expect a graph question |
| III | S15–S16 | The **four conditions** (mutual exclusion, hold-and-wait, no-preemption, circular-wait) | short-answer |
| IV | S18–S22 | **Handling strategies** and **prevention**, walked through on dining philosophers | *the core* — expect "how do you prevent X?" |
| V | S24–S37 | **Avoidance**: safe state, safe sequence, **Banker's safety and resource-request algorithms** | *the exam question* — expect a matrix |
| VI | S39–S44 | **Detection**: the multiple-instance algorithm and its worked example | **not examinable** (S39) |
| — | S45 | Advanced readings | — |

Block V is where the marks are: two full algorithm traces on a 5-process / 3-resource-type matrix,
with the answer sequences `<P1, P3, P4, P2, P0>` and `<P1, P3, P4, P0, P2>`.

## Suggested study path

1. Read [`SUMMARY.md`](SUMMARY.md) once for the shape of the chapter.
2. Work through [`STUDY_GUIDE.md`](STUDY_GUIDE.md) §3 (the three graphs) until you can say **why a
   cycle is not enough** when a resource type has several instances. That one sentence separates a
   correct answer from a half-correct one.
3. Re-derive the `Need` matrix on S31 from `Max − Allocation`, then run the **safety algorithm** on
   paper until you reach `<P1, P3, P4, P2, P0>`. Do it twice: once reading the guide, once with the
   slide closed.
4. Do the same for the **resource-request algorithm**: `Request1 = (1, 0, 2)` must be granted, and
   the *second* `(1, 0, 2)` must be refused at step 1. Then do the `(2, 3, 0)` request that the deck
   sets as homework (§8.10).
5. Do the practice problems in §12 without looking at the solutions.
6. Read [`NOTES.md`](NOTES.md) the night before — it is the trap list, not new material.

Detection (§9) is worth one read for contrast — it is the safety algorithm with `Request` swapped
for `Need` — but S39 says plainly that it is not examinable. Do not spend revision time on it.

## Relationship to the rest of `lectures/`

| Folder | Topic | Lecture |
|---|---|---|
| [c1](../c1) | Introduction & background | L1 |
| [c2](../c2) | Processes & threads | L2 (+ threads) |
| [c3](../c3) | CPU scheduling | L3 |
| [c5](../c5) | Synchronization | L5–6 |
| [c7](../c7) | Deadlocks | L7 **(this folder)** |
| [c8](../c8) | Memory organization | L8 |
| [c9](../c9) | Virtual memory | L9–10 |
| [c11](../c11) | File systems | L11 |
| [c12](../c12) | I/O system & disk | L12 |
| [c6a](../c6a) | Real-time OS | Part 6a |
| [Virtualisation Part 1](</Users/bryangoh/Work/shtudy/sc2005/lectures/2026-10-02 SC2005 - Virtualisation (Part 1).md>) | Virtualization overview | Part 6b |

Two links are worth keeping in mind:

* **S04's second example is `c5`'s example.** Two semaphores `A` and `B`, both initialised to 1,
  acquired in opposite orders. Everything in this chapter is a consequence of that pattern being
  possible.
* **The lecture numbering on this deck's own overview slide is one behind.** S02 prints
  `Synchronization (L4-5)` / `Deadlocks (L6)`, while the overview slides in Part 2 and Part 4 print
  `Synchronization (L5-6)` / `Deadlocks (L7)`. The folder is nevertheless `c7`, matching the newer
  scheme; see [`NOTES.md`](NOTES.md) §3.
