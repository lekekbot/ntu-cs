# I/O System & Disk — Things to Take Note Of

Exam-focused companion to [STUDY_GUIDE.md](STUDY_GUIDE.md): what the deck stresses, what is easy to
get wrong, and where the slides contradict themselves. No new material.

Because this chapter has **no recording**, every citation is a **slide number** (`S17`), not a
timestamp.

---

## 1. What the deck repeatedly stresses

| Point | Slide | Why it matters |
|---|---|---|
| **Devices vary enormously; the kernel's job is to hide that** | S3, S4 | Every design objective (device independence, uniform naming, error handling) is a consequence of this one fact |
| **The kernel is layered: interrupt handler → driver → device-independent → user** | S5 | "Which layer does X?" is the standard structural question |
| **Buffering ≠ caching ≠ spooling** | S7, S8 | The three are defined on adjacent slides precisely because they get confused |
| **Seek time dominates access time** | S16, S17 | It is 10 ms of the 14 ms; it is also the *only* component scheduling can touch |
| **Average rotational latency = ½ rotation** | S17 | Getting this wrong doubles latency and invalidates every number in S18–S19 |
| **Random I/O is ~2000× slower than sequential** | S18, S19 | 28.7 s vs 44 ms for the same 1 MB — this is the *reason* the rest of the chapter exists |
| **The request queue is what scheduling reorders** | S20, S21 | Scheduling only exists when there is a queue; with one request there is nothing to decide |
| **FCFS 640 vs SSTF 236** | S23, S26 | The single most quotable pair in the deck |
| **No algorithm is universally best — it depends on the number and types of requests** | S36 | The correct answer to "which is best?", and the deck says it explicitly |
| **File allocation determines the request pattern** | S37 | The bridge back to [`../c11`](../c11); the reason allocation is an I/O-performance topic |
| **RAID 0+1 vs 1+0 differ only in grouping order** | S44 | The one RAID distinction that is genuinely examinable |

---

## 2. Exam traps

1. **The OS does not manage devices directly — the driver does.** The device-independent layer calls
   the driver; the driver talks to the controller; the controller talks to the device.
2. **A buffer is not a cache.** A buffer holds data **in transit** (one transfer's worth, evicted as
   soon as it is consumed). A cache holds **a copy of data that also lives elsewhere**, many items,
   evicted by policy. "Buffer" for a permanent copy costs marks.
3. **Spooling is about *ordering*, not speed.** It exists for devices that serve **one job at a
   time** (printers). Its dictionary definition ("a buffer that holds output for a device that
   cannot accept interleaved data streams") is really a definition of a **queue**.
4. **Blocking vs asynchronous is about who waits**, not about speed. Blocking is *easier to
   program*; asynchronous is *more concurrent*. Do not call blocking "synchronous I/O is slower".
5. **Average rotational latency = half a rotation**, i.e. **4 ms** with an 8 ms rotation. Never use
   the full 8 ms as latency.
6. **Transfer time is `(bytes ÷ track capacity) × rotation`**, not `bytes ÷ bandwidth` in scheduling
   questions — the deck measures in fractions of a rotation.
7. **Random access ≠ random block.** In S18 "random" means *each sector is positioned
   independently*: the cost multiplies by the **sector count**. Sequential means one positioning
   amortised over a whole track.
8. **The `1 MB` sequential figure on the slide is conservative.** S19 charges a **full rotation per
   track**, giving 44 ms; the pure formula (`14 + (2048/1024)×8`) gives 30 ms. Both are defensible —
   state which one you used.
9. **In C-SCAN the return sweep is unserviced but still costs head movement.** It is a **jump to 0**,
   and it is charged as **199** cylinders. Omitting it gives 183 instead of 382.
10. **C-SCAN does not "serve on the way back".** If your trace has requests being served while the
    head travels from 199 down to 0, you have drawn SCAN, not C-SCAN.
11. **LOOK and C-LOOK stop at the *last request*, not the last cylinder.** That is the whole
    difference from SCAN/C-SCAN, and it is why C-LOOK gets 322 while C-SCAN gets 382 on the same
    queue.
12. **SCAN's answer depends on the current direction.** Toward 0 → 236; toward 199 → **331**. If the
    question omits the direction, say what you assumed.
13. **SSTF can starve.** "Nearest first" is not fair; a steady stream of near arrivals postpones a
    far request indefinitely. This is the standard "why not SSTF?" answer.
14. **Starvation-avoidance ≠ short waits.** SCAN/C-SCAN/C-LOOK bound the wait; they do not minimise
    it for every request. A request arriving just after the head passes waits almost an extra sweep.
15. **One request = no scheduling decision.** If the queue has a single entry, every algorithm gives
    the same answer. Tutorial 12 Q3(a) turns on exactly this.
16. **RAID 0 has no redundancy at all** — it is "redundant" only by the acronym's history. Losing one
    disk loses **every** file, because every file is striped across every disk.
17. **Mirroring halves capacity and does nothing for write bandwidth** (each write is doubled);
    it only improves *read* throughput.
18. **RAID 0+1 is not the same as RAID 1+0.** 0+1 = **mirror of strips** (stripe first); 1+0 =
    **strip of mirrors** (mirror first). On the second failure, **1+0 survives more often**.
19. **A "logical format" is not a partition.** Low-level format = sectors/track headers and trailers;
    logical format = the **file system** structure (that is `c11`); partitioning = slicing the disk
    for several OSes.
20. **Block `b` is in track `b div sectors_per_track`** — integer division, and the sector offset is
    the **remainder**. Same `q`/`r` first step as the whole of `c11`.

---

## 3. Known slips and internal contradictions in the deck

Know the correct version; a marker will.

| # | Slip | Slides | Correct version |
|---|---|---|---|
| 1 | The chapter is labelled **"Part 10"** on S1 but the roadmap slide prints **"Part 7"** | S1, S13 | It is part 10 of the course notes (`10.N` footers throughout). S13's "Part 7" is a stale copy. |
| 2 | **S16 states rotational latency as 8 ms** ("time for the desired sector to move under the head, ≈ 8 ms") while S17 uses a **full rotation of 8 ms** and an **average latency of 4 ms** | S16 vs S17 | With 8 ms full rotation the **average** rotational latency is **4 ms**. S17's numbers (14 ms per random sector) only close with 4 ms; treat S16's "8 ms" as "8 ms **per full rotation**". |
| 3 | Two slides print **out-of-order footers**: the double-buffer slide is footed `10.13` and the request-lifecycle slide `10.11`, while the roadmap is also `10.13` | S10, S11, S13 | S10 should be `10.10` and S11 `10.11`; the S13 duplicate footer confirms the S10 one is wrong. |
| 4 | S10 and S11 carry a **different course code** in the footer (`SCSC002C/ECSC202C`) from the rest of the deck | S10, S11 | These two slides were lifted from another course's deck. Content is still examinable; the code is not. |
| 5 | The **inset legends on the S18/S19 tables are illegible/inconsistent** — the sector counts do not match the arithmetic | S18, S19 | The calculations are all consistent with **1024 sectors/track, 512 B sectors** (track = 512 KB). Use those parameters. |
| 6 | The **S41 striping diagram omits Block 9 and Block 11** | S41 | The rule is `drive = (block mod n) + 1`; the picture is illustrative, not exhaustive. |
| 7 | S29 and S35 pose **questions with no answers printed** | S29, S35 | Answered in §6 below. |
| 8 | The **S3 device table's "speed" column** compares ms and KB/s in one column | S3 | Not a contradiction, just an incomparable axis — do not quote the column as a metric. |
| 9 | **The deck never names RAID 4/5/6** despite explaining RAID as "redundancy without full duplication" | S43, S44 | As taught, redundancy = **mirroring** only. Do not introduce parity into a slide-referenced answer; you may mention it as "beyond this chapter". |

---

## 4. Slides and diagrams: what the text alone does not convey

The deck is diagram-heavy; these are the ones where the picture carries the content.

| Slide | Diagram | What to take from it |
|---|---|---|
| S2 | Bus topology | A **host controller** on the motherboard fans out to a **system bus**, then a **SCSI/expansion bus**, with **device controllers** each serving devices. Note the two-level hierarchy — that is why "the bus" is not a single wire. |
| S5 | Kernel layering | Five boxes: **user-level I/O software → device-independent I/O software → device drivers → interrupt handlers → hardware**. Vertical arrows only — no layer skips a neighbour. |
| S9 | Blocking / non-blocking / asynchronous timelines | Three timelines for the same request. Blocking: process bar and I/O bar are **serial**. Non-blocking: process continues but must **poll**. Asynchronous: process continues and is **notified** at completion. |
| S10 | Double buffer | Two buffers between producer and consumer; the fill of B starts as soon as A is full, before A is consumed. |
| S11 | Request lifecycle | Wait queue → driver → controller → interrupt → wakeup. The loop that explains "why does a single read cost so much". |
| S14 | Photograph of an opened drive | Platters, spindle, **actuator arm** and **read/write head**. Shows physically why seek is mechanical. |
| S15 | Disk geometry | Concentric **tracks**, radial **sectors**, stacked platters → **cylinder**. Block→(track, offset) mapping annotated. |
| S17 | Positioning-time diagram | The arc from the head's current position to the target sector; the **halfway point** marked as the average. |
| S22, S25, S28, S31, S34 | Head-movement graphs | X = cylinder, Y = request sequence. FCFS = a jagged vertical mess; SSTF = short sawtooth; SCAN = one long sweep up then down; C-SCAN = ramp up, **vertical jump**, ramp up; C-LOOK = same but shorter ramps. **Learn to recognise these five shapes** — a graph question is likely. |
| S39 | Disk management | Boot block → partition table → partitions, each with its own **superblock / free space / inodes / data** (all `c11` terms). |
| S41 | Striping | Blocks 0–8,10 laid across four drives, one row per stripe — parallel transfer visualised. |
| S44 | RAID 0+1 vs 1+0 | Two 8-disk layouts side by side; only the **grouping brackets** differ. |

---

## 5. Coverage map (S1–S46)

| Slides | Topic | Study guide § |
|---|---|---|
| S1 | Title / roadmap | 0 |
| S2–S3 | I/O hardware: buses, controllers, device variety | 1 |
| S4 | Design objectives | 2 |
| S5 | Kernel I/O structure (layers) | 3 |
| S6–S8 | Subsystem services: scheduling, buffering, caching, spooling | 4 |
| S9–S12 | Blocking / asynchronous / double buffering / why I/O costs | 5 |
| S13 | Roadmap repeated (the "Part 7" slip) | — |
| S14–S15 | Disk structure, geometry, block addressing | 6 |
| S16–S19 | Positioning time, formulas, random vs sequential | 7 |
| S20–S37 | Disk scheduling: FCFS, SSTF, SCAN, C-SCAN, C-LOOK, selection | 8 |
| S38–S39 | Disk management: format, boot block, bad blocks, swap | 9 |
| S40–S44 | Disk reliability: striping, mirroring, RAID | 10 |
| S45–S46 | Summary slides (I/O system; disk) | — |

Reading order note: **S20 (the concept) → S21 (the queue) → each algorithm's definition, graph, then
calculation.** The deck repeats that triple five times, so the structure of a scheduling answer is
itself being taught: **define the rule, draw the trace, sum the movement.**

---

## 6. Answers to the questions the deck leaves open

**S29 — "After the head reverses direction, does it need to serve requests in the reversed direction
immediately?"**

No. SCAN reverses at the **physical end of the disk** (cylinder 0), not at the last request. The
service order after reversal is fixed by **geometry**: the head serves whatever it meets on the way
up. It is not nearest-first. A request just behind the head therefore waits for the arm to reach 0
and come back — nearly two sweeps.

**S35 — "Do SCAN, C-SCAN and C-LOOK really solve the starvation problem?"**

They **bound** the wait; they do not make it uniformly short. Every pending request is reached
within at most roughly one sweep (C-SCAN/C-LOOK) or two (SCAN), so **indefinite postponement is
impossible**. But under a continuous arrival stream a request can still wait a long time, and a
request arriving just after the head passes pays almost a full extra sweep. **SSTF is the only one
of the five that can starve a request forever.** C-SCAN/C-LOOK's real advantage is **uniformity** of
wait, not a smaller worst case.

**S36 — "which algorithm is best?"**

There isn't one. The deck's own answer: *"performance depends on the number and types of requests"*.
Under **heavy load** (a real queue to reorder) SCAN/C-SCAN/LOOK/C-LOOK do better and starvation is
unlikely; under **light load** FCFS is nearly as good and much simpler.

---

## 7. Memory hooks

* **"Seek, spin, send"** — the three timing components in order.
* **"Half a spin"** — average rotational latency is half a rotation.
* **"FCFS = 640, SSTF = 236"** — the two anchors of the scheduling table. Everything else (236,
  382, 322) you can rebuild from the trace.
* **C-SCAN = "circular" = one-way only** → pays the **199** return. C-LOOK = **"LOOK" = stop at the
  last request** → pays **169**.
* **SCAN = elevator**; an elevator does not wait for the nearest floor, and it does not teleport back
  down — it turns around at the end. That single sentence answers both S29 and "why not SSTF".
* **Striping = speed, mirroring = safety, RAID = both.** Alphabetical: **S**triping/**S**peed first,
  then **M**irroring/**M**irror.
* **0+1 mirrors the stripe; 1+0 stripes the mirror.** Read the digits in construction order (left
  first), and remember the *last* thing built is the outer layer.
* **Buffer = passing through; cache = copy; spool = queue.**

---

## 8. Quick self-check before the exam

1. Which of the three access-time components can disk scheduling reduce, and why only that one?
2. Why is average rotational latency half a rotation, and what is it in milliseconds for an 8 ms
   rotation?
3. Same queue, head at 53: which algorithm gives 382 and which gives 322, and what single structural
   difference causes the 60-cylinder gap?
4. In which algorithm does the *direction of head movement* change the numeric answer, and by how
   much on the S21 queue?
5. Why can SSTF starve but SCAN cannot — and what does SCAN's guarantee *not* cover?
6. Name the three ways buffering helps and the one thing it is not.
7. What is the capacity of RAID 1+0 over `n` disks, and why does it beat RAID 0+1 on the second
   failure?
8. A file's blocks are contiguous. Does disk scheduling still help? (Yes — but it has little to
   exploit, because allocation already produced short seeks.)
9. Order the layers: device driver, interrupt handler, device-independent I/O software, user-level
   I/O software.
10. Random or sequential: which one makes the *number of requests* the dominant cost, and which one
    makes *track capacity* the dominant cost?
