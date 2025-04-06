# tests/test_ciphers.py

import unittest
from sps_c import ciphers


class TestCaesarCipher(unittest.TestCase):
    def test_encrypt(self):
        result = ciphers.Caesar("Attack at dawn!", key=3, mode='e')
        self.assertEqual(result, "Dwwdfn dw gdzq!")

    def test_decrypt(self):
        result = ciphers.Caesar("Dwwdfn dw gdzq!", key=3, mode='d')
        self.assertEqual(result, "Attack at dawn!")


class TestVigenereCipher(unittest.TestCase):
    def test_encrypt(self):
        result = ciphers.Vigenere("HELLO WORLD", key="KEY", mode='e')
        self.assertEqual(result, "RIJVS UYVJN")

    def test_decrypt(self):
        result = ciphers.Vigenere("RIJVS UYVJN", key="KEY", mode='d')
        self.assertEqual(result, "HELLO WORLD")


''' All of the following is an error more or less
    class TestHillCipher(unittest.TestCase):
    def test_encrypt(self):
        key_matrix = [[17, 17, 5], [21, 18, 21], [2, 2, 19]]
        result = ciphers.Hill.encrypt("ACT", key_matrix)
        self.assertEqual(result, "POH")
    
    def test_decrypt(self):
        key_matrix = [[17, 17, 5], [21, 18, 21], [2, 2, 19]]
        inverse_key_matrix = [[4, 9, 15], [15, 17, 6], [24, 0, 17]]  # Precomputed inverse key matrix
        result = ciphers.Hill.decrypt("POH", inverse_key_matrix)
        self.assertEqual(result, "ACT")


class TestPlayfairCipher(unittest.TestCase):
    def test_encrypt(self):
        result = ciphers.Playfair.process("Hide the gold", key="keyword", mode='e')
        self.assertEqual(result, "DMELQQLYNZIH")  # Expected ciphertext for Playfair encryption

    def test_decrypt(self):
        result = ciphers.Playfair.process("DMELQQLYNZIH", key="keyword", mode='d')
        self.assertEqual(result, "HIDETHEGOLDX")  # Includes padding character if added

'''
if __name__ == "__main__":
    unittest.main()
