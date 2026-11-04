# SC2006 A4 visual examination reference

Open `output/pdf/SC2006_A4_Visual_Reference.pdf` to read or print the finished reference. This edition contains **65 A4 portrait pages, 66 captioned figures, 65 tables and 23 compact reference panels**. Two-column layouts and grouping the older papers save **7 pages (9.7%)** from the previous 72-page edition. It is 12 pages shorter than the earlier 77-page edition and still 5 pages above a 60-page target.

The 17 chapters retain ELI5 explanations, visual models, answer checks and essential traps. Tutorial coverage focuses on difficult combinations and constraints: selective Observer with changeable channel strategies, GES proposal/actual-recording invariants, EC/BV ambiguities and CFG feasibility/coverage. Routine projector and basic GES use-case/class/sequence walkthroughs are omitted. Hard EC/BV and CFG solutions remain in their topic chapters rather than being repeated.

The PYP section retains all eight papers and all 32 main question prompts. The four older papers (AY2022/23 and AY2023/24) form a question bank grouped under Q1, Q2, Q3 and Q4. Each group retains the case-specific answers, diagrams, constraints and all original EC/BV/defensive-test tables. The four recent papers (AY2024/25 and AY2025/26) remain complete and chronological. Prompts are summaries; the original question PDFs supply exact wording and marks.

## What changed

- Short explanations, lists, traps and compact diagrams use two columns. Complex diagrams and wide comparison/testing tables remain full-width. Text fonts were not reduced.
- Twenty-three short chapter tables now use labelled reference entries within the columns. Their substantive entries remain. Comparison entries explicitly name both sides; the table count falls because the format changes, not because those facts were deleted.
- The relationship-notation atlas uses four tiles per row, retaining all ten sketches. All 66 captioned figures and their graphic assets remain.
- The older papers are grouped by question type, with a case map showing the page for every Q1–Q4 answer. Common boundary, process, architecture and testing rules are shared; case-specific applications and assumptions remain beside the relevant answer.
- All 32 existing prompt summaries, all original PYP testing-table rows and the four recent papers' full answers remain. No further chapter topics or hard tutorial questions were removed.
- The previous edition's W/S/A/P/C/M templates and earlier content consolidation remain.

Read each two-column band down the left column, then down the right column. Continue below the next full-width diagram or table.

## Find material quickly

Chapters and papers can share pages. These are starting pages, checked against the contents.

| Material | PDF page |
| --- | ---: |
| Navigation and contents | 1 |
| Chapters 1–8: requirements, UML and processes | 2, 2, 5, 7, 9, 11, 13, 15 |
| Chapters 9–11: architecture, patterns and MVC | 18, 20, 22 |
| Chapters 12–14: testing, EC/BV and difficult GES constraints | 23, 26, 29 |
| Chapter 15: hard tutorial questions | 30 |
| Chapter 16: AI and agentic systems | 31 |
| Chapter 17: examination answer checklist | 33 |
| Source index / PYP overview | 33 / 33 |
| Older-paper case map and Q1 use cases | 34 |
| Older Q2: conceptual models, behaviour and process | 38 |
| Older Q3: architecture, NFRs and patterns | 42 |
| Older Q4: testing and maintenance | 45 |
| AY2024/25 S1 / S2, complete papers | 49 / 53 |
| AY2025/26 S1 / S2, complete papers | 57 / 61 |

## Print

Print A4 at **actual size / 100%**, one PDF page per sheet side. All pages are portrait. The compact diagrams have small labels, so avoid multiple pages per side or additional scaling. Check one diagram-heavy page before printing the complete pack. Colours have text labels and remain usable in greyscale. Physical printing has not been tested.

## Edit and compile

Open this folder in the Codex LaTeX editor, with `main.tex` as the main document. Text lives in `sections/`. `papers-overview.tex` contains the case map; `older-q1.tex` through `older-q4.tex` contain the grouped answers. `papers-2024-25.tex` and `papers-2025-26.tex` contain the complete recent papers. The project also compiles with Tectonic (`tectonic main.tex`) or a standard LaTeX installation using pdfLaTeX; repeat pdfLaTeX until contents and references settle. Required packages are listed in `main.tex`.

`images/` contains editable Mermaid sources, SVG renders and PDF graphics. Render settings are in `images/mermaid-config.json` (Mermaid 12.3, classic look). After editing Mermaid, regenerate its PDF and check the physical dimensions in the LaTeX source. Editing the `.mmd` alone does not change the compiled document. Long diagrams use numbered continuation panels; their safe cuts are recorded in `images/portrait-panels.json`. Complete nodes and labels must remain inside each panel. Workflow files ending `-a`, `-b` or `-c` form the connected phases of a single figure.

Some class diagrams omit long parameter lists to save space. Method names, roles, relationships and key attributes remain; the adjacent answer supplies policy details. Assignment replacement remains atomic even though the compact operation is named `replaceAssignment()`.

Source links point to original PDFs in this repository on the author's computer. The document compiles without those PDFs, but the links require the original paths or updating them after moving the repository.

## Evidence and limits

Material follows `../SC2006_Study_Guide.md`, the supplied lectures/tutorials and the eight PDFs in `../pyps/`. The saved source compiles successfully in the desktop editor. All 65 pages were rendered for layout review; the relationship atlas, a grouped older answer and the final testing page received full-size checks. Automated checks confirm portrait A4 dimensions, existing assets, correct chapter/paper contents entries, shared-template page references, the older case/question map, all 32 original PYP prompt summaries and all testing-table rows. No overflowing content, missing glyphs or unresolved references were reported.

Answers remain unofficial; no marking scheme was supplied. Mermaid figures explain concepts; examination drawings must use proper UML notation. Historical formats do not guarantee the next examination's format or permitted materials.
