# SC2005 Lab 4 — Revision Notes

Study material for the Lab 4 checkpoints. Command output and evidence live in
[LAB4_ANSWERS.md](./LAB4_ANSWERS.md); this file is the *learning*: the concepts, the "why", and
the traps. Everything here is answerable without the lab in front of you.

---

## The lab in one paragraph

xv6 allocates physical memory **eagerly**: the moment `sbrk()` returns, every page of the new range
already has a frame. This lab measures that (`countvp`/`countpp`), proves it is wasteful, then
replaces it with **demand paging**: `sbrk()` only moves a number (`p->sz`), and the *first access*
to each page traps into the kernel, which allocates and maps a frame then retries the faulting
instruction. The whole exercise is one sentence — **separating "the address is reserved" from "the
memory exists"** — and the price of that separation is that every place which assumed
"reserved ⇒ mapped" now has to tolerate holes.

---

## The single idea behind everything in this lab

> **A virtual address is a promise; a physical frame is the payment.**

| | Virtual page | PTE | Physical frame |
|---|---|---|---|
| What it is | a 4 KiB numbering slot in a process's address space | an 8-byte entry in a page table that maps one virtual page | a 4 KiB block of real RAM |
| Created by | `sbrk()` moving `p->sz` | `mappages()` | `kalloc()` |
| Exists after lazy `sbrk()`? | **yes** | no | no |

Three different counters follow from that table, and exam questions love to blur them:

- **`VP` (`countvp`)** — how many virtual pages the range `[0, p->sz)` covers. Depends only on `p->sz`.
- **`PP` (`countpp`)** — how many of those pages currently have a frame. Depends on how many faults
  have happened.
- **page-table frames** — frames that hold *PTEs*, allocated by `walk()` when it needs a new level.
  These are never counted by either function, because no user virtual address points at them.

That third row is the source of the single most common wrong answer in this lab: *"`walk()`
allocates memory, so lazy allocation still allocates."* `walk(alloc=1)` allocates **bookkeeping**,
not data. `uvmalloc()`'s explicit `kalloc()` is what allocates **data**.

---

## Background you must have cold: Sv39 translation

### The bit layout

A 39-bit virtual address (xv6 uses the low half only, `MAXVA = 1 << 38`,
[kernel/riscv.h:380](./kernel/riscv.h:380)) splits into four fields:

```
 bit 38    30 29    21 20    12 11         0
+-----------+---------+---------+-----------+
| L2 idx    | L1 idx  | L0 idx  |  offset   |
| 9 bits    | 9 bits  | 9 bits  |  12 bits  |
+-----------+---------+---------+-----------+
```

Why those sizes:

- page = 4,096 B = 2¹² ⇒ offset needs **12** bits;
- one page holds `4096 / 8 = 512` PTEs = 2⁹ ⇒ each index needs **9** bits;
- `12 + 9 + 9 + 9 = 39` ⇒ Sv39.

Strictly, bits 63–39 must replicate bit 38 (sign extension). xv6 caps `MAXVA` at `1 << 38`, so bit
38 is always 0 and those upper bits must all be zero — no sign extension in the low half.
`PX(level, va)` extracts each index ([kernel/riscv.h:374](./kernel/riscv.h:374)).

### The PTE

An 8-byte entry: `PPN[2:0]` (44 bits) plus flags in the low 10 bits
([kernel/riscv.h:358](./kernel/riscv.h:358)):

| Flag | Bit | Meaning |
|---|---|---|
| `PTE_V` | 0 | valid — this entry is meaningful |
| `PTE_R` | 1 | readable |
| `PTE_W` | 2 | writable |
| `PTE_X` | 3 | executable |
| `PTE_U` | 4 | user mode may use this mapping |

`PTE2PA`/`PA2PTE` convert between the encoded PPN and a physical address by shifting through bit 12
and bit 10 respectively. `PTE_FLAGS(pte) = pte & 0x3FF`.

**The "valid but no permission bits" trick.** xv6 marks a *non-leaf* page-table entry — one that
points to the next level of the tree — as `PTE_V` only, with no `R`/`W`/`X`. So:

- `PTE_FLAGS(*pte) == PTE_V` ⇒ this entry points to **another page table**, not to a frame.

That single test appears in `uvmunmap()` and in `countpp()`, and forgetting it in either place is a
real bug (freeing or counting a page table as if it were data).

### `walk()` — the one function to be able to draw

[kernel/vm.c:86](./kernel/vm.c:86):

```c
for(int level = 2; level > 0; level--) {
  pte_t *pte = &pagetable[PX(level, va)];
  if(*pte & PTE_V) {
    pagetable = (pagetable_t)PTE2PA(*pte);   // descend
  } else {
    if(!alloc || (pagetable = (pde_t*)kalloc()) == 0)
      return 0;                              // missing table, alloc==0 → give up
    memset(pagetable, 0, PGSIZE);
    *pte = PA2PTE(pagetable) | PTE_V;        // install pointer entry (V only)
  }
}
return &pagetable[PX(0, va)];                // level 0: return the slot, unexamined
```

Four facts to memorise:

1. It descends levels 2 → 1 only. Level 0 is returned **by address**, not checked.
2. It can therefore return a pointer to a **non-valid** leaf PTE. "`walk()` succeeded" ≠ "the page
   is mapped". You must test `*pte & PTE_V` yourself.
3. `alloc != 0` allocates **page-table pages**. Never data frames.
4. `alloc == 0` makes it a pure lookup with no side effects — this is why `countpp()` and
   `uvmunmap()` use it: they must not create mapping structure just by looking.

### `walkaddr()` — `walk()` plus the permission check

[kernel/vm.c:109](./kernel/vm.c:109) calls `walk(alloc=0)` then rejects three cases: no PTE, not
`PTE_V`, and **not `PTE_U`**. It returns a *physical address*, and it is what `copyin`/`copyout`/
`copyinstr` use.

The `!PTE_U` rejection is the crux of the guard-page question: the guard page has a valid, backed
mapping, but no `PTE_U`. `walkaddr()` refuses it (kernel-mediated copies cannot touch it), while a
raw `walk()` sees it and reports it as present. **Choosing `walk` vs `walkaddr` is choosing whether
the guard page counts.**

---

## Checkpoint 1 — The eager path from `sbrk()` to `kalloc()`

Be able to recite this chain; it is the spine of Parts 1, 2 and 4.

```
user: malloc() → morecore()                     user/umalloc.c:47
  → sbrk(nu * sizeof(Header))                   user/umalloc.c:54
  → stub: li a7, SYS_sbrk ; ecall               user/usys.S  (generated)
kernel: syscall() indexes syscalls[a7]          kernel/syscall.c
  → sys_sbrk()  addr = p->sz ; growproc(n)      kernel/sysproc.c:39
  → growproc()  n>0: uvmalloc(...)              kernel/proc.c:260
  → uvmalloc()  loop: kalloc + memset + mappages  kernel/vm.c:235
  → mappages()  walk(...,1) + install leaf PTE  kernel/vm.c:144
```

`uvmalloc()` rounds `oldsz` **up** to a page boundary first, so a partially used final page is
handled correctly, then for each page: `kalloc()` → `memset(0)` → `mappages(..., PTE_R|PTE_W|PTE_U)`.

### `sbrk()` returns the *old* break

```c
uint64 addr = myproc()->sz;
if(growproc(n) < 0) return -1;
return addr;
```

`sys_sbrk()` ([kernel/sysproc.c:39](./kernel/sysproc.c:39)) reads `p->sz` *before* growing, so a
successful call returns the **previous** break — the start of the new region — even though the break
has already moved. That is why `lazytest` can do `char *start = sbrk(size)` and immediately index
`start[0]`.

| `n` | Effect |
|---|---|
| `n > 0` | grow: `uvmalloc()` (eager) or just move `p->sz` (lazy) |
| `n == 0` | nothing changes; used purely to **query** the current break (`fault.c` does this) |
| `n < 0` | `uvmdealloc()` → `uvmunmap()`, frees whole pages only |

`n == 0` is a favourite trick: `fault.c` uses `sbrk(0)` to learn the break *without* reserving
anything, which is precisely why its target page stays invalid even after lazy allocation exists.

---

## Checkpoint 2 — Counting virtual pages vs physical frames

### `countvp` — arithmetic, no memory access

```c
return PGROUNDUP(myproc()->sz) / PGSIZE;
```

`PGROUNDUP` because the hardware translates whole pages: a page with 1 byte used is a full virtual
page. The range is `[0, p->sz)`, which contains code, data, heap, user stack, **and the stack guard
page**.

### `countpp` — walk the range, count leaves

```c
for(a = 0; a < npages * PGSIZE; a += PGSIZE){
  pte_t *pte = walk(p->pagetable, a, 0);
  if(pte == 0 || (*pte & PTE_V) == 0) continue;   // hole
  if(PTE_FLAGS(*pte) == PTE_V) continue;          // points to another table
  n++;
}
```

Three decisions, each defensible in one sentence:

1. **`alloc = 0`** — counting must be side-effect free. With `alloc = 1` you would allocate page
   tables and change the very thing you are measuring.
2. **`walk`, not `walkaddr`** — `walkaddr` rejects `!PTE_U` and would drop the guard page, making
   `PP` one too low.
3. **`PTE_FLAGS == PTE_V` skip** — a valid non-leaf entry is a page table, not a frame.

### What is *outside* `[0, p->sz)` and why it stays out

| Excluded | Reason |
|---|---|
| Page-table frames | reachable only through `satp`, never through a user virtual address |
| Kernel stack | mapped in the **kernel** page table, not `p->pagetable` |
| `TRAMPOLINE` (`MAXVA - PGSIZE`) | fixed high mapping, above any `p->sz` |
| `TRAPFRAME` (`MAXVA - 2*PGSIZE`) | same |

([kernel/memlayout.h:44](./kernel/memlayout.h:44), [:59](./kernel/memlayout.h:59))

### The guard page — the question this lab always asks

In `exec()`, the stack is `USERSTACK + 1` pages ([kernel/exec.c:83](./kernel/exec.c:83), with
`USERSTACK == 1` in [kernel/param.h:14](./kernel/param.h:14)). The **lowest** of those pages is
then passed to `uvmclear()` ([kernel/exec.c:86](./kernel/exec.c:86)), which clears `PTE_U` while
leaving `PTE_V` and the physical address intact ([kernel/vm.c:347](./kernel/vm.c:347)).

So the guard page:

- **has** a frame (`kalloc` allocated it, and `uvmfree` will free it);
- **is** inside `[0, p->sz)`;
- **is** invisible to user mode and to `walkaddr()`;
- **is** counted by `countpp()`, because `countpp()` deliberately looks at it.

Its purpose: overflowing the stack downwards hits a page that exists but is not user-accessible, so
the hardware raises a **protection** fault instead of the access silently corrupting whatever frame
happened to follow.

Numeric sanity check for an idle process: 2 program pages + 1 guard + 1 stack = `VP=4, PP=4`.

### Why the test's "success" line can lie

`lazytest`'s final check is

```c
if (pp_after_touch - pp_before >= n_pages)
    printf("Success: PP count increased after touching pages\n");
```

Under the **eager** kernel, `pp_after_touch - pp_before` is `34 - 4 = 30`, so it prints "Success" —
but the 30 frames appeared at `sbrk()` time, not at touch time. The `>=` comparison cannot tell the
two apart.

> **The label on a print statement is not evidence.** Only the intermediate
> `After sbrk(...): VP=34, PP=34` line distinguishes eager from lazy. Being able to point at which
> line of output actually carries the proof is the checkpoint.

The eager signature is a triple: `PP` rises **at** `sbrk`, is **flat** at touch, and **equals** `VP`
throughout. The lazy signature is: `PP` flat at `sbrk` (`VP=34, PP=4`), then rising to `VP` only
after the touches.

---

## Checkpoint 3 — Page faults and the trap path

### Reading the fault

| Register | Holds |
|---|---|
| `scause` | **why**: 12 = instruction page fault, 13 = load page fault, 15 = store/AMO page fault |
| `stval` | **the faulting virtual address** (the data address for 13/15) |
| `sepc` | **the address of the instruction** that faulted |

The exam-favourite distinction: for a load/store fault `stval` is a *data* address and `sepc` is a
*code* address, and they are unrelated numbers. `fault read` printing `va=0x4000 sepc=0xc2` shows
this: the fault came from touching `0x4000`, not from fetching at `0xc2`.

`fault.c` computes its target as `PGROUNDUP(sbrk(0))`. If the break is already page-aligned, that is
the **first byte of the next, never-reserved page** — so the access must remain invalid *after* lazy
allocation is implemented too. It is the negative control for Part 4.

### Why `sepc` is not advanced, and why that is the whole point

In the system-call branch of `usertrap()`, xv6 does `p->trapframe->epc += 4` because `ecall` must
not be re-executed. In the page-fault branch it does **not** advance `epc`, so `sret` returns to the
same instruction, which faults again — and this time finds the page mapped, so it succeeds. **The
lazy-allocation "retry" needs no retry loop; it is a consequence of not touching `epc`.**

### The trampoline, in four steps

1. CPU records `sepc`/`scause`/`stval`, enters supervisor mode, jumps to `stvec` — which
   `usertrapret()` set to `TRAMPOLINE + (uservec - trampoline)`.
2. `uservec` ([kernel/trampoline.S:22](./kernel/trampoline.S:22)) runs **with the user page table
   still active**: saves user registers into `TRAPFRAME`, loads `kernel_sp`, `kernel_satp`,
   `kernel_trap`, `kernel_hartid`, runs `sfence.vma`, writes `satp` with the kernel page table.
3. Jumps to `usertrap()` ([kernel/trap.c:37](./kernel/trap.c:37)) in kernel space.
4. `usertrapret()` → `userret` ([kernel/trampoline.S:101](./kernel/trampoline.S:101)) switches `satp`
   back to the user table, restores registers, `sret`.

**Why `TRAMPOLINE` must be the same virtual address in both page tables:** the code that switches
`satp` is itself executing. The instant `satp` changes, the old mapping is gone — so the very next
instruction must still translate. Only a page mapped identically in both tables can survive the
switch. `TRAPFRAME` sits one page below it, also fixed, so `uservec` can find the saved registers
without knowing anything about this process.

---

## Checkpoint 4 — Demand paging

Three edits, each removing one of the three places that assumed "reserved ⇒ mapped".

### 4.1 `growproc()` stops allocating

```c
if(n > 0){
  if(sz + n < sz || sz + n >= TRAMPOLINE)
    return -1;
  sz += n;
}
```

- `p->sz` still moves, so `sbrk(0)` and the returned old break stay correct.
- The wrap check `sz + n < sz` and the `TRAMPOLINE` ceiling stop `p->sz` from running into the
  fixed high mappings — without the ceiling, a `va` that passed `va < p->sz` would eventually
  collide with the trampoline.
- Negative `n` still goes through `uvmdealloc()`.

### 4.2 `usertrap()` repairs only genuinely-missing heap pages

```c
if(va < p->sz && va < MAXVA){
  pte = walk(p->pagetable, va, 0);
  if(pte == 0 || (*pte & PTE_V) == 0)
    lazy = 1;
}
```

The condition is a **conjunction of three** requirements; drop any one and the kernel becomes wrong:

| Requirement | What breaks if you drop it |
|---|---|
| `va < p->sz` | wild pointers anywhere in the address space get frames — the fault test stops terminating, and `fault`'s target (`== p->sz`) would be wrongly repaired |
| no valid PTE | a **protection** fault (guard page: valid, `!PTE_U`) would be "fixed" into a usable page, destroying the stack overflow check |
| `va < MAXVA` | an address above `MAXVA` would reach `walk()`, which `panic`s on `va >= MAXVA` |

On the eligible path the handler mirrors `uvmalloc()` exactly: `kalloc()` → `memset(0)` →
`mappages(PGROUNDDOWN(va), PGSIZE, mem, PTE_W|PTE_R|PTE_U)`.

**The three-way classification** is the checkpoint's real content:

| Fault address | PTE | Verdict |
|---|---|---|
| `< p->sz` | absent | lazy first touch → allocate |
| `< p->sz` | valid, `!PTE_U` (guard page) | protection fault → kill |
| `>= p->sz` | anything | invalid access → kill |

### 4.3 Cleanup must tolerate holes — `uvmunmap()`

```c
if((pte = walk(pagetable, a, 0)) == 0) continue;   // no page table at all
if((*pte & PTE_V) == 0)                continue;   // reserved, never touched
if(PTE_FLAGS(*pte) == PTE_V) panic("uvmunmap: not a leaf");  // kept!
```

Before this change `uvmunmap()` panicked on any unmapped page. Now it skips holes — because
`uvmdealloc()` (shrink) and `uvmfree()` (exit) both route through it, and a lazily reserved heap is
mostly holes.

Note the **asymmetry** with the error handling in the fault handler: `kalloc()` failure and
`mappages()` failure both `kfree()` the fresh frame and `setkilled(p)` — never leak. `usertrap()`
then sees `killed(p)` and calls `exit(-1)`, which unwinds through `uvmfree()` → `uvmunmap()`
successfully *because* holes are skipped.

`freewalk()` is what eventually releases the page-table pages themselves.

### 4.4 Why `fork()` and `copyin`/`copyout` are out of scope

`uvmcopy()` ([kernel/vm.c:315](./kernel/vm.c:315)) still panics on an unmapped page, and
`walkaddr()` still returns 0 for a lazy hole. So:

- `fork()` of a process with untouched lazy pages would panic;
- a kernel `copyin`/`copyout` to an untouched heap page would fail.

The lab's scope is *user* accesses plus cleanup. Saying this explicitly — and knowing the fix
(skip holes in `uvmcopy`, allocate for `va < p->sz` in `copyin`/`copyout`) — is worth marks, because
it shows you know what the passing test does **not** prove.

---

## Optional discussion — Stack growth

Downward stack growth is the mirror image of lazy heap: the fault address is **below** the current
stack, not inside `[0, p->sz)`. A scheme:

1. In `usertrap()`, treat the fault as legitimate growth only if `va` is within one page (or a small
   bounded distance) **below** the current stack base and its PTE is absent.
2. `kalloc()` + `memset()` + `mappages()` a new user page for it.
3. **Move the guard**: the old guard page becomes an ordinary user page, and the page below the new
   lowest page gets `uvmclear()`.
4. Cap growth so the stack cannot collide with the heap, and re-check every run that an overflow
   beyond the new limit still traps.

The reason step 3 is mandatory: leaving the old guard `!PTE_U` would make the *newly grown* page
unusable; removing the guard entirely would silently convert stack overflow into data corruption.

---

## Traps that cost marks

| Trap | Correct version |
|---|---|
| "`walk()` allocates frames, so lazy allocation still allocates on `sbrk`." | `walk(alloc=1)` allocates **page-table pages** only; data frames come from `uvmalloc`'s `kalloc`. |
| "`walk()` returned non-NULL, so the page is mapped." | Level 0 is returned unchecked; you must test `*pte & PTE_V`. |
| "Use `walkaddr()` to count frames." | It rejects `!PTE_U`, so the guard page is missed. Use `walk(...,0)`. |
| "The guard page has no frame." | It has one; only `PTE_U` is cleared. It is counted, and later freed. |
| "`countvp` should count non-zero pages." | It counts **whole virtual pages** in `[0, p->sz)`, hence `PGROUNDUP`. |
| "`sbrk(n)` returns the new break." | It returns the **old** break (the start of the new region). |
| "`PP` went up, so lazy allocation works." | Check **when**: at `sbrk` (eager) or at touch (lazy). `lazytest`'s last line proves neither. |
| "`stval` is the instruction address." | `stval` = faulting **data** address; `sepc` = **instruction** address. |
| "`scause == 13` is an instruction fault." | 12 = instruction, 13 = load, 15 = store/AMO. |
| "The handler must increment `epc` to retry." | Not incrementing `epc` *is* the retry. Only the syscall path does `epc += 4`. |
| "Any fault below `p->sz` should be repaired." | Only if no valid PTE — otherwise a guard-page protection fault becomes an allocation. |
| "`uvmunmap` should skip anything non-leaf too." | No: `PTE_FLAGS == PTE_V` on a valid entry means a page table, which is a kernel bug — keep the panic. |
| "`fork()` works because `lazytest` passes." | `uvmcopy()` still panics on holes; `lazytest` never forks. |
| "Lazy allocation makes `sbrk` free." | It makes it cheap; the frames are still allocated on touch, and `kalloc` failure must be handled. |

---

## Self-check questions

1. Trace `0x4000` through Sv39. Which index selects the root table, and what does `walk()` return
   for it in a process whose `p->sz` is `0x4000`?
2. Why does `countpp()` use `alloc = 0`? What would change if it used `alloc = 1`?
3. A process has `p->sz = 4096`. How many virtual pages does `countvp()` report, and how many frames
   does `countpp()` report if nothing is mapped yet? What if the range is the freshly `exec`'d image?
4. Give the exact condition under which the page-fault handler allocates a frame, and name the two
   other cases it must reject.
5. Why must `TRAMPOLINE` be mapped at the same virtual address in both page tables?
6. After removing `uvmalloc()` from `growproc()`, which three call sites would panic or fail on a
   hole, and what is the minimal change for each?
7. `fault write` and `lazytest` both cause store page faults at `0x4000`. Why does one terminate the
   process and the other continue?

---

## Cross-lab connections

* **Lab 2** was about *who runs next*; the page-fault here is a **scheduling-relevant trap**: the
  process does not get `yield()`ed, it is either repaired and retried or killed via `setkilled` →
  `exit(-1)`.
* **Lab 3**'s `sleep`/`wakeup` machinery and spinlocks are absent here on purpose: a page fault is
  handled entirely by the faulting process on its own page table, so there is no shared state to
  protect. The concurrency hazards in this lab are of a different kind — *stale assumptions* about
  mappings, not races.
* **Lab 1**'s `exec()` is where the address-space layout (`p->sz`, guard page, stack) is created;
  Part 4's accounting is only meaningful against that layout.
* The recurring theme across all four labs: **a data structure's invariant must be re-checked after
  every change to the mechanism that maintains it.** Part 2 adds a query, Part 4 changes the
  invariant, and every consumer of that invariant (`uvmunmap`, `uvmcopy`, `copyin`, `fork`) is now a
  candidate for a latent bug.
