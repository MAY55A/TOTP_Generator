import hmac
import time

def prepare_secret(password, algorithm):
    """Convert a password to a suitable secret for TOTP:
    1. Encode the password to bytes
    2. Repeat the password bytes until it reaches the required length for the hash algorithm
    """
    password_bytes = password.encode('utf-8')
    
    if algorithm.lower() == "sha1":
        # SHA-1 needs at least 20 bytes
        target_len = 20
    elif algorithm.lower() == "sha256":
        # SHA-256 needs at least 32 bytes
        target_len = 32
    elif algorithm.lower() == "sha512":
        # SHA-512 needs at least 64 bytes
        target_len = 64
    else:
        target_len = 20  # Default to SHA-1 length
    
    if len(password_bytes) < target_len:
        repeats = (target_len + len(password_bytes) - 1) // len(password_bytes)
        secret = (password_bytes * repeats)[:target_len]
        return secret
    else:
        return password_bytes

def DT(hs): # Dynamic Truncation
    offset = hs[-1] & 0b1111 # or & 15 or & 0xf to get last 4 bits
    p = hs[offset:offset+4]
    # Get last 31 bits from 32 bits (4 bytes)
    s_bits = bytearray()
    s_bits.append(p[0] & 0x7f) # zero the most significant bit, return 7 bits
    for b in p[1:]:
        s_bits.append(b & 0xff) # return 8 bits exactly (apparently a byte can have more than 8 bits)
    return s_bits

def HOTP(k, c, digits=6, algorithm="sha1"):
    """HTOP :
    k is the shared key,
    C is the counter value,
    digits control the response length,
    algorithm is the hash function to use (e.g., 'sha1', 'sha256', 'sha512')
    """

    k = prepare_secret(k, algorithm)
    counter_bytes = c.to_bytes(8, 'big') # 8-byte big-endian
    hs_hmac = hmac.new(k, counter_bytes, algorithm)
    hs = hs_hmac.digest()
    s_bits = DT(hs)
    s_num = int.from_bytes(s_bits, 'big')
    otp = s_num % (10 ** digits)
    return str(otp).zfill(digits)

def TOTP(k, digits=6, timestep=30, t0=0, algorithm="sha1", unix_time=int(time.time())):
    """TOTP with specific Unix timestamp :
    k is the shared key,
    digits control the response length,
    timestep is the time step in seconds (default 30 seconds),
    t0 is the Unix time to start counting time steps (default 0),
    algorithm is the hash function to use (e.g., 'sha1', 'sha256', 'sha512'),
    unix_time is the specific Unix timestamp to use (default None, which uses current time)
    """

    time_steps = (unix_time - t0) // timestep
    return HOTP(k, time_steps, digits, algorithm)