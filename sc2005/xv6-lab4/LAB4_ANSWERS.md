# SC2005 Lab 4 — Virtual Memory Management

Answers, reasoning, and evidence. Branch: `lab4` (commit `8fc7997`, `add fault.c test program`).
All runs use `make CPUS=3 qemu` on QEMU 11.1.1 with `riscv64-elf-gcc` 16.2.0.

## Checkpoint 0 — Orient yourself before editing

| Item | Evidence |
|---|---|
| Active branch | `git checkout lab4` → `git branch --show-current` prints `lab4` |
| Boots to shell | `xv6 kernel is booting` / `hart 1 starting` / `hart 2 starting` / `init: starting sh` |
| `sys_sbrk()` | [kernel/sysproc.c:39](./kernel/sysproc.c:39) |
| `walk()` | [kernel/vm.c:86](./kernel/vm.c:86) |
| `usertrap()` | [kernel/trap.c:37](./kernel/trap.c:37) |
| Placeholders | [user/lazytest.c](./user/lazytest.c) originally defined `countvp()`/`countpp()` returning `0` |

One pre-existing build blocker had to be fixed before anything could run (see
[Appendix A](#appendix-a--pre-existing-build-blocker)).

---

## Part 1 — Understand page tables and eager allocation

### 1.1 Trace a page-table walk

Sv39 splits a 39-bit virtual address into four fields. A page is 4,096 bytes, so the offset needs
`log2(4096) = 12` bits, and each page-table page holds `4096 / 8 = 512` PTEs, so each index needs
`log2(512) = 9` bits. Working upward from bit 0:

| Field | Bits | Role |
|---|---|---|
| Level-2 (root) index | 38–30 | Select an entry in the level-2 page table |
| Level-1 index | 29–21 | Select an entry in a level-1 page table |
| Level-0 index | 20–12 | Select the level-0 PTE mapping the virtual page to a frame |
| Page offset | 11–0 | Select a byte within the mapped frame |

Bits 63–39 must be zero for the low half of the address space that xv6 uses (`MAXVA` is
`1L << 38`, [kernel/riscv.h:380](./kernel/riscv.h:380)). Each valid PTE holds a 44-bit PPN plus
flags; `PTE_V` means valid, `PTE_R`/`PTE_W`/`PTE_X` grant read/write/execute, and `PTE_U` allows
user-mode access ([kernel/riscv.h:358](./kernel/riscv.h:358)).

**`walk()`** ([kernel/vm.c:86](./kernel/vm.c:86)) starts at the root and, for levels 2 and 1:

* indexes the current table with `PX(level, va)`;
* if the entry is valid, follows `PTE2PA(*pte)` to the next-level table;
* if the entry is invalid and `alloc != 0`, calls `kalloc()`, zeroes the new **page-table page**,
  and installs a pointer entry `PA2PTE(...) | PTE_V` (no R/W/X, which is how xv6 marks a
  non-leaf entry);
* if the entry is invalid and `alloc == 0`, returns `0`.

At level 0 it returns `&pagetable[PX(0, va)]` **without checking that entry**. So `walk()` can
allocate *page-table pages* (frames holding PTEs), never process code/data frames, and it does not
even require the final leaf PTE to be valid.

**`walkaddr()`** ([kernel/vm.c:109](./kernel/vm.c:109)) is the safe lookup used by `copyin()`,
`copyout()` and `copyinstr()`: it calls `walk(alloc=0)` (never allocates), then rejects a missing
PTE, an invalid PTE, and — importantly — an entry without `PTE_U`. Returning `0` on `!PTE_U` keeps
the kernel from reading or writing a user page through a mapping the user itself may not touch.
That is exactly why the stack guard page is invisible to `walkaddr()` but still visible to a raw
`walk()`.

### 1.2 Follow a heap-growth request

Trace of one `morecore()` request:

1. **User allocator** — `morecore()` ([user/umalloc.c:47](./user/umalloc.c:47)) calls
   `sbrk(nu * sizeof(Header))` ([user/umalloc.c:54](./user/umalloc.c:54)).
2. **Stub** — the generated `sbrk` stub in `user/usys.S` loads `SYS_sbrk` into `a7` and executes
   `ecall`.
3. **Dispatch** — `syscall()` indexes the table with `p->trapframe->a7`
   ([kernel/syscall.c:141](./kernel/syscall.c:141)) and calls `sys_sbrk()`.
4. **`sys_sbrk()`** ([kernel/sysproc.c:39](./kernel/sysproc.c:39)) saves `addr = myproc()->sz`,
   calls `growproc(n)`, and returns `addr` (or `-1` on failure).
5. **`growproc()`** ([kernel/proc.c:260](./kernel/proc.c:260)) for `n > 0` calls
   `uvmalloc(p->pagetable, sz, sz + n, PTE_W)` and writes the returned size back to `p->sz`.
6. **`uvmalloc()`** ([kernel/vm.c:235](./kernel/vm.c:235)) rounds the old size up to a page
   boundary, then for every page:
   * `kalloc()` ([kernel/kalloc.c:69](./kernel/kalloc.c:69)) allocates a physical frame;
   * `memset(mem, 0, PGSIZE)` clears it;
   * `mappages()` ([kernel/vm.c:144](./kernel/vm.c:144)) calls `walk(..., alloc=1)` to create any
     missing intermediate page tables and installs the leaf PTE with `PTE_R|PTE_U|PTE_W`.

That is **eager allocation**: frames exist as soon as `sbrk()` returns, before the program touches
the memory. The page-table frames allocated by `walk()` are bookkeeping only; the data frames come
from the explicit `kalloc()` in `uvmalloc()`.

`n > 0` grows the break and allocates; `n == 0` changes nothing and merely reports the break;
`n < 0` calls `uvmdealloc()` ([kernel/vm.c:265](./kernel/vm.c:265)), which unmaps and frees whole
pages between the new and old page-rounded sizes (a shrink inside one page frees nothing). A
successful call always returns the **previous** break, so the caller learns the start of the new
region even though the break has already moved.

### Checkpoint 1

* A **virtual address** is what the program uses; a **PTE** is the 8-byte entry that translates one
  virtual page and carries its permissions; a **physical frame** is the 4,096-byte block of RAM that
  backs it.
* `walk(alloc=1)` may allocate **page-table pages** to hold PTEs; heap allocation allocates **data
  frames** and maps them. They are different kinds of frames, and only the latter hold process data.
* A positive `sbrk()` reaches `uvmalloc()`, which is where eager `kalloc()` + `mappages()` happen.

---

## Part 2 — Count virtual pages and physical frames

### 2.1 What each count includes

Both handlers use `myproc()` and the range `[0, p->sz)`:

```c
// Number of virtual pages intersecting [0, p->sz).
uint64 sys_countvp(void) {
  return PGROUNDUP(myproc()->sz) / PGSIZE;
}
```

([kernel/sysproc.c:54](./kernel/sysproc.c:54)) `PGROUNDUP` makes a partly used final page count as
one page. The range includes code, data, heap, the stack, and the stack guard page. `TRAMPOLINE`
and `TRAPFRAME` live at `MAXVA - PGSIZE` and `MAXVA - 2*PGSIZE`
([kernel/memlayout.h:44](./kernel/memlayout.h:44), [:59](./kernel/memlayout.h:59)), far above
`p->sz`, so they are naturally excluded.

```c
// Number of frames backing [0, p->sz).
uint64 sys_countpp(void) {
  ...
  for(a = 0; a < npages * PGSIZE; a += PGSIZE){
    pte_t *pte = walk(p->pagetable, a, 0);      // alloc = 0
    if(pte == 0 || (*pte & PTE_V) == 0) continue;    // hole / no page table
    if(PTE_FLAGS(*pte) == PTE_V) continue;           // points to another table
    n++;
  }
}
```

([kernel/sysproc.c:63](./kernel/sysproc.c:63)) Three details matter:

* `walk(..., 0)` **counts existing mappings without creating any** — the counting syscalls have no
  side effects.
* `walk()` rather than `walkaddr()` is required: `walkaddr()` rejects `!PTE_U`, which would drop the
  **guard page**, and the lab explicitly requires counting its frame.
* The `PTE_FLAGS(*pte) == PTE_V` check skips a valid entry that points to a lower-level table
  instead of a frame, mirroring the same check in `uvmunmap()`.

**Why the guard page has a frame but no `PTE_U`.** `exec()` allocates `(USERSTACK+1)` stack pages
([kernel/exec.c:81](./kernel/exec.c:81)) and then calls `uvmclear()` on the lowest one
([kernel/exec.c:86](./kernel/exec.c:86)). `uvmclear()`
([kernel/vm.c:347](./kernel/vm.c:347)) clears `PTE_U` while leaving `PTE_V` and the physical address
in place. The frame exists (so it is counted and later freed), but user mode cannot read or write
it, so overflowing the stack traps instead of silently corrupting data.

### 2.2 Wiring

| Layer | Change |
|---|---|
| Numbers | `SYS_countvp 22`, `SYS_countpp 23` — [kernel/syscall.h:23](./kernel/syscall.h:23) |
| Dispatch | `extern` declarations and table entries — [kernel/syscall.c:104](./kernel/syscall.c:104), [:131](./kernel/syscall.c:131) |
| Handlers | [kernel/sysproc.c:54](./kernel/sysproc.c:54), [:63](./kernel/sysproc.c:63) |
| Stubs | `entry("countvp")`, `entry("countpp")` — [user/usys.pl:39](./user/usys.pl:39) |
| Declarations | Already present in [user/user.h:25](./user/user.h:25) |
| Placeholders | Removed from [user/lazytest.c](./user/lazytest.c); everything else unchanged |

`user/usys.S` is generated, so only `usys.pl` was edited. The generated file now contains
`li a7, SYS_countvp` / `SYS_countpp`.

### 2.3 Eager-allocation result

`lazytest` with the **eager** kernel (Part 2 only, before Part 4):

```
Starting lazy allocation test...
Before: VP=4, PP=4
After sbrk(122880): VP=34, PP=34
Error: PP count changed immediately (should be lazy)
Touching pages...
After touching: PP=34
Success: PP count increased after touching pages
```

* `Before` is 4 pages: 2 pages of program text/data, 1 guard page, 1 user stack page
  (`USERSTACK` is 1 in [kernel/param.h:14](./kernel/param.h:14)), and `PP = VP` because every page is
  backed.
* `sbrk(4096*30)` reserves 30 pages: **VP +30 and PP +30 at once**, because `uvmalloc()` eagerly
  maps all 30 frames. The "PP count changed immediately" message is the expected eager result.
* Touching the pages changes nothing (`PP` stays 34): the frames were already there, so no faults
  occur for those pages.
* The final `Success: PP count increased after touching pages` is a **false positive** worth
  explaining: the check is `pp_after_touch - pp_before >= n_pages`, i.e. `34 - 4 >= 30`. It counts
  the increase that happened at `sbrk()` time. The printed label alone therefore does not prove
  demand paging; only the intermediate `After sbrk` line does.

### Checkpoint 2

**The counting boundary.** Both calls describe exactly the range `[0, p->sz)`, rounded up to a
page. That range contains the loaded program, its data, the heap, the user stack, and the stack
guard page — everything the process can name with an ordinary virtual address. Three groups are
deliberately outside it:

* the **page-table frames** themselves (they are reachable only through `satp`, not through any
  user virtual address, so no PTE in this range points at them);
* the **kernel stack**, which is mapped in the kernel page table, not `p->pagetable`;
* **`TRAMPOLINE` and `TRAPFRAME`**, which are fixed mappings at `MAXVA - PGSIZE` and
  `MAXVA - 2*PGSIZE` ([kernel/memlayout.h:44](./kernel/memlayout.h:44)), far above any `p->sz`
  this kernel allows.

A partially used final page still counts as a whole virtual page (hence `PGROUNDUP`), because the
hardware translates whole pages.

**The guard page.** `exec()` allocates `USERSTACK+1` pages and calls `uvmclear()` on the lowest
one, so that page has a real frame and a valid PTE whose `PTE_U` bit is cleared
([kernel/exec.c:86](./kernel/exec.c:86), [kernel/vm.c:347](./kernel/vm.c:347)). It is *inside* the
range and *has* a frame, so `countpp()` counts it. This is exactly why the handler must use
`walk()` and not `walkaddr()`: `walkaddr()` also rejects `!PTE_U`
([kernel/vm.c:109](./kernel/vm.c:109)) and would have reported one frame too few. The visible
effect is that `Before` prints `VP=4, PP=4` rather than `PP=3`.

**`lazytest` is really reaching the system calls.** With the supplied placeholders still in place,
the same program printed:

```
Before: VP=0, PP=0
After sbrk(122880): VP=0, PP=0
Error: VP count did not increase by 30
Success: PP count unchanged (lazy allocation verified)
```

All four values were the hard-coded `return 0`, and `VP` never moved even though `sbrk()` had
succeeded — proof the placeholders were being called, not the kernel. After removing them the
numbers follow the process: `VP` jumps by exactly the 30 pages requested and `PP` tracks the frames
that `kalloc()` actually handed out. Two more checks confirm the wiring end to end:

* `user/usys.S` (generated from [user/usys.pl](./user/usys.pl)) now contains
  `li a7, SYS_countvp` / `li a7, SYS_countpp`;
* [kernel/syscall.h](./kernel/syscall.h) and the dispatch table in [kernel/syscall.c](./kernel/syscall.c)
  map those numbers to `sys_countvp` / `sys_countpp`;
* `lazytest.c` no longer defines either function, so a missing syscall would fail to link rather
  than silently print zeros.

**The eager counts, within one run.** `Before: VP=4, PP=4` is the two program pages plus the guard
page and the one stack page (`USERSTACK` is 1 in [kernel/param.h:14](./kernel/param.h:14)); every
one of them is backed, so `PP = VP`. `After sbrk(122880): VP=34, PP=34` shows both counts rising by
30 at once, because `growproc()` still calls `uvmalloc()`, which `kalloc()`s and maps every page up
front. `After touching: PP=34` shows no further rise: the pages were already mapped, so the writes
cause no faults. That triple — `PP` up at `sbrk`, flat at touch, equal to `VP` throughout — is the
eager signature, and the "PP count changed immediately" line is its expected label. For contrast,
the Part 4 kernel on the same test prints `VP=34, PP=4` after `sbrk()` and `PP=34` only after the
touches.

---

## Part 3 — Observe page faults and trap handling

### 3.1 Diagnostic

Added to `usertrap()` ([kernel/trap.c:71](./kernel/trap.c:71)):

```c
} else if(r_scause() == 13 || r_scause() == 15){
  uint64 va = r_stval();
  ...
  printf("usertrap(): %s page fault pid=%d va=0x%lx sepc=0x%lx\n",
         r_scause() == 13 ? "load" : "store", p->pid, va, r_sepc());
  setkilled(p);
}
```

`scause` is 13 for a load page fault and 15 for a store/AMO page fault (`12` is an instruction
fetch). `stval` holds the faulting **virtual address**; `sepc` holds the **instruction address**.
Other traps keep their original handling and every faulting process is still terminated at this
stage.

### 3.2 Fault test (eager kernel, Part 3)

```
$ fault read
fault: pid 4, break 0x0000000000004000, target 0x0000000000004000, mode read
usertrap(): load page fault pid=4 va=0x4000 sepc=0xc2
$ fault write
fault: pid 5, break 0x0000000000004000, target 0x0000000000004000, mode write
usertrap(): store page fault pid=5 va=0x4000 sepc=0x94
```

`fault.c` calls `sbrk(0)` to learn the break without growing it. Here the break is already
page-aligned at `0x4000`, so `PGROUNDUP(end)` is `0x4000` itself — the first byte of the next,
never-allocated page. The printed target matches `stval` exactly. `sepc` (`0xc2`, `0x94`) is a code
address and is clearly different from `0x4000`; the fault is caused by the data access at
`stval`, not by fetching from `sepc`.

The process is killed: `setkilled(p)` makes `usertrap()` call `exit(-1)`, which frees its address
space. The shell is a different process waiting in `wait()`; its own page table and break are
untouched, so it simply prints the next prompt. The `ERROR: access returned` line is never reached
because the faulting process never resumes.

### 3.3 Trampoline trace

1. On the fault the CPU records `sepc` (faulting instruction), `scause` (13/15), `stval` (faulting
   address), switches to supervisor mode, and jumps to `stvec`, which `usertrapret()` set to
   `TRAMPOLINE + (uservec - trampoline)`.
2. `uservec` ([kernel/trampoline.S:22](./kernel/trampoline.S:22)) runs **with the user page table
   still installed**. It saves the user registers into `TRAPFRAME`, loads `kernel_sp`,
   `kernel_satp`, `kernel_trap` and `kernel_hartid` from the trapframe, executes `sfence.vma`, and
   writes `satp` with the kernel page table.
3. It jumps to `usertrap()`, which reads `r_scause()`, `r_sepc()` and `r_stval()` and handles the
   fault in kernel space.
4. `usertrapret()` prepares the trapframe for the next entry and calls `userret`
   ([kernel/trampoline.S:101](./kernel/trampoline.S:101)), which switches `satp` back to the user
   page table, restores the registers, and executes `sret` to resume at `epc`.

The trampoline must be mapped at the **same virtual address** in both page tables (`TRAMPOLINE`,
above every user mapping) because it is the code that performs the `satp` switch: after the switch,
the old mapping is gone, so the next instruction must still translate. `TRAPFRAME` is mapped just
below it, also at a fixed address, so `uservec` can find the saved state immediately after entry.

### Checkpoint 3

* Load and store faults were both demonstrated; `stval` (data address) and `sepc` (instruction
  address) are different values.
* `fault` picks `PGROUNDUP(sbrk(0))`, the first byte of the next page, which it never reserves; that
  is exactly the address reported in `stval`.
* Trap entry runs `uservec` under the user page table, switches to the kernel page table, enters
  `usertrap()`, and returns through `userret`; both stubs live in the shared trampoline mapping.

---

## Part 4 — Allocate physical frames on demand

### 4.1 Reserve the heap range

`growproc()` ([kernel/proc.c:260](./kernel/proc.c:260)) no longer calls `uvmalloc()`:

```c
if(n > 0){
  if(sz + n < sz || sz + n >= TRAMPOLINE)
    return -1;
  sz += n;
}
```

`p->sz` moves, so `sbrk(0)` and the returned old break stay correct, and negative requests still go
through `uvmdealloc()`. The wrap test (`sz + n < sz`) and the `TRAMPOLINE` limit keep the break away
from the reserved trap mappings. No frame, and not even a leaf PTE, is created; the range is a hole
that will fault on first access.

### 4.2 Handle a valid first access

The page-fault branch in `usertrap()` ([kernel/trap.c:71](./kernel/trap.c:71)) now classifies the
fault before acting:

```c
if(va < p->sz && va < MAXVA){
  pte = walk(p->pagetable, va, 0);
  if(pte == 0 || (*pte & PTE_V) == 0)
    lazy = 1;
}
```

A fault is repairable only when the address is inside the reserved range **and** there is no valid
level-0 PTE. A present mapping (for example the guard page, whose PTE is valid but lacks `PTE_U`)
is therefore a protection fault and is rejected; so is any address at or beyond `p->sz`. On the
eligible path the handler mirrors `uvmalloc()`: `kalloc()`, `memset(..., 0, PGSIZE)`, then
`mappages(..., PTE_W|PTE_R|PTE_U)`. If `kalloc()` fails, or `mappages()` fails after a frame was
allocated, the frame is freed (`kfree`) and the process is marked killed; `usertrap()` then exits it
cleanly. `p->trapframe->epc` is **not** advanced, unlike the system-call path, so `sret` re-executes
the load or store that faulted.

`fork()`/`copyin()`/`copyout()` handling for untouched pages is deliberately **not** implemented;
see [Limits](#limits-of-this-solution).

### 4.3 Reclaim a partially allocated heap

`uvmunmap()` ([kernel/vm.c:178](./kernel/vm.c:178)) previously panicked on any page without a
mapping. It now skips two hole cases:

```c
if((pte = walk(pagetable, a, 0)) == 0)
  continue;              // no intermediate page table at all
if((*pte & PTE_V) == 0)
  continue;              // invalid level-0 entry: page never touched
if(PTE_FLAGS(*pte) == PTE_V)
  panic("uvmunmap: not a leaf");   // retained
```

The not-a-leaf check is retained: a valid entry with no R/W/X bits points to a page table, not a
frame, and unmapping it would be a kernel bug. Present frames are still freed and their PTEs
cleared. Because `uvmdealloc()` and `uvmfree()` both go through `uvmunmap()`, shrinking and exiting
now tolerate untouched pages; `freewalk()` later releases the page-table pages that do exist.

### 4.4 Verification within each run

Full test:

```
Starting lazy allocation test...
Before: VP=4, PP=4
After sbrk(122880): VP=34, PP=4
Success: PP count unchanged (lazy allocation verified)
Touching pages...
After touching: PP=34
Success: PP count increased after touching pages
```

| Point | Expected | Measured |
|---|---|---|
| After reserving 30 pages | VP +30, PP unchanged | VP 4 → 34 (+30), PP 4 → 4 (0) |
| After touching all 30 | VP still +30, PP +30 | VP 34, PP 4 → 34 (+30) |

The final increase is exactly 30, not "at least 30": no extra frames were allocated by the test's
own `printf()` or loop bookkeeping.

Partial touch (loop temporarily reduced to one iteration, 30-page reservation unchanged):

```
After sbrk(122880): VP=34, PP=4
Touching pages...
After touching: PP=5
```

`PP` rises by exactly 1 and the process exits without a `panic`, so the 29 untouched pages were
skipped by `uvmunmap()`.

Negative `sbrk()` (reserve 30, touch 1, then `sbrk(-122880)`):

```
After touching: PP=5
sbrk(-122880) returned 0x0000000000022000
After shrink: VP=4, PP=4
```

The old break is returned, the one present heap frame is freed, the 29 holes are skipped, and there
is no panic. The original 30-iteration test was restored afterwards.

`fault read` / `fault write` after lazy allocation:

```
fault: pid 4, break 0x0000000000004000, target 0x0000000000004000, mode read
usertrap(): load page fault pid=4 va=0x4000 sepc=0xc2
fault: pid 5, break 0x0000000000004000, target 0x0000000000004000, mode write
usertrap(): store page fault pid=5 va=0x4000 sepc=0x94
```

Both accesses remain invalid. `fault` never calls a positive `sbrk()`, so its target equals
`p->sz` (`0x4000`); the handler's `va < p->sz` test fails and the process is killed. `lazytest`, by
contrast, reserves the range with `sbrk(30*4096)` first, so the same kind of first-touch fault falls
inside the range and is repaired, after which the instruction is retried and execution continues.

### Checkpoint 4

* Reservation without allocation and allocation on first touch are shown by `PP=4` right after
  `sbrk()` and `PP=34` only after the touches.
* The handler distinguishes a missing heap page (`va < p->sz` **and** no valid PTE) from a
  protection fault (valid PTE, e.g. the guard page) and from an address outside the range.
* The instruction is retried because `epc` is unchanged; only the system-call path does `epc += 4`.
* A partially touched heap is released without a panic (partial-touch and shrink runs).
* Lazy allocation saves memory because untouched reserved pages never get a data frame; `lazytest`
  does not test `fork()`, kernel `copyin`/`copyout` on untouched pages, or concurrent faults.

---

## Optional discussion — Stack growth

Legitimate downward growth could be recognised in `usertrap()` by checking that the fault address
is just below the current stack base (within one page, or within a bounded distance) and that the
PTE for the page is absent. The kernel would then `kalloc()` + `memset()` + `mappages()` a new
stack page, and move the guard: the old guard page must become a normal user page while the page
below it becomes the new guard (`uvmclear()` on the new lowest page). The guard page must stay
allocated but `PTE_U`-free so an overflow beyond the new limit still traps, and growth must be
capped so it cannot collide with the heap. In `exec()` the stack is currently a fixed
`USERSTACK + 1` pages ([kernel/exec.c:81](./kernel/exec.c:81)) with the lowest page cleared,
which is exactly the layout this scheme would update.

## Limits of this solution

Per the manual, this exercise covers user accesses to the heap and cleanup only:

* `uvmcopy()` ([kernel/vm.c:315](./kernel/vm.c:315)) still panics on an untouched page, so `fork()`
  of a process with lazy holes is unsupported.
* `copyin()`/`copyout()` still use `walkaddr()`, so a kernel copy to or from an untouched heap page
  fails instead of allocating.
* `lazytest` does not exercise either path, so its success does not prove them.

Supporting them would mean skipping holes in `uvmcopy()` (the child inherits the same `p->sz` and
can fault the pages in lazily) and teaching `copyin`/`copyout` to allocate for `va < p->sz`.

## Files changed

| File | Change |
|---|---|
| [kernel/syscall.h](./kernel/syscall.h) | `SYS_countvp`, `SYS_countpp` |
| [kernel/syscall.c](./kernel/syscall.c) | declarations and dispatch entries |
| [kernel/sysproc.c](./kernel/sysproc.c) | counting handlers; `sys_sbrk` unchanged |
| [kernel/proc.c](./kernel/proc.c) | `growproc()` reserves instead of mapping |
| [kernel/trap.c](./kernel/trap.c) | page-fault diagnostic and lazy first-touch handling |
| [kernel/vm.c](./kernel/vm.c) | `uvmunmap()` skips unallocated holes |
| [user/usys.pl](./user/usys.pl) | stubs for the two new syscalls |
| [user/lazytest.c](./user/lazytest.c) | local placeholders removed |
| [user/usertests.c](./user/usertests.c) | pre-existing build blocker only (Appendix A) |

## Appendix A — Pre-existing build blocker

`make` failed before any lab code could be built because GCC 16 promotes
`-Wunused-but-set-variable` and the tree uses `-Werror`:

```
user/usertests.c:2347:7: error: variable 'fsblocks' set but not used [-Werror=unused-but-set-variable=]
```

`fsfull()` accumulated a block count that is never read. Removing the variable and its increment
([user/usertests.c:2344](./user/usertests.c:2344)) restores the build; test behaviour is unchanged.

## Appendix B — Regression checks

`usertests` cases touching memory management were run individually under the lazy kernel:

| Test | Result | Relevant diagnostic |
|---|---|---|
| `stacktest` | `ALL TESTS PASSED` | guard page `load page fault va=0xfe90` → child killed, no allocation |
| `sbrkbasic` | `ALL TESTS PASSED` | — |
| `sbrkmuch` | `ALL TESTS PASSED` | — |
| `sbrkbugs` | `ALL TESTS PASSED` | expected `scause 0xc` from the test's own bad jumps |
| `nowrite` | `ALL TESTS PASSED` | store faults on `0x0`, `0x80000000`, `0x3fffffe000`, … — all rejected |
| `sbrk8000` | `ALL TESTS PASSED` | — |

## How to build and run

```
host$ make clean
host$ make CPUS=3 qemu
xv6$ lazytest
xv6$ fault read
xv6$ fault write
```

Leave QEMU with `Ctrl-a`, release, then `x`.
