# c89 — Memory Organization (memory management lecture series)

Transcripts and study material for a five-part lecture series on **memory management / memory
organization**: address binding, contiguous allocation, paging, TLB, multi-level paging, inverted
page tables, and segmentation.

Total runtime: **1 h 56 min** across five unique recordings.

## What is here

| File | What it is |
|---|---|
| [`STUDY_GUIDE.md`](STUDY_GUIDE.md) | Full teaching document: every concept in the lectures, with derivations, worked examples, comparison tables, practice problems and self-test questions |
| [`SUMMARY.md`](SUMMARY.md) | One-page cheat sheet — the whole series in ~10 minutes of reading |
| [`NOTES.md`](NOTES.md) | Things to take note of: lecturer emphasis, exam traps, known slips/typos in the slides, ASR correction glossary |
| [`transcripts/`](transcripts/) | Ordered transcripts, `.srt` (verbatim) and `.txt` (lightly normalised, timestamped) |

## Order of the recordings

The six source files were **not** in lecture order. Order was established from what the lecturer
says at the seams of each recording, not from file names or file sizes:

| # | File | Length | Topic | Evidence for position |
|---|---|---|---|---|
| 01 | `LTI Launch (1).mp4` | 25:11 | Background, storage hierarchy, process image, compile/link/load, address binding, logical vs physical address | Opens the series ("we begin this part of lecture…"). Ends: *"In the next video recording, we will look at contiguous memory management techniques."* |
| 02 | `LTI Launch (2).mp4` | 22:55 | Contiguous allocation: fixed/dynamic partitioning, first/best/worst fit, fragmentation, compaction, relocation register | Opens with the two allocation categories announced in 01. Ends: *"we stop here for the first part of the memory allocation… In the next video… non-contiguous memory allocation."* |
| 03 | `LTI Launch.mp4` | 36:12 | Paging: frames/pages, page table, address split, PTBR/PTLR, TLB and EMAT, inverted page table | Opens: *"this is the second lecture on memory organization… we will focus on paging."* Ends: *"the next lecture… segmentation."* |
| 04 | `LTI Launch (3).mp4` | 12:59 | Two-level / multi-level paging (supplementary recording) | Standalone: *"This video recording focuses on two-level paging scheme."* The main lecture (05 @ 18:02) says multi-level paging was **not** covered, so this fills that gap. |
| 05 | `LTI Launch (5).mp4` | 19:34 | Segmentation, then chapter wrap-up | Opens: *"This is the last part of the lecture, memory organization… segmentation."* Ends: *"the next part of lecture will be on virtual memory support."* |

`LTI Launch (4).mp4` is a **byte-identical duplicate** of `LTI Launch (3).mp4`
(same SHA-256 `e4e1d7a1…`), so it was dropped.

Note the file-name order is misleading: the base name `LTI Launch.mp4` is actually **part 3**, and
`LTI Launch (1).mp4` is **part 1**.

## Transcripts

Each part has two files:

* `NN-<slug>.srt` — **verbatim** subtitles with per-segment timestamps. Hallucinated repetition
  loops and non-speech noise from the ASR were removed; wording is untouched.
* `NN-<slug>.txt` — same content as timestamped paragraphs, with **obvious ASR term errors
  normalised** (e.g. `offside → offset`, `TRB → TLB`, `bias feet → best fit`, `2.0 of nbis →
  2^n bytes`). Wording is still the lecturer's; no sentences were rewritten or summarised.

The full substitution list and the remaining known errors are in
[`NOTES.md`](NOTES.md#7-asr-correction-glossary).

Transcription: OpenAI Whisper `large-v3-turbo` (MLX) on the extracted 16 kHz mono audio track.

## Suggested study path

1. Read [`SUMMARY.md`](SUMMARY.md) once to get the shape of the chapter.
2. Work through [`STUDY_GUIDE.md`](STUDY_GUIDE.md) section by section, watching the matching
   transcript section when a diagram is referenced.
3. Do the practice problems in §9 of the study guide without looking at the solutions.
4. Read [`NOTES.md`](NOTES.md) the night before — it is the trap list, not new material.

## Relationship to the rest of `lectures/`

This is a self-contained sub-series (`c89`) on memory organization. It precedes the
**virtual memory** topic: the final sentence of part 05 is *"the next part of lecture will be on the
virtual memory support."*

That continuation is transcribed in [`../c910`](../c910) — swapping, demand paging, page replacement,
Belady's anomaly, frame allocation and thrashing.
