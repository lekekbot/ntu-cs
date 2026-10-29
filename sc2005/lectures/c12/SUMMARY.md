# I/O System & Disk — Summary (one page)

One deck, one question: **the CPU is thousands of times faster than a disk — what does the OS
do about it, and in what order should the disk serve requests?**

---

## The 60-second version

1. **I/O hardware** is a shared **bus** (or daisy-chained set of buses) with **controllers** —
   *host* controller on the motherboard, *device* controllers on each device. Devices differ wildly:
   transfer rate, unit of transfer, access method, direction, sharing, speed, error conditions.
2. **The kernel's I/O job** is to hide that mess. Objectives: **device independence**, **uniform
   naming/interfaces**, **error handling** (as many as possible transparently), and **synchronous
   vs asynchronous** transfer as the user needs.
3. The kernel is **layered**: **interrupt handler → device driver → device-independent I/O software
   → user-level I/O software**. Each layer only trusts the one below it.
4. The **subsystem services** are **scheduling** (a queue per device), **buffering** (store data
   in transit), **caching** (a *copy* of data kept for speed), **spooling** (a *queue* for a device
   that can serve only one job at a time, e.g. a printer), **device reservation**, **error
   handling**, and **I/O protection**.
5. **Blocking** = the process sleeps until the transfer completes (easy to use, poor concurrency).
   **Asynchronous** = the call returns immediately and the process continues (fast, hard to write).
   **Double buffering** overlaps fill of one buffer with consumption of the other.
6. A **disk** is **platters → tracks → sectors**; the **cylinder** is the same track across platters.
   Address = `(cylinder, track/surface, sector)`. Block `b` lives in track `b div sectors_per_track`
   at offset `b mod sectors_per_track`.
7. **Access time = seek + rotational latency + transfer.** Seek is **mechanical and dominant**;
   average rotational latency is **half** a rotation. That is why *sequential* I/O is ~2000× faster
   than *random* I/O, and why **disk scheduling exists**.
8. **Scheduling** reorders the request queue to cut total seek: **FCFS** (fair, terrible),
   **SSTF** (best each step, starves the edges), **SCAN** (elevator), **C-SCAN** (uniform wait,
   pays a full unserviced return), **LOOK / C-LOOK** (SCAN without going to the physical end).
9. **Disk management**: formatting (**low-level/physical**, **logical**, **partition**), **boot
   block**, **bad blocks** (sector sparing / sector slipping), **swap space**.
10. One disk is too slow *and* too fragile → **striping** (parallel transfer, no redundancy =
    RAID 0) and **mirroring** (duplicate, 50% capacity = RAID 1). **RAID** = both. Know
    **0, 1, 0+1, 1+0** and why **1+0 beats 0+1** on the second failure.

---

## The three timing components

$$
T_{\text{access}} = \underbrace{T_{\text{seek}}}_{\text{move the arm}} +
\underbrace{T_{\text{rot}}}_{\text{spin to the sector}} +
\underbrace{T_{\text{transfer}}}_{\text{read the bytes}}
$$

| Component | Depends on | Typical | Note |
|---|---|---|---|
| **Seek** | distance in cylinders | 10 ms | mechanical; **the thing scheduling can fix** |
| **Rotational latency** | where the sector happens to be | **½ rotation** = 4 ms of an 8 ms rotation | mechanical; reduced by interleaving / large transfers |
| **Transfer** | `(bytes ÷ sectors_per_track) × rotation` | 8/1024 ms per sector | electrical; the only part you cannot avoid |

**Random vs sequential** (10 ms seek, 8 ms rotation, 512 B sectors, 1024 sectors/track):

| Request | Random | Sequential |
|---|---|---|
| 1 sector (512 B) | `10 + 4 + 0.008` ≈ **14 ms** | 14 ms |
| 8 sectors (4 KB) | `8 × 14` = **112 ms** | **14 ms** |
| 256 sectors (128 KB) | `256 × 14` = **3.59 s** | **16 ms** |
| 2048 sectors (1 MB) | `2048 × 14` = **28.7 s** | **44 ms** |

Read that table twice: **the same 1 MB costs 28.7 s scattered and 44 ms contiguous.** Every design
decision in the chapter (buffering, read-ahead, clustering, striping) is an attempt to turn the
left column into the right one.

---

## Disk scheduling — the numbers to reproduce

Queue **98, 183, 37, 122, 14, 124, 65, 67**, head at **53**, cylinders **0–199**.

| Algorithm | Rule | Total head movement |
|---|---|---|
| **FCFS** | arrival order | **640** |
| **SSTF** | nearest first | **236** |
| **SCAN** (toward 0) | go to 0, then reverse | **236** |
| **C-SCAN** | to 199, jump to 0 **unserved**, sweep up | **382** |
| **C-LOOK** | to last request (183), jump to lowest request (14) | **322** |
| *LOOK* (not on the slides) | SCAN without the ends | *208* |
| *SCAN toward 199* | reverse direction | *331* |

FCFS 640 → the point of the exercise. SSTF 236 → but **starvation**. SCAN 236 → **fair, direction
costs**. C-SCAN 382 → **uniform wait, one wasted sweep**. C-LOOK 322 → **best of both for this
queue**.

```
FCFS   45 + 85 + 146 + 85 + 108 + 110 + 59 + 2                     = 640
SSTF   12 +  2 +  30 + 23 +  84 +  24 +  2 + 59                    = 236
SCAN   16 + 23 +  14 + 65 +   2 +  31 + 24 +  2 + 59               = 236
C-SCAN 12 +  2 +  31 + 24 +   2 +  59 + 16 + 199 + 14 + 23         = 382
C-LOOK 12 +  2 +  31 + 24 +   2 +  59 + 169 + 23                   = 322
```

The **199** in the C-SCAN line is the unserviced return sweep — *it still counts*. Forget it and you
get 183.

---

## Buffering / caching / spooling

| | What it is | Where the data is | Why |
|---|---|---|---|
| **Buffer** | a **holding area** for data *in transit* | memory, **one transfer's worth** | absorb speed mismatch, adapt block size, hold one copy while it is copied in/out |
| **Cache** | a **copy** of data that also exists elsewhere | memory, **many items** | *speed*; hit → avoid the device. The deck's definition: a region that holds a **copy** used for faster access |
| **Spool** | a **queue** for a device that serves one job at a time | disk/memory | **serialise** and **order** jobs (printer) |

Double buffer: with `C` = compute time and `T` = transfer time, the per-block cost drops from
`C + T` to **`max(C, T)`** once pipelined — the reason **double** buffering is the sweet spot:
one buffer being filled while the other is emptied.

---

## RAID

| Level | Name | Redundancy | Capacity of `n` disks | Loses |
|---|---|---|---|---|
| **0** | striping only | **none** | **n × C** (100%) | 1 disk = **all data** |
| **1** | mirroring | full duplicate | **nC / 2** (50%) | 1 per pair |
| **0+1** | **mirror of strips** | mirror each *stripe set* | **nC / 2** | 1 disk; a 2nd in the other set kills it |
| **1+0** | **strip of mirrors** | mirror each *disk*, then stripe | **nC / 2** | **1 per pair** — survives `n/2` |

Rule: **the redundancy you build first is the redundancy you keep.** 0+1 = stripe first, so a
failure takes out a whole stripe; 1+0 = mirror first, so a failure is contained in one pair. **1+0
wins.** The deck stops here — no RAID 4/5/6 (parity) is covered.

---

## Five things that decide exam marks

1. **Average rotational latency is half a rotation.** Quoting the full rotation time doubles your
   latency *and* breaks the 14 ms / 112 ms / 3.59 s / 28.7 s figures.
2. **Seek dominates.** Scheduling questions are seek-minimisation questions; that is the only
   component the OS can move, so it is the only one worth computing in a scheduling answer.
3. **C-SCAN's return sweep counts**, even though nothing is served on it. The current direction of
   the head changes every SCAN answer — state the direction **before** you compute.
4. **SSTF starves.** Nearest-request-first leaves far-away requests waiting indefinitely under a
   steady stream of nearby arrivals. SCAN/C-SCAN were invented for exactly that reason.
5. **Tutorial 12's trap is arrival times.** In Q4 the queue is not static: a request that has not
   arrived yet *cannot* be served, and a nearer request that arrives later **pre-empts** the current
   choice at the moment it appears. Rebuild the table row by row; the average service time is
   **32.24 ms**.

---

## What is *not* in this chapter

* **File systems** — that is [`../c11`](../c11); this deck picks up where it stops (block I/O,
  disk scheduling, RAID).
* **Virtual memory** — [`../c910`](../c910).
* **RAID 4/5/6 (parity)** — the deck stops after 1+0.
* **Flash / SSD** behaviour, NVM, and the IOMMU — not mentioned.
* The **device driver** is only named as a layer; no driver is written or examined.
