exec(open("../challenge/output.txt").read())

P.<x> = PolynomialRing(Zmod(N))
f = (p_high << unknown_bits) + x
f = f.monic()

X = 2 ^ unknown_bits
beta = 1 / 3
epsilon = 0.005

roots = f.small_roots(X=X, beta=float(beta), epsilon=epsilon)
assert roots

x0 = int(roots[0])
p = (int(p_high) << unknown_bits) + x0
assert N % p == 0
print(f"p = {p}")

dp = inverse_mod(e, p - 1)
m = power_mod(c, dp, p)

from Crypto.Util.number import long_to_bytes
flag = long_to_bytes(int(m))
print(f"flag = {flag.decode()}")
