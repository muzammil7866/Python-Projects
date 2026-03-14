class Stack:
    """
    A robust implementation of a Stack (Last-In, First-Out) data structure.
    """
    def __init__(self, initial_values=None):
        """
        Initializes the stack.
        
        Args:
            initial_values: An optional iterable to pre-populate the stack.
        """
        self._items = []
        if initial_values:
            for value in initial_values:
                self.push(value)

    def is_empty(self) -> bool:
        """Checks if the stack is empty."""
        return len(self._items) == 0

    def push(self, item):
        """Adds an item to the top of the stack."""
        self._items.append(item)

    def pop(self):
        """
        Removes and returns the item at the top of the stack.
        
        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """
        Returns the item at the top of the stack without removing it.
        
        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def size(self) -> int:
        """Returns the number of items in the stack."""
        return len(self._items)

    def __len__(self):
        return self.size()

    def __str__(self):
        """Returns a string representation of the stack."""
        return " -> ".join(map(str, self._items))

    def __iter__(self):
        """Iterates through the stack from top to bottom (LIFO order)."""
        for item in reversed(self._items):
            yield item

def main():
    print("--- Stack Implementation ---")
    try:
        # Initialize stack
        s = Stack(["2", "3", "4"])
        print(f"Initial Stack: {s}")
        
        # Push
        print("Pushing 5...")
        s.push("5")
        print(f"Stack after push: {s}")
        print(f"Top element (peek): {s.peek()}")
        
        # Pop
        print(f"Popping: {s.pop()}")
        print(f"Stack after pop: {s}")
        
        # Iteration
        print("Iterating through stack (Top to Bottom):")
        for item in s:
            print(f"- {item}")
            
        print(f"Final size: {len(s)}")

    except IndexError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
