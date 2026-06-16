# Contributing

Contributions that improve clarity, add examples, or extend the benchmark suite are welcome.

## How to contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-idea`
3. Make your changes
4. Test: `python3 examples/your_file.py` — confirm clean output
5. Commit: `git commit -m "feat: describe your addition"`
6. Push: `git push origin feature/your-idea`
7. Open a Pull Request against `main`

## Code style

- Python 3.10+, standard library only (no third-party imports)
- Every recursive function **must** include the 3-line comment block:
  ```python
  # Base case:      <what stops the recursion>
  # Recursive case: <what this call does>
  # Convergence:    <why parameter moves toward base case>
  ```
- Keep lines under 100 characters
- Files are standalone — each must run with `python3 filename.py` without imports from siblings

## Ideas for extensions

- Sierpiński triangle / Koch snowflake (visual recursion)
- N-queens or Sudoku solver (backtracking)
- Graph DFS recursive vs BFS iterative
- Trampoline pattern as TCO alternative
- PyPy vs CPython benchmarks
- Type-annotated versions using `typing` or PEP 695 syntax
