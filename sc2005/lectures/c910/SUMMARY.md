# Virtual Memory — Summary (one page)

**The premise:** a program's logical address space may be bigger than physical memory. Only the
pages needed right now are resident; the rest sit in a **backing store** on disk.

That one decision causes everything else:

```
page might not be resident  -> page fault -> disk I/O is slow
memory full on a fault      -> choose a victim      (page replacement)
more frames can mean more faults                    (Belady's anomaly)
how many frames per process?                        (frame allocation)
too few frames for everyone                         (thrashing)
```

---

## The 60-second version

1. **Swapping** moves a whole process image to/from disk; the **mid-term scheduler** decides. It
   buys multiprogramming at a huge copying cost, and forces **dynamic** address translation.
2. **Demand paging** loads a page only when referenced. A per-entry **valid–invalid bit** says whether
   the page is resident; if not, a **page fault** traps to the OS, which finds a free frame, reads
   the page in, updates the PTE, and **restarts** the instruction.
3. If no frame is free, pick a **victim**. Only **dirty** pages must be written back, so the dirty
   bit saves a disk write. Page replacement is judged by **fault count on a reference string**.
4. **FIFO** evicts the oldest page; **OPT** evicts the page used farthest in the future (unbeatable,
   unimplementable); **LRU** evicts the least recently used; **second chance/clock** approximates
   LRU with a **reference bit**.
5. **Belady's anomaly**: FIFO can fault *more* with more frames. Algorithms satisfying the
   **inclusion property** (OPT, LRU) cannot.
6. **Frame allocation** is fixed (equal/proportional) or variable; **scope** is local (own frames) or
   global (any frame). Fixed requires local; global forces variable.
7. **Thrashing** = too many processes, too few frames each: time goes to paging, CPU utilisation
   collapses. Fix with the **working-set model** (keep D ≤ m) or **PFF** (bound the fault rate);
   both may require **swapping a process out**.

---

## The algorithms

| Algorithm | Evicts | Faults (string below, 4 frames) | Notes |
|---|---|---|---|
| **FIFO** | oldest arrival | **10** | trivial; suffers Belady's anomaly |
| **OPT** | farthest future use | **6** | optimal, not implementable; benchmark |
| **LRU** | oldest last use | **8** | needs hardware support |
| **Second chance / clock** | oldest with `R = 0` | **8** | cheap LRU approximation; worst case = FIFO |

Reference string used throughout:

```
1 2 3 4 1 2 5 1 2 3 4 5
```

FIFO with **3** frames → **9** faults; with **4** frames → **10** faults. That is Belady's anomaly.

---

## Formulas

```
EAT = (1 - p) × memory access time  +  p × page fault time

WS(t) = distinct pages in the last Δ references
WSS_i = |WS_i|
D = Σ WSS_i
thrash when D > m
```

---

## Key numbers

* Page-fault time ≫ memory access time, so even a tiny fault rate dominates EAT.
  Example: 100 ns memory, 10 ms fault, p = 10⁻⁴ → EAT ≈ 1.1 µs (≈ 11× slower).
* Fault with a full memory = **two** disk I/Os (write dirty victim + read missing page).
* Working-set example: Δ = 10 → WS(t₁) = {1,2,5,6,7}, WS(t₂) = {3,4}.

---

## Ten things that decide exam marks

1. A page fault is a **reference to a non-resident page**, not an error.
2. **Valid bit V** → entry holds a frame number; **I** → holds a disk address.
3. The faulting **instruction is restarted** after the page is loaded.
4. Only **dirty** victims are written back.
5. FIFO = arrival order; LRU = last-use order; OPT = future-use order.
6. **OPT is the lower bound**, never a real implementation.
7. **Belady's anomaly** belongs to **FIFO**; the cure is the **inclusion property**.
8. **Fixed allocation ⇒ local replacement**; global replacement implies variable allocation.
9. **Global replacement** makes one process's performance depend on the others'.
10. Thrashing is a **frame-shortage** problem, not a disk-speed problem — adding processes makes it
    worse.

---

## What is *not* in this series

* Segmentation, paging mechanics and address translation — that is [`../c89`](../c89).
* File systems — now covered in [`../c11`](../c11) (directories, block allocation, inode,
  free-space management). Disk scheduling, I/O systems and RAID are in [`../c12`](../c12).
* Copy-on-write and memory-mapped files are not discussed in these recordings.
