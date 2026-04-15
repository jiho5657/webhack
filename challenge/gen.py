#!/usr/bin/env python3
"""
Hollowed -- crypto challenge generator.

We construct an RSA modulus N = p * q * r where p, q, r are primes of
roughly equal size.  The secret flag is encrypted with the usual
textbook RSA, and players are handed the public data together with
a block of the most-significant bits of p.

The number of leaked bits sits just above the Coppersmith threshold
beta^2 * log2(N) with beta = 1/3, which makes standard beta = 1/2
recipes fail.  Recognising that beta = log p / log N ~= 1/3 for
three balanced primes is the whole trick.

Once p is recovered the flag is small enough to be decrypted modulo
p alone: m = c^(e^{-1} mod (p-1)) mod p.
"""

from Crypto.Util.number import getPrime, bytes_to_long
from pathlib import Path


# ------------------------------------------------------------------
# parameters
# ------------------------------------------------------------------
PRIME_BITS = 683          # size of each of p, q, r (N ~ 2049 bits)
UNKNOWN_BITS = 213        # bits of p hidden from the player
LEAK_BITS = PRIME_BITS - UNKNOWN_BITS   # bits of p disclosed (470)
E = 65537

FLAG = b"flag{c0pp3rsm1th_w1th_b3t4_0n3_th1rd_1s_th3_k3y_ad3f12}"


def gen():
    # distinct primes of equal nominal size
    while True:
        p = getPrime(PRIME_BITS)
        q = getPrime(PRIME_BITS)
        r = getPrime(PRIME_BITS)
        if len({p, q, r}) == 3:
            break

    N = p * q * r
    m = bytes_to_long(FLAG)
    assert m < p, "flag must be smaller than the smallest prime"
    c = pow(m, E, N)

    # leak the top LEAK_BITS of p; equivalently, p >> UNKNOWN_BITS
    p_high = p >> UNKNOWN_BITS

    return {
        "N": N,
        "e": E,
        "c": c,
        "prime_bits": PRIME_BITS,
        "unknown_bits": UNKNOWN_BITS,
        "leak_bits": LEAK_BITS,
        "p_high": p_high,
    }


def write_output(data, path):
    lines = [
        "# Hollowed -- public parameters",
        "#",
        "# N  = p * q * r, three primes of equal bit-length.",
        "# c  = flag^e  mod  N.",
        "# p_high  =  p >> unknown_bits   (the top leak_bits of p).",
        "",
        f"prime_bits   = {data['prime_bits']}",
        f"unknown_bits = {data['unknown_bits']}",
        f"leak_bits    = {data['leak_bits']}",
        f"e            = {data['e']}",
        "",
        f"N = {data['N']}",
        "",
        f"p_high = {data['p_high']}",
        "",
        f"c = {data['c']}",
        "",
    ]
    Path(path).write_text("\n".join(lines))


if __name__ == "__main__":
    out = Path(__file__).with_name("output.txt")
    data = gen()
    write_output(data, out)
    print(f"written {out}")
    print(f"  N bits        = {data['N'].bit_length()}")
    print(f"  p bits        = {data['prime_bits']}")
    print(f"  p_high bits   = {data['p_high'].bit_length()}")
    print(f"  unknown bits  = {data['unknown_bits']}")
