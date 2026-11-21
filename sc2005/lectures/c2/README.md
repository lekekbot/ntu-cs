# c2 — Processes & Threads (Part 2)

Study material for **Part 2: Processes and Threads** of SC2005 Operating Systems.

## Source

| | |
|---|---|
| Deck | `Part2 (Process and Threads).pptx` |
| Slides | **40** (S1–S40) |
| Audio | **none** — this deck has no recording |
| Citations | **slide numbers**, e.g. `S17`; there are no timestamps |
| Speaker notes | present, extracted as `[NOTES]` lines — they carry lecturer annotations and are treated as content |

Because there is no audio, every cross-reference in this folder is a slide number. A slide number
here is a *position in this deck*, not a section number shared with other decks.

## What is here

| File | What it is |
|---|---|
| [`STUDY_GUIDE.md`](STUDY_GUIDE.md) | Full teaching document: every concept on the slides, explained and derived, with the fork tree and producer/consumer code reproduced, comparison tables, practice problems and self-test questions |
| [`SUMMARY.md`](SUMMARY.md) | One-page cheat sheet — the whole deck in ~10 minutes of reading |
| [`NOTES.md`](NOTES.md) | Before the exam: what is repeatedly stressed, exam traps, known slips and contradictions in the slides, coverage map, memory hooks |
| [`transcripts/01-processes-and-threads-slides.md`](transcripts/01-processes-and-threads-slides.md) | Verbatim slide text with the speaker notes inline |

## The deck has two halves

| Half | Slides | Topic | Contents |
|---|---|---|---|
| **Processes** | S01–S28 | The process as the OS's unit of work | course overview · process concept and memory layout · process states · PCB · context switch · scheduling queues · the three schedulers · creation and termination (fork, wait/join, exit/abort) · cooperating processes · IPC models · message passing · producer–consumer |
| **Threads** | S29–S40 | The thread as the unit of CPU utilisation | thread components · single vs multithreaded process · benefits · multithreaded server · user vs kernel threads · many-to-one, one-to-one, many-to-many · readings |

### Slide-by-slide map

| Slides | Content |
|---|---|
| S01 | Course overview table — where this part sits in the module |
| S02 | Part 2 outline + review of the previous lecture (DMA, hardware protection) |
| S03 | Process = program in execution; job vs process |
| S04 | Process in memory — text / data / heap / stack between base and base+limit |
| S05 | The five process states |
| S06 | Process state transition diagram; timer interrupt |
| S07–S09 | PCB layout, PCB fields, PCBs in main memory (kernel vs user space) |
| S10 | Section divider (repeats the outline) |
| S11–S12 | Context switch: timer-driven example, definition, overhead |
| S13–S14 | Job / ready / device queues; queue headers, head and tail pointers |
| S15–S16 | Long-term, short-term, medium-term schedulers; invocation frequency; degree of multiprogramming |
| S17 | Section divider |
| S18–S19 | Process creation: fork, process tree, concurrent vs parent-waits, `wait()`/`join()` |
| S20 | Process termination: exit, abort, cascaded termination |
| S21 | Section divider |
| S22–S23 | Cooperating vs independent processes; the two IPC models |
| S24–S25 | Message passing: send/receive, link, direct vs indirect (mailboxes) |
| S26–S27 | Producer–consumer; unbounded vs bounded buffer; the bounded-buffer code |
| S28 | Section divider |
| S29 | Threads outline |
| S30 | What a thread is and what it shares; lightweight vs heavyweight process |
| S31 | Single-threaded vs multithreaded process (figure) |
| S32–S33 | Benefits of multithreading; the multithreaded server |
| S34 | The threading paradox; user threads vs kernel threads |
| S35–S39 | Multithreading models: many-to-one, one-to-one, many-to-many; why no one-to-many |
| S40 | Advanced readings (Beej's IPC guide, pthreads, Win32 threads) |

## Lecture numbering — read this before quoting a lecture number

S01 is a **course overview** slide. It labels the topics like this:

```
Processes (L2)          Scheduling (L3)         Synchronization (L5-6)
Deadlocks (L7)          Memory organization (L8)  Virtual memory (L9-10)
Filesystems (L11)       I/O & disk (L12)        Special: Real-time OS & virtualization
```

**Threads are not numbered on that slide.** They are part of this deck (S29–S40) but no lecture
number is printed for them anywhere in it. By elimination — L1 introduction, L2 processes, L3
scheduling, L5–6 synchronization — threads occupy **L4**. That is an inference, not a quotation;
the deck never states it.

Also note that other decks in this module still print an **older scheme**,
`Synchronization (L4-5)` / `Deadlocks (L6)`, which shifts everything after it. So a lecture number
is safe to use only together with the topic name.

## Suggested study path

1. Read [`SUMMARY.md`](SUMMARY.md) once to get the shape of the two halves.
2. Work through [`STUDY_GUIDE.md`](STUDY_GUIDE.md) section by section, keeping the deck open at the
   slide numbers it cites. The two code fragments (S18 fork tree, S27 bounded buffer) are worth
   reproducing by hand.
3. Do the practice problems in §9 without looking at the solutions; then answer the §10 self-test
   questions out loud.
4. Read [`NOTES.md`](NOTES.md) the night before — it is the trap list, not new material.

## Where this material continues

The deck deliberately stops at *naming* topics it does not teach:

| Named on the slides | Taught in |
|---|---|
| Process scheduling — S15/S16 describe the **schedulers** but teach **no algorithm** (FCFS, SJF, RR, priority, multilevel) | [`../c3`](../c3) CPU scheduling |
| Synchronization — S27's bounded buffer uses `wait` on "mailbox full/empty" without any mutual exclusion or condition variable | [`../c5`](../c5) Synchronization |
| Deadlock — named only in the S01 overview table | [`../c7`](../c7) Deadlocks |

## Relationship to the rest of `lectures/`

| Folder | Topic | Lecture |
|---|---|---|
| [c1](../c1) | Introduction & background | L1 |
| [c2](../c2) | Processes & threads | L2 (+ threads) **(this folder)** |
| [c3](../c3) | CPU scheduling | L3 |
| [c5](../c5) | Synchronization | L5–6 |
| [c7](../c7) | Deadlocks | L7 |
| [c8](../c8) | Memory organization | L8 |
| [c9](../c9) | Virtual memory | L9–10 |
| [c11](../c11) | File systems | L11 |
| [c12](../c12) | I/O system & disk | L12 |
| [c6a](../c6a) | Real-time OS | Part 6a |
| [Virtualisation Part 1](</Users/bryangoh/Work/shtudy/sc2005/lectures/2026-10-02 SC2005 - Virtualisation (Part 1).md>) | Virtualization overview | Part 6b |

This part is the base of everything else in the module: later parts say "process" and mean
**single-threaded** process (S29 notes state this explicitly). The base/limit registers first met on
S04 and S09 are the same pair used for memory protection in [`../c8`](../c8); the PCB fields first
met on S08 are what a context switch actually saves and restores.
