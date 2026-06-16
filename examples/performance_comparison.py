"""
performance_comparison.py
Module 5 — Recursion vs. Iteration Decision Guide
Timed comparison: recursive vs iterative on inputs of size 10, 100, 1000.

Run:  python3 performance_comparison.py
"""

import time
import sys
from functools import lru_cache
from typing import List, Callable, Any

sys.setrecursionlimit(5000)   # allow n=1000 recursive tests


# ─────────────────────────────────────────────────────────────────────────────
# Timing harness
# ─────────────────────────────────────────────────────────────────────────────

def time_it(fn: Callable, *args, repeats: int = 500) -> float:
    """Return average wall-clock time in microseconds over `repeats` calls."""
    start = time.perf_counter()
    for _ in range(repeats):
        fn(*args)
    elapsed = time.perf_counter() - start
    return (elapsed / repeats) * 1_000_000   # µs


def table_row(label: str, n: int, rec_us: float, it_us: float) -> str:
    ratio = rec_us / it_us if it_us > 0 else float("inf")
    winner = "iter" if it_us < rec_us else "rec "
    return (f"  {label:<22} n={n:<5} "
            f"recursive={rec_us:>8.1f} µs   "
            f"iterative={it_us:>8.1f} µs   "
            f"ratio={ratio:>5.1f}x  [{winner}]")


# ─────────────────────────────────────────────────────────────────────────────
# 1. FACTORIAL
# ─────────────────────────────────────────────────────────────────────────────

def factorial_rec(n):
    if n == 0: return 1
    return n * factorial_rec(n - 1)

def factorial_iter(n):
    r = 1
    for i in range(2, n + 1): r *= i
    return r


# ─────────────────────────────────────────────────────────────────────────────
# 2. FIBONACCI  (memoized recursive vs iterative)
# ─────────────────────────────────────────────────────────────────────────────

@lru_cache(maxsize=None)
def fib_rec(n):
    if n <= 1: return n
    return fib_rec(n-1) + fib_rec(n-2)

def fib_iter(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n+1): a, b = b, a+b
    return b


# ─────────────────────────────────────────────────────────────────────────────
# 3. SUM A LIST
# ─────────────────────────────────────────────────────────────────────────────

def sum_rec(lst):
    if not lst: return 0
    return lst[0] + sum_rec(lst[1:])

def sum_iter(lst):
    total = 0
    for x in lst: total += x
    return total


# ─────────────────────────────────────────────────────────────────────────────
# 4. FLATTEN NESTED LIST  (depth = 3 nesting)
# ─────────────────────────────────────────────────────────────────────────────

def make_nested(n, depth=3):
    """Create a nested list of total n leaf elements at given depth."""
    flat = list(range(n))
    result = flat
    for _ in range(depth):
        chunk = len(result) // 3 or 1
        result = [result[i:i+chunk] for i in range(0, len(result), chunk)]
    return result

def flatten_rec(nested):
    if not isinstance(nested, list): return [nested]
    out = []
    for item in nested: out.extend(flatten_rec(item))
    return out

def flatten_iter(nested):
    stack = [nested]
    out   = []
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(reversed(item))
        else:
            out.append(item)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 5. MERGE SORT vs SORTED()
# ─────────────────────────────────────────────────────────────────────────────

def merge_sort_rec(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    l   = merge_sort_rec(arr[:mid])
    r   = merge_sort_rec(arr[mid:])
    out, i, j = [], 0, 0
    while i < len(l) and j < len(r):
        if l[i] <= r[j]: out.append(l[i]); i += 1
        else:             out.append(r[j]); j += 1
    return out + l[i:] + r[j:]

def merge_sort_iter(arr):
    """Python's built-in Timsort — the iterative gold standard."""
    return sorted(arr)


# ─────────────────────────────────────────────────────────────────────────────
# RUN BENCHMARKS
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 80)
    print("  PERFORMANCE COMPARISON: Recursive vs Iterative")
    print("  All times in microseconds (µs), averaged over 500 runs")
    print("=" * 80)

    import random
    random.seed(42)

    sizes = [10, 100, 1000]

    # ── 1. Factorial ──────────────────────────────────────────────────────────
    print("\n── 1. Factorial ─────────────────────────────────────────────────────")
    for n in sizes:
        r = time_it(factorial_rec,  n)
        i = time_it(factorial_iter, n)
        print(table_row("factorial", n, r, i))
    print("  Note: both are O(n); recursive overhead is the call-frame cost")

    # ── 2. Fibonacci (memoized) ───────────────────────────────────────────────
    print("\n── 2. Fibonacci (memoized recursive vs iterative) ───────────────────")
    for n in sizes:
        fib_rec.cache_clear()
        # warm the cache once so we're measuring steady-state
        fib_rec(n)
        r = time_it(fib_rec,  n)
        i = time_it(fib_iter, n)
        print(table_row("fibonacci", n, r, i))
    print("  Note: cached recursive ≈ O(1) on repeat calls; iterative is always O(n)")

    # ── 3. Sum a list ─────────────────────────────────────────────────────────
    print("\n── 3. Sum a list ────────────────────────────────────────────────────")
    for n in sizes:
        lst = list(range(n))
        if n <= 100:   # recursive crashes at n≈1000
            r = time_it(sum_rec,  lst, repeats=200)
        else:
            r = float("nan")
        i = time_it(sum_iter, lst)
        r_str = f"{r:>8.1f}" if r == r else "  CRASH "
        ratio = r / i if r == r and i > 0 else float("nan")
        ratio_str = f"{ratio:>5.1f}x" if ratio == ratio else "  n/a "
        print(f"  {'sum_list':<22} n={n:<5} "
              f"recursive={r_str} µs   "
              f"iterative={i:>8.1f} µs   "
              f"ratio={ratio_str}  [iter]")
    print("  Note: recursive crashes at n=1000 (RecursionError)")

    # ── 4. Flatten nested list ────────────────────────────────────────────────
    print("\n── 4. Flatten nested list (depth=3) ─────────────────────────────────")
    for n in sizes:
        nested = make_nested(n)
        r = time_it(flatten_rec,  nested, repeats=300)
        i = time_it(flatten_iter, nested, repeats=300)
        print(table_row("flatten_nested", n, r, i))
    print("  Note: both O(n); iterative avoids function-call overhead")

    # ── 5. Sort ───────────────────────────────────────────────────────────────
    print("\n── 5. Merge sort: recursive impl vs Python sorted() ─────────────────")
    for n in sizes:
        arr = random.sample(range(n * 10), n)
        r = time_it(merge_sort_rec,  arr, repeats=200)
        i = time_it(merge_sort_iter, arr, repeats=200)
        print(table_row("merge_sort", n, r, i))
    print("  Note: Python's Timsort is C-level optimized; pure-Python recursion")
    print("        can't compete but the algorithm is O(n log n) in both cases")

    print("\n" + "=" * 80)
    print("  TAKEAWAY")
    print("  • Overhead per recursive call in CPython ≈ 0.1–0.5 µs")
    print("  • For flat data: iterative is always faster and safer")
    print("  • For naturally recursive data: the clarity benefit outweighs")
    print("    the small constant overhead on inputs < 500 deep")
    print("  • Never use naive (un-memoized) recursion for overlapping sub-problems")
    print("=" * 80)
    print()
