# File Systems — Summary (one page)

Four lectures, one question: **how does a named byte stream become blocks on a disk, and what does
the bookkeeping cost?**

---

## The 60-second version

1. A **file** is a named, long-lived, shareable collection of information on secondary storage. Its
   **attributes (metadata)** — name, type, location, size, protection, time, owner — live in a
   **directory entry**, and a **directory is itself a special file** on the disk.
2. The file system is **layered**: **logical file system** (metadata, directories, operations,
   protection) → **file organization module** (space allocation, free space, logical→physical
   translation) → **basic file system** (buffers, generic device commands) → **I/O control**
   (driver, interrupts).
3. The OS treats a file as an **unstructured, byte-addressable stream** starting at 0. Turning a
   structured file into that stream (**record-stream translation**) is the **application's** job;
   cutting the stream into blocks (**stream-block translation**) is the **OS's**.
4. Access is **sequential** or **direct (random)**. The six operations are create, delete, open,
   close, write, read. `open()` exists for **efficiency**: it caches the file's disk location in the
   **open file table** so read/write need not re-read the directory.
5. Directories form a **tree**; **path names** (absolute from root, relative from cwd) make files
   unique. **Links** let two entries name one physical file — **symbolic** (entry holds the path,
   slower, always consistent) or **hard** (entry duplicates the attributes, faster, needs a link
   count). Links break the tree and create **traversal** and **dangling-pointer** problems.
6. **Protection** in Unix is nine bits: **owner / group / public** × **rwx**. On a **directory**,
   `r` = list, `w` = insert/delete entries, and **`x` is a prerequisite for both**.
7. The **two-level open file table** splits per-process state (**current position**, permission,
   pointer) from system-wide state (**cached FCB**, open count). `open()` returns the **file
   descriptor** = index into the per-process table.
8. **Allocation**: **contiguous** (`start + i`, fast, external fragmentation), **linked** (chain of
   blocks, no fragmentation, poor random access), **indexed** (index block, good random access, an
   extra block + I/O). Unix uses the **inode** — 12 direct + single/double/triple indirect.
9. **Free space**: a **bitmap** (1 bit/block, cacheable, but scanning is expensive) or a **linked
   list** (almost no space, but every allocation must read the block to follow the pointer).

---

## The three allocation methods

| | **Contiguous** | **Linked** | **Indexed** |
|---|---|---|---|
| Directory entry | start block (+ length) | first block | index block |
| Logical block *i* | `start + i` | walk *i* hops | `index[i]` |
| Direct access | **excellent** | poor | good |
| External frag. | **yes** | no | no |
| Extra cost | must find a hole; growth constrained | pointer per block; chain walk | index block per file; +1 I/O |

Effective block size for **linked** = `block − pointer`; the displacement is shifted by the pointer
size.

---

## Formulas

Let \(x\) be the byte offset, \(S\) the block size, \(p\) the pointer size, and
\(B\) the block size used by an inode.

### Logical-to-physical translation

$$
\begin{aligned}
q &= \left\lfloor \frac{x}{S} \right\rfloor
&\qquad r &= x \bmod S
\end{aligned}
$$

| Allocation | Translation |
|---|---|
| **Contiguous** | \(\text{physical block} = \text{start} + q\) |
| **Linked** | Walk the chain \(q\) times; each block has \(S-p\) data bytes |
| **Indexed** | \(\text{physical block} = \text{index\_block}[q]\) |

For linked allocation:

$$
\begin{aligned}
S_{\mathrm{eff}} &= S-p \\
q &= \left\lfloor \frac{x}{S_{\mathrm{eff}}} \right\rfloor
&\qquad \text{displacement} &= (x\bmod S_{\mathrm{eff}})+p
\end{aligned}
$$

### Inode and bitmap sizing

$$
\begin{aligned}
E &= \frac{B}{p}
&&\text{entries per index or indirect block} \\
C_{\mathrm{inode}} &= 12B + EB + E^2B + E^3B
&&\text{maximum inode data capacity} \\
\text{bitmap bytes} &= \frac{\text{disk size}}{8B}
&&\text{one bit per disk block}
\end{aligned}
$$

The inode formula assumes 12 direct pointers plus single-, double-, and triple-indirect
pointers.

---

## Worked numbers worth remembering

**Contiguous (part 03).** File `mail` starts at block 19, 6 blocks. Byte 2333, block 512:
`2333 div 512 = 4`, remainder **285** → logical block 4 → physical **19 + 4 = 23**.

**Linked (part 03).** Block 512, pointer 4 → `S_eff = 508`. `2333 div 508 = 4`, remainder 301 →
displacement `301 + 4 =` **305**. Chain 0→9, 1→16, 2→1, 3→10, 4→**25**.

**Indexed (part 03).** Max file 128 KB = 2^17, block 512 = 2^9 → 2^8 = 256 blocks; 128 entries per
index block → **2 index blocks**. Byte 2333 → entry 4 → physical block 5.

**Inode capacity (part 03).** 4 B pointers, 4 KB block → `E = 1024`.
```
12 direct          = 48 KB
single indirect    = 2^10 × 4 KB = 4 MB   (2^22)
double indirect    = 2^10 × 4 MB = 4 GB   (2^32)
triple indirect    = 2^10 × 4 GB = 4 TB   (2^42)
```
Lecture: direct = **48 K**; direct + single = **48 K + 2^22**; with double indirect it is
"extremely large".

**Inode example (part 03).** 6 direct pointers, block 1000 B, position 5900, read 200 B:
`5900 div 1000 = 5`, remainder 900 → **block 5** (100 bytes, last direct pointer) + **block 6**
(100 bytes, first indirect entry).

**Bitmap (part 04).** 16 GB disk, 512 B blocks → `2^34 / 2^9 = 2^25` blocks → `2^25` bits →
`2^22` bytes = **4 MB**.

---

## Ten things that decide exam marks

1. **Attributes = metadata**, stored in a **directory entry**; the directory is itself a file.
2. **Record-stream translation is the application's job**, not the OS's.
3. `open()` is about **efficiency**, not permission — it caches the disk location.
4. **fd = index into the per-process open file table**; the system-wide table is shared.
5. Two processes opening the same file get **two** per-process entries and **one** system-wide entry
   → **separate position pointers**.
6. **Symbolic link = path name** (indirection, extra access time); **hard link = duplicated
   attributes** (no indirection, consistency problem).
7. On a **directory**, **`x` gates `r` and `w`**.
8. `q = x div S` first, **always** — then apply the method.
9. **Linked allocation's effective block size is smaller** than the block, and the displacement is
   shifted by the pointer size.
10. Inode levels multiply capacity by **E each time**; memorise the **method**, not "4 TB".

---

## What is *not* in this series

* Disk scheduling, disk structure/RAID, I/O hardware — separate topics.
* The **basic file system** and **I/O control** layers are named but explicitly left to the I/O
  lectures.
* Single-level and two-level **directory structures** are not discussed; part 01 jumps from
  entry layout to the **tree**.
* File-system implementation internals beyond the inode (superblock, cylinder groups, journals).
