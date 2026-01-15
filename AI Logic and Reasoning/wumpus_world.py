from utils import *
from logic import *

def run_wumpus_world():
    print("\n--- Wumpus World Knowledge Base ---\n")

    # 1. Initialize Knowledge Base
    wumpus_kb = PropKB()

    # 2. Define Symbols (Percepts and locations)
    # B = Breeze, P = Pit, S = Stench, W = Wumpus, G = Glitter/Gold
    # Format: Lxy where L is type, x is col, y is row
    symbols_str = "B21, P31, B41, S12, B32, W13, B23, S23, G23, P33, B43, S14, B34, P44"
    
    # Create expressions from string
    percepts = expr(symbols_str)
    
    # If percepts is a single expression (tuple), unpack it, otherwise handle list
    if isinstance(percepts, tuple):
        percept_list = list(percepts)
    else:
        percept_list = [percepts]

    print("Populating KB with initial percepts...")
    
    # 3. Populate KB
    for p in percept_list:
        wumpus_kb.tell(p)
        print(f"Told KB: {p}")

    # 4. Query the KB
    # Note: With only atoms and no rules (like B21 <=> (P22 | P31...)), 
    # the inference is limited to what we explicitly told it.
    
    target_query = ~expr('P31') # Is there NO Pit at 3,1?
    
    print("\nQuerying Knowledge Base:")
    print(f"Asking: Is {target_query} true?")
    
    # Using pl_resolution to ask
    # We verify if the current KB entails the query
    result = wumpus_kb.ask_if_true(target_query)
    
    print(f"Result: {result}")
    
    if result:
        print(f"Interpretation: It is TRUE that {target_query}.")
    else:
        print(f"Interpretation: Cannot determine {target_query} (or it is False) based on current KB.")

    # Debug: Show Clauses
    print("\nCurrent KB Clauses:")
    for c in wumpus_kb.clauses:
        print(f" - {c}")

if __name__ == "__main__":
    run_wumpus_world()