#!/usr/bin/env sage
"""
Hollowed -- reference solution.

Strategy
========

The modulus is a three-prime RSA modulus, N = p * q * r, with the three
primes balanced (log_2 p ~ log_2 q ~ log_2 r ~ log_2(N) / 3).  The
player is handed the top 470 bits of p; the remaining 213 bits are
unknown.

Because p is a divisor of N of size p >= N^beta with beta = 1/3, we use
Coppersmith's theorem with that beta, not the usual beta = 1/2.  The
polynomial

    f(x) = p_high * 2^213 + x        (mod p)

has a small root x0 = (p mod 2^213).  Coppersmith's theorem lets us
recover it provided |x0| < N^(beta^2 - epsilon) = N^(1/9 - epsilon).

For our parameters,
        N^(1/9)      ~ 2^227.56
        bound on x0  = 2^213
        slack        ~ 14.5 bits

so epsilon must sit below about 14.5 / 2048 ~ 0.007.  The default
epsilon in Sage (beta / 7 ~ 0.0476) is therefore too large and the
attack silently fails.  Setting a tighter epsilon (and accepting the
larger lattice) is the whole game.

Once p is recovered, the flag is smaller than p, so we can decrypt
modulo p without ever factoring q * r:

        d_p = e^{-1}  mod (p - 1)
        m   = c^{d_p} mod p
"""

# -- load the public data ------------------------------------------------
exec(open("../challenge/output.txt").read()
     .replace("#", "##"))   # keep Sage happy with comment lines

assert prime_bits == 683
assert unknown_bits == 213
assert leak_bits == 470

# -- Coppersmith -------------------------------------------------------
P.<x> = PolynomialRing(Zmod(N))
f = (p_high << unknown_bits) + x
f = f.monic()

X = 2 ^ unknown_bits          # bound on the unknown low bits of p
beta = 1 / 3                  # because p ~ N^(1/3)
epsilon = 0.005               # tight: default beta/7 is too big here

roots = f.small_roots(X=X, beta=float(beta), epsilon=epsilon)
assert roots, "small_roots returned nothing -- tighten epsilon or enlarge m"

x0 = int(roots[0])
p = (int(p_high) << unknown_bits) + x0
assert N % p == 0, "recovered value is not a factor of N"
print(f"[+] recovered p = {p}")

# -- decrypt -----------------------------------------------------------
dp = inverse_mod(e, p - 1)
m = power_mod(c, dp, p)

from Crypto.Util.number import long_to_bytes   # available via sage -pip
flag = long_to_bytes(int(m))
print(f"[+] flag = {flag.decode()}")
