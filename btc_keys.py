import binascii
import os
import hashlib

#---- modules ---------------
import secp256k1
import ripemd160
import base58
#----------------------------


def generate_random_private_key() -> str:
    while True:
        private_key_int = int.from_bytes(os.urandom(32), 'big')
        if 1 <= private_key_int < secp256k1.N:  # Ensure it's within the valid range
            return format(private_key_int, '064x')


def private_key_to_public_key(private_key_hex: str, compressed: bool = False) -> str:
    private_key_int = int(private_key_hex, 16)
    
    public_key_point = secp256k1.hash(private_key_int)
    
    if compressed:
        prefix = '02' if public_key_point.y % 2 == 0 else '03'
        return prefix + format(public_key_point.x, '064x')
    else:
        return '04' + format(public_key_point.x, '064x') + format(public_key_point.y, '064x')


def public_key_to_p2pkh_address(public_key_hex: str) -> str:
    public_key_bytes = binascii.unhexlify(public_key_hex)
    ripemd160_hash = ripemd160.hash(hashlib.sha256(public_key_bytes).digest())
    
    # Add network byte (0x00 for mainnet)
    network_byte = b'\x00' + ripemd160_hash
    
    # Compute checksum
    checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]
    
    # Encode in Base58
    address = base58.encode(network_byte + checksum)
    return address


def hex_to_wif(hex_key, compressed=True, testnet=False):
    # Convert hex key to bytes
    private_key_bytes = bytes.fromhex(hex_key)

    # Prefix with 0x80 for mainnet, 0xEF for testnet
    prefix = b'\xEF' if testnet else b'\x80'
    extended_key = prefix + private_key_bytes

    # Append 0x01 if using a compressed public key
    if compressed:
        extended_key += b'\x01'

    # Double SHA-256 hash
    first_hash = hashlib.sha256(extended_key).digest()
    second_hash = hashlib.sha256(first_hash).digest()

    # Take first 4 bytes as checksum
    checksum = second_hash[:4]

    # Append checksum
    final_key = extended_key + checksum

    # Encode in Base58Check using your own encode function
    wif_key = base58.encode(final_key)

    return wif_key


def generate_key_pair(compressed: bool = True) -> tuple:
    private_key_hex = generate_random_private_key()
    public_key_hex = private_key_to_public_key(private_key_hex, compressed)
    p2pkh_address = public_key_to_p2pkh_address(public_key_hex)
    wif_private_key = hex_to_wif(private_key_hex, compressed)
    return (wif_private_key, p2pkh_address)