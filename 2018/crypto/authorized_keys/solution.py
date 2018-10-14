#!/usr/bin/env python3

import os
from functools import partial
from itertools import product
from math import gcd

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    load_ssh_public_key,
)

backend = default_backend()


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
    with open("authorized_keys", "rb") as f:
        keys = [load_ssh_public_key(l.strip(), backend) for l in f]

    for k1, k2 in product(keys, repeat=2):
        n1 = k1.public_numbers().n
        n2 = k2.public_numbers().n
        if n1 == n2:
            continue
        p = gcd(n1, n2)
        if p != 1:
            q = n1 // p
            k = rsa_pq(p, q)
            with open("id_rsa", "wb", opener=partial(os.open, mode=0o600)) as f:
                f.write(
                    k.private_bytes(
                        encoding=Encoding.PEM,
                        format=PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=NoEncryption(),
                    )
                )
            break


if __name__ == "__main__":
    main()
