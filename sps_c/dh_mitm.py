#dh_mitm.py
import random
from hashlib import sha256

def is_prime(n):
    """Check if a number n is a prime number"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def is_primitive_root(g, p):
    """Check if g is a primitive root modulo p"""
    if pow(g, p - 1, p) != 1:
        return False
    for k in range(1, p - 1):
        if (p - 1) % k == 0:
            if pow(g, k, p) == 1:
                return False
    return True

def find_primitive_roots(p):
    """Find all primitive roots modulo p"""
    if p == 2:
        return [1]  # Special case: 1 is a primitive root modulo 2
    
    if not is_prime(p):
        return []
        
    primitive_roots = []
    for g in range(1, p):
        if is_primitive_root(g, p):
            primitive_roots.append(g)
    return primitive_roots

def mod_exp(base, exponent, modulus):
    """Compute (base^exponent) % modulus using modular exponentiation"""
    return pow(base, exponent, modulus)

def generate_private_key(p):
    """Generate a random private key less than p"""
    return random.randint(2, p - 2)

def generate_public_key(g, private_key, p):
    """Generate public key using private key"""
    return mod_exp(g, private_key, p)

def generate_shared_secret(received_public_key, private_key, p):
    """Generate shared secret using received public key and own private key"""
    return mod_exp(received_public_key, private_key, p)

def encrypt_message(message, key):
    """Simple encryption using XOR with key hash (for demonstration only)"""
    key_hash = sha256(str(key).encode()).digest()
    encrypted = []
    for i, char in enumerate(message):
        encrypted_char = ord(char) ^ key_hash[i % len(key_hash)]
        encrypted.append(chr(encrypted_char))
    return ''.join(encrypted)

def decrypt_message(encrypted_message, key):
    """Simple decryption using XOR with key hash (for demonstration only)"""
    return encrypt_message(encrypted_message, key)  # XOR is symmetric

def alice(p, g, mallory_active=False):
    """Alice's part in the key exchange"""
    print("\n=== Alice ===")
    private_key = generate_private_key(p)
    print(f"Alice's private key: {private_key}")
    
    public_key = generate_public_key(g, private_key, p)
    print(f"Alice sends public key to Bob: {public_key}")
    
    # Mallory intercepts if active
    if mallory_active:
        print("Mallory intercepts Alice's public key!")
        received_public_key = yield public_key  # Mallory changes this
    else:
        received_public_key = yield public_key  # Bob receives directly
    
    print(f"Alice receives public key (from {'Mallory' if mallory_active else 'Bob'}): {received_public_key}")
    
    shared_secret = generate_shared_secret(received_public_key, private_key, p)
    print(f"Alice's computed shared secret: {shared_secret}")
    
    # Message exchange
    message = "Hello Bob, this is Alice!"
    encrypted = encrypt_message(message, shared_secret)
    print(f"Alice sends encrypted message: {encrypted[:50]}...")
    
    if mallory_active:
        # Mallory intercepts and decrypts
        mallory_secret_alice = yield encrypted
        decrypted_by_mallory = decrypt_message(encrypted, mallory_secret_alice)
        print(f"Mallory decrypts Alice's message: {decrypted_by_mallory}")
        
        # Mallory re-encrypts with Bob's key and forwards
        encrypted_for_bob = yield decrypted_by_mallory
    else:
        encrypted_for_bob = yield encrypted
    
    decrypted = decrypt_message(encrypted_for_bob, shared_secret)
    print(f"Alice receives and decrypts message: {decrypted}")

def bob(p, g, mallory_active=False):
    """Bob's part in the key exchange"""
    print("\n=== Bob ===")
    private_key = generate_private_key(p)
    print(f"Bob's private key: {private_key}")
    
    public_key = generate_public_key(g, private_key, p)
    print(f"Bob sends public key to Alice: {public_key}")
    
    # Mallory intercepts if active
    if mallory_active:
        print("Mallory intercepts Bob's public key!")
        received_public_key = yield public_key  # Mallory changes this
    else:
        received_public_key = yield public_key  # Alice receives directly
    
    print(f"Bob receives public key (from {'Mallory' if mallory_active else 'Alice'}): {received_public_key}")
    
    shared_secret = generate_shared_secret(received_public_key, private_key, p)
    print(f"Bob's computed shared secret: {shared_secret}")
    
    # Message exchange
    if mallory_active:
        encrypted_from_alice = yield
        # This is actually from Mallory, re-encrypted
    else:
        encrypted_from_alice = yield
    
    decrypted = decrypt_message(encrypted_from_alice, shared_secret)
    print(f"Bob receives and decrypts message: {decrypted}")
    
    response = f"Hi Alice, this is Bob! I received: {decrypted[-10:]}..."
    encrypted_response = encrypt_message(response, shared_secret)
    print(f"Bob sends encrypted response: {encrypted_response[:50]}...")
    
    if mallory_active:
        # Mallory intercepts and decrypts
        mallory_secret_bob = yield encrypted_response
        decrypted_by_mallory = decrypt_message(encrypted_response, mallory_secret_bob)
        print(f"Mallory decrypts Bob's message: {decrypted_by_mallory}")
        
        # Mallory re-encrypts with Alice's key and forwards
        encrypted_for_alice = yield decrypted_by_mallory
    else:
        encrypted_for_alice = yield encrypted_response
    
    yield encrypted_for_alice

def mallory(p, g):
    """Mallory's man-in-the-middle attack"""
    print("\n=== Mallory the Attacker ===")
    
    # Generate keys to use with Alice and Bob
    private_key_for_alice = generate_private_key(p)
    private_key_for_bob = generate_private_key(p)
    
    print(f"Mallory's private key for Alice: {private_key_for_alice}")
    print(f"Mallory's private key for Bob: {private_key_for_bob}")
    
    # Get Alice's public key (intercepted)
    alice_public_key = yield
    print(f"Mallory intercepts Alice's real public key: {alice_public_key}")
    
    # Compute Mallory's public key to send to Bob
    mallory_public_key_for_bob = generate_public_key(g, private_key_for_bob, p)
    print(f"Mallory sends fake public key to Bob: {mallory_public_key_for_bob}")
    
    # Get Bob's public key (intercepted)
    bob_public_key = yield mallory_public_key_for_bob
    print(f"Mallory intercepts Bob's real public key: {bob_public_key}")
    
    # Compute Mallory's public key to send to Alice
    mallory_public_key_for_alice = generate_public_key(g, private_key_for_alice, p)
    print(f"Mallory sends fake public key to Alice: {mallory_public_key_for_alice}")
    
    # Compute shared secrets
    mallory_secret_with_alice = generate_shared_secret(alice_public_key, private_key_for_alice, p)
    mallory_secret_with_bob = generate_shared_secret(bob_public_key, private_key_for_bob, p)
    
    print(f"Mallory's shared secret with Alice: {mallory_secret_with_alice}")
    print(f"Mallory's shared secret with Bob: {mallory_secret_with_bob}")
    
    # Now intercept messages between Alice and Bob
    
    # Get Alice's encrypted message
    alice_encrypted = yield mallory_public_key_for_alice
    print("\nMallory intercepting Alice's message to Bob...")
    
    # Decrypt Alice's message using Mallory-Alice secret
    decrypted_from_alice = decrypt_message(alice_encrypted, mallory_secret_with_alice)
    print(f"Mallory decrypts Alice's message: {decrypted_from_alice}")
    
    # Re-encrypt with Mallory-Bob secret and send to Bob
    encrypted_for_bob = encrypt_message(decrypted_from_alice, mallory_secret_with_bob)
    print(f"Mallory re-encrypts and forwards to Bob: {encrypted_for_bob[:50]}...")
    
    # Get Bob's response
    bob_encrypted = yield encrypted_for_bob
    print("\nMallory intercepting Bob's response to Alice...")
    
    # Decrypt Bob's message using Mallory-Bob secret
    decrypted_from_bob = decrypt_message(bob_encrypted, mallory_secret_with_bob)
    print(f"Mallory decrypts Bob's message: {decrypted_from_bob}")
    
    # Re-encrypt with Mallory-Alice secret and send to Alice
    encrypted_for_alice = encrypt_message(decrypted_from_bob, mallory_secret_with_alice)
    print(f"Mallory re-encrypts and forwards to Alice: {encrypted_for_alice[:50]}...")
    
    yield encrypted_for_alice

def simulate_normal_exchange(p, g):
    """Simulate a normal Diffie-Hellman key exchange without attack"""
    print("\n=== Simulating NORMAL Diffie-Hellman Key Exchange ===")
    
    # Initialize Alice and Bob
    alice_gen = alice(p, g)
    bob_gen = bob(p, g)
    
    # Alice sends her public key to Bob
    alice_public_key = next(alice_gen)
    bob_received = bob_gen.send(alice_public_key)
    
    # Bob sends his public key to Alice
    bob_public_key = next(bob_gen)
    alice_received = alice_gen.send(bob_public_key)
    
    # Alice sends encrypted message to Bob
    alice_message = next(alice_gen)
    bob_received_message = bob_gen.send(alice_message)
    
    # Bob sends response to Alice
    bob_response = next(bob_gen)
    alice_gen.send(bob_response)

def simulate_mitm_attack(p, g):
    """Simulate a man-in-the-middle attack on Diffie-Hellman"""
    print("\n=== Simulating MAN-IN-THE-MIDDLE ATTACK ===")
    
    # Initialize Alice, Bob, and Mallory
    alice_gen = alice(p, g, mallory_active=True)
    bob_gen = bob(p, g, mallory_active=True)
    mallory_gen = mallory(p, g)
    
    # Start Mallory
    next(mallory_gen)
    
    # Alice sends her public key (intercepted by Mallory)
    alice_public_key = next(alice_gen)
    mallory_to_bob = mallory_gen.send(alice_public_key)
    
    # Mallory sends fake key to Bob
    bob_received = bob_gen.send(mallory_to_bob)
    
    # Bob sends his public key (intercepted by Mallory)
    bob_public_key = next(bob_gen)
    mallory_to_alice = mallory_gen.send(bob_public_key)
    
    # Mallory sends fake key to Alice
    alice_received = alice_gen.send(mallory_to_alice)
    
    # Alice sends message (intercepted by Mallory)
    alice_message = next(alice_gen)
    mallory_to_bob_msg = mallory_gen.send(alice_message)
    
    # Mallory forwards modified message to Bob
    bob_received_msg = bob_gen.send(mallory_to_bob_msg)
    
    # Bob sends response (intercepted by Mallory)
    bob_response = next(bob_gen)
    mallory_to_alice_msg = mallory_gen.send(bob_response)
    
    # Mallory forwards modified response to Alice
    alice_gen.send(mallory_to_alice_msg)

