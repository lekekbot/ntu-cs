# c910 — Virtual Memory (lecture series)

Transcripts and study material for the five recordings covering **virtual memory**: swapping, demand
paging, page-fault handling, page replacement (FIFO/OPT/LRU/clock), Belady's anomaly, frame
allocation, and thrashing.

This continues directly from [`../c89`](../c89) (memory organization), whose last sentence announces
this topic: *"the next part of lecture will be on the virtual memory support."*

Total runtime: **1 h 36 min** across five recordings.

## What is here

| File | What it is |
|---|---|
| [`STUDY_GUIDE.md`](STUDY_GUIDE.md) | Full teaching document: every concept, the worked reference-string traces, comparison tables, practice problems with solutions, self-test questions |
| [`SUMMARY.md`](SUMMARY.md) | One-page cheat sheet — the whole series in ~10 minutes |
| [`NOTES.md`](NOTES.md) | Exam traps, lecturer emphasis, known slips, ASR correction glossary, coverage map |
| [`transcripts/`](transcripts/) | Ordered transcripts: `.srt` (verbatim) and `.txt` (normalised, timestamped) |

## Order of the recordings

All five source files were checked for duplicates first — all five are **unique** (different SHA-256).
Order was established from what the lecturer says at the seams, and from the topic dependencies:

| # | Source | Length | Topic | Evidence for position |
|---|---|---|---|---|
| 01 | `LTI Launch (6).mp4` | 27:20 | Why virtual memory, **swapping**, demand paging, page-fault handling, EAT | Opens: *"In last part of lecture, under memory organization… in this part… virtually extend the physical memory."* Ends: *"in the next lecture… we look at a specific design issue… page replacement."* |
| 02 | `LTI Launch (7).mp4` | 31:35 | **Page replacement**: victim selection, dirty bit, FIFO, OPT, LRU, second chance/clock | Opens: *"this is the second lecture of virtual memory management… in the last lecture we're talking about what happened if there is a page fault."* Ends: *"next lecture… frame allocation and the performance issue."* |
| 03 | `LTI Launch (8).mp4` | 5:32 | **Belady's anomaly** (supplementary) | Standalone: *"This video recording explains the particular anomaly… Belady's anomaly."* It recaps all four algorithms from 02, including clock, so it must follow 02. |
| 04 | `LTI Launch (9).mp4` | 14:39 | **Frame allocation** (fixed/variable) and **replacement scope** (global/local) | Opens: *"This is the last lecture on virtual memory support… frame allocation… thrashing."* 02 hands off to exactly this topic. |
| 05 | `LTI Launch (10).mp4` | 17:07 | **Thrashing**, locality, working-set model, page-fault-frequency | Opens: *"This recording is about the thrashing… as what we have already explained"* — i.e. after 04 introduced it. |

Unlike the `c89` batch, the file-name numbers here happen to match lecture order
(6 → 7 → 8 → 9 → 10). The duration metadata is also consistent with the content seams.

## Transcripts

Each part has two files:

* `NN-<slug>.srt` — **verbatim** subtitles. ASR hallucination loops and non-speech noise were
  removed; wording is untouched.
* `NN-<slug>.txt` — timestamped paragraphs with **obvious ASR term errors normalised**
  (`page full → page fault`, `OIs → OS`, `belated → Belady's`, `working side → working set`,
  `cloud hand → clock hand`, `5-4 → FIFO`, …).

The substitution list and the remaining known errors are in
[`NOTES.md`](NOTES.md#7-asr-correction-glossary).

Transcription: Whisper `large-v3-turbo` (MLX) on the extracted 16 kHz mono audio.

## Suggested study path

1. Read [`SUMMARY.md`](SUMMARY.md) once.
2. Work through [`STUDY_GUIDE.md`](STUDY_GUIDE.md), doing the reference-string trace by hand before
   checking the table.
3. Do the practice problems in §8 without looking at the solutions.
4. Read [`NOTES.md`](NOTES.md) last — it is the trap list.
