# Stack Implementation (LIFO)

A clean and robust Python implementation of the Stack data structure, following the Last-In, First-Out (LIFO) principle.

## Features
- **Standard Stack Operations**: `push()`, `pop()`, `peek()`, and `is_empty()`.
- **Iteration Support**: Implements `__iter__` to support LIFO iteration (top to bottom).
- **String Representation**: Easy-to-read `__str__` method for debugging.
- **Robustness**: Proper error handling for edge cases, such as popping from an empty stack.

## Technical Details
The implementation uses a Python `list` as the underlying container, which provides amortized O(1) time complexity for both `append` (push) and `pop` operations at the end of the list.

## Usage
Run the demonstration script:

```bash
python stack_implementation.py
```
