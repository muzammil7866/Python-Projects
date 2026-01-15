import sys
from utils import *
from logic import *

def generate_truth_table():
    """
    Generates and prints a truth table for standard logical connectives.
    """
    p = Symbol('p')
    q = Symbol('q')

    print("Truth Table Generator")
    print("-" * 75)
    # Header
    print(f"{'p':<6} | {'q':<6} | {'p or q':<10} | {'p and q':<10} | {'p => q':<10} | {'p <=> q':<10}")
    print("-" * 75)

    # Iterate through all truth values
    # Note: We iterate (False, True) to match standard truth table ordering
    for i in (False, True):
        for j in (False, True):
            # Logical Operations
            or_op = i | j
            and_op = i & j
            # Implication (i => j) is equivalent to (not i) or j
            implies_op = (not i) | j
            # Biconditional (i <=> j) is equivalent to not (i XOR j)
            iff_op = not (i ^ j)

            # Print row
            print(f"{str(i):<6} | {str(j):<6} | {str(or_op):<10} | {str(and_op):<10} | {str(implies_op):<10} | {str(iff_op):<10}")

if __name__ == "__main__":
    generate_truth_table()