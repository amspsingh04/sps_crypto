import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sps_c.ds import RSADigitalSignature, ElGamalDigitalSignature

class TestDigitalSignatures(unittest.TestCase):
    """Test cases for RSA and ElGamal digital signatures"""
    
    def setUp(self):
        self.test_messages = [
            "Hello, world!",
            "Test message 123",
            "Another message to sign",
            "Special characters: !@#$%^&*()",
            ""
        ]
    
    def test_rsa_signature(self):
        """Test RSA signature generation and verification"""
        pub, priv = RSADigitalSignature.generate_keys(512)  # Smaller for faster tests
        
        for msg in self.test_messages:
            signature = RSADigitalSignature.sign(msg, priv)
            self.assertTrue(RSADigitalSignature.verify(msg, signature, pub),
                          f"RSA verification failed for message: '{msg}'")
            
            # Test with wrong message
            if msg:
                wrong_msg = msg + "x"
                self.assertFalse(RSADigitalSignature.verify(wrong_msg, signature, pub),
                               f"RSA verification should fail for altered message: '{msg}'")
    
    def test_elgamal_signature(self):
        """Test ElGamal signature generation and verification"""
        # Use fixed parameters for consistent testing
        p = 23  # Small prime for testing
        g = 5   # Generator for p=23
        x = 6    # Private key
        y = pow(g, x, p)
        
        public_key = (p, g, y)
        private_key = (p, x)
        
        for msg in self.test_messages:
            signature = ElGamalDigitalSignature.sign(msg, private_key)
            self.assertTrue(ElGamalDigitalSignature.verify(msg, signature, public_key),
                          f"ElGamal verification failed for message: '{msg}'")
            
            # Test with wrong message
            if msg:
                wrong_msg = msg + "x"
                self.assertFalse(ElGamalDigitalSignature.verify(wrong_msg, signature, public_key),
                               f"ElGamal verification should fail for altered message: '{msg}'")
    
    def test_signature_uniqueness(self):
        """Test that signatures are different for same message (due to randomness)"""
        pub_rsa, priv_rsa = RSADigitalSignature.generate_keys(512)
        pub_elg, priv_elg = ElGamalDigitalSignature.generate_keys(512)
        
        msg = "Test message"
        
        # RSA signatures should be deterministic (same input produces same output)
        sig1 = RSADigitalSignature.sign(msg, priv_rsa)
        sig2 = RSADigitalSignature.sign(msg, priv_rsa)
        self.assertEqual(sig1, sig2, "RSA signatures should be deterministic")
        
        # ElGamal signatures should be probabilistic (different each time)
        sig1 = ElGamalDigitalSignature.sign(msg, priv_elg)
        sig2 = ElGamalDigitalSignature.sign(msg, priv_elg)
        self.assertNotEqual(sig1, sig2, "ElGamal signatures should be probabilistic")

if __name__ == "__main__":
    # Demonstration of usage
    print("RSA Digital Signature Demo:")
    rsa_pub, rsa_priv = RSADigitalSignature.generate_keys(1024)
    message = "Important document to sign"
    signature = RSADigitalSignature.sign(message, rsa_priv)
    print(f"Message: {message}")
    print(f"Signature: {signature}")
    print(f"Verification: {RSADigitalSignature.verify(message, signature, rsa_pub)}")
    
    print("\nElGamal Digital Signature Demo:")
    elg_pub, elg_priv = ElGamalDigitalSignature.generate_keys(1024)
    message = "Important document to sign"
    signature = ElGamalDigitalSignature.sign(message, elg_priv)
    print(f"Message: {message}")
    print(f"Signature: {signature}")
    print(f"Verification: {ElGamalDigitalSignature.verify(message, signature, elg_pub)}")
    
    # Run unit tests
    print("\nRunning unit tests...")
    unittest.main(argv=[''], exit=False)