import btc_keys

def hex_2_binary(str_hex):
    """takes a string of hex and returns a string of binary"""
    hex_table = {
        "0": "0000", "1": "0001", "2": "0010", "3": "0011",
        "4": "0100", "5": "0101", "6": "0110", "7": "0111",
        "8": "1000", "9": "1001", "a": "1010", "b": "1011",
        "c": "1100", "d": "1101", "e": "1110", "f": "1111",
        "A": "1010", "B": "1011",
        "C": "1100", "D": "1101", "E": "1110", "F": "1111"
    }
    str_bin = ""
    for i in range(0, len(str_hex)):
        str_bin += hex_table[str_hex[i:i+1]]
    return str_bin

def display_binary(key_hex):
    #print(hex(btc_keys.SECP256K1_ORDER)[2:])
    key_bin = hex_2_binary(key_hex)
    segment_len = 8
    segments_per_line = (256 / segment_len) / 2
    for i in range(0, len(key_bin), segment_len):
        if i % (segment_len * segments_per_line) == 0 and i != 0:
            print("")
        print(f"{key_bin[i:i+segment_len]} ", end='')
    print('')

def str_hex_2_int(str_hex):
    int_num = 0
    str_bin = hex_2_binary(str_hex)

    step_num = 0
    for i in range(len(str_bin), 0, -1):
        if(str_bin[i-1:i]=="1"):
            int_num+= 2**step_num
        step_num+=1

    return int_num

def validate_private_key(private_key_int):
    """Generate a valid random private key within the Secp256k1 curve order."""
    # Ensure the private key is within the valid range
    if private_key_int < 1 or private_key_int >= btc_keys.SECP256K1_ORDER:
        private_key_int %= btc_keys.SECP256K1_ORDER
        if private_key_int == 0:
            private_key_int = 1

    # Return the validated private key as a 64-character hexadecimal string
    return f"{private_key_int:064x}"

def generate_key_pair(private_key_int, compressed=True):
    """Generate a Bitcoin key pair."""
    private_key_hex = validate_private_key(private_key_int)
    public_key_hex = btc_keys.priv_to_pub(private_key_hex, compressed)
    p2pkh_address = btc_keys.pub_to_p2pkh(public_key_hex)
    wif = btc_keys.priv_to_wif(private_key_hex, compressed)
    return wif, p2pkh_address

if False:
    wif = "5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreQDpvAKR"
    print("WIF: " + wif)
    priv_hex = btc_keys.wif_to_priv(wif)
    print("HEX: " + priv_hex)
    print("BINARY:")
    display_binary(priv_hex)
    print(f"INT: {str_hex_2_int(priv_hex)}")

    sat_hex = "04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f"
    sat_p2pkh = btc_keys.pub_to_p2pkh(sat_hex)
    print(sat_p2pkh)

if False:
    wif_key, p2pkh_addres = generate_key_pair(private_key_int)
    display_binary(f"{private_key_int:064x}")
    print (wif_key, p2pkh_addres)

if False:
    wif = ""
    # Convert WIF to private key (hex)
    private_key_hex = btc_keys.wif_to_priv(wif)

    # Convert private key to public key (compressed)
    public_key_hex = btc_keys.priv_to_pub(private_key_hex, compressed=True)

    # Construct the descriptor
    descriptor = f"pkh({public_key_hex})"
    print(descriptor)


