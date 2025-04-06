from sps_c.aes_mc import mixColumns_single, invMixColumns_single, mixColumns_state, print_state, printHex, invMixColumns_state

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