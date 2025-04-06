# aes_mc.py

def gmul(a, b):
    p = 0
    while b:
        if b & 1:
            p ^= a
        a = (a << 1) ^ 0x1B if (a & 0x80) else (a << 1)
        a &= 0xFF
        b >>= 1
    return p

def printHex(val):
    print(f'{val:02x}', end=' ')

def mixColumns_single(a, b, c, d):
    r0 = gmul(a, 2) ^ gmul(b, 3) ^ gmul(c, 1) ^ gmul(d, 1)
    r1 = gmul(a, 1) ^ gmul(b, 2) ^ gmul(c, 3) ^ gmul(d, 1)
    r2 = gmul(a, 1) ^ gmul(b, 1) ^ gmul(c, 2) ^ gmul(d, 3)
    r3 = gmul(a, 3) ^ gmul(b, 1) ^ gmul(c, 1) ^ gmul(d, 2)
    return [r0, r1, r2, r3]

def invMixColumns_single(a, b, c, d):
    r0 = gmul(a, 14) ^ gmul(b, 11) ^ gmul(c, 13) ^ gmul(d, 9)
    r1 = gmul(a, 9) ^ gmul(b, 14) ^ gmul(c, 11) ^ gmul(d, 13)
    r2 = gmul(a, 13) ^ gmul(b, 9) ^ gmul(c, 14) ^ gmul(d, 11)
    r3 = gmul(a, 11) ^ gmul(b, 13) ^ gmul(c, 9) ^ gmul(d, 14)
    return [r0, r1, r2, r3]

def mixColumns_state(state):
    return [mixColumns_single(*col) for col in state]

def invMixColumns_state(state):
    return [invMixColumns_single(*col) for col in state]

def print_state(state):
    print("State Matrix:")
    for row in range(4):
        for col in range(4):
            printHex(state[col][row])
        print()
    print()

# ---- Test Vectors ----
'''
print("Forward MixColumns Test:")
test_state = [
    [0xdb, 0x13, 0x53, 0x45],
    [0xf2, 0x0a, 0x22, 0x5c],
    [0x01, 0x01, 0x01, 0x01],
    [0xc6, 0xc6, 0xc6, 0xc6]
]

mixed = mixColumns_state(test_state)
print_state(mixed)

print("Inverse MixColumns Test (restores original):")
restored = invMixColumns_state(mixed)
print_state(restored)

print("Example MixColumns and Inverse:")
example_state = [
    [0x00, 0x11, 0x22, 0x33],
    [0x44, 0x55, 0x66, 0x77],
    [0x88, 0x99, 0xaa, 0xbb],
    [0xcc, 0xdd, 0xee, 0xff]
]

example_mixed = mixColumns_state(example_state)
print("Mixed:")
print_state(example_mixed)

example_restored = invMixColumns_state(example_mixed)
print("Restored:")
print_state(example_restored)
'''