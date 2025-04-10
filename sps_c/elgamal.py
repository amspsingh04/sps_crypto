#elgamal.py
import random
import sys
from math import gcd

def is_eprime(n, k=5):
    """Miller-Rabin primality test"""
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False
    
    # Write n as d*2^s + 1
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime(bits):
    """Generate a large prime number with specified bits"""
    while True:
        p = random.getrandbits(bits)
        # Ensure it's odd and has the right bit length
        p |= (1 << bits - 1) | 1
        if is_eprime(p):
            return p

def find_eprimitive_root(p):
    """Find a primitive root modulo p"""
    if p == 2:
        return 1
    
    # Factorize p-1
    factors = prime_factors(p - 1)
    
    # Test potential primitive roots
    for g in range(2, p):
        if all(pow(g, (p - 1) // f, p) != 1 for f in factors):
            return g
    return None

def prime_factors(n):
    """Return the set of prime factors of n"""
    factors = set()
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.add(i)
            n //= i
        i += 2
    if n > 2:
        factors.add(n)
    return factors

def generate_keys(bits=256):
    """Generate ElGamal public and private keys"""
    p = generate_large_prime(bits)
    g = find_eprimitive_root(p)
    
    if g is None:
        raise ValueError("Failed to find primitive root for p")
    
    x = random.randint(2, p - 2)  # Private key
    y = pow(g, x, p)              # Public key
    
    return {
        'public': {'p': p, 'g': g, 'y': y},
        'private': {'p': p, 'x': x}
    }

def encrypt(public_key, message):
    """Encrypt a message using ElGamal"""
    p, g, y = public_key['p'], public_key['g'], public_key['y']
    
    if not (1 <= message < p):
        raise ValueError("Message must be in range [1, p-1]")
    
    k = random.randint(2, p - 2)
    while gcd(k, p - 1) != 1:
        k = random.randint(2, p - 2)
    
    c1 = pow(g, k, p)
    c2 = (message * pow(y, k, p)) % p
    
    return (c1, c2)

def decrypt(private_key, ciphertext):
    """Decrypt a ciphertext using ElGamal"""
    p, x = private_key['p'], private_key['x']
    c1, c2 = ciphertext
    
    s = pow(c1, x, p)
    s_inv = pow(s, p - 2, p)  # Fermat's little theorem for modular inverse
    message = (c2 * s_inv) % p
    
    return message

def text_to_int(text, max_bits=256):
    """Convert text to integer representation"""
    return int.from_bytes(text.encode('utf-8'), 'big')

def int_to_text(number):
    """Convert integer back to text"""
    return number.to_bytes((number.bit_length() + 7) // 8, 'big').decode('utf-8')
'''

'''