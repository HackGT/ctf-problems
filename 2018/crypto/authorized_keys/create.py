#!/usr/bin/env python3

from random import SystemRandom

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

SMALL_PRIMES = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
]

rng = SystemRandom()
backend = default_backend()


def miller_rabin(n):
    d = n - 1
    r = 0
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(32):
        a = rng.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def is_prime(n):
    for p in SMALL_PRIMES:
        if n % p == 0:
            return False

    return miller_rabin(n)


def random_prime(bits):
    p = 4
    while not is_prime(p):
        p = rng.getrandbits(bits)
    return p


def rsa_pq(p, q, e=65537):
    n = p * q
    public_numbers = rsa.RSAPublicNumbers(e=e, n=n)
    d = rsa._modinv(e, (p - 1) * (q - 1) // 2)
    private_numbers = rsa.RSAPrivateNumbers(
        public_numbers=public_numbers,
        p=p,
        q=q,
        d=d,
        dmp1=rsa.rsa_crt_dmp1(d, p),
        dmq1=rsa.rsa_crt_dmq1(d, q),
        iqmp=rsa.rsa_crt_iqmp(p, q),
    )
    return private_numbers.private_key(backend)


def main():
    p = random_prime(1024)
    q = random_prime(1024)
    r = random_prime(1024)

    k1 = rsa_pq(p, q)
    k2 = rsa_pq(p, r)
    k3 = rsa.generate_private_key(65537, 2048, backend)
    k4 = rsa.generate_private_key(65537, 2048, backend)
    k5 = rsa.generate_private_key(65537, 2048, backend)

    keys = [k1, k2, k3, k4, k5]
    rng.shuffle(keys)

    with open("authorized_keys", "wb") as f:
        for k in keys:
            f.write(
                k.public_key().public_bytes(
                    encoding=Encoding.OpenSSH, format=PublicFormat.OpenSSH
                )
            )
            f.write(b"\n")


if __name__ == "__main__":
    main()
