from sps_c.ds import CryptoUtils, RSADigitalSignature, ElGamalDigitalSignature


def demonstrate_rsa_digital_signature():
    print("\n=== RSA Digital Signature Demonstration ===")
    
    # Generate RSA keys
    print("\nGenerating RSA keys (1024-bit)...")
    public_key, private_key = RSADigitalSignature.generate_keys(1024)
    print(f"Public Key (e, n): ({public_key[0]}, ...{str(public_key[1])[-6:]})")
    print(f"Private Key (d, n): ({private_key[0]}, ...{str(private_key[1])[-6:]})")
    
    # Create a message to sign
    message = "This is a confidential message to be signed with RSA"
    print(f"\nOriginal Message: '{message}'")
    
    # Generate signature
    signature = RSADigitalSignature.sign(message, private_key)
    print(f"\nGenerated Signature: {signature}")
    
    # Verify signature
    is_valid = RSADigitalSignature.verify(message, signature, public_key)
    print(f"\nSignature Verification: {'VALID' if is_valid else 'INVALID'}")
    
    # Tamper with the message and verify again
    tampered_message = message + " (tampered)"
    is_valid_tampered = RSADigitalSignature.verify(tampered_message, signature, public_key)
    print(f"Verification after tampering: {'VALID' if is_valid_tampered else 'INVALID'} (expected: INVALID)")

def demonstrate_elgamal_digital_signature():
    """Demonstrate ElGamal digital signature generation and verification"""
    print("\n=== ElGamal Digital Signature Demonstration ===")
    
    # Generate ElGamal keys
    print("\nGenerating ElGamal keys (1024-bit)...")
    public_key, private_key = ElGamalDigitalSignature.generate_keys(1024)
    p, g, y = public_key
    print(f"Public Key (p, g, y): ({p}, {g}, ...{str(y)[-6:]})")
    print(f"Private Key (p, x): ({private_key[0]}, ...{str(private_key[1])[-6:]})")
    
    # Create a message to sign
    message = "This message will be signed with ElGamal"
    print(f"\nOriginal Message: '{message}'")
    
    # Generate signature
    signature = ElGamalDigitalSignature.sign(message, private_key)
    r, s = signature
    print(f"\nGenerated Signature (r, s): ({r}, {s})")
    
    # Verify signature
    is_valid = ElGamalDigitalSignature.verify(message, signature, public_key)
    print(f"\nSignature Verification: {'VALID' if is_valid else 'INVALID'}")
    
    # Tamper with the message and verify again
    tampered_message = message + " (modified)"
    is_valid_tampered = ElGamalDigitalSignature.verify(tampered_message, signature, public_key)
    print(f"Verification after tampering: {'VALID' if is_valid_tampered else 'INVALID'} (expected: INVALID)")

def demonstrate_crypto_utils():
    print("\n=== Cryptographic Utilities Demonstration ===")
    print("\nGenerating a 256-bit prime number...")
    prime = CryptoUtils.generate_large_prime(256)
    print(f"Generated Prime: {prime}")
    
    print(f"\nIs this number prime? {CryptoUtils.is_prime(prime)}")
    
    a = 17
    m = 3120
    try:
        inv = CryptoUtils.modinv(a, m)
        print(f"\nModular inverse of {a} mod {m} is {inv}")
        print(f"Verification: {a} * {inv} mod {m} = {(a * inv) % m} (should be 1)")
    except Exception as e:
        print(f"\nError computing inverse: {e}")
    
    message = "Hello, cryptographic world!"
    print(f"\nSHA-256 hash of '{message}':")
    hashed = CryptoUtils.hash_message(message)
    print(hashed)

def main():
    print("Digital Signature Demonstration Program")
    print("======================================")
    
    demonstrate_crypto_utils()
    
    demonstrate_rsa_digital_signature()
    
    demonstrate_elgamal_digital_signature()
    
    print("\nDemonstration complete!")

if __name__ == "__main__":
    main()