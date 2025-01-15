import numpy as np

def Caesar(text, mode='e', key=5):
    result = ""
    for i in text:
        if i.isalpha():
            shift = ord('A') if i.isupper() else ord('a')
            key_adjusted = key if mode == 'e' else -1*key
            result += chr((ord(i) - shift + key_adjusted) % 26 + shift)
        else:
            result += i
    return result

def Vigenere(text, mode='e', key = "best"):
    key_length = len(key)
    result = ""
    key_index = 0
    for i in text:
        if i.isalpha():
            shift = ord('A') if i.isupper() else ord('a')
            key_char = key[key_index % key_length].lower()
            key_shift = ord(key_char) - ord('a')
            if mode != 'e':
                key_shift = -key_shift
            result += chr((ord(i) - shift + key_shift) % 26 + shift)
            key_index += 1
        else:
            result += i
    return result


class Hill:
    def encrypt(plaintext: str, key_matrix: list) -> str:
        alpha = "abcdefghijklmnopqrstuvwxyz"
        plaintext = plaintext.lower().replace(" ", "")
        plaintext += 'x' * ((len(key_matrix) - len(plaintext) % len(key_matrix)) % len(key_matrix))
        ciphertext = ""

        for i in range(0, len(plaintext), len(key_matrix)):
            block = plaintext[i:i + len(key_matrix)]
            block_vector = [alpha.index(char) for char in block]
            result_vector = np.dot(key_matrix, block_vector) % 26
            ciphertext += ''.join(alpha[idx] for idx in result_vector)

        return ciphertext

    def decrypt(ciphertext: str, inverse_key_matrix: list) -> str:
        alpha = "abcdefghijklmnopqrstuvwxyz"
        plaintext = ""

        for i in range(0, len(ciphertext), len(inverse_key_matrix)):
            block = ciphertext[i:i + len(inverse_key_matrix)]
            block_vector = [alpha.index(char) for char in block]
            result_vector = np.dot(inverse_key_matrix, block_vector) % 26
            plaintext += ''.join(alpha[idx] for idx in result_vector)

        return plaintext

class Playfair:
    def create_matrix(key: str) -> list:
        key = ''.join(sorted(set(key.upper()), key=key.index))
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix = [char for char in key if char.isalpha()]
        matrix += [char for char in alphabet if char not in matrix]
        return [matrix[i:i + 5] for i in range(0, 25, 5)]

    def process(text: str, key: str, mode: str = 'e') -> str:
        matrix = Playfair.create_matrix(key)
        text = ''.join([c.upper() for c in text if c.isalpha()]).replace("J", "I")
        if len(text) % 2 != 0:
            text += 'X'

        digraphs = [text[i:i + 2] for i in range(0, len(text), 2)]
        result = ""

        for digraph in digraphs:
            row1, col1 = Playfair.find_position(matrix, digraph[0])
            row2, col2 = Playfair.find_position(matrix, digraph[1])

            if row1 == row2:
                shift = 1 if mode == 'e' else -1
                result += matrix[row1][(col1 + shift) % 5] + matrix[row2][(col2 + shift) % 5]
            elif col1 == col2:
                shift = 1 if mode == 'e' else -1
                result += matrix[(row1 + shift) % 5][col1] + matrix[(row2 + shift) % 5][col2]
            else:
                result += matrix[row1][col2] + matrix[row2][col1]

        return result

    def find_position(matrix: list, char: str) -> tuple:
        for i, row in enumerate(matrix):
            if char in row:
                return i, row.index(char)
        return -1, -1
