import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sps_c.S_DES import sdes_encrypt, sdes_decrypt

class TestSDES(unittest.TestCase):
    def test_given_example(self):
        plaintext = "00101000"
        key = "1100011110"
        expected_ciphertext = "10001010"
        self.assertEqual(sdes_encrypt(plaintext, key), expected_ciphertext)
        self.assertEqual(sdes_decrypt(expected_ciphertext, key), plaintext)

    def test_full_cycle_encryption_decryption(self):
        key = "1010101010"
        for p in range(256):  # Test all 8-bit plaintexts
            plaintext = format(p, '08b')
            encrypted = sdes_encrypt(plaintext, key)
            decrypted = sdes_decrypt(encrypted, key)
            self.assertEqual(decrypted, plaintext)

    def test_all_zero_plaintext(self):
        plaintext = "00000000"
        key = "1010101010"
        encrypted = sdes_encrypt(plaintext, key)
        decrypted = sdes_decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)

    def test_all_one_plaintext(self):
        plaintext = "11111111"
        key = "1010101010"
        encrypted = sdes_encrypt(plaintext, key)
        decrypted = sdes_decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)

    def test_all_zero_key(self):
        plaintext = "10101010"
        key = "0000000000"
        encrypted = sdes_encrypt(plaintext, key)
        decrypted = sdes_decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)

    def test_all_one_key(self):
        plaintext = "10101010"
        key = "1111111111"
        encrypted = sdes_encrypt(plaintext, key)
        decrypted = sdes_decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)

    def test_invalid_plaintext_length(self):
        key = "1010101010"
        with self.assertRaises(ValueError):
            sdes_encrypt("1010", key)

    def test_invalid_key_length(self):
        plaintext = "10101010"
        with self.assertRaises(ValueError):
            sdes_encrypt(plaintext, "1111")

if __name__ == '__main__':
    unittest.main()
