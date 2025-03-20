def encode(data: bytes) -> str:
    """Encodes bytes into Base58."""
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    
    # Count leading zero bytes
    leading_zeros = len(data) - len(data.lstrip(b'\x00'))
    
    # Convert to an integer
    num = int.from_bytes(data, 'big')
    
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = alphabet[mod] + result
    
    # Preserve leading zeroes as '1's
    return '1' * leading_zeros + result


def decode(base58_str: str) -> bytes:
    """Decodes a Base58-encoded string into bytes."""
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    base58_map = {char: index for index, char in enumerate(alphabet)}
    
    num = 0
    for char in base58_str:
        num = num * 58 + base58_map[char]
    
    # Convert the integer back to bytes
    byte_length = (num.bit_length() + 7) // 8
    result = num.to_bytes(byte_length, 'big') if num else b''

    # Preserve leading zeroes by counting leading '1's and prepending zero bytes
    leading_zeros = len(base58_str) - len(base58_str.lstrip('1'))
    
    return b'\x00' * leading_zeros + result

