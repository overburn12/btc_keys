import os
import hashlib
import base58
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import RIPEMD160

def ripemd160(data):
    return RIPEMD160.new(data).digest()

# Secp256k1 curve order
SECP256K1_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def generate_private_key():
    """Generate a valid random private key within the Secp256k1 curve order."""
    private_key_int = int.from_bytes(os.urandom(32), 'big')
    while private_key_int == 0 or private_key_int >= SECP256K1_ORDER:
        private_key_int = int.from_bytes(os.urandom(32), 'big')
    return f"{private_key_int:064x}"  # Ensure it's always 64 hex characters


def priv_to_pub(private_key_hex, compressed=True):
    """Convert a private key to a public key (compressed or uncompressed)."""
    private_key_bytes = bytes.fromhex(private_key_hex)
    signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    verifying_key = signing_key.verifying_key
    public_key_bytes = verifying_key.to_string()
    x_bytes, y_bytes = public_key_bytes[:32], public_key_bytes[32:]
    if compressed:
        prefix = b'\x02' if y_bytes[-1] % 2 == 0 else b'\x03'
        return (prefix + x_bytes).hex()
    else:
        return (b'\x04' + public_key_bytes).hex()


def pub_to_p2pkh(public_key_hex):
    """Convert a public key to a P2PKH Bitcoin address."""
    public_key_bytes = bytes.fromhex(public_key_hex)
    sha256_hash = hashlib.sha256(public_key_bytes).digest()
    ripemd160_hash = ripemd160(sha256_hash)
    versioned_payload = b'\x00' + ripemd160_hash  # Mainnet prefix
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
    binary_address = versioned_payload + checksum
    p2pkh = base58.b58encode(binary_address).decode()
    return p2pkh


def priv_to_wif(private_key_hex, compressed=True):
    """Convert a private key in hex format to Wallet Import Format (WIF)."""
    private_key_bytes = bytes.fromhex(private_key_hex)
    if compressed:
        private_key_bytes += b'\x01'  # Append 0x01 if compressed
    versioned_payload = b'\x80' + private_key_bytes  # Mainnet prefix
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
    return base58.b58encode(versioned_payload + checksum).decode()


def wif_to_priv(wif):
    """Convert a Wallet Import Format (WIF) key back to a private key."""
    decoded_wif = base58.b58decode(wif)
    if len(decoded_wif) not in [37, 38]:  # 37 bytes (uncompressed) or 38 bytes (compressed) — includes version + 4-byte checksum
        raise ValueError("Invalid WIF length")
    private_key_bytes = decoded_wif[1:-4]  # Remove version byte and checksum
    compressed = len(private_key_bytes) == 33
    return private_key_bytes[:-1].hex() if compressed else private_key_bytes.hex()


def generate_key_pair(compressed=True):
    """Generate a Bitcoin key pair."""
    private_key_hex = generate_private_key()
    public_key_hex = priv_to_pub(private_key_hex, compressed)
    p2pkh_address = pub_to_p2pkh(public_key_hex)
    wif = priv_to_wif(private_key_hex, compressed)
    return wif, p2pkh_address