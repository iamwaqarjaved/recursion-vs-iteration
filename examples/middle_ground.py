"""
middle_ground.py
Module 5 — Recursion vs. Iteration Decision Guide
Problems where BOTH approaches work — the choice is judgment.

Run:  python3 middle_ground.py
"""

import sys
from functools import lru_cache
from typing import List, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# 1. FIBONACCI  — three versions showing the tradeoff progression
# ─────────────────────────────────────────────────────────────────────────────

def fib_naive_recursive(n: int) -> int:
    """
    AVOID: exponential time O(2^n).  fib(40) does ~2 billion calls.
    Shown here only to illustrate why naive recursion fails for overlapping
    sub-problems.
    """
    if n <= 1:
        return n
    return fib_naive_recursive(n - 1) + fib_naive_recursive(n - 2)


@lru_cache(maxsize=None)
def fib_memoized(n: int) -> int:
    """
    GOOD recursive version with memoization.
    O(n) time, O(n) space (cache + call stack).
    Still hits recursion limit at n ≈ 1000.
    Judgment call: elegant, but the iterative version is just as readable.
    """
    if n <= 1:
        return n
    return fib_memoized(n - 1) + fib_memoized(n - 2)


def fib_iterative(n: int) -> int:
    """
    PREFERRED in production Python.
    O(n) time, O(1) space, no recursion limit.
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# ─────────────────────────────────────────────────────────────────────────────
# 2. FACTORIAL
# ─────────────────────────────────────────────────────────────────────────────

def factorial_recursive(n: int) -> int:
    """
    Classic textbook recursion.  Readable, mathematically direct.
    Fine for small n (Python integers are arbitrary precision).
    Hits RecursionError around n = 998 with default stack.
    """
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n: int) -> int:
    """
    Preferred for n > ~500.  O(1) stack, identical time complexity.
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# VERDICT: for factorial n < 500, either is fine — pick whichever your team
# finds clearer.  For n >= 500, use iterative or math.factorial.


# ─────────────────────────────────────────────────────────────────────────────
# 3. TOWER OF HANOI
# ─────────────────────────────────────────────────────────────────────────────
# The recursive solution is so clean it belongs in every CS course.
# The iterative solution exists (using an explicit stack) but is significantly
# harder to read and maintain — this is a case where recursion wins on
# expressiveness even though both are technically possible.

def hanoi_recursive(n: int, source: str, target: str, aux: str,
                    moves: List[Tuple[str, str]] = None) -> List[Tuple[str, str]]:
    """
    Base case:      n == 0  → no disks to move, return empty list
    Recursive case: move top n-1 to aux, move disk n to target, move n-1 to target
    Convergence:    each call decrements n by 1

    Produces the minimal 2^n − 1 moves.
    """
    if moves is None:
        moves = []
    if n == 0:                             # base case
        return moves
    hanoi_recursive(n - 1, source, aux, target, moves)   # move stack to aux
    moves.append((source, target))                        # move bottom disk
    hanoi_recursive(n - 1, aux, target, source, moves)   # move stack to target
    return moves


def hanoi_iterative(n: int, source: str, target: str, aux: str) -> List[Tuple[str, str]]:
    """
    Iterative version using an explicit call stack.
    Produces identical moves but is ~3× longer and harder to follow.
    Included to show what 'converting recursion to iteration' costs here.
    """
    moves   = []
    stack   = [(n, source, target, aux)]
    while stack:
        disks, src, tgt, tmp = stack.pop()
        if disks == 0:
            continue
        stack.append((disks - 1, tmp, tgt, src))
        stack.append((0, src, tgt, tmp))          # sentinel for the move
        stack.append((disks - 1, src, tmp, tgt))
        # unwind the sentinel
        while stack and stack[-1][0] == 0:
            _, s, t, _ = stack.pop()
            if s != t:                            # skip true base-case sentinels
                moves.append((s, t))
    return moves


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  MIDDLE GROUND — Problems Where Both Approaches Work")
    print("=" * 60)

    # Fibonacci
    print("\n── Fibonacci ──────────────────────────────────────────")
    for n in [10, 20, 30]:
        r = fib_memoized(n)
        i = fib_iterative(n)
        print(f"  fib({n:2d}): memoized={r}  iterative={i}  match={r==i}")

    print(f"\n  Naive recursive fib(35) (slow!):", end=" ", flush=True)
    print(fib_naive_recursive(35))

    print("\n  RecursionError demo:")
    sys.setrecursionlimit(50)              # artificially low to demo
    try:
        fib_memoized.cache_clear()
        fib_memoized(100)
    except RecursionError:
        print("    fib_memoized(100) with limit=50 → RecursionError ✗")
    sys.setrecursionlimit(1000)            # restore

    fib_memoized.cache_clear()
    print(f"  fib_iterative(100) with limit=50  → {fib_iterative(100)} ✓")
    sys.setrecursionlimit(1000)

    # Factorial
    print("\n── Factorial ──────────────────────────────────────────")
    for n in [5, 10, 20]:
        r = factorial_recursive(n)
        i = factorial_iterative(n)
        print(f"  {n}!  recursive={r}  iterative={i}  match={r==i}")

    # Tower of Hanoi
    print("\n── Tower of Hanoi ─────────────────────────────────────")
    for n in [2, 3, 4]:
        rec_moves = hanoi_recursive(n, "A", "C", "B")
        print(f"  hanoi({n}): {len(rec_moves)} moves (= 2^{n}−1 = {2**n-1})")
        if n <= 3:
            for m in rec_moves:
                print(f"    {m[0]} → {m[1]}")

    print()
    print("VERDICT SUMMARY")
    print("  Fibonacci: use iterative in production (no limit, O(1) space)")
    print("  Factorial: either works under n≈500; iterative for large n")
    print("  Hanoi:     recursive wins on expressiveness — keep it")
    print()
