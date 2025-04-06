from sps_c.elgamal import generate_keys, text_to_int, encrypt, decrypt, int_to_text

def main():
    print("ElGamal Encryption System")
    print("------------------------")
    
    print("Generating keys...")
    keys = generate_keys(256)
    public_key = keys['public']
    private_key = keys['private']
    
    print(f"Public Key (p, g, y): {public_key['p']}, {public_key['g']}, {public_key['y']}")
    print(f"Private Key (p, x): {private_key['p']}, {private_key['x']}")
    
    message = input("\nEnter a message to encrypt: ")
    message_int = text_to_int(message)
    
    print("\nEncrypting message...")
    ciphertext = encrypt(public_key, message_int)
    print(f"Ciphertext (c1, c2): {ciphertext}")
    
    print("\nDecrypting message...")
    decrypted_int = decrypt(private_key, ciphertext)
    decrypted_text = int_to_text(decrypted_int)
    print(f"Decrypted message: {decrypted_text}")
    
    if decrypted_text == message:
        print("\nSuccess! Original and decrypted messages match.")
    else:
        print("\nError! Decrypted message doesn't match original.")

if __name__ == "__main__":
    main()