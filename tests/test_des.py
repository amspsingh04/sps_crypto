# tests/test_des.py

import unittest
from des.DES import des_encrypt

class TestDESEncryption(unittest.TestCase):

    def test_hexadecimal_input(self):
        plaintext = "0123456789ABCDEF"
        key = "133457799BBCDFF1"
        expected_output = "85E813540F0AB405"  # Example expected output
        result = des_encrypt(plaintext, key)
        self.assertEqual(result, expected_output, "Hexadecimal input encryption failed")

    def test_string_input(self):
        plaintext = "Hello"  # Example plaintext
        key = "133457799BBCDFF1"
        result = des_encrypt(plaintext, key)
        self.assertTrue(isinstance(result, str), "String input should return a hex string")

    def test_invalid_key_length(self):
        plaintext = "Hello"
        key = "123"  # Invalid key length
        with self.assertRaises(ValueError):
            des_encrypt(plaintext, key)

    def test_empty_plaintext(self):
        plaintext = ""
        key = "133457799BBCDFF1"
        with self.assertRaises(ValueError):
            des_encrypt(plaintext, key)

    def test_special_characters_in_plaintext(self):
        plaintext = "@#$%^&*"
        key = "133457799BBCDFF1"
        result = des_encrypt(plaintext, key)
        self.assertTrue(isinstance(result, str), "Special character encryption failed")

if __name__ == "__main__":
    unittest.main()
