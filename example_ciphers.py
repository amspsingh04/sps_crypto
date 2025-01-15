from sps_crypto.ciphers import Caesar, Vigenere, Hill, Playfair
import numpy as np

def main():
    # Caesar Cipher
    print("Caesar Cipher")
    caesar_plain = "HELLO WORLD"
    caesar_key = 3
    caesar_encrypted = Caesar(caesar_plain, mode='e', key=caesar_key)
    caesar_decrypted = Caesar(caesar_encrypted, mode='d', key=caesar_key)
    print(f"Plaintext: {caesar_plain}")
    print(f"Encrypted: {caesar_encrypted}")
    print(f"Decrypted: {caesar_decrypted}\n")

    # Vigenere Cipher
    print("Vigenere Cipher")
    vigenere_plain = "ATTACK AT DAWN"
    vigenere_key = "LEMON"
    vigenere_encrypted = Vigenere(vigenere_plain, mode='e', key=vigenere_key)
    vigenere_decrypted = Vigenere(vigenere_encrypted, mode='d', key=vigenere_key)
    print(f"Plaintext: {vigenere_plain}")
    print(f"Encrypted: {vigenere_encrypted}")
    print(f"Decrypted: {vigenere_decrypted}\n")

    # Hill Cipher
    print("Hill Cipher")
    hill_plain = "HELLO"
    hill_key = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
    hill_inverse_key = np.linalg.inv(hill_key).astype(int) % 26
    hill_encrypted = Hill.encrypt(hill_plain, hill_key)
    hill_decrypted = Hill.decrypt(hill_encrypted, hill_inverse_key)
    print(f"Plaintext: {hill_plain}")
    print(f"Encrypted: {hill_encrypted}")
    print(f"Decrypted: {hill_decrypted}\n")

    # Playfair Cipher
    print("Playfair Cipher")
    playfair_plain = "HIDETHEGOLDINTHETREESTUMP"
    playfair_key = "MONARCHY"
    playfair_encrypted = Playfair.process(playfair_plain, key=playfair_key, mode='e')
    playfair_decrypted = Playfair.process(playfair_encrypted, key=playfair_key, mode='d')
    print(f"Plaintext: {playfair_plain}")
    print(f"Encrypted: {playfair_encrypted}")
    print(f"Decrypted: {playfair_decrypted}\n")

if __name__ == "__main__":
    main()
