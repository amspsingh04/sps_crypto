# sdes.py

P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8  = [6, 3, 7, 4, 8, 5, 10, 9]
IP  = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
EP  = [4, 1, 2, 3, 2, 3, 4, 1]
P4  = [2, 4, 3, 1]

S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]

def permute(bits, table):
    return [bits[i-1] for i in table]

def left_shift(bits, shifts):
    return bits[shifts:] + bits[:shifts]

def xor(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def bits_to_int(bits):
    return int("".join(map(str, bits)), 2)

def int_to_bits(val, bits=4):
    return [int(x) for x in bin(val)[2:].zfill(bits)]

def sbox_lookup(bits, sbox):
    row = bits[0]*2 + bits[3]
    col = bits[1]*2 + bits[2]
    return int_to_bits(sbox[row][col], 2)

def generate_keys(key):
    key = [int(b) for b in key]
    p10 = permute(key, P10)
    left, right = p10[:5], p10[5:]
    
    left1 = left_shift(left, 1)
    right1 = left_shift(right, 1)
    k1 = permute(left1 + right1, P8)
    
    left2 = left_shift(left1, 2)
    right2 = left_shift(right1, 2)
    k2 = permute(left2 + right2, P8)
    
    return k1, k2

def fk(bits, key):
    left, right = bits[:4], bits[4:]
    ep = permute(right, EP)
    xor_result = xor(ep, key)
    s0_bits = sbox_lookup(xor_result[:4], S0)
    s1_bits = sbox_lookup(xor_result[4:], S1)
    p4 = permute(s0_bits + s1_bits, P4)
    return xor(left, p4) + right

def switch(bits):
    return bits[4:] + bits[:4]

def sdes_encrypt(plaintext, key):
    if len(plaintext) != 8 or len(key) != 10:
        raise ValueError("Plaintext must be 8 bits and key must be 10 bits")
    k1, k2 = generate_keys(key)
    bits = [int(b) for b in plaintext]
    ip = permute(bits, IP)
    temp = fk(ip, k1)
    temp = switch(temp)
    temp = fk(temp, k2)
    cipher = permute(temp, IP_INV)
    return "".join(map(str, cipher))

def sdes_decrypt(ciphertext, key):
    if len(ciphertext) != 8 or len(key) != 10:
        raise ValueError("Plaintext must be 8 bits and key must be 10 bits")
    k1, k2 = generate_keys(key)
    bits = [int(b) for b in ciphertext]
    ip = permute(bits, IP)
    temp = fk(ip, k2)
    temp = switch(temp)
    temp = fk(temp, k1)
    plain = permute(temp, IP_INV)
    return "".join(map(str, plain))

'''
'''