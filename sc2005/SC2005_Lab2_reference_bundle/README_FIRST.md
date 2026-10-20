# SC2005 Lab 2 reference bundle

This is a teaching/reference bundle made from the public `lab2` branch described in the
Lab 2 manual. It is **not** an instructor-provided solution repository.

## What is included

- `completed/user/uthread.c`
  - saved user-thread context
  - 16-byte-aligned per-thread stack
  - `thread_schedule()` context-switch call
  - new-thread `ra`/`sp` initialization
- `completed/user/uthread_switch.S`
  - save/restore `ra`, `sp`, and `s0`–`s11`
- `completed/kernel_scheduler_strict_even.c`
  - replacement `scheduler()` body for the Part 2 strict even-PID policy
- `patches/part2_strict_even_scheduler.patch`
  - patch for the stock `kernel/proc.c`
- `patches/part3_user_threads.patch`
  - patch for the stock user-thread files
- `reference/REFERENCE_MAP.md`
  - paths, symbols, original lab2 line locations, and what each item proves
- `reference/WHAT_THE_LAB_TESTS.md`
  - compact conceptual map for studying

## Recommended way to use it

Keep two copies/branches of the lab:

1. **Part 2 copy:** apply the strict-even scheduler patch and run with `CPUS=1`.
2. **Part 3/final copy:** keep the stock scheduler, but use the completed user-thread files.

That matches the lab manual's instruction to save the strict-priority scheduler evidence and
restore the stock scheduler before Part 3/final verification.

## Apply the user-thread reference files

From the root of your `lab2` checkout:

```sh
cp /path/to/bundle/completed/user/uthread.c user/uthread.c
cp /path/to/bundle/completed/user/uthread_switch.S user/uthread_switch.S
```

Or use:

```sh
patch -p1 < /path/to/bundle/patches/part3_user_threads.patch
```

## Apply the Part 2 scheduler reference

Use a disposable copy/branch, then:

```sh
patch -p1 < /path/to/bundle/patches/part2_strict_even_scheduler.patch
```

Run Part 2 with:

```sh
make clean
make CPUS=1 qemu
```

Inside xv6:

```sh
schedtest
starvetest
```

For `starvetest`, use `Ctrl-p` to inspect the process table and `Ctrl-a x` to exit QEMU.

## Part 3 check

Restore the stock scheduler first, then build and run:

```sh
make clean
make CPUS=3 qemu
```

Inside xv6:

```sh
uthread_test
```

Expected source-defined checks from the manual:
- all three threads start;
- each prints its own values 0 through 99;
- each reports exit after 100;
- the library eventually reports no runnable threads.

## Important limitation

This bundle was source-checked against the public `lab2` branch and the Lab 2 manual, but I
could not run the RISC-V/QEMU build in this environment because the xv6 RISC-V toolchain is
not installed here. Treat it as a reference implementation and verify it in your course VM.
