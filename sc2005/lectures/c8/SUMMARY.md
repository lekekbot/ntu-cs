# Memory Organization — Summary (one page)

Five lectures, one question: **how does a logical address become a physical address, and what does
it cost?**

---

## The 60-second version

1. A process executes in its own **logical address space** (process image: text, data, heap, stack),
   starting at 0. There is only **one physical memory**, shared.
2. **Where** the code and data get bound to physical addresses can be decided at **compile time**
   (absolute), **load time** (relocatable + loader), or **execution time** (add base on every
   reference). Only execution-time binding lets a process **move** — so that is the assumption for
   the rest of the chapter.
3. **Contiguous allocation** keeps the image in one run. Fixed partitions are pre-cut (→ internal
   fragmentation); dynamic partitions create **holes** on demand (→ external fragmentation, fixed
   by first/best/worst-fit and compaction).
4. **Paging** chops logical memory into **pages** and physical memory into equal **frames**, and
   scatters the pages. No external fragmentation; internal fragmentation only in the last page.
   Translation uses a **page table**; that costs an extra memory access → **TLB**; a huge page table
   needs **multi-level paging**; "one table per process" is replaced by a single **inverted page
   table** (saves memory, costs search time).
5. **Segmentation** uses variable-size **logical** units with a **base + limit** table. It gives
   per-segment protection but suffers external fragmentation.

---

## The schemes at a glance

| Scheme | Contiguous? | Unit | Map structure | Internal frag. | External frag. |
|---|---|---|---|---|---|
| Fixed partitioning | yes | fixed partitions | relocation register | ✅ | ❌ |
| Dynamic partitioning | yes | holes | relocation register | ❌ | ✅ |
| Paging | no | 512 B–8 KB pages/frames | page table | ✅ (last page) | ❌ |
| Segmentation | no | variable segments | segment table (base, limit) | ❌ | ✅ |
| Inverted paging | no | pages/frames | one system-wide table | ✅ (last page) | ❌ |

---

## Address formats

```
Contiguous:    [        offset from start of image        ]     physical = base + offset

Paging:        [ page number p | offset d ]                     p = m-n bits, d = n bits
                                                               physical = frame : d

Two-level:     [ P1 | P2 | offset ]                             e.g. 10 | 10 | 12

Segment.:      [ segment s | offset d ]                         physical = base[s] + d
                                                               require d < limit[s]
```

---

## Formulas

```
number of pages        = 2^m / 2^n = 2^(m-n)        (LAS 2^m, page size 2^n)
page table size        = #pages × entry size
inverted table size    = #frames × entry size       (independent of #processes)
EMAT, no TLB           = 2μ
EMAT, with TLB         = α(ε+μ) + (1-α)(ε+2μ)
                       = ε + (2-α)μ
```

`μ` = memory access time, `ε` = TLB access time, `α` = hit ratio, `ε ≪ μ`.

---

## Worked numbers worth remembering

**Paging example (part 03).** 16 B logical space, 4 B pages → 4 pages; 32 B physical, 4 B frames →
8 frames. Mapping `0→5, 1→6, 2→1, 3→2`.
Logical `0111` → `p=01` (page 1), `d=11` (offset 3) → frame `110` → physical `11011` = **27**.

**Two-level paging (part 04).** 32-bit address, 4 KB pages, 4 B PTEs.
→ 2^20 pages → page table 4 MB (too big to keep contiguous) → page the table:
`2^22 / 2^12 = 2^10` pages; `2^12 / 4 = 2^10` entries per page → **P1 = 10, P2 = 10, offset = 12**.

**Contiguous example (part 02).** 2560K memory, 400K OS.
t=0: P1 600 + P2 1000 + P3 300 → 260K left (P4, P5 wait).
t=5: P2 exits → P4 700 loads, 300K left (P5 still waits).
t=10: P1 exits → P5 500 loads, 100K left.
Final holes: 100K, 300K, 260K → external fragmentation.
With **compaction** at t=5, the 300K + 260K holes merge (~560K) and P5 loads at t=5.

**Segmentation (part 05).** `<3,128>`, segment 3 has base 3,200 and limit 1,100 → 128 < 1,100 →
physical = **3,328**.

---

## Ten things that decide exam marks

1. **Page** = logical, **frame** = physical, same size.
2. **Offset bits = log2(page size)**; page-number bits = address bits − offset bits.
3. **Page table size ∝ logical space**; **inverted table size ∝ physical memory**.
4. Paging without TLB → **two** memory accesses → EMAT = **2μ**.
5. TLB hit → **ε + μ**; miss → **ε + 2μ**; weighted by α → **ε + (2−α)μ**.
6. Inverted page table entry must include the **PID**.
7. Two-level paging exists because a big page table cannot be found as one **contiguous** block.
8. **Compaction requires execution-time binding.**
9. **Segmentation checks the offset against the limit**; paging does not need to.
10. Internal: fixed partitioning, paging. External: dynamic partitioning, segmentation.

---

## What is *not* in this series

* **Virtual memory** (demand paging, page replacement, thrashing) — that is the *next* lecture
  series; part 05 ends by announcing it.
* Multi-level paging is skipped in the main lecture; it is covered only in the supplementary
  recording 04.
* Page-replacement algorithms (FIFO/LRU/optimal) are not discussed here.
