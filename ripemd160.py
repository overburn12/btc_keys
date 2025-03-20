import struct

# RIPEMD-160 constants
K = [0x00000000, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E]
K_PRIME = [0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0x00000000]

# RIPEMD-160 shift amounts
S = [
    [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8],
    [7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12],
    [11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5],
    [11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12],
    [9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 7, 5, 11, 7, 6, 15]
]

S_PRIME = [
    [8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6],
    [9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11],
    [9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5],
    [15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8],
    [8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]
]

# RIPEMD-160 message order
R = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8],
    [3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12],
    [1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2],
    [4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13]
]

R_PRIME = [
    [5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12],
    [6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2],
    [15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13],
    [8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14],
    [12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11]
]

# RIPEMD-160 functions
def f(j, x, y, z):
    if j == 0: return x ^ y ^ z
    if j == 1: return (x & y) | (~x & z)
    if j == 2: return (x | ~y) ^ z
    if j == 3: return (x & z) | (y & ~z)
    if j == 4: return x ^ (y | ~z)

# Left rotation
def rol(value, bits):
    return ((value << bits) | (value >> (32 - bits))) & 0xFFFFFFFF

def hash(message):
    # Padding
    ml = len(message) * 8
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += struct.pack('<Q', ml)  # Little-endian length

    # Initial hash values
    h0, h1, h2, h3, h4 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0

    # Process blocks
    for i in range(0, len(message), 64):
        block = message[i:i + 64]
        X = list(struct.unpack('<16I', block))

        A, B, C, D, E = h0, h1, h2, h3, h4
        A_prime, B_prime, C_prime, D_prime, E_prime = A, B, C, D, E

        # Main loop
        for j in range(80):
            r_idx = j // 16
            T = (rol(A + f(r_idx, B, C, D) + X[R[r_idx][j % 16]] + K[r_idx], S[r_idx][j % 16]) + E) & 0xFFFFFFFF
            A, B, C, D, E = E, T, rol(B, 10), C, D

            T = (rol(A_prime + f(4 - r_idx, B_prime, C_prime, D_prime) + X[R_PRIME[r_idx][j % 16]] + K_PRIME[r_idx], S_PRIME[r_idx][j % 16]) + E_prime) & 0xFFFFFFFF
            A_prime, B_prime, C_prime, D_prime, E_prime = E_prime, T, rol(B_prime, 10), C_prime, D_prime

        # Combining results
        T = (h1 + C + D_prime) & 0xFFFFFFFF
        h1 = (h2 + D + E_prime) & 0xFFFFFFFF
        h2 = (h3 + E + A_prime) & 0xFFFFFFFF
        h3 = (h4 + A + B_prime) & 0xFFFFFFFF
        h4 = (h0 + B + C_prime) & 0xFFFFFFFF
        h0 = T

    return struct.pack('<5I', h0, h1, h2, h3, h4)