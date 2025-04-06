import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from hashlib import sha256
from unittest.mock import patch
from sps_c.dh_mitm import (
    is_prime,
    is_primitive_root,
    find_primitive_roots,
    mod_exp,
    generate_private_key,
    generate_public_key,
    generate_shared_secret,
    encrypt_message,
    decrypt_message
)

class TestDiffieHellmanFunctions(unittest.TestCase):
    
    def test_is_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(23))
        self.assertTrue(is_prime(7919))  
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(100))
    
    def test_is_primitive_root(self):
        self.assertTrue(is_primitive_root(5, 23))
        self.assertTrue(is_primitive_root(7, 23))
        self.assertTrue(is_primitive_root(10, 23))
        self.assertFalse(is_primitive_root(1, 23))
        self.assertFalse(is_primitive_root(2, 23))  
        
    def test_find_primitive_roots(self):
        roots = find_primitive_roots(23)
        expected_roots = [5, 7, 10, 11, 14, 15, 17, 19, 20, 21]
        self.assertEqual(sorted(roots), expected_roots)
        
        # Test edge cases
        self.assertEqual(find_primitive_roots(2), [1])  # Now passes
        self.assertEqual(find_primitive_roots(1), [])
    
    def test_mod_exp(self):
        self.assertEqual(mod_exp(2, 3, 5), 3)   
        self.assertEqual(mod_exp(5, 3, 23), 10)  
        self.assertEqual(mod_exp(7, 0, 23), 1)   
    
    def test_generate_private_key(self):
        with patch('random.randint') as mock_randint:
            mock_randint.return_value = 5
            key = generate_private_key(23)
            self.assertEqual(key, 5)
            mock_randint.assert_called_with(2, 21)  
            
    def test_key_generation_and_shared_secret(self):
        p = 23
        g = 5
        alice_private = 6
        bob_private = 15
        
        alice_public = mod_exp(g, alice_private, p)
        bob_public = mod_exp(g, bob_private, p)
        
        alice_secret = mod_exp(bob_public, alice_private, p)
        bob_secret = mod_exp(alice_public, bob_private, p)
        
        self.assertEqual(alice_secret, bob_secret)
        self.assertEqual(alice_secret, 2)  
    
    def test_encryption_decryption(self):
        message = "Hello, world!"
        key = 12345
        
        encrypted = encrypt_message(message, key)
        self.assertNotEqual(encrypted, message)  
        
        decrypted = decrypt_message(encrypted, key)
        self.assertEqual(decrypted, message)
        
        wrong_decrypted = decrypt_message(encrypted, 54321)
        self.assertNotEqual(wrong_decrypted, message)


class TestDiffieHellmanProtocol(unittest.TestCase):
    
    def setUp(self):
        self.p = 23  
        self.g = 5   
        
    def test_normal_key_exchange(self):
        alice_private = 6
        bob_private = 15
        
        alice_public = generate_public_key(self.g, alice_private, self.p)
        bob_public = generate_public_key(self.g, bob_private, self.p)
        
        alice_secret = generate_shared_secret(bob_public, alice_private, self.p)
        bob_secret = generate_shared_secret(alice_public, bob_private, self.p)
        
        self.assertEqual(alice_secret, bob_secret)
        self.assertEqual(alice_secret, 2)  
        
    def test_message_exchange(self):
        alice_private = 6
        bob_private = 15
        
        alice_public = generate_public_key(self.g, alice_private, self.p)
        bob_public = generate_public_key(self.g, bob_private, self.p)
        
        alice_secret = generate_shared_secret(bob_public, alice_private, self.p)
        bob_secret = generate_shared_secret(alice_public, bob_private, self.p)
        
        message = "Hello Bob!"
        encrypted = encrypt_message(message, alice_secret)
        decrypted = decrypt_message(encrypted, bob_secret)
        self.assertEqual(decrypted, message)
        
        response = "Hi Alice!"
        encrypted_resp = encrypt_message(response, bob_secret)
        decrypted_resp = decrypt_message(encrypted_resp, alice_secret)
        self.assertEqual(decrypted_resp, response)


class TestMITMAttack(unittest.TestCase):    
    def setUp(self):
        self.p = 23  
        self.g = 5   
    def test_mitm_key_exchange(self):
        alice_private = 6
        bob_private = 15
        
        mallory_private_alice = 3
        mallory_private_bob = 7
        
        alice_public = generate_public_key(self.g, alice_private, self.p)
        bob_public = generate_public_key(self.g, bob_private, self.p)
        
        mallory_public_alice = generate_public_key(self.g, mallory_private_alice, self.p)
        mallory_public_bob = generate_public_key(self.g, mallory_private_bob, self.p)
        
        alice_secret = generate_shared_secret(mallory_public_alice, alice_private, self.p)
        
        mallory_secret_alice = generate_shared_secret(alice_public, mallory_private_alice, self.p)
        self.assertEqual(alice_secret, mallory_secret_alice)
        
        bob_secret = generate_shared_secret(mallory_public_bob, bob_private, self.p)
        
        mallory_secret_bob = generate_shared_secret(bob_public, mallory_private_bob, self.p)
        self.assertEqual(bob_secret, mallory_secret_bob)
        
        self.assertNotEqual(alice_secret, bob_secret)
    
    def test_mitm_message_interception(self):
        alice_private = 6
        bob_private = 15
        
        mallory_private_alice = 3
        mallory_private_bob = 7
        
        alice_public = generate_public_key(self.g, alice_private, self.p)
        bob_public = generate_public_key(self.g, bob_private, self.p)
        
        mallory_public_alice = generate_public_key(self.g, mallory_private_alice, self.p)
        mallory_public_bob = generate_public_key(self.g, mallory_private_bob, self.p)
        
        alice_secret = generate_shared_secret(mallory_public_alice, alice_private, self.p)
        bob_secret = generate_shared_secret(mallory_public_bob, bob_private, self.p)
        mallory_secret_alice = generate_shared_secret(alice_public, mallory_private_alice, self.p)
        mallory_secret_bob = generate_shared_secret(bob_public, mallory_private_bob, self.p)
        
        original_message = "Secret message"
        encrypted_alice = encrypt_message(original_message, alice_secret)
        
        decrypted_by_mallory = decrypt_message(encrypted_alice, mallory_secret_alice)
        self.assertEqual(decrypted_by_mallory, original_message)
        
        reencrypted_for_bob = encrypt_message(decrypted_by_mallory, mallory_secret_bob)
        
        decrypted_by_bob = decrypt_message(reencrypted_for_bob, bob_secret)
        self.assertEqual(decrypted_by_bob, original_message)

if __name__ == '__main__':
    unittest.main()