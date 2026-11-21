# SC2005 — Lectures

Study material for SC2005 Operating Systems, one folder per topic in lecture order. Every topic
folder follows the same four-file shape plus a verbatim source transcript:

| File | What it is |
|---|---|
| `STUDY_GUIDE.md` | Full teaching document: every concept, derivations, worked examples, practice problems with solutions, self-test questions |
| `SUMMARY.md` | One-page cheat sheet — the whole topic in ~10 minutes of reading |
| `NOTES.md` | The "before the exam" file: lecturer emphasis, exam traps, known slips in the slides, coverage map, memory hooks |
| `README.md` | What the folder is, where the source came from, and how it connects to its neighbours |
| `transcripts/` | The source material, verbatim — audio transcripts (`.srt` + normalised `.txt`) where a recording exists, otherwise a slide-by-slide markdown dump |

## The course, in lecture order

The numbering below follows the `Course Overview` slide printed in the Part 2 and Part 4 decks.

| Lecture | Topic | Folder | Source |
|---|---|---|---|
| L1 | Introduction & background | [`c1`](c1) | `Part1 (Intro and Background).pptx` — 46 slides |
| L2 (+ threads) | Processes & threads | [`c2`](c2) | `Part2 (Process and Threads).pptx` — 40 slides |
| L3 | CPU scheduling | [`c3`](c3) | `Part3 (CPU Scheduling).pptx` — 30 slides |
| L5–6 | Synchronization | [`c5`](c5) | `Part4 (Synchronization).pptx` — 54 slides |
| L7 | Deadlocks | [`c7`](c7) | `Part5 (Deadlocks).pptx` — 45 slides |
| L8 | Memory organization | [`c8`](c8) | `Memory Organization.pdf` — 5 recordings, 1 h 56 min |
| L9–10 | Virtual memory | [`c9`](c9) | `Virtual Memory.pdf` — 5 recordings, 1 h 36 min |
| L11 | File systems | [`c11`](c11) | `File Systems.pdf` — 4 recordings, 1 h 41 min |
| L12 | I/O system & disk | [`c12`](c12) | `IO and Disk.pdf` — 46 slides |
| Part 6a | Real-time OS | [`c6a`](c6a) | `Part6a (RTOS).pptx` — 19 slides |
| Part 6b | Virtualization | see below | `Part6b (Virtualization).pptx` — 31 slides |

Threads are not numbered on the overview slide; by elimination they occupy the gap between
scheduling (L3) and synchronization (L5). The Part 5 and Part 6a decks still print an older
`Synchronization (L4-5) / Deadlocks (L6)` scheme — where they disagree with Part 2 and Part 4, the
newer numbering wins, and the folder names follow it.

## Virtualization is not a folder

Part 6b is the one topic captured as a live lecture rather than derived from a deck, so its material
sits directly in this directory as two files:

- [Virtualisation (Part 1)](<2026-10-02 SC2005 - Virtualisation (Part 1).md>) — the deck walkthrough:
  emulation vs virtualisation, the three mechanisms, vCPUs as processes, the layered model, limited
  direct execution.
- [Virtualisation wrap-up + agent harness (Part 2)](<2026-10-02 SC2005 - Virtualisation wrap-up + agent harness (Part 2).md>)
  — the worked finish, a non-examinable aside, and the lab walkthrough.

## Not covered here

Week 13 is a guest lecture with no examinable material and is deliberately excluded.

This directory is study material, not an archive: the original `.pptx` / `.pdf` decks are **not**
stored here. Each folder's `README.md` names its source deck and, where one exists, the recording
order and runtime.

## Suggested reading order for revision

Read the `SUMMARY.md` of every folder in the table above — that is the whole module in about two
hours. Then work backwards: `STUDY_GUIDE.md` for whichever topics your practice papers keep
missing, and `NOTES.md` for all of them the night before.
