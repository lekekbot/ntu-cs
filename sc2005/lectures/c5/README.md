# c5 — Process Synchronization (lecture L5–6)

Study material for the **Synchronization** chapter of SC2005: race conditions, the critical-section
problem, user-level solutions, atomic hardware instructions, semaphores, the three classical
synchronisation problems, and a one-slide look at monitors.

**Source deck:** `Part4 (Synchronization).pptx` — **54 slides**. This is the largest deck in the
course, and the one the deck itself labels *"Important but difficult"* (`S02`).

**No audio, no video.** There is no recording for this deck, so **every citation in this folder is a
slide number**: `S17` means slide 17 of the deck. The transcripts folder holds the slide text
verbatim, including the lecturer's `[NOTES]` speaker notes, which carry real content (see
[NOTES.md §6](NOTES.md#6-content-that-exists-only-in-the-speaker-notes)).

## What is here

| File | What it is |
|---|---|
| [`STUDY_GUIDE.md`](STUDY_GUIDE.md) | Full teaching document: every concept on every slide, with the register-level interleavings, property tables, all code verbatim, practice problems with solutions, self-test questions and a glossary |
| [`SUMMARY.md`](SUMMARY.md) | One-page cheat sheet — the whole deck in ~10 minutes |
| [`NOTES.md`](NOTES.md) | Before-the-exam file: lecturer emphasis, exam traps, known slips in the slides, coverage map, memory hooks, self-check |
| [`transcripts/01-synchronization-slides.md`](transcripts/01-synchronization-slides.md) | The deck's text **verbatim**, slide by slide, with `[NOTES]` marking the speaker notes |

## The deck's structure

| Slides | Section | What it establishes |
|---|---|---|
| S01–S03 | **Course overview · Background** | Where this chapter sits (L5–6); shared data + context switches ⇒ **data inconsistency**; we need causal ordering |
| S04–S09 | **Race condition** (bounded buffer) | The producer-consumer example; `counter++`/`counter--` expanded to three instructions each; the `counter = 5` interleaving that ends at 4 |
| S10–S14 | **Critical-section problem** | Definition; the entry/critical/exit/remainder skeleton; **mutual exclusion**, **progress**, **bounded waiting** |
| S15–S21 | **User-level solutions** | Algorithm 1 (`turn`), Algorithm 2 (`flag[]`), Algorithm 3 (Peterson) — each with its property analysis; the conclusion that software solutions do not scale |
| S22–S27 | **OS-level solutions: synchronization hardware** | Atomicity; `TestAndSet`; the `mutex` lock; ME and progress hold; the **bounded-waiting failure** trace under round-robin |
| S28–S36 | **Semaphores** | `Wait`/`Signal`; counting vs binary; the `mutex` idiom; the **busy-waiting** implementation and why `Wait` must be atomic; the **blocking** implementation (`value`, `L`, `block()`, `wakeup()`), the negative-value accounting, and why the decrement precedes `block()` |
| S37–S41 | **Using semaphores (and misusing them)** | The three-step method (shared variable vs shared resource); semaphores as an ordering tool; **deadlock** and **starvation** from misuse |
| S42–S53 | **Classical problems** | Bounded buffer (`mutex`/`empty`/`full`, and the deadlock if the `Wait`s are swapped); dining philosophers (`chopstick[5]`, the deadlock, three remedies); readers-writers (`readcount`/`mutex`/`wrt`) |
| S54 | **Monitors** | High-level construct, one process active at a time — the slide is marked *"not examinable"* |

Two things to know before you start:

* **Deadlock here is only semaphore misuse.** `S40`–`S41` give the two-process circular-wait example
  and the starvation definition. The real chapter — four necessary conditions, prevention,
  avoidance, detection, recovery — is [`../c7`](../c7).
* **Monitors are one slide, banner-marked not examinable.** Read it for orientation, not for marks.

## Suggested study path

1. Read [`SUMMARY.md`](SUMMARY.md) once for the shape of the chapter: race condition → three
   properties → five solutions → three classical problems.
2. Work through [`STUDY_GUIDE.md`](STUDY_GUIDE.md) §2–§4 in order. Do not skip the `counter = 5`
   interleaving (§2.3) or the three algorithm analyses (§4) — everything later is the same argument
   with better tools.
3. Then §6–§9, the hardware and semaphore machinery. Reproduce the `S27` bounded-waiting trace on
   paper, and write both semaphore implementations from memory.
4. Then §12, the three classical problems. Be able to write the bounded-buffer and readers-writers
   solutions without notes, and to show both deadlocks (swapped `Wait`s; five philosophers).
5. Do the practice problems in §15 with the solutions covered, then the self-test in §16.
6. Read [`NOTES.md`](NOTES.md) the night before — it is the trap list, not new material.

## Relationship to the rest of `lectures/`

This chapter assumes [`../c2`](../c2) (concurrent processes and context switching) and
[`../c3`](../c3) (a preemptive scheduler that can switch at any instruction — the `S27` trace is
literally a round-robin simulation). It is the prerequisite for [`../c7`](../c7) (deadlocks), which
takes the `S40` circular-wait example and turns it into a full chapter.

| Folder | Topic | Lecture |
|---|---|---|
| [c1](../c1) | Introduction & background | L1 |
| [c2](../c2) | Processes & threads | L2 (+ threads) |
| [c3](../c3) | CPU scheduling | L3 |
| [c5](../c5) | Synchronization | L5–6 **(this folder)** |
| [c7](../c7) | Deadlocks | L7 |
| [c8](../c8) | Memory organization | L8 |
| [c9](../c9) | Virtual memory | L9–10 |
| [c11](../c11) | File systems | L11 |
| [c12](../c12) | I/O system & disk | L12 |
| [c6a](../c6a) | Real-time OS | Part 6a |
| [Virtualisation Part 1](</Users/bryangoh/Work/shtudy/sc2005/lectures/2026-10-02 SC2005 - Virtualisation (Part 1).md>) | Virtualization overview | Part 6b |

Note: the course overview slide in this deck numbers the chapter **`Synchronization (L5-6)`** with
`Deadlocks (L7)`; the Part 5 and Part 6a decks still print the older `Synchronization (L4-5)` /
`Deadlocks (L6)` scheme. Same material, renumbered.
