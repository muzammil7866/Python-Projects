# Microsoft Decypher Challenge

This project provides a robust implementation of the Caesar Cipher algorithm, inspired by the Microsoft Decypher Challenge.

## Features
- **Flexible Encryption/Decryption**: Supports any integer shift (positive for right shift, negative for left shift).
- **Case Preservation**: Correctly handles both uppercase and lowercase letters.
- **Robustness**: Non-alphabetical characters (like spaces, punctuation, or numbers) are preserved without modification.
- **Input Validation**: Gracefully handles invalid inputs for the shift count.

## Logic Overview
The core logic uses the ASCII values of characters and the modulo operator `% 26` to ensure that shifts always wrap around the alphabet (e.g., 'z' shifted by 1 becomes 'a').

## Usage
Run the script using Python:

```bash
python microsoft_cipher_challenge.py
```

Follow the prompts to enter a word and a shift value.
