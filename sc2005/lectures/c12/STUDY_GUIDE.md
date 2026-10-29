# SC2005 — I/O System & Disk: Study Guide

Companion to the slide deck in this folder. Citations are slide numbers, e.g. **`S17`** means page
17 of the PDF (which prints footer `10.17` on most pages — see
[NOTES.md](NOTES.md) §3 for the two pages where the footer lies).

Transcript: [01 — slide transcript](transcripts/01-io-system-and-disk-slides.md) ·
[02 — Tutorial 12](transcripts/02-tutorial-12-io-systems.md)

---

## 0. The chapter in one picture

`c11` finished with the file system: bytes live in blocks, blocks are found through an inode, and
somebody has to hand out free blocks. Every one of those operations eventually becomes **"go read
this sector"**. This chapter is about the layer that does that, and about the one device where the
cost of "go read this sector" depends on *where the head happens to be*.

```
   application:  write(fd, buf, 4096)
        |
        v
   +-------------------------------------------------------+
   | kernel I/O subsystem   scheduling | buffering | caching | spooling |
   |                        error handling | reservation | name translation |
   +-------------------------------------------------------+
        |                                  (S5, S45)
        v
   device-independent -> device driver -> interrupt handler -> controller -> device
   (hide the differences)                 (S5: the driver layer exists to give generality)
        |
        v
   the device is a spinning disk:
   a 1-D array of 512-byte blocks, mapped onto (cylinder, track, sector)     (S15)
   cost to touch one = seek + rotational latency + transfer                   (S16-S17)
        |
        +--> "the seek dominates"  ==> reorder the queue: disk scheduling    (S20-S35)
        +--> "one disk is too slow / too fragile" ==> striping, mirroring, RAID (S40-S44)
```

The single sentence the whole chapter hangs on: **the disk is 4-5 orders of magnitude slower than
memory, and almost all of that cost is the head moving to the right place.** Everything else —
buffering, scheduling, striping — is an attempt to hide or share that movement.

Sections of the deck:

| Slides | Topic |
|---|---|
| S1–S4 | Roadmap, I/O hardware, design objectives (efficiency, generality) |
| S5–S8 | Kernel I/O structure and the services of the kernel I/O subsystem |
| S9–S12 | Performance: blocking vs asynchronous, double buffering, why I/O costs CPU |
| S13–S19 | Disk structure, addressing, and the timing formula |
| S20–S37 | Disk scheduling: FCFS, SSTF, SCAN, C-SCAN, C-LOOK (+ LOOK) |
| S38–S39 | Disk management: low-level format, partition, logical format |
| S40–S44 | Reliability: striping, mirroring, RAID 0 / 1 / 0+1 / 1+0 |
| S45–S46 | Summary |

---

## 1. I/O hardware

### 1.1 The topology (S2)

A device is never attached *directly* to the CPU. The chain is always:

```
CPU --(bus)--> controller --(cable/bus)--> device
```

The slide's PC picture has three buses: a fast local/memory bus (processor + cache + memory behind
the **bridge/memory controller**), a **PCI bus**, and a slower **expansion bus**.

| Attached to | Device | Controller |
|---|---|---|
| PCI bus | monitor | graphics controller |
| PCI bus | disks | SCSI controller → SCSI bus → several disks |
| PCI bus, via the expansion-bus interface | disks | IDE disk controller |
| expansion bus | keyboard, parallel port, serial port | expansion bus interface |

Two facts to take from the picture:

* **A controller is a small processor with its own registers, and it is the thing the CPU actually
  talks to.** The disk itself is dumber than the controller.
* **A controller can serve several devices** (one SCSI controller, many disks). That matters later:
  a single controller queue is where disk scheduling happens.

### 1.2 Devices vary enormously (S3)

This table is the justification for the *whole layering* of the next section — the OS cannot have
one code path per device, so it hides the differences:

| Aspect | Variation | Example |
|---|---|---|
| Data-transfer mode | **character** vs **block** | terminal vs disk |
| Access method | **sequential** vs **random** | modem vs CD-ROM |
| Transfer schedule | **synchronous** vs **asynchronous** | tape vs keyboard |
| Sharing | **dedicated** vs **shared** | tape vs keyboard |
| Device speed | latency, seek time, transfer rate, delay between operations | — |
| I/O direction | **read only**, **write only**, **read–write** | CD-ROM, graphics controller, disk |

Note the two entries that reappear in the rest of the chapter: *sharing* (a printer is dedicated →
therefore it needs **spooling**, S8) and *speed* (enormous range → therefore **buffering**, S7).

---

## 2. Design objectives (S4)

Two, and they pull in opposite directions.

| Objective | Why | What it buys | What it costs |
|---|---|---|---|
| **Efficiency** | I/O is a bottleneck; devices are extremely slow compared with memory and CPU; **disk I/O** gets the most attention | buffering, caching, scheduling, DMA, double buffering | complexity |
| **Generality** | Handle all devices uniformly, both for *processes* (a uniform interface: `read`/`write`/`open`) and for *the OS* (uniform management) | the driver layer, the vnode/file abstraction | the layers that make I/O system calls expensive (S45) |

The tension is the exam answer to "why are I/O system calls costly?": generality requires many
software layers, and every layer costs CPU.

---

## 3. Kernel I/O structure (S5)

Reading the slide from the bottom up:

```
        devices        (SCSI devices, keyboard, mouse, PCI bus, floppy, ATAPI)
           |  ^
           v  |
     controllers      (SCSI, keyboard, mouse, PCI bus, floppy, ATAPI)
           |  ^
           v  |
     interrupt handler
           |  ^
           v  |
     device drivers   <-- the "I/O request" boundary: drivers are per-device
           |  ^
           v  |
  kernel I/O subsystem  <-- device-independent, one copy for all devices
           |  ^
           v  |
        user process     (system-call interface)
```

The crucial layer is the **device driver**: it is the only place that knows the device's register
set, and it presents a *uniform* interface upward (`read`, `write`, `ioctl`, `open`, `close`).
That is exactly how S45 summarises it: *"the device-driver layer hides the differences among device
controllers from the I/O subsystem of the kernel."*

Note the ordering consequence: **device drivers are inside the kernel** but *below* the kernel I/O
subsystem (they are part of the kernel's I/O *structure*, not of the device-independent subsystem).
This distinction is Tutorial 12 Q1(c).

---

## 4. Kernel I/O subsystem: the services (S6–S8, S45)

S45 lists the services as: **I/O scheduling, buffering, spooling, error handling, device
reservation, device name translation** — and S6–S8 develop four of them.

### 4.1 I/O scheduling (S6)

* Rearranging the **order of service** of requests, e.g. disk scheduling.
* Improves efficiency by making the device's mechanical work smaller.

The diagram is the important part: the kernel keeps a **per-device request queue** (the picture
shows queues feeding `mag tape unit 0/1`, `disk unit 0/1`, `terminal unit 0`, each as a `head`/`tail`
list of PCBs), and the scheduler decides the order in which the PCBs in that queue are handed to the
device. Scheduling cannot create locality — it can only exploit the locality that is already in the
queue. That limitation is Tutorial 12 Q3.

### 4.2 Buffering (S7)

* Store data **in memory while transferring** between devices.
* Purpose 1: cope with **speed mismatch** (fast producer, slow consumer).
* Purpose 2: cope with **transfer-size mismatch** — e.g. networking delivers small packets, but a
  file write wants big blocks (or the reverse).

### 4.3 Caching (S8)

* **Fast memory holding a copy of data.** (The copy is the point; a buffer you *own* is not a
  cache.)
* Purpose: *"to improve I/O efficiency for files that are being written and reread rapidly."*

### 4.4 Spooling (S8)

* Hold output for a device.
* Used for a device that **can serve only one request at a time**, e.g. a printer: the spooler
  accepts output from many processes and queues it, so processes never block on the printer.

### 4.5 Buffering vs caching vs spooling — the distinction that gets examined

| | What it is | Problem it solves | Typical use |
|---|---|---|---|
| **Buffer** | a temporary area for data **in transit**; the data is consumed and gone | speed mismatch, transfer-size mismatch | `read()` into a user buffer; network reassembly |
| **Cache** | a **copy** of data that also lives elsewhere, kept for reuse | repeated access to the same data | buffer cache / page cache; files written and re-read rapidly |
| **Spool** | a queue of **whole jobs** for a device that can serialise them | a shared device that can serve only one at a time | print queue |

The one-line discriminator: a **buffer** holds data *moving*; a **cache** holds data *for reuse*; a
**spool** holds *requests*.

This is exactly Tutorial 12 Q1(a): "Buffering can be used to improve I/O efficiency for files that
are being written and re-read rapidly" — that sentence is the slide's definition of **caching**,
word for word (S8), so the statement is false *as written*.

---

## 5. Performance: blocking, asynchronous, double buffering (S9–S12)

### 5.1 Blocking vs asynchronous (S9)

Both diagrams run top-to-bottom in time, across `user land` / `kernel` / `hardware`, with the stack
*requesting process → device driver → interrupt handler → device controller → device*.

| | Blocking I/O | Asynchronous I/O |
|---|---|---|
| When the system call returns | after the I/O **completes** | **immediately**, once the request is queued |
| Process state meanwhile | **waiting** (blocked) | keeps **running** its own code |
| Who wakes the process | the interrupt handler puts it back on the ready queue | the system **signals** the process on completion |
| Programming model | simple | needs completion notification (signal / callback / poll) |
| Concurrency | needs another process to use the CPU | one process can overlap its own I/O with its own computation |

**Non-blocking / asynchronous is the same idea for this purpose**: the call does not wait. So a
process that issues a non-blocking I/O call is **not** put into the waiting state — Tutorial 12
Q1(b) is false.

### 5.2 Double buffering (S10)

```
I/O device --In--> [ b1 | b2 ] --Move--> user process
```

While the device fills one buffer, the process empties the other. The gain is *overlap*:

```
single buffer:   |--device t_d--|--process t_p--|--device--|--process--|   period = t_d + t_p
double buffer:   |--device t_d--|--device t_d--|--device t_d--|
                        |--process t_p--|--process t_p--|                 period = max(t_d, t_p)
```

| Device time per block | Process time per block | 1 buffer | double buffer | speed-up |
|---|---|---|---|---|
| 100 ms | 10 ms | 110 ms/block | 100 ms/block | 1.10× |
| 10 ms | 100 ms | 110 ms/block | 100 ms/block | 1.10× |
| 100 ms | 100 ms | 200 ms/block | 100 ms/block | **2.00×** |

The lesson: double buffering helps **only when the two times are comparable**. If one side is 10×
faster, the slow side is the whole story and overlap buys ~nothing. (That is why the tutorial
question about the read-process loop wants *asynchronous I/O + double buffering*, and would be
disappointed if the process took 1 ms per block.)

### 5.3 Why I/O is a major factor in system performance (S12)

Three distinct costs, and they are all **CPU** costs even though none of them is the disk:

1. **Driver code executes on the CPU** — every request runs driver instructions.
2. **Interrupts cause context switches** — each completion is an interrupt, a trap into the kernel,
   a wake-up, later a reschedule.
3. **Data copying** between I/O controllers and physical memory — bytes move twice (device → kernel
   buffer → user buffer).

This is the accounting behind S45's *"I/O system calls are costly in terms of CPU consumption,
because of the many layers of software between a physical device and the application."*

---

## 6. Disk structure and addressing (S14–S15)

### 6.1 The geometry

| Term | Meaning |
|---|---|
| **Platter** | one disk surface carrier; a drive stacks several |
| **Head** | one read/write head per platter *surface*; all heads move together on one **arm assembly** |
| **Track** | one concentric circle on one surface |
| **Cylinder** | the set of tracks at the **same radius on all platters** — i.e. what all heads can reach without moving the arm |
| **Sector** | the smallest addressable unit on a track; **512 bytes** on this deck |
| **Spindle / rotation** | the platters spin at constant angular velocity |

The cylinder is the natural unit for scheduling, because switching between tracks in the same
cylinder costs **no seek** — only head selection.

### 6.2 The address model (S15)

The OS never speaks geometry. It sees:

> *"Disk drives are addressed as large 1-dimensional arrays of physical blocks, where the physical
> block is the smallest unit of transfer (usually 512 bytes). The array of physical blocks is
> mapped into the sectors of the disk sequentially."*

So physical block `b` → a position determined by the constants of the drive:

```
sectors_per_track = SPT          (this deck: 1 K = 1024)
track             = b div SPT
sector offset     = b mod SPT
bytes per track   = SPT × 512 B  = 1024 × 512 = 512 KB
```

Example: block `5000` → track `5000 div 1024 = 4`, offset `5000 mod 1024 = 904`. This is the same
`div`/`mod` idiom as the file-allocation formulas in `c11` §6 — logical block → physical location is
always quotient-and-remainder, and only the meaning of the divisor changes.

---

## 7. Disk I/O timing (S16–S19)

### 7.1 The three components

```
                request arrives
                      |
        [1] seek: move arm to the right cylinder        T_seek
                      |
        [2] rotational latency: wait for the sector      T_rot   (on average = ½ rotation)
            to spin under the head
                      |
        [3] transfer: sectors stream past the head       T_transfer(N)
                      |
                 request done
```

S17 gives the model explicitly:

```
T_access(N)  =  Positioning Time  +  Data Transfer Time(N)
Positioning  =  Seek Time  +  Rotational Latency
Transfer     =  (N / sectors_per_track) × Full Rotation Time
```

and the parameters used for every worked example in the deck:

| Parameter | Value |
|---|---|
| Seek time | **10 ms** |
| Full rotation time | **8 ms** |
| → average rotational latency | **4 ms** (= ½ rotation) |
| Sector size | **512 B** |
| Sectors per track | **1 K = 1024** |
| Track capacity | 1024 × 512 B = **512 KB** |

**Why ½ rotation for latency:** the sector you want is, on average, half a revolution away from the
head. Full rotation = worst case, ½ = average. S16 quotes `8 milliseconds` for "rotational
latency"; S17 correctly uses 8 ms as the *full rotation* and 4 ms as the latency. Use **4 ms** in
calculations — see [NOTES.md](NOTES.md) §3.

### 7.2 Random access (S18)

A random request touches one place, so it pays the full positioning **per request**:

```
1 sector  = 10 ms (seek) + 4 ms (rot) + (1/1024) × 8 ms  ≈  14 ms
```

Note that the transfer term is *negligible*: 7.8 µs out of 14 ms. **The seek is 71% of the cost and
the positioning is 99.94% of it.** Every scheduling result in this chapter follows from that ratio.

| Request size | Sectors | Random total (N × 14 ms) |
|---|---|---|
| 4 KB | 8 | **112 ms** |
| 128 KB | 256 | 3584 ms ≈ **3.5 s** |
| 1 MB | 2048 | 28 672 ms ≈ **28 s** |

The slide's random model is "one positioning per sector": it treats `N` sectors spread randomly as
`N` independent 1-sector requests. That is deliberately pessimistic, but it is the model being
tested.

### 7.3 Sequential access (S19)

Now positioning happens **once per track**, not once per request, because consecutive sectors come
past the head anyway:

| Request size | Sectors | Tracks | Sequential total | Ratio vs random |
|---|---|---|---|---|
| 4 KB | 8 | 1 (fits) | 14 ms + (8/1024)×8 = 14.06 ms | ~8× |
| 128 KB | 256 | 1 (fits) | 14 ms + 2 ms = **16 ms** | ~224× |
| 1 MB | 2048 | 2 | 2 × 22 ms = **44 ms** | ~650× |

The 1 MB line is the deck's most-quoted result:

```
1 MB random     = 2048 × 14 ms = 28 s
1 MB sequential = 2 tracks × (14 ms positioning + 8 ms full rotation) = 44 ms
```

Two things to say about the 44 ms:

* The slide charges **a full rotation per track** (14 + 8 = 22 ms per track), i.e. it assumes you
  wait for a full revolution to read a whole track. It is conservative. A more precise figure for
  1 MB over 2 tracks is 14 ms + 2 × 8 ms = 30 ms, which is what the pure formula gives
  (10 + 4 + 2048/1024 × 8). **Quote 44 ms when reproducing the slide; quote 30 ms only if you show
  the formula.**
* Either way the conclusion is the same: **sequential I/O is ~600× faster than random I/O on the
  same device.** Effective bandwidth: 1 MB / 44 ms ≈ 23 MB/s versus 36 KB/s random.

This is the number that makes the rest of the chapter obvious:

* → the OS should **buffer** and **schedule** to turn random into sequential (S6–S8, S20).
* → the file system should allocate **contiguously** (S37, and `c11` §6.3).
* → a disk array should **stripe** so that one logical sequential stream becomes `n` parallel ones
  (S40).

---

## 8. Disk scheduling (S20–S37)

### 8.1 The goal (S20)

| Quantity | Slide definition |
|---|---|
| Access time | seek + rotational latency (+ transfer) |
| **Seek time ≈ seek distance** | this is why we minimise *head movement* in cylinders |
| **Disk bandwidth** | total bytes transferred ÷ total time between the 1st request and completion of the last transfer |

So: **minimise total head movement** (a proxy for seek time), while not starving anyone, while
maximising bandwidth.

### 8.2 The running example

Every algorithm in the deck is run on the same input (S21), which is worth memorising because the
exam will reuse it:

```
request queue (cylinders 0..199):  98, 183, 37, 122, 14, 124, 65, 67
initial head position:             53
```

### 8.3 The five algorithms, with the full traces

| Algorithm | Rule | Service order from 53 | Total movement |
|---|---|---|---|
| **FCFS** | serve in arrival order | 98, 183, 37, 122, 14, 124, 65, 67 | **640** (S23) |
| **SSTF** | nearest request to the current head | 65, 67, 37, 14, 98, 122, 124, 183 | **236** (S26) |
| **SCAN** (toward 0) | sweep to the physical end, then reverse | 37, 14, 0, 65, 67, 98, 122, 124, 183 | **236** (S29) |
| **C-SCAN** | sweep up to 199, jump to 0 unserved, sweep up again | 65, 67, 98, 122, 124, 183, 199, (0), 14, 37 | **382** (S32) |
| **C-LOOK** | sweep up to the *last request*, jump to the *lowest request*, sweep up | 65, 67, 98, 122, 124, 183, (14), 37 | **322** (S35) |
| *LOOK* (not worked in the deck) | sweep only as far as the last request in that direction, then reverse | 37, 14, 65, 67, 98, 122, 124, 183 | *208* |

Each total, line by line, exactly as on the slides:

```
FCFS   45 + 85 + 146 + 85 + 108 + 110 + 59 + 2                        = 640
SSTF   12 +  2 +  30 + 23 +  84 +  24 +  2 + 59                       = 236
SCAN   16 + 23 +  14 + 65 +   2 +  31 + 24 +  2 + 59                  = 236
C-SCAN 12 +  2 +  31 + 24 +   2 +  59 + 16 + 199 + 14 + 23            = 382
C-LOOK 12 +  2 +  31 + 24 +   2 +  59 + 169 + 23                      = 322
```

### 8.4 What each algorithm is really doing

**FCFS** (S22–S23) — no reordering at all. The graph shows "wild swings back and forth": the head
goes 53 → 98 → 183 and then all the way back to 37, then to 122, then to 14. Total 640, the worst
of the five. Its virtue is fairness and simplicity: **it can never starve**.

**SSTF** (S24–S26) — always take the closest request. It is **SJF applied to seeks** (the slide says
so), and it inherits SJF's defect: **starvation**. Look at the trace — after 14 the head is stranded
at the low end (nothing left near it), so it makes one 84-cylinder jump to 98. A stream of requests
arriving just behind the head keeps the arm local forever, and 183 waits. The slide's warning is
exact: *distant requests may never be serviced*. Note also *"requests are from processes executing
concurrently"* — the queue is shared, so an unfair algorithm is a global fairness problem.

**SCAN** (S27–S29) — the **elevator algorithm**: keep going in one direction to the *end of the
disk*, then reverse. Because every request is guaranteed to be passed within one sweep, **starvation
is unlikely**, at the price of possibly long waits. Note the deck assumes the head is moving
**toward 0**, and this matters: SCAN is *not* direction-symmetric (see §8.6). Movement 236 — equal
to SSTF here, but with the fairness property SSTF lacks.

**C-SCAN** (S30–S32) — "circular": sweep low → high servicing, then fly back from 199 to 0
**without servicing**, then sweep up again. Why: pure SCAN treats the two directions unequally (a
request just behind the head waits almost two sweeps; a request just ahead waits a moment). C-SCAN
makes the wait **uniform**, because service only ever happens while travelling in one direction.
Cost: the return trip is pure waste — 199 cylinders here — which is why 382 > 236.

**C-LOOK** (S33–S35) — C-SCAN without the trip to the physical end: go only as far as the **highest
pending request (183)**, then return to the **lowest pending request (14)**, not to 0. Movement 322
instead of 382: the two "empty" stretches (183→199 and 0→14) are skipped.

**LOOK** (mentioned in S36 but never worked) — SCAN without going to the physical end: reverse at
the last pending request in that direction. Here 53 → 37 → 14 → then reverse → 65 → 67 → 98 → 122 →
124 → 183 = `16 + 23 + 51 + 2 + 31 + 24 + 2 + 59 = 208`, the best of all six. It is not in the
deck's worked set, but S36 names it ("SCAN and C-SCAN (or LOOK and C-LOOK)").

**The family tree** — the one thing to be able to reproduce:

```
                     reorder the queue?
                            |
              no -----------+----------- yes
              |                          |
            FCFS            nearest first? ---- yes ---> SSTF
                                     |
                                     no (one-directional sweep)
                                     |
                     go to the physical end? ---- yes ---> SCAN ---> one direction only? ---> C-SCAN
                                     |                                              |
                                     no (go to last request) ---> LOOK ------> C-LOOK
```

### 8.5 The two questions the slides leave open

S29 asks: *"After the head reverses direction, does it need to serve requests in the reversed
direction immediately?"*

**Answer: no.** The reversal happens at the *physical end of the disk* (cylinder 0), not at the last
request. So after reaching 0 the head starts moving up and serves whatever it encounters **in the
order it encounters it** — nearest-first is not what SCAN does; the order is fixed by geometry.
Consequence: a request at, say, cylinder 10 that arrives just after the head passed cylinder 10
going down must wait for the arm to reach 0, then come back up to 10 — nearly two full sweeps. That
asymmetry is precisely what C-SCAN removes.

S35 asks: *"Does SCAN, C-SCAN and C-LOOK really solve the starvation problem?"*

**Answer: they bound the wait, which is not the same as making it short.**

* In principle **no request starves**: because service sweeps monotonically, every pending request
  is reached within at most one sweep (SCAN: up to ~2 sweeps for a request just behind the head;
  C-SCAN / C-LOOK: at most one sweep plus the return).
* But if requests keep arriving, a request can still wait a long time; and a request that arrives
  just after the head has passed can wait almost a full extra sweep. So **starvation in the formal
  sense (indefinite postponement) is avoided; long delays are not**.
* C-SCAN / C-LOOK give *more uniform* waits than SCAN, which is their real advantage.
* SSTF is the only one of the five that can starve a request **indefinitely**.

### 8.6 Direction matters, and it changes the answer

SCAN's total depends on which way the head is already moving. Same queue, head at 53, but moving
**toward 199**:

```
65, 67, 98, 122, 124, 183, 199, then reverse: 37, 14
12 + 2 + 31 + 24 + 2 + 59 + 16 + 162 + 23 = 331
```

331, not 236. **Whenever a SCAN question is set, find the direction in the question first**; if the
question does not state one, state your assumption explicitly.

### 8.7 Choosing an algorithm (S36–S37)

| Statement (S36) | Reading |
|---|---|
| "SSTF is common and has a natural appeal" | it is the obvious greedy choice, and it is easy to implement |
| "SCAN and C-SCAN (or LOOK and C-LOOK) perform better for systems that place a heavy load on the disk (since starvation is unlikely)" | under load there *is* a queue to reorder, and fairness matters |
| "Performance depends on the number and types of requests" | **no algorithm is universally best** — see the tutorial question below |

S37 adds the coupling to `c11`: **the file-allocation method determines the request pattern, which
determines how much scheduling can help.**

| Allocation | Request pattern generated | Scheduling headroom |
|---|---|---|
| **Contiguous** | consecutive blocks → requests close together → often same/adjacent cylinder | little to exploit, but already optimal; SSTF/LOOK still help |
| **Linked** | follows a chain of scattered blocks → requests widely apart | large, but nothing can make them close |
| **Indexed** | data blocks scattered, **plus** an index block read first | large, plus an extra random access per file |

The one-sentence answer to "which allocation is best for I/O performance?": **contiguous**, because
it generates the fewest and shortest seeks. That is Tutorial 12 Q2(b).

---

## 9. Disk management (S38–S39)

Three formatting steps, in order:

| Step | Name | What it produces | Done by |
|---|---|---|---|
| 1 | **Low-level (physical) formatting** | the track/sector structure the **controller** can read and write (preamble, ECC, gap per sector) | manufacturer / `format` |
| 2 | **Partitioning** | the disk split into groups of **cylinders** (partitions) | OS / user |
| 3 | **Logical formatting ("making a file system")** | the OS's own data structures on the partition: boot block, free-space map, inodes, root directory | OS (`mkfs`) |

S39's diagram adds the vocabulary layer on top:

```
volume  --> partition --> storage device
```

A **partition** is a contiguous slice of one device. A **volume** is what the user mounts, and it can
**span partitions on different devices** (volume 3 = partition C on device 2 + partition D on
device 3). That mapping (volume → partition → device) is the layer above the file system, and it is
the only place in this deck where more than one device appears except for RAID.

---

## 10. Reliability and performance across disks (S40–S44)

### 10.1 The problem

One disk is both **too slow** (S19: 44 ms per MB sequential, 28 s random) and **too fragile** (one
head crash and the data is gone). Both problems are solved by using **several disks together** —
but the two goals need *different* arrangements, and RAID is the study of the trade-off.

### 10.2 Striping — speed (S40–S41)

* One **group of disks used as one storage unit**.
* A file is broken into blocks spread over the disks.
* Transfer is faster because blocks come in **parallel**, and because one sequential stream becomes
  `n` sequential streams.

The rule on the slide: with `n` drives, block `i` goes to drive `(i mod n) + 1`.

```
Disk #1   Disk #2   Disk #3   Disk #4
Block 0   Block 1   Block 2   Block 3
Block 4   Block 5   Block 6   Block 7
Block 8   Block 10
```

Note the omissions in the picture (`Block 9` and `Block 11` are missing) — it is illustrative only.

**Striping has no redundancy at all**: lose one disk and *every* file is damaged, because every file
has blocks on every disk. This is RAID 0.

### 10.3 Mirroring — reliability (S42)

* **Duplicate of each disk**: a logical disk = two physical disks with identical content.
* If one fails, read from the other.
* Costs **50% of the capacity** and does nothing for write bandwidth (each write is done twice).

### 10.4 RAID (S43–S44)

**RAID = Redundant Array of Independent Disks**: improve performance *and* reliability by storing
**redundant** data.

| Level | Name on slide | Speed | Redundancy | Capacity of `n` disks | Tolerates |
|---|---|---|---|---|---|
| **RAID 0** | non-redundant striping | best (read + write, n×) | **none** | 100% | **0 disks** |
| **RAID 1** | mirroring | read n×, write 1× | full duplicate | 50% | 1 per *mirror pair* |
| **RAID 0+1** | **mirror of strips** | good | mirror of a whole stripe set | 50% | 1 disk (sometimes more if lucky) |
| **RAID 1+0** | **strip of mirrors** | good | each disk mirrored | 50% | 1 per mirror pair (≥1 guaranteed) |

**The difference between 0+1 and 1+0 is only the order of the grouping** (S44), and it is the
classic exam question:

```
RAID 0+1  (mirror of strips)          RAID 1+0  (strip of mirrors)

  stripe set A: [0][1][2][3]            stripe across:  [0][1][2][3]
                   |                                       |  |  |  |
                 mirror (copy)                        mirror pairs
  stripe set B: [0][1][2][3]                          [0][1][2][3]
```

* **0+1**: first **stripe** across 4 disks, then **mirror** the stripe set onto 4 more. If *one*
  disk dies, its whole stripe set is gone and you must run from the mirror; if **any second disk in
  the other set** also dies, all data is lost. So 0+1 has a *worse* second-failure survival rate
  than 1+0.
* **1+0**: first **mirror** each disk, then **stripe** across the pairs. Each pair is independent,
  so one disk per pair can fail — for `n` disks you can lose `n/2` disks (one from each pair) and
  still run.

Mental rule: **the redundancy you construct first is the redundancy you keep.** 0+1 mirrors at the
top, so a failure takes out a whole stripe; 1+0 mirrors at the bottom, so failures are contained.

Also worth stating, since the deck stops at RAID 1+0: it never covers **RAID 4/5/6** (parity), which
is how real systems get redundancy without paying 50% capacity. Do not import that into a slide
answer, but know why parity is the next step.

---

## 11. Formula sheet

### Disk geometry

```
track capacity  = sectors_per_track × sector_size
track of block b        = b div sectors_per_track
sector offset of block b = b mod sectors_per_track
byte offset of block b  = b × sector_size
```

### Access time

```
T_access(N) = T_seek + T_rot + T_transfer
T_rot       = ½ × T_full_rotation            (average)
T_transfer  = (N / sectors_per_track) × T_full_rotation
```

With the deck's parameters (seek 10 ms, full rotation 8 ms, 512 B sector, 1024 sectors/track):

```
T_random(1 sector) = 10 + 4 + 8/1024 ≈ 14 ms
T_random(N)        = N × 14 ms                      (one positioning per sector)
T_sequential(N)    = 14 ms + (N/1024)×8 ms          (one positioning per track)
T_sequential(N, tracks) ≈ tracks × (14 ms + 8 ms)   (the slide's conservative form)
```

### Bandwidth

```
disk bandwidth = total bytes transferred / (completion time of last − arrival of first)
```

### Scheduling totals (queue `98,183,37,122,14,124,65,67`, head 53, 0–199)

```
FCFS   640      SSTF   236      SCAN→0   236      SCAN→199  331
C-SCAN 382      C-LOOK 322      LOOK     208
```

### RAID capacity

```
RAID 0   : n × C
RAID 1   : (n/2) × C          n even
RAID 0+1 : (n/2) × C          n divisible by 2; mirror of strips
RAID 1+0 : (n/2) × C          n even; strip of mirrors
```

---

## 12. Tutorial 12 — worked solutions

Source: [transcripts/02-tutorial-12-io-systems.md](transcripts/02-tutorial-12-io-systems.md).
These solutions are not from the tutorial sheet.

### Q1 — True or false

**(a) "Buffering can be used to improve I/O efficiency for files that are being written and re-read
rapidly." → FALSE (as stated).**

That sentence is verbatim the deck's definition of **caching** (S8): *"Caching — fast memory holding
copy of data — to improve I/O efficiency for files that are being written and reread rapidly."*
**Buffering** (S7) exists to cope with *speed mismatch* and *transfer-size mismatch*, and its data is
consumed, not retained for reuse. A buffer does incidentally reduce the number of device accesses
while it is being filled, which is why the statement is a plausible trap; but the mechanism that
gives the stated benefit — keeping a **copy** for a *re-read* — is the cache.

**(b) "Process will be in waiting state after performing an I/O system call if non-blocking I/O is
used." → FALSE.**

With non-blocking/asynchronous I/O the system call **returns immediately after the request is
queued** (S9), and the process **continues executing**; it is only *signalled* when the transfer
completes. Waiting is the defining property of **blocking** I/O.

**(c) "Device drivers are part of the kernel I/O subsystem." → TRUE.**

The device-driver layer is **inside the kernel** (S5) and is part of the kernel's I/O structure; its
job is to hide device differences from the device-independent I/O subsystem above it (S45). The
precise formulation: drivers are part of the **kernel**, layered **below** the kernel I/O subsystem
— so "part of the kernel I/O subsystem" is true in the loose sense (they are kernel I/O code) and
false only if you read "subsystem" as the narrow device-independent box in the S5 diagram. State the
nuance and answer **True**.

### Q2 — the read-process loop

The code alternates: `read` block (blocking, device busy, process idle) then `process` block (CPU
busy, device idle). The two resources are **never used at the same time**.

```
time  -->   | read | process | read | process |
device      |####|          |####|          |
CPU         |    |##########|    |##########|
```

**(a) How to improve it**

1. **Double buffering + asynchronous I/O** (S10, S9): issue the read for block *k+1* while
   processing block *k*. Then `period = max(t_read, t_process)` instead of `t_read + t_process`. In
   the timeline above this removes the idle gaps entirely.
2. **Read ahead / larger blocks**: fewer requests → fewer positionings. The gain is 8× to 650×
   depending on block size (S18 vs S19).
3. **Increase the multiprogramming level**: with other processes runnable, the CPU is not idle while
   this one waits — the OS hides the stall rather than removing it.
4. **Reduce the number of layers / copies** (S12): direct I/O or DMA into user buffers avoids the
   kernel→user copy.
5. Cache the file if it is re-read (S8).

**(b) Which file allocation scheme is best?**

**Contiguous allocation.** The loop reads the file **sequentially**, so contiguous allocation places
successive blocks in successive sectors on the same or adjacent cylinders: one positioning per
track instead of one per block, and the request stream that the scheduler sees is already sorted
(S37: *"a program reading a contiguously allocated file will generate requests that are close
together"*). Linked allocation forces the arm to follow a chain of scattered blocks, and indexed
allocation adds an index-block read before every data block — both produce the wide-apart requests
S37 warns about.

### Q3 — the salesman's SCAN

**(a) Was the salesman lying? → No.**

His two claims are both true *and* both useless for your program:

* SCAN reduces seek time **only if there is a queue of pending requests to reorder** (S6: the
  scheduler reorders the *per-device request queue*).
* "Queue multiple requests within a cylinder in sector order" exploits **rotational** latency, but
  only when several pending requests land on the same cylinder.

Your program reads **10 000 blocks spread randomly across the disk**, one at a time, synchronously.
So: (i) there is only one outstanding request, so there is nothing to reorder — the queue is always
of length 1; (ii) consecutive requests almost never share a cylinder, so the intra-cylinder
optimisation never triggers; (iii) successive targets are far apart, so every request is one long
seek regardless of order.

Scheduling can only **exploit locality that already exists** in the queue (S37). A random workload
has none, so the measured behaviour **is** FCFS. The salesman's implementation is fine; the workload
is the problem. (If you had issued the 10 000 reads asynchronously so they queued up, SCAN would
have helped somewhat.)

**(b) When can disk scheduling fail to help, or hurt?**

1. **Load is too light.** One outstanding request → no reordering possible → no gain.
2. **The request stream already has no seek locality** (random access over a working set larger than
   the queue), as in (a). Reordering random seeks does not reduce their total length.
3. **The access pattern is already sequential/contiguous** — the head is already moving the optimal
   way, and aggressive reordering can even *delay* a request that was about to be served.
4. **The medium has no seek cost** — SSD, RAM disk, or a fully cached file. Reordering then only
   adds CPU overhead.
5. **Queueing delay dominates.** If arrival rate ρ → 1, average response time is dominated by queue
   length, not by service order; no ordering fixes an overloaded disk.
6. **Fairness / starvation costs.** SSTF can starve (`S26`); SCAN/C-SCAN can delay a request by
   nearly two sweeps; a real-time or latency-sensitive request may be worse off than under FCFS.
7. **Scheduling overhead** — maintaining a sorted queue, and preemption/merging costs — can exceed
   the saved seek time when seeks are cheap.
8. **Write-back / caching policies** may already have changed the order (elevator queues in the
   controller, or a disk's own reordering) so the OS-level scheduler adds nothing.

### Q4 — SSTF with arrivals

Given: 200 cylinders, head starts at **0**; `seek = 20 + 0.1 × T` ms; rotational latency **2 ms**;
transfer **8 ms**.

Service at each step = `20 + 0.1·T + 2 + 8`. The only skill is: **at the moment the disk becomes
free, consider only the requests that have arrived by then**, and pick the nearest.

| # | Served (arrival, cyl) | Head before → after | T | Seek = 20+0.1T | Rot | Transfer | **Service** | Completes at |
|---|---|---|---|---|---|---|---|---|
| 1 | (0, 45) | 0 → 45 | 45 | 24.5 | 2 | 8 | **34.5** | 34.5 |
| 2 | (20, 35) | 45 → 35 | 10 | 21.0 | 2 | 8 | **31.0** | 65.5 |
| 3 | (65, 40) | 35 → 40 | 5 | 20.5 | 2 | 8 | **30.5** | 96.0 |
| 4 | (88, 35) | 40 → 35 | 5 | 20.5 | 2 | 8 | **30.5** | 126.5 |
| 5 | (30, 23) | 35 → 23 | 12 | 21.2 | 2 | 8 | **31.2** | 157.7 |
| 6 | (70, 10) | 23 → 10 | 13 | 21.3 | 2 | 8 | **31.3** | 189.0 |
| 7 | (23, 4) | 10 → 4 | 6 | 20.6 | 2 | 8 | **30.6** | 219.6 |
| 8 | (35, 50) | 4 → 50 | 46 | 24.6 | 2 | 8 | **34.6** | 254.2 |
| 9 | (50, 70) | 50 → 70 | 20 | 22.0 | 2 | 8 | **32.0** | 286.2 |
| 10 | (15, 132) | 70 → 132 | 62 | 26.2 | 2 | 8 | **36.2** | 322.4 |

**Average service time = 322.4 / 10 = 32.24 ms.**

Checks worth doing in the exam:

* **Step 1** — at t = 0 only the cylinder-45 request exists; the head is at 0, so 45 is forced.
* **Step 3** — at t = 65.5 the queue is {132, 35, 4, 23, 50, 70, 40}: distances from 35 are 97, 0, —,
  31, 12, 35, 5 → nearest is **40** (5), not 50.
* **Step 4** — request (88, 35) has *arrived* by t = 96.0, and from 40 the distance to 35 is **5**,
  so it jumps ahead of (35, 50) at distance 10. **Forgetting an arrival is the standard mistake
  here** — it is the whole difference between 32.24 ms and a wrong answer.
* **Step 8** — after serving 4, everything nearby is done, so the head makes a 46-cylinder jump to
  50; this is SSTF's weakness (and note that 132, the oldest request, is served **last** — that is
  starvation in the making).
* The total service time equals the completion time of the last request (322.4 ms) because the disk
  starts idle at t = 0 and is never idle afterwards.

If instead the question wants **average turnaround/response time** (completion − arrival), it is
`(34.5 + 50.5 + 76 + 104 + 128.5 + 154.7 + 171 + 186.6 + 218.2 + 236.4) / 10 = 135.56 ms`. Quote the
32.24 ms figure as the answer to "time to **service** a request", and mention 135.56 ms if the
question says "response/turnaround".

---

## 13. Practice problems

**P1.** Using the deck's queue (`98, 183, 37, 122, 14, 124, 65, 67`), head at 53, compute total head
movement for **LOOK** (moving toward 0 first) and for **C-SCAN moving downward** (i.e. sweep
199 → 0 servicing, then jump to 199).

**P2.** Same queue, head at 53, but the head is currently moving **toward 199**. Compute SCAN.

**P3.** With the deck's parameters (seek 10 ms, full rotation 8 ms, 512 B sectors, 1024
sectors/track), compute the time for a 64 KB transfer (a) randomly accessed as independent 512-byte
requests and (b) sequentially. What is the ratio?

**P4.** Physical block 5000 must be read. Which track is it on, and at what offset?

**P5.** A device transfers a 4 KB block in 100 ms; the process needs 10 ms to process one block.
Compare 1000 blocks with a single buffer vs double buffering, and compute the speed-up.

**P6.** A RAID array of six 1 TB disks. Give usable capacity and the failure tolerance of RAID 0,
RAID 1, RAID 0+1 and RAID 1+0.

**P7.** A disk rotates at 7200 rpm. What is the average rotational latency? What is the transfer time
for 64 sectors at 512 B/sector if the track holds 512 sectors?

### Solutions

**P1.** LOOK toward 0: 53 → 37 → 14 (reverse at the last *request*, not at 0) → 65 → 67 → 98 → 122
→ 124 → 183.

```
16 + 23 + 51 + 2 + 31 + 24 + 2 + 59 = 208
```

C-SCAN downward: 53 → 37 → 14 → 0 → (jump to 199) → 183 → 124 → 122 → 98 → 67 → 65.

```
16 + 23 + 14 + 199 + 16 + 59 + 2 + 24 + 31 + 2 + 2 = 386
```

Note how close 386 is to the upward C-SCAN's 382: the **unserviced 199-cylinder return dominates
the total**, so for C-SCAN the direction barely matters. That is exactly the uniformity C-SCAN is
bought for — contrast SCAN, where the direction changes 236 into 331 (P2).

**P2.** Moving toward 199: serve upward first, to the physical end, then reverse.

```
53 → 65 → 67 → 98 → 122 → 124 → 183 → 199 → 37 → 14
12 + 2 + 31 + 24 + 2 + 59 + 16 + 162 + 23 = 331
```

**P3.** 64 KB = 128 sectors.

```
(a) random:     128 × (10 + 4 + 8/1024) = 128 × 14.0078  ≈ 1793 ms
(b) sequential: 10 + 4 + (128/1024) × 8 = 15.0 ms
    ratio:      1793 / 15 ≈ 120×
```

(140× if you exclude seek from the sequential case; the honest figure is ~120×.)

**P4.** `1024` sectors per track, so:

```
track  = 5000 div 1024 = 4          (i.e. the 5th track)
offset = 5000 mod 1024 = 904        (sector 904 of that track)
byte offset within the track = 904 × 512 = 462 848
```

**P5.**

```
single buffer:  1000 × (100 + 10) = 110 000 ms  = 110 s
double buffer:  100 + 1000 × 100  = 100 100 ms  = 100.1 s      (first fill, then overlap)
speed-up      = 110 000 / 100 100 ≈ 1.098×
```

The device is the bottleneck, so overlap buys only ~10%. Double buffering would pay off properly only
if the processing time were comparable to 100 ms.

**P6.**

| Level | Usable | Tolerates |
|---|---|---|
| RAID 0 | **6 TB** | **0** disks — any loss destroys everything |
| RAID 1 (3 pairs) | **3 TB** | 1 disk per pair (up to 3, one from each pair) |
| RAID 0+1 (2 stripe sets of 3) | **3 TB** | 1 disk; a second loss in the other stripe set is fatal |
| RAID 1+0 (3 mirror pairs, striped) | **3 TB** | 1 disk per pair — up to 3, and at minimum 1 |

**P7.**

```
7200 rpm = 7200 / 60 = 120 rev/s  →  T_full = 1/120 s = 8.33 ms
average rotational latency = T_full / 2 = 4.17 ms
transfer time = (64/512) × 8.33 ms = 1.04 ms
```

Note how close the 8.33 ms is to the deck's 8 ms — that is where the 8 ms came from (a 7200 rpm
drive).

---

## 14. Self-test questions

1. Why does the deck say *efficiency* and *generality* are the two design objectives, and which
   layer exists to buy generality?
2. Name the six services of the kernel I/O subsystem (S45), and say which one turns random access
   into sequential access.
3. A printer "can serve only one request at a time". Which of buffering / caching / spooling fixes
   that, and why is the other two insufficient?
4. Why is a buffer not a cache? Give the one-sentence test.
5. In the blocking-I/O diagram, where exactly does the process spend its time, and what removes that
   time?
6. When does double buffering double throughput, and when does it do nothing?
7. Give the three CPU-side costs that make I/O a system-performance factor (S12).
8. Define track, cylinder, sector. Why is the cylinder a natural unit for scheduling?
9. A disk has 1024 sectors/track and 512 B sectors. How big is a track, and how many tracks does a
   1 MB file occupy if it is stored contiguously?
10. Explain with the numbers why a random 1 MB read costs 28 s but a sequential one costs 44 ms.
11. Why does the deck use 4 ms as the rotational latency when S16 says 8 ms?
12. FCFS and SSTF both give 236 vs 640 on the example queue — no, wait: which two algorithms give
    exactly 236 here, and why do they tie? Which one would you keep, and why?
13. C-SCAN moves 382 cylinders — more than SCAN's 236. Why would anyone prefer it?
14. LOOK and C-LOOK exist to fix what inefficiency in SCAN / C-SCAN?
15. The queue is fixed but SCAN's answer changes from 236 to 331. What changed?
16. Answer S29's and S35's questions in one sentence each.
17. Distinguish low-level formatting, partitioning, and logical formatting. Which one creates
    inodes?
18. With 6 disks, RAID 0+1 and RAID 1+0 both give 3 TB. Give the arrangement difference and one
    consequence.
19. Why does striping alone (RAID 0) make the system *less* reliable?
20. A workload reads 10 000 blocks at random. Will adding SCAN help? Why / why not?

---

## 15. Glossary

| Term | Meaning |
|---|---|
| **Blocking I/O** | system call returns only when the transfer completes; the process waits |
| **Asynchronous / non-blocking I/O** | system call returns once the request is queued; the process continues and is signalled on completion |
| **Buffer** | memory area holding data **in transit** between devices |
| **Cache** | fast memory holding a **copy** of data kept for reuse |
| **Spool** | queue of whole jobs for a device that serves one request at a time |
| **Device driver** | kernel code that knows one device's registers; hides device differences |
| **Controller** | the hardware unit the CPU talks to, which drives one or more devices |
| **Seek time** | time to move the arm to the target cylinder |
| **Rotational latency** | time for the target sector to spin under the head (average = ½ rotation) |
| **Transfer time** | `(N / sectors_per_track) × full rotation` |
| **Track** | one concentric circle on one platter surface |
| **Cylinder** | the same track position across all platters |
| **Sector** | smallest addressable unit on a track (512 B here) |
| **Disk bandwidth** | bytes transferred ÷ time from first request to last completion |
| **FCFS** | first-come-first-served; no reordering; never starves |
| **SSTF** | shortest-seek-time-first; greedy nearest; SJF analogue; **can starve** |
| **SCAN** | elevator: sweep to the physical end, reverse |
| **C-SCAN** | circular SCAN: sweep one way, return unserved, sweep again → uniform waits |
| **LOOK** | SCAN that reverses at the last pending request instead of the disk end |
| **C-LOOK** | C-SCAN that returns to the lowest pending request instead of cylinder 0 |
| **Low-level formatting** | laying down sectors the controller can read/write |
| **Partition** | contiguous group of cylinders on one device |
| **Logical formatting** | writing the file system's structures (`mkfs`) |
| **Volume** | what is mounted; may span partitions on several devices |
| **Striping** | spreading blocks across disks for parallel transfer (RAID 0) |
| **Mirroring** | keeping an identical copy of every disk (RAID 1) |
| **RAID** | Redundant Array of Independent Disks |
| **RAID 0+1** | mirror of strips |
| **RAID 1+0** | strip of mirrors |
