# Changelog

All notable changes to this project will be documented here.

---

## [1.0.0] — 2026-06-16

### Added
- `README.md` — full GitHub tutorial with flowchart, all examples inline, benchmark results
- `RECURSION_VS_ITERATION_GUIDE.md` — complete 13-page engineering reference
- `examples/recursive_examples.py` — 5 naturally recursive problems (BST traversal, directory size, merge sort, flatten nested list, quick select)
- `examples/iterative_examples.py` — 5 naturally iterative problems (sum, count, max, reverse, search), each shown both ways
- `examples/middle_ground.py` — Fibonacci (3 versions), factorial, Tower of Hanoi with verdicts
- `examples/performance_comparison.py` — timed benchmarks at n=10, 100, 1000 across 5 problem types
- `examples/call_stack_and_tail_recursion.py` — CPython call-stack mechanics, TCO explanation, 3 practical strategies
- `LICENSE` — MIT
- `.gitignore` — Python + IDE + OS patterns
- `requirements.txt` — documents stdlib-only dependency
- `CHANGELOG.md` — this file
- `.github/workflows/ci.yml` — GitHub Actions: runs all examples on push
