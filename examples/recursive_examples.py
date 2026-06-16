"""
recursive_examples.py
Module 5 — Recursion vs. Iteration Decision Guide
Five problems that are CLEARLY BETTER solved recursively.

Run:  python3 recursive_examples.py
"""

# ─────────────────────────────────────────────────────────────────────────────
# 1. BINARY TREE TRAVERSAL (in-order)
# ─────────────────────────────────────────────────────────────────────────────
# Why recursive? The data IS a recursive structure — every node is the root of
# its own sub-tree.  The code mirrors the shape of the data perfectly.
# Iterative equivalent requires an explicit stack and is ~3× longer.

from dataclasses import dataclass, field
from typing import Optional, List, Any


@dataclass
class TreeNode:
    val: Any
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def inorder(node: Optional[TreeNode]) -> List[Any]:
    """
    Base case:      node is None  → return []
    Recursive case: traverse left sub-tree, visit root, traverse right sub-tree
    Convergence:    each call receives a strictly smaller sub-tree (height − 1)
    """
    if node is None:                        # base case
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)


def build_bst(values: List[int]) -> Optional[TreeNode]:
    """Helper: insert values into a BST."""
    root = None
    def insert(node, v):
        if node is None:
            return TreeNode(v)
        if v < node.val:
            node.left = insert(node.left, v)
        else:
            node.right = insert(node.right, v)
        return node
    for v in values:
        root = insert(root, v)
    return root


# ─────────────────────────────────────────────────────────────────────────────
# 2. DIRECTORY-TREE SIZE  (nested filesystem structure)
# ─────────────────────────────────────────────────────────────────────────────
# Why recursive? Directories are arbitrarily deep nested containers — identical
# to the tree case above but on the real filesystem.

import os


def directory_size(path: str) -> int:
    """
    Base case:      path is a file  → return its size in bytes
    Recursive case: path is a dir   → sum directory_size(child) for each child
    Convergence:    filesystem is finite; depth strictly increases to leaf files
    """
    if os.path.isfile(path):               # base case
        return os.path.getsize(path)
    total = 0
    try:
        for entry in os.scandir(path):
            total += directory_size(entry.path)
    except PermissionError:
        pass
    return total


# ─────────────────────────────────────────────────────────────────────────────
# 3. MERGE SORT  (divide-and-conquer)
# ─────────────────────────────────────────────────────────────────────────────
# Why recursive? The algorithm DEFINES itself in terms of smaller instances of
# itself.  "Sort a list" = "sort the left half, sort the right half, merge."
# The recursion is the algorithm — there is no natural iterative translation.

def merge_sort(arr: List[int]) -> List[int]:
    """
    Base case:      len(arr) <= 1  → already sorted, return as-is
    Recursive case: split in half, sort each half, merge sorted halves
    Convergence:    each call receives an array of length ⌊n/2⌋ → reaches 0
    """
    if len(arr) <= 1:                       # base case
        return arr
    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid])           # recursive call on left half
    right = merge_sort(arr[mid:])           # recursive call on right half
    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]


# ─────────────────────────────────────────────────────────────────────────────
# 4. FLATTEN ARBITRARILY NESTED LIST
# ─────────────────────────────────────────────────────────────────────────────
# Why recursive? The depth of nesting is unknown at write-time.  You cannot
# write a fixed number of nested loops to handle unknown depth — recursion is
# the only clean solution.

def flatten(nested: Any) -> List[Any]:
    """
    Base case:      item is not a list  → yield the item directly
    Recursive case: item is a list      → flatten each element inside
    Convergence:    each recursive call receives a strictly shorter/shallower list
    """
    if not isinstance(nested, list):        # base case
        return [nested]
    result = []
    for item in nested:
        result.extend(flatten(item))        # recursive call per element
    return result


# ─────────────────────────────────────────────────────────────────────────────
# 5. QUICK SELECT  (k-th smallest element, divide-and-conquer)
# ─────────────────────────────────────────────────────────────────────────────
# Why recursive? Like merge sort, the algorithm IS its own recurrence relation.
# "Find k-th in arr" = "partition around pivot; recurse only into the half that
# contains k."  Average O(n), and the recursive structure makes it obvious why.

def quick_select(arr: List[int], k: int) -> int:
    """
    Base case:      len(arr) == 1   → return arr[0]
    Recursive case: partition; recurse on sub-array that contains rank k
    Convergence:    each call receives an array strictly smaller than arr
    """
    if len(arr) == 1:                       # base case
        return arr[0]
    pivot  = arr[len(arr) // 2]
    lows   = [x for x in arr if x < pivot]
    highs  = [x for x in arr if x > pivot]
    pivots = [x for x in arr if x == pivot]
    if k < len(lows):
        return quick_select(lows, k)
    elif k < len(lows) + len(pivots):
        return pivot
    else:
        return quick_select(highs, k - len(lows) - len(pivots))


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  RECURSIVE EXAMPLES — 5 Naturally Recursive Problems")
    print("=" * 60)

    # 1. Binary tree traversal
    bst = build_bst([5, 3, 7, 1, 4, 6, 8])
    print(f"\n1. BST in-order traversal: {inorder(bst)}")

    # 2. Directory size (use current directory as demo)
    size = directory_size(".")
    print(f"2. Directory size ('.'): {size:,} bytes")

    # 3. Merge sort
    unsorted = [38, 27, 43, 3, 9, 82, 10]
    print(f"3. Merge sort {unsorted}")
    print(f"   → {merge_sort(unsorted)}")

    # 4. Flatten nested list
    nested = [1, [2, [3, [4]], 5], [6, 7]]
    print(f"4. Flatten {nested}")
    print(f"   → {flatten(nested)}")

    # 5. Quick select
    data = [7, 2, 10, 1, 4, 9, 3]
    k = 3
    print(f"5. Quick-select k={k} from {data}: {quick_select(data, k)}")
    print(f"   (verify: sorted = {sorted(data)}, index {k} = {sorted(data)[k]})")
    print()
