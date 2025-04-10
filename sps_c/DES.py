# DES.py
## Tables of DES
KP = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
IP = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]
IPI = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]
PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
E = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]

S_BOXES = [
    [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7], [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8], [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0], [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
    [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10], [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5], [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15], [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
    [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8], [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1], [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7], [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
    [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15], [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9], [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4], [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
    [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9], [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6], [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14], [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
    [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11], [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8], [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6], [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
    [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1], [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6], [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2], [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
    [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7], [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2], [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8], [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
]

P = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]

# Utility functions
def xor(str1, str2):
    return ''.join('0' if a == b else '1' for a, b in zip(str1, str2))

def f(rstr,kstr):
    r_ret=''
    for i in E:
        r_ret+=rstr[i-1]
    ret = xor(kstr,r_ret)
    ans=''
    j=1
    jdict={1:S_BOXES[0],2:S_BOXES[1],3:S_BOXES[2],4:S_BOXES[3],5:S_BOXES[4],6:S_BOXES[5],7:S_BOXES[6],8:S_BOXES[7]}
    for i in range(0,len(ret),6):
        
        x=ret[i:i+6]
        ends=int(x[0]+x[5],2)
        mids=int(x[1:5],2)
        l=jdict[j]
        lenn = len((bin((l[ends][mids]))[2:]))
        while(lenn<4):
            ans+='0'
            lenn+=1
        ans+=bin(l[ends][mids])[2:]
        j+=1
    toret=''
    for i in P:
        toret+=ans[i-1]
    return toret  

def generate_keys(key):
    binary_key = bin(int(key, 16))[2:].zfill(64)
    KPlus = ''.join(binary_key[i-1] for i in KP)

    C = [KPlus[:28]]
    D = [KPlus[28:]]

    subkeys = []
    for i in range(1, 17):
        shifts = 1 if i in [1, 2, 9, 16] else 2
        C.append(C[i-1][shifts:] + C[i-1][:shifts])
        D.append(D[i-1][shifts:] + D[i-1][:shifts])

        CD = C[i] + D[i]
        subkey = ''.join(CD[j-1] for j in PC2)
        subkeys.append(subkey)

    return subkeys


def initial_permutation(plaintext):
    return ''.join(plaintext[i-1] for i in IP)

def inverse_initial_permutation(data):
    return ''.join(data[i-1] for i in IPI)

def des_decrypt(ciphertext, key="133457799BBCDFF1"):
    if(len(ciphertext)<1 or len(key)!=16):
        raise ValueError
    try:
        binary_cipher=bin(int(ciphertext,16))[2:].zfill(64)
    except ValueError as e:
        if isinstance(ciphertext,str):
            binary_cipher=''.join(format(ord(c),'08b') for c in ciphertext)
        if len(binary_cipher) < 64:
            binary_cipher = binary_cipher.ljust(64,'0')
    binary_cipher = ''.join(binary_cipher[i-1] for i in IP)
    l,r=binary_cipher[:32],binary_cipher[32:]
    subkeys=generate_keys(key)
    for i in reversed(range(1,17)):
        l,r=r,xor(l,f(r,subkeys[i-1]))
    RL = r+l
    decrypted_binary = ''.join(RL[i-1] for i in IPI)
    decrypted_hex = hex(int(decrypted_binary, 2))[2:].upper().zfill(16)
    return decrypted_hex 
    
def des_encrypt(plaintext, key="133457799BBCDFF1"):
    
    if(len(plaintext)<1 or len(key)!=16):
        raise ValueError
    try:
        binary_plaintext = bin(int(plaintext, 16))[2:].zfill(64)
    except ValueError as e:
        if isinstance(plaintext, str):
            binary_plaintext = ''.join(format(ord(c), '08b') for c in plaintext)
            if len(binary_plaintext) < 64:
                binary_plaintext = binary_plaintext.ljust(64, '0')  

    IPM = ''.join(binary_plaintext[i-1] for i in IP)
    L = [IPM[:32]]
    R = [IPM[32:]]
    subkeys = generate_keys(key)
    for i in range(1, 17):
        L.append(R[i-1])
        R.append(xor(L[i-1], f(R[i-1], subkeys[i-1])))
    RL = R[16] + L[16]
    encrypted_binary = ''.join(RL[i-1] for i in IPI)
    encrypted_hex = hex(int(encrypted_binary, 2))[2:].upper()
    return encrypted_hex


__all__ = ['des_encrypt','des_decrypt']
