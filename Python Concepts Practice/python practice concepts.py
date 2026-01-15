"""
Python Practice Concepts
------------------------
This script demonstrates various Python programming concepts including:
1. Generators
2. List Comprehensions
3. Functional Programming (Map, Filter)
4. OOP Access Modifiers (Public, Protected, Private)
5. Variable-length Arguments (*args)
6. Closures and Nested Functions
"""

# ---------------------------------------------------------
# 1. Generators
# Generators are a simple way to create iterators using 'yield'.
# ---------------------------------------------------------
def count_to_three_generator():
    """Simple generator that yields numbers 0, 1, 2."""
    for i in range(3):
        yield i

def demo_generators():
    print("\n--- 1. Generators Demo ---")
    gen = count_to_three_generator()
    try:
        print(f"First: {next(gen)}")
        print(f"Second: {next(gen)}")
        print(f"Third: {next(gen)}")
        # next(gen)  # This would raise StopIteration
    except StopIteration:
        print("Generator exhausted.")

# ---------------------------------------------------------
# 2. List Comprehensions
# A concise way to create lists.
# ---------------------------------------------------------
def demo_list_comprehensions():
    print("\n--- 2. List Comprehensions Demo ---")
    # Basic list comprehension
    squares = [x**2 for x in range(5)]
    print(f"Squares: {squares}")
    
    # Conditional list comprehension
    even_squares = [x**2 for x in range(10) if x % 2 == 0]
    print(f"Even Squares: {even_squares}")

# ---------------------------------------------------------
# 3. Functional Programming: Map & Filter
# Higher-order functions that take a function and an iterable.
# ---------------------------------------------------------
def demo_functional():
    print("\n--- 3. Functional Programming Demo ---")
    numbers = [1, 2, 3, 4, 5, 6]
    
    # Map: Apply function to every element
    squared = map(lambda x: x**2, [1, 2, 3, 4])
    print(f"Mapped Squares: {list(squared)}")
    
    # Filter: Keep elements that satisfy a condition
    even = filter(lambda x: x % 2 == 0, numbers)
    print(f"Filtered Evens: {list(even)}")

# ---------------------------------------------------------
# 4. OOP Access Modifiers
# Demonstrating Public, Protected, and Private members.
# ---------------------------------------------------------
class AccessDemo:
    def __init__(self):
        self.public_var = "Public: Accessible everywhere"
        self._protected_var = "Protected: Use with caution (internal use)"
        self.__private_var = "Private: Name mangled, use getter"

    def get_private(self):
        """Getter for private variable."""
        return self.__private_var

def demo_oop():
    print("\n--- 4. OOP Access Modifiers Demo ---")
    obj = AccessDemo()
    print(f"Public: {obj.public_var}")
    print(f"Protected: {obj._protected_var}")
    print(f"Private (via getter): {obj.get_private()}")
    # print(obj.__private_var)  # This would fail with AttributeError

# ---------------------------------------------------------
# 5. Variable-length Arguments (*args)
# Allows passing any number of positional arguments.
# ---------------------------------------------------------
def flexible_sum(*args):
    """Calculates the sum of any number of inputs."""
    return sum(args)

def demo_args():
    print("\n--- 5. Variable Arguments (*args) Demo ---")
    total = flexible_sum(1, 2, 3, 4, 10, 20)
    print(f"Sum of (1, 2, 3, 4, 10, 20): {total}")

# ---------------------------------------------------------
# 6. Closures and Nested Functions
# A nested function that remembers the state of its outer scope.
# ---------------------------------------------------------
def outer_adder(x):
    """Creates a closure that adds 'x' to its input."""
    def inner_adder(y):
        return x + y
    return inner_adder

def demo_closures():
    print("\n--- 6. Closures Demo ---")
    add_five = outer_adder(5)
    print(f"5 + 3 = {add_five(3)}")
    print(f"5 + 10 = {add_five(10)}")

# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    demo_generators()
    demo_list_comprehensions()
    demo_functional()
    demo_oop()
    demo_args()
    demo_closures()
