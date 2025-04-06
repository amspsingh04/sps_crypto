import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sps_c.aes_mc import mixColumns_state, invMixColumns_state

class TestMixColumns(unittest.TestCase):

    def test_forward_mix_columns(self):
        input_state = [
            [0xdb, 0x13, 0x53, 0x45],
            [0xf2, 0x0a, 0x22, 0x5c],
            [0x01, 0x01, 0x01, 0x01],
            [0xc6, 0xc6, 0xc6, 0xc6]
        ]
        expected_outputs = [
            [0x8e, 0x4d, 0xa1, 0xbc],
            [0x9f, 0xdc, 0x58, 0x9d],
            [0x01, 0x01, 0x01, 0x01],
            [0xc6, 0xc6, 0xc6, 0xc6]
        ]
        outputs = mixColumns_state(input_state)
        self.assertEqual(outputs, expected_outputs)

    def test_inverse_mix_columns(self):
        original_state = [
            [0x2d, 0x26, 0x31, 0x4c]
        ] * 4
        mixed = mixColumns_state(original_state)
        restored = invMixColumns_state(mixed)
        self.assertEqual(restored, original_state)

    def test_round_trip(self):
        state = [
            [0x00, 0x11, 0x22, 0x33],
            [0x44, 0x55, 0x66, 0x77],
            [0x88, 0x99, 0xaa, 0xbb],
            [0xcc, 0xdd, 0xee, 0xff]
        ]
        mixed = mixColumns_state(state)
        restored = invMixColumns_state(mixed)
        self.assertEqual(restored, state)

if __name__ == '__main__':
    unittest.main()
