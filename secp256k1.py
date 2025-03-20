class Point:
    """Represents a point on the secp256k1 curve."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({hex(self.x)}, {hex(self.y)})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# secp256k1 parameters
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A = 0
B = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

G = Point(Gx, Gy)


def inverse_mod(k, p):
    """Returns the modular inverse of k modulo p using Fermat's Little Theorem."""
    if k == 0:
        raise ValueError("Cannot compute modular inverse of zero.")
    return pow(k, -1, p)


def point_addition(P1, P2):
    """Adds two points on the secp256k1 curve using elliptic curve addition rules."""
    if P1 is None:
        return P2
    if P2 is None:
        return P1

    if P1.x == P2.x and P1.y != P2.y:
        return None  # Point at infinity (identity element)

    if P1 == P2:
        # Point doubling formula
        if P1.y == 0:
            return None  # Point at infinity
        lam = (3 * P1.x * P1.x * inverse_mod(2 * P1.y, P)) % P
    else:
        # Point addition formula
        lam = ((P2.y - P1.y) * inverse_mod(P2.x - P1.x, P)) % P

    x3 = (lam * lam - P1.x - P2.x) % P
    y3 = (lam * (P1.x - x3) - P1.y) % P
    return Point(x3, y3)


def hash(k):
    """Performs scalar multiplication k * point using the double-and-add algorithm."""
    point = G
    if k % N == 0 or point is None:
        return None  # Point at infinity

    R = None  # Identity element (point at infinity)
    temp = point  # Copy of the input point

    while k:
        if k & 1:
            R = point_addition(R, temp)
        temp = point_addition(temp, temp)
        k >>= 1

    return R
