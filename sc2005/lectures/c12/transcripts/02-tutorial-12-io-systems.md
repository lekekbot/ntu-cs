# Tutorial Twelve — I/O Systems (verbatim)

Transcription of `tut12.pdf` (1 page, printed page `12-1`). Questions copied exactly. Solutions
are **not** part of the source document; they are worked in
[STUDY_GUIDE.md §12](../STUDY_GUIDE.md#12-tutorial-12--worked-solutions).

`SC2005 Operating Systems` — `TUTORIAL TWELVE` — `I/O Systems`

---

**1.** Indicate whether the following statements are true or false. Justify your answer.

a) Buffering can be used to improve I/O efficiency for files that are being written and re-read
rapidly.

b) Process will be in waiting state after performing an I/O system call if non-blocking I/O is used.

c) Device drivers are part of the kernel I/O subsystem.

---

**2.** Suppose that in a multiprogramming system, a process reads blocks of data from a file on
disk for processing. As shown below, it reads one block of data at a time to a buffer using
synchronous I/O and then processes the data.

```
while ( not end of file) {

    buffer <- read a block of data from disk using synchronous I/O;

    process data in buffer;
}
```

`[Diagram]` Beside the code: a shaded `Disk` and a `buffer` box between disk and process, with the
arrow `read a block` — one buffer, read-then-process, serially.

a) Discuss how the performance of the above process can be improved.

b) For a system running mainly with this type of processes, which file allocation scheme is best in
terms of I/O performance?

---

**3.**

a) During his presentation, a salesman emphasized on the substantial effort his company has made to
improve the performance of their UNIX version - one example he quoted was that the disk driver used
the SCAN algorithm and also queued multiple requests within a cylinder in sector order. You bought
a copy and wrote a program to randomly read 10,000 blocks spread across the disk. The performance
measured was the same as what would be expected from FCFS algorithm. Was the salesman lying?

b) Under what circumstances could a disk scheduling discipline not improve the performance or even
degrade performance of the system?

---

**4.** Assume that a disk drive has 200 cylinders, numbered 0 to 199. The disk head starts at
cylinder 0. A seek takes (20 + 0.1×T) milliseconds, where T is the number of cylinders to move.
Rotational latency is 2 milliseconds and data transfer per request takes 8 milliseconds, assuming
each request accesses the same amount of data. The following table shows the arrival time and
destination cylinder number of requests:

| Arrive Time (ms) | 0 | 15 | 20 | 23 | 30 | 35 | 50 | 65 | 70 | 88 |
|---|---|---|---|---|---|---|---|---|---|---|
| Cylinder Number | 45 | 132 | 35 | 4 | 23 | 50 | 70 | 40 | 10 | 35 |

Compute the average time to service a request using the Shortest Seek Time First (SSTF) disk head
scheduling algorithm.
