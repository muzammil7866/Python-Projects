from utils import *
from logic import *

def solve_crime():
    print("\n--- First-Order Logic Crime Solver ---\n")

    # 1. Initialize the Knowledge Base
    # We use FolKB (First-Order Logic Knowledge Base) which is optimized for 
    # definite clauses (Horn clauses) and Forward Chaining.
    clauses = []

    print("Adding rules and facts to the Knowledge Base...")

    # --- Rule 1: The "Traitor" Rule ---
    # "It is a crime for an American to sell weapons to hostile nations"
    # Logic: American(x) AND Weapon(y) AND Sells(x,y,z) AND Hostile(z) -> Criminal(x)
    clauses.append(expr("(American(x) & Weapon(y) & Sells(x, y, z) & Hostile(z)) ==> Criminal(x)"))

    # --- Facts about the Scenario ---
    clauses.append(expr("Enemy(Nono, America)"))  # Nono is an enemy
    clauses.append(expr("Owns(Nono, M1)"))        # Nono owns M1
    clauses.append(expr("Missile(M1)"))           # M1 is a missile
    clauses.append(expr("American(West)"))        # West is American

    # --- Rule 2: The "Sales" Implication ---
    # "If Nono owns a missile, West must have sold it to them"
    clauses.append(expr("(Missile(x) & Owns(Nono, x)) ==> Sells(West, x, Nono)"))

    # --- Rule 3: Classification Rules ---
    # "Missiles are Weapons"
    clauses.append(expr("Missile(x) ==> Weapon(x)"))
    
    # "Enemies of America are Hostile"
    clauses.append(expr("Enemy(x, America) ==> Hostile(x)"))

    # --- Extra Robustness Clauses ---
    # "Rockets are Weapons" (Generic rule)
    clauses.append(expr("Rocket(x) ==> Weapon(x)"))

    # Complex Rule (Sanitized): 
    # "If American sells weapon to Nono and is identified, they are criminal"
    clauses.append(expr("(American(x) & Sells(x, y, Nono) & Weapon(y) & Identified(Government, x)) ==> Criminal(x)"))

    # 2. Load Clauses into KB
    crime_kb = FolKB(clauses)

    # 3. Query the Knowledge Base
    # We want to prove: Is West a Criminal?
    query = expr("Criminal(West)")
    print(f"\nQuerying: Is '{query}' true?")

    # [Explanation of fol_fc_ask]
    # This function performs Forward Chaining. It starts with known facts and 
    # triggers rules until it either derives the query or runs out of new facts.
    # It returns a GENERATOR of substitutions (assignments).
    
    # We convert to list to check if any proof was found.
    # [{}] means "Proven, with no variables needing substitution".
    # []   means "False / Not Proven".
    answer = list(fol_fc_ask(crime_kb, query))

    print(f"Result: {answer}")

    if len(answer) > 0:
        print("\n>> PROVEN: West is a Criminal.")
        # Triggering a diagram to visualize the inference steps
        # 
        print(">> Logic Chain:")
        print("   1. Enemy(Nono, America)        => Hostile(Nono)")
        print("   2. Missile(M1)                 => Weapon(M1)")
        print("   3. Missile(M1) + Owns(Nono,M1) => Sells(West, M1, Nono)")
        print("   4. American(West) + Weapon(M1) + Sells(...) + Hostile(Nono) => Criminal(West)")
    else:
        print(">> FAILED: Could not prove West is a Criminal.")

if __name__ == "__main__":
    solve_crime()