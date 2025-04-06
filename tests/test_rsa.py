import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sps_c.rsa import generate_rkeys, rencrypt, rdecrypt

class TestRSA(unittest.TestCase):
    def setUp(self):
        self.public_key, self.private_key = generate_rkeys(61, 53)  # n = 3233

    def test_rencrypt_rdecrypt_int(self):
        original = 42
        rencrypted = rencrypt(original, self.public_key)
        rdecrypted = rdecrypt(rencrypted, self.private_key, 'int')
        self.assertEqual(rdecrypted, original)

    def test_rencrypt_rdecrypt_hex(self):
        original = "0x2A"
        rencrypted = rencrypt(original, self.public_key)
        rdecrypted = rdecrypt(rencrypted, self.private_key, 'int')
        self.assertEqual(rdecrypted, 42)

    def test_rencrypt_rdecrypt_text(self):
        original = "A"  
        rencrypted = rencrypt(original, self.public_key)
        rdecrypted = rdecrypt(rencrypted, self.private_key, 'text')
        self.assertEqual(rdecrypted, original)

    def test_encoding_failure(self):
        rencrypted = rencrypt(2047, self.public_key)
        result = rdecrypt(rencrypted, self.private_key, 'text')
        self.assertTrue(result.startswith("<Failed to decode"))

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            rencrypt("Hello, world!", self.public_key)

if __name__ == "__main__":
    unittest.main()
