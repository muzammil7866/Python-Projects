def caesar_cipher(text: str, shift: int) -> str:
    """
    Encrypts or decrypts text using the Caesar Cipher algorithm.
    
    Args:
        text: The input string to be processed.
        shift: The number of positions to shift each character.
        
    Returns:
        The resulting string after applying the shift.
    """
    result = []
    
    # Normalize shift to be within 0-25
    shift %= 26
    
    for char in text:
        if char.isalpha():
            # Determine if uppercase or lowercase
            start = ord('A') if char.isupper() else ord('a')
            # Calculate the new character with wrapping
            new_char = chr(start + (ord(char) - start + shift) % 26)
            result.append(new_char)
        else:
            # Keep spaces and special characters as they are
            result.append(char)
            
    return "".join(result)

def main():
    print("--- Microsoft Decypher Challenge ---")
    try:
        word = input("ENTER THE WORD: ")
        shift_str = input("ENTER THE SHIFT COUNT: ")
        
        # Validate shift input
        if not shift_str.strip():
            print("Error: Shift count cannot be empty.")
            return
            
        shift = int(shift_str)
        
        processed_word = caesar_cipher(word, shift)
        print(f"Result: {processed_word}")
        
    except ValueError:
        print("Error: Shift count must be an integer.")
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

if __name__ == "__main__":
    main()
