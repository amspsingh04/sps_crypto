from sps_c.rsa import generate_rkeys, rencrypt, rdecrypt

def simple_rsa_demo():
    print("Simple RSA Encryption Demo")
    print("=========================")
    
    # Step 1: Generate keys
    print("\n1. Generating RSA keys...")
    p = 61  # In real usage, use large primes (at least 1024 bits)
    q = 53
    public_key, private_key = generate_rkeys(p, q)
    print(f"Public Key (e, n): {public_key}")
    print(f"Private Key (d, n): {private_key}")

    # Step 2: Encrypt a message
    message = "Hello RSA!"
    print(f"\n2. Encrypting message: '{message}'")
    ciphertext = rencrypt(message, public_key)
    print(f"Ciphertext (as integer): {ciphertext}")

    # Step 3: Decrypt the message
    print("\n3. Decrypting ciphertext...")
    decrypted = rdecrypt(ciphertext, private_key)
    print(f"Decrypted message: '{decrypted}'")

    # Bonus: Show different output formats
    print("\nBonus: Different decryption formats:")
    print(f"As hex: {rdecrypt(ciphertext, private_key, 'hex')}")
    print(f"As integer: {rdecrypt(ciphertext, private_key, 'int')}")

if __name__ == "__main__":
    simple_rsa_demo()