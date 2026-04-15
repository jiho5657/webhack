from Crypto.Util.number import getPrime, bytes_to_long
from pathlib import Path


PRIME_BITS = 683
UNKNOWN_BITS = 213
LEAK_BITS = PRIME_BITS - UNKNOWN_BITS
E = 65537

FLAG = b"MJSEC{c0pp3rsm1th_w1th_b3t4_0n3_th1rd_1s_th3_k3y_ad3f12}"


def gen():
    while True:
        p = getPrime(PRIME_BITS)
        q = getPrime(PRIME_BITS)
        r = getPrime(PRIME_BITS)
        if len({p, q, r}) == 3:
            break

    N = p * q * r
    m = bytes_to_long(FLAG)
    assert m < p
    c = pow(m, E, N)
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
