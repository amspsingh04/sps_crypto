# rsa.py

from math import gcd

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_rkeys(p, q):
    n = p * q
    totient = (p - 1) * (q - 1)
    e = next(i for i in range(2, totient) if gcd(i, totient) == 1)
    d = modinv(e, totient)
    return (e, n), (d, n)

def encrypt_integer(m, public_key):
    e, n = public_key
    if m >= n:
        raise ValueError(f"Message integer ({m}) must be less than modulus n ({n}).")
    return pow(m, e, n)

def decrypt_integer(c, private_key):
    d, n = private_key
    return pow(c, d, n)

def string_to_int(s):
    return int.from_bytes(s.encode(), 'big')

def int_to_string(i):
    try:
        return i.to_bytes((i.bit_length() + 7) // 8, 'big').decode()
    except Exception:
        return f"<Failed to decode to string: {i}>"

def rencrypt(message, public_key):
    if isinstance(message, int):
        m = message
    elif isinstance(message, str) and message.startswith("0x"):
        m = int(message, 16)
    elif isinstance(message, str):
        m = string_to_int(message)
    else:
        raise ValueError("Unsupported message type. Use int, hex string (starting with '0x'), or plain text.")

    return encrypt_integer(m, public_key)

def rdecrypt(cipher, private_key, output_format='text'):
    m = decrypt_integer(cipher, private_key)

    if output_format == 'hex':
        return hex(m)
    elif output_format == 'int':
        return m
    elif output_format == 'text':
        return int_to_string(m)
    else:
        raise ValueError("Unsupported format. Use 'text', 'hex', or 'int'.")
