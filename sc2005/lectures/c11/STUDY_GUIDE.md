# SC2005 — File Systems: Study Guide

Companion to the four recordings in this folder. Timestamps refer to the transcript of the part
named, e.g. **`03 @ 10:51`** means part 03, 10 min 51 s.

Transcripts: [01](transcripts/01-file-system-1-user-view-attributes-and-directories.txt) ·
[02](transcripts/02-file-system-2-file-protection-and-open-file-table.txt) ·
[03](transcripts/03-file-system-3-allocation-methods-and-unix-inode.txt) ·
[04](transcripts/04-file-system-4-free-space-management.txt)

---

## 0. The chapter in one picture

`c89` answered *how a process's memory is laid out*; `c910` answered *how to pretend memory is
bigger than it is*. Both ended the same way: something has to live on **secondary storage**. This
chapter is about the component that organises that storage.

```
                        a user wants:  "my data, by name, forever, shared"
                                              |
                        +---------------------+---------------------+
                        |                                           |
                 WHAT the user sees                          WHERE it lives
                 (logical file system)                       (file organization module)
                        |                                           |
        file = named byte stream                        logical blocks -> physical blocks
        attributes / metadata                           contiguous | linked | indexed (inode)
        directories, links, path names                  free-space bitmap | linked list
        protection (rwx), open file table
                        |                                           |
                        +---------------------+---------------------+
                                              |
                                    HOW the bytes move
                                    (basic file system + I/O control)
                                    buffers, caches, device driver, interrupts
```

Everything in the four recordings follows from one chain:

```
a file is a named, long-lived, shareable byte stream
      => it needs METADATA (name, type, location, size, protection)
      => metadata lives in a DIRECTORY ENTRY        (part 01)
      => names need structure: directories, paths, links   (part 01)
      => sharing needs PROTECTION and an OPEN FILE TABLE   (part 02)
      => the disk is block-oriented, so bytes must be cut into LOGICAL BLOCKS
      => who owns which PHYSICAL BLOCK?              -> allocation method (part 03)
      => which blocks are still free?                -> free-space management (part 04)
```

Parts of the series:

| Part | Topic | Transcript |
|---|---|---|
| 01 | File concept, the layered file system, attributes, record/stream translation, access methods, file operations, open file table, directories, links, directory operations | [01](transcripts/01-file-system-1-user-view-attributes-and-directories.txt) |
| 02 | **File protection** (Unix owner/group/public) and the **two-level open file table** — supplementary recording | [02](transcripts/02-file-system-2-file-protection-and-open-file-table.txt) |
| 03 | **Allocation methods**: contiguous, linked, indexed; address translation; the Unix **inode** | [03](transcripts/03-file-system-3-allocation-methods-and-unix-inode.txt) |
| 04 | **Free-space management**: block-size trade-off, bitmap, linked list — supplementary recording | [04](transcripts/04-file-system-4-free-space-management.txt) |

---

## 1. What a file is (part 01, 00:13)

> A **file** is a named collection of related information recorded on secondary storage.

The lecture gives two defining properties (01 @ 00:13):

| Property | Meaning |
|---|---|
| **Long-term existence** | It survives power-off. Files live on the hard disk, not in memory. |
| **Shareable** | Several processes/users may use it at the same time. |

Because it is shared, a file also carries **a name** and **protection information** —
*specifies who is allowed to do what on the file*.

### 1.1 Why the OS needs a file system

A hard disk gives you **blocks addressed by number**. A user wants **names, directories, sizes,
permissions, sequential or random access, sharing**. The file system is the **resource abstraction**
that bridges the two (`01 @ 00:13`).

### 1.2 The four layers (01 @ 01:28 – 05:08)

| Layer | Responsibility | Recorded in |
|---|---|---|
| **Logical file system** | Manages **file attributes (metadata)**. Attributes form a **directory entry**; a directory contains one entry per file. Manages the **directory structure** (searching), supports **file and directory operations** (create, delete, read, write), and enforces **protection and security** | parts 01, 02 |
| **File organization module** | (1) **File space allocation** — which blocks a file gets; (2) **free-space management** — which blocks are available; (3) **translation of logical block address → physical block address** | parts 03, 04 |
| **Basic file system** | Buffers and caches; issues **generic commands** to the device drivers to read/write physical blocks | *not recorded* ("covered in I/O") |
| **I/O control** | Device driver + interrupt handler; performs the **actual transfer** | *not recorded* |

Two consequences worth memorising:

* **Operations are issued in *logical* block addresses.** The upper layer never knows where the
  data physically is. The file organization module is the *only* layer that translates.
* **The logical file system owns metadata; the file organization module owns space.**

> **Exam framing.** If a question asks "which layer does X?", answer with the *responsibility*, not
> the layer number: metadata/names/permissions → logical file system; block placement/free space →
> file organization module; buffering/device commands → basic file system / I/O control.

### 1.3 File attributes = metadata (01 @ 05:08)

| Attribute | Example |
|---|---|
| **Name** | the human-readable identifier |
| **Type** | needed for systems that support several types |
| **Location** | where on the disk the file lives |
| **Size** | current size |
| **Protection** | who may read / write / execute |
| **Time / owner** | created when, by whom; last modified |

Collectively these are the **metadata** of the file: *"not the actual data, but the data that
specify what the file is."*

**Where they live:** in a **directory entry**. A **directory is a special kind of file** — it is
itself stored on the disk (so it has long-term existence) and consists of a sequence of entries,
one per file.

### 1.4 File type (01 @ 07:32)

Logically a file is a contiguous address space, but the contents may be of different types. The
common way to indicate the type is the **file extension**:

| Type | Extensions named in the lecture |
|---|---|
| Executable | `.exe`, `.com`, `.bin` |
| Text | `.txt` |
| Library | `.lib` |

The type tells the *system* which program can interpret the bytes; the OS itself does not need it.

### 1.5 Internal structure, and the two translations (01 @ 08:47 – 11:14)

Depending on the type, a file may have its own **internal structure** — for example a data file may
be a collection of records (or a tree of records) so that a particular record can be searched.

A hard disk is a **block-oriented device**. Storing a structured file therefore takes two steps:

```
1. RECORD-STREAM TRANSLATION
   internal structure (records, tree of records, ...)  ->  a flat sequence of bytes

2. STREAM-BLOCK TRANSLATION
   sequence of bytes  ->  a sequence of blocks  ->  physical blocks on disk
```

Reading the file performs the **reverse** of both.

> **Who does step 1?** **Not the OS** (01 @ 11:14). To do it the OS would have to understand the
> internal structure of *every* application and file type, and carry the code for all of them. So
> the task is **left to the application program**.

Consequently the OS adopts one simplifying model:

```
        THE OS VIEW:  a file is an UNSTRUCTURED sequence of bytes
                      byte addressable, starting from offset 0
```

Unix and early versions of Microsoft OS work this way, and **this is the assumption used for the
whole chapter**.

---

## 2. Access methods and file operations (part 01, 12:25 – 21:59)

### 2.1 Two access methods

| Method | Also called | How a byte is found | Suits |
|---|---|---|---|
| **Sequential** | — | read bytes in order from the beginning; the position advances | tapes, logs, compilers reading source |
| **Direct** | **random** | address byte *n* directly by its byte number | databases, executables, indexes |

The distinction matters later: **contiguous** and **indexed** allocation support direct access
efficiently; **linked** allocation does not (part 03).

### 2.2 The file operations (01 @ 13:38)

| Operation | What the OS must do |
|---|---|
| **Create** | allocate space for the file + **create a directory entry** (the entry holds the attributes) |
| **Delete** | **deallocate** the space + **remove the directory entry** |
| **Open** | find the directory entry once, and cache what is needed in the **open file table** |
| **Close** | decrement the open counter; at zero, remove the open-file-table entry |
| **Write** | parameters: **file descriptor** (index into the open file table) + **amount of data** |
| **Read** | parameters: **file descriptor** + **where the data goes** (buffer address) |

> The lecture says *"that's basically the five operations"* while enumerating six. Count the list,
> not the sentence.

### 2.3 Why `open()` exists (01 @ 16:04)

The slide's reasoning is a chain of four facts:

1. To read or write a file, the OS must know **where the file is on the disk**.
2. The disk location is one of the file's **attributes**.
3. The attributes are stored in the file's **directory entry**.
4. The directory is itself stored **on the disk**.

Therefore, a naive implementation would need to consult the directory on the disk every time a
`read` or `write` is issued, just to rediscover the file's location. That would add a repeated disk
access before the access that actually reads or writes the file. The purpose of `open()` is to do
this lookup once and cache the result for later operations. The lecture explicitly gives
**efficiency**, rather than permission checking, as the reason for opening a file first.

Conceptually:

```text
without open:
    read/write -> access the directory on disk -> find file location -> access file data
    read/write -> access the directory on disk -> find file location -> access file data
    ...

with open:
    open(name) -> find the directory entry -> cache file information in the open file table
    read/write -> use the cached table entry -> access file data
    read/write -> use the cached table entry -> access file data
    ...
```

An open-file-table entry contains information associated with the file while it is in use:

| Cached information | Why it is needed |
|---|---|
| **Disk location** (a cached file attribute) | tells the OS where to access the file data |
| **Current-position pointer** | tells the next `read` or `write` where to begin |
| **Open counter** | records how many processes currently have the file open |

`open(name)` returns a **file descriptor**, which is an index used to locate this entry later.
Consequently, a `read` or `write` does not need to search the directory again: it uses the file
descriptor to find the open-file-table entry, obtains the current position and cached disk
location, and then performs the data operation. The later two-level design splits these fields
between a per-process table and a system-wide table; see §5.

`close()` is the reverse bookkeeping operation. It decrements the open counter. When the counter
reaches **zero**, no process is using the file, so the corresponding open-file-table entry can be
deleted.

### 2.4 What actually happens on a write (01 @ 19:38)

```
write(fd, nbytes)
   fd                 -> entry in the open file table
   entry.current_pos  -> where to start writing
   entry.disk_location-> where the file is on disk
   nbytes             -> how much
```

`read()` is the same, except the second argument is the **destination buffer** instead of a length
to write. The two-level version of this table (per-process vs system-wide) is §5.

---

## 3. Directories (part 01, 21:59 – end)

### 3.1 Two layouts for a directory entry

A directory is a **sequence of entries**. There are two ways to lay out each entry:

| Layout | Entry contains | Attributes live |
|---|---|---|
| **A. Inline** | file name **and all attributes** | in the directory itself |
| **B. Indirection** | file name **and a pointer** to a data structure | in a **file control block (FCB)**, one per file, on disk |

Layout B is the one used for the rest of the chapter: a **Unix inode** is the classic example of an
FCB (part 02 @ 04:47, part 03 @ 26:43).

### 3.2 How the entry sequence is implemented (01 @ 23:11)

| Implementation | Search cost | Notes |
|---|---|---|
| **Linear list** | O(n) — compare names one by one | simple; deletion is awkward |
| **Hash table** | O(1) average | needs a hash on the name and a collision scheme |

The lecture explicitly leaves the data-structure detail to your data-structures notes; the point is
that the choice is a **performance** decision.

### 3.3 Tree-structured directories (01 @ 24:26)

Directories can be organised into a **tree**. Three purposes are named:

1. **Searching** — given a name, locate the file efficiently.
2. **Naming convenience** — the **same file name may exist in different directories**.
3. **Grouping** — related files can be collected into a subdirectory, e.g. all C programs in one
   subdirectory, all Java programs in another.

### 3.4 Path names (01 @ 25:36 – 29:09)

```
        /            <- root  (rectangle = directory, circle = file)
        |
      spell
        |
       mail
        |
       prt
        |
      file   <- /spell/mail/prt/file
```

| Kind | Starts from | Example |
|---|---|---|
| **Absolute path name** | the **root** | `/spell/mail/prt/file` |
| **Relative path name** | the **current working directory** | `prt/file` if `mail` is the cwd |

A path name is a **sequence of directory names** ending in the file name, and it makes the file
**uniquely identifiable**. Two files may share a name as long as their **path names** differ.

### 3.5 Links: sharing one physical file (01 @ 29:09 – 35:18)

A directory entry *is* a name for a physical file, so sharing can be achieved by letting **two
directory entries name the same physical file**. That destroys the tree: the structure becomes a
**graph with a cycle**.

| | **Symbolic link** | **Hard link** |
|---|---|---|
| How created | a **special directory entry** whose content is the **path name** of the original file | **duplicate the attributes** of the original entry into the new entry |
| Access cost | **higher**: the OS must follow the path name, find the original entry, and read its attributes before it can reach the file | **lower**: the file entry is self-contained; direct access |
| Consistency | automatic (there is only one copy of the attributes) | **a problem**: if the file is modified, every duplicated entry must be updated |
| Delete behaviour | the link **dangles**: its path no longer resolves | the other entry keeps working, but if the underlying blocks are freed it now points at blocks that are no longer the file's — which is why Unix keeps a **link count** |

### 3.6 The two problems links create (01 @ 35:18)

**(a) Traversal visits a shared file more than once.**
Solution: **ignore link entries while traversing** the file system.

**(b) Deleting a file leaves a dangling link.**
Three solutions are given:

| # | Solution | Cost |
|---|---|---|
| 1 | On delete, **search for all links** to the file and remove them at the same time | an expensive search |
| 2 | **Leave the link dangling**; detect it and delete the link the *next time it is used* | error deferred to the user |
| 3 | **Do not delete the file at all** until the **last link** is removed (reference counting) | needs a link count in the FCB — this is what Unix does |

The lecturer flags that solution 2 "may cause some problem… we will further elaborate during the
tutorial" — think about *when* the error is reported and to *whom*.

### 3.7 Directory operations (01 @ 38:55)

| Operation | Effect | Unix specifics |
|---|---|---|
| **Create** | allocate space for the directory + create an entry for it in the **current** directory | Unix automatically creates two entries: **`.`** (current) and **`..`** (parent) |
| **Delete** | deallocate the directory's space + remove its entry | Unix deletes **only an empty** directory — one containing just `.` and `..` |
| **List** | list all entries in the directory | — |
| **Search** | given a file name, locate its entry | — |
| **Traverse** | access every entry in every directory | "walk the file system" — see §3.6(a) |

---

## 4. File protection (part 02, 00:00 – 04:47)

Protection is a responsibility of the **logical file system**. The question it answers: *the file's
owner should control what may be done, and by whom.*

### 4.1 Unix: three classes × three rights

In Unix every file belongs to a **primary group**. At creation the file is associated with the
creator's primary group; groups are created by the **system administrator**.

```
                 owner            group            public
              (creator)     (same group as owner)  (everyone else)
            +-----------+    +-----------+        +-----------+
   bits:    |  r  w  x  |    |  r  w  x  |        |  r  w  x  |
            +-----------+    +-----------+        +-----------+
                 |                |                    |
             read/write/      read/write/          read/write/
             execute          execute              execute
```

The lecture's example file: **owner `rwx`, group `r-x`, public `--x`** (octal **751**) — the owner
may read, write and execute; same-group users may read and execute; everyone else may only execute.

### 4.2 Directories need the `x` bit (02 @ 02:22)

A directory is a **special kind of file** with the same nine bits, but the bits mean something
different:

| Bit | On a **file** | On a **directory** |
|---|---|---|
| **r** | read the contents | **list** the contents |
| **w** | modify the contents | **modify the contents**: insert an entry, delete an entry |
| **x** | execute the file | **traverse / access the directory at all** |

> **The key point.** For a directory, **`x` is a prerequisite**: *"if there is no execution
> permission, then the corresponding read and write operation on the directory cannot be
> performed,"* even when `r` and `w` are set.

The lecture's directory example: owner `rwx`, group `r-x` (may list), everyone else has no `r` and
no `w`.

---

## 5. The two-level open file table (part 02, 04:47 → end)

### 5.1 The problem

`open()` is easy for **one** process. It is hard when several processes open **the same** file at
the same time: some state is **per process** (how far *this* process has read) and some is
**global** (the file's own metadata, how many processes hold it open).

### 5.2 The two tables

```
   PROCESS                       PER-PROCESS OPEN FILE TABLE        SYSTEM-WIDE OPEN FILE TABLE
   +-----------+                 +------------------------------+   +-----------------------------+
   | fd = i    |---------------->| [i] current position pointer |   | [j] cached copy of the FCB  |
   +-----------+                 |     permission of this proc  |-->|     file open counter       |
                                 |     ...                      |   |     ...                     |
                                 +------------------------------+   +-----------------------------+
                                                                             |
                                                                             v
                                                                  FILE CONTROL BLOCK (on disk)
                                                                  (e.g. a Unix inode)
```

| Table | Scope | Holds |
|---|---|---|
| **Per-process open file table** | one per process, one entry per file **that process** has open | **current position pointer**, **permission of this process** on the file, and a **pointer to the system-wide entry** |
| **System-wide open file table** | one for the whole system, one entry per **distinct open file** | a **cached copy of the FCB**, and the **file open counter** (how many processes have it open) |

Notes from the recording (02 @ 05:57 – 08:28):

* Two processes opening the *same* file share **one** system-wide entry but have **two** per-process
  entries → each process has its **own current position**. (This is why two processes reading the
  same file do not interfere.)
* When a second process opens a file that is already open, the system-wide table is **not**
  duplicated; its **counter is incremented**.

### 5.3 The file descriptor (02 @ 08:28)

**`open()` returns the index of the entry in the per-process open file table.** That integer is the
**file descriptor**.

```
fd = open("mail")
        |
        +--> integer index into THIS process's open file table
```

### 5.4 The full read/write path (02 @ 10:51)

```
read(fd, buffer, n)
   |
   |  1. fd                         -> per-process open file table entry
   |  2. entry.current_position     -> first logical block to touch
   |     + n                       -> how many logical blocks
   |  3. entry.pointer              -> system-wide entry (cached FCB)
   |  4. FCB + allocation method    -> which physical blocks hold those logical blocks
   |  5. issue I/O on those physical blocks -> copy into buffer
```

Every layer contributes exactly one thing:

| Layer | Contributes |
|---|---|
| Per-process OFT | *this process's* position and permission |
| System-wide OFT | the *shared* FCB and open count |
| FCB / inode | the block map |
| Allocation method | logical block → physical block |
| Basic FS / I/O control | the actual transfer |

---

## 6. Block allocation (part 03, 00:00 – 26:43)

### 6.1 Logical blocks and physical blocks (03 @ 00:00)

```
   FILE (user view)         : a sequence of BYTES, addressable from 0
   DISK (device view)       : a sequence of BLOCKS (512 B, 4 KB, ...)

   step 1: cut the byte stream into LOGICAL BLOCKS   (numbered 0, 1, 2, ...)
   step 2: map each logical block to a PHYSICAL BLOCK on the disk
```

**Which physical block holds logical block *i* is exactly what the allocation method decides.**
That is the whole subject of part 03.

### 6.2 The universal translation recipe

Every method uses the same two-step procedure (03 @ 05:55):

Given a byte offset \(x\) inside the file, let \(S\) be the block size (or the effective
block size for linked allocation):

$$
\begin{aligned}
q &= \left\lfloor \frac{x}{S} \right\rfloor
&&\text{logical block number} \\
r &= x \bmod S
&&\text{displacement inside that block}
\end{aligned}
$$

The allocation method then determines the physical block:

| Method | Physical-block lookup |
|---|---|
| **Contiguous** | \(\text{start} + q\) |
| **Linked** | Walk the chain \(q\) times from the first block |
| **Indexed** | Look up entry \(q\) in the index block or inode |

**Exam habit:** write `q = x div S, r = x mod S` first, *always*. Every worked example in the three
methods starts with the same division.

### 6.3 Contiguous allocation (03 @ 02:21)

Each file occupies a **set of contiguous blocks** on the disk. The directory entry keeps the
**starting block** and (implicitly or explicitly) the length.

```
logical block i  ->  physical block (start + i)
```

**Example (03 @ 08:27).** File `mail` starts at physical block **19** and is **6** blocks long:

| logical block | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| physical block | 19 | 20 | 21 | 22 | 23 | 24 |

Access byte **2333** (block size 512):

```
2333 div 512 = 4        -> logical block 4
2333 mod 512 = 285      -> displacement 285 inside the block
physical = 19 + 4 = 23
```

**Advantages**

* Translation is one addition — **direct access is trivial**.
* Contiguous blocks ⇒ good **sequential** performance too.

**Problems**

| Problem | Why |
|---|---|
| Need a **large enough hole** | you must find a run of free blocks (first-fit / best-fit / worst-fit — the same policies as `../c89` §3) |
| **External fragmentation** | as files are created and deleted, holes become too small |
| **Growth is constrained** | the free blocks *after* the file may not be enough; the file must then be **moved** to a bigger hole |
| **Internal fragmentation** if over-allocated | allocating more blocks than needed wastes the tail |

### 6.4 Linked allocation (03 @ 12:06)

Each file is a **linked list of disk blocks**, scattered anywhere. The **directory entry** keeps the
**first block**. Each block begins with a **pointer to the next block** of the same file.

```
directory entry: mail -> [9] --+--> [16] --+--> [1] --+--> [10] --+--> [25] --+--> ...
                               |           |          |           |           |
                        logical 0   logical 1  logical 2   logical 3   logical 4
```

**Effective block size.** With a 512 B block and a **4-byte** pointer, only `512 − 4 = 508` bytes of
each block carry file data. So (03 @ 16:51):

```
q = x div 508
r = x mod 508
displacement inside the block = r + 4        <- skip the pointer
```

**Example (03 @ 18:06).** Chain `0 → 9`, `1 → 16`, `2 → 1`, `3 → 10`, `4 → 25`.

Access byte **2333**:

```
2333 div 508 = 4   (508 × 4 = 2032, remainder 301)
2333 mod 508 = 301 -> displacement 301 + 4 = 305
logical block 4    -> must walk 0 -> 1 -> 2 -> 3 -> 4, arriving at physical block 25
```

**Advantages**

* **No external fragmentation** — any free block will do.
* **No size limit** — the file grows by adding another block anywhere.
* Only the first block number must be stored.

**Disadvantage**

* **Direct access is inefficient.** Reaching logical block *k* costs *k* pointer hops, *"and each of
  these will require a disk I/O"*. Reliability is also poorer (one bad pointer breaks the chain).

### 6.5 Indexed allocation (03 @ 20:31)

Each file has an **index block**: **one entry per logical block**, each entry holding that block's
**physical block number**. The **directory entry** keeps the **index block number**.

```
directory entry: mail -> index block
                        +----+----+----+----+----+---
                        |  9 | 16 |  1 | 10 |  5 | ...     <- entry i = physical block of logical i
                        +----+----+----+----+----+---
                          0    1    2    3    4
```

Access byte **2333** (block size 512): `q = 4`, `r = 285` → look up **entry 4** → physical block
(see the example table above).

**Advantages**

* **Direct access is efficient** — one lookup, no chain walk.
* **No external fragmentation** — any free block can be used.

**Costs**

* The **index block itself occupies space** (overhead grows with file size).
* **One extra I/O** to read the index block before the data.
* The index block must be found — which is the problem that leads to the inode.

### 6.6 How big is the index? (03 @ 23:05)

Lecture example: **maximum file size 128 KB**, block size **512 B**, pointer size **4 B**.

```
blocks in the file   = 2^17 / 2^9 = 2^8 = 256 logical blocks
entries per index blk= 512 / 4    = 128 = 2^7
index blocks needed  = 256 / 128  = 2
```

So a file of that size needs **two** index blocks — and the directory entry can only name one. The
fix is to chain or nest index blocks (or use an inode).

### 6.7 Comparison

| | **Contiguous** | **Linked** | **Indexed** |
|---|---|---|---|
| Directory entry holds | start block (+ length) | first block | index block |
| Logical → physical | `start + q` | walk chain *q* hops | `index[q]` |
| Direct access | **excellent** | **poor** | **good** |
| External fragmentation | **yes** | no | no |
| Internal fragmentation | yes if over-allocated, and in the last block | yes, in the last block | yes, in the last block (+ index-block overhead) |
| File growth | hard (must be able to extend) | **easy** | easy |
| Extra space | — | 4 B (or so) per block | one index block per file |
| Extra I/O per access | **0** — pure arithmetic | *q* (chain walk) | **1** (the index block) |

*(Part 04 makes the general point: whatever the method, the **last** block of a file is partly
empty — that internal fragmentation is unavoidable.)*

---

## 7. The Unix inode (part 03, 26:43 → end)

### 7.1 What it is

> Unix uses the **inode** — an **extension of indexed allocation** — as the file control block.
> Every file has exactly one inode, stored on the disk. The **directory entry contains the file name
> and the inode number** (03 @ 34:02).

Layout (03 @ 27:55):

```
   +-----------------------------------+
   |  file attributes (metadata)       |
   +-----------------------------------+
   |  direct[0]   -> data block        |   \
   |  direct[1]   -> data block        |    |  12 direct pointers:
   |  ...                              |    |  cover logical blocks 0 .. 11
   |  direct[11]  -> data block        |   /
   +-----------------------------------+
   |  single indirect -> [ ][ ][ ] ... |  -> index block of pointers to data blocks
   |  double indirect -> [ ]...        |  -> index block of pointers to *index* blocks
   |  triple indirect -> [ ]...        |  -> three levels
   +-----------------------------------+
```

| Pointer | Levels of indirection | Physical blocks reachable | Covers logical blocks |
|---|---|---|---|
| **direct** (×12) | 0 | 12 | 0 – 11 |
| **single indirect** | 1 | *E* | 12 … 12+*E*−1 |
| **double indirect** | 2 | *E²* | next *E²* blocks |
| **triple indirect** | 3 | *E³* | next *E³* blocks |

where *E* = entries per block = block size ÷ pointer size.

**Why this shape?** Most files are small, so 12 direct pointers cover them with **zero** index
overhead and **zero** extra I/O. Only large files pay for indirection.

### 7.2 Capacity: the standard calculation (03 @ 31:40)

Lecture figures: **pointer = 4 B**, **block = 4 KB**.

```
E = 4096 / 4 = 1024 = 2^10 entries per indirect block

direct          : 12 × 4 KB            = 48 KB
single indirect : 2^10 × 4 KB          = 2^22 = 4 MB
double indirect : 2^10 × 2^22          = 2^32 = 4 GB
triple indirect : 2^10 × 2^32          = 2^42 = 4 TB
                                        ------------------
maximum file size                      ≈ 4 TB (plus the smaller terms)
```

The lecture computes **48 K**, then **48 K + 2^22** (direct + single), then notes that adding the
double indirect makes it *"extremely large"*. The triple level completes the ladder.

> **Do not memorise 4 TB — memorise the method:** *entries per block = block ÷ pointer*, then each
> level multiplies the capacity by *E*. The numbers change with the block size; the method does not.

### 7.3 Worked example: which physical blocks does a read touch? (03 @ 35:14)

Simplified inode with **6 direct pointers** + **1 single indirect pointer**. Block size **1000 B**.
`current position = 5900`, read **200 bytes**.

**Step 1 — which logical blocks does the request touch?**

```
5900 div 1000 = 5      -> starts in logical block 5
5900 mod 1000 = 900    -> at offset 900 in that block
bytes 5900 .. 6099:
     5900 .. 5999  -> 100 bytes in block 5   (offsets 900 .. 999)
     6000 .. 6099  -> 100 bytes in block 6   (offsets   0 ..  99)
```

**Step 2 — where are blocks 5 and 6?**

| logical block | where it is | why |
|---|---|---|
| 5 | **6th (last) direct pointer** | blocks 0–5 are covered by the six direct pointers |
| 6 | **single indirect** → indirect block entry **index 0** | blocks 6, 7, 8, … are covered by the indirect block, starting at entry 0 |

```
logical block 6  ->  (6 - 6) = 0  ->  indirect_block[0]  ->  physical block of logical block 6
```

> The recording says *"the fourth entry in this indirect block"*. With **six** direct pointers,
> logical block 6 must be the **first** entry of the indirect block. Treat the "fourth" as a slip
> and confirm the indexing rule rather than the number — see
> [`NOTES.md`](NOTES.md#3-known-slips-and-internal-contradictions).

### 7.4 The general formula for the inode lookup

```
Let D = 12 (number of direct pointers), E = entries per block, q = logical block number.

if q < D                     -> direct[q]
else if q < D + E            -> single_indirect[q - D]
else if q < D + E + E^2      -> double_indirect[(q - D - E) div E][(q - D - E) mod E]
else                         -> triple_indirect[...]
```

---

## 8. Free-space management (part 04)

### 8.1 The block-size trade-off (04 @ 00:00)

> *"Block size affects both data read and disk space utilization. There is a trade-off between the
> two."*

| Block size | Blocks per file | I/Os to read | Read speed | Space wasted |
|---|---|---|---|---|
| **Large** | fewer | fewer | **fast** | **more** — the last block is partly empty (internal fragmentation) |
| **Small** | many | many | **slow** | **less** |

```
 speed
   |            ___________  data rate (increases with block size, then flattens)
   |        ___/
   |    ___/
   |___/                    \  ... and utilization falls
   |                         \______
   +-----------------------------------> block size
```

**Why the waste is unavoidable.** *"No matter which file allocation method is used, they all suffer
from internal fragmentation, and this happens to the last block."*

**What to do?** *"Some OS actually use two block sizes for file allocation"* — discussed in a
tutorial question (see the practice problems).

### 8.2 Bitmap (04 @ 02:34)

One **bit per block**; the bitmap is a bit vector indexed by block number.

```
block :  0  1  2  3  4  5  6  7  8  9 ...
bit   :  0  1  0  0  1  1  0  1  0  0 ...
         |  |  |  |  |  |  |  |  |  |
         |  +--+--+--+--+--+--+  |  +--> free
         |        allocated      |
         +--> free               +--> allocated
```

**The convention as stated in the recording (04 @ 02:34):** free → **0**, allocated → **1**.

**Size.** It must have one bit per block, so it costs `disk size / block size / 8` bytes:

```
lecture example:  block = 512 B = 2^9,   disk = 2^34 B = 16 GB
blocks = 2^34 / 2^9 = 2^25  blocks
bits   = 2^25
bytes  = 2^25 / 8 = 2^22 = 4 MB
```

**Properties**

* **Fixed location** on the disk (usually); can be **cached in memory** — 4 MB is affordable, and
  then *"the bitmap can be searched without accessing the hard disk."*
* If it is cached, the memory copy and the disk copy must be kept consistent → **write back
  occasionally** (the usual cache-consistency problem).
* **An exhaustive search is still expensive.** To create an n-block file under contiguous
  allocation, the OS must find **n consecutive free bits**; deleting changes n bits. So many systems
  keep **additional structures** to avoid rescanning.

### 8.3 Linked list (04 @ 06:11)

Free blocks are **chained**: the OS keeps **one pointer**, to the first free block; each free block
holds a pointer to the next free block.

```
free_list_head -> [ free ] -> [ free ] -> [ free ] -> nil
```

| | Cost |
|---|---|
| Space overhead | **negligible** — no extra structure, just one pointer |
| Allocate one block (linked/indexed allocation) | **cheap**: take the head, advance the pointer |
| Allocate **n contiguous** blocks (contiguous allocation) | **must scan the whole chain** for a run of n; then splice it out |
| Every allocation | must **read the block** to recover the next pointer before writing data → **slow** if many blocks are needed at once |
| Deleting a file with scattered blocks | **very slow** — freed blocks must be re-inserted in order |

### 8.4 Comparison

| | **Bitmap** | **Linked list** |
|---|---|---|
| Space | 1 bit/block (4 MB for 16 GB disk) | ~0 (one pointer word per free block) |
| Find 1 free block | scan for a free bit (a `0` under the stated convention) | **O(1)** from the head |
| Find **n contiguous** free blocks | scan the bitmap (can be cached) | **scan the whole chain** |
| Read/write cost per allocation | none (bitmap in memory) | **must read the block** to get the next pointer |
| Deleting | clear n bits | insert into the ordered chain |

---

## 9. Putting it all together

One `read()` on Unix, end to end:

```
read(fd, buf, n)
 1. fd                    -> per-process open file table entry          (part 02)
 2. current position + n  -> logical blocks q1 .. q2                    (part 03)
 3. pointer               -> system-wide open file table entry          (part 02)
 4. cached FCB            -> the inode                                  (part 03)
 5. inode                 -> direct / single / double / triple indirect (part 03)
                          -> physical block numbers                    (part 03)
 6. basic file system     -> issue block reads                          (not recorded)
 7. I/O control           -> device driver + interrupts                 (not recorded)
 8. data copied into buf
```

And the *creation* of that file, end to end:

```
create("mail")
 1. logical file system: allocate/append a directory entry (name + attributes/inode number)  (01)
 2. file organization module: find a free block — from the bitmap or the free list            (04)
 3. record the mapping (start block / first block / index block / inode pointers)            (03)
 4. associate the file with the creator's primary group and set the protection bits          (02)
```

---

## 10. Formula sheet

Let \(x\) be a byte offset, \(S\) a block size, \(p\) a pointer size, and \(B\) an inode block
size.

### Translation

$$
\begin{aligned}
q &= \left\lfloor \frac{x}{S} \right\rfloor
&\qquad r &= x \bmod S \\
S_{\mathrm{eff}} &= S-p
&\qquad d_{\mathrm{linked}} &= (x\bmod S_{\mathrm{eff}})+p
\end{aligned}
$$

| Method | Physical-block lookup |
|---|---|
| **Contiguous** | \(\text{start}+q\) |
| **Linked** | Walk the chain \(q\) times from the first block |
| **Indexed** | \(\text{index\_block}[q]\) |
| **Inode** | \(q<12\): direct[\(q\)]; otherwise use the appropriate indirect level |

For the first two inode ranges:

$$
\begin{aligned}
q < 12 &\Rightarrow \text{direct}[q] \\
12 \le q < 12+E &\Rightarrow \text{indirect}[q-12] \\
\end{aligned}
$$

For the double-indirect range, let \(t=q-12-E\):

$$
12+E \le q < 12+E+E^2
\quad\Rightarrow\quad
\text{double}\!\left[\left\lfloor \frac{t}{E}\right\rfloor\right][t\bmod E]
$$

where \(E=B/p\).

### Sizes and free space

$$
\begin{aligned}
E &= \frac{B}{p}
&&\text{entries per index or indirect block} \\
\text{index blocks needed} &= \left\lceil \frac{\text{file blocks}}{E} \right\rceil \\
C_{\mathrm{inode}} &= 12B + EB + E^2B + E^3B \\
\text{bitmap bits} &= \frac{\text{disk size}}{B} \\
\text{bitmap bytes} &= \frac{\text{disk size}}{8B}
\end{aligned}
$$

### Protection

$$
9\text{ bits}=(\text{owner rwx})(\text{group rwx})(\text{public rwx}),
\qquad \text{octal digit}=4r+2w+1x
$$

---

## 11. Practice problems

Try each before reading the solution.

**P1.** Block size 1 KB. A file `report` is contiguous, starts at physical block 100, and is 40
blocks long. Which physical block holds byte 15 000? What is the displacement?

**P2.** Same file, but stored with **linked** allocation (block 1 KB, 4-byte pointer). Give the
effective block size, the logical block number of byte 15 000, and the displacement *inside the
physical block*.

**P3.** An indexed-allocation file system has block size **4 KB** and **4-byte** pointers. What is
the largest file size representable with **one** index block? How many index blocks does a **1 MB**
file need?

**P4.** An inode has **10 direct**, 1 single, 1 double and 1 triple indirect pointer. Block size
**1 KB**, pointer **4 B**. Compute the maximum file size and the logical block ranges covered by
each level.

**P5.** Using the inode of P4 and a `read` starting at byte **10 000** of length **3 000** bytes,
list every logical block touched and say **which pointer** reaches each one.

**P6.** A 1 TB disk uses 4 KB blocks. How large is the free-space bitmap? Would you cache it?

**P7.** Two processes both `open("/spell/mail/prt/file")`. Process A reads 100 bytes, then process B
reads 100 bytes. How many entries exist in the per-process tables? In the system-wide table? How
many distinct current-position pointers are there?

**P8.** A file has mode `751`. Can another user in the same group read it? Can a user outside the
group execute it? Now suppose the same `751` is applied to a **directory** — can a same-group user
list its contents? Can they *create* a file in it?

**P9.** Explain why contiguous allocation suffers external fragmentation but linked and indexed
allocation do not. Then explain why indexed allocation has an overhead that neither of the others
has.

**P10.** A file is deleted while a symbolic link and a hard link to it exist. What does the user see
on each link? What would the three deletion policies in §3.6 do differently?

### Solutions

**S1.** `15000 div 1024 = 14` (14 × 1024 = 14 336, remainder 664) → logical block 14, displacement
**664**, physical block **100 + 14 = 114**.

**S2.** `S_eff = 1024 − 4 = 1020`. `15000 div 1020 = 14` (14 × 1020 = 14 280, remainder 720) →
logical block **14**; displacement inside the physical block = `720 + 4` = **724**. Reaching it
costs **14 pointer hops**, i.e. 14 extra block reads on top of the data read.

**S3.** `E = 4096 / 4 = 1024` entries → `1024 × 4 KB = 4 MB` per index block. A 1 MB file is
`1 MB / 4 KB = 256` blocks → `ceil(256 / 1024) = 1` index block. (This is why one index block
suffices until 4 MB.)

**S4.** `E = 1024 / 4 = 256`.
```
direct          : 10 × 1 KB              = 10 KB            logical blocks 0 .. 9
single indirect : 256 × 1 KB             = 256 KB           blocks 10 .. 265
double indirect : 256^2 × 1 KB           = 64 MB            blocks 266 .. 65 801
triple indirect : 256^3 × 1 KB           = 16 GB            blocks 65 802 .. 16 843 017
maximum         = 10 KB + 256 KB + 64 MB + 16 GB
```

**S5.** `10000 div 1024 = 9`, remainder `784` → starts in block 9 at offset 784. 3000 bytes span
blocks 9 (240 bytes: 784–1023), 10 (1024 bytes), 11 (1024 bytes), 12 (712 bytes).
```
block  9 -> direct[9]                       (last direct pointer)
block 10 -> single indirect[0]              (block 10 - 10)
block 11 -> single indirect[1]
block 12 -> single indirect[2]
```

**S6.** Blocks = `2^40 / 2^12 = 2^28` → bits = `2^28` → bytes = `2^25` = **32 MB**.
Yes, cache it: 32 MB of RAM to remove a disk read from every allocation decision is a good trade —
but it must be written back to keep the disk copy consistent.

**S7.** Two per-process entries (one per process) and **one** system-wide entry (same file, counted
twice). There are **two** distinct current-position pointers — one per per-process entry — which is
why the two reads do not disturb each other. If they had shared the position, B would continue where
A stopped.

**S8.** `751` = owner `rwx`, group `r-x`, public `--x`.
* Same-group user: **yes**, can read (the `r` bit).
* Outside user: **yes**, can execute (`--x`) — though executing a plain data file usually fails for
  other reasons.
* On a **directory**: same-group user **can list** (`r` **and** `x` both set). They **cannot
  create/delete** entries, because `w` is not set for the group.

**S9.** Contiguous allocation needs a **run** of free blocks, so holes between files become
unusable (external fragmentation). Linked and indexed allocation accept **any** free block, so no
hole is ever "too small" — there is no external fragmentation. Indexed allocation, however, needs an
**index block per file**, which consumes space in proportion to the number of files (and blocks) and
costs one extra read to reach the index.

**S10.** With a **hard link** the entry is independent: if the file's blocks are freed, the hard
link points at blocks that are no longer the file's — silent corruption unless the system counts
links. With a **symbolic link**, the path name no longer resolves — an error on the *next access*.
Policy 1 (remove all links at delete) avoids both but costs a full search; policy 2 leaves the
symbolic link dangling and reports the error on use, which is why "the tutorial will elaborate";
policy 3 (reference counting, Unix) keeps the data until the **last** link goes, so neither link
breaks.

---

## 12. Self-test questions

1. Name the four layers of a file system and one responsibility of each. Which layer translates
   logical to physical block addresses?
2. What are the seven file attributes, and where are they stored?
3. Why is a **directory** called a special kind of file? Give two consequences.
4. What are record-stream translation and stream-block translation? Which one does the OS **not**
   do, and why?
5. Why does the OS treat a file as an unstructured byte stream? Name two systems that do this.
6. Distinguish **sequential** and **direct** access. Which allocation methods support direct access
   well?
7. List the six file operations and say what each must do to the disk and to the directory.
8. Why must a file be opened before it is read or written? What three things does the open file
   table entry hold?
9. Describe the two ways to lay out a directory entry. What is an FCB? Give a Unix example.
10. Why can the same file name exist twice in a tree-structured directory but still identify two
    different files?
11. Compare symbolic and hard links on: creation, access cost, consistency, and behaviour when the
    file is deleted.
12. What are the two problems links create, and what are the three deletion policies?
13. Which Unix directory entries are created automatically, and what do they mean? When may a
    directory be deleted?
14. State the meaning of `r`, `w` and `x` for a **directory**. Why is `x` special?
15. Draw the two-level open file table and say what each level contains. What is a file descriptor?
16. Give the universal translation recipe and apply it to byte 2333 with a 512-byte block size.
17. For each allocation method, state: what the directory entry holds, how logical block *i* is
    found, and the main disadvantage.
18. Why is a linked file's **effective** block size smaller than the physical block size? Where does
    the displacement shift come from?
19. How many index blocks are needed for a 128 KB file with 512-byte blocks and 4-byte pointers?
20. Draw a Unix inode. Compute `E`, the capacity of each level, and the maximum file size, for a
    4 KB block and 4-byte pointers.
21. Given an inode with 6 direct pointers and a 1000-byte block, work out which blocks a
    200-byte read at position 5900 touches, and which pointer reaches each.
22. Explain the block-size trade-off for free space and data rate. Why can it never be resolved
    perfectly?
23. Compute the bitmap size for a 16 GB disk with 512-byte blocks. What are the pros and cons of
    the bitmap vs the linked list of free blocks?

---

## 13. Glossary

| Term | Meaning |
|---|---|
| **File** | named, long-lived, shareable collection of related information on secondary storage |
| **Metadata / attributes** | name, type, location, size, protection, time, owner — the data *about* the file |
| **Directory entry** | the record holding one file's name and attributes (or a pointer to its FCB) |
| **FCB (file control block)** | per-file data structure holding the attributes and the block map; a Unix **inode** is one |
| **Logical block** | a block-sized unit of the *file*, numbered from 0 |
| **Physical block** | a block on the *disk* |
| **Record-stream translation** | flattening a file's internal structure into a byte stream (done by the application) |
| **Stream-block translation** | cutting the byte stream into blocks (done by the OS) |
| **Open file table** | in-memory table of currently open files; per-process and system-wide levels |
| **File descriptor** | index into the per-process open file table, returned by `open()` |
| **Absolute / relative path name** | path from the root / path from the current working directory |
| **Symbolic (soft) link** | a directory entry holding the *path name* of another file |
| **Hard link** | a directory entry holding a *copy of the attributes* of another entry |
| **Dangling link** | a link whose target file no longer exists |
| **Contiguous allocation** | a file occupies one run of blocks; `physical = start + i` |
| **Linked allocation** | a file is a chain of blocks; each block points to the next |
| **Indexed allocation** | a per-file index block maps logical block → physical block |
| **Inode** | Unix FCB: attributes + 12 direct + single/double/triple indirect pointers |
| **Direct / indirect pointer** | a pointer straight to a data block / to a block of pointers |
| **Bitmap** | one bit per disk block, marking free or allocated |
| **Free list** | chain of free blocks, head pointer only |
| **Internal fragmentation** | waste *inside* an allocated unit (the last block of a file) |
| **External fragmentation** | free space exists but not in a large enough *run* (contiguous allocation) |
