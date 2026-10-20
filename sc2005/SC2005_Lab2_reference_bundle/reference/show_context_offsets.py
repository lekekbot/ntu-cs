#!/usr/bin/env python3
"""Teaching helper: prints the intended user-thread context offsets."""
fields = ["ra","sp","s0","s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11"]
for i, name in enumerate(fields):
    print(f"{name:>3} : {i*8:>3} bytes")
print("\nExpected total saved-context size: 112 bytes")
