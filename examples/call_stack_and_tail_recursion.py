"""
call_stack_and_tail_recursion.py
Module 5 — Recursion vs. Iteration Decision Guide
Call-stack mechanics + tail recursion strategies for CPython.

Run:  python3 call_stack_and_tail_recursion.py
"""

import sys
import traceback
import threading


# ─────────────────────────────────────────────────────────────────────────────
# PART A — Call-stack mechanics
# ─────────────────────────────────────────────────────────────────────────────

def show_stack_depth(n: int, depth: int = 0) -> int:
    """
    Prints the call-stack depth at each level so you can SEE the stack growing.
    Each recursive call pushes a new frame until n == 0.
    """
    if n == 0:
        # At the deepest point, inspect the live stack
        frame = sys._getframe()
        live_depth = 0
        while frame:
            live_depth += 1
            frame = frame.f_back
        print(f"  Base case reached: {live_depth} frames on the Python call stack")
        return 0
    return 1 + show_stack_depth(n - 1, depth + 1)


def demonstrate_recursion_limit():
    """Show exactly what RecursionError looks like and when it fires."""
    print("Default recursion limit:", sys.getrecursionlimit())

    def count_down(n):
        if n == 0:
            return 0
        return 1 + count_down(n - 1)

    # Find the actual crash point
    for test_n in [500, 900, 950, 990, 995]:
        try:
            count_down(test_n)
            print(f"  count_down({test_n}) → OK")
        except RecursionError:
            print(f"  count_down({test_n}) → RecursionError  ← crashed here")
            break


def measure_frame_cost():
    """
    Measure how much memory one stack frame uses.
    Each CPython frame object ≈ 200–400 bytes of heap + ~8 bytes on the C stack.
    """
    import tracemalloc

    tracemalloc.start()

    def recurse(n):
        if n == 0:
            return tracemalloc.take_snapshot()
        return recurse(n - 1)

    depth   = 200
    snap    = recurse(depth)
    stats   = snap.statistics("lineno")
    total   = sum(s.size for s in stats)
    per_frame = total / depth

    tracemalloc.stop()
    print(f"  ~{per_frame:.0f} bytes allocated per recursive frame at depth {depth}")
    print(f"  → {depth * per_frame / 1024:.1f} KB total for {depth} frames")
    print(f"  → at limit (1000 frames): ~{1000 * per_frame / 1024:.0f} KB just for frames")


# ─────────────────────────────────────────────────────────────────────────────
# PART B — Tail recursion
# ─────────────────────────────────────────────────────────────────────────────
# A function is TAIL-RECURSIVE when the recursive call is the LAST operation —
# no work remains after the call returns.  Many languages (Scheme, Haskell,
# Scala, Kotlin) optimize this into a loop (Tail Call Optimization, TCO).
# CPython does NOT.  The call still pushes a frame.

def factorial_NOT_tail_recursive(n: int, acc: int = 1) -> int:
    """
    Looks tail-recursive but IS NOT: Python still builds the full call stack.
    The `acc` accumulator pattern is TCO-friendly in other languages, but
    CPython ignores it.
    """
    if n == 0:
        return acc
    return factorial_NOT_tail_recursive(n - 1, acc * n)   # CPython: still a frame


# The three strategies CPython developers actually use:

# ── Strategy 1: Rewrite as a plain loop ──────────────────────────────────────

def factorial_loop(n: int) -> int:
    """
    Simplest and fastest.  The mental model: replace the accumulator + tail call
    with a mutable accumulator + loop counter.
    """
    acc = 1
    while n > 1:
        acc *= n
        n -= 1
    return acc


# ── Strategy 2: Explicit stack (for non-tail, tree-shaped recursion) ──────────

def inorder_with_explicit_stack(root) -> list:
    """
    Convert tree traversal from recursive to iterative using an explicit stack.
    Use this when the recursion is NOT tail-recursive (binary trees, etc.)
    and the tree might be deeper than ~500 levels.
    """
    from dataclasses import dataclass
    from typing import Optional, Any

    @dataclass
    class Node:
        val: Any
        left: Optional["Node"] = None
        right: Optional["Node"] = None

    result = []
    stack  = []
    current = root

    while current or stack:
        # Go as far left as possible
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.val)
        current = current.right

    return result


# ── Strategy 3: sys.setrecursionlimit + threading (last resort) ──────────────

def deep_recursive_with_thread(n: int, target_fn) -> int:
    """
    For algorithms that genuinely need depth > 1000 and can't be easily
    rewritten: run in a new thread with a larger stack.
    Python threads have a larger C stack than the main thread on some platforms.
    This is a last resort — prefer rewriting the algorithm.
    """
    result = [None]
    error  = [None]

    def run():
        try:
            result[0] = target_fn(n)
        except Exception as e:
            error[0] = e

    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    t.join()

    if error[0]:
        raise error[0]
    return result[0]


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 65)
    print("  CALL STACK & TAIL RECURSION — CPython Mechanics")
    print("=" * 65)

    # A. Stack growth
    print("\n── A. Stack depth at recursion depth 10 ───────────────────")
    show_stack_depth(10)

    # B. Where the limit hits
    print("\n── B. Recursion limit ──────────────────────────────────────")
    demonstrate_recursion_limit()

    # C. Memory cost per frame
    print("\n── C. Memory per stack frame ───────────────────────────────")
    measure_frame_cost()

    # D. Tail call: CPython does NOT optimize
    print("\n── D. Tail recursion in CPython ────────────────────────────")
    print("  factorial_NOT_tail_recursive(10):", factorial_NOT_tail_recursive(10))
    print("  → This LOOKS like TCO but CPython still allocates a frame per call.")
    print("  → At n=997 it will raise RecursionError just like any other recursion.")

    # E. Strategy 1: loop
    print("\n── E. Strategy 1 — rewrite as loop ────────────────────────")
    print("  factorial_loop(10):", factorial_loop(10))
    import sys; sys.set_int_max_str_digits(0); print("  factorial_loop(5000): [result has", len(str(factorial_loop(5000))), "digits]")

    # F. Strategy 2: explicit stack
    print("\n── F. Strategy 2 — explicit stack for tree traversal ──────")
    from dataclasses import dataclass
    from typing import Optional, Any

    @dataclass
    class N:
        val: Any
        left: Optional["N"] = None
        right: Optional["N"] = None

    root = N(4, N(2, N(1), N(3)), N(6, N(5), N(7)))
    print("  in-order (explicit stack):", inorder_with_explicit_stack(root))

    # G. setrecursionlimit note
    print("\n── G. sys.setrecursionlimit — use with caution ─────────────")
    print(f"  Current limit: {sys.getrecursionlimit()}")
    print("  sys.setrecursionlimit(5000) is sometimes used but:")
    print("  • The C stack is fixed-size; setting it too high causes segfault")
    print("  • Each frame ≈ 200-400 bytes; 5000 frames ≈ 1-2 MB just for overhead")
    print("  • Prefer rewriting the algorithm over raising the limit")
    print()

    print("SUMMARY — What to do when recursion depth is a problem:")
    print("  1. Rewrite as iteration (while loop + accumulator)")
    print("  2. Use an explicit stack data structure (list as stack)")
    print("  3. Add memoization to cut repeated calls (overlapping sub-problems)")
    print("  4. Use sys.setrecursionlimit() as a temporary measure only")
    print("  5. Run in a thread with a larger stack (true last resort)")
    print()
