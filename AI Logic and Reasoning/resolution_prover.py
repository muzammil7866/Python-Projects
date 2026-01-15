from utils import *
from logic import *

def demonstrate_resolution():
    print("\n--- Propositional Logic Resolution Prover ---\n")

    # 1. Define Symbols
    P, Q, R, S = map(Symbol, ['P', 'Q', 'R', 'S'])

    # 2. Define the Sentence
    # Sentence: ((P or Q) and (not P or R) and (not R or S)) implies (Q and S)
    # We use the 'aima-python' syntax where logical operators are overloaded
    # and implication is checked.
    sentence = (P | Q) & (~P | R) & (~R | S) |'==>'| (Q & S)
    
    print(f"Original Sentence: {sentence}")
    
    # 3. Convert to CNF (Conjunctive Normal Form)
    cnf_sentence = to_cnf(sentence)
    print(f"CNF Form: {cnf_sentence}")

    # 4. Create Knowledge Base (KB)
    # We load the premises into the KB
    kb = PropKB()
    kb.tell(P | Q)      # Premise 1
    kb.tell(~P | R)     # Premise 2
    kb.tell(~R | S)     # Premise 3
    
    # To prove Q & S, we add the NEGATION of the conclusion to the KB
    # Negation of (Q & S) is (~Q | ~S) by De Morgan's Law
    kb.tell(~Q | ~S)    

    print("\n[Step 1] Manual Resolution Trace:")
    # Attempting to resolve clauses manually to find empty clause (Contradiction)
    try:
        # Resolve (~R | S) with (~Q | ~S) -> Eliminates S -> Result: ~R | ~Q
        r1 = pl_resolve(~R | S, ~Q | ~S)
        print(f"1. Resolved (~R | S) and (~Q | ~S) -> {r1[0]}")

        # Resolve Result 1 (~R | ~Q) with (P | Q) -> Eliminates Q -> Result: ~R | P
        r2 = pl_resolve(r1[0], P | Q)
        print(f"2. Resolved {r1[0]} and (P | Q)     -> {r2[0]}")

        # Resolve Result 2 (~R | P) with (~P | R) -> Eliminates P and R?
        # Note: Usually resolution removes one literal pair. 
        # Let's resolve (~R | P) with (~P | R). If we resolve on P, we get ~R | R (Tautology).
        # Let's look closely at your sequence.
        # Your previous code did: r3 = pl_resolve(r2[0], ~P | R)
        
        r3 = pl_resolve(r2[0], ~P | R) 
        # If r3 contains an empty clause or leads to True/False reduction
        print(f"3. Resolved {r2[0]} and (~P | R)    -> {r3}")

        # Check for empty clause
        # In aima-python, an empty set of clauses or False usually indicates contradiction found
        if not r3 or False in r3: 
            print(">> Empty clause derived! Contradiction found.")
            print(">> Therefore, the original statement is VALID.")
        else:
            print(">> No contradiction found yet in manual steps.")

    except Exception as e:
        print(f"Manual resolution error: {e}")

    # 5. Automated Check using AIMA's pl_resolution
    # This is the robust way to check entailment
    print("\n[Step 2] Automated Entailment Check:")
    
    # We rebuild a clean KB with just premises
    kb_check = PropKB()
    kb_check.tell(P | Q)
    kb_check.tell(~P | R)
    kb_check.tell(~R | S)
    
    query = Q & S
    is_valid = pl_resolution(kb_check, query)
    
    print(f"Query: Does KB entail ({query})?")
    print(f"Result: {is_valid}")
    
    if is_valid:
        print("Conclusion: The statement is VALID.")
    else:
        print("Conclusion: The statement is INVALID.")

if __name__ == "__main__":
    demonstrate_resolution()