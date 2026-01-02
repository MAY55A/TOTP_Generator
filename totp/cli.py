import argparse
from totp.core import totp

def main():
    parser = argparse.ArgumentParser(description="RFC 6238 TOTP generator")
    parser.add_argument("--secret", required=True, help="Secret in ASCII format")
    parser.add_argument("--digits", type=int, default=6, help="Number of digits in the TOTP code, default is 6")
    parser.add_argument("--algo", default="sha1", choices=["sha1", "sha256", "sha512"], help="Hash algorithm to use, default is sha1")
    parser.add_argument("--timestep", type=int, default=30, help="Time step in seconds, default is 30")
    parser.add_argument("--t0", type=int, default=0, help="Unix time to start counting time steps (T0), default is 0")
    parser.add_argument("--timestamp", type=int, help="Unix timestamp to use instead of current time")

    args = parser.parse_args()

    code = totp(
        k=args.secret.encode("utf-8"),
        digits=args.digits,
        algorithm=args.algo,
        timestep=args.timestep,
        t0=args.t0,
        unix_time=args.timestamp
    )

    print(f"Generated TOTP code: {code}")

if __name__ == "__main__":
    main()
