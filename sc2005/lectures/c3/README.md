# c3 — CPU Scheduling (process scheduling, L3)

Study material for **lecture 3** of SC2005 Operating Systems: how the OS decides *which* ready
process gets a CPU core, and what that decision costs in waiting time.

This is the calculation lecture. Two thirds of the marks in this chapter come from drawing a Gantt
chart and getting the average right, so the study guide reproduces every worked example in the deck
step by step.

## What is here

| File | What it is |
|---|---|
| [`STUDY_GUIDE.md`](STUDY_GUIDE.md) | Full teaching document: every concept on the slides, every worked example rebuilt slice by slice, comparison tables, practice problems with solutions, self-test questions |
| [`SUMMARY.md`](SUMMARY.md) | One-page cheat sheet — algorithms, formulas, and the deck's actual answers in ~10 minutes |
| [`NOTES.md`](NOTES.md) | Before-the-exam file: what is stressed, exam traps, known slips in the slides, coverage map, memory hooks |
| [`transcripts/01-cpu-scheduling-slides.md`](transcripts/01-cpu-scheduling-slides.md) | Verbatim slide text of the whole deck, including the `[NOTES]` speaker notes |

## The source deck

`Part3 (CPU Scheduling).pptx` — **30 slides**, no audio recording. There is nothing to transcribe, so
every citation in these files is a **slide number**: `S14` means slide 14 of this deck.

The slides carry a lot of content in the **speaker notes** — tie-breaking rules, the Linux priority
range, the answer to "which transitions *must* schedule", the FCFS turnaround figure for S21. Those
notes are treated as lecture content and are quoted or paraphrased throughout.

One caveat about the extracted text: the Gantt-chart labels come out of the `.pptx` as a loose pile
of numbers and process names with no positions. Every chart in the study guide has therefore been
**rebuilt from the arrival/burst data and then cross-checked against the average the slide prints**.
Where the reconstruction matches the printed average, it is safe; that check is shown in the guide.

## Deck outline

| Section | Slides | What it covers |
|---|---|---|
| Course overview | S01 | Where L3 sits in the module |
| Chapter outline | S02 | Basic concepts → criteria → algorithms (uni, then multi) |
| Basic concepts | S03–S06 | CPU–I/O bursts, CPU scheduler, state transitions, preemptive vs nonpreemptive |
| Scheduling criteria | S07–S09 | CPU utilisation, throughput; turnaround, waiting, response time |
| Uniprocessor algorithms — setup | S10 | The five algorithms and the simplifying assumptions |
| FCFS | S11–S13 | Two worked examples, convoy effect |
| SJF / SRTF | S14–S16 | Definition, nonpreemptive worked example, preemptive worked example, optimality |
| Priority scheduling | S17 | Priorities, starvation, aging |
| Round robin | S18–S19 | Quantum, properties, worked `q = 20` example |
| Quantum trade-offs | S20–S21 | Context-switch overhead; turnaround vs quantum |
| Multilevel queue | S22–S23 | Foreground/background queues, fixed priority vs time slice |
| Multiprocessor scheduling | S24–S26 | Partitioned (AMP) vs global (SMP); mapping is NP-hard |
| SMP worked examples | S27–S29 | Global scheduling, dual-core SRTF, dual-core RR |
| SMP issues | S30 | Clock synchronisation, selection overhead, cache migration |

## CPU scheduling is *not* disk scheduling

Two different chapters in this course use the words "FCFS" and "scheduling":

| | CPU scheduling (this folder, L3) | Disk scheduling ([c12](../c12), L12) |
|---|---|---|
| What is being ordered | **processes/threads** waiting for a **CPU core** | **I/O requests** waiting for the **disk head** |
| Service time of a "job" | its **CPU burst**, given | seek + rotational latency, computed from cylinder numbers |
| The classic algorithms | FCFS, SJF/SRTF, priority, RR, multilevel queue | FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK |
| The metric | turnaround / waiting / response **time in ms** | total **head movement in cylinders** |
| Preemption | possible (RR, SRTF) | not meaningful — the head is where it is |

Only FCFS is common to both. If a question talks about **cylinders**, **seek time** or **head
movement**, it is disk scheduling — go to [`../c12`](../c12).

## Suggested study path

1. Read [`SUMMARY.md`](SUMMARY.md) once for the shape of the chapter.
2. Work [`STUDY_GUIDE.md`](STUDY_GUIDE.md) §1–§2, then **re-draw every Gantt chart on paper before
   reading the next one**. The deck's own advice (S11 notes): *"In the exam, I encourage you to draw
   the Gantt chart to help your calculation."*
3. Do §10 (practice problems) closed-book. The solutions show the slice-by-slice bookkeeping.
4. Answer the §11 self-test questions out loud — they are the "explain" marks.
5. Read [`NOTES.md`](NOTES.md) the night before. It contains no new material, only traps.

## Sibling folders

| Folder | Topic | Lecture |
|---|---|---|
| [c1](../c1) | Introduction & background | L1 |
| [c2](../c2) | Processes & threads | L2 (+ threads) |
| [c3](../c3) | CPU scheduling | L3 **(this folder)** |
| [c5](../c5) | Synchronization | L5–6 |
| [c7](../c7) | Deadlocks | L7 |
| [c8](../c8) | Memory organization | L8 |
| [c9](../c9) | Virtual memory | L9–10 |
| [c11](../c11) | File systems | L11 |
| [c12](../c12) | I/O system & disk | L12 |
| [c6a](../c6a) | Real-time OS | Part 6a |
| [Virtualisation Part 1](</Users/bryangoh/Work/shtudy/sc2005/lectures/2026-10-02 SC2005 - Virtualisation (Part 1).md>) | Virtualization overview | Part 6b |

The deck's own course-overview slide (S01) places this lecture as `Scheduling (L3)`, between
`Processes (L2)` and `Synchronization (L5-6)` — the ready queue this chapter schedules is the one
built in L2, and the locks that make a shared ready queue safe are L5–6.
