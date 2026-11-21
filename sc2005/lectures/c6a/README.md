# c6a — Real-Time OS (Part 6a slide deck)

Study material for **Part 6a of the SC2005 special topic**: real-time operating systems. What a
cyber-physical system demands from an OS, how a real-time process is *specified*, and the two
scheduling algorithms the course teaches for it — **Rate Monotonic** (fixed priority) and
**Earliest Deadline First** (dynamic priority).

This folder is built from a **slide deck, not a recording**. There is no audio for Part 6a, so
everything here cites **slide numbers** (`S17`), not timestamps.

## What is here

| File | What it is |
|---|---|
| [`STUDY_GUIDE.md`](STUDY_GUIDE.md) | Full teaching document: every concept on all 19 slides, the S13/S14/S17/S18 process sets worked out as timelines, an RM-vs-EDF comparison, practice problems with solutions, self-test questions |
| [`SUMMARY.md`](SUMMARY.md) | One-page cheat sheet — the whole deck in ~5 minutes |
| [`NOTES.md`](NOTES.md) | Before-the-exam file: lecturer emphasis, exam traps, slide slips and numbering inconsistencies in the deck, coverage map, memory hooks |
| [`transcripts/01-rtos-slides.md`](transcripts/01-rtos-slides.md) | Verbatim slide text, S01–S19, with the speaker notes marked `[NOTES]` |

## The source deck

`Part6a (RTOS).pptx` — **19 slides**, the shortest deck in the course. No lecture recording exists,
so the notes above are the only "lecturer voice" available, and this folder quotes them instead of
timestamps.

The deck's own S02 divides it into three questions:

1. What is a Real-Time OS?
2. Real-Time Process Specification
3. Real-Time CPU Scheduling

S12 repeats that outline with the scheduling half expanded into **fixed-priority** and
**dynamic-priority** scheduling.

## Structure of the deck

| Slides | Topic |
|---|---|
| S01 | Course overview — where the "special" topic sits among CPU, memory, filesystem, I/O and synchronization |
| S02 | Part 6a outline: what is an RTOS → process specification → real-time CPU scheduling |
| S03 – S05 | **What an RTOS is, part 1** — cyber-physical systems (S03), why real-time is the common requirement (S04), what a "reasonable time" depends on (S05) |
| S06 – S07 | **What an RTOS is, part 2** — "real-time ≠ fast, real-time = predictable" (S06), the definition of a real-time system and of an RTOS (S07) |
| S08 | Repeats the part outline — but with the wrong part number |
| S09 – S11 | **Real-time process specification** — `<R,C,D>` (S09), recurrent processes (S10), periodic processes `<T,C,D>` (S11) |
| S12 – S13 | **Why classic CPU scheduling fails** — the scheduling section outline (S12), FCFS/SJF/RR against deadlines (S13) |
| S14 | **The real-time scheduling problem** stated, with the running periodic example |
| S15 – S17 | **Fixed-priority scheduling** — what "fixed" means (S15), Rate Monotonic (S16), and RM failing to prioritise the urgent process (S17) |
| S18 – S19 | **Dynamic-priority scheduling** — Earliest Deadline First (S18), RM vs EDF trade-off (S19) |

## Suggested study path

1. Read [`SUMMARY.md`](SUMMARY.md) once to get the shape of the deck — it is 19 slides, so this
   really is the whole thing.
2. Work through [`STUDY_GUIDE.md`](STUDY_GUIDE.md) §1–§7 with the slide text open beside it
   ([`transcripts/01-rtos-slides.md`](transcripts/01-rtos-slides.md)), drawing each timeline by hand
   before reading the one in the guide. The deck's Gantt figures come out of a shape-based text
   extractor in scrambled order, so the guide **rebuilds** them — do the same, then compare.
3. Do the practice problems in §10 without looking at the solutions.
4. Read [`NOTES.md`](NOTES.md) the night before — it is the trap list, not new material.

## Relationship to the virtualisation material

SC2005 groups these two subjects into one **"special" topic** (S01 calls it *Special: Real-time OS &
virtualization*, and the deck's S02 speaker note slips into virtualisation at the end). They are
taught as **Part 6a** (RTOS) and **Part 6b** (virtualisation), but there is no `c6b` folder: the
virtualisation material lives as two loose markdown files **one level up**:

* [2026-10-02 SC2005 - Virtualisation (Part 1).md](</Users/bryangoh/Work/shtudy/sc2005/lectures/2026-10-02 SC2005 - Virtualisation (Part 1).md>) —
  virtualisation overview: why virtualise, the VMM/hypervisor, type 1 vs type 2, trap-and-emulate,
  binary translation, the CPU-scheduling ledger.
* `2026-10-02 SC2005 - Virtualisation wrap-up + agent harness (Part 2).md` — the same day's wrap-up
  recording.

**They are not a continuation of this deck.** RTOS is a *scheduling* topic; virtualisation is an
*abstraction/resource-multiplexing* topic. The deck simply stops after S19. Read this folder for the
scheduling half of "the special topic" and the two files above for the virtualisation half; the only
shared idea is that both ask the OS to give a **guarantee** (deadlines there, isolation here).

## Relationship to the rest of `lectures/`

| Folder | Topic | Lecture |
|---|---|---|
| [c1](../c1) | Introduction & background | L1 |
| [c2](../c2) | Processes & threads | L2 (+ threads) |
| [c3](../c3) | CPU scheduling | L3 |
| [c5](../c5) | Synchronization | L5–6 |
| [c7](../c7) | Deadlocks | L7 |
| [c8](../c8) | Memory organization | L8 |
| [c9](../c9) | Virtual memory | L9–10 |
| [c11](../c11) | File systems | L11 |
| [c12](../c12) | I/O system & disk | L12 |
| [c6a](../c6a) | Real-time OS | Part 6a **(this folder)** |
| [Virtualisation Part 1](</Users/bryangoh/Work/shtudy/sc2005/lectures/2026-10-02 SC2005 - Virtualisation (Part 1).md>) | Virtualization overview | Part 6b |

Two dependencies matter:

* **S12 says the real-time scheduler *is* "the short-term scheduler from Week 3".** Everything in
  §3 (why FCFS/SJF/RR fail) assumes you know those three algorithms and their metrics — that is
  [`../c3`](../c3). The deck's argument is precisely that **c3's metrics stop being the right ones**.
* **Fixed-priority scheduling can starve a process** — the vocabulary for "a process that is always
  outranked and never runs" is in [`../c7`](../c7). RM's S17 failure is the same shape of problem:
  the rule is correct-looking, yet one process cannot get the CPU when it needs it.

> **Honesty note.** The deck never states a Rate Monotonic **utilisation bound** (the Liu & Layland
> `n(2^(1/n) − 1)` result). It is outside this deck and not examinable in that form here — if you
> quote it, quote it as external knowledge, not as slide content.
