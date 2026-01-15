def factorial_iterative(n: int) -> int:
    """Calculates factorial using an iterative approach."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def factorial_recursive(n: int) -> int:
    """Calculates factorial using a recursive approach."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n == 0 or n == 1:
        return 1
    return n * factorial_recursive(n - 1)

def main():
    print("--- Factorial Calculator ---")
    try:
        user_input = input("Enter a non-negative integer: ")
        if not user_input.strip():
            print("Error: Input cannot be empty.")
            return
            
        n = int(user_input)
        
        # Demonstrating iterative method
        iter_result = factorial_iterative(n)
        print(f"Iterative Result: {iter_result}")
        
        # Demonstrating recursive method
        recur_result = factorial_recursive(n)
        print(f"Recursive Result: {recur_result}")
        
    except ValueError as e:
        print(f"Error: {e}")
    except RecursionError:
        print("Error: Number too large for recursive calculation.")
    except KeyboardInterrupt:
        print("\nProgram terminated.")

if __name__ == "__main__":
    main()
