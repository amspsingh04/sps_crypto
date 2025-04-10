# sps-crypto
A Python library providing implementations of various cryptographic algorithms. This project includes classical ciphers, modern symmetric and asymmetric encryption algorithms, digital signatures, and related utilities. It is primarily intended for educational purposes and developers interested in exploring cryptography.

**Note:** This library is currently in **Stable** status (version `1.0.78`).

## Features

The library currently includes implementations for:

**Classical Ciphers:**
* Caesar Cipher
* Vigenere Cipher
* Playfair Cipher

**Symmetric Encryption:**
* DES (Data Encryption Standard)
* S-DES (Simplified DES)
* AES (Advanced Encryption Standard) - *Currently includes MixColumns/InvMixColumns operations.*

**Asymmetric Encryption:**
* RSA (Rivest–Shamir–Adleman)
* ElGamal Encryption System

**Digital Signatures:**
* RSA Digital Signature
* ElGamal Digital Signature

**Key Exchange:**
* Diffie-Hellman Key Exchange (including simulation of Man-in-the-Middle attack)

**Utilities:**
* Prime number generation and testing
* Primitive root finding
* Modular exponentiation and modular inverse
* Hashing (SHA-256 used internally for signatures)
* Text/Integer conversions for cryptographic operations

**Networking:**
* Basic client/server socket implementation (details in `examples/sockets.py`)

## Installation

You can install the library using pip:

```bash
pip install sps-crypto
```

Requires Python version 3.6 or higher.

Usage Examples
Usage examples can be found in the examples directory



Project Links
GitHub Repository: https://github.com/amspsingh04/sps_crypto
Bug Reports: https://github.com/amspsingh04/sps_crypto/issues

Contributing
Contributions, issues, and feature requests are welcome. Please refer to the GitHub repository and issue tracker.
