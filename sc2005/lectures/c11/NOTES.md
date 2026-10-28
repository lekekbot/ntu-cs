# File Systems — Things to Take Note Of

Exam-focused companion to [STUDY_GUIDE.md](STUDY_GUIDE.md): what the lecturer stresses, what is easy
to get wrong, and where the recordings are unreliable. No new material.

---

## 1. What the lecturer repeatedly stresses

| Point | Where | Why it matters |
|---|---|---|
| **The OS sees a file as an unstructured byte stream** | 01 @ 12:25 | Every translation formula assumes it; `q = x div S` is only meaningful for a byte stream |
| **Record-stream translation is the application's job** | 01 @ 11:14 | The standard "why not the OS?" question |
| **`open()` exists for efficiency** | 01 @ 18:26 | Not for permission checking — it caches the disk location |
| **Metadata lives in the directory entry** | 01 @ 06:20 | Links, protection and inodes all follow from this |
| **`x` on a directory gates `r` and `w`** | 02 @ 02:22 | The one directory-permission fact that is not obvious |
| **The file organization module owns *both* allocation and free space** | 01 @ 02:41 | Explains why parts 03 and 04 belong together |
| **`q = quotient`, `r = displacement` — same first step every time** | 03 @ 07:13 | All three methods share it; only step 2 differs |
| **Direct access is the discriminator between the methods** | 03 @ 14:31 | The standard comparison question |
| **The inode exists to support very large files cheaply** | 03 @ 30:27 | 12 direct pointers keep small files free of indirection |
| **Block size trades data rate against waste** | 04 @ 00:00 | The curve with two opposite trends |

---

## 2. Exam traps

1. **A file is *not* stored contiguously by default.** "A file is a contiguous address space" is a
   *logical* statement; physically it may be scattered.
2. **The directory is a file.** It consumes blocks, has attributes and (in Unix) has its own
   protection bits.
3. **`open()` does not read the file's data** — it reads the directory entry once and caches the
   location.
4. **The file descriptor is an index into the *per-process* table**, not the system-wide table.
5. **Two processes sharing a file get two position pointers.** A shared position is the classic
   wrong answer.
6. **Hard link ≠ copy of the file.** It duplicates the *directory entry's attributes*; the data
   blocks are shared.
7. **Symbolic link costs extra accesses**; hard link does not (but breaks consistency).
8. **Contiguous allocation suffers *external* fragmentation; the other two do not.**
9. **Linked allocation still wastes the tail of the last block** (internal fragmentation) — but its
   *headline* cost is the chain walk. The 4-byte pointer is *overhead*, not fragmentation.
10. **The effective block size of a linked file is `S − pointer_size`**, and the displacement is
    `r + pointer_size`. Forgetting the shift is the most common arithmetic error.
11. **Indexed allocation costs one extra I/O** (read the index block) — say so when comparing.
12. **12 direct pointers cover logical blocks 0–11**, so block 12 is the *first* single-indirect
    block.
13. **Inode capacity multiplies by `E` per level**, where `E = block ÷ pointer`. It is not `2^n` by
    magic.
14. **The bitmap has one bit per *block*, not per byte.**
15. **A bitmap can be cached** — and if it is, it must be written back for consistency.
16. **Free-list allocation from the head is O(1); finding *n contiguous* blocks is a full scan.**
17. **Directory `w` means insert/delete an entry**, not "write the file's contents".

---

## 3. Known slips and internal contradictions

These are places where the recording contradicts itself or the standard definition. Know the correct
version, because an exam marker will.

| Where | What was said | Correct version |
|---|---|---|
| 04 @ 02:34 vs 04 @ 06:11 | First: *"if a block is free, the bit will be zero; if occupied, one."* Then: *"search the bitmap to locate n consecutive bits whose value is **1**"* to find n free blocks. | The two statements are **incompatible**. Pick one convention and say it explicitly. The definition given first (free = 0) is what the recording states; the textbook (Silberschatz) uses **1 = free, 0 = allocated**, which is what the *second* statement implies. Whichever you use, be consistent for the whole answer. |
| 01 @ 21:59 | *"that's basically the five operations"* | **Six** were enumerated: create, delete, open, close, write, read. |
| 03 @ 25:25 vs 03 @ 26:43 | The index-block example maps logical block 4 → physical block **5**; one paragraph later, *"this logical block 4 is in physical block **25**"*. | **5** is correct for the index example (25 came from the *linked* example in the previous section). |
| 03 @ 38:53 | *"the **fourth** entry in this indirect block… pointing to [logical] block 6"*, with **six** direct pointers | With six direct pointers, blocks 0–5 are direct, so logical block 6 is indirect entry **(6 − 6) = 0**, i.e. the **first** entry. |
| 03 @ 29:08 | *"the inode contains the file attributes, and have **12 indirect pointers**… each indirect pointer basically is a physical block number"* | The twelve are **direct** pointers; the three others are the single/double/triple **indirect** pointers. |
| 03 @ 30:27 | *"the block 0, 1, 2, and data block 11, so **can't** be located directly by the direct pointer"* | Blocks **0–11 can** be located directly; block **12 onwards** needs indirection. |
| 03 @ 26:43 | *"inode is the short for index block"* | Inode = **index node**. ("Index block" is the separate, simpler structure of §6.5.) |
| 03 @ 12:06 | *"link allocation"* | Standard term is **linked allocation**. |
| 04 @ 02:34 | *"So this is the same block."* | Garbled; means roughly *"this is one bit per block"*. |

**No arithmetic errors were found** in the four recordings. Every calculation checks out by hand:

* contiguous: `2333 div 512 = 4`, `mod = 285`, `19 + 4 = 23` ✓
* linked: `S_eff = 508`, `2333 div 508 = 4`, `mod = 301`, `301 + 4 = 305` ✓
* index blocks for 128 KB: `2^17 / 2^9 = 2^8 = 256`, `512/4 = 128` → `256/128 = 2` ✓
* inode: `4096/4 = 1024`; `12 × 4 K = 48 K`; `2^10 × 4 K = 2^22` ✓
* bitmap: `2^34 / 2^9 = 2^25` bits `= 2^22` B `= 4 MB` ✓

---

## 4. Slides and diagrams: what you cannot see in the transcript

Slide numbers are **never read out** in these four recordings, so — unlike `c89`/`c910` — a slide
index cannot be reconstructed. What you *can* rely on:

* The lecturer continuously points at figures: *"this picture"*, *"the diagram here"*, *"graphically,
  that's how it looks like"*. Whenever a sentence begins that way, a **figure you cannot see** is
  carrying part of the argument. Those moments are marked below.
* The **contiguous / linked / indexed** examples all share the same picture: a directory entry box,
  five or six data blocks, and one request for byte **2333**. Learning that one picture is worth more
  than reading the transcript three times.

| Figure referenced | Where |
|---|---|
| Layered file system (4 layers) | 01 @ 01:28 |
| File-attribute table | 01 @ 05:08 |
| Directory-entry-with-FCB diagram | 01 @ 21:59 |
| Tree directory with `rect = dir, circle = file` | 01 @ 25:36 |
| Symbolic-link and hard-link diagrams | 01 @ 31:37 |
| Unix nine-bit protection table | 02 @ 01:12 |
| Two-level open file table diagram | 02 @ 05:57 |
| Contiguous / linked / indexed examples | 03 @ 08:27, 18:06, 25:25 |
| Inode diagram | 03 @ 29:08 |
| Simplified inode (6 direct + 1 indirect) | 03 @ 35:14 |
| Bitmap vs linked-list diagram | 04 @ 02:34 |
| Block-size trade-off curves | 04 @ 01:11 |

---

## 5. Coverage map (what to watch when)

| Topic | Part | Timestamp |
|---|---|---|
| File concept; the two properties; roadmap | 01 | 00:13 – 01:28 |
| Four layers and their responsibilities | 01 | 01:28 – 05:08 |
| File attributes; directory entry | 01 | 05:08 – 07:32 |
| File type via extensions | 01 | 07:32 – 08:47 |
| Internal structure; record-stream and stream-block translation | 01 | 08:47 – 11:14 |
| Why the OS treats a file as a byte stream | 01 | 11:14 – 12:25 |
| Sequential vs direct access | 01 | 12:25 – 13:38 |
| The six file operations | 01 | 13:38 – 16:04 |
| Why `open()` exists; the open file table | 01 | 16:04 – 19:38 |
| `write` and `read` parameters | 01 | 19:38 – 21:59 |
| Directory entry layouts; FCB | 01 | 21:59 – 23:11 |
| Directory implementations (linear list, hash) | 01 | 23:11 – 24:26 |
| Tree structure; path names | 01 | 24:26 – 29:09 |
| Links: symbolic and hard | 01 | 29:09 – 35:18 |
| Link problems: traversal, dangling pointers, 3 policies | 01 | 35:18 – 38:55 |
| Directory operations | 01 | 38:55 – end |
| Unix protection: classes and bits | 02 | 00:00 – 02:22 |
| Directory `r`/`w`/`x`; `x` is essential | 02 | 02:22 – 04:47 |
| Why two levels; the per-process table | 02 | 04:47 – 07:10 |
| System-wide table; the open counter | 02 | 07:10 – 08:28 |
| File descriptor; the read/write path | 02 | 08:28 – end |
| Logical vs physical blocks; the three methods | 03 | 00:00 – 02:21 |
| Contiguous allocation and its problems | 03 | 02:21 – 05:55 |
| Translation recipe; the 512 example | 03 | 05:55 – 12:06 |
| Linked allocation; effective block size | 03 | 12:06 – 20:31 |
| Indexed allocation | 03 | 20:31 – 23:05 |
| Index-block sizing (128 KB example) | 03 | 23:05 – 26:43 |
| Inode structure | 03 | 26:43 – 30:27 |
| Inode capacity calculation | 03 | 30:27 – 34:02 |
| Inode directory entry; worked read example | 03 | 34:02 – end |
| Block-size trade-off | 04 | 00:00 – 02:34 |
| Bitmap: definition, size, caching | 04 | 02:34 – 06:11 |
| Linked list of free blocks | 04 | 06:11 – end |

---

## 6. Memory hooks

* **"Attributes in a directory entry; the directory is a file."** Everything about metadata, links
  and inodes follows from that one sentence.
* **"Application flattens, OS chops."** Record-stream = application; stream-block = OS.
* **`open` = cache the location, not check the permission.**
* **Symbolic = *shortcut* (follow it). Hard = *photocopy* (self-contained, but must be kept in
  sync).**
* **`x` on a directory = "the right to walk through the door".** You can see the sign (`r`) but not
  the room without it.
* **Contiguous = *row of seats*. Linked = *treasure hunt*. Indexed = *table of contents*.**
* **Linked file: subtract the pointer, add it back to the displacement.**
* **Inode = 12 doors, then a floor plan, then plans of plans, then plans of plans of plans.**
* **Bitmap = one seat per bit; free list = each free seat tells you the next.**
* **Big blocks = fast but wasteful; small blocks = frugal but slow.**

---

## 7. ASR correction glossary

The `.srt` files are verbatim; the `.txt` files apply the substitutions below.

| In the transcript | Actual term |
|---|---|
| puncture / punctor / puncters / puncting / puncturing | **pointer / pointers / pointing** |
| puncton ("laser puncton") | **allocation** |
| anode, iNode | **inode** |
| direction, directions, direction tree | **directory(ies), directory entry** |
| hot link, hotlink | **hard link** |
| dunkling (link / punctus) | **dangling (link / pointer)** |
| 9-16 file, nice setting file | **non-existent file** |
| sharp file | **shared file** |
| "file is a charm" | **file is shared** |
| caution | **quotient** |
| reminder | **remainder** |
| excise, exercise ("random excise/exercise") | **access ("random access")** |
| assessing the directory | **accessing the directory** |
| HADISK, HADISC, "the hardest" | **hard disk** |
| OIS, OIs, ois | **OS** |
| five organization module | **file organization module** |
| logic block / logic address | **logical block / logical address** |
| basic block ("which basic block") | **physical block** |
| in-drive block | **indirect block** |
| top punctures (03 @ 27:55) | **twelve pointers** |
| 2.9 / 2.34 / 2.22 / 2.10 / 2 power of 17 | **2^9 / 2^34 / 2^22 / 2^10 / 2^17** |
| FATFIND2, "5 by 2", 5125 | **512** |
| "2 3 3 3" | **2333** |
| SINFA | **the file** |
| sequence of best / sequence of bias | **sequence of bytes** |
| "address is my pin" / "addresses my pin" | **address mapping** |
| "run them access" | **random access** |
| "a resource space" | **a waste of space** |
| "hide this space to the file" | **assign this space to the file** |
| "a census file from 1 to 0" | **assigned to the file from 1 to 0** |
| "if a location is a block at the time" | **if the allocation is a block at a time** |
| "the link or index location" | **the link or index allocation** |
| "SQL file", "basketball file" | **executable file** |
| "BSE and CON, BIN" | **`.exe, .com and .bin`** |
| Unix Assistant Administrator | **Unix system administrator** |
| protection piece | **protection bits** |
| "server processes" (02 @ 05:57) | **several processes** |
| "another person ask queues" | **another process issues** |
| "the sound surface" | **so on and so forth** |
| "the three available physical blocks" | **the free available physical blocks** |
| "written write" / "written right" | **write** |
| "a different time" (01 @ 07:32) | **a different type** |
| "for state programs" | **for C programs** |
| "first feed / best feed / worst feed" | **first fit / best fit / worst fit** |
| "i will control" | **I/O control** |
| "hardware size" (04 @ 02:34) | **hard disk size** |
| "install the data into" | **store the data into** |

Remaining known errors that were **left as-is** because the intent is ambiguous: *"So this is the
same block"* (04 @ 02:34), *"we have two prof10 entries"* → **2^10** (fixed, but grammatical
damage remains), and the half-sentences at the end of 02 (from 10:51) where the recording trails off.

---

## 8. Quick self-check before the exam

- [ ] Can you name the four layers and say which one translates logical → physical block addresses?
- [ ] Can you list the file attributes and say where they are stored?
- [ ] Can you explain why the directory is "a special kind of file"?
- [ ] Can you say which of record-stream / stream-block translation the OS does *not* do, and why?
- [ ] Can you justify `open()` in one sentence, and list the three fields of its table entry?
- [ ] Can you draw both levels of the open file table and say what a file descriptor indexes?
- [ ] Can you compare symbolic and hard links on four dimensions?
- [ ] Can you state the three dangling-link policies?
- [ ] Can you give the meaning of `r`, `w`, `x` on a directory and explain why `x` is essential?
- [ ] Can you do `q = x div S` and then finish the translation for all three methods?
- [ ] Can you say why the linked method needs an *effective* block size, and get `301 + 4 = 305`?
- [ ] Can you compute how many index blocks a file needs?
- [ ] Can you draw an inode and compute its capacity from `E = block ÷ pointer`?
- [ ] Can you work out which pointer reaches logical block 6 in a 6-direct-pointer inode?
- [ ] Can you size a bitmap from a disk size and block size, and argue both sides of caching it?
- [ ] Can you explain the block-size trade-off curve in two sentences?
