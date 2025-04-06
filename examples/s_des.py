from sps_c.S_DES import sdes_decrypt, sdes_encrypt

if __name__ == "__main__":
    plaintext = "00101000"
    key = "1100011110"
    encrypted = sdes_encrypt(plaintext, key)
    decrypted = sdes_decrypt(encrypted, key)

    print("Plaintext:", plaintext)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)