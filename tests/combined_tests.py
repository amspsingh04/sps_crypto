import unittest
import hashlib
import hmac
from sps_c import aes_mc, ciphers, DES, dh_mitm, ds, elgamal, rsa, S_DES

class TestCryptoSuite(unittest.TestCase):
    def test_mix_columns(self):
        original = [0xdb, 0x13, 0x53, 0x45]
        expected = [0x8e, 0x4d, 0xa1, 0xbc]
        result = aes_mc.mixColumns_single(*original)
        self.assertEqual(result, expected)

    def test_inv_mix_columns(self):
        mixed = [0x8e, 0x4d, 0xa1, 0xbc]
        restored = aes_mc.invMixColumns_single(*mixed)
        self.assertEqual(restored, [0xdb, 0x13, 0x53, 0x45])

    def test_caesar_cipher(self):
        text = "HELLO"
        encrypted = ciphers.Caesar(text, 'e', 3)
        decrypted = ciphers.Caesar(encrypted, 'd', 3)
        self.assertEqual(decrypted, text)

    def test_vigenere_cipher(self):
        text = "HELLO"
        encrypted = ciphers.Vigenere(text, 'e', "KEY")
        decrypted = ciphers.Vigenere(encrypted, 'd', "KEY")
        self.assertEqual(decrypted, text)

    def test_playfair_cipher(self):
        text = "HELLO"
        key = "MONARCHY"
        encrypted = ciphers.Playfair.process(text, key, 'e')
        decrypted = ciphers.Playfair.process(encrypted, key, 'd')
        self.assertTrue(text[0] in decrypted)

    def test_des_encryption(self):
        plaintext = "0123456789ABCDEF"
        key = "133457799BBCDFF1"
        encrypted = DES.des_encrypt(plaintext, key)
        decrypted = DES.des_decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)

    def test_rsa_encryption_decryption(self):
        pub, priv = rsa.generate_rkeys(61, 53)
        message = "Hi"
        cipher = rsa.rencrypt(message, pub)
        decrypted = rsa.rdecrypt(cipher, priv)
        self.assertEqual(decrypted, message)

    def test_sdes(self):
        plaintext = "10101010"
        key = "1010000010"
        cipher = S_DES.sdes_encrypt(plaintext, key)
        decrypted = S_DES.sdes_decrypt(cipher, key)
        self.assertEqual(decrypted, plaintext)

    def test_elgamal_encryption_decryption(self):
        keys = elgamal.generate_keys(256)
        message = 12345
        ciphertext = elgamal.encrypt(keys['public'], message)
        decrypted = elgamal.decrypt(keys['private'], ciphertext)
        self.assertEqual(decrypted, message)

    def test_rsa_signature(self):
        pub, priv = ds.RSADigitalSignature.generate_keys(512)
        message = "Test RSA Signature"
        signature = ds.RSADigitalSignature.sign(message, priv)
        verified = ds.RSADigitalSignature.verify(message, signature, pub)
        self.assertTrue(verified)

    def test_elgamal_signature(self):
        pub, priv = ds.ElGamalDigitalSignature.generate_keys(256)
        message = "Test ElGamal Signature"
        signature = ds.ElGamalDigitalSignature.sign(message, priv, pub)
        verified = ds.ElGamalDigitalSignature.verify(message, signature, pub)
        self.assertTrue(verified)

    def test_hmac_variants(self):
        key = b"abracadabra"
        message = b"Welcome to SPSCrypto."
        self.assertTrue(hmac.new(key, message, hashlib.md5).digest())
        self.assertTrue(hmac.new(key, message, hashlib.sha1).digest())
        self.assertTrue(hmac.new(key, message, hashlib.sha256).digest())
        self.assertTrue(hmac.new(key, message, hashlib.sha512).digest())

if __name__ == '__main__':
    unittest.main()