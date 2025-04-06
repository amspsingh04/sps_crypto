import random
import hashlib
import unittest
from math import gcd

class CryptoUtils:
    """Utility functions for cryptographic operations"""
    
    @staticmethod
    def is_prime(n, k=5):
        """Miller-Rabin primality test"""
        if n <= 1:
            return False
        elif n <= 3:
            return True
        elif n % 2 == 0:
            return False
        
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

    @staticmethod
    def generate_large_prime(bits):
        """Generate a large prime number"""
        while True:
            p = random.getrandbits(bits)
            p |= (1 << bits - 1) | 1
            if CryptoUtils.is_prime(p):
                return p

    @staticmethod
    def extended_gcd(a, b):
        """Extended Euclidean algorithm"""
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = CryptoUtils.extended_gcd(b % a, a)
            return (g, x - (b // a) * y, y)

    @staticmethod
    def modinv(a, m):
        """Modular inverse using extended Euclidean algorithm"""
        g, x, y = CryptoUtils.extended_gcd(a, m)
        if g != 1:
            raise Exception('Modular inverse does not exist')
        return x % m

    @staticmethod
    def hash_message(message):
        """Hash a message using SHA-256 and return as integer"""
        return int.from_bytes(hashlib.sha256(message.encode()).digest(), byteorder='big')

class RSADigitalSignature:
    """RSA Digital Signature Implementation"""
    
    @staticmethod
    def generate_keys(bit_length=1024):
        """Generate RSA key pair"""
        p = CryptoUtils.generate_large_prime(bit_length // 2)
        q = CryptoUtils.generate_large_prime(bit_length // 2)
        
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # Choose e such that 1 < e < phi and gcd(e, phi) = 1
        e = 65537  # Common choice for e
        while gcd(e, phi) != 1:
            e = random.randint(2, phi - 1)
        
        d = CryptoUtils.modinv(e, phi)
        
        return (e, n), (d, n)  # (public, private)

    @staticmethod
    def sign(message, private_key):
        """Sign a message with private key"""
        d, n = private_key
        hashed = CryptoUtils.hash_message(message)
        # Ensure the hash is less than n
        hashed = hashed % n
        signature = pow(hashed, d, n)
        return signature

    @staticmethod
    def verify(message, signature, public_key):
        """Verify a signature with public key"""
        e, n = public_key
        hashed = CryptoUtils.hash_message(message) % n
        decrypted_hash = pow(signature, e, n)
        return hashed == decrypted_hash

class ElGamalDigitalSignature:
    """ElGamal Digital Signature Implementation"""
    
    @staticmethod
    def generate_keys(bit_length=1024):
        """Generate ElGamal key pair"""
        p = CryptoUtils.generate_large_prime(bit_length)
        
        # Find a generator (primitive root) of the multiplicative group modulo p
        # For testing purposes, we'll use a simplified approach
        # In production, use a proper primitive root finding algorithm
        def is_primitive_root(g, p):
            if gcd(g, p) != 1:
                return False
            order = p - 1
            factors = set()
            n = order
            i = 2
            while i * i <= n:
                if n % i == 0:
                    factors.add(i)
                    while n % i == 0:
                        n //= i
                i += 1
            if n > 1:
                factors.add(n)
            for factor in factors:
                if pow(g, order // factor, p) == 1:
                    return False
            return True
        
        g = 2
        while not is_primitive_root(g, p):
            g += 1
        
        x = random.randint(2, p - 2)  # Private key
        y = pow(g, x, p)              # Public key
        
        return (p, g, y), (p, x)  # (public, private)

    @staticmethod
    def sign(message, private_key):
        """Sign a message with private key"""
        p, x = private_key
        hashed = CryptoUtils.hash_message(message) % (p - 1)
        
        while True:
            k = random.randint(2, p - 2)
            if gcd(k, p - 1) == 1:
                break
                
        r = pow(p, k, p)
        s = (CryptoUtils.modinv(k, p - 1) * (hashed - x * r)) % (p - 1)
        return (r, s)

    @staticmethod
    def verify(message, signature, public_key):
        """Verify a signature with public key"""
        p, g, y = public_key
        r, s = signature
        
        if not (1 <= r < p):
            return False
            
        hashed = CryptoUtils.hash_message(message) % (p - 1)
        left = (pow(y, r, p) * pow(r, s, p)) % p
        right = pow(g, hashed, p)
        return left == right
