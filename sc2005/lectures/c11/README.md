# c11 — File Systems (lecture series)

Transcripts and study material for the four recordings covering **file systems**: the layered file
system, file attributes and directories, Unix protection, the two-level open file table, block
allocation (contiguous / linked / indexed), the Unix **inode**, and free-space management.

This continues from [`../c910`](../c910) (virtual memory). In `c89` the third column of the
"resource → question" table was **file systems**: *"How is space allocated to files?"* — this folder
answers it.

Total runtime: **1 h 41 min** across four unique recordings.

## What is here

| File | What it is |
|---|---|
| [`STUDY_GUIDE.md`](STUDY_GUIDE.md) | Full teaching document: every concept, the worked address-translation examples, capacity calculations, comparison tables, practice problems with solutions, self-test questions |
| [`SUMMARY.md`](SUMMARY.md) | One-page cheat sheet — the whole series in ~10 minutes |
| [`NOTES.md`](NOTES.md) | Lecturer emphasis, exam traps, the contradictions between slides/statements, ASR correction glossary, coverage map |
| [`transcripts/`](transcripts/) | Ordered transcripts: `.srt` (verbatim) and `.txt` (normalised, timestamped) |

## Order of the recordings

All four source files were checked for duplicates first — all four are **unique** (different
SHA-256). Order was established from what the lecturer says at the seams, and from the dependency
between the topics:

| # | Source | Length | Topic | Evidence for position |
|---|---|---|---|---|
| 01 | `LTI Launch.mp4` | 40:24 | File system from the **user's model view**: layers, attributes, record/stream translation, access methods, file operations, open file table, directories, links, directory operations | Opens the series: *"in this part of lecture we look at the file system from a user's model view"*, and lays out the roadmap *"logical file system first, followed by the file organization module"*. Ends with directory operations (list / search / traverse). |
| 02 | `LTI Launch (1).mp4` | 12:21 | **File protection** (Unix owner/group/public, rwx, directory bits) and the **two-level open file table** (supplementary) | Opens: *"This video recording is file protection and open file table."* Inside it: *"That's the last part of the logical file system."* — so it belongs to the logical-file-system topic of 01, after 01 introduced the single open file table. |
| 03 | `LTI Launch (2).mp4` | 39:27 | **File organization module**: logical vs physical blocks, **contiguous / linked / indexed** allocation, address translation, Unix **inode** | Opens: *"this is the second lecture, file system… we will focus on the file organization module"* — exactly the layer 01 says comes next. |
| 04 | `LTI Launch (3).mp4` | 9:22 | **Disk space management**: block-size trade-off, **bitmap**, **linked list** of free blocks (supplementary) | Standalone: *"This video recording is on disk space management."* It is the second responsibility of the file organization module named in 01 (*"managing the free available space on hard disk"*). |

Note the file-name order is misleading: the base name `LTI Launch.mp4` is actually **part 01**, and
`LTI Launch (1).mp4` is a **supplementary recording**, not part 2. The two main lectures are
`LTI Launch.mp4` (01) and `LTI Launch (2).mp4` (03); the two supplements are `(1)` and `(3)`.

## Transcripts

Each part has two files:

* `NN-<slug>.srt` — **verbatim** subtitles with per-segment timestamps. ASR hallucination loops
  (long `So, right. So, right. …` and `the file system and the file system …` runs) and non-speech
  noise were removed; wording is otherwise untouched.
* `NN-<slug>.txt` — the same content as timestamped paragraphs with **obvious ASR term errors
  normalised** (`puncture → pointer`, `direction → directory`, `anode → inode`, `caution →
  quotient`, `excise → access`, `2.22 → 2^22`, …). Wording is still the lecturer's; no sentences
  were rewritten or summarised.

The substitution list and the remaining known errors are in
[`NOTES.md`](NOTES.md#7-asr-correction-glossary).

Transcription: OpenAI Whisper `large-v3-turbo` (MLX) on the extracted 16 kHz mono audio track.

## Suggested study path

1. Read [`SUMMARY.md`](SUMMARY.md) once to get the shape of the chapter.
2. Work through [`STUDY_GUIDE.md`](STUDY_GUIDE.md) section by section, re-deriving each address
   translation by hand (the technique is identical in all three allocation methods — only the
   bookkeeping differs).
3. Do the practice problems in §11 without looking at the solutions.
4. Read [`NOTES.md`](NOTES.md) the night before — it is the trap list, not new material.

## Relationship to the rest of `lectures/`

| Folder | Topic | Ends by announcing |
|---|---|---|
| [`../c89`](../c89) | Memory organization | virtual memory |
| [`../c910`](../c910) | Virtual memory | *"file systems and disk scheduling — later topics"* |
| `c11` (this folder) | File systems | nothing — the recordings are self-contained supplements |
| [`../c12`](../c12) | I/O systems, disks, scheduling, RAID | the last topic in this sequence |

Not covered in these four recordings: disk scheduling, I/O systems, RAID, and file-system
implementation details beyond the inode (e.g. superblock, cylinder groups). The first three are
[`../c12`](../c12) — its S37 picks up the last idea in this folder, showing how the **allocation
method** determines the **disk request pattern**, and therefore how much disk scheduling can help.
