from sps_crypto import DES

# Example usage
plaintext = "0123456789ABCDEF"
key = "133457799BBCDFF1"
encrypted = DES.des_encrypt(plaintext, key)
print("Encrypted message:", encrypted)
## output will be 85E813540F0AB405