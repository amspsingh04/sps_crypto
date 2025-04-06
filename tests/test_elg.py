import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from sps_c.elgamal import (
    is_eprime,
    generate_large_prime,
    find_eprimitive_root,
    prime_factors,
    generate_keys,
    encrypt,
    decrypt,
    text_to_int,
    int_to_text
)

class TestPrimeFunctions(unittest.TestCase):
    """Test prime number related functions"""
    
    def test_is_eprime(self):
        self.assertTrue(is_eprime(2))
        self.assertTrue(is_eprime(3))
        self.assertTrue(is_eprime(7919))  # Known prime
        self.assertFalse(is_eprime(1))
        self.assertFalse(is_eprime(4))
        self.assertFalse(is_eprime(100))
        
        # Test some larger primes
        self.assertTrue(is_eprime(32416190071))
        self.assertFalse(is_eprime(32416190072))
    
    def test_generate_large_prime(self):
        for bits in [8, 16, 32, 64]:
            p = generate_large_prime(bits)
            self.assertEqual(p.bit_length(), bits)
            self.assertTrue(is_eprime(p))
    
    def test_prime_factors(self):
        self.assertEqual(prime_factors(2), {2})
        self.assertEqual(prime_factors(10), {2, 5})
        self.assertEqual(prime_factors(17), {17})  # Prime
        self.assertEqual(prime_factors(36), {2, 3})
        self.assertEqual(prime_factors(101), {101})  # Prime

class TestPrimitiveRoot(unittest.TestCase):
    """Test primitive root finding"""
    
    def test_find_eprimitive_root(self):
        # Known primitive roots for small primes
        test_cases = [
            (2, 1),
            (3, 2),
            (5, 2),
            (7, 3),
            (11, 2),
            (13, 2),
            (17, 3),
            (19, 2),
            (23, 5)
        ]
        
        for p, expected_root in test_cases:
            root = find_eprimitive_root(p)
            self.assertEqual(root, expected_root)
    
    def test_primitive_root_properties(self):
        # Verify that found roots are indeed primitive roots
        for p in [5, 7, 11, 13, 17, 19, 23]:
            g = find_eprimitive_root(p)
            seen = set()
            for i in range(1, p):
                val = pow(g, i, p)
                self.assertNotIn(val, seen, f"{g} is not a primitive root mod {p}")
                seen.add(val)

class TestKeyGeneration(unittest.TestCase):
    """Test ElGamal key generation"""
    
    def test_key_generation(self):
        keys = generate_keys(64)  # Use smaller size for faster tests
        pub = keys['public']
        priv = keys['private']
        
        # Check public key components
        self.assertTrue(is_eprime(pub['p']))
        self.assertEqual(pub['p'], priv['p'])  # p should match
        
        # Verify g is a primitive root
        g = pub['g']
        p = pub['p']
        factors = prime_factors(p - 1)
        for f in factors:
            self.assertNotEqual(pow(g, (p - 1) // f, p), 1)
        
        # Verify y = g^x mod p
        self.assertEqual(pub['y'], pow(g, priv['x'], p))
        
        # Check private key is in valid range
        self.assertTrue(1 < priv['x'] < p - 1)

class TestEncryptionDecryption(unittest.TestCase):
    """Test encryption and decryption"""
    
    def setUp(self):
        self.keys = generate_keys(64)  # Smaller size for faster tests
        self.pub = self.keys['public']
        self.priv = self.keys['private']
    
    def test_encrypt_decrypt_small_numbers(self):
        # Test with small numbers directly
        test_messages = [1, 2, 5, 10, 100, 1000]
        for m in test_messages:
            if m >= self.pub['p']:
                continue  # Skip messages too large for current p
            
            ciphertext = encrypt(self.pub, m)
            decrypted = decrypt(self.priv, ciphertext)
            self.assertEqual(m, decrypted)
    
    def test_encrypt_decrypt_text(self):
        test_messages = [
            "Hello",
            "ElGamal",
            "Test message",
            "12345",
            "Special chars: !@#$%^&*()"
        ]
        
        for message in test_messages:
            m = text_to_int(message)
            if m >= self.pub['p']:
                continue  # Skip messages too large for current p
                
            ciphertext = encrypt(self.pub, m)
            decrypted = decrypt(self.priv, ciphertext)
            decrypted_text = int_to_text(decrypted)
            self.assertEqual(message, decrypted_text)
    
    def test_randomness_of_encryption(self):
        # Same message should encrypt to different ciphertexts
        m = text_to_int("Test")
        ciphertext1 = encrypt(self.pub, m)
        ciphertext2 = encrypt(self.pub, m)
        self.assertNotEqual(ciphertext1, ciphertext2)
    
    def test_invalid_message_range(self):
        # Message must be 1 <= m < p
        p = self.pub['p']
        with self.assertRaises(ValueError):
            encrypt(self.pub, 0)
        with self.assertRaises(ValueError):
            encrypt(self.pub, p)
        with self.assertRaises(ValueError):
            encrypt(self.pub, p + 1)

class TestTextConversion(unittest.TestCase):
    """Test text to integer conversion and back"""
    
    def test_text_conversion(self):
        test_strings = [
            "Hello",
            "Test",
            "12345",
            "Special chars: !@#$%^&*()",
            "Unicode: 😊🌍",
            ""
        ]
        
        for s in test_strings:
            num = text_to_int(s)
            converted = int_to_text(num)
            self.assertEqual(s, converted)
    
    def test_empty_string(self):
        self.assertEqual(int_to_text(text_to_int("")), "")

if __name__ == '__main__':
    unittest.main()