# ---------- Problem 1: reimplement len for lists ----------


def my_len_recursive(xs):
    """Recursive (no accumulator)."""
    if xs == []:
        return 0
    return 1 + my_len_recursive(xs[1:])

def list_length1(L):
    if L:
        return 1 + list_length1(L[1:])
    return 0

def list_length2(L): # tail-recursive with accumulator
    return list_length2_helper(L)

# n is an accumulator
def list_length2_helper(L, acc=0):
    if L:
        return list_length2_helper(L[1:], acc + 1)
    return acc



# -----------------------------------------------------------------------------------------
def my_len_tail(xs):
    """Tail-recursive using an accumulator."""

    def helper(rest, acc):
        if rest == []:
            return acc
        return helper(rest[1:], acc + 1)

    return helper(xs, 0)


def my_len_iter(xs):
    """Iterative (no recursion)."""
    count = 0
    for _ in xs:
        count += 1
    return count


# ---------- Problem 2: count vowels in a string ----------

_VOWELS = set("aeiouAEIOU")


def count_vowels_recursive(s):
    """Recursive (no accumulator)."""
    if s == "":
        return 0
    head, tail = s[0], s[1:]
    return (1 if head in _VOWELS else 0) + count_vowels_recursive(tail)


def count_vowels_tail(s):
    """Tail-recursive with accumulator."""

    def helper(rest, acc):
        if rest == "":
            return acc
        head, tail = rest[0], rest[1:]
        return helper(tail, acc + (1 if head in _VOWELS else 0))

    return helper(s, 0)


def count_vowels_iter(s):
    """Iterative (no recursion)."""
    count = 0
    for ch in s:
        if ch in _VOWELS:
            count += 1
    return count


# ---------- Problem 3: binary strings of length n without consecutive '00' ----------


def binaries_no_consecutive_zeros(n):
    """
    Recursive generation of all binary strings of length n (n >= 1)
    with no '00' substring.
    """
    if n == 1:
        return ["0", "1"]
    # Build from length n-1 strings by appending '0' or '1' as allowed
    shorter = binaries_no_consecutive_zeros(n - 1)
    out = []
    for s in shorter:
        # Always can append '1'
        out.append(s + "1")
        # Append '0' only if last char isn't '0'
        if s[-1] != "0":
            out.append(s + "0")
    return out


# ---------- Problem 4: binary strings length n with Hamming weight <= c ----------


def binaries_with_weight_at_most(n, c):
    """
    Recursive generation of all binary strings of length n and
    Hamming weight (number of '1's) <= c. Assumes n >= 1, c >= 0.
    """
    if n == 0:
        return [""]  # base to build on

    res = []
    # Place '0' at current position
    for tail in binaries_with_weight_at_most(n - 1, c):
        res.append("0" + tail)

    # Place '1' if we still can
    if c > 0:
        for tail in binaries_with_weight_at_most(n - 1, c - 1):
            res.append("1" + tail)

    return res


# ---------- (Optional) quick sanity checks ----------

if __name__ == "__main__":
    assert my_len_recursive([1, 2, 3, 4]) == 4
    assert my_len_tail([1, 2, 3, 4]) == 4
    assert my_len_iter([1, 2, 3, 4]) == 4

    s = "Abacus & Umbrella"
    expected_vowels = 7
    assert count_vowels_recursive(s) == expected_vowels
    assert count_vowels_tail(s) == expected_vowels
    assert count_vowels_iter(s) == expected_vowels

    # Problem 3 example: n = 3 -> 5 strings
    n3 = sorted(binaries_no_consecutive_zeros(3))
    assert set(n3) == {"010", "011", "101", "110", "111"}

    # Problem 4 example: n = 3, c = 1 -> strings with <=1 ones
    n3c1 = sorted(binaries_with_weight_at_most(3, 1))
    assert set(n3c1) == {"000", "001", "010", "100"}
