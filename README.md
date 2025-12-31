# TOTP Generator (RFC 6238)

A lightweight Python implementation of **Time-based One-Time Passwords (TOTP)** compliant with **RFC 6238**.

This project focuses on correctness, simplicity, and educational clarity.

---

## Features

- RFC 6238 compliant TOTP generation
- Supports SHA-1, SHA-256, and SHA-512
- Configurable digit length and time step
- Optional custom timestamp (useful for testing)
- Minimal dependencies (standard library only)

> Note: An internal HOTP implementation exists as part of the TOTP logic, but only TOTP generation is exposed for now.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/MAY55A/TOTP_Generator.git
cd TOTP_Generator
```

## Usage

### Command Line Interface

Generate a TOTP code using the CLI:

```bash
python cli.py --secret "your-secret-key"
```

#### CLI Options

- `--secret` (required): Secret key in ASCII format
- `--digits`: Number of digits (default: 6)
- `--algo`: Hash algorithm - `sha1`, `sha256`, or `sha512` (default: `sha1`)
- `--timestep`: Time step in seconds (default: 30)
- `--t0`: Unix time to start counting (default: 0)
- `--timestamp`: Unix timestamp to use instead of current time

#### CLI Examples

```bash
# Basic TOTP with default settings
python cli.py --secret "MySecretKey"

# Custom digit length and algorithm
python cli.py --secret "MySecretKey" --digits 8 --algo sha256

# With specific timestamp (RFC 6238 test vector)
python cli.py --secret "12345678901234567890" --digits 8 --timestamp 59
```

### Python API

#### Generate a TOTP

```python
from core import totp

secret_key = b'your-secret-key'
token = totp(secret_key)
print(token)
```

#### Generate an HOTP

```python
from core import hotp

# Generate a 6-digit HOTP with counter
secret_key = b'your-secret-key'
token = hotp(secret_key, counter=0)
print(token)  # e.g., "123456"
```

## References

- [RFC 6238 - TOTP: Time-Based One-Time Password Algorithm](https://tools.ietf.org/html/rfc6238)
- [RFC 4226 - HOTP: An HMAC-Based One-Time Password Algorithm](https://tools.ietf.org/html/rfc4226)
