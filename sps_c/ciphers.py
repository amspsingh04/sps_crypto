import numpy as np

def Caesar(text, mode='e', key=5):
    result = ""
    for i in text:
        if i.isalpha():
            shift = ord('A') if i.isupper() else ord('a')
            key_adjusted = key if mode == 'e' else -1 * key
            result += chr((ord(i) - shift + key_adjusted) % 26 + shift)
        else:
            result += i
    return result

def Vigenere(text, mode='e', key="best"):
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

def create_playfair_square(key):
    key = key.replace('J', 'I').upper() + 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    key = "".join(dict.fromkeys(key))  
    grid = [[k for k in key[i:i+5]] for i in range(0, 25, 5)]
    return grid

def find_location(grid, char):
    for i in range(5):
        for j in range(5):
            if grid[i][j] == char:
                return i, j

def playfair_encrypt(message: str, key: str) -> str:
    playfair_square = create_playfair_square(key)
    ciphertext = ''
    message = "".join(filter(str.isalpha, message.upper())).replace('J', 'I')

    i = 0
    while i < len(message) - 1:
        if message[i] == message[i+1]:
            message = message[:i+1] + 'X' + message[i+1:]
        i += 1

    if len(message) % 2 == 1:
        message += 'X'

    for i in range(0, len(message), 2):
        digraph = message[i:i+2]
        row1, col1 = find_location(playfair_square, digraph[0])
        row2, col2 = find_location(playfair_square, digraph[1])
        if row1 == row2:
            sub1 = playfair_square[row1][(col1 + 1) % 5]
            sub2 = playfair_square[row2][(col2 + 1) % 5]
        elif col1 == col2:
            sub1 = playfair_square[(row1 + 1) % 5][col1]
            sub2 = playfair_square[(row2 + 1) % 5][col2]
        else:
            sub1 = playfair_square[row1][col2]
            sub2 = playfair_square[row2][col1]
        ciphertext += sub1 + sub2
    return ciphertext

def playfair_decrypt(ciphertext: str, key: str) -> str:
    playfair_square = create_playfair_square(key)
    message = ''
    for i in range(0, len(ciphertext), 2):
        digraph = ciphertext[i:i+2]
        row1, col1 = find_location(playfair_square, digraph[0])
        row2, col2 = find_location(playfair_square, digraph[1])
        if row1 == row2:
            sub1 = playfair_square[row1][(col1 - 1) % 5]
            sub2 = playfair_square[row2][(col2 - 1) % 5]
        elif col1 == col2:
            sub1 = playfair_square[(row1 - 1) % 5][col1]
            sub2 = playfair_square[(row2 - 1) % 5][col2]
        else:
            sub1 = playfair_square[row1][col2]
            sub2 = playfair_square[row2][col1]
        message += sub1 + sub2

    i = 0
    while i < len(message) - 2:
        if message[i] == message[i+2] and message[i+1] == 'X':
            message = message[:i+1] + message[i+2:]
        i += 1

    if message[-1] == 'X':
        message = message[:-1]

    return message
