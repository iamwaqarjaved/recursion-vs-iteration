"""
iterative_examples.py
Module 5 — Recursion vs. Iteration Decision Guide
Five problems that are CLEARLY BETTER solved iteratively.

Run:  python3 iterative_examples.py
"""

from typing import List, Any, TypeVar, Optional
T = TypeVar("T")


# ─────────────────────────────────────────────────────────────────────────────
# 1. SUM A LIST
# ─────────────────────────────────────────────────────────────────────────────
# Why iterative? The data is flat — a plain sequence.  Iteration maps directly
# to "walk the sequence once."  The recursive version adds a call frame per
# element with zero conceptual benefit and crashes at ~1000 elements.

def sum_list_iterative(numbers: List[float]) -> float:
    """O(n) time, O(1) space.  Hits no recursion limit."""
    total = 0.0
    for n in numbers:
        total += n
    return total


def sum_list_recursive(numbers: List[float]) -> float:
    """Same answer, O(n) call stack.  Crashes if len(numbers) > ~1000."""
    if not numbers:
        return 0.0
    return numbers[0] + sum_list_recursive(numbers[1:])


# ─────────────────────────────────────────────────────────────────────────────
# 2. COUNT OCCURRENCES
# ─────────────────────────────────────────────────────────────────────────────
# Why iterative? Single linear scan over flat data — the textbook loop.

def count_occurrences_iterative(sequence: List[Any], target: Any) -> int:
    """O(n) time, O(1) space."""
    count = 0
    for item in sequence:
        if item == target:
            count += 1
    return count


def count_occurrences_recursive(sequence: List[Any], target: Any) -> int:
    """Correct but wastes stack frames and slices the list on each call O(n²) space."""
    if not sequence:
        return 0
    return (1 if sequence[0] == target else 0) + \
           count_occurrences_recursive(sequence[1:], target)


# ─────────────────────────────────────────────────────────────────────────────
# 3. FIND MAXIMUM
# ─────────────────────────────────────────────────────────────────────────────
# Why iterative? Classic running-maximum pattern — one variable, one loop.

def find_max_iterative(numbers: List[float]) -> float:
    """O(n) time, O(1) space."""
    if not numbers:
        raise ValueError("empty sequence")
    current_max = numbers[0]
    for n in numbers[1:]:
        if n > current_max:
            current_max = n
    return current_max


def find_max_recursive(numbers: List[float]) -> float:
    """Correct, O(n) stack.  The loop is clearer to every reader."""
    if len(numbers) == 1:
        return numbers[0]
    rest_max = find_max_recursive(numbers[1:])
    return numbers[0] if numbers[0] > rest_max else rest_max


# ─────────────────────────────────────────────────────────────────────────────
# 4. STRING REVERSAL
# ─────────────────────────────────────────────────────────────────────────────
# Why iterative? Python slicing (`s[::-1]`) is idiomatic and O(n) with no stack
# cost.  The recursive form creates O(n) string objects via concatenation.

def reverse_string_iterative(s: str) -> str:
    """One line, O(n) time, O(n) space for the result only."""
    return s[::-1]


def reverse_string_recursive(s: str) -> str:
    """O(n²) time due to repeated string concatenation; crashes on long strings."""
    if len(s) <= 1:
        return s
    return reverse_string_recursive(s[1:]) + s[0]


# ─────────────────────────────────────────────────────────────────────────────
# 5. LINEAR SEARCH
# ─────────────────────────────────────────────────────────────────────────────
# Why iterative? "Walk until found or exhausted" is the definition of a loop.
# Recursion adds no expressiveness here and burns stack space for no gain.

def linear_search_iterative(sequence: List[Any], target: Any) -> Optional[int]:
    """Returns index of first match or None.  O(n) time, O(1) space."""
    for i, item in enumerate(sequence):
        if item == target:
            return i
    return None


def linear_search_recursive(sequence: List[Any], target: Any,
                             index: int = 0) -> Optional[int]:
    """Same result with an O(n) call stack and an awkward index parameter."""
    if index >= len(sequence):
        return None
    if sequence[index] == target:
        return index
    return linear_search_recursive(sequence, target, index + 1)


# ─────────────────────────────────────────────────────────────────────────────
# DEMO — run both versions side-by-side to confirm identical results
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    print("=" * 60)
    print("  ITERATIVE EXAMPLES — 5 Naturally Iterative Problems")
    print("=" * 60)

    nums = [4.0, 7.5, 2.1, 9.8, 3.3]
    words = ["cat", "dog", "cat", "bird", "cat"]
    sentence = "recursion"

    print(f"\n1. Sum {nums}")
    print(f"   iterative: {sum_list_iterative(nums)}")
    print(f"   recursive: {sum_list_recursive(nums)}")

    print(f"\n2. Count 'cat' in {words}")
    print(f"   iterative: {count_occurrences_iterative(words, 'cat')}")
    print(f"   recursive: {count_occurrences_recursive(words, 'cat')}")

    print(f"\n3. Max of {nums}")
    print(f"   iterative: {find_max_iterative(nums)}")
    print(f"   recursive: {find_max_recursive(nums)}")

    print(f"\n4. Reverse '{sentence}'")
    print(f"   iterative: {reverse_string_iterative(sentence)}")
    print(f"   recursive: {reverse_string_recursive(sentence)}")

    data = [10, 23, 5, 42, 17, 8]
    print(f"\n5. Search 42 in {data}")
    print(f"   iterative: index {linear_search_iterative(data, 42)}")
    print(f"   recursive: index {linear_search_recursive(data, 42)}")

    # Demonstrate the limit: recursive sum crashes on large input
    print(f"\n--- Recursion limit demo ---")
    big = list(range(1500))
    print(f"   iterative sum(range(1500)) = {sum_list_iterative(big):,.0f}  ✓")
    try:
        sum_list_recursive(big)
    except RecursionError as e:
        print(f"   recursive sum(range(1500)) → RecursionError  ✗")
    print()
