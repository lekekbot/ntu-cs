# Part 10 — I/O System & Disk (slide transcript)

Verbatim transcription of `IO and Disk.pdf`, 46 slides. Each section is one slide.

* **Slide number** — `S<n>` is the *page* in the PDF (1–46). The printed footer (`10.<n>`) is given
  too, because on two slides it does not match the page order (see [NOTES.md](../NOTES.md) §3).
* **Slide text** — copied exactly, including typos and odd spacing (`reread`, `Double Buffer`,
  `1 K sectors per track`). Nothing is paraphrased.
* **`[Diagram]`** — description of the figure on the slide, since the figure carries content the
  text does not. Numbers quoted in a diagram are read off the slide.

Header on every slide: `I/O System & Disk` — `SC2005/CE2005/CZ2005 Operating Systems`.

---

## S1 — footer `10.1` — title / roadmap

`Part 10:  I/O System & Disk`

* I/O Hardware
* I/O System Design and Implementation
  * Design Objectives
  * Kernel I/O Structure
  * Kernel I/O Subsystem
  * Performance Consideration
* Disk
  * Disk Structure
  * Disk Scheduling

    `FCFS, SSTF, SCAN, C-SCAN, C-LOOK`
  * Disk Management
  * Disk Reliability

---

## S2 — footer `10.2` — I/O Hardware

`I/O Hardware`

`[Diagram]` Classic PC bus topology, three buses:

```
  monitor        processor            cache    memory
      |              |                  |        |
  graphics        +--+--- bridge/memory controller ---+
  controller      |                                     |
      |           |                                     |
      +-----------(========= PCI bus ===================+
                  |            |                  |
             SCSI controller   |            IDE disk controller
                  |     expansion bus interface     |
             SCSI bus      expansion bus            |
                  |            |                     |
            4 × disk    parallel port,         2 × disk
                        serial port, keyboard
```

Label `PCI bus` runs horizontally under processor/cache/memory; the `bridge/memory controller`
joins processor, cache, memory and the PCI bus.

---

## S3 — footer `10.3` — I/O Hardware (device variety)

`I/O Hardware`

* Devices vary in many dimensions

`[Diagram]` A six-row classification table.

| aspect | variation | example |
|---|---|---|
| data-transfer mode | character / block | terminal / disk |
| access method | sequential / random | modem / CD-ROM |
| transfer schedule | synchronous / asynchronous | tape / keyboard |
| sharing | dedicated / shared | tape / keyboard |
| device speed | latency, seek time, transfer rate, delay between operations | — |
| I/O direction | read only / write only / read–write | CD-ROM / graphics controller / disk |

---

## S4 — footer `10.4` — I/O System Design Objectives

`I/O System Design Objectives`

* Efficiency
  * Important because I/O operations often form a bottleneck
  * Most I/O devices are extremely slow compared with main memory and the processor
  * The area that has received the most attention is disk I/O
* Generality
  * Desirable to handle all devices in a uniform manner
  * Applies to the way processes view I/O devices and the way the operating system manages I/O
    devices and operations

---

## S5 — footer `10.5` — Kernel I/O Structure

`Kernel I/O Structure`

`[Diagram]` Layering diagram, top to bottom:

```
+-------------------------------------------------------------+
| kernel  +------------------------------------------------+  |
|         |          kernel I/O subsystem                    |  |
|         +------------------------------------------------+  |
+-------------------------------------------------------------+
   SCSI     keyboard   mouse    ...   PCI bus   floppy   ATAPI
   device   device     device         device    device   device
   driver   driver     driver         driver    driver   driver      <- "I/O request"
   ------------------------------------------------------------
   SCSI     keyboard   mouse    ...   PCI bus   floppy   ATAPI
   device   device     device         device    device   device
   controller ...                                                 <- "hardware"
   ------------------------------------------------------------
   SCSI     keyboard   mouse    ...   PCI bus   floppy   ATAPI devices
   devices                                        drives  (disks, tapes, drives)
```

Vertical lines join each driver to its controller. Left-hand braces label the driver row
`I/O request` and the controller/device rows `hardware`.

---

## S6 — footer `10.6` — Kernel I/O Subsystem: I/O scheduling

`Kernel I/O Subsystem`

* I/O Scheduling
  * Schedule I/O request through rearranging the order of service, e.g. disk scheduling
  * Can improve the system efficiency

`[Diagram]` `process` → `request queue` (three processes, three queues; the top queue is also
linked to a `Free list`) → per-device request queues labelled `FCFS` (two overlapping queues drawn)
→ `disk`; a separate `Terminal` box hangs off the same structure. Shows scheduling as *reordering
the per-device queue*.

---

## S7 — footer `10.7` — Kernel I/O Subsystem: buffering

`Kernel I/O Subsystem`

* Buffering
  * Store data in memory while transferring between devices
  * To cope with device speed mismatch
  * To cope with device transfer size mismatch, e.g. in networking

`[Diagram]` Bar chart of data-transfer time per layer for several devices (disk, modem, network …),
with braces marking `device driver` and `kernel`; illustrates how much of a request's time is spent
in each layer.

---

## S8 — footer `10.8` — Kernel I/O Subsystem: caching, spooling

`Kernel I/O Subsystem`

* Caching
  * Fast memory holding copy of data
  * To improve I/O efficiency for files that are being written and reread rapidly.
* Spooling
  * Hold output for a device
  * Used in device that can serve only one request at a time, e.g. printing

---

## S9 — footer `10.9` — Performance Consideration: blocking vs asynchronous

`Performance Consideration`

* Application I/O Interface

`[Diagram]` Two side-by-side timelines, `user land` above `kernel`, time flowing downwards.
Stack, top to bottom: requesting process → device driver → interrupt handler → hardware
(controller) → device.

**(a) Blocking I/O**

1. A process makes an I/O request and the request is sent to the I/O device where it is processed.
2. The process is in the waiting state while the request is being processed by I/O device.
3. The process is put back to the ready queue when the I/O request is completed.

**(b) Asynchronous I/O**

1. A process makes an I/O request and the request is sent to the I/O device where it is processed.
2. The system call returns after the request is queued at I/O device.
3. The requesting process continues to execute its code while the request is being processed by I/O
   device.
4. When the I/O completes, the requesting process is signaled.

---

## S10 — footer printed as `10.13` — Performance Consideration: double buffer

`Performance Consideration`

* Using asynchronous I/O and double-buffer to improve performance

`[Diagram]`

```
  I/O Device --- In ---> Double Buffer --- Move ---> User Process
                             b1 | b2
```

`b1` and `b2` are two buffers between device and process; while the device fills one, the process
drains the other.

---

## S11 — footer printed as `10.11` — Performance Consideration: request lifecycle

`[Diagram]` One tall timeline with numbered markers 1–10 down the page, columns labelled
`user land`, `kernel`, `hardware`. Annotations on the arrows, in order:

* `system call`
* `I/O subsystem`
* `device driver` — `request to device driver; block, allowing another process to run`
* `interrupt handler` — `device driver requests device controller to perform operation`
* `device controller` — `perform operation, data changes to I/O subsystem`
* `required I/O` / `remaining I/O`
* `data transfer`
* `I/O complete, generate interrupt` — `release internal space in device driver, and make another
  operation`
* `I/O completes, data available in buffer` — `operate hardware, interrupt device`
* `return from system call` — `perform I/O`

This slide has no bullet text of its own; it is the annotated version of the S9 blocking path.

---

## S12 — footer `10.12` — Performance Consideration: why I/O costs

`Performance Consideration`

* I/O is a major factor in system performance
  * It demands CPU to execute device driver code
  * Context switches due to interrupts may stress CPU
  * Data copying between I/O controllers and physical memory also affect system performance.

---

## S13 — footer `10.13` — roadmap repeated

`Part 7:  I/O System & Disk`

* I/O Hardware
* I/O System Design and Implementation
  * Design Objectives
  * Kernel I/O Structure
  * Kernel I/O Subsystem
  * Performance Consideration
* Disk
  * Disk Structure
  * Disk Scheduling

    `FCFS, SSTF, SCAN, C-SCAN, C-LOOK`
  * Disk Management
  * Disk Reliability

Identical to S1 — a section divider. The `Part 7` is a copy-paste slip (S1 says `Part 10`).

---

## S14 — footer `10.14` — Disk Structure (photograph)

`Disk Structure`

`[Diagram]` Photograph of an opened hard disk: stacked `Platters`, an actuator carrying `Disk
heads` over the platter surfaces, and the label `Sectors (1 sector = 512 bytes)`.

---

## S15 — footer `10.15` — Disk Structure (geometry, block mapping)

`Disk Structure`

* Disk drives are addressed as large 1-dimensional arrays of physical blocks, where the physical
  block is the smallest unit of transfer (usually 512 bytes)
* The array of physical blocks is mapped into the sectors of the disk sequentially

`[Diagram]` Cross-section of a drive: `platter` on a `spindle`, `arm assembly` ending in a
`read-write head`, `rotation` arrow. Concentric `track t` circles on the platter surface; a
`cylinder c` drawn as a vertical column through several platters at the same radius; `sector s`
highlighted as a wedge on `track t`.

The point of the figure: a **cylinder** is the same track across all platters, which is why
"cylinder" is the unit used in disk scheduling.

---

## S16 — footer `10.16` — Disk I/O: positioning time

`Disk I/O`

* To read a requested sector, disk drive needs to position the disk head and perform data transfer.
* Position time has two major components
  * Seek time for the disk to move the heads to the track containing the desired sector (5 -25
    milliseconds)
  * Rotational latency for the disk to rotate the desired sector to the disk head (8 milliseconds)

`[Diagram]` Top view of one platter with concentric `Track` circles and one `Sector` shaded. An
orange curved arrow labelled `seek` moves the head radially (track to track); a blue curved arrow
labelled `rotation` follows the disc's spin (sector to under-the-head).

---

## S17 — footer `10.17` — Disk I/O: the formulas and the parameters

`Disk I/O (Cont.)`

* How long to read or write N sectors?
* Positioning Time + Data Transfer Time (N)
* Positioning time: Seek Time + Rotational Latency
* Transfer time: (N / Number of Sectors per Track) × Full Rotation Time
* Some parameters:
  * Seek time: 10 ms
  * Full rotational time: 8 ms (Rotational latency: 4 ms)
  * Sector size: 512 Bytes
  * Track size: 1 K sectors per track

---

## S18 — footer `10.18` — Disk I/O: random requests

`Disk I/O (Cont.)`

* Random Request
  * Seek Time + Rotational Latency + Transfer Time

    `10 ms + 4 ms + (1/1024) × 8ms = ∼14 ms`
* Time and bandwidth for random request of size:
  * 4 KB = 8 sectors = 8 * 14 ms = 112 ms
  * 128 KB = 256 sectors = 256 * 14 ms = 3.5 secs
  * 1 MB = 2048 sectors = 2048 * 14 ms = 28 seconds !!

`[Diagram]` Small inset legend, orange rule: `Seek time: 10 ms`, `Full rotational time: 8 ms
(Rotational latency: ~4 ms)`, `Sector size: 0.5 KB`, `Track size: … sectors per track` (the last
line is illegible/differs across S18/S19 — see [NOTES.md](../NOTES.md) §3). Below it, a top view of
a platter with a green head on an actuator arm.

---

## S19 — footer `10.19` — Disk I/O: sequential requests

`Disk I/O (Cont.)`

* Sequential Request
  * 4KB? 8 sectors
    * 1 positioning time = 14 ms
    * Transfer time = (8 / 1024) × full rotational time = 0.0625 ms
    * Total = ~14 ms
  * 128 KB? 256 sectors
    * Still fits in a track, hence 1 positioning time = 14 ms
    * Transfer time = (256 / 1024) × full rotational time = 2 ms
    * Total = 16 ms
  * 1 MB? 2048 sectors
    * Does not fit in a track, fits in 2 tracks (at best) or 3 tracks (at worst).
    * Read one track: positioning time + full rotation time = 14 ms + 8 ms = 22 ms
    * Read two tracks: 2 * 22 ms = 44 ms (vs. 28 seconds of random I/Os)

`[Diagram]` Same inset legend as S18, plus a top view of a platter (blue tracks, green head); the
figure shows the whole set of sectors lying on one track.

---

## S20 — footer `10.20` — Disk Scheduling

`Disk Scheduling`

* The OS is responsible for using hardware efficiently — for disk drives this means having a fast
  access time and high disk bandwidth
* Minimize seek time
* Seek time ≈ seek distance
* Disk bandwidth is the total number of bytes transferred, divided by the total time between the
  1st request and completion of the last transfer

---

## S21 — footer `10.21` — Disk Scheduling: the example

`Disk Scheduling (Cont.)`

* Several algorithms exist to schedule the servicing of disk I/O requests
* We illustrate them with a request queue (0 -199)

  `98, 183, 37, 122, 14, 124, 65, 67`
* Assume that head is initially at cylinder 53

---

## S22 — footer `10.22` — FCFS (graph)

`First-Come-First-Served (FCFS)`

`[Diagram]` Cylinder axis 0–199 with ticks at `0, 14, 37, 53, 65, 67, 98, 122, 124, 183, 199`;
`queue = 98, 183, 37, 122, 14, 124, 65, 67`; `head starts at 53`. Red polyline: one vertical step
per request, time running downwards. The path zig-zags across the whole surface (53 → 98 → 183 → 37
→ 122 → 14 → 124 → 65 → 67).

---

## S23 — footer `10.23` — FCFS (calculation)

`FCFS (Cont.)`

Total head movement =

`|98 - 53| + |183 - 98| + |37 - 183| + |122 - 37| + |14 -122| + |124 -14| + |65 -124| + |67 - 65|`

`= 640`

Problem: FCFS may have wild swings back and forth!

---

## S24 — footer `10.24` — SSTF (definition)

`Shortest-Seek-Time-First (SSTF)`

* Selects the request with the minimum seek time from the current head position
* SSTF scheduling is a form of SJF scheduling; may have starvation under heavy load, since distant
  requests may never be serviced
* Note: requests are from processes executing concurrently

---

## S25 — footer `10.25` — SSTF (graph)

`SSTF (Cont.)`

`[Diagram]` Same axis and queue as S22. Red polyline now stays near the head: 53 → 65 → 67 → 37 →
14, then one long jump 14 → 98, then 122 → 124, then a long jump to 183.

---

## S26 — footer `10.26` — SSTF (calculation)

`SSTF (Cont.)`

Total head movement =

`|65 - 53| + |67 - 65| + |37 - 67| + |14 - 37| + |98 -14| + |122 - 98| + |124 - 122| + |183 - 124|`

`= 236`

Problem: SSTF may cause starvation!

---

## S27 — footer `10.27` — SCAN (definition)

`SCAN`

* Disk arm starts at one end of the disk, and moves toward the other end, servicing requests until
  it gets to the other end of the disk, where the head movement is reversed and servicing continues
* Also called the elevator algorithm
* Assuming here the head is moving toward 0
* Starvation unlikely but servicing requests may be delayed

---

## S28 — footer `10.28` — SCAN (graph)

`SCAN (Cont.)`

`[Diagram]` Same axis and queue. Red polyline descends 53 → 37 → 14 → 0 (the end of the disk),
then reverses and climbs 65 → 67 → 98 → 122 → 124 → 183.

---

## S29 — footer `10.29` — SCAN (calculation + question)

`SCAN (Cont.)`

Total head movement =

`|37 - 53| + |14 - 37| + |0 - 14| + |65 - 0| + |67 - 65| + |98 - 67| + |122 - 98| + |124 - 122| + |183 - 124|`

`= 236`

`After the head reverses direction, does it needs to serve requests in the reversed direction
immediately?`

---

## S30 — footer `10.30` — C-SCAN (definition)

`Circular-Scan (C-SCAN)`

* Head moves from low end to high end of the disk, servicing requests along
* When reaching the high end, head immediately returns to the beginning of the disk, without
  servicing any requests

---

## S31 — footer `10.31` — C-SCAN (graph)

`C-SCAN (Cont.)`

`[Diagram]` Same axis and queue. Red polyline climbs 53 → 65 → 67 → 98 → 122 → 124 → 183 → 199,
then a long straight segment from 199 back to 0 (drawn as travel, no servicing), then climbs 0 → 14
→ 37.

---

## S32 — footer `10.32` — C-SCAN (calculation)

`C-SCAN (Cont.)`

Total head movement =

`|65 - 53| + |67 - 65| + |98 - 67| + |122 - 98| + |124 - 122| + |183 -124| + |199 - 183| + |0 -199| + |14 - 0| + |37 -14|`

`= 382`

---

## S33 — footer `10.33` — C-LOOK (definition)

`C-LOOK`

* Version of C-SCAN
* Head moves from low end to high end of the disk, servicing requests along
* When reaching the last request, head returns immediately to the lowest cylinder # request
* From there it services the requests towards the high end of the disk

---

## S34 — footer `10.34` — C-LOOK (graph)

`C-LOOK (Cont.)`

`[Diagram]` Same axis and queue. Red polyline climbs 53 → 65 → 67 → 98 → 122 → 124 → 183, then
returns straight from 183 to 14 (the lowest request, *not* to cylinder 0), then climbs 14 → 37.

---

## S35 — footer `10.35` — C-LOOK (calculation + question)

`C-LOOK (Cont.)`

Total head movement =

`|65 - 53| + |67 - 65| + |98 - 67| + |122 - 98| + |124 -122| + |183 -124| + |14 -183| + |37 - 14|`

`= 322`

`Does SCAN, C-SCAN and C-LOOK really solve the starvation problem?`

---

## S36 — footer `10.36` — Selecting a Disk-Scheduling Algorithm

`Selecting a Disk-Scheduling Algorithm`

* SSTF is common and has a natural appeal
* SCAN and C-SCAN (or LOOK and C-LOOK) perform better for systems that place a heavy load on the
  disk (since starvation is unlikely)
* Performance depends on the number and types of requests

---

## S37 — footer `10.37` — Selecting an algorithm: file allocation interacts

`Selecting a Disk-Scheduling Algorithm (Cont.)`

* Requests for disk service can be influenced by the file-allocation method:
  * A program reading a contiguously allocated file will generate requests that are close together
  * A linked or indexed file, may generate requests that are widely apart, resulting in greater
    head movement

---

## S38 — footer `10.38` — Disk Management

`Disk Management`

* Low-level formatting (physical formatting) — Dividing a disk into sectors that the disk
  controller can read and write
* To use a disk to hold files, the OS needs to record its own data structures on the disk.
  Two steps:
  * Partition the disk into one or more groups of cylinders
  * Logical formatting or “making a file system”

---

## S39 — footer `10.39` — Disk Management (diagram)

`Disk Management (Cont.)`

`[Diagram]` Volumes over partitions over storage devices:

```
 volume 1 --> partition A \
 volume 2 --> partition B /  storage device 1
                             each division holds: [directory][files]

 volume 3 --> partition C ---- storage device 2   [directory][files]
             partition D ---- storage device 3
```

Shows that a **volume** (what the user mounts) can span **partitions** which may live on different
**storage devices**.

---

## S40 — footer `10.40` — Disk Reliability: striping

`Disk Reliability`

* Several improvements in disk-use techniques involve multiple disks working cooperatively
* Disk striping uses a group of disks as one storage unit
  * Each file is broken into several blocks, which are stored on different disks
  * Time to transfer a file into memory is faster because blocks can be transferred in parallel

---

## S41 — footer `10.41` — Disk Reliability: striping diagram

`Disk Reliability (cont.)`

`[Diagram]` `System` → `RAID Controller` → four disks.

| Disk #1 | Disk #2 | Disk #3 | Disk #4 |
|---|---|---|---|
| Block 0 | Block 1 | Block 2 | Block 3 |
| Block 4 | Block 5 | Block 6 | Block 7 |
| Block 8 | Block 10 | | |

`with n drives, block i of a file stores on drive (i mod n) + 1`

---

## S42 — footer `10.42` — Disk Reliability: mirroring

`Disk Reliability (cont.)`

* Mirroring keeps duplicate of each disk
  * A logical disk consists of two physical disks
  * If one fails, the data can be read from the other

`[Diagram]` `System` → `RAID Controller` → `Disk #1` and `Disk #2`, each labelled
`File 1, File 2, File 3 ...` — the same content on both.

---

## S43 — footer `10.43` — Disk Reliability: RAID

`Disk Reliability (cont.)`

* RAID (Redundant-Array-of-Independent-Disks) improves performance and reliability of the storage
  system by storing redundant data
  * RAID 0: non-redundant striping
  * Mirroring (RAID 1) keeps duplicate of each disk
  * Mirror of Strip (RAID 0+1) or Strip of Mirrors (RAID 1+0) provides high performance and high
    reliability

---

## S44 — footer `10.44` — Disk Reliability: RAID 0+1 vs 1+0

`Disk Reliability (cont.)`

`[Diagram]`

```
a) RAID 0 + 1  with a single disk failure.      b) RAID 1 + 0  with a single disk failure.

  stripe: [0][1][2][3]                            stripe ---------> across
             |  mirror (all four)                   [0][1][2][3]
  stripe: [0][1][2][3]                              |  |  |  |
                                                   mirror |  |  |   (one mirror per disk)
                                                      [0][1][2][3]
```

Grouping is the whole point: in **0+1** you stripe first, then mirror the *stripe set*; in **1+0**
you mirror first, then stripe across the *mirror pairs*. Disk icons at the bottom of (b) show one
physical disk per block column.

---

## S45 — footer `10.45` — Summary (I/O system)

`Summary`

* Device-driver layer hides the differences among device controllers from the I/O subsystem of the
  kernel.
* The I/O subsystem provides functions for: I/O scheduling, buffering, spooling, error handling,
  device reservation, and device name translation.
* I/O system calls are costly in terms of CPU consumption, because of the many layers of software
  between a physical device and the application.

---

## S46 — footer `10.46` — Summary (disk)

`Summary`

* Disk scheduling algorithms optimize seek time:
  * FCFS, SSTF, SCAN, C-SCAN, C-LOOK
* Disk management requires disk partitioning and formatting
* Disk striping improve performance
* Mirroring improves reliability
